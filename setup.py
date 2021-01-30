import os
from setuptools import setup

setup(
    name = "link",
    version = "0.1",
    author = "Davide Rizzuto",
    author_email = "yodadr01@gmail.com",
    license = "MIT",
    url = "https://github.com/DavideAlwaysMe/link-shortcut",
    packages=['link'],
    scripts = ['link/link.py'],
    data_files = [
        ('/usr/share/applications', ['link.desktop']),('/usr/share/pixmaps',['icona.png'])
    ],
    install_requires = [ 'requests','favicon'],
)
