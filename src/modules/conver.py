from config.base_converter import BaseConverter
from src.utils.system_utils import *

from typing import Optional
import subprocess
import os

class Conver(BaseConverter):
    def __init__(self) -> None:
        self.output_dir: str = ride_path('src/temp')
        self.output_file: Optional[str] = None

    def base_converter(self, input_file: str, output_extension: str) -> str:
        create_path(self.output_dir)
        
        command = ['libreoffice', '--headless', '--convert-to', output_extension, '--outdir', 'src/temp', input_file]
        subprocess.run(command, check=True)
        
        self.output_file = os.path.join(self.output_dir, os.path.basename(input_file).replace(os.path.splitext(input_file)[1], f'.{output_extension}'))
        
        return self.output_file