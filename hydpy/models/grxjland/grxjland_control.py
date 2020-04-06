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

class Z(parametertools.Parameter):
    """Mean subbasin elevation [m]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (1e-10, None)

class NSnowLayers(parametertools.Parameter):
    """Number of snow layers  [-].

    Note that |NmbZones| determines the length of the 1-dimensional
    HydPy-GRXJ-Land snow parameters and sequences.  This required that the value of
    the respective |NSnowLayers| instance is set before any of the values
    of these 1-dimensional parameters or sequences are set.  Changing the
    value of the |NSnowLayers| instance necessitates setting their values
    again.

    Examples:

        >>> from hydpy.models.grxjland import *
        >>> parameterstep('1d')
        >>> nsnowlayers(5)
    """
    NDIM, TYPE, TIME, SPAN = 0, int, None, (1, 101)

    def __call__(self, *args, **kwargs):
        """The prefered way to pass a value to |NmbZones| instances within
        parameter control files.  Sets the shape of most 1-dimensional
        snow parameter objects and sequence objects
        additionally.
        """
        super().__call__(*args, **kwargs)
        self.subpars.pars.model.parameters.derived.zlayers.shape = self.value
        self.subpars.pars.model.sequences.fluxes.player.shape = self.value

class HypsoData(parametertools.Parameter):
    """Array of length 101 : min, q01 to q99 and max of catchment elevation distribution [m]."""
    NDIM, TYPE, TIME, SPAN = 1, float, None, (0, None)

    def __call__(self, *args, **kwargs):
        """Set shape of HypsoData to 1010
        """
        self.shape = 101
        super().__call__(*args, **kwargs)


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
    
class X5(parametertools.Parameter):
    """Intercatchment exchange threshold [-]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (None, None)
    
class X6(parametertools.Parameter):
    """coefficient for emptying exponential store [mm]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (0, None)
    


