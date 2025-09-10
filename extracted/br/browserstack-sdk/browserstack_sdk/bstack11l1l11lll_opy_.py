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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll1l1l11_opy_():
  def __init__(self, args, logger, bstack11111l11ll_opy_, bstack1111l111l1_opy_, bstack111111ll11_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
    self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
    self.bstack111111ll11_opy_ = bstack111111ll11_opy_
  def bstack1l111ll1l1_opy_(self, bstack1111l11ll1_opy_, bstack11lll111ll_opy_, bstack111111l1ll_opy_=False):
    bstack1l111111_opy_ = []
    manager = multiprocessing.Manager()
    bstack11111l1l1l_opy_ = manager.list()
    bstack1l111111l1_opy_ = Config.bstack11l11lllll_opy_()
    if bstack111111l1ll_opy_:
      for index, platform in enumerate(self.bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪႋ")]):
        if index == 0:
          bstack11lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫႌ")] = self.args
        bstack1l111111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11ll1_opy_,
                                                    args=(bstack11lll111ll_opy_, bstack11111l1l1l_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷႍࠬ")]):
        bstack1l111111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11ll1_opy_,
                                                    args=(bstack11lll111ll_opy_, bstack11111l1l1l_opy_)))
    i = 0
    for t in bstack1l111111_opy_:
      try:
        if bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫႎ")):
          os.environ[bstack1ll11ll_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬႏ")] = json.dumps(self.bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ႐")][i % self.bstack111111ll11_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴ࠼ࠣࡿࢂࠨ႑").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l111111_opy_:
      t.join()
    return list(bstack11111l1l1l_opy_)