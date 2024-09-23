from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def connect_to_db():
    try:
        # Koneksi ke MongoDB
        client = MongoClient("mongodb://localhost:27017/fastapiCrud")
        # Ping untuk memeriksa apakah koneksi berhasil
        client.admin.command('ping')
        print("Koneksi ke database MongoDB berhasil")
        return client['fastapiCrud']  # Mengembalikan database
    except ConnectionFailure:
        print("Gagal terhubung ke MongoDB")
        return None
