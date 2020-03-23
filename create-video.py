#!/usr/bin/env python

import os
import cv2
import re
import sys
from PIL import Image


def frame_dir():
    try:
        return sys.argv[1]
    except:
        return os.getcwd()


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    source: https://stackoverflow.com/a/5967539
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def listframes(path_with_frames):
    _listframes = [img for img in os.listdir(path_with_frames)
                    if img.endswith(".jpg") or
                       img.endswith(".jpeg") or
                       img.endswith(".png")]
    _listframes.sort(key=natural_keys)
    return _listframes


def get_video_size(path_with_frames, list_of_frames):
    mean_height = 0
    mean_width = 0
    num_of_images = len(list_of_frames)

    for frame in list_of_frames:
        width, height = Image.open(os.path.join(path_with_frames, frame)).size
        mean_height += height
        mean_width += width

    mean_height /= num_of_images
    mean_width /= num_of_images
    return (int(mean_width), int(mean_height))


def resize_frames(path_with_frames, list_of_frames, size):
    for frame in list_of_frames:
        framepath = os.path.join(path_with_frames, frame)
        im = Image.open(framepath)

        imResize = im.resize(size, Image.ANTIALIAS)
        imResize.save(framepath, 'PNG', quality = 100) # setting quality
        # printing each resized image name
        print("resized:", frame)


def generate_video(path_with_frames, list_of_frames, video_file, size):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 1

    video = cv2.VideoWriter(video_file, fourcc, fps, size, True)

    for frame in list_of_frames:
        print("adding frame:", frame)
        framepath = os.path.join(path_with_frames, frame)
        video.write(cv2.imread(framepath))

    cv2.destroyAllWindows() # Deallocating memories taken for window creation
    video.release()  # releasing the video generated


video_name = '/tmp/mygeneratedvideo.avi'
path_with_frames = frame_dir()
all_frames = listframes(path_with_frames)
if all_frames == None or len(all_frames) == 0:
    print("found no frames at %s" % (path_with_frames))
    sys.exit(1)
video_size = get_video_size(path_with_frames, all_frames)
resize_frames(path_with_frames, all_frames, video_size)
generate_video(path_with_frames, all_frames, video_name, video_size)
