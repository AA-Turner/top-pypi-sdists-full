# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from bstack_utils.constants import bstack111ll1llll1_opy_
def bstack11lll1ll_opy_(bstack111ll1lll1l_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack111l1lll1_opy_
    host = bstack111l1lll1_opy_(cli.config, [bstack1111l_opy_ (u"ࠧࡧࡰࡪࡵࠥᬺ"), bstack1111l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣᬻ"), bstack1111l_opy_ (u"ࠢࡢࡲ࡬ࠦᬼ")], bstack111ll1llll1_opy_)
    return bstack1111l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᬽ").format(host, bstack111ll1lll1l_opy_)