# utils/save_results.py

def save_to_file(data):
    file_path = "data/results.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)

    print(f"📁 Results saved to {file_path}")