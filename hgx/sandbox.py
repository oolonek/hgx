from matchms import Spectrum
from matchms.importing import load_from_mgf
import json
from hgx.helpers import load_and_filter_from_mgf
import numpy as np
import hypernetx as hnx


name_of_sample = "erythroxylum_coca"
file_mgf = f"data/{name_of_sample}.mgf"

# alternatively, we iterate over *.mgf files in a directory
# we extract the species name from the file name
# and store the spectra for each species in a common dictionary

mgf_path = "data/"

collection_of_spectra = {}
for file in os.listdir(mgf_path):
    if file.endswith(".mgf"):
        species = file.split(".")[0]
        collection_of_spectra[species] = list(load_and_filter_from_mgf(path = mgf_path + file, intensity_from=5E5, intensity_to = np.inf, no_peaks = 2, intensity_percent = 20))



spectra = list(load_from_mgf(file_mgf))

spectra = load_and_filter_from_mgf(path = file_mgf, intensity_from=1E6, intensity_to = np.inf, no_peaks = 2, intensity_percent = 5)

round(spectra['erythroxylum_coca'][0].get("precursor_mz"), 1)

# Returns a numpy array

# array([ 51.0233,  57.0576,  58.0654,  58.8909,  62.5096,  65.0386,
#         68.0496,  70.0651,  74.1799,  77.0383,  79.0539,  81.0694,
#         82.0648,  83.0682,  83.0725,  91.0537,  91.7644,  93.0329,
#         93.0693,  94.0643,  94.4401,  95.0485,  96.0802,  97.0641,
#        105.0326, 105.0692, 107.0486, 108.0798, 108.0872, 114.0902,
#        118.0403, 119.0479, 122.0951, 125.0586, 132.0796, 133.0636,
#        135.0661, 150.0899, 151.0743, 154.0847, 182.1158, 183.1192,
#        194.0627, 272.1258, 304.1514, 305.1551])

# Round each peak to 2 decimal places

spectra[0].peaks.mz.round(2)

# Apply to all spectra
# Store in a similar structure. The digits correspond to the spectra feature_id and the list of letter pairs are the rounded mz values
# {
#   "0": ["FN", "TH"],
#   "1": ["TH", "JV"],
#   "2": ["BM", "FN", "JA"],
#   "3": ["JV", "JU", "CH", "BM"],
#   "4": ["JU", "CH", "BR", "CN", "CC", "JV", "BM"],
#   "5": ["TH", "GP"],
#   "6": ["GP", "MP"],
#   "7": ["MA", "GP"]
# }


spectra[0].peaks.mz


# # Create an empty dict

# hg_dict = {}


# for spectrum in spectra:
#     # mz are rounded and removed if duplicate
#     # hg_dict[spectrum.get("feature_id")] = spectrum.peaks.mz.round(-1).tolist()
#     hg_dict[spectrum.get("feature_id")] = list(set(spectrum.peaks.mz.round(2).tolist()))

# hg_dict

# The same operation as previously are repeated but we now need to respect the follwoing structures
# Meaning that at the end of the spectral_id need to be individualized e.g erythroxylum_coca_0, erythroxylum_coca_1, etc and that at the end of the dict we grouup all peaks of the spectra by species

# {
#   "0": ["FN", "TH"],
#   "1": ["TH", "JV"],
#   "2": ["BM", "FN", "JA"],
#   "3": ["JV", "JU", "CH", "BM"],
#   "4": ["JU", "CH", "BR", "CN", "CC", "JV", "BM"],
#   "5": ["TH", "GP"],
#   "6": ["GP", "MP"],
#   "7": ["MA", "GP"],
#   "8": ["TH", "BM"], 
#   "9": ["JU", "FN"],
#   "10": ["CC", "GP"],
#   "11": ["MA", "BM"],
#   "species_1": ["FN", "TH", "JV", "BM", "JA", "JU", "CH", "BR", "CN", "CC", "GP"],
#   "species_2": ["GP", "MP", "MA", "TH", "BM", "JU", "FN", "CC"]
# }

hg_dict = {}



# for species in collection_of_spectra:
#     for spectrum in collection_of_spectra[species]:
#         hg_dict[f"{species}_{spectrum.get('feature_id')}"] = list(set(spectrum.peaks.mz.round(1).tolist()))

#     hg_dict[species] = list(set([mz for spectrum in collection_of_spectra[species] for mz in spectrum.peaks.mz.round(1).tolist()]))

# We can access the precursor mass by spectra['erythroxylum_coca'][0].get("precursor_mz")
# So we enhance the function by also keeping the precursor mass for each spectra in the dict
# for the species, we only keep the precursor mass of each spectra.


for species in collection_of_spectra:
    for spectrum in collection_of_spectra[species]:
        mz_values = []
        mz_values.extend(spectrum.peaks.mz.round(1).tolist())
        mz_values.append(round(spectrum.get("precursor_mz"), 1))
        hg_dict[f"f_{species}_{spectrum.get('feature_id')}"] = list(set(mz_values))

    # hg_dict[f"taxon_{species}"] = list(set([round(spectrum.get("precursor_mz"), 1) for spectrum in collection_of_spectra[species]]))



# Save as a json file

# with open(f'data/{name_of_sample}.json', 'w') as f:
#     json.dump(hg_dict, f)

with open('data/full_json.json', 'w') as f:
    json.dump(hg_dict, f)

# We generate a bipartite graph where the taxon_ and the f_ are the nodes on one side and the mz values are the nodes on the other side
# The edges are the mz values that are shared between the taxon_ and the f_ nodes

# We can use the hypernetx library to generate the bipartite graph

# We first need to generate the edges

edges = []
for taxon in hg_dict:
    for mz in hg_dict[taxon]:
        edges.append((taxon, mz))



# We can now generate the bipartite graph

B = hnx.Hypergraph(edges)

# We can now generate the bipartite graph

# We save the edges as a csv file

with open('data/edges.csv', 'w') as f:
    header = ["source", "target"]
    f.write(f"{header[0]},{header[1]}\n")
    for edge in edges:
        f.write(f"{edge[0]},{edge[1]}\n")