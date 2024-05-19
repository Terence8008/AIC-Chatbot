# Getting response
import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "Can you recommend a good destination for Winter holidays?",
})

print(output)