import os

def ride_path(path: str) -> str:
    return os.path.normpath(os.path.join(os.getcwd(), path))
    
def create_path(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def clean_up(input_file: str, output_file: str) -> None:
    if output_file and os.path.exists(output_file):
        os.remove(output_file)

    if input_file and os.path.exists(input_file):
        os.remove(input_file)