import cv2
import mediapipe as mp

# Инициализация необходимых модулей MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Установка параметров видео
input_video_path = 'input_files/input_video_3.mp4'
output_video_path = 'output_files/output_video.mp4'

# Захват видео
cap = cv2.VideoCapture(input_video_path)

# Получение параметров оригинального видео
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Инициализация VideoWriter для записи выходного видео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Выбираем кодек
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Инициализация Face Mesh
with mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1) as face_mesh:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Конвертация в RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        # Если обнаружены лица, рисуем на кадре
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)

        # Записываем обработанный кадр в выходное видео
        out.write(frame)

        # # Показ видео (можно убрать или закомментировать)
        # cv2.imshow('Face Mesh', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

# Освобождение ресурсов
cap.release()
out.release()
cv2.destroyAllWindows()
