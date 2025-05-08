# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll1111l1_opy_():
  def __init__(self, args, logger, bstack1111ll1ll1_opy_, bstack1111llll1l_opy_, bstack1111ll11ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
    self.bstack1111llll1l_opy_ = bstack1111llll1l_opy_
    self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
  def bstack1ll11lll11_opy_(self, bstack111l1111l1_opy_, bstack11ll1l111_opy_, bstack1111ll11l1_opy_=False):
    bstack11ll1ll1ll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111ll1l11_opy_ = manager.list()
    bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
    if bstack1111ll11l1_opy_:
      for index, platform in enumerate(self.bstack1111ll1ll1_opy_[bstack1l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဋ")]):
        if index == 0:
          bstack11ll1l111_opy_[bstack1l1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩဌ")] = self.args
        bstack11ll1ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111l1_opy_,
                                                    args=(bstack11ll1l111_opy_, bstack1111ll1l11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111ll1ll1_opy_[bstack1l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဍ")]):
        bstack11ll1ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111l1_opy_,
                                                    args=(bstack11ll1l111_opy_, bstack1111ll1l11_opy_)))
    i = 0
    for t in bstack11ll1ll1ll_opy_:
      try:
        if bstack11l1l1l1l_opy_.get_property(bstack1l1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩဎ")):
          os.environ[bstack1l1lll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪဏ")] = json.dumps(self.bstack1111ll1ll1_opy_[bstack1l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭တ")][i % self.bstack1111ll11ll_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠦထ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll1ll1ll_opy_:
      t.join()
    return list(bstack1111ll1l11_opy_)