================================
Scipion plugin integrating aitom
================================

AITom is an open-source platform for AI driven cellular electron cryo-tomography analysis.

The tomominer module was adapted from an extended version of the tomominer library, developed at Alber Lab.


=====
Setup
=====
- **Requirements**

Scipion has to be installed

scipion-em-xmipp too

scipion-em-tomo (in developement):
  - git clone https://github.com/scipion-em/scipion-em-tomo
  - scipion installp -p local/path/to/scipion-em-tomo --devel

- **Install this plugin in devel mode:**



Using the command line:

.. code-block::

    scipion installp -p local/path/to/scipion-em-aitom --devel
    
Testing it:

.. code-block::

   scipion test aitom.tests.tests_picking.TestAitomPicking
