# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
from bstack_utils.constants import bstack1111l11l1l1_opy_
def bstack1l11llll1_opy_(bstack1111l11l11l_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11lll111ll_opy_
    host = bstack11lll111ll_opy_(cli.config, [bstack1ll_opy_ (u"ࠧࡧࡰࡪࡵࠥᶆ"), bstack1ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣᶇ"), bstack1ll_opy_ (u"ࠢࡢࡲ࡬ࠦᶈ")], bstack1111l11l1l1_opy_)
    return bstack1ll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᶉ").format(host, bstack1111l11l11l_opy_)