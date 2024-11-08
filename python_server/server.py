from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import uuid

import psycopg2
import os
import time

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Połączono z bazą danych")
            return conn
        except psycopg2.OperationalError:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            time.sleep(5)

conn = connect_to_db()
cursor = conn.cursor()


class SimpleRequestHandler(BaseHTTPRequestHandler):

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
        #self.wfile.write(json.dumps(self.user_list).encode())
        cursor.execute("SELECT first_name, last_name, role, user_id FROM users;")
        users = cursor.fetchall()
            # Konwertuj wyniki do listy słowników
        user_list = [
            {
                'first_name': user[0],
                'last_name': user[1],
                'role': user[2],
                'user_id': user[3]
            } for user in users
        ]
        self.wfile.write(json.dumps(user_list).encode())

    # Obsługa metody POST
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        new_user = json.loads(post_data)
        #self.user_list.append(new_user)  # Dodanie nowego użytkownika do listy

        # Sprawdź, czy wszystkie wymagane pola są obecne
        required_fields = ['first_name', 'last_name', 'role', 'user_id']
        if not all(field in new_user for field in required_fields):
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Missing fields in request"}).encode())
            return

        # Wstaw nowego użytkownika do bazy danych
        insert_query = """
        INSERT INTO users (first_name, last_name, role, user_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            new_user['first_name'],
            new_user['last_name'],
            new_user['role'],
            new_user['user_id']
        ))
        conn.commit()
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
        
         # Usunięcie użytkownika z bazy danych
        delete_query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
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
