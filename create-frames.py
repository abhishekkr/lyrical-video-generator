#!/usr/bin/env python

import csv
import os
import re
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


def allowed_line_count(max_height, font, margin_top=10, line_gap=1, buffer=0):
    _, font_height = font.getsize('test !;qgp text')
    return int(max_height / (font_height + line_gap + buffer))


def create_frame(frame_index, for_millisec, lyric_list, shabda, font):
    lvg_frame_filepath = os.path.join(lvg_frames_dir, "lvg-%d.png" % (frame_index))
    canvas = Image.new('RGB', (FRAME_WIDTH, FRAME_HEIGHT), FRAME_BGCOLOR)
    draw = ImageDraw.Draw(canvas)
    line_gap = 5
    y_text = 10
    lines_to_use = allowed_line_count(FRAME_HEIGHT, font, y_text, line_gap)
    line_to_add_from = len(lyric_list) - lines_to_use

    shabda_width, shabda_height = font.getsize(" " + shabda + " ")

    for line in lyric_list[line_to_add_from:]:
        width, height = font.getsize(line)
        x_text = (FRAME_WIDTH - width) / 2
        if (width + shabda_width) < FRAME_WIDTH: x_text -= (shabda_width/2)
        draw.text(
            (x_text, y_text),
            line,
            fill=FRAME_TEXTCOLOR,
            font=font)
        y_text += height + line_gap

    x_text = 0
    if len(lyric_list) > 0:
        width, height = font.getsize(lyric_list[-1])
        x_shabda = (FRAME_WIDTH - shabda_width) / 2
        y_shabda = y_text
        if (width + shabda_width) < FRAME_WIDTH:
            x_shabda = ((FRAME_WIDTH - width) / 2) - (shabda_width/2) + width
            y_shabda -= (height + line_gap)
        draw.text(
            (x_shabda, y_shabda),
            " " + shabda,
            fill=FRAME_TEXTCOLOR_CURRENT,
            font=font)

    canvas.save(lvg_frame_filepath, "PNG")
    del draw
    del canvas



def text_wrap(text, font, max_width):
    """
    source: https://haptik.ai/tech/putting-text-on-images-using-python-part2/
    """
    margin_left_right = 10
    lines = []
    if (font.getsize(text)[0] + margin_left_right) <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and (font.getsize(line + words[i])[0] + margin_left_right) <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines


def csv_to_frames():
    default_font = ImageFont.truetype(default_font_path, 73, encoding="unic")
    os.makedirs(lvg_frames_dir, exist_ok=True)
    with open(lvg_frame_data_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        read_lyric = ""
        for row in csv_reader:
            frame_lyric = text_wrap(read_lyric, default_font, FRAME_WIDTH)
            print("%s\t'%s'" % (row[1], frame_lyric))
            create_frame(line_count, row[1], frame_lyric, row[0], default_font)
            read_lyric += " " + row[0]
            line_count += 1
        print('Processed %d lines.' % (line_count))


FRAME_WIDTH = 800
FRAME_HEIGHT = 600

FRAMES_PER_SECOND = 24  ## common across scripts
FRAME_BGCOLOR = (236, 128, 16) # dull orange
FRAME_TEXTCOLOR = (73, 73, 96) # muddy purple
FRAME_TEXTCOLOR_CURRENT = (64, 64, 255) # blue
FRAME_TEXTCOLOR_NEXT = (192, 192, 255) # light purple

default_font_path = fontspath['freeserf_bold']
lvg_data_dir = 'lvg-data'
lvg_frame_data_file = os.path.join(lvg_data_dir, 'transcript.txt.lvg')
lvg_frames_dir = os.path.join(lvg_data_dir, 'frames')
csv_to_frames()
