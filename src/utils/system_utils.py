import os

def ride_path(path):
    return os.path.normpath(os.path.join(os.getcwd(), path))
    
def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_up(input_file, output_file):
        if output_file and os.path.exists(output_file):
            os.remove(output_file)
    
        if input_file and os.path.exists(input_file):
            os.remove(input_file)