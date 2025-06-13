from transformers import pipeline

_gen = None

def get_gen():
    global _gen
    if _gen is None:
        _gen = pipeline("text-generation", model="gpt2", max_length=50)
    return _gen

def suggest_next_action(user_message: str) -> str:
    prompt = f"User said: '{user_message}'. Suggest a helpful next step:"
    gen = get_gen()
    suggestion = gen(prompt, max_length=50, num_return_sequences=1)
    return suggestion[0]['generated_text'].split("Suggest a helpful next step:")[-1].strip()