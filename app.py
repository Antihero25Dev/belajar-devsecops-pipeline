"""Modul backend autentikasi Flask dengan implementasi kueri aman."""

import sqlite3
from flask import Flask, request

app = Flask(__name__)


def init_db():
    """Inisialisasi basis data dan membuat data pengguna awal."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES ('admin', 'supersecret')"
    )
    conn.commit()
    conn.close()


@app.route("/login", methods=["POST"])
def login():
    """Endpoint login menggunakan parameterized query."""
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Parameterized query (?) mencegah manipulasi sintaks SQL
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return "<h3>Login Berhasil!</h3>"
    return "<h3>Login Gagal!</h3>"


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
