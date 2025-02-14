# from gtts import gTTS
# import sounddevice as sd
# import numpy as np
# import tempfile
# import wave
# from pydub import AudioSegment
# import os
# # from gtts.lang import tts_langs

# # print(tts_langs())

# def text_to_speech_stream(text, lang="en", speedup=1.2):

#     try:
#         # Generate speech and save as MP3
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
#             temp_mp3_name = temp_mp3.name
#             gTTS(text=text, lang=lang, slow=False).save(temp_mp3_name)

#         # Load the MP3 and speed it up
#         audio = AudioSegment.from_mp3(temp_mp3_name)
#         speedup_audio = audio.speedup(playback_speed=speedup)

#         # Convert to WAV (required for sounddevice playback)
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
#             temp_wav_name = temp_wav.name
#             speedup_audio.export(temp_wav_name, format="wav")

#             # Read WAV file into numpy array
#             with wave.open(temp_wav_name, 'rb') as f:
#                 framerate = f.getframerate()
#                 num_frames = f.getnframes()
#                 audio_data = np.frombuffer(f.readframes(num_frames), dtype=np.int16)

#             # Play the processed audio
#             sd.play(audio_data, samplerate=framerate)
#             sd.wait()  # Wait until playback is complete

#         # Clean up temporary files
#         os.remove(temp_mp3_name)
#         os.remove(temp_wav_name)

#     except Exception as e:
#         print(f"Error: {e}")

# # Example Usage
# user_text = input("Enter the text to convert to speech: ")
# text_to_speech_stream(user_text)



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gtts import gTTS
import sounddevice as sd
import numpy as np
import tempfile
import wave
from pydub import AudioSegment
import os
import uvicorn

# Create FastAPI app
app = FastAPI()

# Request body structure for text and speed
class TextToSpeechRequest(BaseModel):
    text: str
    speed: float = 1.2  # Default speed is 1.2

def text_to_speech_stream(text, lang="en", speedup=1.2):
    try:
        # Generate speech and save as MP3
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
            temp_mp3_name = temp_mp3.name
            gTTS(text=text, lang=lang, slow=False).save(temp_mp3_name)

        # Load the MP3 and speed it up
        audio = AudioSegment.from_mp3(temp_mp3_name)
        speedup_audio = audio.speedup(playback_speed=speedup)

        # Convert to WAV (required for sounddevice playback)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            temp_wav_name = temp_wav.name
            speedup_audio.export(temp_wav_name, format="wav")

            # Read WAV file into numpy array
            with wave.open(temp_wav_name, 'rb') as f:
                framerate = f.getframerate()
                num_frames = f.getnframes()
                audio_data = np.frombuffer(f.readframes(num_frames), dtype=np.int16)

            # Play the processed audio
            sd.play(audio_data, samplerate=framerate)
            sd.wait()  # Wait until playback is complete

        # Clean up temporary files
        os.remove(temp_mp3_name)
        os.remove(temp_wav_name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speak/")
async def convert_text_to_speech(request: TextToSpeechRequest):
    try:
        # Default language is "en" if not provided in the payload
        text_to_speech_stream(request.text, lang="en", speedup=request.speed)
        return {"message": "Text-to-speech conversion completed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# If this script is run directly, launch the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
