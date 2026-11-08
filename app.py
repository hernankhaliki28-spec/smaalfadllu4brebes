import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parent
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8000"))

BOOKS = [
    {
        "title": "Dunia Sophie",
        "author": "Jostein Gaarder",
        "filename": "Dunia Sophie - CraftopiaDigital.pdf",
        "category": "Filsafat",
        "tags": ["filsafat", "novel", "pemikiran"],
    },
    {
        "title": "Laut Bercerita",
        "author": "Leila S. Chudori",
        "filename": "Laut Bercerita.pdf",
        "category": "Novel Indonesia",
        "tags": ["novel", "sejarah", "sastra indonesia"],
    },
    {
        "title": "Ronggeng Dukuh Paruk",
        "author": "Ahmad Tohari",
        "filename": "Ronggeng Dukuh Paruk - eBookWave.pdf",
        "category": "Novel Indonesia",
        "tags": ["novel", "budaya", "sastra indonesia"],
    },
    {
        "title": "Janji",
        "author": "Tere Liye",
        "filename": "Tere Liye - Janji (1).pdf",
        "category": "Novel Indonesia",
        "tags": ["novel", "inspirasi", "sastra indonesia"],
    },
]

INTERESTS = {
    "filsafat": ["filsafat", "pemikiran"],
    "novel": ["novel"],
    "sejarah": ["sejarah", "budaya", "sastra indonesia"],
    "inspirasi": ["inspirasi", "novel"],
}


def available_books():
    result = []
    for book in BOOKS:
        relative_path = Path("BUKU NOVEL RANDOM") / book["filename"]
        if not (ROOT / relative_path).is_file():
            continue
        result.append(
            {
                **book,
                "url": quote(relative_path.as_posix(), safe="/"),
            }
        )
    return result


class LibraryHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def list_directory(self, path):
        self.send_error(404, "Directory listing is disabled.")
        return None

    def do_GET(self):
        request = urlsplit(self.path)
        request_path = unquote(request.path)
        path_parts = Path(request_path).parts
        if any(part.startswith(".") for part in path_parts) or Path(
            request_path
        ).name in {"app.py", "README.txt", "render.yaml"}:
            self.send_error(404)
            return

        if request_path == "/api/books":
            self.send_json({"books": available_books()})
            return

        if request_path == "/api/search":
            query = parse_qs(request.query).get("q", [""])[0].strip().casefold()
            if len(query) > 100:
                self.send_json({"error": "Kata pencarian terlalu panjang."}, 400)
                return
            matches = [
                book
                for book in available_books()
                if query
                in " ".join(
                    [book["title"], book["author"], book["category"], *book["tags"]]
                ).casefold()
            ]
            self.send_json({"books": matches})
            return

        if request_path == "/api/recommendations":
            interest = parse_qs(request.query).get("interest", [""])[0].casefold()
            wanted_tags = INTERESTS.get(interest)
            if wanted_tags is None:
                self.send_json({"error": "Minat bacaan tidak dikenal."}, 400)
                return
            matches = [
                book
                for book in available_books()
                if any(tag in book["tags"] for tag in wanted_tags)
            ]
            self.send_json({"books": matches})
            return

        super().do_GET()


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), LibraryHandler)
    print(f"Perpustakaan berjalan di port {PORT}.")
    print(f"Di komputer ini: http://localhost:{PORT}/")
    print(f"Perangkat lain: http://<IP-komputer-ini>:{PORT}/")
    print("Cari alamat IPv4 komputer dengan menjalankan ipconfig.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
    finally:
        server.server_close()
