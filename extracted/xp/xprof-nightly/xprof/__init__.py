# Copyright 2025 The XProf Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Entry point for the TensorBoard plugin package for XProf.

Public submodules:
  profile_plugin: The TensorBoard plugin integration.
  profile_plugin_loader: TensorBoard's entrypoint for the plugin.
  server: Standalone server entrypoint.
  version: The version of the plugin.
"""

from importlib import metadata
import warnings


def _check_for_conflicts():
  """Checks for conflicting packages and raises an error if any are found."""
  try:
    dist_map = metadata.packages_distributions()
  except Exception:  # pylint: disable=broad-except
    return

  xprof_providers = dist_map.get("xprof", [])
  if len(xprof_providers) > 1:
    raise RuntimeError(
        "Installation Conflict: Multiple 'xprof' providers found:"
        f" {xprof_providers}. Please install only one."
    )

_check_for_conflicts()
