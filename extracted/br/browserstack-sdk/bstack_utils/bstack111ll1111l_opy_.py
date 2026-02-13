# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from bstack_utils.constants import bstack11l11111l11_opy_
def bstack11l111ll1_opy_(bstack11l111111ll_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l11l1llll_opy_
    host = bstack1l11l1llll_opy_(cli.config, [bstack11l11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨᥓ"), bstack11l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᥔ"), bstack11l11_opy_ (u"ࠥࡥࡵ࡯ࠢᥕ")], bstack11l11111l11_opy_)
    return bstack11l11_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᥖ").format(host, bstack11l111111ll_opy_)