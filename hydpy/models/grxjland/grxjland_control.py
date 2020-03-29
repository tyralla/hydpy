# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

# import...
# from site-packages
import numpy
# ...from HydPy
from hydpy.core import parametertools
# ...from grxjland
from hydpy.core import objecttools

class Area(parametertools.Parameter):
    """Subbasin area [km²]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (1e-10, None)

class X1(parametertools.Parameter):
    """Maximum capacity of the production storage [mm]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (0, None)
    
class X2(parametertools.Parameter):
    """groundwater exchange coefficient [mm]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (None, None)
    
class X3(parametertools.Parameter):
    """One timestep ahead maximum capacity of the routing store [mm]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (0, None)
    
class X4(parametertools.Parameter):
    """Time base of unit hydrographs UH1 (X4) and UH2 (2*X4) [d]."""
    NDIM, TYPE, TIME, SPAN = 0, float, False, (0.5, None)
