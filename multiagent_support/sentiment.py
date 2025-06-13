from transformers import pipeline

_sentiment_pipeline = None

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return _sentiment_pipeline

def analyze_sentiment(text: str) -> str:
    pipe = get_sentiment_pipeline()
    result = pipe(text)
    label = result[0]["label"]
    return label.upper()