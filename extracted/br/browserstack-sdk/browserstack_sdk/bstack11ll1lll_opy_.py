# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11l11l11ll_opy_():
  def __init__(self, args, logger, bstack1llll1l1l1l_opy_, bstack1llll1ll11l_opy_, bstack1lll1ll1l11_opy_):
    self.args = args
    self.logger = logger
    self.bstack1llll1l1l1l_opy_ = bstack1llll1l1l1l_opy_
    self.bstack1llll1ll11l_opy_ = bstack1llll1ll11l_opy_
    self.bstack1lll1ll1l11_opy_ = bstack1lll1ll1l11_opy_
  def bstack111ll11lll_opy_(self, bstack1llll11l11l_opy_, bstack11ll1l1lll_opy_, bstack1lll1ll11ll_opy_=False):
    bstack111ll1111l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1llll11ll11_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1lll1ll11ll_opy_:
      for index, platform in enumerate(self.bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᆊ")]):
        if index == 0:
          bstack11ll1l1lll_opy_[bstack1lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᆋ")] = self.args
        bstack111ll1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll11l11l_opy_,
                                                    args=(bstack11ll1l1lll_opy_, bstack1llll11ll11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᆌ")]):
        bstack111ll1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll11l11l_opy_,
                                                    args=(bstack11ll1l1lll_opy_, bstack1llll11ll11_opy_)))
    i = 0
    for t in bstack111ll1111l_opy_:
      try:
        if global_config.get_property(bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᆍ")):
          os.environ[bstack1lll1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᆎ")] = json.dumps(self.bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᆏ")][i % self.bstack1lll1ll1l11_opy_])
      except Exception as e:
        self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᆐ").format(str(e)))
      i += 1
      t.start()
    for t in bstack111ll1111l_opy_:
      t.join()
    return list(bstack1llll11ll11_opy_)