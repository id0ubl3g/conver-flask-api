import os

from typing import Optional

def ride_path(path: str) -> str:
    return os.path.normpath(os.path.join(os.getcwd(), path))
    
def create_path(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def clean_up(file_path: Optional[str], output_file: Optional[str]) -> None:
    if output_file and os.path.exists(output_file):
        os.remove(output_file)

    if file_path and os.path.exists(file_path):
        os.remove(file_path)