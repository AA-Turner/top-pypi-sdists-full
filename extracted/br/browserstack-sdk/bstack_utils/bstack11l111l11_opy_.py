# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
import json
from bstack_utils.bstack11111llll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1l1lll_opy_(object):
  bstack1l1l1l1lll_opy_ = os.path.join(os.path.expanduser(bstack1l11lll_opy_ (u"ࠩࢁࠫᘶ")), bstack1l11lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᘷ"))
  bstack11lll1l1ll1_opy_ = os.path.join(bstack1l1l1l1lll_opy_, bstack1l11lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫᘸ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11lll1111l_opy_ = None
  bstack11l1l1ll1_opy_ = None
  bstack11llll1ll11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l11lll_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧᘹ")):
      cls.instance = super(bstack11lll1l1lll_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1l1l1l_opy_()
    return cls.instance
  def bstack11lll1l1l1l_opy_(self):
    try:
      with open(self.bstack11lll1l1ll1_opy_, bstack1l11lll_opy_ (u"࠭ࡲࠨᘺ")) as bstack1l111l1l_opy_:
        bstack11lll1ll111_opy_ = bstack1l111l1l_opy_.read()
        data = json.loads(bstack11lll1ll111_opy_)
        if bstack1l11lll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᘻ") in data:
          self.bstack11lllll1ll1_opy_(data[bstack1l11lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᘼ")])
        if bstack1l11lll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᘽ") in data:
          self.bstack1l11lll11l_opy_(data[bstack1l11lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᘾ")])
    except:
      pass
  def bstack1l11lll11l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l11lll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᘿ"),bstack1l11lll_opy_ (u"ࠬ࠭ᙀ"))
      self.bstack11lll1111l_opy_ = scripts.get(bstack1l11lll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᙁ"),bstack1l11lll_opy_ (u"ࠧࠨᙂ"))
      self.bstack11l1l1ll1_opy_ = scripts.get(bstack1l11lll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᙃ"),bstack1l11lll_opy_ (u"ࠩࠪᙄ"))
      self.bstack11llll1ll11_opy_ = scripts.get(bstack1l11lll_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᙅ"),bstack1l11lll_opy_ (u"ࠫࠬᙆ"))
  def bstack11lllll1ll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1l1ll1_opy_, bstack1l11lll_opy_ (u"ࠬࡽࠧᙇ")) as file:
        json.dump({
          bstack1l11lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᙈ"): self.commands_to_wrap,
          bstack1l11lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣᙉ"): {
            bstack1l11lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᙊ"): self.perform_scan,
            bstack1l11lll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᙋ"): self.bstack11lll1111l_opy_,
            bstack1l11lll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᙌ"): self.bstack11l1l1ll1_opy_,
            bstack1l11lll_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᙍ"): self.bstack11llll1ll11_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack1l11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥᙎ").format(e))
      pass
  def bstack1llll111l1_opy_(self, bstack1ll11lll11l_opy_):
    try:
      return any(command.get(bstack1l11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙏ")) == bstack1ll11lll11l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11l111l11_opy_ = bstack11lll1l1lll_opy_()