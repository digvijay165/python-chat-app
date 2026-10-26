"""
server.py
---------
Server-side of the Python Chat Application.

Listens for an incoming connection from client.py, then allows
two-way messaging through the shared Tkinter layout defined in
layout.py. Incoming messages are received on a background thread
and placed on a queue; the GUI's "Recieve" button (and the
automatic poll in layout.py) drains that queue and prints the
messages to the chat window.
"""

import socket
import threading
import queue

from layout import ChatLayout
from main import HOST, PORT

incoming_messages = queue.Queue()
client_conn = None
client_addr = None


def start_server_socket():
    """Create the listening socket and accept a single client connection."""
    global client_conn, client_addr

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT} ... waiting for a client to connect")

    client_conn, client_addr = server_socket.accept()
    print(f"Client connected from {client_addr}")

    listen_thread = threading.Thread(target=listen_for_messages, daemon=True)
    listen_thread.start()


def listen_for_messages():
    """Background thread: continuously read messages from the client."""
    while True:
        try:
            data = client_conn.recv(1024)
            if not data:
                incoming_messages.put("[Client disconnected]")
                break
            incoming_messages.put(f"Client: {data.decode('utf-8')}")
        except OSError:
            break


def send_message(message):
    """Callback wired to the Send button - sends text to the client."""
    if client_conn is None:
        layout.display_message("[Not connected to a client yet]")
        return
    try:
        client_conn.sendall(message.encode("utf-8"))
        layout.display_message(f"Server: {message}")
    except OSError:
        layout.display_message("[Failed to send - connection lost]")


def receive_messages():
    """Callback wired to the Recieve button - drains the message queue."""
    while not incoming_messages.empty():
        msg = incoming_messages.get()
        layout.display_message(msg)


if __name__ == "__main__":
    layout = ChatLayout(title="Server", on_send=send_message, on_receive=receive_messages)

    # Accept the client connection on a separate thread so the GUI
    # can open immediately instead of freezing while waiting.
    threading.Thread(target=start_server_socket, daemon=True).start()

    layout.run()
