##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
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

""" Test module for the AbstractPhotonAnalyzer module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import os, shutil
import unittest


# Import the class to test.
from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator

from TestUtilities import TestUtilities

class TestPhotonAnalyzer(AbstractPhotonAnalyzer):

    def __init__(self):
        input_path = TestUtilities.generateTestFilePath('FELsource_out.h5')
        super(TestPhotonAnalyzer, self).__init__()

    def backengine(self):
        pass

    def saveH5(self): pass
    def _readH5(self): pass
    def expectedData(self): pass
    def providedData(self): pass


class AbstractPhotonAnalyzerTest(unittest.TestCase):
    """
    Test class for the AbstractPhotonAnalyzer.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__dirs_to_remove = []
    def tearDown(self):
        """ Tearing down a test. """
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree( d )

    def testConstruction(self):
        """ Testing the default construction of the class. """

        self.assertRaises(TypeError, AbstractPhotonAnalyzer )

    def notestThis(self):
        aps = AbstractPhotonAnalyzer()

        self.assertIsInstance(aps, AbstractPhotonAnalyzer)

    def testConstructionDerived(self):
        """ Test that we can construct a derived class and it has the correct inheritance. """

        # Ensure proper cleanup:
        self.__dirs_to_remove.append('analysis')


        test_source = TestPhotonAnalyzer()

        self.assertIsInstance( test_source, TestPhotonAnalyzer )
        self.assertIsInstance( test_source, object )
        self.assertIsInstance( test_source, AbstractBaseCalculator )
        self.assertIsInstance( test_source, AbstractPhotonAnalyzer )


    def testDefaultPaths(self):
        """ Check that default pathnames are chosen correctly. """

        # Ensure proper cleanup:
        self.__dirs_to_remove.append('analysis')

        # Construct with no paths given.
        instance = TestPhotonAnalyzer()

        self.assertEqual(instance.output_path, os.path.abspath('analysis'))
        self.assertEqual(instance.input_path, os.path.abspath('detector'))

if __name__ == '__main__':
    unittest.main()

