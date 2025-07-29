# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
import json
from bstack_utils.bstack1ll11l1ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11ll11l_opy_(object):
  bstack1l1l1l1lll_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"࠭ࡾࠨᝄ")), bstackl_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᝅ"))
  bstack11ll11ll1l1_opy_ = os.path.join(bstack1l1l1l1lll_opy_, bstackl_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᝆ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll1l1llll_opy_ = None
  bstack111lllll1l_opy_ = None
  bstack11ll1llll1l_opy_ = None
  bstack11ll11llll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstackl_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᝇ")):
      cls.instance = super(bstack11ll11ll11l_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11l1lll_opy_()
    return cls.instance
  def bstack11ll11l1lll_opy_(self):
    try:
      with open(self.bstack11ll11ll1l1_opy_, bstackl_opy_ (u"ࠪࡶࠬᝈ")) as bstack11l11111l1_opy_:
        bstack11ll11ll1ll_opy_ = bstack11l11111l1_opy_.read()
        data = json.loads(bstack11ll11ll1ll_opy_)
        if bstackl_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᝉ") in data:
          self.bstack11ll1lll111_opy_(data[bstackl_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᝊ")])
        if bstackl_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᝋ") in data:
          self.bstack111l1ll11_opy_(data[bstackl_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᝌ")])
        if bstackl_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᝍ") in data:
          self.bstack11ll11ll111_opy_(data[bstackl_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᝎ")])
    except:
      pass
  def bstack11ll11ll111_opy_(self, bstack11ll11llll1_opy_):
    if bstack11ll11llll1_opy_ != None:
      self.bstack11ll11llll1_opy_ = bstack11ll11llll1_opy_
  def bstack111l1ll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstackl_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᝏ"),bstackl_opy_ (u"ࠫࠬᝐ"))
      self.bstack1ll1l1llll_opy_ = scripts.get(bstackl_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᝑ"),bstackl_opy_ (u"࠭ࠧᝒ"))
      self.bstack111lllll1l_opy_ = scripts.get(bstackl_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᝓ"),bstackl_opy_ (u"ࠨࠩ᝔"))
      self.bstack11ll1llll1l_opy_ = scripts.get(bstackl_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧ᝕"),bstackl_opy_ (u"ࠪࠫ᝖"))
  def bstack11ll1lll111_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11ll1l1_opy_, bstackl_opy_ (u"ࠫࡼ࠭᝗")) as file:
        json.dump({
          bstackl_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢ᝘"): self.commands_to_wrap,
          bstackl_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢ᝙"): {
            bstackl_opy_ (u"ࠢࡴࡥࡤࡲࠧ᝚"): self.perform_scan,
            bstackl_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ᝛"): self.bstack1ll1l1llll_opy_,
            bstackl_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ᝜"): self.bstack111lllll1l_opy_,
            bstackl_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ᝝"): self.bstack11ll1llll1l_opy_
          },
          bstackl_opy_ (u"ࠦࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠣ᝞"): self.bstack11ll11llll1_opy_
        }, file)
    except Exception as e:
      logger.error(bstackl_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥ᝟").format(e))
      pass
  def bstack1ll1111l1_opy_(self, bstack1ll11l1llll_opy_):
    try:
      return any(command.get(bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝠ")) == bstack1ll11l1llll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l111l111_opy_ = bstack11ll11ll11l_opy_()