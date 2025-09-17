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
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1l111ll_opy_
bstack111lllll11_opy_ = Config.bstack1lll111l1l_opy_()
def bstack111111111ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111111111l1_opy_(bstack1111111111l_opy_, bstack11111111l1l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111111111l_opy_):
        with open(bstack1111111111l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111111111ll_opy_(bstack1111111111l_opy_):
        pac = get_pac(url=bstack1111111111l_opy_)
    else:
        raise Exception(bstack1l11ll1_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧἺ").format(bstack1111111111l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l11ll1_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤἻ"), 80))
        bstack11111111ll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111111ll1_opy_ = bstack1l11ll1_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪἼ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111111l1l_opy_, bstack11111111ll1_opy_)
    return proxy_url
def bstack1l111ll11_opy_(config):
    return bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭Ἵ") in config or bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨἾ") in config
def bstack111l1l1l_opy_(config):
    if not bstack1l111ll11_opy_(config):
        return
    if config.get(bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨἿ")):
        return config.get(bstack1l11ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩὀ"))
    if config.get(bstack1l11ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫὁ")):
        return config.get(bstack1l11ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬὂ"))
def bstack11llllll11_opy_(config, bstack11111111l1l_opy_):
    proxy = bstack111l1l1l_opy_(config)
    proxies = {}
    if config.get(bstack1l11ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬὃ")) or config.get(bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧὄ")):
        if proxy.endswith(bstack1l11ll1_opy_ (u"ࠫ࠳ࡶࡡࡤࠩὅ")):
            proxies = bstack111lll1lll_opy_(proxy, bstack11111111l1l_opy_)
        else:
            proxies = {
                bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ὆"): proxy
            }
    bstack111lllll11_opy_.bstack11l111l1ll_opy_(bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭὇"), proxies)
    return proxies
def bstack111lll1lll_opy_(bstack1111111111l_opy_, bstack11111111l1l_opy_):
    proxies = {}
    global bstack11111111lll_opy_
    if bstack1l11ll1_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪὈ") in globals():
        return bstack11111111lll_opy_
    try:
        proxy = bstack111111111l1_opy_(bstack1111111111l_opy_, bstack11111111l1l_opy_)
        if bstack1l11ll1_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣὉ") in proxy:
            proxies = {}
        elif bstack1l11ll1_opy_ (u"ࠤࡋࡘ࡙ࡖࠢὊ") in proxy or bstack1l11ll1_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤὋ") in proxy or bstack1l11ll1_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥὌ") in proxy:
            bstack11111111l11_opy_ = proxy.split(bstack1l11ll1_opy_ (u"ࠧࠦࠢὍ"))
            if bstack1l11ll1_opy_ (u"ࠨ࠺࠰࠱ࠥ὎") in bstack1l11ll1_opy_ (u"ࠢࠣ὏").join(bstack11111111l11_opy_[1:]):
                proxies = {
                    bstack1l11ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧὐ"): bstack1l11ll1_opy_ (u"ࠤࠥὑ").join(bstack11111111l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὒ"): str(bstack11111111l11_opy_[0]).lower() + bstack1l11ll1_opy_ (u"ࠦ࠿࠵࠯ࠣὓ") + bstack1l11ll1_opy_ (u"ࠧࠨὔ").join(bstack11111111l11_opy_[1:])
                }
        elif bstack1l11ll1_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧὕ") in proxy:
            bstack11111111l11_opy_ = proxy.split(bstack1l11ll1_opy_ (u"ࠢࠡࠤὖ"))
            if bstack1l11ll1_opy_ (u"ࠣ࠼࠲࠳ࠧὗ") in bstack1l11ll1_opy_ (u"ࠤࠥ὘").join(bstack11111111l11_opy_[1:]):
                proxies = {
                    bstack1l11ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὙ"): bstack1l11ll1_opy_ (u"ࠦࠧ὚").join(bstack11111111l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὛ"): bstack1l11ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ὜") + bstack1l11ll1_opy_ (u"ࠢࠣὝ").join(bstack11111111l11_opy_[1:])
                }
        else:
            proxies = {
                bstack1l11ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ὞"): proxy
            }
    except Exception as e:
        print(bstack1l11ll1_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨὟ"), bstack111l1l111ll_opy_.format(bstack1111111111l_opy_, str(e)))
    bstack11111111lll_opy_ = proxies
    return proxies