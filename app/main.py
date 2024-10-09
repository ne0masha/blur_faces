import os
import cv2
import mediapipe as mp
import numpy as np


def process_img(img, face_detection):
    H, W, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x_min, y_min, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

            x_min = int(x_min * W)
            y_min = int(y_min * H)
            w = int(w * W)
            h = int(h * H)

            # Увеличиваем высоту размываемого фрагмента на 1/3 для лба
            additional_height = int(h / 3)
            y_min = max(0, y_min - additional_height)  # y_min не выходит за пределы изображения
            h += additional_height  # Увеличиваем высоту

            # Рассчитываем центр и размеры овала
            center_x = x_min + w // 2
            center_y = y_min + h // 2
            axes = (w // 2, h // 2)  # Полуоси овала

            # Создаем маску овала
            mask = np.zeros_like(img, dtype=np.uint8)
            cv2.ellipse(mask, (center_x, center_y), axes, 0, 0, 360, (255, 255, 255), -1)  # Белый овал на черном фоне

            # Размываем область, соответствующую овалу
            blurred_face = cv2.GaussianBlur(img, (75, 75),0)
            img = np.where(mask == 255, blurred_face, img)  # Заменяем область овала на размытое изображение

    return img


def process_video(input_video_path):
    output_dir = 'outputs'  # Папка для сохранения обработанного видео
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Инициализируем средства детекции лиц
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.1) as face_detection:
        cap = cv2.VideoCapture(input_video_path)

        # Проверка на корректность открытия видео
        if not cap.isOpened():
            raise Exception(f"Ошибка открытия видеофайла: {input_video_path}")

        ret, frame = cap.read()
        if not ret:
            raise Exception(f"Ошибка чтения первого кадра видео: {input_video_path}")

        output_video_path = os.path.join(output_dir, 'output_video.mp4')
        output_video = cv2.VideoWriter(output_video_path,
                                       cv2.VideoWriter_fourcc(*'MP4V'),
                                       25,
                                       (frame.shape[1], frame.shape[0]))

        while ret:
            frame = process_img(frame, face_detection)
            output_video.write(frame)
            ret, frame = cap.read()

        cap.release()
        output_video.release()

    return output_video_path  # Возвращаем путь к обработанному видео, чтобы app нормально отработал