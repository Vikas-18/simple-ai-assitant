# get vector embedding

from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np


load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def get_embedding(text):
    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=text
    )
    return response.data[0].embedding
