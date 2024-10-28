import os

def ride_path(path):
    return os.path.normpath(os.path.join(os.getcwd(), path))
    
def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)