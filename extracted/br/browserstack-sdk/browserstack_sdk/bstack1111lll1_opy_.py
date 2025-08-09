# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll1lllll_opy_():
  def __init__(self, args, logger, bstack11111ll1l1_opy_, bstack1111ll1111_opy_, bstack11111l11ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111ll1l1_opy_ = bstack11111ll1l1_opy_
    self.bstack1111ll1111_opy_ = bstack1111ll1111_opy_
    self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
  def bstack1lllll1ll_opy_(self, bstack11111lll11_opy_, bstack1l1l1111ll_opy_, bstack11111l1l11_opy_=False):
    bstack11ll111l11_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1l111_opy_ = manager.list()
    bstack1l1llll1l_opy_ = Config.bstack1l1lll11l_opy_()
    if bstack11111l1l11_opy_:
      for index, platform in enumerate(self.bstack11111ll1l1_opy_[bstack11l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧႁ")]):
        if index == 0:
          bstack1l1l1111ll_opy_[bstack11l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨႂ")] = self.args
        bstack11ll111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111lll11_opy_,
                                                    args=(bstack1l1l1111ll_opy_, bstack1111l1l111_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111ll1l1_opy_[bstack11l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႃ")]):
        bstack11ll111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111lll11_opy_,
                                                    args=(bstack1l1l1111ll_opy_, bstack1111l1l111_opy_)))
    i = 0
    for t in bstack11ll111l11_opy_:
      try:
        if bstack1l1llll1l_opy_.get_property(bstack11l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨႄ")):
          os.environ[bstack11l1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩႅ")] = json.dumps(self.bstack11111ll1l1_opy_[bstack11l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬႆ")][i % self.bstack11111l11ll_opy_])
      except Exception as e:
        self.logger.debug(bstack11l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠥႇ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll111l11_opy_:
      t.join()
    return list(bstack1111l1l111_opy_)