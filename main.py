from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room
import os  # Импортируем модуль для работы с переменными окружения

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Храним комнаты и их участников
rooms = {
    "один": set(),
    "два": set()
}

@socketio.on('connect') #обработка подключения клиента
def handle_connect():
    print(f'Client connected: {request.sid}')
    socketio.emit('rooms_list', list(rooms.keys()), room=request.sid) #отправляет список комнат клиенту

@socketio.on('join') #обработка присоединения к комнате
def handle_join(data):
    room = data.get('room')
    if room in rooms:
        leave_current_room(request.sid)
        join_room(room)
        rooms[room].add(request.sid)
        print(f'Client {request.sid} joined room {room}')

def leave_current_room(sid):
    for room in rooms:
        if sid in rooms[room]:
            leave_room(room)
            rooms[room].remove(sid)
            print(f'Client {sid} left room {room}')
            break

@socketio.on('message')
def handle_message(data):
    room = data.get('room')
    message = data.get('message')
    if room in rooms and request.sid in rooms[room]:
        print(f'Message in {room}: {message}')
        socketio.emit('message', 
            {'message': message, 'sender': request.sid}, 
            room=room
        )


if __name__ == '__main__':
    # Получаем хост из переменной окружения HOST, если не задан - используем 0.0.0.0
    host = os.getenv('HOST', '0.0.0.0')
    socketio.run(app, host=host, port=5000)