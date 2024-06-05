from openai import OpenAI
import os
from pydub import AudioSegment
from pydub.playback import play
import streamlit as st
import google.generativeai as genai

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])

def getTranscript(audio_file):
    client = OpenAI()

    transcription =  client.audio.transcriptions.create(
                model="whisper-1", # specifies the model to be used for transcription
                response_format="verbose_json", # indicates that the response should be in a detailed JSON format.
                timestamp_granularities=["word"], # requests that timestamps be provided for each word in the transcription, which allows for precise tracking of when each word occurs in the audio
                file=audio_file,
            )
    return transcription

def getBlockedWords(text,btext):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(btext+f"from the following text:{text}")
    return response.text

def configureBlocked(text):
    words = [] # store blocked words
    sentance = [] # store blocked phrases 
    blockedWords = text.split('\n') # split the response above 

    for index in range(len(blockedWords)):
        word = blockedWords[index]
        word = word.replace("*","")
        word = word.strip()
        arr = word.split(" ")
        if index > 0 and word != '' and len(arr) == 1:
            words.append(word)
        if index > 0 and word != '' and len(arr) > 1:
            sentance.append(word)

    return words,sentance

def blockingWords(dictWords,words):
    for dic in dictWords:
        if dic['word']  in words:
            dic['word'] = '*'

    return dictWords

def blockingSentance(dictWords,sentance):
    for s in sentance:
        arr = s.split(" ")
        end = 0
        i = 0
        j = 0
        while end < len(arr) and j<len(dictWords):
            if dictWords[j]['word'].lower() ==  arr[i].lower():
                dictWords[j]['word'] = '*'
                end = end + 1
                i = i + 1
            j = j + 1

    return dictWords

def createAudio(audio,dictWords):
    blp = AudioSegment.from_file("resource/censor-beep-01.mp3")
    bleeped_audio = AudioSegment.silent(duration=0)

    for dc in dictWords:
        if dc['word'] == "*":
            bleeped_audio += blp
        else:
             word_audio = audio[float(dc['start'])*1000:float(dc['end'])*1000]
             bleeped_audio = bleeped_audio + word_audio

    return bleeped_audio

def get_bleeped_audio(audio,btext):
    transcription = getTranscript(audio)

    blockedWords = getBlockedWords(transcription.text,btext)

    words, sentance = configureBlocked(blockedWords)

    dictWords = blockingWords(transcription.words,words)

    dictWords = blockingSentance(dictWords,sentance)

    return createAudio(audio,dictWords)







    



