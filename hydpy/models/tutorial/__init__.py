# -*- coding: utf-8 -*-
"""
Simple model for educational purposes
"""
# import...
# ...from HydPy
from hydpy.exe.modelimports import *
# ...from tutorial
from hydpy.models.tutorial.tutorial_model import Model

# create object to test the doctests of the implemented methods and classes
tester = Tester()

# create object to compile code in C
cythonizer = Cythonizer()
cythonizer.finalise()


