# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
from bstack_utils.constants import bstack11l111l11ll_opy_
def bstack1l1l1111ll_opy_(bstack11l111l11l1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1llll1ll_opy_
    host = bstack1llll1ll_opy_(cli.config, [bstack11ll111_opy_ (u"ࠣࡣࡳ࡭ࡸࠨᥚ"), bstack11ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᥛ"), bstack11ll111_opy_ (u"ࠥࡥࡵ࡯ࠢᥜ")], bstack11l111l11ll_opy_)
    return bstack11ll111_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᥝ").format(host, bstack11l111l11l1_opy_)