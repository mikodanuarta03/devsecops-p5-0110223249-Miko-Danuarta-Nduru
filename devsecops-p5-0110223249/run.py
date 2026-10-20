"""Entry point untuk menjalankan aplikasi Task Manager API."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Bind ke localhost saja (aman) dan debug dimatikan.
    app.run(host="127.0.0.1", port=5000, debug=False)
