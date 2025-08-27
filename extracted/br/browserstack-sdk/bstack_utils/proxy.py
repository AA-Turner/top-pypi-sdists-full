# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1l11l1l_opy_
bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
def bstack11111111lll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111111l1ll_opy_(bstack1111111ll11_opy_, bstack1111111l111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111111ll11_opy_):
        with open(bstack1111111ll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111111lll_opy_(bstack1111111ll11_opy_):
        pac = get_pac(url=bstack1111111ll11_opy_)
    else:
        raise Exception(bstack1111lll_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫἷ").format(bstack1111111ll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1111lll_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨἸ"), 80))
        bstack1111111ll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111111ll1l_opy_ = bstack1111lll_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧἹ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111111l111_opy_, bstack1111111ll1l_opy_)
    return proxy_url
def bstack1lll111ll1_opy_(config):
    return bstack1111lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪἺ") in config or bstack1111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬἻ") in config
def bstack1llll1ll1_opy_(config):
    if not bstack1lll111ll1_opy_(config):
        return
    if config.get(bstack1111lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬἼ")):
        return config.get(bstack1111lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭Ἵ"))
    if config.get(bstack1111lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨἾ")):
        return config.get(bstack1111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩἿ"))
def bstack1lll1llll1_opy_(config, bstack1111111l111_opy_):
    proxy = bstack1llll1ll1_opy_(config)
    proxies = {}
    if config.get(bstack1111lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩὀ")) or config.get(bstack1111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫὁ")):
        if proxy.endswith(bstack1111lll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ὂ")):
            proxies = bstack11lll11ll1_opy_(proxy, bstack1111111l111_opy_)
        else:
            proxies = {
                bstack1111lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨὃ"): proxy
            }
    bstack1ll111ll11_opy_.bstack11111l1l_opy_(bstack1111lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪὄ"), proxies)
    return proxies
def bstack11lll11ll1_opy_(bstack1111111ll11_opy_, bstack1111111l111_opy_):
    proxies = {}
    global bstack1111111l11l_opy_
    if bstack1111lll_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧὅ") in globals():
        return bstack1111111l11l_opy_
    try:
        proxy = bstack1111111l1ll_opy_(bstack1111111ll11_opy_, bstack1111111l111_opy_)
        if bstack1111lll_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧ὆") in proxy:
            proxies = {}
        elif bstack1111lll_opy_ (u"ࠨࡈࡕࡖࡓࠦ὇") in proxy or bstack1111lll_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨὈ") in proxy or bstack1111lll_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢὉ") in proxy:
            bstack1111111l1l1_opy_ = proxy.split(bstack1111lll_opy_ (u"ࠤࠣࠦὊ"))
            if bstack1111lll_opy_ (u"ࠥ࠾࠴࠵ࠢὋ") in bstack1111lll_opy_ (u"ࠦࠧὌ").join(bstack1111111l1l1_opy_[1:]):
                proxies = {
                    bstack1111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὍ"): bstack1111lll_opy_ (u"ࠨࠢ὎").join(bstack1111111l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭὏"): str(bstack1111111l1l1_opy_[0]).lower() + bstack1111lll_opy_ (u"ࠣ࠼࠲࠳ࠧὐ") + bstack1111lll_opy_ (u"ࠤࠥὑ").join(bstack1111111l1l1_opy_[1:])
                }
        elif bstack1111lll_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤὒ") in proxy:
            bstack1111111l1l1_opy_ = proxy.split(bstack1111lll_opy_ (u"ࠦࠥࠨὓ"))
            if bstack1111lll_opy_ (u"ࠧࡀ࠯࠰ࠤὔ") in bstack1111lll_opy_ (u"ࠨࠢὕ").join(bstack1111111l1l1_opy_[1:]):
                proxies = {
                    bstack1111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ὖ"): bstack1111lll_opy_ (u"ࠣࠤὗ").join(bstack1111111l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ὘"): bstack1111lll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦὙ") + bstack1111lll_opy_ (u"ࠦࠧ὚").join(bstack1111111l1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack1111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὛ"): proxy
            }
    except Exception as e:
        print(bstack1111lll_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ὜"), bstack111l1l11l1l_opy_.format(bstack1111111ll11_opy_, str(e)))
    bstack1111111l11l_opy_ = proxies
    return proxies