# from groq import Groq
# from gtts import gTTS
# import os

# # Initialize Groq client
# client = Groq(
#     api_key='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',
# )

# # Make the chat request
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",  
#             "content": "Provide brief, concise, one-paragraph responses to all user queries.",
#         },
#         {
#             "role": "user",
#             "content": "write short notes on artificial intelligence",
#         }
#     ],
#     model="llama3-70b-8192",
#     max_tokens=150,
#     temperature=0.7,
# )

# # Extract the generated answer
# generated_answer = chat_completion.choices[0].message.content

# print(f"Generated Answer: {generated_answer}")

# # Convert the generated answer to speech and save it as an MP3 file
# gTTS(text=generated_answer, lang='en', slow=False).save("generated_answer.mp3")

# # Play the converted audio file (Windows-specific, use alternative for other OS)
# os.system("start generated_answer.mp3")  # Use "open" on macOS, or "mpg321" on Linux

# stream auaddio ------------------------------------------------------------------------------------------------     

# from groq import Groq
# from gtts import gTTS
# import sounddevice as sd
# import numpy as np
# import tempfile
# import wave

# # Initialize Groq client with API key
# client = Groq(
#     api_key='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',
# )

# # Make the chat request to Groq API
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",  
#             "content": "Provide brief, concise, one-paragraph responses to all user queries.",
#         },
#         {
#             "role": "user",
#             "content": "write short notes on artificial intelligence",
#         }
#     ],
#     model="llama3-70b-8192",
#     max_tokens=150,
#     temperature=0.7,
# )

# # Extract the generated answer from the response
# generated_answer = chat_completion.choices[0].message.content
# print(f"Generated Answer: {generated_answer}")

# # Convert the generated answer to speech using gTTS and save as MP3
# gTTS(text=generated_answer, lang='en', slow=False).save("generated_answer.mp3")

# # Convert MP3 file to WAV format using tempfile and pydub
# from pydub import AudioSegment

# # Load the MP3 file and speed it up
# audio = AudioSegment.from_mp3("generated_answer.mp3")
# speedup_audio = audio.speedup(playback_speed=1.2)  # Speed up by 1.5x

# # Save the fast audio as WAV (required for sounddevice playback)
# with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
#     temp_wav_file_name = temp_wav_file.name
#     speedup_audio.export(temp_wav_file_name, format="wav")

#     # Read the WAV file into a numpy array
#     with wave.open(temp_wav_file_name, 'rb') as f:
#         # Get audio file properties
#         framerate = f.getframerate()
#         num_frames = f.getnframes()

#         # Read audio frames
#         audio_data = np.frombuffer(f.readframes(num_frames), dtype=np.int16)

#     # Play the adjusted audio in real-time with sounddevice
#     sd.play(audio_data, samplerate=framerate)
#     sd.wait()  # Wait until the audio finishes playing



# Alternatively, if you are on a platform like Windows and want to use os.system for playback
# Uncomment this to play the generated MP3 directly
# os.system("start generated_answer.mp3")  # For Windows
# os.system("open generated_answer.mp3")   # For macOS
# os.system("mpg321 generated_answer.mp3") # For Linux


# user inputs ------------------------------------------------------------------------------------------------     



from gtts import gTTS
import sounddevice as sd
import numpy as np
import tempfile
import wave
from groq import Groq
from pydub import AudioSegment
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
api_key = os.getenv("MODEL_ID")
if not api_key:
    raise ValueError("ID key not found. Please set MODEL_ID in your .env file.")

# Initialize Groq client with API key
client = Groq(api_key=api_key)

# Ask the user for their input query
user_query = input("Please enter your query: ")

# Make the chat request to Groq API with the user's query
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",  
            "content": "Provide brief, concise, one-paragraph responses to all user queries.",
        },
        {
            "role": "user",
            "content": user_query,  # Use the user's input here
        }
    ],
    model="llama3-70b-8192",
    max_tokens=150,
    temperature=0.7,
)

# Extract the generated answer from the response
generated_answer = chat_completion.choices[0].message.content
print(f"Generated Answer: {generated_answer}")

