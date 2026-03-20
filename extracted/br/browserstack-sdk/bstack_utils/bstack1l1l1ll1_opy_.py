# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
from bstack_utils.constants import bstack111ll111l11_opy_
def bstack1lllll1l11_opy_(bstack111ll111l1l_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11111l11ll_opy_
    host = bstack11111l11ll_opy_(cli.config, [bstack11lll1_opy_ (u"ࠢࡢࡲ࡬ࡷࠧᮂ"), bstack11lll1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥᮃ"), bstack11lll1_opy_ (u"ࠤࡤࡴ࡮ࠨᮄ")], bstack111ll111l11_opy_)
    return bstack11lll1_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᮅ").format(host, bstack111ll111l1l_opy_)