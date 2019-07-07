'''
File for deploying with mod_wsgi on Apache
'''
import sys

sys.path.insert(0, "absolute/path/to/your/application/folder")

from chat import app as application
