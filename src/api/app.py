from docs.flasgger import init_flasgger
from src.modules.conver import Conver
from src.utils.system_utils import *

from flask import Flask, request, jsonify, send_file, Response
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask_cors import CORS

import subprocess
import mimetypes
import uuid
import os

class Server:
    def __init__(self) -> None:
        self.app: Flask = Flask(__name__)
        CORS(self.app)
        self.converter: Conver = Conver()

        MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024
        UPLOAD_FOLDER: str = 'src/temp'
        
        self.app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.app.errorhandler(413)(self.too_large)
        self._register_routes()

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        self.allowed_extensions: dict[str, list[str]] = {
            'input': ['doc', 'docx', 'odt', 'txt', 'rtf'],
            'output': ['pdf', 'doc', 'docx', 'odt', 'txt', 'rtf']
        }

        self.expected_mime_types: dict[str, str] = {
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'odt': 'application/vnd.oasis.opendocument.text',
            'txt': 'text/plain',
            'rtf': 'application/rtf'
        }

        self.output_extension: str = None
        self.output_filename: str = None
        self.file_extension: str = None
        self.full_filename: str = None
        self.file: FileStorage = None
        self.output_file: str = None
        self.file_path: str = None
        self.unique_id: str = None
        self.mime_type: str = None
        self.filename: str = None
        
        init_flasgger(self.app)

    def create_error_response(self, message: str, code: int) -> Response:
        return jsonify({'error': message}), code
    
    def too_large(self, error: Exception) -> Response:
        return self.create_error_response('File size exceeds the maximum limit of 50 MB.', 413)

    def reset_optional_values(self):
        self.output_extension = None
        self.output_filename = None
        self.file_extension = None
        self.full_filename = None
        self.file = None
        self.output_file = None
        self.file_path = None
        self.unique_id = None
        self.mime_type = None
        self.filename = None

    def _register_routes(self) -> None:
        @self.app.route('/converter', methods=['POST'])
        def convert_file() -> Response:
            try:
                self.file = request.files['file']

                if not self.file:
                    return self.create_error_response('No file uploaded', 400)

                self.full_filename = secure_filename(self.file.filename)
                self.file_extension = self.full_filename.rsplit('.', 1)[-1].lower() if '.' in self.file.filename else None

                if not self.file_extension or self.file_extension not in self.allowed_extensions['input']:
                    return self.create_error_response(f'Unsupported file extension: {self.file_extension}', 400)

                self.output_extension = request.form.get('extension')

                if self.output_extension not in self.allowed_extensions['output']:
                    return self.create_error_response(f'Unsupported output extension: {self.output_extension}', 400)
                
                self.mime_type, _ = mimetypes.guess_type(self.full_filename)

                if self.mime_type not in self.expected_mime_types.values():
                    return self.create_error_response(f'Unsupported MIME type: {self.mime_type}', 400)

                self.unique_id = str(uuid.uuid4())
                self.file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], f"{self.unique_id}_{self.full_filename}")
                self.file.save(self.file_path)

                try:
                    self.output_file = self.converter.base_converter(self.file_path, self.output_extension)

                except subprocess.CalledProcessError:
                    return self.create_error_response('Error running LibreOffice command', 500)
        
                except FileNotFoundError:
                    return self.create_error_response('File not found', 500)
        
                except Exception:
                    return self.create_error_response('Conversion failed', 500)

                if not self.output_file or not os.path.exists(self.output_file):
                    return self.create_error_response('Conversion failed, output file not found', 500)

                self.filename = self.full_filename.split('.')[0]
                self.output_filename = f"Conver - {self.filename}.{self.output_extension}"

                return send_file(self.output_file, as_attachment=True, download_name=self.output_filename), 200
            
            except KeyError:
                return self.create_error_response('File not found', 400)

            finally:
                if self.converter:
                    clean_up(self.file_path, self.output_file)
                    self.reset_optional_values()

    def run_production(self, host: str = '0.0.0.0', port: int = 5000) -> None:
        self.app.run(debug=False, host=host, port=port, use_reloader=False)