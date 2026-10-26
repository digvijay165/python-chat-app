"""
client.py
---------
Client-side of the Python Chat Application.

Connects to server.py, then allows two-way messaging through the
shared Tkinter layout defined in layout.py. Incoming messages are
received on a background thread and placed on a queue; the GUI's
"Recieve" button (and the automatic poll in layout.py) drains that
queue and prints the messages to the chat window.
"""

import socket
import threading
import queue

from layout import ChatLayout
from main import HOST, PORT

incoming_messages = queue.Queue()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_to_server():
    """Connect to the server and start listening for messages."""
    try:
        client_socket.connect((HOST, PORT))
        incoming_messages.put(f"[Connected to server {HOST}:{PORT}]")
    except OSError as e:
        incoming_messages.put(f"[Could not connect to server: {e}]")
        return

    listen_thread = threading.Thread(target=listen_for_messages, daemon=True)
    listen_thread.start()


def listen_for_messages():
    """Background thread: continuously read messages from the server."""
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                incoming_messages.put("[Server disconnected]")
                break
            incoming_messages.put(f"Server: {data.decode('utf-8')}")
        except OSError:
            break


def send_message(message):
    """Callback wired to the Send button - sends text to the server."""
    try:
        client_socket.sendall(message.encode("utf-8"))
        layout.display_message(f"Client: {message}")
    except OSError:
        layout.display_message("[Failed to send - not connected]")


def receive_messages():
    """Callback wired to the Recieve button - drains the message queue."""
    while not incoming_messages.empty():
        msg = incoming_messages.get()
        layout.display_message(msg)


if __name__ == "__main__":
    layout = ChatLayout(title="Client", on_send=send_message, on_receive=receive_messages)

    # Connect to the server on a separate thread so the GUI opens
    # immediately instead of freezing while the connection is made.
    threading.Thread(target=connect_to_server, daemon=True).start()

    layout.run()
