import os
import zipfile
import subprocess
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import ffmpeg
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['OUTPUT_FOLDER'] = './output'

socketio = SocketIO(app)  # Initialize Flask-SocketIO

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def video_to_mp3_with_album_art(video_path, output_dir, seconds_per_file=3, album=""):
    # Get video duration and total frames
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    total_frames = int(next((s for s in probe['streams'] if s['codec_type'] == 'video'), {}).get('nb_frames', 0))

    mp3_files = []
    screenshot_files = []

    processed_frames = 0

    for i in range(int(duration // seconds_per_file)):
        start_time = i * seconds_per_file
        mp3_filename = f"clip_{i+1}.mp3"
        screenshot_filename = f"screenshot_{i+1}.jpg"
        mp3_path = os.path.join(output_dir, mp3_filename)
        screenshot_path = os.path.join(output_dir, screenshot_filename)

        # Extract MP3
        ffmpeg.input(video_path, ss=start_time, t=seconds_per_file).output(mp3_path, format='mp3').run(overwrite_output=True)

        # Take screenshot
        ffmpeg.input(video_path, ss=start_time).output(screenshot_path, vframes=1, format='image2').run(overwrite_output=True)

        mp3_files.append(mp3_path)
        screenshot_files.append(screenshot_path)

        # Simulate processed frames based on time
        processed_frames += int((seconds_per_file / duration) * total_frames)

        # Emit progress update
        progress_percent = min(100, int((processed_frames / total_frames) * 100))
        socketio.emit('progress', {'progress': progress_percent})

    # Embed album art
    output_files = []
    for idx, (mp3_path, screenshot_path) in enumerate(zip(mp3_files, screenshot_files)):
        output_mp3_path = os.path.join(output_dir, f"clip_{idx+1}_with_art.mp3")
        command = [
            'ffmpeg',
            '-i', os.path.abspath(mp3_path),
            '-i', os.path.abspath(screenshot_path),
            '-map', '0:0',
            '-map', '1:0',
            '-c', 'copy',
            '-id3v2_version', '3',
            '-metadata:s:v', 'title=Album cover',
            '-metadata:s:v', 'comment=Cover (front)',
            '-metadata', f'track={idx+1}/{len(mp3_files)}',
            '-metadata', f'album={album}'
        ]
        command.append(output_mp3_path)
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        output_files.append(output_mp3_path)

    return output_files

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'album' not in request.form:
        return jsonify({"error": "Missing file or album metadata"}), 400

    file = request.files['file']
    album = request.form['album']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(video_path)

    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], os.path.splitext(filename)[0])
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Process the video to generate MP3 files
        mp3_files = video_to_mp3_with_album_art(video_path, output_dir, seconds_per_file=3, album=album)

        # Create a ZIP file with all MP3 files
        zip_filename = f"{os.path.splitext(filename)[0]}.zip"
        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in mp3_files:
                zipf.write(file, os.path.basename(file))
                os.remove(file)  # Cleanup final MP3

        os.remove(video_path)  # Cleanup uploaded video
        return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name=zip_filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Cleanup uploads and outputs on startup
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    app.run(debug=True)
