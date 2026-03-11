# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from bstack_utils.constants import bstack1ll1llll1l11_opy_
def bstack1lll1l11_opy_(bstack11111llllll_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l1ll11lll_opy_
    host = bstack1l1ll11lll_opy_(cli.config, [bstack1ll111_opy_ (u"ࠧࡧࡰࡪࡵࠥ≏"), bstack1ll111_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ≐"), bstack1ll111_opy_ (u"ࠢࡢࡲ࡬ࠦ≑")], bstack1ll1llll1l11_opy_)
    return bstack1ll111_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ≒").format(host, bstack11111llllll_opy_)