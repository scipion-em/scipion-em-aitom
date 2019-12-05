from pyworkflow.tests import DataSet

import tests_picking

# Define aitom dataset (hosted at scipion server)
DataSet(name='aitom', folder='aitom',
        files={
               'cellular': 'aitom_demo_cellular_tomogram.mrc',
               'single_particle': 'aitom_demo_single_particle_tomogram.mrc',
               'pickle': 'aitom_demo_subtomograms.pickle'
        })
