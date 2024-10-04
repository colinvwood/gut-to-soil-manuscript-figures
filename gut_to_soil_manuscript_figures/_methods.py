# ----------------------------------------------------------------------------
# Copyright (c) 2024, Liz Gehret.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources
import skbio
import subprocess

import qiime2


def pcoa_2d(output_dir: str, metadata: qiime2.Metadata,
            ordination: skbio.OrdinationResults,
            measure: str = 'Unweighted Unifrac',
            average: bool = False, week_annotations: bool = True,
            invert_x: bool = True, invert_y: bool = True,
            swap_axes: bool = False, himalaya: bool = False,
            pit_toilet: bool = False, highlighted_buckets: str = ''):

    md = metadata.to_dataframe()

    metadata_fp = os.path.join(output_dir, 'metadata.tsv')
    ordination_fp = os.path.join(output_dir, 'ordination.txt')

    md.to_csv(metadata_fp, sep='\t', index_label='sample-id')
    ordination.write(ordination_fp)

    script_path = \
        pkg_resources.resource_filename(
            'gut_to_soil_manuscript_figures',
            'scripts/plot_pcoa_2d.py'
        )

    # Convert boolean parameters to strings
    average = str(average)
    week_annotations = str(week_annotations)
    invert_x = str(invert_x)
    invert_y = str(invert_y)
    swap_axes = str(swap_axes)
    himalaya = str(himalaya)
    pit_toilet = str(pit_toilet)

    plot_fp = os.path.join(output_dir, 'pcoa_plot.png')

    command = [
        'python', script_path,
        metadata_fp,
        ordination_fp,
        measure,
        average,
        week_annotations,
        plot_fp,
        invert_x,
        invert_y,
        swap_axes,
        himalaya,
        pit_toilet,
        highlighted_buckets
    ]
    subprocess.run(command, check=True)

    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>2D {measure} PCoA Plot</title>
        </head>
        <body>
            <h1>2D {measure} PCoA Plot</h1>
            <img src="pcoa_plot.png" alt="PCoA Plot">
        </body>
        </html>
        ''')
