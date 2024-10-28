import sys
import os

def add_project_root_to_path():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


add_project_root_to_path()

from src.modules.conver import Conver

converter = Conver()

input_file = '/home/george/Desktop/test_document.docx'
output_extension = 'pdf'

output_file = converter.base_converter(input_file, output_extension)

print(f"Converted '{input_file}' to '{output_file}'")
