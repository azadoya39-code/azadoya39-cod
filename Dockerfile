# Используем легковесный образ Python 3.11-slim
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Запускаем бота через main.py
CMD ["python", "main.py"]