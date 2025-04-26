# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1111lll1_opy_
bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
def bstack111l1ll11l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1ll11ll_opy_(bstack111l1l1llll_opy_, bstack111l1ll1111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1l1llll_opy_):
        with open(bstack111l1l1llll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1ll11l1_opy_(bstack111l1l1llll_opy_):
        pac = get_pac(url=bstack111l1l1llll_opy_)
    else:
        raise Exception(bstack1l11lll_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫᴜ").format(bstack111l1l1llll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l11lll_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨᴝ"), 80))
        bstack111l1ll1l11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll1l11_opy_ = bstack1l11lll_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧᴞ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1ll1111_opy_, bstack111l1ll1l11_opy_)
    return proxy_url
def bstack1ll1111111_opy_(config):
    return bstack1l11lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᴟ") in config or bstack1l11lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᴠ") in config
def bstack1lll1ll111_opy_(config):
    if not bstack1ll1111111_opy_(config):
        return
    if config.get(bstack1l11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᴡ")):
        return config.get(bstack1l11lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᴢ"))
    if config.get(bstack1l11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᴣ")):
        return config.get(bstack1l11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴤ"))
def bstack1llll1111l_opy_(config, bstack111l1ll1111_opy_):
    proxy = bstack1lll1ll111_opy_(config)
    proxies = {}
    if config.get(bstack1l11lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᴥ")) or config.get(bstack1l11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᴦ")):
        if proxy.endswith(bstack1l11lll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ᴧ")):
            proxies = bstack11ll1l1111_opy_(proxy, bstack111l1ll1111_opy_)
        else:
            proxies = {
                bstack1l11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴨ"): proxy
            }
    bstack11lll1l1ll_opy_.bstack111111l1l_opy_(bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᴩ"), proxies)
    return proxies
def bstack11ll1l1111_opy_(bstack111l1l1llll_opy_, bstack111l1ll1111_opy_):
    proxies = {}
    global bstack111l1l1lll1_opy_
    if bstack1l11lll_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧᴪ") in globals():
        return bstack111l1l1lll1_opy_
    try:
        proxy = bstack111l1ll11ll_opy_(bstack111l1l1llll_opy_, bstack111l1ll1111_opy_)
        if bstack1l11lll_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧᴫ") in proxy:
            proxies = {}
        elif bstack1l11lll_opy_ (u"ࠨࡈࡕࡖࡓࠦᴬ") in proxy or bstack1l11lll_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨᴭ") in proxy or bstack1l11lll_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢᴮ") in proxy:
            bstack111l1ll111l_opy_ = proxy.split(bstack1l11lll_opy_ (u"ࠤࠣࠦᴯ"))
            if bstack1l11lll_opy_ (u"ࠥ࠾࠴࠵ࠢᴰ") in bstack1l11lll_opy_ (u"ࠦࠧᴱ").join(bstack111l1ll111l_opy_[1:]):
                proxies = {
                    bstack1l11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᴲ"): bstack1l11lll_opy_ (u"ࠨࠢᴳ").join(bstack111l1ll111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᴴ"): str(bstack111l1ll111l_opy_[0]).lower() + bstack1l11lll_opy_ (u"ࠣ࠼࠲࠳ࠧᴵ") + bstack1l11lll_opy_ (u"ࠤࠥᴶ").join(bstack111l1ll111l_opy_[1:])
                }
        elif bstack1l11lll_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤᴷ") in proxy:
            bstack111l1ll111l_opy_ = proxy.split(bstack1l11lll_opy_ (u"ࠦࠥࠨᴸ"))
            if bstack1l11lll_opy_ (u"ࠧࡀ࠯࠰ࠤᴹ") in bstack1l11lll_opy_ (u"ࠨࠢᴺ").join(bstack111l1ll111l_opy_[1:]):
                proxies = {
                    bstack1l11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᴻ"): bstack1l11lll_opy_ (u"ࠣࠤᴼ").join(bstack111l1ll111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴽ"): bstack1l11lll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᴾ") + bstack1l11lll_opy_ (u"ࠦࠧᴿ").join(bstack111l1ll111l_opy_[1:])
                }
        else:
            proxies = {
                bstack1l11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᵀ"): proxy
            }
    except Exception as e:
        print(bstack1l11lll_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᵁ"), bstack11l1111lll1_opy_.format(bstack111l1l1llll_opy_, str(e)))
    bstack111l1l1lll1_opy_ = proxies
    return proxies