#!/usr/bin/env bash

dependencies(){
  echo "[+] installing/upgrading dependency packages"

  pip install --upgrade \
    pyyaml \
    SpeechRecognition \
    pydub \
    Pillow \
    opencv-python
}

case $1 in
  dep*)
    dependencies
    ;;
  dataframes)
    python to-frame-data.py
    ;;
  txt-to-vid|t2v)
    set -ex
    python to-frame-data.py
    python create-frames.py
    python create-video.py ${PWD}/lvg-data/frames
    set +ex
    ;;
  frames)
    python create-frames.py
    ;;
  frame-n-vid|fnv)
    set -ex
    python create-frames.py
    python create-video.py ${PWD}/lvg-data/frames
    set +ex
    ;;
  vid)
    python create-video.py ${PWD}/lvg-data/frames
    ;;
  **)
    echo "unknown option: ${1:-empty_parameter_set}"
    echo "usage: $0 <dep|txt-to-vid|t2v|frame-n-vid|fnv|dataframes|frames|vid>"
    echo ""
    echo "Parameters Help"
    echo "* dep: to install pip dependencies"
    echo "* dataframes: convert available transcription/text to input data format for create-frame"
    echo "* frames: to create frame images for video from dataframes"
    echo "* vid: to create video from existing frames"
    echo "* tnv (or txt-to-vid): to run all commands from creating dataframes to creating video"
    echo "* fnv (or frame-n-vid): to create frame images and video from it"
    exit 123
    ;;
esac
