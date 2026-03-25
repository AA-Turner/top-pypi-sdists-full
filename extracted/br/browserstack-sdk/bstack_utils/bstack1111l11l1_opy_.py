# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
from bstack_utils.constants import bstack111ll11111l_opy_
def bstack11l11l1l1l_opy_(bstack111ll111111_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11l1lll11_opy_
    host = bstack11l1lll11_opy_(cli.config, [bstack1l1_opy_ (u"ࠣࡣࡳ࡭ࡸࠨᮊ"), bstack1l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᮋ"), bstack1l1_opy_ (u"ࠥࡥࡵ࡯ࠢᮌ")], bstack111ll11111l_opy_)
    return bstack1l1_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᮍ").format(host, bstack111ll111111_opy_)