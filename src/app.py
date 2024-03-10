from flask import Flask, request, send_file
import tempfile
import os
from moviepy.editor import VideoFileClip
import uuid
from datetime import datetime
import threading
import time

app = Flask(__name__)


def generate_unique_filename():
    unique_id = uuid.uuid4()
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    unique_id_with_timestamp = f"{timestamp}-{unique_id}"
    return unique_id_with_timestamp


def validate_video_file(file):
    if file.filename == "":
        return False, "No file selected"

    if not file.filename.endswith(".mkv"):
        return False, "Only mkv files are supported"

    max_size = 100 * 1024 * 1024  # 100MB
    if request.content_length > max_size:
        return False, "File size exceeds the limit (100MB)"

    return True, ""


def cleanup_temp_files(video_path, audio_path, temp_dir):
    time.sleep(10)  # Wait for 10 seconds
    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)


@app.route("/convert", methods=["POST"])
def convert_video_to_audio():
    if "video" not in request.files:
        return "No file part", 400

    video_file = request.files["video"]

    is_valid, error_message = validate_video_file(video_file)
    if not is_valid:
        return error_message, 400

    output_filename = generate_unique_filename() + ".mp3"

    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, video_file.filename)
    video_file.save(video_path)

    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio_path = os.path.join(temp_dir, output_filename)
        audio.write_audiofile(audio_path)

        response = send_file(audio_path, as_attachment=True)

        cleanup_thread = threading.Thread(
            target=cleanup_temp_files, args=(video_path, audio_path, temp_dir)
        )
        cleanup_thread.start()

        return response
    except Exception as e:
        return f"Error converting file: {str(e)}", 500


if __name__ == "__main__":
    app.run()
