import streamlit as st
from pydub import AudioSegment
from pydub.playback import play
import bleep as bl
import ffmpeg

st.title("Bleep words/phrases from any audio")

uploaded_file = st.file_uploader("Choose an audio file",type = [".wav",".wave",".ogg",".mp3",".flac"])

text = st.text_input("Enter words or phrases you want to censor/bleep:")

if uploaded_file is not None and text is not None:
    audio = AudioSegment.from_ogg(uploaded_file)

    r_audio = bl.get_bleeped_audio(audio,text)

    r_audio.export('bleep_audio.wav', format='wav')

