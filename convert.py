import ffmpeg
import os
import subprocess
x=input('Enter Album: ')
def video_to_mp3_with_album_art(video_path, output_dir, seconds_per_file=2, album=x):
    print('starting...')
    # Get the duration of the video
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])

    # Create a list to store the MP3 files and screenshots
    mp3_files = []
    screenshot_files = []

    # Loop through the video and create MP3 files and screenshots
    for i in range(int(duration // seconds_per_file)):
        start_time = i * seconds_per_file
        end_time = (i + 1) * seconds_per_file

        # Create MP3 file
        mp3_filename = f"clip_{i+1}.mp3"
        mp3_path = os.path.join(output_dir, mp3_filename)
        (
            ffmpeg
            .input(video_path, ss=start_time, to=end_time)
            .output(mp3_path, format='mp3')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        mp3_files.append(mp3_filename)

        # Create screenshot
        screenshot_filename = f"screenshot_{i+1}.jpg"
        screenshot_path = os.path.join(output_dir, screenshot_filename)
        (
            ffmpeg
            .input(video_path, ss=start_time)
            .output(screenshot_path, vframes=1, format='image2')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        screenshot_files.append(screenshot_filename)

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
        ]

        command.append(output_mp3_path)

        # Suppress ffmpeg output
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Delete the original MP3 file without art
        os.remove(mp3_path)

        # Delete the screenshot file
        os.remove(screenshot_path)

    return mp3_files, screenshot_files

# Example usage
video_path = "in.mp4"
output_dir = "."
seconds_per_file = 3  # adjust this value as needed
mp3_files, screenshot_files = video_to_mp3_with_album_art(video_path, output_dir, seconds_per_file, x)
print("Done.")
