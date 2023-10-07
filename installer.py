#!/usr/bin/python3
import os

modules = ['ping3', 'psutil']
try:
    os.system(f"pip3 install {' '.join(modules)}")
except:
    print("")
