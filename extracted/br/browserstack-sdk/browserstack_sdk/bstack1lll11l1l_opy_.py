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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1lll11ll11_opy_():
  def __init__(self, args, logger, bstack1lllll111l1_opy_, bstack1llll1ll1ll_opy_, bstack1ll111ll11l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
    self.bstack1llll1ll1ll_opy_ = bstack1llll1ll1ll_opy_
    self.bstack1ll111ll11l_opy_ = bstack1ll111ll11l_opy_
  def bstack11l1l1111l_opy_(self, bstack1ll11l11ll1_opy_, bstack1111lll1l1_opy_, bstack1ll111ll111_opy_=False):
    bstack1lllll1111_opy_ = multiprocessing.get_context(bstack111ll11_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨᎫ"))
    bstack11ll1lll_opy_ = []
    manager = bstack1lllll1111_opy_.Manager()
    bstack1ll111ll1ll_opy_ = manager.list()
    global_config = Config.bstack1lllll1lll1_opy_()
    if bstack1ll111ll111_opy_:
      for index, platform in enumerate(self.bstack1lllll111l1_opy_[bstack111ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ꭼ")]):
        if index == 0:
          bstack1111lll1l1_opy_[bstack111ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᎭ")] = self.args
        bstack11ll1lll_opy_.append(bstack1lllll1111_opy_.Process(name=str(index),
                                          target=bstack1ll11l11ll1_opy_,
                                          args=(bstack1111lll1l1_opy_, bstack1ll111ll1ll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllll111l1_opy_[bstack111ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎮ")]):
        bstack11ll1lll_opy_.append(bstack1lllll1111_opy_.Process(name=str(index),
                                          target=bstack1ll11l11ll1_opy_,
                                          args=(bstack1111lll1l1_opy_, bstack1ll111ll1ll_opy_)))
    i = 0
    for t in bstack11ll1lll_opy_:
      try:
        if global_config.get_property(bstack111ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᎯ")):
          os.environ[bstack111ll11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᎰ")] = json.dumps(self.bstack1lllll111l1_opy_[bstack111ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᎱ")][i % self.bstack1ll111ll11l_opy_])
      except Exception as e:
        self.logger.debug(bstack111ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᎲ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll1lll_opy_:
      t.join()
    return list(bstack1ll111ll1ll_opy_)