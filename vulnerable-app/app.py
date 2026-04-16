"""
vulnerable-app/app.py — Учебное веб-приложение с намеренными уязвимостями
==========================================================================
Курс OTUS: Безопасный код с SonarQube (Community Edition)
Урок 3 — OWASP Top 10 2021

ВНИМАНИЕ: код содержит НАМЕРЕННЫЕ уязвимости. Не для production.
"""

import os
import pickle
import sqlite3
import subprocess
import hashlib
import secrets
import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


# ── A02 Cryptographic Failures — Hard-coded credentials (CWE-798) ────
DB_PASSWORD = "admin123"
SECRET_KEY  = "mysecretkey12345"
API_TOKEN   = "tok_prod_abc123xyz"


def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)
    conn.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, item TEXT)")
    conn.execute("INSERT OR IGNORE INTO users VALUES (1,'admin','admin123','admin')")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2,'alice','pass456','user')")
    conn.execute("INSERT OR IGNORE INTO orders VALUES (1, 2, 'book')")
    conn.commit()
    conn.close()


# ── A03 Injection — SQL Injection (CWE-89) ──────────────────────────
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        return jsonify({"status": "ok", "role": user["role"]})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


# ── A03 Injection — Command Injection (CWE-78) ──────────────────────
@app.route("/ping", methods=["GET"])
def ping():
    host = request.args.get("host", "localhost")
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result.decode()


# ── A05 Security Misconfiguration — Path Traversal (CWE-22) ─────────
@app.route("/file", methods=["GET"])
def read_file():
    filename = request.args.get("filename", "readme.txt")
    base_dir = "/var/app/files"
    filepath = os.path.join(base_dir, filename)
    with open(filepath) as f:
        return f.read()


# ── A02 Cryptographic Failures — Weak Hash (CWE-327) ────────────────
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


# ── A01 Broken Access Control — /admin без авторизации ───────────────
@app.route("/admin", methods=["GET"])
def admin_panel():
    return jsonify({"users": ["admin", "alice"], "secret": SECRET_KEY})


# ── A01 Broken Access Control — IDOR (CWE-639) ──────────────────────
@app.route("/user/<int:user_id>/orders", methods=["GET"])
def user_orders(user_id):
    conn = get_db_connection()
    rows = conn.execute(f"SELECT * FROM orders WHERE user_id={user_id}").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# ── A04 Insecure Design — сброс пароля без токена (CWE-640) ─────────
@app.route("/reset-password", methods=["POST"])
def reset_password():
    email = request.form.get("email", "")
    new_password = request.form.get("new_password", "")
    conn = get_db_connection()
    conn.execute(f"UPDATE users SET password='{new_password}' WHERE username='{email}'")
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


# ── A07 Auth Failures — предсказуемый session_id (CWE-330) ──────────
@app.route("/issue-session/<int:user_id>", methods=["GET"])
def issue_session(user_id):
    session_id = str(user_id)
    resp = make_response(jsonify({"session": session_id}))
    resp.set_cookie("sid", session_id)
    return resp


# ── A08 Software & Data Integrity — pickle.loads (CWE-502) ──────────
@app.route("/load-state", methods=["POST"])
def load_state():
    obj = pickle.loads(request.data)
    return jsonify({"loaded": str(obj)[:100]})


# ── A09 Logging & Monitoring Failures — нет аудита (CWE-778) ────────
@app.route("/delete-account/<int:user_id>", methods=["POST"])
def delete_account(user_id):
    conn = get_db_connection()
    try:
        conn.execute(f"DELETE FROM users WHERE id={user_id}")
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()
    return jsonify({"status": "ok"})


# ── A10 SSRF — Server-Side Request Forgery (CWE-918) ────────────────
@app.route("/fetch", methods=["GET"])
def fetch_url():
    url = request.args.get("url", "")
    r = requests.get(url, timeout=5)
    return r.text


# ── Безопасный пример: хеширование (для сравнения) ───────────────────
def hash_password_secure(password: str) -> str:
    salt = secrets.token_hex(16)
    return hashlib.sha256((salt + password).encode()).hexdigest() + ":" + salt


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
