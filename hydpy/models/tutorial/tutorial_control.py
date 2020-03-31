# -*- coding: utf-8 -*-

from hydpy.core import parametertools

class Area(parametertools.Parameter):
    """Subbasin area [km²]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (1e-10, None)


class MaxS1(parametertools.Parameter):
    """Maximum capacity of storage 1 [mm]."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (0, None)


class KS2(parametertools.Parameter):
    """Outflow coefficient of storage 2 [T]."""
    NDIM, TYPE, TIME, SPAN = 0, float, False, (0, None)