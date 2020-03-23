## lyrical-video-generator

> to generate a lyrical video from provided audio file

### Utilities | **WIP**

* [transcribe.py](transcribe.py) to convert `lvg-data/transcription/transcript.mp3` into text at `lvg-data/transcript.txt`

* [to-frame-data.py](to-frame-data.py) to convert transcription `lvg-data/transcript.txt` into frame data input file `lvg-data/transcript.txt.lvg` for next step

* [create-frames.py](create-frames.py) to create frames based on `lvg-data/transcript.txt.lvg`

* [create-video.py](create-video.py) to create video `/tmp/mygeneratedvideo.avi` from frame files at `lvg-data/frames`

---



