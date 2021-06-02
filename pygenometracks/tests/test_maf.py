# -*- coding: utf-8 -*-
import matplotlib as mpl
mpl.use('agg')
from matplotlib.testing.compare import compare_images
from tempfile import NamedTemporaryFile
import os.path
import pygenometracks.plotTracks


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "test_data")

browser_tracks = """
[maf]
file = first.maf
reference = mm10.chr2
title = default
height = 3

[spacer]

[maf]
file = first.maf
reference = mm10.chr2
title = choose order
species_order = hg19 rn5   sorAra1
species_labels = Human Rat  Shrew
height = 3

[spacer]

[maf]
file = first.maf
reference = mm10.chr2
title = specify only zebrafish
species_order = danRer11
species_labels = Zebrafish
height = 3

[x-axis]
"""
with open(os.path.join(ROOT, "first_maf.ini"), 'w') as fh:
    fh.write(browser_tracks)

tolerance = 13  # default matplotlib pixed difference tolerance


def test_first_maf():
    extension = '.png'

    outfile = NamedTemporaryFile(suffix=extension, prefix='pyGenomeTracks_test_',
                                 delete=False)
    ini_file = os.path.join(ROOT, "first_maf.ini")
    bed_file = os.path.join(ROOT, 'regions_maf.bed')
    args = f"--tracks {ini_file} --BED {bed_file} "\
           "--trackLabelFraction 0.2 --width 38 --dpi 130 "\
           f"--outFileName {outfile.name}".split()
    pygenometracks.plotTracks.main(args)
    for region in ['chr2:34704975-34705208', 'chr2:34705032-34707346']:
        region_str = region.replace(':', '-')
        output_file = outfile.name[:-4] + '_' + region_str + extension
        expected_file = os.path.join(ROOT, 'master_first_maf_'
                                     + region_str + extension)
        res = compare_images(expected_file,
                             output_file, tolerance)
        assert res is None, res

        os.remove(output_file)
