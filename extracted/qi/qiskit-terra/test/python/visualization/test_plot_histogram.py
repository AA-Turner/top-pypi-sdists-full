# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for plot_histogram."""

import unittest
from io import BytesIO
from collections import Counter

from qiskit.visualization import plot_histogram
from qiskit.result import QuasiDistribution, ProbDistribution
from qiskit.utils import optionals
from .visualization import QiskitVisualizationTestCase

if optionals.HAS_MATPLOTLIB:
    import matplotlib as mpl
if optionals.HAS_PIL:
    from PIL import Image


@unittest.skipUnless(optionals.HAS_MATPLOTLIB, "matplotlib not available.")
class TestPlotHistogram(QiskitVisualizationTestCase):
    """Qiskit plot_histogram tests."""

    def test_different_counts_lengths(self):
        """Test plotting two different length dists works"""
        exact_dist = {
            "000000": 1,
            "000001": 1,
            "000011": 2,
            "000111": 4,
            "100000": 1,
            "100001": 1,
            "100011": 2,
            "100111": 4,
            "110000": 2,
            "110001": 2,
            "110011": 4,
            "110111": 10,
            "111111": 32,
        }

        raw_dist = {
            "000000": 26,
            "000001": 29,
            "010000": 10,
            "010001": 12,
            "010010": 6,
            "010011": 14,
            "010100": 2,
            "010101": 6,
            "010110": 4,
            "010111": 24,
            "011000": 2,
            "011001": 5,
            "011011": 5,
            "011101": 4,
            "011110": 7,
            "011111": 77,
            "000010": 9,
            "100000": 31,
            "100001": 25,
            "100010": 8,
            "100011": 46,
            "100100": 3,
            "100101": 3,
            "100110": 9,
            "100111": 114,
            "101000": 3,
            "101001": 6,
            "101010": 1,
            "101011": 6,
            "101100": 7,
            "101101": 9,
            "101110": 6,
            "101111": 48,
            "000011": 82,
            "110000": 42,
            "110001": 53,
            "110010": 9,
            "110011": 102,
            "110100": 10,
            "110101": 8,
            "110110": 14,
            "110111": 215,
            "111000": 25,
            "111001": 12,
            "111010": 2,
            "111011": 41,
            "111100": 18,
            "111101": 24,
            "111110": 58,
            "111111": 621,
            "000100": 1,
            "000101": 7,
            "000110": 9,
            "000111": 73,
            "001000": 1,
            "001001": 5,
            "001011": 6,
            "001100": 1,
            "001101": 7,
            "001110": 1,
            "001111": 34,
        }

        fig = plot_histogram([raw_dist, exact_dist])
        self.assertIsInstance(fig, mpl.figure.Figure)

    def test_with_number_to_keep(self):
        """Test plotting using number_to_keep"""
        dist = {"00": 3, "01": 5, "11": 8, "10": 11}
        fig = plot_histogram(dist, number_to_keep=2)
        self.assertIsInstance(fig, mpl.figure.Figure)

    def test_with_number_to_keep_multiple_executions(self):
        """Test plotting using number_to_keep with multiple executions"""
        dist = [{"00": 3, "01": 5, "11": 8, "10": 11}, {"00": 3, "01": 7, "10": 11}]
        fig = plot_histogram(dist, number_to_keep=2)
        self.assertIsInstance(fig, mpl.figure.Figure)

    @unittest.skipUnless(optionals.HAS_PIL, "matplotlib not available.")
    def test_with_number_to_keep_multiple_executions_correct_image(self):
        """Test plotting using number_to_keep with multiple executions"""
        data_noisy = {
            "00000": 22,
            "00001": 3,
            "00010": 5,
            "00011": 0,
            "00100": 4,
            "00101": 1,
            "00110": 4,
            "00111": 1,
            "01000": 5,
            "01001": 0,
            "01010": 2,
            "01011": 0,
            "01100": 225,
            "01101": 1,
            "01110": 3,
            "01111": 3,
            "10000": 12,
            "10001": 2,
            "10010": 1,
            "10011": 1,
            "10100": 247,
            "10101": 4,
            "10110": 3,
            "10111": 1,
            "11000": 225,
            "11001": 5,
            "11010": 2,
            "11011": 0,
            "11100": 15,
            "11101": 4,
            "11110": 1,
            "11111": 0,
        }
        data_ideal = {
            "00000": 25,
            "00001": 0,
            "00010": 0,
            "00011": 0,
            "00100": 0,
            "00101": 0,
            "00110": 0,
            "00111": 0,
            "01000": 0,
            "01001": 0,
            "01010": 0,
            "01011": 0,
            "01100": 25,
            "01101": 0,
            "01110": 0,
            "01111": 0,
            "10000": 0,
            "10001": 0,
            "10010": 0,
            "10011": 0,
            "10100": 25,
            "10101": 0,
            "10110": 0,
            "10111": 0,
            "11000": 25,
            "11001": 0,
            "11010": 0,
            "11011": 0,
            "11100": 0,
            "11101": 0,
            "11110": 0,
            "11111": 0,
        }
        data_ref_noisy = dict(Counter(data_noisy).most_common(5))
        data_ref_noisy["rest"] = sum(data_noisy.values()) - sum(data_ref_noisy.values())
        data_ref_ideal = dict(Counter(data_ideal).most_common(4))  # do not add 0 values
        data_ref_ideal["rest"] = 0
        figure_ref = plot_histogram([data_ref_ideal, data_ref_noisy])
        figure_truncated = plot_histogram([data_ideal, data_noisy], number_to_keep=5)
        with BytesIO() as img_buffer_ref:
            figure_ref.savefig(img_buffer_ref, format="png")
            img_buffer_ref.seek(0)
            with BytesIO() as img_buffer:
                figure_truncated.savefig(img_buffer, format="png")
                img_buffer.seek(0)
                self.assertImagesAreEqual(Image.open(img_buffer_ref), Image.open(img_buffer), 0.2)
        mpl.pyplot.close(figure_ref)
        mpl.pyplot.close(figure_truncated)

    def test_number_of_items_in_legend_with_data_starting_with_zero(self):
        """Test legend if there's a 0 value at the first item of the dataset"""
        dist_1 = {"0": 369, "1": 140}
        dist_2 = {"0": 0, "1": 488}
        legend = ["lengend_1", "lengend_2"]
        plot = plot_histogram([dist_1, dist_2], legend=legend)
        self.assertEqual(
            len(plot._localaxes[0].legend_.texts),
            2,
            "Plot should have the same number of legend items as defined",
        )

    def test_deprecation(self):
        """Test that passing `QuasiDist`, `ProbDist` or a dict of floats is deprecated."""
        with self.assertWarns(DeprecationWarning):
            plot_histogram(QuasiDistribution({"00": 1.0}))
        with self.assertWarns(DeprecationWarning):
            plot_histogram(ProbDistribution({"00": 1.0}))
        with self.assertWarns(DeprecationWarning):
            plot_histogram({"00": 1.0})


if __name__ == "__main__":
    unittest.main(verbosity=2)
