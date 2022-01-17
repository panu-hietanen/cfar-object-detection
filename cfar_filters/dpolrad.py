import numpy as np
from rs_utils.sar_functions import db2in
from .fast_functions import fast_edge_mean, fast_center_mean

def _mask_edges(image, N):
    image[0:N, :] = np.nan
    image[:, 0:N] = np.nan
    image[-N:, :] = np.nan
    image[:, -N:] = np.nan
    return image

def transform(image, mask=0):

    # if no mask is given, assume all pixels are valid
    if np.all(mask == 0):
        mask = np.ones_like(image[0, ...]) > 0

    eps = db2in(-100)  # small number

    HV_target = fast_center_mean(image[1, ...], mask)
    HV_clutter = fast_edge_mean(image[1, ...], mask)
    HH_clutter = fast_edge_mean(image[0, ...], mask)
    # TODO, maybe remove the eps thing and add a check for HH_clutter == 0?
    Δ = (HV_target - HV_clutter) / (HH_clutter + eps)

    Δ = _mask_edges(Δ, 6)

    return Δ
