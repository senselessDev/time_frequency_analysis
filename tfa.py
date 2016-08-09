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

    if data_len % 2 == 0:
        print('Even input data length not supported yet.')
        return

    N = int((data_len + 1) / 2)
    data = numpy.concatenate((numpy.zeros(N-1), data, numpy.zeros(N-1)))

    x = numpy.arange(data_len)
    idxs = scipy.linalg.hankel(x, x + data_len - 1)
    rev_idxs = idxs[::-1,:]

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
    wv = wv * win.T
    rolled = numpy.roll(wv, N, axis=0)
    result = numpy.fft.fft(rolled, axis=0)

    result = numpy.real(result)

    return result
