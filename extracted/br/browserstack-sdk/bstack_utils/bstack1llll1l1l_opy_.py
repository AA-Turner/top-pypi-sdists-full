# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from bstack_utils.constants import bstack111llll11ll_opy_
def bstack11ll1ll1l1_opy_(bstack111llll1l11_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l1ll1l11l_opy_
    host = bstack1l1ll1l11l_opy_(cli.config, [bstack1lll1l_opy_ (u"ࠧࡧࡰࡪࡵࠥ᪄"), bstack1lll1l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ᪅"), bstack1lll1l_opy_ (u"ࠢࡢࡲ࡬ࠦ᪆")], bstack111llll11ll_opy_)
    return bstack1lll1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ᪇").format(host, bstack111llll1l11_opy_)