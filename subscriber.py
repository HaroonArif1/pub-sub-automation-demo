import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox

HOST = "127.0.0.1"
PORT = 5001


class SubscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subscriber")
        self.root.geometry("460x330")

        self.socket = None
        self.running = True
        self.subscribed = False

        self.build_ui()
        self.connect_to_publisher()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        title = ttk.Label(self.root, text="Subscriber Application", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=8)

        self.subscribe_btn = ttk.Button(button_frame, text="Subscribe", command=self.subscribe)
        self.subscribe_btn.grid(row=0, column=0, padx=8)

        self.unsubscribe_btn = ttk.Button(button_frame, text="Unsubscribe", command=self.unsubscribe)
        self.unsubscribe_btn.grid(row=0, column=1, padx=8)

        self.check_status_btn = ttk.Button(button_frame, text="Check Status", command=self.check_status)
        self.check_status_btn.grid(row=0, column=2, padx=8)

        self.mode_label = tk.Label(self.root, text="Subscription Mode: Unsubscribed", bg="tomato", width=35, pady=6)
        self.mode_label.pack(pady=8)

        text_label = ttk.Label(self.root, text="Received Events / Status:")
        text_label.pack(anchor="w", padx=20)

        self.text_box = tk.Text(self.root, height=10, width=52)
        self.text_box.pack(padx=20, pady=8)

    def connect_to_publisher(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((HOST, PORT))

            listener_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
            listener_thread.start()

            self.append_text("Connected to Publisher server")
            self.append_text("Default mode: Unsubscribed")

        except ConnectionRefusedError:
            messagebox.showerror(
                "Publisher Not Running",
                "Please start publisher.py first, then start subscriber.py."
            )

    def listen_for_messages(self):
        buffer = ""

        while self.running:
            try:
                data = self.socket.recv(1024).decode("utf-8")
                if not data:
                    break

                buffer += data

                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    self.process_message(message.strip())

            except OSError:
                break

    def process_message(self, message):
        if not message:
            return

        if message.startswith("EVENT:"):
            event_text = message.replace("EVENT:", "", 1)
            self.root.after(0, self.append_text, event_text)

        elif message in ["Connected", "Disconnected"]:
            self.root.after(0, self.append_text, message)

        elif message in ["Subscribed", "Unsubscribed"]:
            self.root.after(0, self.append_text, message)

    def send_command(self, command):
        if not self.socket:
            self.append_text("Not connected to Publisher server")
            return

        try:
            self.socket.sendall(f"{command}\n".encode("utf-8"))
        except OSError:
            self.append_text("Unable to send command to Publisher")

    def subscribe(self):
        self.subscribed = True
        self.mode_label.config(text="Subscription Mode: Subscribed", bg="lightgreen")
        self.send_command("SUBSCRIBE")

    def unsubscribe(self):
        self.subscribed = False
        self.mode_label.config(text="Subscription Mode: Unsubscribed", bg="tomato")
        self.send_command("UNSUBSCRIBE")

    def check_status(self):
        # This is the only polling action.
        # No timer or background status polling is used.
        self.send_command("STATUS")

    def append_text(self, text):
        self.text_box.insert(tk.END, text + "\n")
        self.text_box.see(tk.END)

    def on_close(self):
        self.running = False

        try:
            if self.socket:
                self.socket.close()
        except OSError:
            pass

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SubscriberApp(root)
    root.mainloop()