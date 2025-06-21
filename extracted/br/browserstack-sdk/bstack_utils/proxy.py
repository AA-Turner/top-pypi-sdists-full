# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111ll1111l1_opy_
bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
def bstack11111lll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11111lll11l_opy_(bstack11111lll1l1_opy_, bstack11111ll1lll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111lll1l1_opy_):
        with open(bstack11111lll1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111lll111_opy_(bstack11111lll1l1_opy_):
        pac = get_pac(url=bstack11111lll1l1_opy_)
    else:
        raise Exception(bstack1l1l1l1_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ṙ").format(bstack11111lll1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1l1l1_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣṚ"), 80))
        bstack11111llll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111llll11_opy_ = bstack1l1l1l1_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩṛ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111ll1lll_opy_, bstack11111llll11_opy_)
    return proxy_url
def bstack1ll1ll1111_opy_(config):
    return bstack1l1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬṜ") in config or bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧṝ") in config
def bstack11l1111ll1_opy_(config):
    if not bstack1ll1ll1111_opy_(config):
        return
    if config.get(bstack1l1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧṞ")):
        return config.get(bstack1l1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨṟ"))
    if config.get(bstack1l1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪṠ")):
        return config.get(bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫṡ"))
def bstack11ll11l1_opy_(config, bstack11111ll1lll_opy_):
    proxy = bstack11l1111ll1_opy_(config)
    proxies = {}
    if config.get(bstack1l1l1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫṢ")) or config.get(bstack1l1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ṣ")):
        if proxy.endswith(bstack1l1l1l1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨṤ")):
            proxies = bstack1ll1l11lll_opy_(proxy, bstack11111ll1lll_opy_)
        else:
            proxies = {
                bstack1l1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪṥ"): proxy
            }
    bstack11lll11111_opy_.bstack1llll1111_opy_(bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬṦ"), proxies)
    return proxies
def bstack1ll1l11lll_opy_(bstack11111lll1l1_opy_, bstack11111ll1lll_opy_):
    proxies = {}
    global bstack11111llll1l_opy_
    if bstack1l1l1l1_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩṧ") in globals():
        return bstack11111llll1l_opy_
    try:
        proxy = bstack11111lll11l_opy_(bstack11111lll1l1_opy_, bstack11111ll1lll_opy_)
        if bstack1l1l1l1_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢṨ") in proxy:
            proxies = {}
        elif bstack1l1l1l1_opy_ (u"ࠣࡊࡗࡘࡕࠨṩ") in proxy or bstack1l1l1l1_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣṪ") in proxy or bstack1l1l1l1_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤṫ") in proxy:
            bstack11111lll1ll_opy_ = proxy.split(bstack1l1l1l1_opy_ (u"ࠦࠥࠨṬ"))
            if bstack1l1l1l1_opy_ (u"ࠧࡀ࠯࠰ࠤṭ") in bstack1l1l1l1_opy_ (u"ࠨࠢṮ").join(bstack11111lll1ll_opy_[1:]):
                proxies = {
                    bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ṯ"): bstack1l1l1l1_opy_ (u"ࠣࠤṰ").join(bstack11111lll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨṱ"): str(bstack11111lll1ll_opy_[0]).lower() + bstack1l1l1l1_opy_ (u"ࠥ࠾࠴࠵ࠢṲ") + bstack1l1l1l1_opy_ (u"ࠦࠧṳ").join(bstack11111lll1ll_opy_[1:])
                }
        elif bstack1l1l1l1_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦṴ") in proxy:
            bstack11111lll1ll_opy_ = proxy.split(bstack1l1l1l1_opy_ (u"ࠨࠠࠣṵ"))
            if bstack1l1l1l1_opy_ (u"ࠢ࠻࠱࠲ࠦṶ") in bstack1l1l1l1_opy_ (u"ࠣࠤṷ").join(bstack11111lll1ll_opy_[1:]):
                proxies = {
                    bstack1l1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨṸ"): bstack1l1l1l1_opy_ (u"ࠥࠦṹ").join(bstack11111lll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪṺ"): bstack1l1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨṻ") + bstack1l1l1l1_opy_ (u"ࠨࠢṼ").join(bstack11111lll1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ṽ"): proxy
            }
    except Exception as e:
        print(bstack1l1l1l1_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧṾ"), bstack111ll1111l1_opy_.format(bstack11111lll1l1_opy_, str(e)))
    bstack11111llll1l_opy_ = proxies
    return proxies