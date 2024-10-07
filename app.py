from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Создание папки, если она не существует


@app.route('/')
def upload_form():
    return render_template('index.html')  # Возвращаем HTML-форму для загрузки


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return "No video part", 400

    video = request.files['video']

    if video.filename == '':
        return "No selected video", 400

    # Сохраняем файл
    file_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(file_path)

    return f"Video uploaded successfully: <a href='/uploads/{video.filename}'>Download</a>", 200


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
