import os
from pathlib import Path

directory_path = Path.cwd() 

i = 0

def write_file(i):
    try:
        file_name = f"text_file{i}.txt"
        file_path = os.path.join(directory_path, file_name)

        while os.path.exists(file_path):
            i += 10
            file_name = f"text_file{i}.txt"
            file_path = os.path.join(directory_path, file_name)             
        
        with open(file_path, 'w') as file:
            file.write(f'This is file number {i}.')
        
        print(f'File "{file_name}" created successfully at "{file_path}."')        
            
        
    except IOError as e:
        print(f'Error creating the file: {e}')
        i += 1

while i < 10:
        write_file(i)
        i += 1

