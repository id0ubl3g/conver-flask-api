from config.path_config import *
from src.api.app import Server

add_project_root_to_path()

app = Server().app

if __name__ == '__main__':
    server = Server()
    server.run_production()
