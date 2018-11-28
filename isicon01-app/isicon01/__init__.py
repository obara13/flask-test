"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import isicon01.views
import isicon01.admin
