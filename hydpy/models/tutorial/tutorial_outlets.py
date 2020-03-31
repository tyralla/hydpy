# -*- coding: utf-8 -*-


from hydpy.core import sequencetools


class Q(sequencetools.OutletSequence):
    """Runoff [m3/s]."""
    NDIM, NUMERIC = 0, False
