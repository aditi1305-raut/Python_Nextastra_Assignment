# backend/utils.py
from gtts import gTTS
import tempfile
import os

def text_to_speech(text: str):
    tts = gTTS(text=text, lang="en")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name

# Very simple stub: returns a placeholder transcription
def transcribe_audio_stub(path):
    # For a quick prototype we just return a placeholder
    return "Transcription placeholder (replace with OpenAI/Whisper for real STT)."
