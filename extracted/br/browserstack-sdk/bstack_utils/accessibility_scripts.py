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
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1111l11l1ll_opy_(object):
  bstack11l11lll1l_opy_ = os.path.join(os.path.expanduser(bstack111ll11_opy_ (u"ࠬࢄࠧᵿ")), bstack111ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᶀ"))
  bstack1111l11ll1l_opy_ = os.path.join(bstack11l11lll1l_opy_, bstack111ll11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧᶁ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack1111l1llll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111ll11_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪᶂ")):
      cls.instance = super(bstack1111l11l1ll_opy_, cls).__new__(cls)
      cls.instance.bstack1111l11l11l_opy_()
    return cls.instance
  def bstack1111l11l11l_opy_(self):
    try:
      with open(self.bstack1111l11ll1l_opy_, bstack111ll11_opy_ (u"ࠩࡵࠫᶃ")) as bstack1l11ll111l_opy_:
        bstack1111l11lll1_opy_ = bstack1l11ll111l_opy_.read()
        data = json.loads(bstack1111l11lll1_opy_)
        if bstack111ll11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᶄ") in data:
          self.bstack1l11lll11ll_opy_(data[bstack111ll11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᶅ")])
        if bstack111ll11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱࠫᶆ") in data:
          self.bstack1111l11l1l1_opy_(data[bstack111ll11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲࠬᶇ")])
        if bstack111ll11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᶈ") in data:
          self.bstack1l1l1l1l11_opy_(data[bstack111ll11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᶉ")])
        if bstack111ll11_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᶊ") in data:
          self.bstack1111l11ll11_opy_(data[bstack111ll11_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᶋ")])
    except:
      pass
  def bstack1111l11ll11_opy_(self, bstack1111l1llll1_opy_):
    if bstack1111l1llll1_opy_ != None:
      self.bstack1111l1llll1_opy_ = bstack1111l1llll1_opy_
  def bstack1l1l1l1l11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack111ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᶌ"),bstack111ll11_opy_ (u"ࠬ࠭ᶍ"))
      self.get_results = scripts.get(bstack111ll11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᶎ"),bstack111ll11_opy_ (u"ࠧࠨᶏ"))
      self.get_results_summary = scripts.get(bstack111ll11_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᶐ"),bstack111ll11_opy_ (u"ࠩࠪᶑ"))
      self.save_test_results = scripts.get(bstack111ll11_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᶒ"),bstack111ll11_opy_ (u"ࠫࠬᶓ"))
  def bstack1l11lll11ll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack1111l11l1l1_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack1111l11ll1l_opy_, bstack111ll11_opy_ (u"ࠬࡽࠧᶔ")) as file:
        json.dump({
          bstack111ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᶕ"): self.commands_to_wrap,
          bstack111ll11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࡕࡱࡕࡹࡳࠨᶖ"): self.scripts_to_run,
          bstack111ll11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤᶗ"): {
            bstack111ll11_opy_ (u"ࠤࡶࡧࡦࡴࠢᶘ"): self.perform_scan,
            bstack111ll11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᶙ"): self.get_results,
            bstack111ll11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᶚ"): self.get_results_summary,
            bstack111ll11_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᶛ"): self.save_test_results
          },
          bstack111ll11_opy_ (u"ࠨ࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠥᶜ"): self.bstack1111l1llll1_opy_
        }, file)
    except Exception as e:
      logger.error(bstack111ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᶝ").format(e))
      pass
  def bstack1llllll1lll_opy_(self, command_name):
    try:
      return any(command.get(bstack111ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᶞ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack1111l11l1ll_opy_()