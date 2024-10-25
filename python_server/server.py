from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import uuid

class SimpleRequestHandler(BaseHTTPRequestHandler):
    user_list = [{
        'first_name': 'Michal',
        'last_name': 'Mucha',
        'role': 'instructor',
        'user_id': str(uuid.uuid4()) 
    }]

    # Ustawienia nagłówków (w tym CORS)
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Pozwala na dostęp z dowolnej domeny
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')  # Dozwolone metody
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Dozwolone nagłówki
        self.end_headers()

    # Obsługa metody GET
    def do_GET(self):
        self._set_headers(200)
        self.wfile.write(json.dumps(self.user_list).encode())

    # Obsługa metody POST
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        new_user = json.loads(post_data)
        self.user_list.append(new_user)  # Dodanie nowego użytkownika do listy

        self._set_headers(201)
        self.wfile.write(json.dumps(new_user).encode())  # Zwróć dodanego użytkownika

    # Obsługa metody DELETE (usuwanie po user_id)
    def do_DELETE(self):
        # Pobieramy user_id z URL
        user_id = self.path.strip("/")

        # Sprawdzenie czy user_id zostało przekazane
        if not user_id:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "User ID is required"}).encode())
            return

        user_found = False

        # Szukanie użytkownika po user_id
        for user in self.user_list:
            if user['user_id'] == user_id:
                self.user_list.remove(user)
                user_found = True
                break

        if not user_found:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "User not found"}).encode())
        else:
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "User deleted successfully"}).encode())

    # Obsługa metody OPTIONS (CORS)
    def do_OPTIONS(self):
        self._set_headers(200)

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleRequestHandler)
    print("Server running on port 8000")
    httpd.serve_forever()
