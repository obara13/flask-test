"""
This script runs the isicon01 application using a development server.
"""

from os import environ
from isicon01 import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '80'))
    except ValueError:
        PORT = 81
    app.run(HOST, PORT)

