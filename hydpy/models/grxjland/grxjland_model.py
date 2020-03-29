# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

# imports...
import numpy
# ...from HydPy
from hydpy.core import modeltools
# ...from grxjland
from hydpy.models.grxjland import grxjland_inputs
from hydpy.models.grxjland import grxjland_fluxes
from hydpy.models.grxjland import grxjland_control
from hydpy.models.grxjland import grxjland_states
from hydpy.models.grxjland import grxjland_outlets
from hydpy.models.grxjland import grxjland_derived
from hydpy.models.grxjland import grxjland_logs


class Calc_En_Pn_V1(modeltools.Method):
    """ Calculate net rainfall and net evapotranspiration capacity.

    Basic equations:
    
        Determination of net rainfall and PE by subtracting E from P to determine either a net rainfall Pn or a net evapotranspiration capacity En:
    
      :math:`Pn = P - E, En = 0 \\ | \\ P \\geq E`
      
      :math:`Pn = 0,  En = E - P\\ | \\ P < E``

    Examples:
        
        Evapotranspiration larger than precipitation:
        
        >>> from hydpy.models.grxjland import *
        >>> parameterstep('1d')
        >>> inputs.p = 20.
        >>> inputs.e = 30.
        >>> model.calc_en_pn_v1()
        >>> fluxes.en
        en(10.0)
        >>> fluxes.pn
        pn(0.0)
        
        Precipitation larger than evapotranspiration:
        >>> inputs.p = 50.
        >>> inputs.e = 10.
        >>> model.calc_en_pn_v1()
        >>> fluxes.en
        en(0.0)
        >>> fluxes.pn
        pn(40.0)
    
    """
    
    REQUIREDSEQUENCES = (
        grxjland_inputs.P,
        grxjland_inputs.E,
    )
    RESULTSEQUENCES = (
        grxjland_fluxes.Pn,
        grxjland_fluxes.En,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        inp = model.sequences.inputs.fastaccess
        flu = model.sequences.fluxes.fastaccess
        
        if inp.p >= inp.e:
            flu.pn = inp.p - inp.e
            flu.en = 0.
        else:
            flu.pn = 0.
            flu.en = inp.e - inp.p
            

class Calc_Ps_V1(modeltools.Method):
    """ Calculate part of net rainfall filling the production store.

    Basic equation:
    
        In case Pn is not zero, a part Ps of Pn fills the production store. It is determined as a function of the level S in the store by:
    
      :math:`Ps = \\frac{X1(1-(\\frac{S}{X1}^{2}tanh(\\frac{Pn}{X1}){1+\\frac{S}{X1}tanh(\\frac{Pn}{X1})}`

    Examples:
        
        Example production store full, no rain fills the production store
        
        >>> from hydpy.models.grxjland import *
        >>> from hydpy import pub
        >>> parameterstep('1d')
        >>> pub.options.reprdigits = 6
        >>> x1(300)
        >>> states.s = 300
        >>> fluxes.pn = 50
        >>> model.calc_ps_v1()
        >>> fluxes.ps
        ps(0.0)
        
        Example routing store empty, nearly all net rainfall fills the production store:
        
        >>> states.s = 0
        >>> model.calc_ps_v1()
        >>> fluxes.ps
        ps(49.542124)
        
        Example no net rainfall:
        
        >>> fluxes.pn = 0
        >>> model.calc_ps_v1()
        >>> fluxes.ps
        ps(0.0)
    """
    
    REQUIREDSEQUENCES = (
        grxjland_fluxes.Pn,
        grxjland_states.S,
    )
    CONTROLPARAMETERS = (
        grxjland_control.X1,
    )
    
    RESULTSEQUENCES = (
        grxjland_fluxes.Ps,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        flu = model.sequences.fluxes.fastaccess
        sta = model.sequences.states.fastaccess
        con = model.parameters.control.fastaccess
        
        flu.ps = con.x1 * (1. - (sta.s / con.x1) ** 2.) * numpy.tanh(flu.pn / con.x1) / (1. + sta.s / con.x1 * numpy.tanh(flu.pn / con.x1))
        
class Calc_Es_Perc_S_V1(modeltools.Method):
    """ Calculate actual evaporation rate, water content and percolation leakage from the production store.

    Basic equations:
    
        Actual evaporation rate is determined as a function of the level in the production store to calculate the quantity 
        Es of water that will evaporate from the store. It is obtained by:
    
      :math:`Es = \\frac{S(2-\\frac{S}{X1}tanh(\\frac{En}{X1})}{1+(1-\\frac{S}{X1})tanh(\\frac{En}{X1})}`
      
        The water content in the production store is then updated with:
      
      :math:`S = S - Es + Ps`
      
        A percolation leakage Perc from the production store is then calculated as a power function of the reservoir content:
        
      :math:`Perc = S{1-[1+(\\frac{4 S}{9 X1})^{4}]^{-1/4}}`
      
        The reservoir content becomes:
        
      :math:`S = S- Perc`

    Examples:
        
        Example production store nearly full, no rain:
        
        >>> from hydpy.models.grxjland import *
        >>> from hydpy import pub
        >>> parameterstep('1d')
        >>> pub.options.reprdigits = 6
        >>> x1(300.)
        >>> fluxes.ps = 0.
        >>> fluxes.en = 10.
        >>> states.s = 270.
        >>> model.calc_es_perc_s_v1()
        >>> fluxes.es
        es(9.863469)
        >>> fluxes.perc
        perc(1.415145)
        >>> states.s
        s(258.721386)
        
        Check water balance:
        
        >>> 270. + fluxes.ps - fluxes.perc - fluxes.es - states.s
        0.0
        
        Example production store nearly full, rain:
        
        >>> fluxes.ps = 25.
        >>> fluxes.en = 0.
        >>> states.s = 270.
        >>> model.calc_es_perc_s_v1()
        >>> fluxes.es
        es(0.0)
        >>> fluxes.perc
        perc(2.630796)
        >>> states.s
        s(292.369204)
        
        Check water balance:
        
        >>> 270. + fluxes.ps - fluxes.perc - fluxes.es - states.s
        0.0
        
        Example production store empty, no rain
        
        >>> fluxes.ps = 0.
        >>> fluxes.en = 10.
        >>> states.s = 0.
        >>> model.calc_es_perc_s_v1()
        >>> fluxes.es
        >>> fluxes.perc
        >>> states.s
        
        Example production store empty, rain
        
        >>> fluxes.ps = 30.
        >>> fluxes.en = 0.
        >>> states.s = 0.
        >>> model.calc_es_perc_s_v1()
        >>> fluxes.es
        es(0.0)
        >>> fluxes.perc
        perc(0.000029)
        >>> states.s
        s(29.999971)
        
        Check water balance:
        
        >>> 0. + fluxes.ps - fluxes.perc - fluxes.es - states.s
        0.0
    """
    
    REQUIREDSEQUENCES = (
        grxjland_fluxes.Ps,
        grxjland_fluxes.En,
    )
    CONTROLPARAMETERS = (
        grxjland_control.X1,
    )

    UPDATEDSEQUENCES = (
        grxjland_states.S,
    )
    
    RESULTSEQUENCES = (
        grxjland_fluxes.Es,
        grxjland_fluxes.Perc,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        flu = model.sequences.fluxes.fastaccess
        sta = model.sequences.states.fastaccess
        con = model.parameters.control.fastaccess
        flu.es = (sta.s * (2. - sta.s / con.x1) * numpy.tanh(flu.en / con.x1)) / (1. + (1. - sta.s / con.x1) * numpy.tanh(flu.en / con.x1))
        sta.s = sta.s -flu.es + flu.ps
        # flu.perc = sta.s * (1. - (1. + (4. * sta.s / 9. / con.x1) ** 4.) ** (-0.25))
        # probably faster
        flu.perc = sta.s * (1. - (1. + (sta.s / con.x1) ** 4. / 25.62890625) ** (-0.25)) 
        sta.s = sta.s - flu.perc
        

class Calc_OutUH1_Q9_V1(modeltools.Method):
    """Calculate the unit hydrograph output (convolution).

    Examples:

        Prepare a unit hydrograph with only three ordinates:

        >>> from hydpy.models.grxjland import *
        >>> from hydpy import pub
        >>> parameterstep('1d')
        >>> simulationstep('1d')
        >>> pub.options.reprdigits = 6
        >>> x4(3)
        >>> derived.uh1.update()
        >>> derived.uh1
        uh1(0.06415, 0.298737, 0.637113)
        >>> logs.q9 = 1.0, 3.0, 0.0

        Without new input, the actual output is simply the first value
        stored in the logging sequence and the values of the logging
        sequence are shifted to the left:

        >>> fluxes.pr = 0.0
        >>> model.calc_outuh1_q9_v1()
        >>> fluxes.q9
        q9(1.0)
        >>> logs.q9
        q9(3.0, 0.0, 0.0)

        With an new input of 4mm, the actual output consists of the first
        value stored in the logging sequence and the input value
        multiplied with the first unit hydrograph ordinate.  The updated
        logging sequence values result from the multiplication of the
        input values and the remaining ordinates:

        >>> fluxes.pr = 4.0
        >>> model.calc_outuh1_q9_v1()
        >>> fluxes.q9
        q9(3.2566)
        >>> logs.q9
        q9(1.194949, 2.548451, 0.0)
        
        In the next example we set the memory to zero (no input in the past), and apply a single input signal:
        
        >>> logs.q9 = 0.0, 0.0, 0.0
        >>> fluxes.pr = 4.0
        >>> model.calc_outuh1_q9_v1()
        >>> fluxes.q9
        q9(3.2566)
        >>> fluxes.pr = 0.0
        >>> model.calc_outuh1_q9_v1()
        >>> fluxes.q9
        >>> model.calc_outuh1_q9_v1()
        >>> fluxes.q9
        q9(2.548451)
        >>> model.calc_outuh1_q9_v1()
        >>> fluxes.q9
        q9(0.0)
        
        A unit hydrograph with only one ordinate results in the direct
        routing of the input:
        
        >>> x4(3)
        >>> derived.uh1.update()
        >>> derived.uh1

        >>> derived.uh.shape = 1
        >>> derived.uh = 1.0
        >>> fluxes.inuh = 0.0
        >>> logs.quh.shape = 1
        >>> logs.quh = 0.0
        >>> model.calc_outuh_quh_v1()
        >>> fluxes.outuh
        outuh(0.0)
        >>> logs.quh
        quh(0.0)
        >>> fluxes.inuh = 4.0
        >>> model.calc_outuh_quh()
        >>> fluxes.outuh
        outuh(4.0)
        >>> logs.quh
        quh(0.0)
    """
    DERIVEDPARAMETERS = (
        grxjland_derived.UH1,
    )
    REQUIREDSEQUENCES = (
        grxjland_fluxes.Pr,
    )
    UPDATEDSEQUENCES = (
        grxjland_logs.Q9,
    )
    RESULTSEQUENCES = (
        grxjland_fluxes.Q9,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        der = model.parameters.derived.fastaccess
        flu = model.sequences.fluxes.fastaccess
        log = model.sequences.logs.fastaccess
        # 90 % of Pr enters UH1
        flu.q9 = der.uh1[0] * 0.9 * flu.pr + log.q9[0]
        for jdx in range(1, len(der.uh1)):
            log.q9[jdx - 1] = der.uh1[jdx] * 0.9 * flu.pr + log.q9[jdx]
            
class Calc_OutUH2_Q1_V1(modeltools.Method):
    """Calculate the unit hydrograph output (convolution).

    Examples:

        Prepare a unit hydrograph with only three ordinates:

        >>> from hydpy.models.grxjland import *
        >>> from hydpy import pub
        >>> parameterstep('1d')
        >>> simulationstep('1d')
        >>> pub.options.reprdigits = 6
        >>> x4(3)
        >>> derived.uh2.update()
        >>> derived.uh2
        uh2(0.06415, 0.298737, 0.637113)
        >>> logs.q1 = 1.0, 3.0, 0.0

        Without new input, the actual output is simply the first value
        stored in the logging sequence and the values of the logging
        sequence are shifted to the left:

        >>> fluxes.pr = 0.0
        >>> model.calc_outuh2_q1_v1()
        >>> fluxes.q1
        q1(1.0)
        >>> logs.q1
        q1(3.0, 0.0, 0.0)

        With an new input of 4mm, the actual output consists of the first
        value stored in the logging sequence and the input value
        multiplied with the first unit hydrograph ordinate.  The updated
        logging sequence values result from the multiplication of the
        input values and the remaining ordinates:

        >>> fluxes.pr = 4.0
        >>> model.calc_outuh2_q1_v1()
        >>> fluxes.q1
        q1(3.2566)
        >>> logs.q1
        q1(1.194949, 2.548451, 0.0)
        
        In the next example we set the memory to zero (no input in the past), and apply a single input signal:
        
        >>> logs.q1 = 0.0, 0.0, 0.0
        >>> fluxes.pr = 4.0
        >>> model.calc_outuh2_q1_v1()
        >>> fluxes.q1
        q1(3.2566)
        >>> fluxes.pr = 0.0
        >>> model.calc_outuh2_q1_v1()
        >>> fluxes.q1
        >>> model.calc_outuh2_q1_v1()
        >>> fluxes.q1
        q1(2.548451)
        >>> model.calc_outuh2_q1_v1()
        >>> fluxes.q1
        q1(0.0)
        
        A unit hydrograph with only one ordinate results in the direct
        routing of the input:
        
        >>> x4(3)
        >>> derived.uh2.update()
        >>> derived.uh2

        >>> derived.uh.shape = 1
        >>> derived.uh = 1.0
        >>> fluxes.inuh = 0.0
        >>> logs.quh.shape = 1
        >>> logs.quh = 0.0
        >>> model.calc_outuh_quh_v1()
        >>> fluxes.outuh
        outuh(0.0)
        >>> logs.quh
        quh(0.0)
        >>> fluxes.inuh = 4.0
        >>> model.calc_outuh_quh()
        >>> fluxes.outuh
        outuh(4.0)
        >>> logs.quh
        quh(0.0)
    """
    DERIVEDPARAMETERS = (
        grxjland_derived.UH2,
    )
    REQUIREDSEQUENCES = (
        grxjland_fluxes.Pr,
    )
    UPDATEDSEQUENCES = (
        grxjland_logs.Q1,
    )
    RESULTSEQUENCES = (
        grxjland_fluxes.Q1,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        der = model.parameters.derived.fastaccess
        flu = model.sequences.fluxes.fastaccess
        log = model.sequences.logs.fastaccess
        # 10 % of Pr enters UH2
        flu.q1 = der.uh2[0] * 0.1 * flu.pr + log.q1[0]
        for jdx in range(1, len(der.uh2)):
            log.q1[jdx - 1] = der.uh2[jdx] * 0.1 * flu.pr + log.q1[jdx]
            
class Calc_F_Qr_R_V1(modeltools.Method):
    """ Calculate groundwater exchange term F, level of the non-linear routing store R and the outflow Qr of the reservoir.

    Basic equations:
    
        The ground waterexchange term F that acts on both flow components is calculated as:
        
      :math:`F = X2 \frac{R}{X3}^{7/2}`
      
      
        X2 is the water exchange coefficient. X2 can be either positive in case of water imports, negative for water exports or zero when there is no water exchange.
        The  higher the level in the routing store, the larger the  exchange.
       
        The level in the routing store is updated by adding the output Q9 of UH1 and F:
      
      :math:`R = max(0; R + Q9 + F)`
      
        The outflow Qr of the reservoir is then calculated as:
        
      :math:`Qr = R{1-[1+(\\frac{R}{X3})^{4}]^{-1/4}}`
      
        The level in the reservoir becomes:
      
      :math:`R = R - Qr`
      

    Examples:
        
        Positive groundwater exchange coefficient, routing storage nearly full
        
        >>> from hydpy.models.grxjland import *
        >>> from hydpy import pub
        >>> parameterstep('1d')
        >>> pub.options.reprdigits = 6
        >>> x2(20.)
        >>> x3(100.)
        >>> fluxes.q9 = 20.
        >>> states.r = 95.
        >>> model.calc_f_qr_r_v1()
        >>> fluxes.f
        f(16.713316)
        >>> states.r
        r(93.079181)
        >>> fluxes.qr
        qr(38.634135)
        
        Positive groundwater exchange coefficient, routing storage nearly empty:
        
        >>> states.r = 10.
        >>> model.calc_f_qr_r_v1()
        >>> fluxes.f
        f(0.006325)
        >>> states.r
        r(29.945817)
        >>> fluxes.qr
        qr(0.060508)
        
        Negative groundwater exchange coefficient, routing storage nearly full
        
        >>> x2(-20.)
        >>> states.r = 95.
        >>> model.calc_f_qr_r_v1()
        >>> fluxes.f
        f(-16.713316)
        >>> states.r
        r(83.353723)
        >>> fluxes.qr
        qr(14.932961)
        
        Negative groundwater exchange coefficient, routing storage nearly empty:
        
        >>> states.r = 10.
        >>> model.calc_f_qr_r_v1()
        >>> fluxes.f
        f(-0.006325)
        >>> states.r
        r(29.933295)
        >>> fluxes.qr
        qr(0.060381)
        
        
    """
    
    REQUIREDSEQUENCES = (
        grxjland_fluxes.Q9,
    )
    CONTROLPARAMETERS = (
        grxjland_control.X2,
        grxjland_control.X3,
    )

    UPDATEDSEQUENCES = (
        grxjland_states.R,
    )
    
    RESULTSEQUENCES = (
        grxjland_fluxes.F,
        grxjland_fluxes.Qr,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        flu = model.sequences.fluxes.fastaccess
        sta = model.sequences.states.fastaccess
        con = model.parameters.control.fastaccess
        flu.f = con.x2 * (sta.r / con.x3) ** 3.5
        sta.r = numpy.maximum(0, sta.r + flu.q9 + flu.f)
        flu.qr = sta.r * (1 - (1 + (sta.r/con.x3)**4)**(-0.25))
        sta.r = sta.r - flu.qr
        
class Calc_Qd_V1(modeltools.Method):
    """ Calculate direct flow component.

    Basic equations:
    
        Output Q1 of unit hydrograph UH2 is subject to the same water exchange F as the routing storage to
        give the flow component as:
        
      :math:`Qd = max(0; Q1 + F)`
      
      
    Examples:
        
        Positive groundwater exchange: 
        
        >>> from hydpy.models.grxjland import *
        >>> parameterstep('1d')
        >>> fluxes.q1 = 20
        >>> fluxes.f = 20
        >>> model.calc_qd_v1()
        >>> fluxes.qd
        qd(40.0)
        
        Negative groundwater exchange:
        
        >>> fluxes.f = -10
        >>> model.calc_qd_v1()
        >>> fluxes.qd
        qd(10.0)
        
        Negative groundwater exchange exceeding outflow of unit hydrograph:
        >>> fluxes.f = -30
        >>> model.calc_qd_v1()
        >>> fluxes.qd
        
    """
    
    REQUIREDSEQUENCES = (
        grxjland_fluxes.Q1,
        grxjland_fluxes.F,
    )
    
    RESULTSEQUENCES = (
        grxjland_fluxes.Qd,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        flu = model.sequences.fluxes.fastaccess
        flu.qd = numpy.maximum(0, flu.q1 + flu.f)
        
class Calc_Qt_V1(modeltools.Method):
    """ Calculate total flow.

    Basic equations:
    
        Total streamflow is obtained by
    
      :math:`Qt = Qr + Qd`
    
      
    Examples:
        
        >>> from hydpy.models.grxjland import *
        >>> parameterstep('1d')
        >>> fluxes.qr = 20
        >>> fluxes.qd = 10
        >>> model.calc_qt_v1()
        >>> fluxes.qt
        qt(30.0)
        
    """
    
    REQUIREDSEQUENCES = (
        grxjland_fluxes.Qr,
        grxjland_fluxes.Qd,
    )
    
    RESULTSEQUENCES = (
        grxjland_fluxes.Qt,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        flu = model.sequences.fluxes.fastaccess
        flu.q = flu.qr + flu.qd
        
class Pass_Q_v1(modeltools.Method):
    """Update the outlet link sequence.

    Basic equation:
      :math:`Q = QFactor \\cdot QT`
      
    
    """
    DERIVEDPARAMETERS = (
        grxjland_derived.QFactor,
    )
    REQUIREDSEQUENCES = (
        grxjland_fluxes.Qt,
    )
    RESULTSEQUENCES = (
        grxjland_outlets.Q,
    )
    @staticmethod
    def __call__(model: modeltools.Model) -> None:
        der = model.parameters.derived.fastaccess
        flu = model.sequences.fluxes.fastaccess
        out = model.sequences.outlets.fastaccess
        out.q[0] += der.qfactor*flu.qt


class Model(modeltools.AdHocModel):
    """The HydPy-H-Land base model."""
    INLET_METHODS = ()
    RECEIVER_METHODS = ()
    RUN_METHODS = (
        Calc_En_Pn_V1,
        Calc_Ps_V1,
        Calc_Es_Perc_S_V1,
        Calc_OutUH1_Q9_V1,
        Calc_OutUH2_Q1_V1,
        Calc_F_Qr_R_V1,
        Calc_Qd_V1,
        Calc_Qt_V1,
    )
    ADD_METHODS = ()
    OUTLET_METHODS = (
        Pass_Q_v1,
    )
    SENDER_METHODS = ()
