#!/usr/bin/python3
import os

modules = ['ping3', 'psutil', 'python_arptable']
try:
    os.system(f"pip3 install {' '.join(modules)}")
except:
    print("")
