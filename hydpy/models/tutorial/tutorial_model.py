# -*- coding: utf-8 -*-

from hydpy.core import modeltools
from hydpy.models.tutorial import tutorial_inputs
from hydpy.models.tutorial import tutorial_fluxes
from hydpy.models.tutorial import tutorial_control
from hydpy.models.tutorial import tutorial_states
from hydpy.models.tutorial import tutorial_outlets
from hydpy.models.tutorial import tutorial_derived

class Calc_Storage1_V1(modeltools.Method):
    """ Calculate water content and outflow of storage 1.
        
        Basic equations: 
        
      :math:`F2 = \\Bigl \\lbrace
      {
      {S1 + F1 - MaxS1 \\ | \\ S1 + F1 > MaxS1}
      \\atop
      {0 \\ | \\ S1 + F1 \\leq MaxS1}
      }`
      
      :math:`S1 = S1 + F1`
    

    Examples:
        
        Outflow of storage 1 S1 + F1 > MaxS1
        
        >>> from hydpy.models.tutorial import *
        >>> parameterstep('1d')
        >>> maxs1(200)
        >>> inputs.f1 = 50.
        >>> states.s1 = 180.
        >>> model.calc_storage1()
        >>> fluxes.f2
        f2(30.0)
        >>> states.s1
        s1(200.0)
        
        No outflow of storage 1
        >>> states.s1 = 20.
        >>> model.calc_storage1()
        >>> fluxes.f2
        f2(0.0)
        >>> states.s1
        s1(70.0)
        
    """
    
    REQUIREDSEQUENCES = (
        tutorial_inputs.F1,
    )
    CONTROLPARAMETERS = (
        tutorial_control.MaxS1,
    )

    UPDATEDSEQUENCES = (
        tutorial_states.S1,
    )
    
    RESULTSEQUENCES = (
        tutorial_fluxes.F2,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        inp = model.sequences.inputs.fastaccess
        flu = model.sequences.fluxes.fastaccess
        sta = model.sequences.states.fastaccess
        con = model.parameters.control.fastaccess
        sta.s1 = sta.s1 + inp.f1
        if sta.s1 > con.maxs1:
            flu.f2 = sta.s1 - con.maxs1
            sta.s1 = sta.s1 - flu.f2
        else:
            flu.f2 = 0.
        

class Calc_Storage2_V1(modeltools.Method):
    """ Calculate water content and outflow of storage 2.
    
        Basic equations:
        
      :math:`S2 = S2 + F2` 
        
      :math:`F3 = \\frac{1}{KS2}S2`
      
      :math:`S2 = S2 - F3`    

    Examples:
        
        Empty Storage 2:
        
        >>> from hydpy.models.tutorial import *
        >>> parameterstep('1d')
        >>> simulationstep('1d')
        >>> ks2(10.)
        >>> fluxes.f2 = 50.
        >>> states.s2 = 10.
        >>> model.calc_storage2()
        >>> fluxes.f3
        f3(6.0)
        >>> states.s2
        s2(54.0)
        
        Large storage content Storage 2:
        >>> states.s2 = 400.
        >>> model.calc_storage2()
        >>> fluxes.f3
        f3(45.0)
        >>> states.s2
        s2(405.0)
        
    """
    
    REQUIREDSEQUENCES = (
        tutorial_fluxes.F2,
    )
    CONTROLPARAMETERS = (
        tutorial_control.KS2,
    )

    UPDATEDSEQUENCES = (
        tutorial_states.S2,
    )
    
    RESULTSEQUENCES = (
        tutorial_fluxes.F3,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        flu = model.sequences.fluxes.fastaccess
        sta = model.sequences.states.fastaccess
        con = model.parameters.control.fastaccess
        sta.s2 = sta.s2 + flu.f2
        flu.f3 = sta.s2 / con.ks2
        sta.s2 = sta.s2 - flu.f3
        

class Pass_Q_V1(modeltools.Method):
    """Update the outlet link sequence.

    Basic equation:
      :math:`Q = QFactor \\cdot QT`
      
    
    """
    DERIVEDPARAMETERS = (
        tutorial_derived.QFactor,
    )
    REQUIREDSEQUENCES = (
        tutorial_fluxes.F3,
    )
    RESULTSEQUENCES = (
        tutorial_outlets.Q,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        der = model.parameters.derived.fastaccess
        flu = model.sequences.fluxes.fastaccess
        out = model.sequences.outlets.fastaccess
        out.q[0] += der.qfactor*flu.f3
        

class Model(modeltools.AdHocModel):
    """Definition of the base model of the simple tutorial model with 2 storages.
    """
    INLET_METHODS = ()
    RECEIVER_METHODS = ()
    RUN_METHODS = (
        Calc_Storage1_V1,
        Calc_Storage2_V1,
    )
    ADD_METHODS = ()
    OUTLET_METHODS = (
        Pass_Q_V1,
    )
    SENDER_METHODS = ()

