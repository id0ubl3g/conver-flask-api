from src.modules.conver import Conver
from src.utils.system_utils import *

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS

import subprocess
import mimetypes
import uuid
import os

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.converter = Conver()

        UPLOAD_FOLDER = 'src/temp'
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
        self.app.errorhandler(413)(self.too_large)
        self._register_routes()

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        self.allowed_extensions = {
            'input': ['doc', 'docx', 'odt', 'txt', 'rtf'],
            'output': ['pdf', 'doc', 'docx', 'odt', 'txt', 'rtf']
        }

        self.expected_mime_types = {
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'odt': 'application/vnd.oasis.opendocument.text',
            'txt': 'text/plain',
            'rtf': 'application/rtf'
        }

    def create_error_response(self, message, code):
        return jsonify({'error': message}), code
    
    def too_large(self, error):
        return self.create_error_response('File size exceeds the maximum limit of 50 MB.', 413)

    def _register_routes(self):
        @self.app.route('/converter', methods=['POST'])
        def convert_file():
            file_path = None
            output_file = None

            try:
                file = request.files['file']

                if not file:
                    return self.create_error_response('No file uploaded', 400)

                file_name = secure_filename(file.filename)

                file_extension = file_name.rsplit('.', 1)[-1].lower() if '.' in file.filename else None

                if not file_extension or file_extension not in self.allowed_extensions['input']:
                    return self.create_error_response(f'Unsupported file extension: {file_extension}', 400)

                output_extension = request.form.get('extension')

                if output_extension not in self.allowed_extensions['output']:
                    return self.create_error_response(f'Unsupported output extension: {output_extension}', 400)
                
                mime_type, _ = mimetypes.guess_type(file_name)

                if mime_type not in self.expected_mime_types.values():
                    return self.create_error_response(f'Unsupported MIME type: {mime_type}', 400)

                unique_id = str(uuid.uuid4())
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], f"{unique_id}_{file_name}")
                file.save(file_path)

                self.converter = Conver()

                try:
                    output_file = self.converter.base_converter(file_path, output_extension)

                except subprocess.CalledProcessError:
                    return self.create_error_response('Error running LibreOffice command', 500)
        
                except FileNotFoundError:
                    return self.create_error_response('File not found', 500)
        
                except Exception:
                    return self.create_error_response('Conversion failed', 500)

                if not output_file or not os.path.exists(output_file):
                    return self.create_error_response('Conversion failed, output file not found', 500)

                filename = file_name.split('.')[0]
                output_filename = f"Conver - {filename}.{output_extension}"

                return send_file(output_file, as_attachment=True, download_name=output_filename), 200
            
            except KeyError:
                return self.create_error_response('File not found', 400)

            finally:
                if self.converter:
                    clean_up(file_path, output_file)
    
    def run_development(self, host='127.0.0.1', port=5000):
        self.app.run(debug=True, host=host, port=port, use_reloader=True)

    def run_production(self, host='0.0.0.0', port=5000):
        self.app.run(debug=False, host=host, port=port, use_reloader=False)


            
