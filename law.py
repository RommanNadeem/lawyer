
from openai import OpenAI
import streamlit as st
from moviepy import AudioFileClip
import tempfile
import os




client = OpenAI(
  api_key= os.getenv("OPENAI_KEY")
)


def transcribe(file_path):

    chunk = open(file_path, "rb")
    resp = client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file= chunk,
        prompt=(
        "Transcribe the audio into English only, "
        "Translate to english"
        "don't use non-Roman characters or Urdu script."
        )
    )
    content = resp.text

    return content




st.title("Audio Transcription with OpenAI")

# Upload audio file
audio_file = st.file_uploader("Upload your audio file", type=["mp3", "m4a", "wav"])


if audio_file is not None:
    st.audio(audio_file, format="audio/mp3")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_file.getbuffer())
        tmp_audio_path = tmp_file.name

    audio_clip = AudioFileClip(tmp_audio_path)
    duration = audio_clip.duration  # Get the duration of the audio
    # MoviePy v2.x: method is now `subclipped`, not `subclip`
    duration = audio_clip.duration                 # total length in seconds
    quarter = duration / 3

    quarter = duration / 3
    first_quarter = audio_clip.subclipped(0, quarter)
    second_quarter = audio_clip.subclipped(quarter, 2 * quarter)
    third_quarter = audio_clip.subclipped(2 * quarter, duration)

    chunk3_path = None
    with st.spinner("Creating audio chunks... Please wait!"):
            while chunk3_path is None:
    # Save the chunks as temporary files
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as chunk1:
                    first_quarter.write_audiofile(chunk1.name)
                    chunk1_path = chunk1.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as chunk2:
                    second_quarter.write_audiofile(chunk2.name)
                    chunk2_path = chunk2.name
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as chunk3:
                    third_quarter.write_audiofile(chunk3.name)
                    chunk3_path = chunk3.name

    transcript1 = None
    transcript2 = None
    transcript3 = None


    with st.spinner("Transcribing audio chunks... Please wait!"):
            while transcript3 is None:
                # Simulating the transcription process
                transcript1 = transcribe(chunk1_path)
                transcript2 = transcribe(chunk2_path)
                transcript3 = transcribe(chunk3_path)
        
        # Combine the results and show the transcription
    final_transcript = transcript1 + "\n\n" + transcript2 + "\n\n" + transcript3
    st.text_area("Transcription", final_transcript, height=300)
        
        # Process the uploaded audio file and display the transcription

    os.remove(tmp_audio_path)
    os.remove(chunk1_path)
    os.remove(chunk2_path)
    os.remove(chunk3_path)




# chunk22 = audio_file = open("chunk22.mp3", "rb")
# resp = client.audio.transcriptions.create(
#     model="gpt-4o-transcribe",
#     file= chunk22,
#     prompt=(
#     "Please transcribe the audio into English only, "
#     "translate to english "
#     "don't use non-Roman characters or Urdu script."
#     )
# )
# content = resp.text 

# print(content)


