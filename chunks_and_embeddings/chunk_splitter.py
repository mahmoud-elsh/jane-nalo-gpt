from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import json


def get_pdf_text(pdf):
    text = ""
    reader = PdfReader(pdf)
    for page in reader.pages:
        text += page.extract_text().strip().replace("\n", " ")
    return text


def get_text_chunks(text):
    split = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 100,
    )
    return split.create_documents([text])


def create_vector_embeddings():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("chunks.json", "r") as file:
        chunks = json.load(file)

    embeddings = model.encode(chunks)

    np.save("embeddings.npy", embeddings)


input = "output2.pdf"
text = get_pdf_text(input)
chunks = get_text_chunks(text)

with open("chunks.json", "w") as file:
    json.dump([chunk.page_content for chunk in chunks], file)

create_vector_embeddings()
