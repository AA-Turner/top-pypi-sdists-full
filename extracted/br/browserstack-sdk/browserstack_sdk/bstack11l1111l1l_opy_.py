# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l111l1l_opy_():
  def __init__(self, args, logger, bstack1111l1111l_opy_, bstack1111ll1111_opy_, bstack11111l111l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l1111l_opy_ = bstack1111l1111l_opy_
    self.bstack1111ll1111_opy_ = bstack1111ll1111_opy_
    self.bstack11111l111l_opy_ = bstack11111l111l_opy_
  def bstack1lllllll11_opy_(self, bstack11111lll11_opy_, bstack11l11111l_opy_, bstack11111l1111_opy_=False):
    bstack11l1111l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1l11l_opy_ = manager.list()
    bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
    if bstack11111l1111_opy_:
      for index, platform in enumerate(self.bstack1111l1111l_opy_[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧႁ")]):
        if index == 0:
          bstack11l11111l_opy_[bstackl_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨႂ")] = self.args
        bstack11l1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111lll11_opy_,
                                                    args=(bstack11l11111l_opy_, bstack1111l1l11l_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l1111l_opy_[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႃ")]):
        bstack11l1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111lll11_opy_,
                                                    args=(bstack11l11111l_opy_, bstack1111l1l11l_opy_)))
    i = 0
    for t in bstack11l1111l_opy_:
      try:
        if bstack1l1llll1l1_opy_.get_property(bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨႄ")):
          os.environ[bstackl_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩႅ")] = json.dumps(self.bstack1111l1111l_opy_[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬႆ")][i % self.bstack11111l111l_opy_])
      except Exception as e:
        self.logger.debug(bstackl_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠥႇ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11l1111l_opy_:
      t.join()
    return list(bstack1111l1l11l_opy_)