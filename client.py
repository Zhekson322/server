import socketio
import threading

sio = socketio.Client()
current_room = None

def send_message():
    try:
        while True:
            message = input()
            if message.lower() == '/exit':
                sio.disconnect()
                break
            if current_room:
                sio.emit('message', {'room': current_room, 'message': message})
    except KeyboardInterrupt:
        sio.disconnect()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def rooms_list(data):
    print("\nAvailable rooms:", data)
    room = input("Enter room name to join: ")
    if room in data:
        global current_room
        current_room = room
        sio.emit('join', {'room': room})
        print(f"Joined room: {room}. Type messages (type /exit to quit)")
        threading.Thread(target=send_message, daemon=True).start()
    else:
        print("Invalid room!")
        sio.disconnect()

@sio.event
def message(data):
    print(f"\n[{data['sender'][:5]}]: {data['message']}")

@sio.event
def disconnect():
    print("Disconnected from server")

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    sio.wait()