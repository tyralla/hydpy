# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

from hydpy.core import sequencetools


class P(sequencetools.InputSequence):
    """Precipitation [mm]."""
    NDIM, NUMERIC = 0, False


class T(sequencetools.InputSequence):
    """Air temperature [°C]."""
    NDIM, NUMERIC = 0, False


class E(sequencetools.InputSequence):
    """Potential Evapotranspiration (PE) [mm]."""
    NDIM, NUMERIC = 0, False

