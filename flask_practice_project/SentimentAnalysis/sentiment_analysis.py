# sentiment_analysis.py
"""
This module defines sentiment_analyzer(), which calls Watson NLP and returns a simple dict.
"""

import json
import requests

def sentiment_analyzer(text_to_analyse):
    """
    Returns a dict with keys:
      - label:   e.g. "document_sentiment_positive" or "ERROR_No Text Provided"
      - score:   float or None
      - error:   None or a short message
    """
    print(f"Received text_to_analyse: {text_to_analyse!r}")

    # 1) Empty‐input check
    if not text_to_analyse or text_to_analyse.strip() == "":
        return {
            "label": "ERROR_No Text Provided",
            "score": None,
            "error": "No text provided. Input text"
        }

    # 2) URL 
    url = (
        "https://sn-watson-sentiment-bert.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/SentimentPredict"
    )
    myobj = {"raw_document": {"text": text_to_analyse}}
    header = {
        "grpc-metadata-mm-model-id":
        "sentiment_aggregated-bert-workflow_lang_multi_stock"
    }

    # 3) Call Watson and bail on non‐200
    try:
        response = requests.post(url, json=myobj, headers=header, timeout=10)
    except requests.RequestException as e:
        print(f"Network/timeout error: {e}")
        return {"label": None, "score": None, "error": f"Request failed: {e}"}

    print("Response status code: ", response.status_code)
    if response.status_code != 200:
        print(f"Error with status code: {response.status_code}")
        return {
            "label": None,
            "score": None,
            "error": f"Service returned status code {response.status_code}"
        }

    # 4) Parse JSON and return
    try:
        data = response.json()
        label = data["documentSentiment"]["label"]
        score = data["documentSentiment"]["score"]
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return {"label": None, "score": None, "error": f"Unexpected response format: {e}"}

    return {"label": label, "score": score, "error": None}
