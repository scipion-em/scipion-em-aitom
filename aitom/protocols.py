# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     you (you@yourinstitution.email)
# *
# * your institution
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'you@yourinstitution.email'
# *
# **************************************************************************
import json
import os
from os.path import dirname

from aitom import Plugin
from pyworkflow.em import EMProtocol
from pyworkflow.protocol import Protocol, params
from pyworkflow.utils.properties import Message
from tomo.objects import Coordinate3D
from tomo.protocols import ProtTomoBase

from aitom.convert import json2Coordinates3D

OUTPUT_EXT = ".json"

"""
Describe your python module here:
This module will provide the traditional Hello world example
"""

class AiTomPicking(ProtTomoBase, EMProtocol):
    """ This protocol will pick 3d particles in a tomogram"""
    _label = 'picking'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ Define the input parameters that will be used.
        Params:
            form: this is the form to be populated with sections and params.
        """
        # You need a params to belong to a section:
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputTomograms', params.PointerParam,
                      pointerClass='SetOfTomograms',
                      label='Tomograms', important=True,
                      help='Tomograms to be picked.')

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        deps = []
        # Let's load input data for the already existing tomograms
        for tomogram in self.inputTomograms.get().iterItems():

            pickingStepId = self._insertFunctionStep('pickTomogramStep',
                                                tomogram)

            deps.append(pickingStepId)

        self._insertFunctionStep('createOutputStep', prerequisites=deps)

    def pickTomogramStep(self, tomogram ):

        # pick this tomogram
        tomofile = tomogram.getFileName()
        output = os.path.basename(tomofile) + OUTPUT_EXT
        print("need to pick %s" % tomogram.getFileName())
        print("output going here --> %s" % self._getExtraPath(output))

        args= []
        args.append(tomogram.getFileName())
        args.append(self._getExtraPath(output))

        Plugin.runAitom(self, 'picking', args)

    def createOutputStep(self):

        # Create the output set of coordinates
        coordinates = self._createSetOfCoordinates3D(self.inputTomograms.get())

        # Note we need a box size!!
        coordinates.setBoxSize(100)

        # For each output file
        for jsonFile in os.listdir(self._getExtraPath()):

            if jsonFile.endswith(OUTPUT_EXT):
                json2Coordinates3D(self._getExtraPath(jsonFile), coordinates)

        self._defineOutputs(output3DCoordinates=coordinates)

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        if self.isFinished():

            summary.append("This protocol has printed *%s* %i times." % (self.message, self.times))
        return summary

    def _methods(self):
        methods = []

        if self.isFinished():
            methods.append("%s has been printed in this run %i times." % (self.message, self.times))
            if self.previousCount.hasPointer():
                methods.append("Accumulated count from previous runs were %i."
                               " In total, %s messages has been printed."
                               % (self.previousCount, self.count))
        return methods