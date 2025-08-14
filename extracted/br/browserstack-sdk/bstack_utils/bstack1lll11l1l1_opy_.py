# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
import json
from bstack_utils.bstack1l1l11lll1_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11ll1l1_opy_(object):
  bstack1lll11llll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"࠭ࡾࠨᝋ")), bstack1l1l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᝌ"))
  bstack11ll11lll11_opy_ = os.path.join(bstack1lll11llll_opy_, bstack1l1l1ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᝍ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11l1l1l11l_opy_ = None
  bstack111111ll_opy_ = None
  bstack11ll1l11l11_opy_ = None
  bstack11ll1l11111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1l1ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᝎ")):
      cls.instance = super(bstack11ll11ll1l1_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11lll1l_opy_()
    return cls.instance
  def bstack11ll11lll1l_opy_(self):
    try:
      with open(self.bstack11ll11lll11_opy_, bstack1l1l1ll_opy_ (u"ࠪࡶࠬᝏ")) as bstack11l111l111_opy_:
        bstack11ll11ll11l_opy_ = bstack11l111l111_opy_.read()
        data = json.loads(bstack11ll11ll11l_opy_)
        if bstack1l1l1ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᝐ") in data:
          self.bstack11ll1l11l1l_opy_(data[bstack1l1l1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᝑ")])
        if bstack1l1l1ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᝒ") in data:
          self.bstack1l111l1111_opy_(data[bstack1l1l1ll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᝓ")])
        if bstack1l1l1ll_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᝔") in data:
          self.bstack11ll11ll1ll_opy_(data[bstack1l1l1ll_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᝕")])
    except:
      pass
  def bstack11ll11ll1ll_opy_(self, bstack11ll1l11111_opy_):
    if bstack11ll1l11111_opy_ != None:
      self.bstack11ll1l11111_opy_ = bstack11ll1l11111_opy_
  def bstack1l111l1111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1l1ll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ᝖"),bstack1l1l1ll_opy_ (u"ࠫࠬ᝗"))
      self.bstack11l1l1l11l_opy_ = scripts.get(bstack1l1l1ll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩ᝘"),bstack1l1l1ll_opy_ (u"࠭ࠧ᝙"))
      self.bstack111111ll_opy_ = scripts.get(bstack1l1l1ll_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫ᝚"),bstack1l1l1ll_opy_ (u"ࠨࠩ᝛"))
      self.bstack11ll1l11l11_opy_ = scripts.get(bstack1l1l1ll_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧ᝜"),bstack1l1l1ll_opy_ (u"ࠪࠫ᝝"))
  def bstack11ll1l11l1l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11lll11_opy_, bstack1l1l1ll_opy_ (u"ࠫࡼ࠭᝞")) as file:
        json.dump({
          bstack1l1l1ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢ᝟"): self.commands_to_wrap,
          bstack1l1l1ll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢᝠ"): {
            bstack1l1l1ll_opy_ (u"ࠢࡴࡥࡤࡲࠧᝡ"): self.perform_scan,
            bstack1l1l1ll_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᝢ"): self.bstack11l1l1l11l_opy_,
            bstack1l1l1ll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨᝣ"): self.bstack111111ll_opy_,
            bstack1l1l1ll_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣᝤ"): self.bstack11ll1l11l11_opy_
          },
          bstack1l1l1ll_opy_ (u"ࠦࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠣᝥ"): self.bstack11ll1l11111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1l1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥᝦ").format(e))
      pass
  def bstack1l1lll1ll1_opy_(self, command_name):
    try:
      return any(command.get(bstack1l1l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝧ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1lll11l1l1_opy_ = bstack11ll11ll1l1_opy_()