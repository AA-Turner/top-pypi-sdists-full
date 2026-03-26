# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack111lll1ll1_opy_():
  def __init__(self, args, logger, bstack1lllllll11l_opy_, bstack1llllll1l11_opy_, bstack1ll1lll1l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
    self.bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_
    self.bstack1ll1lll1l1l_opy_ = bstack1ll1lll1l1l_opy_
  def bstack11l111ll11_opy_(self, bstack1lll11111l1_opy_, bstack11lllllll_opy_, bstack1ll1lll1ll1_opy_=False):
    bstack11111lllll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lll111ll11_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1ll1lll1ll1_opy_:
      for index, platform in enumerate(self.bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨቬ")]):
        if index == 0:
          bstack11lllllll_opy_[bstack1ll1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩቭ")] = self.args
        bstack11111lllll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll11111l1_opy_,
                                                    args=(bstack11lllllll_opy_, bstack1lll111ll11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪቮ")]):
        bstack11111lllll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll11111l1_opy_,
                                                    args=(bstack11lllllll_opy_, bstack1lll111ll11_opy_)))
    i = 0
    for t in bstack11111lllll_opy_:
      try:
        if global_config.get_property(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩቯ")):
          os.environ[bstack1ll1lll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪተ")] = json.dumps(self.bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ቱ")][i % self.bstack1ll1lll1l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠦቲ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11111lllll_opy_:
      t.join()
    return list(bstack1lll111ll11_opy_)