"""Navigation progress bar for Mantine."""

from reflex.vars.base import Var

from reflex_enterprise.components.component import ComponentEnterprise


class NProgress(ComponentEnterprise):
    """NProgress component for Mantine."""

    library = "@mantine/nprogress@8.3.9"

    tag = "NProgress"

    alias = "MantineNProgress"

    # Progress bar color
    color: Var[str]

    # Initial progress value, 0 by default
    initial_progress: Var[int]

    # Props to pass down to the Portal when withinPortal is true
    portal_props: Var[dict]

    # Controls height of the progress bar
    size: Var[int]

    # Step interval in ms, 500 by default
    step_interval: Var[int]

    # Component store, controls state
    store: Var[dict]

    # Determines whether the progress bar should be rendered within Portal, true by default
    within_portal: Var[bool]

    # Progressbar z-index, 9999 by default
    z_index: Var[int]
