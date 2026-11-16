"""
BEGINNER NOTES: edge-tts + pydub + ffmpeg
=========================================
This file is for learning, not for your finished lesson exporter.

What each tool does:
- edge-tts: turns TEXT into a spoken MP3 (text-to-speech).
- pydub: loads audio, adds pauses, and stitches clips together.
- ffmpeg: the engine that actually reads/writes many audio formats.
  pydub uses ffmpeg in the background when you export.

Install once (in your virtual environment):
    pip install edge-tts pydub

You also need ffmpeg installed on your computer.
On Ubuntu/WSL:
    sudo apt install ffmpeg
Check it works:
    ffmpeg -version
"""

# ---------------------------------------------------------------------------
# 1) edge-tts: generate speech from text
# ---------------------------------------------------------------------------
# Communicate() is the main class.
#   text  = the words you want spoken
#   voice = which speaker to use
#
# save_sync() downloads the audio and writes it to a file.
# "sync" means: wait until the file is finished, then continue.
# That is easier for beginners than async/await.

import edge_tts

english_text = "I decided to study Japanese."
japanese_text = "日本語を勉強することにしました。"

# A few useful voice names:
#   English: en-US-JennyNeural
#   Japanese: ja-JP-NanamiNeural
english_voice = "en-US-JennyNeural"
japanese_voice = "ja-JP-NanamiNeural"

# Make two short speech files.
edge_tts.Communicate(english_text, english_voice).save_sync("english.mp3")
edge_tts.Communicate(japanese_text, japanese_voice).save_sync("japanese.mp3")

# Optional: speak a little slower or faster.
# Rate is a percent string, like "-10%" (slower) or "+20%" (faster).
# edge_tts.Communicate(japanese_text, japanese_voice, rate="-10%").save_sync("japanese_slow.mp3")


# ---------------------------------------------------------------------------
# 2) pydub: load audio, add pauses, combine clips
# ---------------------------------------------------------------------------
# AudioSegment is pydub's name for "one piece of audio".
# You can:
#   - load a file
#   - make silence (a pause)
#   - glue pieces together with +
#   - export the result

from pydub import AudioSegment

# Load the MP3 files we just made.
english = AudioSegment.from_file("english.mp3")
japanese = AudioSegment.from_file("japanese.mp3")

# Make silent pauses. The number is milliseconds.
# 1000 milliseconds = 1 second.
pause_short = AudioSegment.silent(duration=800)   # 0.8 seconds
pause_long = AudioSegment.silent(duration=2000)   # 2 seconds

# Glue pieces in order: English, pause, Japanese, longer pause.
# The + sign means "play this, then that".
lesson = english + pause_short + japanese + pause_long

# You can also stack several clips in a list, then join them:
# parts = [english, pause_short, japanese, pause_long]
# lesson = sum(parts)


# ---------------------------------------------------------------------------
# 3) ffmpeg: export / convert the finished audio
# ---------------------------------------------------------------------------
# You usually do not call ffmpeg yourself.
# pydub.export() finds ffmpeg and uses it to write the file.
#
# format="mp3"  -> compressed, small file, good for listening
# format="wav"  -> uncompressed, larger file, easy to edit later

lesson.export("lesson.mp3", format="mp3")
lesson.export("lesson.wav", format="wav")

# If you want to run ffmpeg yourself (same idea, different style):
# This example converts lesson.wav to a smaller mp3 from the command line.
import subprocess

subprocess.run(
    [
        "ffmpeg",
        "-y",              # overwrite the output file if it already exists
        "-i", "lesson.wav",  # -i means "input file"
        "-codec:a", "libmp3lame",  # use the mp3 encoder
        "-qscale:a", "4",  # quality: lower number = better quality
        "lesson_ffmpeg.mp3",
    ],
    check=True,
)

# Other beginner ffmpeg commands you can type in the terminal:
#   ffmpeg -i lesson.mp3 lesson.wav          convert mp3 -> wav
#   ffmpeg -i lesson.wav -ar 44100 out.wav   set sample rate to 44100 Hz
#   ffmpeg -i lesson.mp3 -ss 0 -t 5 clip.mp3 keep the first 5 seconds
#     -ss = start time in seconds
#     -t  = how many seconds to keep


# ---------------------------------------------------------------------------
# Tiny recap
# ---------------------------------------------------------------------------
# 1. edge-tts writes spoken MP3 files from your phrase text.
# 2. pydub loads those files, inserts silence, and concatenates them.
# 3. export() (or ffmpeg) saves the finished lesson as mp3 or wav.
print("Done. Listen to lesson.mp3")
