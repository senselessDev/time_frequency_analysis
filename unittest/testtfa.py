#!/usr/bin/env python

import unittest
import subprocess
import os

import tfa
from tfa import numpy as numpy


class OctaveComparisonTest(unittest.TestCase):
    """
    For testing the time frequency analysis routines, the results of this
    implementation are compared to the results of the time frequency
    toolbox (TFTB) for octave/MATLAB.
    """
    def setUp(self):
        self.octave_generate_file = 'test_{}.m'.format(self.test_string)

        completedProcess = subprocess.run(
            ["octave", self.octave_generate_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)

        if completedProcess.returncode is not 0:
            print(('Generation of comparison data from Octaves '
                   'Time-Frequency-Toolbox for the {} test failed.\n'
                   'Possibly the tftb-source folder does not exist. '
                   'Use the Makefile to get the source files. '
                   'Skipping...'.format(self.test_string)))
            raise unittest.SkipTest()

        #data_file = completedProcess.stdout.strip().decode('utf-8')
        #if not os.path.exists(data_file):
        #    print(('Octave script should return path to the generated data. '
        #           'But it seems that "{}" does not exist for the {} test. '
        #           'Skipping...').format(data_file, self.test_string))
        #    raise unittest.SkipTest()

        self.octave_data_file = 'octave_{}.csv'.format(self.test_string)

        self.octave_data = tfa.numpy.genfromtxt(self.octave_data_file)

    def tearDown(self):
        os.remove(self.octave_data_file)

    def _compare(self):

        min_max = min((numpy.max(self.python_data), numpy.max(self.octave_data)))
        max_min = max((numpy.min(self.python_data), numpy.min(self.octave_data)))
        amplt_range = min_max - max_min

        one_dimensional = numpy.reshape(self.python_data - self.octave_data, -1)

        inf_norm = numpy.linalg.norm(one_dimensional, numpy.inf)
        inf_norm_rel = inf_norm / amplt_range

        euclidean_norm = numpy.linalg.norm(one_dimensional, 2)
        euclidean_norm_rel = euclidean_norm / amplt_range

        print(('\n[{}] Difference between {} of Octaves Time-Frequency-Toolbox '
               'and this implementation is used as test criterium.'.format(
                   self.test_string.upper(), self.test_user_string)))
        print(('[{}] Infinity norm of difference matrix: {:.2e} ppm;'
               ' Euclidean norm of difference matrix: {:.2e} ppm').format(
                   self.test_string.upper(),
                   inf_norm_rel * 10**6,
                   euclidean_norm_rel * 10**6))

        # make sure that maximum absolute deviation is below 1 ppb
        self.assertGreater(
            1e-9,
            inf_norm_rel,
            msg = 'Infinity norm of difference matrix greater than 1 ppb')

        self.assertGreater(
            1e-6,
            euclidean_norm_rel,
            msg = 'Euclidean norm of difference matrix greater than 1 ppm')

# not supported yet
""" WVDEnergyTest(unittest.TestCase):
    def testEnergy(self):
        size = 1025
        x = numpy.arange(size)
        y = numpy.sin(2 * numpy.pi * (0.02 + 0.04 / size * x) * x)

        result = tfa.wvd(y)

        print('\n', numpy.sum(result), numpy.sum(numpy.abs(y) ** 2))
        doff = numpy.sum(result, axis = 1) - numpy.square(numpy.abs(y))
        print(doff)
"""

class WVDOddTest(OctaveComparisonTest):
    """
    Simple test that compares results of the Discrete Wigner Ville Distribution
    from the octave TFTB with this implementation.
    The test signal is a simple linear frequency chirp with an odd number of
    samples.
    """
    test_string = "wvd_odd"
    test_user_string = "Wigner-Ville-Distribution"

    def testWVD(self):
        size = 1025
        x = numpy.arange(size)
        y = numpy.sin(2 * numpy.pi * (0.02 + 0.04 / size * x) * x)

        self.python_data = tfa.wvd(y)

        self._compare()

class WVDEvenTest(OctaveComparisonTest):
    """
    Simple test that compares results of the Discrete Wigner Ville Distribution
    from the octave TFTB with this implementation.
    The test signal is a simple linear frequency chirp with an even number of
    samples.
    """
    test_string = "wvd_even"
    test_user_string = "Wigner-Ville-Distribution"

    def testWVD(self):
        size = 1024
        x = numpy.arange(size)
        y = numpy.sin(2 * numpy.pi * (0.02 + 0.04 / size * x) * x)

        self.python_data = tfa.wvd(y)

        self._compare()


class PWVDTest(OctaveComparisonTest):
    """
    Simple test that compares results of the Discrete Pseudo Wigner Ville
    Distribution (frequency smoothed version of WVD, using window functions)
    from the octave TFTB with this implementation.
    The test signal is a simple linear frequency chirp.
    Because the default window implementation of the TFTB is wrong, the wrong
    implementation has to be simulated here.
    """

    test_string = "pwvd"
    test_user_string = "Pseudo-Wigner-Ville-Distribution"

    def _tftb_hamming(self, M):
        """Hamming Window in TFTB is wrong. See folder 'hamming_window_comparison'.
        correct is: 0.54 - 0.46 * cos(2 * pi * n / (M - 1)) for n = 0...M-1
        TFTB uses:  0.54 - 0.46 * cos(2 * pi * n / (M + 1)) for n = 1...M
        """
        n = numpy.arange(M)
        window = 0.54 - 0.46 * numpy.cos(2 * numpy.pi * (n + 1) / (M + 1))
        return window

    def equivalent_default_window(self, M):
        return numpy.sqrt(self._tftb_hamming(M))

    def testPWVD(self):
        size = 1025
        x = numpy.arange(size)
        y = numpy.sin(2 * numpy.pi * (0.02 + 0.04 / size * x) * x)

        self.python_data = tfa.wvd(y,
                                   window = self.equivalent_default_window,
                                   window_length = 257)

        self._compare()

if __name__ == '__main__':
    unittest.main()
