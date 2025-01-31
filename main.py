from sentence_transformers import SentenceTransformer
import json
import openai
import os
import discord
import time
import faiss

user_cooldowns = {}

openai.api_key = os.environ.get("OPENAI_API_KEY")
discord_bot_token = os.environ.get("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
messages = []

async def is_user_on_cooldown(user_id, message):
    if user_id in user_cooldowns and time.time() < user_cooldowns[user_id] and message.content.startswith("!question"):
        return True
    return False

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id

    if await is_user_on_cooldown(user_id, message):
        await message.channel.send("You’re on cooldown. Please wait a few seconds.")
        return

    user_cooldowns[user_id] = time.time() + 5

    print(message.content)
    if message.content.startswith("!question"):
        user_query = message.content[len("!question "):]
        closest_chunk = find_closest_chunk(user_query, index)
        response = gpt_response(user_query, closest_chunk, messages)
        await message.channel.send(response)


def find_closest_chunk(query, index):
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, 1)
    chunk = chunks[indices[0][0]]
    return chunk


def gpt_response(query, chunk, messages):
    messages.append({
        "role": "system",
        "content": f"The following is information from Roblox game Deepwoken: {chunk}",
    })
    messages.append({
        "role": "system",
        "content": "Your name is Jane Nalo, You are a Deepwoken expert assistant. Your knowledge spans lore,"
                   "gameplay  mechanics, combat strategies, builds, and exploration tips. Answer user queries clearly, "
                   "accurately, and in a friendly tone, helping players answer questions about popular Roblox game "
                   "Deepwoken. You base most, if not all answers from the relevant information you are provided. "
                   "If you do not know the answer to a question accurately, please do not make up anything and state "
                   "that you are unsure and to please restate the question in different terms. Make sure to keep the "
                   "answer concise, but informative. Keep the answers 170 tokens or less."
    })
    messages.append({"role": "user", "content": query})

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6,
        max_tokens=175,
    )

    assistant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_db.bin")

with open("chunks.json", "r") as f:
    chunks = json.load(f)

client.run(discord_bot_token)
