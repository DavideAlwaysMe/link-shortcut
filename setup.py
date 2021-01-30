import os
import subprocess
from setuptools import setup

#cartella home tramite comando terminale
home = subprocess.check_output(['xdg-user-dir', 'HOME']).decode("utf-8").rstrip()
#dove salvare l'icona
icon_path=home+"/.icons"

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
    package_data = {'link': ['icona.png']},
    install_requires = [ 'requests','favicon'],
)
