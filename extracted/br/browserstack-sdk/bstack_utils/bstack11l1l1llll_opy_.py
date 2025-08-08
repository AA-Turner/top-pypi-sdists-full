# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import json
from bstack_utils.bstack111111111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11lll11_opy_(object):
  bstack1llll11l11_opy_ = os.path.join(os.path.expanduser(bstack1ll1ll_opy_ (u"࠭ࡾࠨᝄ")), bstack1ll1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᝅ"))
  bstack11ll11lll1l_opy_ = os.path.join(bstack1llll11l11_opy_, bstack1ll1ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᝆ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1llll1ll_opy_ = None
  bstack11l1l1111l_opy_ = None
  bstack11ll1ll1ll1_opy_ = None
  bstack11ll1lll111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᝇ")):
      cls.instance = super(bstack11ll11lll11_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11lllll_opy_()
    return cls.instance
  def bstack11ll11lllll_opy_(self):
    try:
      with open(self.bstack11ll11lll1l_opy_, bstack1ll1ll_opy_ (u"ࠪࡶࠬᝈ")) as bstack11l11lll11_opy_:
        bstack11ll11ll1ll_opy_ = bstack11l11lll11_opy_.read()
        data = json.loads(bstack11ll11ll1ll_opy_)
        if bstack1ll1ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᝉ") in data:
          self.bstack11ll1lllll1_opy_(data[bstack1ll1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᝊ")])
        if bstack1ll1ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᝋ") in data:
          self.bstack1l1llll1_opy_(data[bstack1ll1ll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᝌ")])
        if bstack1ll1ll_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᝍ") in data:
          self.bstack11ll11llll1_opy_(data[bstack1ll1ll_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᝎ")])
    except:
      pass
  def bstack11ll11llll1_opy_(self, bstack11ll1lll111_opy_):
    if bstack11ll1lll111_opy_ != None:
      self.bstack11ll1lll111_opy_ = bstack11ll1lll111_opy_
  def bstack1l1llll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll1ll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᝏ"),bstack1ll1ll_opy_ (u"ࠫࠬᝐ"))
      self.bstack1llll1ll_opy_ = scripts.get(bstack1ll1ll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᝑ"),bstack1ll1ll_opy_ (u"࠭ࠧᝒ"))
      self.bstack11l1l1111l_opy_ = scripts.get(bstack1ll1ll_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᝓ"),bstack1ll1ll_opy_ (u"ࠨࠩ᝔"))
      self.bstack11ll1ll1ll1_opy_ = scripts.get(bstack1ll1ll_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧ᝕"),bstack1ll1ll_opy_ (u"ࠪࠫ᝖"))
  def bstack11ll1lllll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11lll1l_opy_, bstack1ll1ll_opy_ (u"ࠫࡼ࠭᝗")) as file:
        json.dump({
          bstack1ll1ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢ᝘"): self.commands_to_wrap,
          bstack1ll1ll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢ᝙"): {
            bstack1ll1ll_opy_ (u"ࠢࡴࡥࡤࡲࠧ᝚"): self.perform_scan,
            bstack1ll1ll_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ᝛"): self.bstack1llll1ll_opy_,
            bstack1ll1ll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ᝜"): self.bstack11l1l1111l_opy_,
            bstack1ll1ll_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ᝝"): self.bstack11ll1ll1ll1_opy_
          },
          bstack1ll1ll_opy_ (u"ࠦࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠣ᝞"): self.bstack11ll1lll111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1ll1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥ᝟").format(e))
      pass
  def bstack1l11llll_opy_(self, command_name):
    try:
      return any(command.get(bstack1ll1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝠ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack11l1l1llll_opy_ = bstack11ll11lll11_opy_()