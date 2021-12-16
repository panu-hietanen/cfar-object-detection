import numpy as np
from rs_utils.sar_functions import db2in
from .fast_functions import fast_edge_mean, fast_center_mean


def transform(image, mask=0):

    # if no mask is given, assume all pixels are valid
    if np.all(mask == 0):
        mask = np.ones_like(image[0, ...]) > 0

    eps = db2in(-100)

    #  HV_test = fast_center_mean(image[1, ...], mask)
    HV_test = image[1, ...]  # just testing what happens now
    HV_train = fast_edge_mean(image[1, ...], mask)
    HH_train = fast_edge_mean(image[0, ...], mask)

    Δ = (HV_test - HV_train) / (HH_train + eps) > HV_test

    detection_image = (Δ * image[1, ...]**2 + eps)

    return detection_image
