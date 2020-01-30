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
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
import os
from os.path import dirname

import pyworkflow.em
from pyworkflow import Config
from pyworkflow.utils import Environ

CONDA_ACTIVATION_CMD_VAR = 'CONDA_ACTIVATION_CMD'
AITOM_ENV_ACTIVATION = 'AITOM_ENV_ACTIVATION'

DEFAULT_VERSION = '0.0.1'
def getAITomoEnvName(version=DEFAULT_VERSION):
    return "aitom-%s" % version

DEFAULT_ACTIVATION_CMD = 'conda activate ' + getAITomoEnvName()

_logo = "logo.gif"
_references = ['you2019']

class Plugin(pyworkflow.em.Plugin):

    _condaActivationCmd = None

    @classmethod
    def _defineVariables(cls):
        cls._defineVar(AITOM_ENV_ACTIVATION, DEFAULT_ACTIVATION_CMD)

    @classmethod
    def getCondaActivationCmd(cls):

        if cls._condaActivationCmd is None:
            condaActivationCmd = os.environ.get(CONDA_ACTIVATION_CMD_VAR, "")
            correctCondaActivationCmd = condaActivationCmd.replace(
                Config.SCIPION_HOME + "/", "")
            if not correctCondaActivationCmd:
                print("WARNING!!: %s variable not defined. "
                      "Relying on conda being in the PATH" % CONDA_ACTIVATION_CMD_VAR)
            elif correctCondaActivationCmd[-1] not in [";", "&"]:
                correctCondaActivationCmd += "&&"

            cls._condaActivationCmd = correctCondaActivationCmd

        return cls._condaActivationCmd

    @classmethod
    def getAitomEnvActivation(cls):
        activation = cls.getVar(AITOM_ENV_ACTIVATION)
        scipionHome = pyworkflow.Config.SCIPION_HOME + os.path.sep

        return activation.replace(scipionHome, "", 1)

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch aitom. """
        environ = Environ(os.environ)
        if 'PYTHONPATH' in environ:
            # this is required for python virtual env to work
            del environ['PYTHONPATH']
        return environ

    @classmethod
    def runAitom(cls, protocol, program, args, cwd=None):
        """ Run Aitom command from a given protocol. """
        #program = os.path.join(
        #    dirname(protocol.getClassPackage().__file__),
        #    "scripts",
        #    program)

        fullProgram = '%s %s && %s' % (cls.getCondaActivationCmd(), cls.getAitomEnvActivation(), program)
        protocol.runJob(fullProgram, args, env=cls.getEnviron(), cwd=cwd)

    @classmethod
    def defineBinaries(cls, env):

        cls.addAITomoPackage(env, default=bool(cls.getCondaActivationCmd()))


    @classmethod
    def addAITomoPackage(cls, env, version=DEFAULT_VERSION, default=False):

        AITOMO_INSTALLED = 'aitom_%s_installed' % version
        ENV_NAME = getAITomoEnvName(version)

        # try to get CONDA activation command
        installationCmd = cls.getCondaActivationCmd()

        # Create the environment
        installationCmd += 'conda create -y -n %s -c anaconda python=3.6 &&' % ENV_NAME

        # Activate new the environment
        installationCmd += 'conda activate %s &&' % ENV_NAME

        # Install downloaded code
        installationCmd += 'pip install -r requirements.txt &&'

        installationCmd += 'pip install . &&'
        # Build it
        installationCmd += 'sh build.sh &&'

        # Flag installation finished
        installationCmd += 'touch %s' % AITOMO_INSTALLED

        aitom_commands = [(installationCmd, AITOMO_INSTALLED)]

        envPath = os.environ.get('PATH', "")  # keep path since conda likely in there
        installEnvVars = {'PATH': envPath} if envPath else None
        env.addPackage('aitom', version=version,
                       # url='https://github.com/pconesa/aitom/archive/V%s.tar.gz' % version,
                       url='https://github.com/xulabs/aitom/archive/%s.tar.gz' % version,
                       tar='aitom-%s.tar.gz' % version,
                       commands=aitom_commands,
                       default=default,
                       vars=installEnvVars)

pyworkflow.em.Domain.registerPlugin(__name__)
