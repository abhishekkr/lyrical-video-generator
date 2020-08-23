#!/usr/bin/env python

import speech_recognition as sr
import os
from pydub import AudioSegment


def transcribe_sound(sound_file, lyrics_file):
    wav_file = sound_file + ".wav"
    file_extension = os.path.basename(sound_file).split('.')[1]
    # convert mp3 file to wav
    sound = AudioSegment.from_file(sound_file, file_extension)
    sound.export(wav_file, format="wav")
    transcribe_wav(wav_file, lyrics_file)
    os.remove(wav_file)


def transcribe_wav(wav_file, lyrics_file):
    # use the audio file as the audio source
    r = sr.Recognizer()
    lyrics = ''
    with sr.AudioFile(wav_file) as source:
        audio = r.record(source)
    lyrics += r.recognize_google(audio)
    print(lyrics)
    with open(lyrics_file, 'w') as f:
        f.write(lyrics)


if __name__ == "__main__":
    lvg_data_dir = 'lvg-data'
    lvg_data_transcript_dir = os.path.join(lvg_data_dir, 'transcription')
    mp3_file = os.path.join(lvg_data_transcript_dir, "transcript.mp3")
    wav_file = os.path.join(lvg_data_transcript_dir, "transcript.wav")
    lyrics_file = 'lvg-data/transcript.txt'
    os.makedirs(lvg_data_transcript_dir, exist_ok=True)
    transcribe_sound(mp3_file, lyrics_file)
