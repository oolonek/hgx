
from matchms.importing import load_from_mgf
from matchms.filtering import normalize_intensities
from matchms.filtering import require_minimum_number_of_peaks
from matchms.filtering import require_maximum_number_of_peaks
from matchms.filtering import select_by_relative_intensity
from matchms.filtering import select_by_intensity
from matchms.filtering import reduce_to_number_of_peaks
from matchms.filtering import require_minimum_number_of_high_peaks
import numpy as np

def load_and_filter_from_mgf(path, intensity_from, intensity_to, no_peaks, intensity_percent) -> list:
    """Load and filter spectra from mgf file

    Returns:
        spectrums (list of matchms.spectrum): a list of matchms.spectrum objects
    """
    def apply_filters(spectrum):
        # spectrum = normalize_intensities(spectrum)
        spectrum = select_by_intensity(spectrum, intensity_from = intensity_from, intensity_to = intensity_to)
        # spectrum = require_minimum_number_of_peaks(spectrum, n_required= n_required)
        # spectrum = require_maximum_number_of_peaks(spectrum, n_required= 10)
        spectrum = require_minimum_number_of_high_peaks(spectrum, no_peaks = no_peaks, intensity_percent = intensity_percent)
        # spectrum = reduce_to_number_of_peaks(spectrum, n_required=  n_required, n_max = n_required)
        return spectrum

    spectra_list = [apply_filters(s) for s in load_from_mgf(path)]
    spectra_list = [s for s in spectra_list if s is not None]
    return spectra_list 