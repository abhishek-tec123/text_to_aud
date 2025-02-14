from fastapi import FastAPI
from pydantic import BaseModel
import pyttsx3
import uvicorn

app = FastAPI()

class SpeechRequest(BaseModel):
    text: str
    voice_id: str = "com.apple.speech.synthesis.voice.samantha"
    rate: int = 150
    volume: float = 0.5

def text_to_speech(text: str, voice_id: str, rate: int, volume: float):
    """Convert text to speech with given parameters."""
    engine = pyttsx3.init()

    # Set voice
    engine.setProperty('voice', voice_id)

    # Adjust speaking rate & volume
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

@app.post("/speak/")
async def speak(request: SpeechRequest):
    """API endpoint to convert text to speech."""
    try:
        text_to_speech(request.text, request.voice_id, request.rate, request.volume)
        return {"message": "Speech synthesis completed successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/voice_list/")
async def list_voices():
    """API endpoint to list available voices."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return [{"index": i, "name": voice.name, "id": voice.id} for i, voice in enumerate(voices)]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
