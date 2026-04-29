import socket
import threading


class SocketServer:
    def __init__(self, host, port, on_status):
        self.host = host
        self.port = port
        self.on_status = on_status
        self.clients = []
        self.subscribed_clients = set()
        self.lock = threading.Lock()
        self.running = True
        self._server_socket = None

    def start(self):
        threading.Thread(target=self._server_loop, daemon=True).start()

    def _server_loop(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen()

        while self.running:
            try:
                client_socket, _ = self._server_socket.accept()
                with self.lock:
                    self.clients.append(client_socket)
                threading.Thread(
                    target=self._handle_client, args=(client_socket,), daemon=True
                ).start()
            except OSError:
                break

    def _handle_client(self, client_socket):
        while self.running:
            try:
                data = client_socket.recv(1024).decode("utf-8").strip()
                if not data:
                    break

                if data == "SUBSCRIBE":
                    with self.lock:
                        self.subscribed_clients.add(client_socket)
                    client_socket.sendall(b"Subscribed\n")

                elif data == "UNSUBSCRIBE":
                    with self.lock:
                        self.subscribed_clients.discard(client_socket)
                    client_socket.sendall(b"Unsubscribed\n")

                elif data == "STATUS":
                    client_socket.sendall(f"{self.on_status()}\n".encode("utf-8"))

            except ConnectionError:
                break

        with self.lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            self.subscribed_clients.discard(client_socket)

        try:
            client_socket.close()
        except OSError:
            pass

    def broadcast(self, event_text):
        with self.lock:
            subscribers = list(self.subscribed_clients)

        for client_socket in subscribers:
            try:
                client_socket.sendall(f"EVENT:{event_text}\n".encode("utf-8"))
            except ConnectionError:
                with self.lock:
                    self.subscribed_clients.discard(client_socket)

    def shutdown(self):
        self.running = False

        try:
            self._server_socket.close()
        except Exception:
            pass

        with self.lock:
            for client in self.clients:
                try:
                    client.close()
                except OSError:
                    pass
