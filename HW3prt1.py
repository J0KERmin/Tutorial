import os
import shutil
from multiprocessing.dummy import Pool as ThreadPool

def copy_file(file_info):
    source_file, dest_directory = file_info
    ext = os.path.splitext(source_file)[1][1:].lower()  # отримання розширення файлу без крапки
    if ext:  # перевірка, чи є розширення
        dest_dir = os.path.join(dest_directory, ext)
        os.makedirs(dest_dir, exist_ok=True)  # створення директорії, якщо вона не існує
        try:
            shutil.copy(source_file, dest_dir)
        except Exception as e:
            print(f"Error copying {source_file}: {e}")

def process_directory(source_dir, dest_dir='dist'):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    files = []
    directories = [source_dir]
    
    while directories:
        current_dir = directories.pop()
        for root, _, filenames in os.walk(current_dir):
            files.extend([(os.path.join(root, filename), dest_dir) for filename in filenames])
            # Додаємо піддиректорії в чергу для обробки
            directories.extend([os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))])
    
    pool = ThreadPool()
    pool.map(copy_file, files)
    pool.close()
    pool.join()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py source_directory [destination_directory]")
        sys.exit(1)

    source_directory = sys.argv[1]
    destination_directory = sys.argv[2] if len(sys.argv) > 2 else 'dist'
    
    process_directory(source_directory, destination_directory)
    print("Files copied and sorted successfully.")

