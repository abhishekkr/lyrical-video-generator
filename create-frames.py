#!/usr/bin/env python

import csv
import math
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


def last_line_y(current_y, font_height):
    return current_y - (font_height + DEFAULT_LINE_GAP)


def next_line_y(current_y, font_height):
    return current_y + font_height + DEFAULT_LINE_GAP


def line_x(line_width, shabda_width):
    x_text = (FRAME_WIDTH - line_width) / 2
    if (line_width + shabda_width) < FRAME_WIDTH: x_text -= (shabda_width/2)
    return x_text


def next_word_coordinates(line, shabda, y_text, font):
    line_width, line_height = font.getsize(line)
    shabda_width, _ = font.getsize(' ' + shabda)
    x_text = line_x(line_width, shabda_width)
    x_shabda = (FRAME_WIDTH - shabda_width) / 2
    y_shabda = y_text
    if (x_text + line_width + shabda_width + MARGIN_LEFT_RIGHT) < FRAME_WIDTH:
        x_shabda = x_text + line_width
        y_shabda = last_line_y(y_text, line_height)
    return (x_shabda, y_shabda)


def allowed_line_count(max_height, font, margin_top=10, buffer=0):
    _, font_height = font.getsize('test !;qgp text')
    return int(max_height / (next_line_y(0, font_height) + buffer))


def draw_read_line(canvas, lyric_line, y_text, font, shabda_width=0):
    draw = ImageDraw.Draw(canvas)
    line_width, line_height = font.getsize(lyric_line)
    x_text = line_x(line_width, shabda_width)
    draw.text(
        (x_text, y_text),
        lyric_line,
        fill=FRAME_TEXTCOLOR,
        font=font)
    y_text = next_line_y(y_text, line_height)
    del draw
    return y_text


def draw_next_word(canvas, last_line, shabda, x_coordinates, font, color):
    print("last line: %s" % (last_line))
    print("shabda: %s" % (shabda))
    print("x: %s" % str(x_coordinates))
    print("----------------------------")
    draw = ImageDraw.Draw(canvas)
    draw.text(
        x_coordinates,
        ' ' + shabda,
        fill=color,
        font=font)
    del draw


def save_image_times(canvas, frame_index, times, subindex=0):
    for idx in range(0,times):
        lvg_frame_filepath = os.path.join(lvg_frames_dir, "lvg-%d-%d.png" % (frame_index, subindex))
        subindex += 1
        canvas.save(lvg_frame_filepath, "PNG")
    return subindex


def create_frame_shabda(canvas, frame_index, y_text, for_millisec, line, shabda, font):
    x_coordinates = next_word_coordinates(line, shabda, y_text, font)

    if len(line) > 0:
        draw_next_word(canvas, line, shabda, x_coordinates, font, FRAME_TEXTCOLOR_NEXT)

    frames_count = math.ceil(FRAMES_PER_SECOND * (int(for_millisec)/1000))
    subindex = 0
    if len(shabda) < 1:
        subindex = save_image_times(canvas, frame_index, frames_count, subindex)
    if len(shabda) < 2:
        subindex = save_image_times(canvas, frame_index, frames_count/2, subindex)
        draw_next_word(canvas, line, shabda, x_coordinates, font, FRAME_TEXTCOLOR_CURRENT)
        subindex = save_image_times(canvas, frame_index, frames_count/2, subindex)
    elif len(shabda) == 2:
        subindex = save_image_times(canvas, frame_index, int(frames_count/3), subindex)
        draw_next_word(canvas, line, shabda[0], x_coordinates, font, FRAME_TEXTCOLOR_CURRENT)
        subindex = save_image_times(canvas, frame_index, int(frames_count/3), subindex)
        draw_next_word(canvas, line, shabda, x_coordinates, font, FRAME_TEXTCOLOR_CURRENT)
        subindex = save_image_times(canvas, frame_index, int(frames_count/3), subindex)
    else:
        token_size = math.ceil(len(shabda) / 3)
        subindex = save_image_times(canvas, frame_index, int(frames_count/4), subindex)
        draw_next_word(canvas, line, shabda[:(token_size)], x_coordinates, font, FRAME_TEXTCOLOR_CURRENT)
        subindex = save_image_times(canvas, frame_index, int(frames_count/4), subindex)
        draw_next_word(canvas, line, shabda[:(token_size*2)], x_coordinates, font, FRAME_TEXTCOLOR_CURRENT)
        subindex = save_image_times(canvas, frame_index, int(frames_count/4), subindex)
        draw_next_word(canvas, line, shabda, x_coordinates, font, FRAME_TEXTCOLOR_CURRENT)
        subindex = save_image_times(canvas, frame_index, int(frames_count/4), subindex)


def create_frame(frame_index, for_millisec, lyric_list, shabda, font):
    canvas = Image.new('RGB', (FRAME_WIDTH, FRAME_HEIGHT), FRAME_BGCOLOR)
    y_text = 10
    lines_to_use = allowed_line_count(FRAME_HEIGHT, font, y_text)
    line_to_add_from = len(lyric_list) - lines_to_use

    shabda_width, _ = font.getsize(" " + shabda)

    lines_already_read = lyric_list[line_to_add_from:-1]
    line_currently_read = lyric_list[-1]

    for line in lines_already_read:
        y_text = draw_read_line(canvas, line, y_text, font)
        print("~", line)

    y_text = draw_read_line(canvas, line_currently_read, y_text, font, shabda_width)

    create_frame_shabda(canvas, frame_index, y_text, for_millisec, line_currently_read, shabda, font)
    # cleaning up to avoid corrupted memory errors
    del canvas


def text_wrap(text, font, max_width):
    """
    source: https://haptik.ai/tech/putting-text-on-images-using-python-part2/
    """
    lines = []
    if (font.getsize(text)[0] + (2*MARGIN_LEFT_RIGHT)) <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and (font.getsize(line + words[i])[0] + (2*MARGIN_LEFT_RIGHT)) <= max_width:
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
MARGIN_LEFT_RIGHT = 15
DEFAULT_LINE_GAP = 10

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
