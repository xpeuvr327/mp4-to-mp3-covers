import ffmpeg
import os
import subprocess
import math
import sys
import argparse

def display_help():
    """Display the help message for the script."""
    help_message = """
Video to MP3 Converter with Album Art

Usage: python convert.py [options]

Options:
  --help              Display this help message
  --in FILENAME       Specify input video file (default: in.mp4)
  --time SECONDS      Duration per clip in seconds (default: 3)
  --album NAME        Album name for the MP3 metadata
  --artist NAME       Artist name for the MP3 metadata (default: xpeuvr327)
  --save-folder PATH  Create a new folder for output files

If no options are provided, the script will run in interactive mode.
"""
    print(help_message)

def get_total_frames(video_path):
    """
    Get the total number of frames in the video using ffprobe.
    """
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-count_packets',
        '-show_entries', 'stream=nb_read_packets',
        '-of', 'csv=p=0',
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    return int(result.stdout.strip())

def video_to_mp3_with_album_art(video_path, output_dir, seconds_per_file, album, artist):
    print('Starting...')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the duration and total frames of the video
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    total_frames = get_total_frames(video_path)
    
    # Calculate the total number of MP3 files
    total_clips = math.ceil(duration / seconds_per_file)
    
    # Create a list to store the MP3 files and screenshots
    mp3_files = []
    screenshot_files = []
    processed_clips = 0

    # Determine the number of digits needed for zero-padding
    num_digits = len(str(total_clips))

    # Loop through the video and create MP3 files and screenshots
    for i in range(total_clips):
        start_time = i * seconds_per_file
        end_time = (i + 1) * seconds_per_file

        # Create MP3 file with normalized naming (0001, 0002, etc.)
        clip_num = str(i+1).zfill(num_digits)
        mp3_filename = f"clip_{clip_num}.mp3"
        mp3_path = os.path.join(output_dir, mp3_filename)
        (
            ffmpeg
            .input(video_path, ss=start_time, to=end_time)
            .output(mp3_path, format='mp3')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        mp3_files.append(mp3_filename)

        # Create screenshot
        screenshot_filename = f"screenshot_{clip_num}.jpg"
        screenshot_path = os.path.join(output_dir, screenshot_filename)
        (
            ffmpeg
            .input(video_path, ss=start_time)
            .output(screenshot_path, vframes=1, format='image2')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        screenshot_files.append(screenshot_filename)

        # Update progress
        processed_clips += 1
        progress = (processed_clips / total_clips) * 100
        if progress % 10 <= (100 / total_clips):
            print(f"Progress: {int(progress)}%")

    print("Embedding metadata and album art...")

    # Embed album art and track number into the MP3 files using subprocess
    for idx, (mp3_file, screenshot_file) in enumerate(zip(mp3_files, screenshot_files)):
        mp3_path = os.path.join(output_dir, mp3_file)
        screenshot_path = os.path.join(output_dir, screenshot_file)
        output_mp3_path = os.path.join(output_dir, f"{os.path.splitext(mp3_file)[0]}_with_art.mp3")

        command = [
            'ffmpeg',
            '-i', mp3_path,
            '-i', screenshot_path,
            '-map', '0:0',
            '-map', '1:0',
            '-c', 'copy',
            '-id3v2_version', '3',
            '-metadata:s:v', 'title="Album cover"',
            '-metadata:s:v', 'comment="Cover (front)"',
            '-metadata', f'track={idx+1}/{len(mp3_files)}',
            '-metadata', f'album="{album}"',
            '-metadata', f'artist="{artist}"',
        ]

        command.append(output_mp3_path)

        # Suppress ffmpeg output
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Delete the original MP3 file without art
        os.remove(mp3_path)

        # Delete the screenshot file
        os.remove(screenshot_path)

    print("All files processed successfully.")
    return mp3_files, screenshot_files

def main():
    # Check if the script is being run directly (double-clicked)
    if len(sys.argv) <= 1 and os.name == 'nt' and not sys.stdin.isatty():
        print("WARNING: This script should be run from the command line.")
        print("Please open a command prompt and run: python convert.py")
        input("Press Enter to exit...")
        sys.exit(1)
        
    # Parse command line arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true', help='Display help message')
    parser.add_argument('--in', dest='input_file', help='Input video file')
    parser.add_argument('--time', type=int, help='Duration per clip in seconds')
    parser.add_argument('--album', help='Album name')
    parser.add_argument('--artist', help='Artist name')
    parser.add_argument('--save-folder', help='Output folder path')
    
    args, _ = parser.parse_known_args()
    
    # Display help if requested
    if args.help:
        display_help()
        sys.exit(0)
    
    # Interactive mode or command-line mode
    if args.input_file or args.time or args.album or args.artist or args.save_folder:
        # Command-line mode
        input_file = args.input_file if args.input_file else "in.mp4"
        seconds_per_file = args.time if args.time else 3
        album = args.album if args.album else "Unknown Album"
        artist = args.artist if args.artist else "xpeuvr327"
        output_dir = args.save_folder if args.save_folder else "."
    else:
        # Interactive mode
        input_file = "in.mp4"  # Default input file
        
        # Check if the default file exists
        if not os.path.exists(input_file):
            print(f"Error: Default input file '{input_file}' not found.")
            input_file = input("Enter video file path (or press Enter to exit): ")
            if not input_file:
                sys.exit(1)
            if not os.path.exists(input_file):
                print(f"Error: File '{input_file}' not found.")
                sys.exit(1)
        
        # Get album name
        album = input('Enter Album name: ')
        if not album:
            album = "Unknown Album"
        
        # Get duration per file
        duration_input = input('Enter duration per clip in seconds (default: 3): ')
        seconds_per_file = int(duration_input) if duration_input else 3
        
        # Get artist name
        artist_input = input('Enter Artist name (default: xpeuvr327): ')
        artist = artist_input if artist_input else "xpeuvr327"
        
        # Check if output should go to a new folder
        create_folder = input('Create a new folder for output? (y/n, default: n): ').lower()
        if create_folder == 'y':
            folder_name = input('Enter folder name: ')
            output_dir = folder_name
        else:
            output_dir = "."
    
    # Run the conversion
    try:
        print(f"Converting {input_file} to MP3 clips...")
        print(f"Album: {album}")
        print(f"Artist: {artist}")
        print(f"Duration per clip: {seconds_per_file} seconds")
        print(f"Output directory: {output_dir}")
        
        video_to_mp3_with_album_art(input_file, output_dir, seconds_per_file, album, artist)
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
