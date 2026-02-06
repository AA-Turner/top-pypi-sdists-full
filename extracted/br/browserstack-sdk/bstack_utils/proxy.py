# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11111lll11l_opy_
from bstack_utils import logger_utils
bstack1l111111_opy_ = Config.bstack1llll1l111_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1ll1l1l1_opy_())
def bstack1llll111llll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llll11l1111_opy_(bstack1llll111l1ll_opy_, bstack1llll111lll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llll111l1ll_opy_):
        with open(bstack1llll111l1ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1llll111llll_opy_(bstack1llll111l1ll_opy_):
        pac = get_pac(url=bstack1llll111l1ll_opy_)
    else:
        raise Exception(bstack11lllll_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬ⃱").format(bstack1llll111l1ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11lllll_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢ⃲"), 80))
        bstack1llll111ll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llll111ll11_opy_ = bstack11lllll_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨ⃳")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llll111lll1_opy_, bstack1llll111ll11_opy_)
    return proxy_url
def bstack1ll11l111l_opy_(config):
    return bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⃴") in config or bstack11lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⃵") in config
def bstack1l1l1l1ll1_opy_(config):
    if not bstack1ll11l111l_opy_(config):
        return
    if config.get(bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⃶")):
        return config.get(bstack11lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⃷"))
    if config.get(bstack11lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⃸")):
        return config.get(bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⃹"))
def bstack11l1l1111_opy_(config, bstack1llll111lll1_opy_):
    proxy = bstack1l1l1l1ll1_opy_(config)
    proxies = {}
    if config.get(bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⃺")) or config.get(bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⃻")):
        if proxy.endswith(bstack11lllll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ⃼")):
            proxies = bstack1l11lll11_opy_(proxy, bstack1llll111lll1_opy_)
        else:
            proxies = {
                bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ⃽"): proxy
            }
    bstack1l111111_opy_.bstack1llll1ll1l_opy_(bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ⃾"), proxies)
    return proxies
def bstack1l11lll11_opy_(bstack1llll111l1ll_opy_, bstack1llll111lll1_opy_):
    proxies = {}
    global bstack1llll111ll1l_opy_
    if bstack11lllll_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨ⃿") in globals():
        return bstack1llll111ll1l_opy_
    try:
        proxy = bstack1llll11l1111_opy_(bstack1llll111l1ll_opy_, bstack1llll111lll1_opy_)
        if bstack11lllll_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨ℀") in proxy:
            proxies = {}
        elif bstack11lllll_opy_ (u"ࠢࡉࡖࡗࡔࠧ℁") in proxy or bstack11lllll_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢℂ") in proxy or bstack11lllll_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣ℃") in proxy:
            bstack1llll111l1l1_opy_ = proxy.split(bstack11lllll_opy_ (u"ࠥࠤࠧ℄"))
            if bstack11lllll_opy_ (u"ࠦ࠿࠵࠯ࠣ℅") in bstack11lllll_opy_ (u"ࠧࠨ℆").join(bstack1llll111l1l1_opy_[1:]):
                proxies = {
                    bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬℇ"): bstack11lllll_opy_ (u"ࠢࠣ℈").join(bstack1llll111l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ℉"): str(bstack1llll111l1l1_opy_[0]).lower() + bstack11lllll_opy_ (u"ࠤ࠽࠳࠴ࠨℊ") + bstack11lllll_opy_ (u"ࠥࠦℋ").join(bstack1llll111l1l1_opy_[1:])
                }
        elif bstack11lllll_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥℌ") in proxy:
            bstack1llll111l1l1_opy_ = proxy.split(bstack11lllll_opy_ (u"ࠧࠦࠢℍ"))
            if bstack11lllll_opy_ (u"ࠨ࠺࠰࠱ࠥℎ") in bstack11lllll_opy_ (u"ࠢࠣℏ").join(bstack1llll111l1l1_opy_[1:]):
                proxies = {
                    bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧℐ"): bstack11lllll_opy_ (u"ࠤࠥℑ").join(bstack1llll111l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩℒ"): bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧℓ") + bstack11lllll_opy_ (u"ࠧࠨ℔").join(bstack1llll111l1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack11lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬℕ"): proxy
            }
    except Exception as e:
        print(bstack11lllll_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ№"), bstack11111lll11l_opy_.format(bstack1llll111l1ll_opy_, str(e)))
    bstack1llll111ll1l_opy_ = proxies
    return proxies