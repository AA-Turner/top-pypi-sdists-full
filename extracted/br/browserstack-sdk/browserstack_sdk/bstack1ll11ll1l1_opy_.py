# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11lll1ll_opy_():
  def __init__(self, args, logger, bstack1llll111111_opy_, bstack1llll11ll1l_opy_, bstack1lll1l1l1ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1llll111111_opy_ = bstack1llll111111_opy_
    self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
    self.bstack1lll1l1l1ll_opy_ = bstack1lll1l1l1ll_opy_
  def bstack1l1111111_opy_(self, bstack1llll1l11l1_opy_, bstack11ll1lll1_opy_, bstack1lll1l1l1l1_opy_=False):
    bstack11l1ll1111_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lll1lllll1_opy_ = manager.list()
    bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
    if bstack1lll1l1l1l1_opy_:
      for index, platform in enumerate(self.bstack1llll111111_opy_[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᅽ")]):
        if index == 0:
          bstack11ll1lll1_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᅾ")] = self.args
        bstack11l1ll1111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll1l11l1_opy_,
                                                    args=(bstack11ll1lll1_opy_, bstack1lll1lllll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1llll111111_opy_[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᅿ")]):
        bstack11l1ll1111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll1l11l1_opy_,
                                                    args=(bstack11ll1lll1_opy_, bstack1lll1lllll1_opy_)))
    i = 0
    for t in bstack11l1ll1111_opy_:
      try:
        if bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᆀ")):
          os.environ[bstack11l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩᆁ")] = json.dumps(self.bstack1llll111111_opy_[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᆂ")][i % self.bstack1lll1l1l1ll_opy_])
      except Exception as e:
        self.logger.debug(bstack11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠥᆃ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11l1ll1111_opy_:
      t.join()
    return list(bstack1lll1lllll1_opy_)