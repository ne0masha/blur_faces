from flask import Flask, request, send_from_directory, render_template, Response, url_for
import os
from main import process_video

app = Flask(__name__)

# Папки для сохранения загруженных и обработанных файлов
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/')
def upload_form():
    return render_template('index.html')  # Возвращаем HTML-шаблон для загрузки


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return "No video part", 400

    video = request.files['video']

    if video.filename == '':
        return "No selected video", 400

    # Сохраняем файл
    input_video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(input_video_path)

    # Обрабатываем видео
    processed_video_path = process_video(
        input_video_path)  # Предполагается, что эта функция возвращает путь к обработанному файлу

    # Генерируем URL для скачивания обработанного видео
    video_filename = os.path.basename(processed_video_path)
    video_url = url_for('output_file', filename=video_filename)

    # Возвращаем страницу успеха
    return render_template('success.html', video_url=video_url)


@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
