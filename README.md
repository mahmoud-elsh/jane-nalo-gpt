# JaneNalo-GPT
An AI-powered discord bot for popular Roblox game <a href="https://www.roblox.com/games/4111023553/Deepwoken-WORLD-EVENTS">Deepwoken</a> using vector embeddings constructed from a parsed <a href="https://deepwoken.fandom.com/wiki/Deepwoken_Wiki">Deepwoken Wiki<a>.
# Features
- Ask Deepwoken related questions in any Discord channel using the "!question" prefix
- Uses related information from the Deepwoken Wiki and GPT-4's chat completion to answer user queries
# Installation
**Discord Bot Application Required**
- Register an application from https://discord.com/developers/applications and invite to desired server
<hr>

To run the project on your local machine:
### Step 1: Clone the Repository
```
git clone https://github.com/mahmoud-elsh/jane-nalo-gpt.git
cd jane-nalo-gpt
```
### Step 2: Setup Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```
### Step 3: Install Dependencies
```
pip install -r requirements.txt
```
### Step 4: Run Required Files
```
cd parser
python parse_script.py
```
*Move output2.pdf to chunks_and_embeddings directory*
```
cd chunks_and_embeddings
python chunk_splitter.py
```
*Move embeddings.npy to main directory*
### Step 5: Run Main File
*Put the required discord bot token and OpenAi API key in .env file or in IDE of your choice*
```
python main.py
```
### Step 6: Access the Bot
Ask desired questions using "!question" prefix.
