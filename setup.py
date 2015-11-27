#-*- coding: utf-8 -*-
__author__ = 'muti'

import os
from setuptools import setup

def package_data(pkg, root):
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}

setup(
    name='zplayer-xblock',
    version='0.1',
    description='Zplayer XBlock',
    packages=[
        'zplayer',
    ],
    # py_modules=['zplayer'],
    install_requires=['XBlock', 'requests'],
    entry_points={
        'xblock.v1': [
            'zplayer = zplayer:ZplayerXBlock',
        ]
    },
    package_data=package_data("zplayer", "static")
)
