# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

from hydpy.core import sequencetools

class F2(sequencetools.FluxSequence):
    """Outflow of storage 1 [mm]"""
    NDIM, NUMERIC = 0, False


class F3(sequencetools.FluxSequence):
    """Outflow of storage 2 [mm]"""
    NDIM, NUMERIC = 0, False