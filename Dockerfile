# Используем официальный образ Python
FROM python:3.12-slim

# Указываем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем все файлы в контейнер
COPY . .

# Указываем команду для запуска
CMD ["python", "main.py"]