# Convert the generated answer to speech using gTTS and save as MP3
gTTS(text=generated_answer, lang='en', slow=False).save("generated_answer.mp3")

# Load the MP3 file and speed it up using pydub
audio = AudioSegment.from_mp3("generated_answer.mp3")
speedup_audio = audio.speedup(playback_speed=1.2)  # Speed up by 1.2x (or change this value as needed)

# Save the fast audio as WAV (required for sounddevice playback)
with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
    temp_wav_file_name = temp_wav_file.name
    speedup_audio.export(temp_wav_file_name, format="wav")

    # Read the WAV file into a numpy array
    with wave.open(temp_wav_file_name, 'rb') as f:
        # Get audio file properties
        framerate = f.getframerate()
        num_frames = f.getnframes()

        # Read audio frames into a numpy array
        audio_data = np.frombuffer(f.readframes(num_frames), dtype=np.int16)

    # Play the adjusted audio in real-time with sounddevice
    sd.play(audio_data, samplerate=framerate)
    sd.wait()  # Wait until the audio finishes playing
    
    
# with streamlit interface ------------------------------------------------------------------------------------------------     


# import os
# import streamlit as st
# from gtts import gTTS
# import sounddevice as sd
# import numpy as np
# import tempfile
# import wave
# from groq import Groq
# from pydub import AudioSegment
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Retrieve API key from environment variable
# MODEL_ID = os.getenv("MODEL_ID")
# if not MODEL_ID:
#     raise ValueError("ID key not found. Please set MODEL_ID in your .env file.")

# # Initialize Groq client with API key
# client = Groq(api_key=MODEL_ID)

# # Streamlit Interface
# st.title("Chat and Listen to the Answer")

# # Ask the user for their input query
# user_query = st.text_input("Please enter your query:")

# # Function to play the audio
# def play_audio(generated_answer, speed_factor=1.2, lang='en'):
#     # Convert the generated answer to speech using gTTS and save as MP3
#     tts = gTTS(text=generated_answer, lang=lang, slow=False)
#     mp3_file = "generated_answer.mp3"
#     tts.save(mp3_file)

#     # Load the MP3 file and speed it up using pydub
#     audio = AudioSegment.from_mp3(mp3_file)
#     speedup_audio = audio.speedup(playback_speed=speed_factor)  # Speed up by 1.2x (or adjust as needed)

#     # Save the fast audio as WAV (required for sounddevice playback)
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
#         temp_wav_file_name = temp_wav_file.name
#         speedup_audio.export(temp_wav_file_name, format="wav")

#         # Read the WAV file into a numpy array
#         with wave.open(temp_wav_file_name, 'rb') as f:
#             # Get audio file properties
#             framerate = f.getframerate()
#             num_frames = f.getnframes()

#             # Read audio frames into a numpy array
#             audio_data = np.frombuffer(f.readframes(num_frames), dtype=np.int16)

#         # Play the adjusted audio in real-time with sounddevice
#         sd.play(audio_data, samplerate=framerate)
#         sd.wait()  # Wait until the audio finishes playing

#     # Optionally, remove the temporary MP3 and WAV files
#     os.remove(mp3_file)
#     os.remove(temp_wav_file_name)

# # Process the prompt when the user enters a query
# if user_query:
#     # Display a message saying it's processing
#     with st.spinner("Processing your query..."):
#         # Make the chat request to Groq API with the user's query
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",  
#                     "content": "Provide brief, concise, one-paragraph responses to all user queries.",
#                 },
#                 {
#                     "role": "user",
#                     "content": user_query,  # Use the user's input here
#                 }
#             ],
#             model="llama3-70b-8192",
#             max_tokens=150,
#             temperature=0.7,
#         )

#         # Extract the generated answer from the response
#         generated_answer = chat_completion.choices[0].message.content
#         st.write(f"Generated Answer: {generated_answer}")

#         # Play the audio of the answer
#         play_audio(generated_answer)

#         # Show the answer in an expandable section (Optional)
#         with st.expander("See full response"):
#             st.write(generated_answer)
