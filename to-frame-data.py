#!/usr/bin/env python

import os
import csv


def convert_lyrics_file_to_frame_data_file(lyrics_file, word_pause):
    lvg_frame_data_file = "%s.lvg" % (lyrics_file)
    lyric_lines = open(lyrics_file, encoding='utf-8').readlines()

    with open(lvg_frame_data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for lyric_line in lyric_lines:
            convert_lyric_line_to_frame_data_file(writer, lyric_line, word_pause)
    return lvg_frame_data_file

def convert_lyric_line_to_frame_data_file(writer, line, word_pause):
    for shabda in line.strip().split():
        line_list = [shabda, word_pause, ""]
        writer.writerow(line_list)
    # on decipher consecutive linebreak would mean explicit pagebreak
    writer.writerow(["", word_pause, "LINEBREAK"])


if __name__ == "__main__":
    lvg_data_dir = 'lvg-data'
    lvg_frame_data_file = os.path.join(lvg_data_dir, 'transcript.txt')
    default_word_pause_millisecond = '500'
    lvg_frame_data_file = convert_lyrics_file_to_frame_data_file(
        lvg_frame_data_file,
        default_word_pause_millisecond
    )
    print(lvg_frame_data_file)
