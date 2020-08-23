#!/usr/bin/env python

import pyttsx3
from gtts import gTTS
import os
import time


def create_audio_with_gtts(transcript_file, audio_file):
    file = open(transcript_file, "r").read().replace("[\n\r]", " ")
    language = 'en'
    print("creating audio file... started at %s:%s:%s" % (time.gmtime().tm_hour, time.gmtime().tm_min, time.gmtime().tm_sec))
    speech = gTTS(text = str(file), lang = language, slow = False)
    speech.save(audio_file)
    print("finshing at %s:%s:%s" % (time.gmtime().tm_hour, time.gmtime().tm_min, time.gmtime().tm_sec))

def print_english_voice_options_for_pyttsx3():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    idx = 0
    for voice in voices:
        if voice.id != "english":
            continue
        print("Voice: #%s" % (idx))
        print(" - ID: %s" % voice.id)
        print(" - Name: %s" % voice.name)
        print(" - Languages: %s" % voice.languages)
        print(" - Gender: %s" % voice.gender)
        print(" - Age: %s" % voice.age)
        idx += 1
    del voices
    del engine

def create_audio_with_pyttsx3(transcript_file, audio_file):
    text = str(open(transcript_file, "r").read().replace("\n", " ").replace('"', ''))
    print("creating audio file... started at %s:%s:%s" % (time.gmtime().tm_hour, time.gmtime().tm_min, time.gmtime().tm_sec))
    ## word
    engine = pyttsx3.init()
    print(text)
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    print("finshing at %s:%s:%s" % (time.gmtime().tm_hour, time.gmtime().tm_min, time.gmtime().tm_sec))

def create_audio(transcript_file, audio_file):
    # current just default to one
    create_audio_with_pyttsx3(transcript_file, audio_file)


if __name__ == '__main__':
    import sys
    TRANSCRIPT_FILE = "lvg-data/transcript.txt"
    AUDIO_FILE = "/tmp/my_generated_audio.mp3"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--show-pyttsx3-english-voices":
            print_english_voice_options_for_pyttsx3()
            sys.exit(0)
        TRANSCRIPT_FILE = sys.argv[1]
        if len(sys.argv) > 2:
            AUDIO_FILE = sys.argv[2]
    create_audio(TRANSCRIPT_FILE, AUDIO_FILE)
