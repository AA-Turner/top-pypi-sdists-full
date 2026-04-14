# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1111l11l1ll_opy_(object):
  bstack1ll1111l11_opy_ = os.path.join(os.path.expanduser(bstack1l111l_opy_ (u"ࠬࢄࠧᵿ")), bstack1l111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᶀ"))
  bstack1111l11l1l1_opy_ = os.path.join(bstack1ll1111l11_opy_, bstack1l111l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧᶁ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack1111l1lll1l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l111l_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪᶂ")):
      cls.instance = super(bstack1111l11l1ll_opy_, cls).__new__(cls)
      cls.instance.bstack1111l11ll11_opy_()
    return cls.instance
  def bstack1111l11ll11_opy_(self):
    try:
      with open(self.bstack1111l11l1l1_opy_, bstack1l111l_opy_ (u"ࠩࡵࠫᶃ")) as bstack11111lll1l_opy_:
        bstack1111l11l11l_opy_ = bstack11111lll1l_opy_.read()
        data = json.loads(bstack1111l11l11l_opy_)
        if bstack1l111l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᶄ") in data:
          self.bstack1l1l1l11ll1_opy_(data[bstack1l111l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᶅ")])
        if bstack1l111l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱࠫᶆ") in data:
          self.bstack1111l11lll1_opy_(data[bstack1l111l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲࠬᶇ")])
        if bstack1l111l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᶈ") in data:
          self.bstack11l111111l_opy_(data[bstack1l111l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᶉ")])
        if bstack1l111l_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᶊ") in data:
          self.bstack1111l11ll1l_opy_(data[bstack1l111l_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᶋ")])
    except:
      pass
  def bstack1111l11ll1l_opy_(self, bstack1111l1lll1l_opy_):
    if bstack1111l1lll1l_opy_ != None:
      self.bstack1111l1lll1l_opy_ = bstack1111l1lll1l_opy_
  def bstack11l111111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l111l_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᶌ"),bstack1l111l_opy_ (u"ࠬ࠭ᶍ"))
      self.get_results = scripts.get(bstack1l111l_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᶎ"),bstack1l111l_opy_ (u"ࠧࠨᶏ"))
      self.get_results_summary = scripts.get(bstack1l111l_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᶐ"),bstack1l111l_opy_ (u"ࠩࠪᶑ"))
      self.save_test_results = scripts.get(bstack1l111l_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᶒ"),bstack1l111l_opy_ (u"ࠫࠬᶓ"))
  def bstack1l1l1l11ll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack1111l11lll1_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack1111l11l1l1_opy_, bstack1l111l_opy_ (u"ࠬࡽࠧᶔ")) as file:
        json.dump({
          bstack1l111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᶕ"): self.commands_to_wrap,
          bstack1l111l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࡕࡱࡕࡹࡳࠨᶖ"): self.scripts_to_run,
          bstack1l111l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤᶗ"): {
            bstack1l111l_opy_ (u"ࠤࡶࡧࡦࡴࠢᶘ"): self.perform_scan,
            bstack1l111l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᶙ"): self.get_results,
            bstack1l111l_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᶚ"): self.get_results_summary,
            bstack1l111l_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᶛ"): self.save_test_results
          },
          bstack1l111l_opy_ (u"ࠨ࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠥᶜ"): self.bstack1111l1lll1l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᶝ").format(e))
      pass
  def bstack1111l1111_opy_(self, command_name):
    try:
      return any(command.get(bstack1l111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᶞ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack1111l11l1ll_opy_()