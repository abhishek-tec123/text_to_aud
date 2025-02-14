# from gtts import gTTS
# import sounddevice as sd
# import numpy as np
# import tempfile
# import wave
# from pydub import AudioSegment
# import os

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


import pyttsx3

def text_to_speech(text, voice_id="com.apple.speech.synthesis.voice.samantha", rate=150, volume=0.5):

    engine = pyttsx3.init()

    # Set voice if provided
    if voice_id:
        engine.setProperty('voice', voice_id)

    # Adjust speaking rate & volume
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

# List available voices
def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.name} ({voice.id})")

# Example Usage
if __name__ == "__main__":
    # list_voices()  # Show available voices
    user_text = input("Enter text to convert to speech: ")
    text_to_speech(user_text)


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
