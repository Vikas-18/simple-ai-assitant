
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

def get_cosine_similarity(embedding1, embedding2):
    dot_product = np.dot(embedding1, embedding2)
    magnitude1 = np.linalg.norm(embedding1)
    magnitude2 = np.linalg.norm(embedding2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


text1 = "This is leetcode problem text"
text2 = "dsa is a way to solve leetcode problems"
text3 = "i love apples"

embedding1 = get_embedding(text1)
embedding2 = get_embedding(text2)
similarity1 = get_cosine_similarity(embedding1, embedding2)
print(f"Cosine similarity between text1 and text2: {similarity1}")

embedding3 = get_embedding(text3)
similarity2 = get_cosine_similarity(embedding1, embedding3)
print(f"Cosine similarity between text1 and text3: {similarity2}")
