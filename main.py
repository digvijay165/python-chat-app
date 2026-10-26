"""
main.py
-------
Shared configuration and a convenience launcher for the chat
application.

Both client.py and server.py import HOST/PORT from here so the
connection settings only need to be changed in one place. Running
this file directly lets you pick whether to start the server side
or the client side from a single entry point.
"""

import subprocess
import sys

# --- Shared network configuration -------------------------------------
HOST = "127.0.0.1"   # localhost - change to the server's LAN/IP address
                      # if client and server run on different machines
PORT = 5050


def main():
    print("Python Chat Application")
    print("1. Start Server")
    print("2. Start Client")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "1":
        subprocess.run([sys.executable, "server.py"])
    elif choice == "2":
        subprocess.run([sys.executable, "client.py"])
    else:
        print("Invalid choice. Please run again and enter 1 or 2.")


if __name__ == "__main__":
    main()
