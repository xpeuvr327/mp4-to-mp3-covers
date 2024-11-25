from flask import Flask, request, jsonify, send_file, render_template
import os
import ffmpeg
import subprocess
import zipfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['OUTPUT_FOLDER'] = './output'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

#modify seconds_per_file to the framerate 1/x you want

def video_to_mp3_with_album_art(video_path, output_dir, seconds_per_file=2):
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])

    # Create a list to store the MP3 files
    mp3_files = []
    screenshot_files = []

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
            .run(overwrite_output=True)
        )
        mp3_files.append(mp3_path)

        # Create screenshot
        screenshot_filename = f"screenshot_{i+1}.jpg"
        screenshot_path = os.path.join(output_dir, screenshot_filename)
        (
            ffmpeg
            .input(video_path, ss=start_time)
            .output(screenshot_path, vframes=1, format='image2')
            .run(overwrite_output=True)
        )
        screenshot_files.append(screenshot_path)

    # Embed album art and track number into MP3 files
    output_files = []
    for idx, (mp3_path, screenshot_path) in enumerate(zip(mp3_files, screenshot_files)):
        output_mp3_path = os.path.join(output_dir, f"clip_{idx+1}_with_art.mp3")

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
            output_mp3_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        output_files.append(output_mp3_path)

        os.remove(mp3_path)  # Clean up original MP3
        os.remove(screenshot_path)  # Clean up screenshot

    return output_files

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(video_path)

    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], os.path.splitext(filename)[0])
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Process video and create MP3s with album art
        mp3_files = video_to_mp3_with_album_art(video_path, output_dir)
        zip_filename = f"{os.path.splitext(filename)[0]}.zip"
        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)

        # Create a zip file
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in mp3_files:
                zipf.write(file, os.path.basename(file))
                os.remove(file)  # Clean up processed MP3

        os.remove(video_path)  # Clean up uploaded video
        return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name=zip_filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
