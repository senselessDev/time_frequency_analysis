#!/usr/bin/env python

import numpy
import scipy.linalg

def wvd(data, window = numpy.ones, window_length = None):
    """
    Discrete Pseudo Wigner Ville Distribution

    .. math:: #TODO
    W(n, m \frac{\pi}{M}) = 2 \sum_{k=-N+1}^{N-1} e^{-jkm \frac{2\pi}{M}} f\left(n+k\right) f^{*}\left(n-k\right)

    based on http://publik.tuwien.ac.at/files/PubDat_249646.pdf

    another interesting discussion: http://www.ciaranhope.com/paper1.html
    """

    if not isinstance(data, numpy.ndarray):
        try:
            data = numpy.array(data)
        except:
            print('Input data must be numpy array!')
            return

    data = data.squeeze()

    if data.ndim > 1:
        print('Input data must be one dimensional!')
        return

    data_len = data.shape[0]

    N = round((data_len - 1) / 2)
    data = numpy.concatenate((numpy.zeros(N), data, numpy.zeros(N)))

    x = numpy.arange(data_len)
    # special case for an even number of input data samples
    x_ = numpy.arange(data_len + 1 - (data_len % 2))
    idxs = scipy.linalg.hankel(x, x_ + data_len - 1)
    rev_idxs = idxs[::,::-1]

    if window_length is None:
        window_length = data_len

    win = window(window_length)
    win_len_diff = data_len - window_length
    if win_len_diff < 0:
        print('Window length must be shorter or equal data length!')
        return
    elif win_len_diff > 0:
        zero_len = int(win_len_diff / 2)
        win = numpy.concatenate((numpy.zeros(zero_len), win, numpy.zeros(zero_len)))


    win = win * numpy.conjugate(win[::-1])
    win = numpy.tile(win, (data_len,1))

    wv = data[idxs] * numpy.conj(data[rev_idxs])
    ########
    #filt = numpy.hamming(103)
    #filt = filt / numpy.sum(filt)
    #wv = numpy.apply_along_axis(lambda m: numpy.convolve(m, filt, mode='same'), axis = 1, arr = wv)
    ####
    # reshape to square matrix for even number of input data samples
    wv = wv[:data_len, :data_len] * win
    # roll depending on even/odd number of input data samples
    rolled = numpy.roll(wv, N + (data_len % 2), axis=1)
    result = numpy.fft.fft(rolled, axis=1)

    result = numpy.real(result).T

    return result
