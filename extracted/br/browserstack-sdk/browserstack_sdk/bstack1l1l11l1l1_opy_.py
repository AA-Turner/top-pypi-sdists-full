# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11l1111l11_opy_():
  def __init__(self, args, logger, bstack1111l11l11_opy_, bstack11111ll111_opy_, bstack11111l11ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l11l11_opy_ = bstack1111l11l11_opy_
    self.bstack11111ll111_opy_ = bstack11111ll111_opy_
    self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
  def bstack1l11l111ll_opy_(self, bstack11111ll1l1_opy_, bstack11111l11_opy_, bstack11111l1l11_opy_=False):
    bstack111l11lll_opy_ = []
    manager = multiprocessing.Manager()
    bstack11111llll1_opy_ = manager.list()
    bstack1llll11l_opy_ = Config.bstack1l11llllll_opy_()
    if bstack11111l1l11_opy_:
      for index, platform in enumerate(self.bstack1111l11l11_opy_[bstack1ll1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧႁ")]):
        if index == 0:
          bstack11111l11_opy_[bstack1ll1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨႂ")] = self.args
        bstack111l11lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111ll1l1_opy_,
                                                    args=(bstack11111l11_opy_, bstack11111llll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l11l11_opy_[bstack1ll1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႃ")]):
        bstack111l11lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111ll1l1_opy_,
                                                    args=(bstack11111l11_opy_, bstack11111llll1_opy_)))
    i = 0
    for t in bstack111l11lll_opy_:
      try:
        if bstack1llll11l_opy_.get_property(bstack1ll1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨႄ")):
          os.environ[bstack1ll1ll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩႅ")] = json.dumps(self.bstack1111l11l11_opy_[bstack1ll1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬႆ")][i % self.bstack11111l11ll_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠥႇ").format(str(e)))
      i += 1
      t.start()
    for t in bstack111l11lll_opy_:
      t.join()
    return list(bstack11111llll1_opy_)