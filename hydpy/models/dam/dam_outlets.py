# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

# import...
# ...from standard library
from __future__ import division, print_function
# ...HydPy specific
from hydpy.core import sequencetools


class Q(sequencetools.LinkSequence):   # pylint: disable=invalid-name
    """Discharge [m³/s]."""
    NDIM, NUMERIC = 0, False


class S(sequencetools.LinkSequence):   # pylint: disable=invalid-name
    """Water Supply [m³/s]."""
    NDIM, NUMERIC = 0, False


class OutletSequences(sequencetools.LinkSequences):
    """Downstream link sequences of the dam model."""
    _SEQCLASSES = (Q,
                   S)
