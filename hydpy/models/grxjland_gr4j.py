# -*- coding: utf-8 -*-
# pylint: disable=line-too-long, wildcard-import, unused-wildcard-import
"""
Gr4J Version of the GrXJ-Land model.
The model can briefly be summarized as follows:

TODO

The following figure shows the general structure of HydPy GrXJ-Land Version Gr4J:

.. image:: HydPy-GrXJ-Land_Version-Gr4J.png

Integration tests:

    All integration tests are performed over a period of 50 days with
    a simulation step of one day:

    >>> from hydpy import pub
    >>> pub.timegrids = '01.01.2000', '20.02.2000', '1d'

    Prepare the model instance and build the connections to element `land`
    and node `outlet`:

    >>> from hydpy.models.grxjland import *
    >>> parameterstep('1d')
    >>> simulationstep('1d')
    >>> from hydpy import Node, Element
    >>> outlet = Node('outlet')
    >>> land = Element('land', outlets=outlet)
    >>> land.model = model

    All tests are performed using a lumped basin with a size of
    100 km²:

    >>> area(100.0)

    Initialize a test function object, which prepares and runs the tests
    and prints their results for the given sequences:

    >>> from hydpy import IntegrationTest
    >>> IntegrationTest.plotting_options.height = 900
    >>> IntegrationTest.plotting_options.activated=(
    ...     inputs.e, inputs.p, fluxes.qt)
    >>> test = IntegrationTest(land)
    >>> test.dateformat = '%d.%m. %H:00'

    .. _grxjland_gr4j_ex1:

    **Example 1**

    We use the example of the Gr4J Implementation of the airGR package
    
    Set control parameters:
    
    >>> x1(257.238)
    >>> x2(1.012)
    >>> x3(88.235)
    >>> x4(2.208)
    
    Set initial storage levels: production store 30% filled, routing store 50% filled. log.sequences empty
    

    >>> test.inits = ((states.s, 0.3 * x1.value),
    ...               (states.r, 0.5 * x3.value),
    ...               (logs.q9, [0,0,0]),
    ...               (logs.q1, [0,0,0,0,0]))

    Input sequences |P| and |E|:

    >>> inputs.p.series = (
    ...     4.1, 15.9,  0.8,  0.0,  0.0,  0.0,  0.0,  0.0,  2.9,  0.0,  2.9,  5.8,  7.4,  0.0,  1.2,
    ...     0.0,  0.0,  0.1,  0.0, 11.7,  0.0,  0.0,  0.0,  3.0,  1.1, 13.9,  4.3,  2.0,  1.1,  0.6,
    ...     0.0,  5.6,  1.8,  6.1,  1.8,  0.0,  0.0,  3.5, 10.0,  0.0,  2.0,  9.1,  3.7, 23.5,  1.6,
    ...     0.0,  2.9,  3.9,  1.3,  0.6)
    
    >>> inputs.e.series = (
    ...     0.2, 0.2, 0.3, 0.3, 0.1, 0.3, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.5, 0.5, 0.5, 0.4, 0.4,
    ...     0.5, 0.2, 0.1, 0.1, 0.2, 0.2, 0.3, 0.4, 0.3, 0.2, 0.0, 0.0, 0.4, 0.6, 0.7, 0.5, 0.6, 0.9, 1.1,
    ...     0.6, 0.5, 0.5, 0.7, 0.6, 0.5, 0.5, 0.5, 0.7, 0.8, 0.7, 0.6)


    >>> test('grxjland_gr4j_ex1')

    .. raw:: html

        <iframe
            src="grxjland_gr4j_ex1.html"
            width="100%"
            height="930px"
            frameborder=0
        ></iframe>


"""

# import...
# ...from HydPy
from hydpy.exe.modelimports import *
from hydpy.core import modeltools
# ...from  grxjland
from hydpy.models.grxjland import grxjland_model


class Model(modeltools.AdHocModel):
    INLET_METHODS = ()
    RECEIVER_METHODS = ()
    RUN_METHODS = (
        grxjland_model.Calc_En_Pn_V1,
        grxjland_model.Calc_Ps_V1,
        grxjland_model.Calc_Es_Perc_S_V1,
        grxjland_model.Calc_OutUH1_Q9_V1,
        grxjland_model.Calc_OutUH2_Q1_V1,
        grxjland_model.Calc_F_Qr_R_V1,
        grxjland_model.Calc_Qd_V1,
        grxjland_model.Calc_Qt_V1,
    )
    ADD_METHODS = ()
    OUTLET_METHODS = (
        grxjland_model.Pass_Q_v1,
    )
    SENDER_METHODS = ()


tester = Tester()
#cythonizer = Cythonizer()
#cythonizer.finalise()
