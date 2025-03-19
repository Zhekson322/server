# Используем официальный образ Python
FROM python:3.12-slim
# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем зависимости
COPY requirements.txt .
# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Команда для запуска приложения
CMD ["python","-u", "main.py"]