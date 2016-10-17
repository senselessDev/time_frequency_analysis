import tfa
import matplotlib.pyplot
import numpy
import scipy.signal

fig, ((sub1, sub2), (sub3, sub4)) = matplotlib.pyplot.subplots(2,2)

size = 1025
x = numpy.arange(size)
y = numpy.sin(2 * numpy.pi * (0.02 + 0.04 / size * x) * x)
y = scipy.signal.hilbert(y)
result = tfa.wvd(y)


sub2.plot(numpy.square(numpy.abs(y)) * size)
sub2.plot(numpy.sum(result, axis = 0))
#sub3.plot(1/2.0 * numpy.fft.fft(y) * numpy.conjugate(numpy.fft.fft(y)), label='fft')
sub3.plot(numpy.square(numpy.abs(numpy.fft.fft(y))), label='fft')
sub3.plot(numpy.sum(result, axis = 1), label = 'sum')
sub4.imshow(result)
sub3.legend()
fig.show()
