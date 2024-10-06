import cv2
import dlib

# Укажите путь к вашему видеофайлу
video_path = 'input_files/input_video_1.mp4'
video_capture = cv2.VideoCapture(video_path)

# Инициализация детектора лиц
detector = dlib.get_frontal_face_detector()

# Получаем параметры для записи выходного видео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 24

output_path = 'output_files/output_video.mp4'

width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

while True:
    # Захват кадра из видео
    ret, frame = video_capture.read()

    # Если кадры закончились, выйдите из цикла
    if not ret:
        break

    # Преобразование в градации серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Обнаружение лиц
    rects = detector(gray, 0)

    # Размываем лица
    for rect in rects:
        x = rect.left()
        y = rect.top()
        x1 = rect.right()
        y1 = rect.bottom()

        # Размытие области лица
        face_region = frame[y:y1, x:x1]
        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
        frame[y:y1, x:x1] = blurred_face

    # Запись обработанного кадра в выходное видео
    out.write(frame)


# Освобождение ресурсов
video_capture.release()
out.release()
cv2.destroyAllWindows()