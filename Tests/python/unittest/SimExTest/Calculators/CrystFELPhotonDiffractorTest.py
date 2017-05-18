##########################################################################
#                                                                        #
# Copyright (C) 2015,2016 Carsten Fortmann-Grote                         #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

""" Test module for the CrystFELPhotonDiffractor.

    @author : CFG
    @institution : XFEL
    @creation 20151109

"""
import os
import h5py
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest


# Import the class to test.
from SimEx.Calculators.CrystFELPhotonDiffractor import CrystFELPhotonDiffractor, CrystFELPhotonDiffractorParameters
from SimEx.Calculators.CrystFELPhotonDiffractor import _rename_files
from SimEx.Calculators.AbstractPhotonDiffractor import AbstractPhotonDiffractor
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from TestUtilities import TestUtilities

class CrystFELPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the CrystFELPhotonDiffractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testShapedConstruction(self):
        """ Testing the construction of the class with parameters. """

        # Setup parameters.
        parameters=CrystFELPhotonDiffractorParameters(sample="5udc.pdb")

        # Construct the object.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None)

        # Check type.
        self.assertIsInstance(diffractor, CrystFELPhotonDiffractor)
        self.assertIsInstance(diffractor, AbstractPhotonDiffractor)

    def testBackengineSinglePattern(self):
        """ Check we can run pattern_sim with a minimal set of parameter. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")

        # Get parameters.
        parameters = CrystFELPhotonDiffractorParameters(sample="5udc.pdb",
                geometry=TestUtilities.generateTestFilePath("simple.geom"),
                number_of_diffraction_patterns=1)

        # Get calculator.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out_0000001.h5" , os.listdir( diffractor.output_path ))



    def testBackengineMultiplePatterns(self):
        """ Check we can run pattern_sim with a minimal set of parameter. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")

        # Get parameters.
        parameters = CrystFELPhotonDiffractorParameters(sample="5udc.pdb",
                geometry=TestUtilities.generateTestFilePath("simple.geom"),
                number_of_diffraction_patterns=2)

        # Get calculator.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out-1.h5" , os.listdir( diffractor.output_path ))
        self.assertIn( "diffr_out-2.h5" , os.listdir( diffractor.output_path ))

    def testSaveH5(self):
        """ Check that saveh5() creates correct filenames. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")

        # Get parameters.
        parameters = CrystFELPhotonDiffractorParameters(sample="5udc.pdb",
                geometry=TestUtilities.generateTestFilePath("simple.geom"),
                number_of_diffraction_patterns=2)

        # Get calculator.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Save correctly.
        diffractor.saveH5()

        # Check return code.
        self.assertEqual(status, 0)

        # Check output dir was created.
        self.assertTrue( os.path.isdir( diffractor.output_path ) )

        # Check pattern was written.
        self.assertIn( "diffr_out_0000001.h5" , os.listdir( diffractor.output_path ))
        self.assertIn( "diffr_out_0000002.h5" , os.listdir( diffractor.output_path ))

        # FIXME: Link all output into one hdf5.
        self.assertIn( diffractor.output_path+".h5", os.listdir( os.path.dirname( diffractor.output_path) ) )

    def notestRenameFiles(self):

        _rename_files( "diffr" )

    def testBackengineWithBeamParametersObject(self):
        """ Check beam parameter logic if they are set as parameters. """

        # Ensure cleanup.
        self.__dirs_to_remove.append("diffr")
        self.__files_to_remove.append("5udc.pdb")

        # Setup beam parameters.
        beam_parameters = PhotonBeamParameters(
                photon_energy=16.0e3,
                photon_energy_relative_bandwidth=0.001,
                pulse_energy=2.0e-3,
                beam_diameter_fwhm=100e-9,
                divergence=None,
                )

        # Get parameters.
        parameters = CrystFELPhotonDiffractorParameters(sample="5udc.pdb",
                geometry=TestUtilities.generateTestFilePath("simple.geom"),
                beam_parameters=beam_parameters,
                number_of_diffraction_patterns=2,
                )

        # Get calculator.
        diffractor = CrystFELPhotonDiffractor(parameters=parameters, input_path=None, output_path='diffr')

        # Run backengine
        status = diffractor.backengine()

        # Check return code.
        self.assertEqual(status, 0)


if __name__ == '__main__':
    unittest.main()

