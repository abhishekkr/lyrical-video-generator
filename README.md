## lyrical-video-generator

> to generate a lyrical video from provided audio file or text file

### Usage

* syntax: `./tasks.sh <help|dep|txt-to-vid|t2v|frame-n-vid|fnv|dataframes|frames|vid|transcribe>`

* hard-coded path as of now (WIP for config)

> * base data dir at './lvg-data'
>
> * dir for audio files at './lvg-data/transcription'
>
> * mp3 audio file used as input at './lvg-data/transcription/transcript.mp3'
>
> * transcripted text file from audio at 'lvg-data/transcript.txt'
>
> * dataframe file created from text file at './lvg-data/transcript.txt.lvg'
>
> * image frames created from dataframes at './lvg-data/frames'
>
> * video name = '/tmp/mygeneratedvideo.avi'

* Parameters Help

> * dep: to install pip dependencies
>
> * transcribe: to convert audio file to text
>
> * dataframes: convert available transcription/text to input data format for create-frame
>
> * frames: to create frame images for video from dataframes
>
> * vid: to create video from existing frames
>
> * tnv (or txt-to-vid): to run all commands from creating dataframes to creating video (if uou have text file)
>
> * fnv (or frame-n-vid): to create frame images and video from it

### Utilities

* [transcribe.py](transcribe.py) to convert `lvg-data/transcription/transcript.mp3` into text at `lvg-data/transcript.txt`

* [to-frame-data.py](to-frame-data.py) to convert transcription `lvg-data/transcript.txt` into frame data input file `lvg-data/transcript.txt.lvg` for next step

* [create-frames.py](create-frames.py) to create frames based on `lvg-data/transcript.txt.lvg`

* [create-video.py](create-video.py) to create video `/tmp/mygeneratedvideo.avi` from frame files at `lvg-data/frames`

---



