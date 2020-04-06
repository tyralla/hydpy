# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

from hydpy.core import sequencetools

class En(sequencetools.FluxSequence):
    """Net evapotranspiration capacity [mm]."""
    NDIM, NUMERIC = 0, False

class PLayer(sequencetools.FluxSequence):
    """Rainfall of each snow layer[mm]."""
    NDIM, NUMERIC = 1, False

class TLayer(sequencetools.FluxSequence):
    """Mean air temperature of each snow layer [°C]."""
    NDIM, NUMERIC = 1, False

class Pn(sequencetools.FluxSequence):
    """Net rainfall [mm]."""
    NDIM, NUMERIC = 0, False
    
class Ps(sequencetools.FluxSequence):
    """Part of Pn filling the production store [mm]."""
    NDIM, NUMERIC = 0, False
    
class Es(sequencetools.FluxSequence):
    """Actual evaporation rate [mm]."""
    NDIM, NUMERIC = 0, False
    
class Pr(sequencetools.FluxSequence):
    """Total quantity of water reaching routing functions [mm]."""
    NDIM, NUMERIC = 0, False
    
class Perc(sequencetools.FluxSequence):
    """Percolation leakage [mm]."""
    NDIM, NUMERIC = 0, False
    
class Q9(sequencetools.FluxSequence):
    """Output of unit hydrograph UH1 [mm]."""
    NDIM, NUMERIC = 0, False
    
class Q1(sequencetools.FluxSequence):
    """Output of unit hydrograph UH2 [mm]."""
    NDIM, NUMERIC = 0, False
    
class F(sequencetools.FluxSequence):
    """Groundwater exchange term [mm]."""
    NDIM, NUMERIC = 0, False
class Qr(sequencetools.FluxSequence):
    """Outflow of the routing storage [mm]."""
    NDIM, NUMERIC = 0, False
class Qr2(sequencetools.FluxSequence):
    """Outflow of the exponential storage [mm]."""
    NDIM, NUMERIC = 0, False
class Qd(sequencetools.FluxSequence):
    """Flow component direct flow [mm]."""
    NDIM, NUMERIC = 0, False
class Qt(sequencetools.FluxSequence):
    """Total streamflow [mm]."""
    NDIM, NUMERIC = 0, False

