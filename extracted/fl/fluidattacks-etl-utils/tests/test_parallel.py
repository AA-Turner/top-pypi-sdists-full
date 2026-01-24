import pytest
from fa_purity import (
    Cmd,
    PureIterFactory,
)

from fluidattacks_etl_utils.parallel import (
    ThreadPool,
)
from fluidattacks_etl_utils.retry import (
    sleep_cmd,
)


@pytest.mark.timeout(2)
def test_threads() -> None:
    cmd: Cmd[None] = ThreadPool.new(10).bind(
        lambda p: p.in_threads_none(
            PureIterFactory.from_range(range(10)).map(lambda _: sleep_cmd(1)),
        ),
    )
    with pytest.raises(SystemExit):
        cmd.compute()
