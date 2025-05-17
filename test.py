import os

for currentdir, dirs, files in os.walk('static/img'):
    print(len(files))