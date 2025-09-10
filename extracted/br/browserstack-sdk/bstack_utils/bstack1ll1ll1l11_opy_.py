# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll1111l11_opy_ import bstack11ll11111l1_opy_
from bstack_utils.constants import bstack11l1l1ll11l_opy_, bstack1ll1l1lll_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack1ll1l111_opy_
from bstack_utils import bstack1lll1llll_opy_
bstack11l11llllll_opy_ = 10
class bstack11llll1lll_opy_:
    def __init__(self, bstack1l1llll1l1_opy_, config, bstack11l1l11l11l_opy_=0):
        self.bstack11l1l11111l_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1l111l11_opy_ = bstack1ll11ll_opy_ (u"ࠨࡻࡾ࠱ࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡦࡢ࡫࡯ࡩࡩ࠳ࡴࡦࡵࡷࡷࠧ᫒").format(bstack11l1l1ll11l_opy_)
        self.bstack11l11lll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣ᫓").format(os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᫔"))))
        self.bstack11l11lll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣ᫕").format(os.environ.get(bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᫖"))))
        self.bstack11l1l111111_opy_ = 2
        self.bstack1l1llll1l1_opy_ = bstack1l1llll1l1_opy_
        self.config = config
        self.logger = bstack1lll1llll_opy_.get_logger(__name__, bstack1ll1l1lll_opy_)
        self.bstack11l1l11l11l_opy_ = bstack11l1l11l11l_opy_
        self.bstack11l1l111ll1_opy_ = False
        self.bstack11l1l11l111_opy_ = not (
                            os.environ.get(bstack1ll11ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥ᫗")) and
                            os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ᫘")) and
                            os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ᫙"))
                        )
        if bstack1ll1l111_opy_.bstack11l11ll1ll1_opy_(config):
            self.bstack11l1l111111_opy_ = bstack1ll1l111_opy_.bstack11l1l11l1ll_opy_(config, self.bstack11l1l11l11l_opy_)
            self.bstack11l11llll1l_opy_()
    def bstack11l1l1111ll_opy_(self):
        return bstack1ll11ll_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨ᫚").format(self.config.get(bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ᫛")), os.environ.get(bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ᫜")))
    def bstack11l11lll1ll_opy_(self):
        try:
            if self.bstack11l1l11l111_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l11lll1l1_opy_, bstack1ll11ll_opy_ (u"ࠥࡶࠧ᫝")) as f:
                        bstack11l11lllll1_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l11lllll1_opy_ = set()
                bstack11l1l111l1l_opy_ = bstack11l11lllll1_opy_ - self.bstack11l1l11111l_opy_
                if not bstack11l1l111l1l_opy_:
                    return
                self.bstack11l1l11111l_opy_.update(bstack11l1l111l1l_opy_)
                data = {bstack1ll11ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤ᫞"): list(self.bstack11l1l11111l_opy_), bstack1ll11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣ᫟"): self.config.get(bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᫠")), bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧ᫡"): os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ᫢")), bstack1ll11ll_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢ᫣"): self.config.get(bstack1ll11ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ᫤"))}
            response = bstack11ll11111l1_opy_.bstack11l1l11l1l1_opy_(self.bstack11l1l111l11_opy_, data)
            if response.get(bstack1ll11ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᫥")) == 200:
                self.logger.debug(bstack1ll11ll_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧ᫦").format(data))
            else:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥ᫧").format(response))
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢ᫨").format(e))
    def bstack11l1l111lll_opy_(self):
        if self.bstack11l1l11l111_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l11lll1l1_opy_, bstack1ll11ll_opy_ (u"ࠣࡴࠥ᫩")) as f:
                        bstack11l11ll1lll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l11ll1lll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧ᫪").format(failed_count))
                if failed_count >= self.bstack11l1l111111_opy_:
                    self.logger.info(bstack1ll11ll_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦ᫫").format(failed_count, self.bstack11l1l111111_opy_))
                    self.bstack11l1l1111l1_opy_(failed_count)
                    self.bstack11l1l111ll1_opy_ = True
            return
        try:
            response = bstack11ll11111l1_opy_.bstack11l1l111lll_opy_(bstack1ll11ll_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣ᫬").format(self.bstack11l1l111l11_opy_, self.config.get(bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᫭")), os.environ.get(bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ᫮")), self.config.get(bstack1ll11ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᫯"))))
            if response.get(bstack1ll11ll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᫰")) == 200:
                failed_count = response.get(bstack1ll11ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧ᫱"), 0)
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧ᫲").format(failed_count))
                if failed_count >= self.bstack11l1l111111_opy_:
                    self.logger.info(bstack1ll11ll_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦ᫳").format(failed_count, self.bstack11l1l111111_opy_))
                    self.bstack11l1l1111l1_opy_(failed_count)
                    self.bstack11l1l111ll1_opy_ = True
            else:
                self.logger.error(bstack1ll11ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ᫴").format(response))
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢ᫵").format(e))
    def bstack11l1l1111l1_opy_(self, failed_count):
        with open(self.bstack11l11lll11l_opy_, bstack1ll11ll_opy_ (u"ࠢࡸࠤ᫶")) as f:
            f.write(bstack1ll11ll_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨ᫷").format(datetime.now()))
            f.write(bstack1ll11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨ᫸").format(failed_count))
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦ᫹").format(self.bstack11l11lll11l_opy_))
    def bstack11l11llll1l_opy_(self):
        def bstack11l11llll11_opy_():
            while not self.bstack11l1l111ll1_opy_:
                time.sleep(bstack11l11llllll_opy_)
                self.bstack11l11lll1ll_opy_()
                self.bstack11l1l111lll_opy_()
        bstack11l11lll111_opy_ = threading.Thread(target=bstack11l11llll11_opy_, daemon=True)
        bstack11l11lll111_opy_.start()