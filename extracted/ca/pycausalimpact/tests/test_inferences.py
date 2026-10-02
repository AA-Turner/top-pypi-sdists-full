# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

import numpy as np
import pandas as pd
import pytest
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.statespace.structural import UnobservedComponents

from causalimpact import CausalImpact
from causalimpact.inferences import Inferences
from causalimpact.misc import standardize


@pytest.fixture
def inferer():
    return Inferences(10)


def test_inferer_cto():
    inferer = Inferences(10)
    assert inferer.n_sims == 10
    assert inferer.inferences is None
    assert inferer.p_value is None


def test_p_value_read_only(inferer):
    with pytest.raises(AttributeError):
        inferer.p_value = 0.4
        inferer.p_value = 0.3


def test_p_value_bigger_than_one(inferer):
    with pytest.raises(ValueError):
        inferer.p_value = 2


def test_p_value_lower_than_zero(inferer):
    with pytest.raises(ValueError):
        inferer.p_value = -1


def test_inferences_read_only(inferer):
    with pytest.raises(AttributeError):
        inferer.inferences = pd.DataFrame([1, 2, 3])
        inferer.inferences = pd.DataFrame([1, 2, 3])


def test_inferences_raises_invalid_input(inferer):
    with pytest.raises(ValueError):
        inferer.inferences = 1


def test_default_causal_cto_w_positive_signal():
    np.random.seed(1)
    ar = np.r_[1, 0.9]
    ma = np.array([1])
    arma_process = ArmaProcess(ar, ma)
    X = 100 + arma_process.generate_sample(nsample=100)
    y = 1.2 * X + np.random.normal(size=(100))
    y[70:] += 1
    data = pd.DataFrame({'y': y, 'X': X}, columns=['y', 'X'])
    ci = CausalImpact(data, [0, 69], [70, 99])
    assert ci.p_value < 0.05


def test_causal_cto_w_positive_signal_no_standardization():
    np.random.seed(1)
    ar = np.r_[1, 0.9]
    ma = np.array([1])
    arma_process = ArmaProcess(ar, ma)
    X = 100 + arma_process.generate_sample(nsample=100)
    y = 1.2 * X + np.random.normal(size=(100))
    y[70:] += 1
    data = pd.DataFrame({'y': y, 'X': X}, columns=['y', 'X'])
    ci = CausalImpact(data, [0, 69], [70, 99], standardize=False)
    assert ci.p_value < 0.05


def test_default_causal_cto_w_negative_signal():
    np.random.seed(1)
    ar = np.r_[1, 0.9]
    ma = np.array([1])
    arma_process = ArmaProcess(ar, ma)
    X = 100 + arma_process.generate_sample(nsample=100)
    y = 1.2 * X + np.random.normal(size=(100))
    y[70:] -= 1
    data = pd.DataFrame({'y': y, 'X': X}, columns=['y', 'X'])
    ci = CausalImpact(data, [0, 69], [70, 99])
    assert ci.p_value < 0.05


def test_causal_cto_w_negative_signal_no_standardization():
    np.random.seed(1)
    ar = np.r_[1, 0.9]
    ma = np.array([1])
    arma_process = ArmaProcess(ar, ma)
    X = 100 + arma_process.generate_sample(nsample=100)
    y = 1.2 * X + np.random.normal(size=(100))
    y[70:] -= 1
    data = pd.DataFrame({'y': y, 'X': X}, columns=['y', 'X'])
    ci = CausalImpact(data, [0, 69], [70, 99], standardize=False)
    assert ci.p_value < 0.05


def test_default_causal_cto_no_signal():
    np.random.seed(1)
    ar = np.r_[1, 0.9]
    ma = np.array([1])
    arma_process = ArmaProcess(ar, ma)
    X = 100 + arma_process.generate_sample(nsample=100)
    y = 1.2 * X + np.random.normal(size=(100))
    data = pd.DataFrame({'y': y, 'X': X}, columns=['y', 'X'])
    ci = CausalImpact(data, [0, 69], [70, 99])
    assert ci.p_value > 0.05


def test_lower_upper_percentile():
    np.random.seed(1)
    ar = np.r_[1, 0.9]
    ma = np.array([1])
    arma_process = ArmaProcess(ar, ma)
    X = 100 + arma_process.generate_sample(nsample=100)
    y = 1.2 * X + np.random.normal(size=(100))
    data = pd.DataFrame({'y': y, 'X': X}, columns=['y', 'X'])
    ci = CausalImpact(data, [0, 69], [70, 99])
    ci.lower_upper_percentile == [2.5, 97.5]


def test_simulated_y_default_model():
    np.random.seed(1)
    ar = np.r_[1, 0.9]
    ma = np.array([1])
    arma_process = ArmaProcess(ar, ma)
    X = 100 + arma_process.generate_sample(nsample=100)
    y = 1.2 * X + np.random.normal(size=(100))
    data = pd.DataFrame({'y': y, 'X': X}, columns=['y', 'X'])
    ci = CausalImpact(data, [0, 69], [70, 99])

    assert ci.simulated_y.shape == (1000, 30)

    lower, upper = np.percentile(ci.simulated_y.mean(axis=1), [5, 95])
    assert lower > 119
    assert upper < 121


def test_simulated_y_custom_model():
    np.random.seed(1)
    ar = np.r_[1, 0.9]
    ma = np.array([1])
    arma_process = ArmaProcess(ar, ma)
    X = 100 + arma_process.generate_sample(nsample=100)
    y = 1.2 * X + np.random.normal(size=(100))
    data = pd.DataFrame({'y': y, 'X': X}, columns=['y', 'X'])
    intervention_idx = 70
    normed_pre_data, _ = standardize(data.iloc[:intervention_idx])

    model = UnobservedComponents(
        endog=normed_pre_data['y'].iloc[0:intervention_idx],
        level='llevel',
        exog=normed_pre_data['X'].iloc[0:intervention_idx]
    )

    ci = CausalImpact(data, [0, 69], [70, 99], model=model)

    assert ci.simulated_y.shape == (1000, 30)

    lower, upper = np.percentile(ci.simulated_y.mean(axis=1), [5, 95])
    assert lower > 119
    assert upper < 121
