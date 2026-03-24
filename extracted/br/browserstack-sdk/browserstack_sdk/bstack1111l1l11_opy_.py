# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1lllll1ll1_opy_():
  def __init__(self, args, logger, bstack1lll11111l1_opy_, bstack1lll111l1l1_opy_, bstack1ll1lllll1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lll11111l1_opy_ = bstack1lll11111l1_opy_
    self.bstack1lll111l1l1_opy_ = bstack1lll111l1l1_opy_
    self.bstack1ll1lllll1l_opy_ = bstack1ll1lllll1l_opy_
  def bstack1111ll1ll_opy_(self, bstack1lll11llll1_opy_, bstack1l1ll111l_opy_, bstack1ll1llllll1_opy_=False):
    bstack1111111lll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lll1111111_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1ll1llllll1_opy_:
      for index, platform in enumerate(self.bstack1lll11111l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬቔ")]):
        if index == 0:
          bstack1l1ll111l_opy_[bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ቕ")] = self.args
        bstack1111111lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll11llll1_opy_,
                                                    args=(bstack1l1ll111l_opy_, bstack1lll1111111_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lll11111l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧቖ")]):
        bstack1111111lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll11llll1_opy_,
                                                    args=(bstack1l1ll111l_opy_, bstack1lll1111111_opy_)))
    i = 0
    for t in bstack1111111lll_opy_:
      try:
        if global_config.get_property(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭቗")):
          os.environ[bstack1ll1lll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧቘ")] = json.dumps(self.bstack1lll11111l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ቙")][i % self.bstack1ll1lllll1l_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠣቚ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1111111lll_opy_:
      t.join()
    return list(bstack1lll1111111_opy_)