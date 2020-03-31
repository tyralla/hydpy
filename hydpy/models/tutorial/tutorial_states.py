# -*- coding: utf-8 -*-

from hydpy.core import sequencetools
from hydpy.models.tutorial import tutorial_control

class S1(sequencetools.StateSequence):
    """Water content storage 1 [mm]."""
    NDIM, NUMERIC, SPAN = 0, False, (0., None)

    CONTROLPARAMETERS = (
        tutorial_control.MaxS1,
    )

    def trim(self, lower=None, upper=None):
        """Trim values in accordance with :math:`S1 \\leq MaxS1`.

        >>> from hydpy.models.tutorial import *
        >>> parameterstep('1d')
        >>> maxs1(200.0)
        >>> states.s1(-100.0)
        >>> states.s1
        s1(0.0)
        >>> states.s1(300.0)
        >>> states.s1
        s1(200.0)
        """
        if upper is None:
            upper = self.subseqs.seqs.model.parameters.control.maxs1
        super().trim(lower, upper)


class S2(sequencetools.StateSequence):
    """Water content storage 2 [mm]."""
    NDIM, NUMERIC, SPAN = 0, False, (0., None)

