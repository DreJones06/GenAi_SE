# storage/file_store.py

import os

def save_result(data, path):
    os.makedirs("data", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)