# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l11ll1l11_opy_():
  def __init__(self, args, logger, bstack1lll11l111l_opy_, bstack1lll111l111_opy_, bstack1ll1llllll1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lll11l111l_opy_ = bstack1lll11l111l_opy_
    self.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
    self.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
  def bstack1l1ll111l_opy_(self, bstack1lll11111ll_opy_, bstack1llll1l11_opy_, bstack1ll1lllll1l_opy_=False):
    bstack1ll1l111ll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lll111ll11_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1ll1lllll1l_opy_:
      for index, platform in enumerate(self.bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬቔ")]):
        if index == 0:
          bstack1llll1l11_opy_[bstack11lll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ቕ")] = self.args
        bstack1ll1l111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll11111ll_opy_,
                                                    args=(bstack1llll1l11_opy_, bstack1lll111ll11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧቖ")]):
        bstack1ll1l111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll11111ll_opy_,
                                                    args=(bstack1llll1l11_opy_, bstack1lll111ll11_opy_)))
    i = 0
    for t in bstack1ll1l111ll_opy_:
      try:
        if global_config.get_property(bstack11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭቗")):
          os.environ[bstack11lll1_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧቘ")] = json.dumps(self.bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ቙")][i % self.bstack1ll1llllll1_opy_])
      except Exception as e:
        self.logger.debug(bstack11lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠣቚ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll1l111ll_opy_:
      t.join()
    return list(bstack1lll111ll11_opy_)