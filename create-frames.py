#!/usr/bin/env python

import os
import csv
import textwrap
from PIL import Image, ImageDraw, ImageFont


fontspath = {
    'freesans': '/usr/share/fonts/gnu-free/FreeSans.ttf',
    'freesans_bold': '/usr/share/fonts/gnu-free/FreeSansBold.ttf',
    'freeserif': '/usr/share/fonts/gnu-free/FreeSerif.ttf',
    'freeserf_bold': '/usr/share/fonts/gnu-free/FreeSerifBold.ttf',
    'freemono': '/usr/share/fonts/gnu-free/FreeMonoBold.ttf',
    'freemono_bold': '/usr/share/fonts/gnu-free/FreeMono.ttf',
    'caladea': '/usr/share/fonts/google-crosextra-caladea/Caladea-Regular.ttf',
    'caladea_bold': '/usr/share/fonts/google-crosextra-caladea/Caladea-Bold.ttf',
    'caladea_italic': '/usr/share/fonts/google-crosextra-caladea/Caladea-Italic.ttf',
    'caladea_bold_italic': '/usr/share/fonts/google-crosextra-caladea/Caladea-BoldItalic.ttf',
    'carterone': '/usr/share/fonts/carterone/CarterOne.ttf',
    'montserrat_black_italic': '/usr/share/fonts/julietaula-montserrat/Montserrat-BlackItalic.otf',
    'noto_sans_black': '/usr/share/fonts/google-noto/NotoSans-Black.ttf',
}


def allowed_line_count(max_height, font, line_gap=10, buffer=2):
    _, font_height = font.getsize('test !;qgp text')
    return int(max_height / (font_height + line_gap + buffer))


def create_frame(frame_index, lyric_list, font):
    lvg_frame_filepath = os.path.join(lvg_frames_dir, "lvg-%d.png" % (frame_index))
    frame_width = 800
    frame_height = 600
    text_color = 'blue'
    canvas = Image.new('RGB', (frame_width, frame_height), "orange")
    draw = ImageDraw.Draw(canvas)
    y_text = 10
    lines_to_use = allowed_line_count(frame_height, font, y_text)
    line_to_add_from = len(lyric_list) - lines_to_use
    for line in lyric_list[line_to_add_from:]:
        width, height = font.getsize(line)
        draw.text(
            ((frame_width - width) / 2, y_text),
            line,
            fill=text_color,
            font=font,
            align ="left")
        y_text += height
    canvas.save(lvg_frame_filepath, "PNG")
    del draw
    del canvas


default_font_path = fontspath['freeserf_bold']
default_font = ImageFont.truetype(default_font_path, 43, encoding="unic")
lvg_data_dir = 'lvg-data'
lvg_frame_data_file = os.path.join(lvg_data_dir, 'transcript.txt.lvg')
lvg_frames_dir = os.path.join(lvg_data_dir, 'frames')
os.makedirs(lvg_frames_dir, exist_ok=True)
with open(lvg_frame_data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    read_lyric = ""
    for row in csv_reader:
        frame_lyric = textwrap.wrap(read_lyric, width=25)
        print("%s\t'%s'" % (row[1], frame_lyric))
        create_frame(line_count, frame_lyric, default_font)
        read_lyric += " " + row[0]
        line_count += 1
    print('Processed %d lines.' % (line_count))
