import tkinter as tk
from tkinter import ttk

from socket_server import SocketServer

HOST = "127.0.0.1"
PORT = 5001

CONNECTED = "CONNECTED"
DISCONNECTED = "DISCONNECTED"


class PublisherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Publisher")
        self.root.geometry("360x230")

        self.connection_state = DISCONNECTED
        self.server = SocketServer(HOST, PORT, on_status=self._get_status)

        self.build_ui()
        self.server.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _get_status(self):
        return "Connected" if self.connection_state == CONNECTED else "Disconnected"

    def build_ui(self):
        title = ttk.Label(self.root, text="Publisher Application", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.connect_btn = ttk.Button(button_frame, text="Connect", command=self.connect_action)
        self.connect_btn.grid(row=0, column=0, padx=10)

        self.disconnect_btn = ttk.Button(button_frame, text="Disconnect", command=self.disconnect_action)
        self.disconnect_btn.grid(row=0, column=1, padx=10)

        state_frame = ttk.LabelFrame(self.root, text="Connection State")
        state_frame.pack(pady=15, padx=20, fill="x")

        self.connected_label = tk.Label(state_frame, text="CONNECTED: False", width=22, pady=8)
        self.connected_label.pack(pady=4)

        self.disconnected_label = tk.Label(state_frame, text="DISCONNECTED: True", width=22, pady=8)
        self.disconnected_label.pack(pady=4)

        self.update_state_display()

    def update_state_display(self):
        if self.connection_state == CONNECTED:
            self.connected_label.config(text="CONNECTED: True", bg="lightgreen")
            self.disconnected_label.config(text="DISCONNECTED: False", bg="lightgray")
        else:
            self.connected_label.config(text="CONNECTED: False", bg="lightgray")
            self.disconnected_label.config(text="DISCONNECTED: True", bg="tomato")

    def connect_action(self):
        self.connection_state = CONNECTED
        self.update_state_display()
        self.server.broadcast("Connected")

    def disconnect_action(self):
        self.connection_state = DISCONNECTED
        self.update_state_display()
        self.server.broadcast("Disconnected")

    def on_close(self):
        self.server.shutdown()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PublisherApp(root)
    root.mainloop()
