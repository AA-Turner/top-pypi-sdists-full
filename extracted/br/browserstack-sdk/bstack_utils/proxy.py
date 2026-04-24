# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll1l111l1l_opy_
from bstack_utils import logger_utils
global_config = Config.bstack1lllll1lll1_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1ll1l11l111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1l11l11ll_opy_(bstack1ll1l11l1l1l_opy_, bstack1ll1l11l11l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1l11l1l1l_opy_):
        with open(bstack1ll1l11l1l1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1l11l111l_opy_(bstack1ll1l11l1l1l_opy_):
        pac = get_pac(url=bstack1ll1l11l1l1l_opy_)
    else:
        raise Exception(bstack111ll11_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬ☿").format(bstack1ll1l11l1l1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111ll11_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢ♀"), 80))
        bstack1ll1l11l1111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1l11l1111_opy_ = bstack111ll11_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨ♁")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l11l11l1_opy_, bstack1ll1l11l1111_opy_)
    return proxy_url
def bstack1llllll1ll1_opy_(config):
    return bstack111ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ♂") in config or bstack111ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭♃") in config
def bstack1ll11111l_opy_(config):
    if not bstack1llllll1ll1_opy_(config):
        return
    if config.get(bstack111ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭♄")):
        return config.get(bstack111ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ♅"))
    if config.get(bstack111ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ♆")):
        return config.get(bstack111ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ♇"))
def bstack11l1ll1l_opy_(config, bstack1ll1l11l11l1_opy_):
    proxy = bstack1ll11111l_opy_(config)
    proxies = {}
    if config.get(bstack111ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ♈")) or config.get(bstack111ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ♉")):
        if proxy.endswith(bstack111ll11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ♊")):
            proxies = bstack11l1111l1_opy_(proxy, bstack1ll1l11l11l1_opy_)
        else:
            proxies = {
                bstack111ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ♋"): proxy
            }
    global_config.bstack1l111l1ll1_opy_(bstack111ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ♌"), proxies)
    return proxies
def bstack11l1111l1_opy_(bstack1ll1l11l1l1l_opy_, bstack1ll1l11l11l1_opy_):
    proxies = {}
    global bstack1ll1l11l1l11_opy_
    if bstack111ll11_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨ♍") in globals():
        return bstack1ll1l11l1l11_opy_
    try:
        proxy = bstack1ll1l11l11ll_opy_(bstack1ll1l11l1l1l_opy_, bstack1ll1l11l11l1_opy_)
        if bstack111ll11_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨ♎") in proxy:
            proxies = {}
        elif bstack111ll11_opy_ (u"ࠢࡉࡖࡗࡔࠧ♏") in proxy or bstack111ll11_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢ♐") in proxy or bstack111ll11_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣ♑") in proxy:
            bstack1ll1l11l1ll1_opy_ = proxy.split(bstack111ll11_opy_ (u"ࠥࠤࠧ♒"))
            if bstack111ll11_opy_ (u"ࠦ࠿࠵࠯ࠣ♓") in bstack111ll11_opy_ (u"ࠧࠨ♔").join(bstack1ll1l11l1ll1_opy_[1:]):
                proxies = {
                    bstack111ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ♕"): bstack111ll11_opy_ (u"ࠢࠣ♖").join(bstack1ll1l11l1ll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ♗"): str(bstack1ll1l11l1ll1_opy_[0]).lower() + bstack111ll11_opy_ (u"ࠤ࠽࠳࠴ࠨ♘") + bstack111ll11_opy_ (u"ࠥࠦ♙").join(bstack1ll1l11l1ll1_opy_[1:])
                }
        elif bstack111ll11_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥ♚") in proxy:
            bstack1ll1l11l1ll1_opy_ = proxy.split(bstack111ll11_opy_ (u"ࠧࠦࠢ♛"))
            if bstack111ll11_opy_ (u"ࠨ࠺࠰࠱ࠥ♜") in bstack111ll11_opy_ (u"ࠢࠣ♝").join(bstack1ll1l11l1ll1_opy_[1:]):
                proxies = {
                    bstack111ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ♞"): bstack111ll11_opy_ (u"ࠤࠥ♟").join(bstack1ll1l11l1ll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ♠"): bstack111ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ♡") + bstack111ll11_opy_ (u"ࠧࠨ♢").join(bstack1ll1l11l1ll1_opy_[1:])
                }
        else:
            proxies = {
                bstack111ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ♣"): proxy
            }
    except Exception as e:
        print(bstack111ll11_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ♤"), bstack1lll1l111l1l_opy_.format(bstack1ll1l11l1l1l_opy_, str(e)))
    bstack1ll1l11l1l11_opy_ = proxies
    return proxies