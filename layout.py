"""
layout.py
---------
Shared Tkinter GUI layout used by both client.py and server.py.

The layout is intentionally identical for both sides of the chat
(a scrollable message area on top, a text entry box, and two
buttons - "Recieve" and "Send") so that the client window and the
server window look and behave the same way.

Usage:
    from layout import ChatLayout

    layout = ChatLayout(title="Client", on_send=my_send_func, on_receive=my_receive_func)
    layout.run()
"""

import tkinter as tk
from tkinter import scrolledtext


class ChatLayout:
    """Builds and owns the chat window UI, and wires up callbacks."""

    def __init__(self, title="Chat", on_send=None, on_receive=None, width=420, height=430):
        self.on_send = on_send
        self.on_receive = on_receive

        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        # --- Message display area -------------------------------------
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state="disabled",
            font=("Segoe UI", 10),
            bg="#f2f2f2",
        )
        self.chat_display.pack(padx=10, pady=(10, 5), fill=tk.BOTH, expand=True)

        # --- Message entry box ------------------------------------------
        self.message_entry = tk.Entry(self.root, font=("Segoe UI", 10))
        self.message_entry.pack(padx=10, pady=(0, 5), fill=tk.X)
        self.message_entry.bind("<Return>", lambda event: self._handle_send())

        # --- Buttons ------------------------------------------------------
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.receive_button = tk.Button(
            button_frame, text="Recieve", command=self._handle_receive
        )
        self.receive_button.pack(fill=tk.X, pady=(0, 5))

        self.send_button = tk.Button(
            button_frame, text="Send", command=self._handle_send
        )
        self.send_button.pack(fill=tk.X)

        # Periodically check for incoming messages in the background
        # so the chat window updates itself even without pressing
        # the "Recieve" button (nice UX on top of the manual button).
        self.root.after(500, self._auto_poll)

    # ----------------------------------------------------------------- #
    # Public helpers
    # ----------------------------------------------------------------- #
    def display_message(self, text):
        """Append a line of text to the chat display area."""
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, text + "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see(tk.END)

    def get_entry_text(self):
        return self.message_entry.get()

    def clear_entry(self):
        self.message_entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

    # ----------------------------------------------------------------- #
    # Internal event handlers
    # ----------------------------------------------------------------- #
    def _handle_send(self):
        message = self.get_entry_text().strip()
        if not message:
            return
        if self.on_send:
            self.on_send(message)
        self.clear_entry()

    def _handle_receive(self):
        if self.on_receive:
            self.on_receive()

    def _auto_poll(self):
        # Silently pull any queued messages every 500ms so messages
        # show up even if the user forgets to click "Recieve".
        if self.on_receive:
            self.on_receive()
        self.root.after(500, self._auto_poll)
