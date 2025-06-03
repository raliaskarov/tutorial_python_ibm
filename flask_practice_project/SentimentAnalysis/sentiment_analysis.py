"""
This module defines the sentiment_analyzer function, which sends a text string
to IBM Skills Network Watson NLP API to perform sentiment analysis and returns
the result.
"""

import json
import requests  # Import the requests library to handle HTTP requests

def sentiment_analyzer(text_to_analyse):
    """
    Analyzes the sentiment of the provided text using the Watson NLP API.

    Args:
        text_to_analyse (str): The text to be analyzed.

    Returns:
        dict: A dictionary containing sentiment 'label', 'score', and 'error' (if any).
    """

    if not text_to_analyse or text_to_analyse.strip() == "":
        return {"label": None, "score": None, "error": "No text provided. Input text"}

    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService\
        /SentimentPredict'  # URL of the sentiment analysis service
    myobj = { "raw_document":
            { "text": text_to_analyse } }  # Create a dictionary with the text to be analyzed

    # Set the headers required for the API request
    header = {"grpc-metadata-mm-model-id":
            "sentiment_aggregated-bert-workflow_lang_multi_stock"}

    # Send a POST request to the API with the text and headers
    response = requests.post(url,
                json = myobj, headers=header, timeout = 10)
    formatted_response = json.loads(response.text)

    res_status_code = response.status_code
    print("Response status code: ", res_status_code)

    output = {"label": None, "score": None}

    try:
        label = formatted_response['documentSentiment']['label']
        score = formatted_response['documentSentiment']['score']
        output["label"] = label
        output["score"] = score
    except (KeyError, TypeError) as e:
        print(f"Error parsing response: {e}")
        output["error"] = f"API returned status code: {e}"

    print(f"Returning output: {output}")
    return output
