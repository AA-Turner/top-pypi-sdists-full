# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111l1llllll_opy_ import bstack111l1lllll1_opy_
from bstack_utils.constants import bstack111l111l111_opy_, bstack1l1l1l1ll1_opy_
from bstack_utils.bstack1l11llll1l_opy_ import bstack1ll1lll1l_opy_
from bstack_utils import logger_utils
bstack1111ll1llll_opy_ = 10
class bstack1l1111l111_opy_:
    def __init__(self, bstack1111lllll_opy_, config, bstack1111lll11ll_opy_=0):
        self.bstack111l1111111_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1111lll111l_opy_ = bstack1l1_opy_ (u"ࠨࡻࡾ࠱ࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡦࡢ࡫࡯ࡩࡩ࠳ࡴࡦࡵࡷࡷࠧἹ").format(bstack111l111l111_opy_)
        self.bstack1111llllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣἺ").format(os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ἳ"))))
        self.bstack111l11111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣἼ").format(os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨἽ"))))
        self.bstack1111lll1111_opy_ = 2
        self.bstack1111lllll_opy_ = bstack1111lllll_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1l1l1l1ll1_opy_)
        self.bstack1111lll11ll_opy_ = bstack1111lll11ll_opy_
        self.bstack111l111111l_opy_ = False
        self.bstack1111llll11l_opy_ = not (
                            os.environ.get(bstack1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥἾ")) and
                            os.environ.get(bstack1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣἿ")) and
                            os.environ.get(bstack1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣὀ"))
                        )
        if bstack1ll1lll1l_opy_.bstack1111lll1l1l_opy_(config):
            self.bstack1111lll1111_opy_ = bstack1ll1lll1l_opy_.bstack1111ll1lll1_opy_(config, self.bstack1111lll11ll_opy_)
            self.bstack1111ll1ll1l_opy_()
    def bstack1111llll1ll_opy_(self):
        return bstack1l1_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨὁ").format(self.config.get(bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫὂ")), os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨὃ")))
    def bstack1111lll1l11_opy_(self):
        try:
            if self.bstack1111llll11l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111l11111l1_opy_, bstack1l1_opy_ (u"ࠥࡶࠧὄ")) as f:
                        bstack1111lllllll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1111lllllll_opy_ = set()
                bstack1111llll111_opy_ = bstack1111lllllll_opy_ - self.bstack111l1111111_opy_
                if not bstack1111llll111_opy_:
                    return
                self.bstack111l1111111_opy_.update(bstack1111llll111_opy_)
                data = {bstack1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤὅ"): list(self.bstack111l1111111_opy_), bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ὆"): self.config.get(bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ὇")), bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧὈ"): os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧὉ")), bstack1l1_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢὊ"): self.config.get(bstack1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨὋ"))}
            response = bstack111l1lllll1_opy_.bstack1111lll11l1_opy_(self.bstack1111lll111l_opy_, data)
            if response.get(bstack1l1_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦὌ")) == 200:
                self.logger.debug(bstack1l1_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧὍ").format(data))
            else:
                self.logger.debug(bstack1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥ὎").format(response))
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢ὏").format(e))
    def bstack1111lllll11_opy_(self):
        if self.bstack1111llll11l_opy_:
            with self.lock:
                try:
                    with open(self.bstack111l11111l1_opy_, bstack1l1_opy_ (u"ࠣࡴࠥὐ")) as f:
                        bstack1111llll1l1_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1111llll1l1_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l1_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧὑ").format(failed_count))
                if failed_count >= self.bstack1111lll1111_opy_:
                    self.logger.info(bstack1l1_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦὒ").format(failed_count, self.bstack1111lll1111_opy_))
                    self.bstack1111lllll1l_opy_(failed_count)
                    self.bstack111l111111l_opy_ = True
            return
        try:
            response = bstack111l1lllll1_opy_.bstack1111lllll11_opy_(bstack1l1_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣὓ").format(self.bstack1111lll111l_opy_, self.config.get(bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨὔ")), os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬὕ")), self.config.get(bstack1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬὖ"))))
            if response.get(bstack1l1_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣὗ")) == 200:
                failed_count = response.get(bstack1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧ὘"), 0)
                self.logger.debug(bstack1l1_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧὙ").format(failed_count))
                if failed_count >= self.bstack1111lll1111_opy_:
                    self.logger.info(bstack1l1_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦ὚").format(failed_count, self.bstack1111lll1111_opy_))
                    self.bstack1111lllll1l_opy_(failed_count)
                    self.bstack111l111111l_opy_ = True
            else:
                self.logger.error(bstack1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤὛ").format(response))
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢ὜").format(e))
    def bstack1111lllll1l_opy_(self, failed_count):
        with open(self.bstack1111llllll1_opy_, bstack1l1_opy_ (u"ࠢࡸࠤὝ")) as f:
            f.write(bstack1l1_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨ὞").format(datetime.now()))
            f.write(bstack1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨὟ").format(failed_count))
        self.logger.debug(bstack1l1_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦὠ").format(self.bstack1111llllll1_opy_))
    def bstack1111ll1ll1l_opy_(self):
        def bstack1111lll1ll1_opy_():
            while not self.bstack111l111111l_opy_:
                time.sleep(bstack1111ll1llll_opy_)
                self.bstack1111lll1l11_opy_()
                self.bstack1111lllll11_opy_()
        bstack1111lll1lll_opy_ = threading.Thread(target=bstack1111lll1ll1_opy_, daemon=True)
        bstack1111lll1lll_opy_.start()