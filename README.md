# Video to MP3 Converter with Album Art (v2)

A command-line tool that extracts audio from videos, converts it to MP3 format, and automatically adds screenshots as album art.

## Features

- Extract audio clips from video files and convert them to MP3 format
- Automatically generate screenshots from the video to use as album art
- Embed metadata (album name, artist, track number) into MP3 files
- Normalized file naming with zero-padded numbers (0001, 0002, etc.)
- Flexible command-line options
- Interactive mode for ease of use

## Requirements

### FFmpeg

This project requires [FFmpeg](https://www.ffmpeg.org/) to be installed on your system.
- Windows users can install it via [Chocolatey](https://community.chocolatey.org/packages/ffmpeg-shared): `choco install ffmpeg-shared`

### Python Dependencies

Install the necessary Python libraries using pip:

```bash
pip install -r requirements.txt
```

Required packages:
- ffmpeg-python

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/xpeuvr327/mp4-to-mp3-covers
   cd mp4-to-mp3-covers
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode

Simply run the script without any parameters:

```bash
python convert.py
```

You'll be prompted to:
1. Enter the album name
2. Specify duration per clip (defaults to 3 seconds)
3. Enter the artist name (defaults to xpeuvr327)
4. Choose whether to create a new folder for output

### Command-Line Options

```bash
python convert.py [options]
```

Available options:
- `--help`: Display help message
- `--in FILENAME`: Specify input video file (default: in.mp4)
- `--time SECONDS`: Duration per clip in seconds (default: 3)
- `--album NAME`: Album name for the MP3 metadata
- `--artist NAME`: Artist name for the MP3 metadata (default: xpeuvr327)
- `--save-folder PATH`: Create a new folder for output files

### Examples

Basic usage with default settings:
```bash
python convert.py
```

Process a specific video with custom settings:
```bash
python convert.py --in myvideo.mp4 --album "My Album" --time 5 --artist "Artist Name"
```

Save output to a specific folder:
```bash
python convert.py --in video.mp4 --save-folder my_output_folder
```

## Output

The script generates MP3 files with embedded metadata and album art in the specified output directory:
- Files are named with zero-padded numbers based on the total number of clips (e.g., `clip_0001_with_art.mp3`)
- Each MP3 includes a screenshot from the corresponding segment of the video as album art
- Metadata includes album name, artist name, and track number

## Notes for Users

- If you double-click the script instead of running it from the command line, a warning will appear with instructions
- The script looks for a file named `in.mp4` in the current directory by default
- Temporary files are automatically deleted after processing

## iPod Usage Tips

These MP3 files work well with iTunes and can be synced to iPods:

1. Import the MP3 files into iTunes
2. Create a new playlist for the files
3. Select all files and enable "ignore on shuffle" (under the "playback" section)
   - This prevents the iPod from being unusable due to the large number of files

## Troubleshooting

- If the script fails with an error about missing libraries, make sure you've installed all requirements
- If FFmpeg isn't found, ensure it's installed and accessible in your system PATH
- For any other issues, check that your video file format is supported by FFmpeg
