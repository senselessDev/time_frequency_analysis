import numpy
import matplotlib.pyplot

M = 257

octave_window = numpy.genfromtxt('octave_hamming.csv')
python_window = numpy.hamming(M)

n = numpy.arange(M)
wiki_window = 0.54 - 0.46 * numpy.cos(2 * numpy.pi * n / (M - 1))

matplotlib.pyplot.plot(octave_window, label = 'tftb hamming')
matplotlib.pyplot.plot(python_window, label = 'numpy hamming')
matplotlib.pyplot.plot(wiki_window, label = 'wikipedia hamming')
matplotlib.pyplot.legend()
matplotlib.pyplot.show()

tftb_numpy_difference = numpy.sqrt(numpy.sum(numpy.square(octave_window - python_window)))
tftb_wiki_difference = numpy.sqrt(numpy.sum(numpy.square(octave_window - wiki_window)))
numpy_wiki_difference = numpy.sqrt(numpy.sum(numpy.square(python_window - wiki_window)))

print('Integrated difference between:\n'
      'TFTB and numpy Hamming window: {}\n'
      'TFTB and Wikipedia Hamming window: {}\n'
      'numpy and Wikipedia Hamming window: {}'
      ''.format(tftb_numpy_difference,
                tftb_wiki_difference,
                numpy_wiki_difference))
