# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from bstack_utils.constants import bstack11l11llll1l_opy_
def bstack11l1l1ll11_opy_(bstack11l11lllll1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1lll1l111l_opy_
    host = bstack1lll1l111l_opy_(cli.config, [bstack11l1ll1_opy_ (u"ࠤࡤࡴ࡮ࡹࠢᢉ"), bstack11l1ll1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᢊ"), bstack11l1ll1_opy_ (u"ࠦࡦࡶࡩࠣᢋ")], bstack11l11llll1l_opy_)
    return bstack11l1ll1_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᢌ").format(host, bstack11l11lllll1_opy_)