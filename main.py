import cv2
import dlib
import time

# путь к input video
video_path = 'input_files/input_video_5.mp4'
video_capture = cv2.VideoCapture(video_path)

# инициализация детектора лиц
detector = dlib.get_frontal_face_detector()

# получаем параметры для записи output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 24

output_path = 'output_files/output_video_5_1.mp4'

width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

start_time = time.time()  # время начала

while True:
    # читаем кадры из видео
    ret, frame = video_capture.read()

    if not ret:
        break

    # преобразование в монохром
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # обнаружение лиц
    rects = detector(gray, 0)

    # размываем лица
    for rect in rects:
        x_left = rect.left()
        y_top = rect.top()
        x_right = rect.right()
        y_bottom = rect.bottom()

        y_forehead = y_top + int(1/3*(y_top - y_bottom))
        # размытие области лица
        face_region = frame[y_forehead:y_bottom, x_left:x_right]

        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
        frame[y_forehead:y_bottom, x_left:x_right] = blurred_face

    # записываем обработанный кадр в output video
    out.write(frame)


# овобождаем ресурсы
video_capture.release()
out.release()
cv2.destroyAllWindows()

end_time = time.time()  # время окончания
processing_time = end_time - start_time  # Рассчитать время обработки

cv2.destroyAllWindows()
print(f"Время обработки видео: {processing_time:.2f} секунд")