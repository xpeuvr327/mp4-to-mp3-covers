# Video to MP3 Converter with Album Art

This repository contains two tools for converting video files into MP3 clips with embedded album art:
1. A **command-line script** for developers and power users.
2. A **web-based application** for a more user-friendly experience.

Both tools use FFmpeg for video and audio processing.

---

## Features

- Extracts audio clips from video files and converts them to MP3 format.
- Automatically generates screenshots from the video to use as album art.
- Embeds metadata (album name, track number) into MP3 files.

### Command-Line Script:
- Ideal for automation and integration into other workflows.
- Allows customization of clip duration and metadata directly in the script.

### Web Application:
- Simple and intuitive interface accessible via a web browser.
- Real-time progress tracking with WebSockets (broken ): )
- Outputs a ZIP archive of processed MP3 files.

---

## Requirements

1. **Python**: Version 3.7 or higher.
2. **FFmpeg**: Installed and added to your system's PATH.
   - Test installation:
     ```bash
     ffmpeg -version
     ```
3. (**Web** only)
```
Flask
flask_socketio
werkzeug
zipfile
```

### Python Libraries:
Install the necessary dependencies using `pip`:
```bash
pip install -r requirements.txt
```


## Installation

### For Both Tools:
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/video-to-mp3-album-art
   cd video-to-mp3-album-art
   ```

### For Command-Line Script:
- Ensure FFmpeg is installed.
- The script is ready to run without additional setup.

### For Web Application:
- Install the required Python libraries:
  ```bash
  pip install flask flask_socketio werkzeug zipfile
  ```

---

## Usage Instructions

### Command-Line Script:
1. Place the script and video file in the same directory.
2. Run the script:
   ```bash
   python script_name.py
   ```
3. Enter the album name when prompted.
4. MP3 files with album art will be saved in the output directory.

#### Example Workflow:
- Input: `in.mp4`
- Processing:
  - Extracts MP3 clips of 3 seconds each.
  - Takes screenshots from the video for album art.
- Output:
  - `clip_1_with_art.mp3`
  - `clip_2_with_art.mp3`

### Web Application:
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```
3. Upload a video file and enter the album name.
4. Download the processed ZIP file containing MP3 clips.

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

---

## Customization

### Clip Duration:
- Modify the `seconds_per_file` parameter in both tools to change the duration of each MP3 clip.

### Metadata:
- Customize fields like `album` and `track` in the script or web app for personalized output.

---

## Deployment (Web Application)

### Development:
1. Start the server locally:
   ```bash
   python app.py
   ```

### Production:
1. Use Gunicorn for deployment:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
2. Set up a reverse proxy with NGINX for scalability and security.

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
