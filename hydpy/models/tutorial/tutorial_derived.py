# -*- coding: utf-8 -*-

from hydpy.core import parametertools
from hydpy.models.tutorial import tutorial_control

class QFactor(parametertools.Parameter):
    """Factor for converting mm/stepsize to m³/s."""
    NDIM, TYPE, TIME, SPAN = 0, float, None, (0., None)

    CONTROLPARAMETERS = (
        tutorial_control.Area,
    )

    def update(self):
        """Update |QFactor| based on |Area| and the current simulation
        step size.

        >>> from hydpy.models.tutorial import *
        >>> from hydpy import pub
        >>> parameterstep('1d')
        >>> simulationstep('1d')
        >>> pub.options.reprdigits = 6
        >>> area(50.0)
        >>> derived.qfactor.update()
        >>> derived.qfactor
        qfactor(0.578704)
        
        change simulatio step to 1 h
        
        >>> simulationstep('1h')
        >>> derived.qfactor.update()
        >>> derived.qfactor
        qfactor(13.888889)
        
        """
        self(self.subpars.pars.control.area*1000. /
             self.subpars.qfactor.simulationstep.seconds)
