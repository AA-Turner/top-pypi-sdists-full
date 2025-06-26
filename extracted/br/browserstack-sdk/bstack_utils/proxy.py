# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1llll1l_opy_
bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
def bstack11111ll11ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11111ll1l11_opy_(bstack11111ll111l_opy_, bstack11111ll1l1l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111ll111l_opy_):
        with open(bstack11111ll111l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111ll11ll_opy_(bstack11111ll111l_opy_):
        pac = get_pac(url=bstack11111ll111l_opy_)
    else:
        raise Exception(bstack11ll1l1_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪṹ").format(bstack11111ll111l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11ll1l1_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧṺ"), 80))
        bstack11111ll1ll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111ll1ll1_opy_ = bstack11ll1l1_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ṻ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111ll1l1l_opy_, bstack11111ll1ll1_opy_)
    return proxy_url
def bstack11lll1ll_opy_(config):
    return bstack11ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩṼ") in config or bstack11ll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫṽ") in config
def bstack1l1ll11l_opy_(config):
    if not bstack11lll1ll_opy_(config):
        return
    if config.get(bstack11ll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫṾ")):
        return config.get(bstack11ll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬṿ"))
    if config.get(bstack11ll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧẀ")):
        return config.get(bstack11ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨẁ"))
def bstack1lll11l11l_opy_(config, bstack11111ll1l1l_opy_):
    proxy = bstack1l1ll11l_opy_(config)
    proxies = {}
    if config.get(bstack11ll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨẂ")) or config.get(bstack11ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪẃ")):
        if proxy.endswith(bstack11ll1l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬẄ")):
            proxies = bstack1l1l1ll1l1_opy_(proxy, bstack11111ll1l1l_opy_)
        else:
            proxies = {
                bstack11ll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧẅ"): proxy
            }
    bstack1111ll111_opy_.bstack1lll1lll_opy_(bstack11ll1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩẆ"), proxies)
    return proxies
def bstack1l1l1ll1l1_opy_(bstack11111ll111l_opy_, bstack11111ll1l1l_opy_):
    proxies = {}
    global bstack11111ll1111_opy_
    if bstack11ll1l1_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ẇ") in globals():
        return bstack11111ll1111_opy_
    try:
        proxy = bstack11111ll1l11_opy_(bstack11111ll111l_opy_, bstack11111ll1l1l_opy_)
        if bstack11ll1l1_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦẈ") in proxy:
            proxies = {}
        elif bstack11ll1l1_opy_ (u"ࠧࡎࡔࡕࡒࠥẉ") in proxy or bstack11ll1l1_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧẊ") in proxy or bstack11ll1l1_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨẋ") in proxy:
            bstack11111ll11l1_opy_ = proxy.split(bstack11ll1l1_opy_ (u"ࠣࠢࠥẌ"))
            if bstack11ll1l1_opy_ (u"ࠤ࠽࠳࠴ࠨẍ") in bstack11ll1l1_opy_ (u"ࠥࠦẎ").join(bstack11111ll11l1_opy_[1:]):
                proxies = {
                    bstack11ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪẏ"): bstack11ll1l1_opy_ (u"ࠧࠨẐ").join(bstack11111ll11l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬẑ"): str(bstack11111ll11l1_opy_[0]).lower() + bstack11ll1l1_opy_ (u"ࠢ࠻࠱࠲ࠦẒ") + bstack11ll1l1_opy_ (u"ࠣࠤẓ").join(bstack11111ll11l1_opy_[1:])
                }
        elif bstack11ll1l1_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣẔ") in proxy:
            bstack11111ll11l1_opy_ = proxy.split(bstack11ll1l1_opy_ (u"ࠥࠤࠧẕ"))
            if bstack11ll1l1_opy_ (u"ࠦ࠿࠵࠯ࠣẖ") in bstack11ll1l1_opy_ (u"ࠧࠨẗ").join(bstack11111ll11l1_opy_[1:]):
                proxies = {
                    bstack11ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬẘ"): bstack11ll1l1_opy_ (u"ࠢࠣẙ").join(bstack11111ll11l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧẚ"): bstack11ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥẛ") + bstack11ll1l1_opy_ (u"ࠥࠦẜ").join(bstack11111ll11l1_opy_[1:])
                }
        else:
            proxies = {
                bstack11ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪẝ"): proxy
            }
    except Exception as e:
        print(bstack11ll1l1_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤẞ"), bstack111l1llll1l_opy_.format(bstack11111ll111l_opy_, str(e)))
    bstack11111ll1111_opy_ = proxies
    return proxies