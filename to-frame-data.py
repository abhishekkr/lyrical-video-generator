#!/usr/bin/env python

import os
import csv


def convert_lyrics_file_to_frame_data_file(lyrics_file, word_pause):
    lvg_frame_data_file = "%s.lvg" % (lyrics_file)
    lyrics = open(lyrics_file, encoding='utf-8').read()

    with open(lvg_frame_data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for shabda in lyrics.strip().split():
            writer.writerow([shabda, word_pause])
    return lvg_frame_data_file


lvg_data_dir = 'lvg-data'
lvg_frame_data_file = os.path.join(lvg_data_dir, 'transcript.txt')
default_word_pause_millisecond = '500'
lvg_frame_data_file = convert_lyrics_file_to_frame_data_file(
    lvg_frame_data_file,
    default_word_pause_millisecond
)
print(lvg_frame_data_file)
