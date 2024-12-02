from flasgger import Swagger as Flasgger
from flask import Flask

def init_flasgger(app: Flask) -> None:
    Flasgger(app, template={
        'swagger': '2.0',
        'info': {
            'title': 'Conver Flask API',
            'version': '1.0.0',
            'description': 'Flask API for document conversion.'
        },
        'basePath': '',
        'paths': {
            '/converter': {
                'post': {
                    'parameters': [
                        {
                            'name': 'file',
                            'in': 'formData',
                            'type': 'file',
                            'required': True,
                            'description': 'File to be converted. Allowed extensions: doc, docx, odt, txt, rtf'
                        },
                        {
                            'name': 'extension',
                            'in': 'formData',
                            'type': 'string',
                            'required': True,
                            'enum': ['pdf', 'doc', 'docx', 'odt', 'txt', 'rtf'],
                            'description': 'Desired output file extension. Supported formats: pdf, doc, docx, odt, txt, rtf'
                        }
                    ],
                    'responses': {
                        200: {
                            'description': 'File converted successfully',
                            'schema': {
                                'type': 'application/octet-stream',
                                'example': 'Conver - filename.pdf'
                            }
                        },
                        400: {
                            'description': 'Bad Request',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'error': {
                                        'type': 'string',
                                        'example': 'Unsupported file extension: xlsx'
                                    }
                                }
                            }
                        },
                        413: {
                            'description': 'File size exceeds the maximum limit of 50 MB',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'error': {
                                        'type': 'string',
                                        'example': 'File size exceeds the maximum limit of 50 MB.'
                                    }
                                }
                            }
                        },
                        500: {
                            'description': 'Internal Server Error',
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'error': {
                                        'type': 'string',
                                        'example': 'Conversion failed, output file not found'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    })
