"""Tests for quick-check short-circuit behavior."""

import unittest
from contextlib import ExitStack
from unittest.mock import patch

from pyunormalize import normalization


class TestQuickCheckShortCircuit(unittest.TestCase):

    def assert_short_circuits(
        self,
        form_name,
        qc_loader_name,
        forbidden_names,
    ):
        source = "déjà normalisé"

        ccc_table = object()
        qc_set = object()

        with ExitStack() as stack:
            ccc_loader = stack.enter_context(
                patch.object(normalization, "_ccc", return_value=ccc_table)
            )
            qc_loader = stack.enter_context(
                patch.object(
                    normalization,
                    qc_loader_name,
                    return_value=qc_set,
                )
            )
            quick_check = stack.enter_context(
                patch.object(normalization, "_quick_check", return_value=True)
            )

            forbidden = {
                name: stack.enter_context(patch.object(normalization, name))
                for name in forbidden_names
            }

            result = getattr(normalization, form_name)(source)

        self.assertIs(result, source)
        ccc_loader.assert_called_once_with()
        qc_loader.assert_called_once_with()
        quick_check.assert_called_once_with(source, qc_set, ccc_table)

        for mock in forbidden.values():
            mock.assert_not_called()

    def test_quick_check_true_short_circuits_all_forms(self):
        cases = [
            (
                "NFD",
                "_nfd_qc_no",
                (
                    "_cdecomp_table",
                    "_decompose",
                    "_reorder",
                ),
            ),
            (
                "NFKD",
                "_nfkd_qc_no",
                (
                    "_kdecomp_table",
                    "_decompose",
                    "_reorder",
                ),
            ),
            (
                "NFC",
                "_nfc_qc_no_or_maybe",
                (
                    "NFD",
                    "_composition_table",
                    "_compose",
                ),
            ),
            (
                "NFKC",
                "_nfkc_qc_no_or_maybe",
                (
                    "NFKD",
                    "_composition_table",
                    "_compose",
                ),
            ),
        ]

        for form_name, qc_loader_name, forbidden_names in cases:
            with self.subTest(form=form_name):
                self.assert_short_circuits(
                    form_name,
                    qc_loader_name,
                    forbidden_names,
                )


if __name__ == "__main__":
    unittest.main()
