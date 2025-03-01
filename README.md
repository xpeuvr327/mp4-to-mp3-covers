# Video to MP3 Converter with Album Art

This repo contains two tools: convert.py and app.py

---

## Features

- Extracts audio clips from video files and converts them to MP3 format.
- Automatically generates screenshots from the video to use as album art.
- Embeds metadata (album name, track number) into MP3 files.

---

## Requirements

1. **FFmpeg**: [website](https://www.ffmpeg.org/), tested with [choco](https://community.chocolatey.org/packages/ffmpeg-shared)
2. (**Web** only) python packages: (are in requirements.txt)
```
Flask
flask_socketio
werkzeug
zipfile
```
note: if you have any error like `X library missing`, install it with `pip install <whatever>`, or google it.
### Python Libraries:
Install the necessary dependencies using `pip`:
```bash
pip install -r requirements.txt
```


## Installation

### For Both Tools:
1. Clone this repository:
   ```bash
   git clone https://github.com/xpeuvr327/mp4-to-mp3-covers
   cd mp4-to-mp3-covers
   ```
---

## Usage Instructions

### Command-Line Script:
1. Place the script and a video file named "in.mp4" in the same directory.
2. Run the script:
   ```bash
   python .\convert.py
   ```
3. Enter the album name when prompted.
4. wait a while. if it seems like the ui is stuck at "starting...", check the dir in the explorer if a lot of files are being generated. your cpu fans should begin to spin too.
4. MP3 files with album art will be saved in the output directory.

#### Example:
- Input: `in.mp4`
- Processing:
  - Extracts MP3 clips of 3 seconds each. //todo: use input() instead of hardcoded
  - Takes screenshots from the video for album art.
- Output:
  - `clip_1_with_art.mp3`
  - `clip_2_with_art.mp3`
  - ...

### Web Application:
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```
3. Upload a video file (**without any spaces**)and enter the album name.
4. Download the processed ZIP file containing MP3 clips. You can also find it under the output folder.

---

## Output Files

### Command-Line Script:
- Individual MP3 files with embedded album art.
- Each clip is named as:
  - `clip_1_with_art.mp3`
  - `clip_2_with_art.mp3`

### Web Application:
- ZIP archive containing all MP3 clips:
  - `clip_1_with_art.mp3`
  - `clip_2_with_art.mp3`
- inside the app.py folder, a `output` subfolder containing the results

---

## Customization

### Clip Duration:
- Modify the `seconds_per_file` parameter in both tools to change the duration of each MP3 clip.

### Metadata:
- Customize fields like `album` and `artist` in the script or web app for personalized output.

---

## what can i do with these files?  

you can play them inside iTunes, which works great, but NOT vlc, since it seems like it uses the first file's thumbnail  

if you want to put these on an iPod (the device for which i created this tool)
you can playback video on a gen7 iPod by following these steps:
with the clip_1_with_art.mp3 files, move them into a new playlist on iTunes, then select them all, and enable "ignore on shuffle" (under the "playback" section), which isn't mandatory but it prevents the iPod from being unusable due to the excessive numbers of files created. for youtube videos i'd recommend downloading them in 360p or 240p (since the iPod's resolution is 240p apparently, and most yt-downloaders cap to 360, then the next lowest quality option is often 144p, but it's really up to you), and the only downside is that since most videos are 16:9, you will get a black bezel on the top and right. the total output files are generally not that big, around 18.9mb for a 18 min 240p with 3s/files and around 450 files. the copy process to the iPod can be long tho, due to, not the file sizes, but the files count.

---

## Notes

### Temporary Files:
- Both tools delete temporary files (e.g., screenshots, intermediate MP3s) after processing to save space.

### SEO Keywords:
- **Command-Line Script**:
  - Python video to MP3 script
  - Embed album art in MP3 Python
  - Extract audio from video FFmpeg
- **Web Application**:
  - Web-based video to MP3 converter
  - Flask MP3 conversion app
  - MP3 generator with screenshots

---

This repository provides versatile solutions for converting videos to MP3 clips with embedded album art, catering to developers and general users alike.
