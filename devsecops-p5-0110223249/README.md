# Task Manager API — DevSecOps P5

## 1. Nama Aplikasi & Fungsi
**Task Manager API** adalah REST API sederhana untuk mengelola daftar tugas (to-do list).
Fitur: membuat, melihat, mengubah, menghapus task, memfilter berdasarkan status selesai, dan melihat statistik task.
Data disimpan di memori (tanpa database) sehingga cocok untuk demo pipeline CI/CD.

## 2. Bahasa & Framework
- Python 3.11
- Flask 3 (web framework)
- pytest (unit test)
- Bandit (SAST tool)

## 3. Struktur Proyek
```
.
├── .github/workflows/devsecops.yml   # pipeline CI/CD
├── app/
│   ├── __init__.py                   # application factory
│   ├── config.py                     # konfigurasi
│   ├── models.py                     # model Task
│   ├── routes.py                     # endpoint REST
│   ├── storage.py                    # penyimpanan in-memory
│   └── validators.py                 # validasi input
├── tests/test_app.py                 # unit test
├── run.py                            # entry point
├── requirements.txt
└── README.md
```

## 4. Cara Menjalankan
```bash
# 1. Buat virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate   |  Linux/Mac: source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan aplikasi
python run.py
# buka http://127.0.0.1:5000

# 4. Jalankan unit test
pytest -v
```

Contoh penggunaan:
```bash
curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"title":"Belajar DevSecOps"}'
curl http://127.0.0.1:5000/tasks
curl http://127.0.0.1:5000/tasks/stats
```

| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | `/health` | Cek status aplikasi |
| GET | `/tasks` | Daftar task (`?done=true/false`) |
| POST | `/tasks` | Buat task baru |
| GET | `/tasks/<id>` | Detail task |
| PUT | `/tasks/<id>` | Ubah task |
| DELETE | `/tasks/<id>` | Hapus task |
| GET | `/tasks/stats` | Statistik task |

## 5. Overview Pipeline CI/CD
Pipeline ada di `.github/workflows/devsecops.yml`, berjalan di `ubuntu-latest`, dan terpicu saat **push** atau **pull request** ke branch `main`.

| Job | Fungsi |
|-----|--------|
| `build` | Checkout, setup Python, install dependencies, compile check, dan menjalankan unit test dengan pytest |
| `sast-scan` | Berjalan setelah `build` sukses (`needs: build`). Menjalankan **Bandit** untuk analisis keamanan statis; pipeline gagal jika ditemukan isu severity medium ke atas, dan laporan JSON diunggah sebagai artifact |

Alur: `push / pull_request ke main` → `build` → `sast-scan`.
