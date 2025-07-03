# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import json
from bstack_utils.bstack1lll1l1l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11lll11_opy_(object):
  bstack1ll1l1111_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"࠭ࡾࠨ᜽")), bstack1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᜾"))
  bstack11ll11lll1l_opy_ = os.path.join(bstack1ll1l1111_opy_, bstack1l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ᜿"))
  commands_to_wrap = None
  perform_scan = None
  bstack11llll1l1_opy_ = None
  bstack1lllll111_opy_ = None
  bstack11ll1l11ll1_opy_ = None
  bstack11ll1l1l111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᝀ")):
      cls.instance = super(bstack11ll11lll11_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11ll1ll_opy_()
    return cls.instance
  def bstack11ll11ll1ll_opy_(self):
    try:
      with open(self.bstack11ll11lll1l_opy_, bstack1l1_opy_ (u"ࠪࡶࠬᝁ")) as bstack111lll1l_opy_:
        bstack11ll11ll1l1_opy_ = bstack111lll1l_opy_.read()
        data = json.loads(bstack11ll11ll1l1_opy_)
        if bstack1l1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᝂ") in data:
          self.bstack11ll1lllll1_opy_(data[bstack1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᝃ")])
        if bstack1l1_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᝄ") in data:
          self.bstack1l111l11ll_opy_(data[bstack1l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᝅ")])
        if bstack1l1_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᝆ") in data:
          self.bstack11ll11llll1_opy_(data[bstack1l1_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᝇ")])
    except:
      pass
  def bstack11ll11llll1_opy_(self, bstack11ll1l1l111_opy_):
    if bstack11ll1l1l111_opy_ != None:
      self.bstack11ll1l1l111_opy_ = bstack11ll1l1l111_opy_
  def bstack1l111l11ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᝈ"),bstack1l1_opy_ (u"ࠫࠬᝉ"))
      self.bstack11llll1l1_opy_ = scripts.get(bstack1l1_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᝊ"),bstack1l1_opy_ (u"࠭ࠧᝋ"))
      self.bstack1lllll111_opy_ = scripts.get(bstack1l1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᝌ"),bstack1l1_opy_ (u"ࠨࠩᝍ"))
      self.bstack11ll1l11ll1_opy_ = scripts.get(bstack1l1_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧᝎ"),bstack1l1_opy_ (u"ࠪࠫᝏ"))
  def bstack11ll1lllll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11lll1l_opy_, bstack1l1_opy_ (u"ࠫࡼ࠭ᝐ")) as file:
        json.dump({
          bstack1l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢᝑ"): self.commands_to_wrap,
          bstack1l1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢᝒ"): {
            bstack1l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᝓ"): self.perform_scan,
            bstack1l1_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ᝔"): self.bstack11llll1l1_opy_,
            bstack1l1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ᝕"): self.bstack1lllll111_opy_,
            bstack1l1_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ᝖"): self.bstack11ll1l11ll1_opy_
          },
          bstack1l1_opy_ (u"ࠦࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠣ᝗"): self.bstack11ll1l1l111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥ᝘").format(e))
      pass
  def bstack1lll1111l1_opy_(self, bstack1ll1l111l1l_opy_):
    try:
      return any(command.get(bstack1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᝙")) == bstack1ll1l111l1l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11ll1lllll_opy_ = bstack11ll11lll11_opy_()