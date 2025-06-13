import speech_recognition as sr
from gtts import gTTS
import os

def speech_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    return r.recognize_google(audio)

def text_to_speech(text, lang="en", filename="output.mp3", play_audio=True):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    if play_audio:
        try:
            os.system(f"mpg123 {filename}")
        except Exception:
            pass
    return filename