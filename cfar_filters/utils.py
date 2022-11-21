import numpy as np
import pandas as pd

def db2in(image):
    """
    Convert decibel to intensity

    Parameters:
    ----------
    image : numpy.ndarray (N,X,Y)
        SAR image in decibel

    Returns:
    ----------
    image : numpy.ndarray (N,X,Y)
        SAR image in intensity
    """
    return np.power(10, np.divide(image, 10))


def in2db(image):
    """
    Convert intensity to decibel

    Parameters:
    ----------
    image : numpy.ndarray (N,X,Y)
        SAR image in intensity

    Returns:
    ----------
    image : numpy.ndarray (N,X,Y)
        SAR image in decibel

    """
    return 10 * np.log10(np.absolute(image))

"""
simple mom method for estimating the ENL
theoretically only works for gamma, but are commonly used for other distributions as well
"""
def calc_enl(samples):
    return np.nanmean(samples)**2 / np.nanstd(samples)**2


def smells_like(image, K=1000):
    """
    Often, SAR images are visualized in decibel scale.
    However, processing is often executed in linear intensity scale.
    This leads to errors, if eg. a decibel image is given as an input to a function expecting linear intensity.
    This function executes a "soft test" in order to try to guess what format the input is.
    The function is used to warn about likely wrong formats.

    Parameters:
    ----------
    image : numpy.ndarray (N,X,Y)
        SAR image
    K : integer
        Number of samples used to create the statistics

    Returns:
    ----------
    smells_like : string
        'decibel'/'intensity'/'fishy'
    """
    samples = pd.DataFrame(image[:, np.random.choice(image.shape[1], K), np.random.choice(image.shape[2], K)].T)

    describe = samples.describe()

    # if mean < 0 and std > 1 and min < -20 => smells like db
    if np.all([describe.loc['mean'] < 0, describe.loc['std'] > 1, describe.loc['min'] < -20]):
        smells_like = 'decibel'
    # if 0 < mean < 1 and 0 < std < 1 and min > 0 => smells like intensity
    elif np.all([0 < describe.loc['mean'], describe.loc['mean'] < 1, 0 < describe.loc['std'],
                describe.loc['std'] < 1, describe.loc['min'] > 0]):
        smells_like = 'intensity'
    else:
        smells_like = 'fishy'

    return smells_like

def mask_edges(image, N, fill=False):
    """
    Masks the edges of an image

    Parameters:
    ----------
    image : numpy.ndarray (X,Y)
        Image to be masked
    fill : fill value
        e.g. False or np.nan

    Returns:
    ----------
    image : numpy.ndarray (X,Y)
        masked image

    """
    image[0:N, :] = fill
    image[:, 0:N] = fill
    image[-N:, :] = fill
    image[:, -N:] = fill

    return image
