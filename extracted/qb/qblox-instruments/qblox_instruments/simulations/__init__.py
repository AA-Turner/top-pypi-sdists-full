try:
    from qblox_simulator_plugin.predistortions import (
        bias_tee_correction,
        bias_tee_correction_hw,
        exponential_overshoot_correction,
        exponential_overshoot_correction_hw,
        fir_correction,
        fir_correction_hw,
        get_filter_delay,
        get_impulse_response,
    )

except ModuleNotFoundError:
    from .predistortions import (
        exponential_overshoot_correction,
        fir_correction,
        get_filter_delay,
        get_impulse_response,
    )
