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
                   'Time-Frequency-Toolbox for the {} test failed. '
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

        max_diff = numpy.max(numpy.abs(self.python_data - self.octave_data))

        print(('\n[{}] Difference between Wigner-Ville-Distribution of Octaves '
               'Time-Frequency-Toolbox and this implementation is used as test '
               'criterium.'.format(self.test_string.upper())))
        print(('[{}] Maxmimum absolute deviation between both implementations: '
               '{:.2e} %').format(self.test_string.upper(),
                                 max_diff / amplt_range * 100))

        # make sure that maximum absolute deviation is below 1 ppm
        self.assertGreater(1e-6,
                           max_diff / amplt_range,
                           msg = 'Maximum absolute deviation greater than 1 ppm')

class WVDTest(OctaveComparisonTest):
    """
    Simple test that compares results of the Discrete Wigner Ville Distribution
    from the octave TFTB with this implementation.
    The test signal is a simple linear frequency chirp.
    """
    test_string = "wvd"

    def testWVD(self):
        size = 1025
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

    def _tftb_hamming(self, M):
        """Hamming Window in TFTB is wrong.
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
