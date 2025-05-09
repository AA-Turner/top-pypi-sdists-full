# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1111ll1l_opy_
bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
def bstack111l1ll111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1l1llll_opy_(bstack111l1l1ll11_opy_, bstack111l1ll11l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1l1ll11_opy_):
        with open(bstack111l1l1ll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1ll111l_opy_(bstack111l1l1ll11_opy_):
        pac = get_pac(url=bstack111l1l1ll11_opy_)
    else:
        raise Exception(bstack11lll_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨᴧ").format(bstack111l1l1ll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11lll_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥᴨ"), 80))
        bstack111l1ll1111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll1111_opy_ = bstack11lll_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫᴩ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1ll11l1_opy_, bstack111l1ll1111_opy_)
    return proxy_url
def bstack11lll11l_opy_(config):
    return bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴪ") in config or bstack11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴫ") in config
def bstack1l1lll11_opy_(config):
    if not bstack11lll11l_opy_(config):
        return
    if config.get(bstack11lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᴬ")):
        return config.get(bstack11lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᴭ"))
    if config.get(bstack11lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᴮ")):
        return config.get(bstack11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᴯ"))
def bstack1ll111111l_opy_(config, bstack111l1ll11l1_opy_):
    proxy = bstack1l1lll11_opy_(config)
    proxies = {}
    if config.get(bstack11lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᴰ")) or config.get(bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᴱ")):
        if proxy.endswith(bstack11lll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪᴲ")):
            proxies = bstack1l111l1l1l_opy_(proxy, bstack111l1ll11l1_opy_)
        else:
            proxies = {
                bstack11lll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᴳ"): proxy
            }
    bstack1llllll11_opy_.bstack1llllll1l1_opy_(bstack11lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧᴴ"), proxies)
    return proxies
def bstack1l111l1l1l_opy_(bstack111l1l1ll11_opy_, bstack111l1ll11l1_opy_):
    proxies = {}
    global bstack111l1l1ll1l_opy_
    if bstack11lll_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫᴵ") in globals():
        return bstack111l1l1ll1l_opy_
    try:
        proxy = bstack111l1l1llll_opy_(bstack111l1l1ll11_opy_, bstack111l1ll11l1_opy_)
        if bstack11lll_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤᴶ") in proxy:
            proxies = {}
        elif bstack11lll_opy_ (u"ࠥࡌ࡙࡚ࡐࠣᴷ") in proxy or bstack11lll_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥᴸ") in proxy or bstack11lll_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦᴹ") in proxy:
            bstack111l1l1lll1_opy_ = proxy.split(bstack11lll_opy_ (u"ࠨࠠࠣᴺ"))
            if bstack11lll_opy_ (u"ࠢ࠻࠱࠲ࠦᴻ") in bstack11lll_opy_ (u"ࠣࠤᴼ").join(bstack111l1l1lll1_opy_[1:]):
                proxies = {
                    bstack11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴽ"): bstack11lll_opy_ (u"ࠥࠦᴾ").join(bstack111l1l1lll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᴿ"): str(bstack111l1l1lll1_opy_[0]).lower() + bstack11lll_opy_ (u"ࠧࡀ࠯࠰ࠤᵀ") + bstack11lll_opy_ (u"ࠨࠢᵁ").join(bstack111l1l1lll1_opy_[1:])
                }
        elif bstack11lll_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨᵂ") in proxy:
            bstack111l1l1lll1_opy_ = proxy.split(bstack11lll_opy_ (u"ࠣࠢࠥᵃ"))
            if bstack11lll_opy_ (u"ࠤ࠽࠳࠴ࠨᵄ") in bstack11lll_opy_ (u"ࠥࠦᵅ").join(bstack111l1l1lll1_opy_[1:]):
                proxies = {
                    bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᵆ"): bstack11lll_opy_ (u"ࠧࠨᵇ").join(bstack111l1l1lll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᵈ"): bstack11lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᵉ") + bstack11lll_opy_ (u"ࠣࠤᵊ").join(bstack111l1l1lll1_opy_[1:])
                }
        else:
            proxies = {
                bstack11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᵋ"): proxy
            }
    except Exception as e:
        print(bstack11lll_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᵌ"), bstack11l1111ll1l_opy_.format(bstack111l1l1ll11_opy_, str(e)))
    bstack111l1l1ll1l_opy_ = proxies
    return proxies