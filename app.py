from flask import Flask, request, send_from_directory, render_template, Response
import os
from main import process_video

app = Flask(__name__)

# Папки для сохранения загруженных и обработанных файлов
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


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
    processed_video_path = process_video(input_video_path)

    # Возвращаем вторую страницу успешной обработки
    return f"Video processed successfully: <a href='/outputs/{os.path.basename(processed_video_path)}'>Download Processed Video</a>", 200


# Кнопка загрузки видео
@app.route('/outputs/<filename>')
def processed_file(filename):
    response = send_from_directory(PROCESSED_FOLDER, filename, mimetype='video/mp4')
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


if __name__ == '__main__':
    app.run(debug=True)
