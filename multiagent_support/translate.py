from transformers import pipeline
from langdetect import detect as lang_detect

_translation_pipes = {}

def get_translate_pipeline(src_lang="en", tgt_lang="en"):
    key = (src_lang, tgt_lang)
    if key not in _translation_pipes:
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
        _translation_pipes[key] = pipeline("translation", model=model_name)
    return _translation_pipes[key]

def translate_text(text, src_lang="en", tgt_lang="en"):
    if src_lang == tgt_lang:
        return text
    try:
        pipe = get_translate_pipeline(src_lang, tgt_lang)
        return pipe(text)[0]['translation_text']
    except Exception:
        return text

def detect(text):
    try:
        return lang_detect(text)
    except Exception:
        return "en"