# -*- coding: utf-8 -*-
def pytest_load_initial_conftests():
    # make sure we monkey_patch before local conftests
    import eventlet

    eventlet.monkey_patch()
