#!/usr/bin/env python
from distutils.core import setup
import sys
if sys.version_info >= (3, 0):
    tkinter = "tkinter"
else:
    tkinter = "Tkinter"
    
setup(name='pick-geometry',
      version='1.0',
      description='GUI tool to query location on an image from user',
      author='Dmitry Shintyakov',
      author_email='shintyakov@gmail.com',
      url='https://github.com/dmishin/pick-geometry',
      packages=[],
      scripts=['pick-geometry'],
      license='MIT',
      requires=["PIL",tkinter]
)
