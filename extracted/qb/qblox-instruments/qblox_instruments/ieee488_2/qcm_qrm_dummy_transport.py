# ----------------------------------------------------------------------------
# Description    : Transport layer (abstract, IP, file, dummy)
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import warnings

from qblox_instruments.ieee488_2.module_dummy_transport import ModuleDummyTransport

# -- class -------------------------------------------------------------------


class QcmQrmDummyTransport(ModuleDummyTransport):
    def __init__(self, *args, **kwargs) -> None:
        warnings.warn(
            """
            After April 2025, QcmQrmDummyTransport is deprecated and will be removed in the future.
            "Please use qblox_instruments.ieee488_2.module_dummy_transport.ModuleDummyTransport instead.",
            See https://qblox-qblox-instruments.readthedocs-hosted.com/en/main/getting_started/deprecated.html
            """,  # noqa: E501
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
