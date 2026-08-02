# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# base class for configuration syntax sugar

import abc


class KV(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, key: list[str]) -> str:
        pass

    @abc.abstractmethod
    def __contains__(self, key: list[str]) -> bool:
        """Populate the configuration from a dictionary"""
