from src.utils.installer import *
from config.path_config import *
from src.api.app import Server

add_project_root_to_path()

if __name__ == '__main__':
    if not check_and_install_libreoffice():
        exit(1)
        
    server = Server()
    server.run_development()