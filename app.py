import streamlit as st
from pydub import AudioSegment
from pydub.playback import play
import bleep as bl
import ffmpeg
from tempfile import NamedTemporaryFile

st.title("Bleep words/phrases from any audio")

uploaded_file = st.file_uploader("Choose an audio file",type = ["wav"])

text = st.text_input("Enter words or phrases you want to censor/bleep:")

btn = st.button("Censor")

if btn:
    if uploaded_file is not None:
        with NamedTemporaryFile(suffix=".wav") as temp:
            temp.write(uploaded_file.getvalue())
            temp.seek(0)
            a = AudioSegment.from_file(file=temp.name)
            r_audio = bl.get_bleeped_audio(uploaded_file,text,a)
            example = r_audio.export()
            st.audio(example.read())
    


