# server.py
'''
Simple Flask wrapper around sentiment_analyzer.
'''
from flask import Flask, render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

app = Flask("Sentiment Analyzer")

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    text_to_analyze = request.args.get("textToAnalyze")

    # 1) If the query param is empty or whitespace → 400 + “String empty…”
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "String empty, please provide text", 400

    # 2) Call the analyzer
    response = sentiment_analyzer(text_to_analyze)

    # 3) If analyzer returned an “error” field, show that
    if response.get("error"):
        # If it was exactly “No text provided. Input text” it won’t reach here,
        # because we already checked for empty above.
        return f"Error: {response['error']}", 400

    # 4) If label is still None → “meaningless/unparsable”
    if response["label"] is None:
        return "Please enter meaningful sentence", 400

    # 5) Otherwise we have a valid label like “documentSentiment_positive”
    #    or “documentSentiment_negative”. Split off the part after underscore.
    #    (If your actual label format is “positive” you can adjust accordingly.)
    sentiment = response["label"].split("_")[-1]
    score = response["score"]
    return f"Text sentiment: {sentiment}\nScore: {score}"

@app.route("/")
def render_index_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
