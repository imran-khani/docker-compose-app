import psycopg2
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


with open(os.environ["DB_PASSWORD_FILE"]) as f:
	db_password = f.read().strip()

def check_database():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=db_password,
        dbname=os.environ["DB_NAME"],
    )

    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = check_database()
        message = f"Database returned: {result}\n".encode()

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)


server = HTTPServer(("0.0.0.0", 3000), Handler)
print("Python app listening on port 3000")
print("Database host:", os.environ["DB_HOST"])
server.serve_forever()
