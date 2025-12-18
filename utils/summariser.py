
# utils/summariser.py
import os
import requests
from django.conf import settings

# Hugging Face API router endpoint
API_URL = "https://router.huggingface.co/hf-inference/models/csebuetnlp/mT5_multilingual_XLSum"
def chunk_text(text, max_chars=3500):
    """
    Split long text into smaller chunks safe for Hugging Face summarization.
    Each chunk will be at most max_chars characters.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end
    return chunks

def get_book_summary(text, max_length=150):
    if not text or len(text.strip()) < 50:
        return "No Summary Available"

    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json"
    }

    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks[:5]:  # limit to first 5 chunks to avoid timeouts
        payload = {
            "inputs": chunk,
            "parameters": {
                "max_length": max_length,
                "min_length": 40,
                "do_sample": False
            }
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

            if response.status_code != 200:
                print("HF ERROR:", response.status_code, response.text)
                continue

            result = response.json()
            if isinstance(result, list) and "summary_text" in result[0]:
                summaries.append(result[0]["summary_text"])

        except Exception as e:
            print("HF EXCEPTION:", e)
            continue

    if not summaries:
        return "No Summary Available"

    return " ".join(summaries)
