# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from browserstack_sdk.bstack1111l11l1_opy_ import bstack1ll11l1l11_opy_
from browserstack_sdk.bstack1111ll1lll_opy_ import RobotHandler
def bstack11ll11l111_opy_(framework):
    if framework.lower() == bstack1l11ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᫴"):
        return bstack1ll11l1l11_opy_.version()
    elif framework.lower() == bstack1l11ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ᫵"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11ll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ᫶"):
        import behave
        return behave.__version__
    else:
        return bstack1l11ll1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩ᫷")
def bstack11l1l1l1l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l11ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ᫸"))
        framework_version.append(importlib.metadata.version(bstack1l11ll1_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧ᫹")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ᫺"))
        framework_version.append(importlib.metadata.version(bstack1l11ll1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ᫻")))
    except:
        pass
    return {
        bstack1l11ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᫼"): bstack1l11ll1_opy_ (u"ࠧࡠࠩ᫽").join(framework_name),
        bstack1l11ll1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ᫾"): bstack1l11ll1_opy_ (u"ࠩࡢࠫ᫿").join(framework_version)
    }