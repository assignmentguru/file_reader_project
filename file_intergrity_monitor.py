import os
import hashlib
import schedule
import time
from models import FileModel, db

known_checksums = {}

def calculate_checksum(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

def scan_file(file_path):
    current_checksum = calculate_checksum(file_path)
    existing_file = FileModel.query.filter_by(file_path=file_path).first()

    if not existing_file:
        new_file = FileModel(file_path=file_path, checksum=current_checksum)
        db.session.add(new_file)
        db.session.commit()
    elif existing_file.checksum != current_checksum:
        existing_file.checksum = current_checksum
        db.session.commit()
        print(f"Change detected in file: {file_path}")
def scan_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            scan_file(file_path)
        elif os.path.isdir(file_path):
            scan_directory(file_path)

def main():
    schedule.every(5).minutes.do(scan_directory, directory_path='/path/to/directory')
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        
if __name__ == "__main__":
    main()
