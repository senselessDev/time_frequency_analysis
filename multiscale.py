import tfa
import numpy
import matplotlib.pyplot
import scipy.ndimage

def pt2(x, K, d, T):
    sq = numpy.sqrt(1 - numpy.square(d))
    return K - (K / sq * numpy.exp(-d/T*x) * numpy.sin(sq / T * x + numpy.arctan(sq / d)))

x = numpy.arange(1024)
freq = pt2(x, 0.25, 0.4, 30)
y = numpy.sin(numpy.pi * freq * x)


#matplotlib.pyplot.plot(y)
#matplotlib.pyplot.show()

res = tfa.wvd(y)

steps = 4
fig, subs = matplotlib.pyplot.subplots(2,2)
subs = numpy.reshape(subs, -1)
scales = []
for step in numpy.arange(steps):
    subs[step].imshow(res, interpolation = 'none')
    subs[step].plot(numpy.argmax(res[:len(res)/2], axis = 0))
    if step < steps - 1:
        scales.append(res)
        res = scipy.signal.convolve2d(res, numpy.array([[1/4, 1/4],[1/4, 1/4]]))
        res = res[::2, ::2]


print(scales)
#subs[0].plot(numpy.linspace(0,1000, 128), 8 * numpy.argmax(res[:len(res)/2], axis = 0), 'r')
fig.show()
#res = scipy.ndimage.filters.gaussian_filter(res, 5)

#matplotlib.pyplot.imshow(res)
#matplotlib.pyplot.plot(numpy.argmax(res[:1000/2], axis = 0))
#matplotlib.pyplot.show()
fig, sub = matplotlib.pyplot.subplots(1,1)
f,t,sxx = scipy.signal.spectrogram(y, nperseg = 256, noverlap = 128)
matplotlib.pyplot.pcolormesh(t, f, sxx)
matplotlib.pyplot.show()
