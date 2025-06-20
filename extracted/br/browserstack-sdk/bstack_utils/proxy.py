# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111ll1111l1_opy_
bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
def bstack11111lll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11111ll1lll_opy_(bstack11111llll1l_opy_, bstack11111llll11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111llll1l_opy_):
        with open(bstack11111llll1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111lll111_opy_(bstack11111llll1l_opy_):
        pac = get_pac(url=bstack11111llll1l_opy_)
    else:
        raise Exception(bstack11ll11_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬṘ").format(bstack11111llll1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11ll11_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢṙ"), 80))
        bstack11111lll1ll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111lll1ll_opy_ = bstack11ll11_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨṚ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111llll11_opy_, bstack11111lll1ll_opy_)
    return proxy_url
def bstack1ll111l11l_opy_(config):
    return bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫṛ") in config or bstack11ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭Ṝ") in config
def bstack1l111111l1_opy_(config):
    if not bstack1ll111l11l_opy_(config):
        return
    if config.get(bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ṝ")):
        return config.get(bstack11ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧṞ"))
    if config.get(bstack11ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩṟ")):
        return config.get(bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪṠ"))
def bstack1l1ll111_opy_(config, bstack11111llll11_opy_):
    proxy = bstack1l111111l1_opy_(config)
    proxies = {}
    if config.get(bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪṡ")) or config.get(bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬṢ")):
        if proxy.endswith(bstack11ll11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧṣ")):
            proxies = bstack1ll1lll1_opy_(proxy, bstack11111llll11_opy_)
        else:
            proxies = {
                bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩṤ"): proxy
            }
    bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫṥ"), proxies)
    return proxies
def bstack1ll1lll1_opy_(bstack11111llll1l_opy_, bstack11111llll11_opy_):
    proxies = {}
    global bstack11111lll1l1_opy_
    if bstack11ll11_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨṦ") in globals():
        return bstack11111lll1l1_opy_
    try:
        proxy = bstack11111ll1lll_opy_(bstack11111llll1l_opy_, bstack11111llll11_opy_)
        if bstack11ll11_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨṧ") in proxy:
            proxies = {}
        elif bstack11ll11_opy_ (u"ࠢࡉࡖࡗࡔࠧṨ") in proxy or bstack11ll11_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢṩ") in proxy or bstack11ll11_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣṪ") in proxy:
            bstack11111lll11l_opy_ = proxy.split(bstack11ll11_opy_ (u"ࠥࠤࠧṫ"))
            if bstack11ll11_opy_ (u"ࠦ࠿࠵࠯ࠣṬ") in bstack11ll11_opy_ (u"ࠧࠨṭ").join(bstack11111lll11l_opy_[1:]):
                proxies = {
                    bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬṮ"): bstack11ll11_opy_ (u"ࠢࠣṯ").join(bstack11111lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧṰ"): str(bstack11111lll11l_opy_[0]).lower() + bstack11ll11_opy_ (u"ࠤ࠽࠳࠴ࠨṱ") + bstack11ll11_opy_ (u"ࠥࠦṲ").join(bstack11111lll11l_opy_[1:])
                }
        elif bstack11ll11_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥṳ") in proxy:
            bstack11111lll11l_opy_ = proxy.split(bstack11ll11_opy_ (u"ࠧࠦࠢṴ"))
            if bstack11ll11_opy_ (u"ࠨ࠺࠰࠱ࠥṵ") in bstack11ll11_opy_ (u"ࠢࠣṶ").join(bstack11111lll11l_opy_[1:]):
                proxies = {
                    bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧṷ"): bstack11ll11_opy_ (u"ࠤࠥṸ").join(bstack11111lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩṹ"): bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧṺ") + bstack11ll11_opy_ (u"ࠧࠨṻ").join(bstack11111lll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬṼ"): proxy
            }
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦṽ"), bstack111ll1111l1_opy_.format(bstack11111llll1l_opy_, str(e)))
    bstack11111lll1l1_opy_ = proxies
    return proxies