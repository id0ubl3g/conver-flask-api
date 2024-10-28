import sys
import os

def add_project_root_to_path():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


add_project_root_to_path()

from src.api.app import Server

sv = Server()
sv.run_development()
