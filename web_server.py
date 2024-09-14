from flask import Flask
import threading
import asyncio
from app import main  # Импортируем вашу основную функцию

app = Flask(__name__)

@app.route('/')
def home():
    return "Tournament is running!"

def start_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    threading.Thread(target=start_flask).start()

    # Запустим ваш основной турнирный процесс
    asyncio.run(main())
