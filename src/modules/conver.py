from config.base_converter import BaseConverter
from src.utils.system_utils import *

import subprocess
import os

class Conver(BaseConverter):
    def base_converter(self, input_file, output_extension):
        output_dir = ride_path('src/temp')
    
        create_path(output_dir)
        
        command = ['libreoffice', '--headless', '--convert-to', output_extension, '--outdir', 'src/temp', input_file]
        subprocess.run(command, check=True)
        
        output_file = os.path.join(output_dir, os.path.basename(input_file).replace(os.path.splitext(input_file)[1], f'.{output_extension}'))
        
        return output_file