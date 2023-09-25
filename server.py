import socket
import json
import math

# Load config from external JSON file
def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# RPC Functions
def floor(x):
    return math.floor(x)

def nroot(n, x):
    return x ** (1 / n)

def reverse(s):
    return s[::-1]

FUNCTION_MAP = {
    "floor": floor,
    "nroot": nroot,
    "reverse": reverse,
}

class RequestHandler:
    def handle_request(self, request_json):
        try:
            request = json.loads(request_json)
            method = request["method"]
            params = request["params"]
            param_types = request["param_types"]
            req_id = request["id"]

            if method in FUNCTION_MAP:
                func = FUNCTION_MAP[method]
                result = func(*params)
                response = {
                    "results": str(result),
                    "result_type": str(type(result).__name__),
                    "id": req_id
                }
            else:
                response = {
                    "error": "Unknown method",
                    "id": req_id
                }
        except Exception as e:
            response = {
                "error": str(e),
                "id": "unknown"
            }
        
        return json.dumps(response)

class SocketManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
    
    def accept_connection(self):
        return self.socket.accept()

def main():
    config = load_config("config.json")
    HOST = config["host"]
    PORT = config["port"]
    
    socket_manager = SocketManager(HOST, PORT)
    request_handler = RequestHandler()
    
    conn, addr = socket_manager.accept_connection()
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            response = request_handler.handle_request(data.decode('utf-8'))
            conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    main()
