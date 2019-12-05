from pyworkflow.object import Pointer
from pyworkflow.tests import BaseTest, setupTestProject, DataSet
from tomo.protocols import ProtImportTomograms

from aitom.protocols import AiTomPicking


class TestAitomPicking(BaseTest):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.ds = DataSet.getDataSet('aitom')

    def test_picking(self):
        print("Run aitom picking")

        protImportTomogram = self.newProtocol(ProtImportTomograms,
                                 filesPath=self.ds.getFile("single_particle"),
                                 samplingRate=5)

        self.launchProtocol(protImportTomogram)
        # Create the picking protocol and link it.
        protPicking = self.newProtocol(AiTomPicking)
        protPicking.inputTomograms = Pointer(protImportTomogram, extended="outputTomograms")

        # Launch the picking
        self.launchProtocol(protPicking)

        # Check it has something
        self.assertSetSize(protPicking.output3DCoordinates, 21509,
                             "There was a problem with coordinates 3d output")
