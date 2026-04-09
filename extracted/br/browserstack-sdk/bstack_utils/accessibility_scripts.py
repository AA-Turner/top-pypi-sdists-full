# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1111l1l1l1l_opy_(object):
  bstack11l111llll_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠬࢄࠧᵣ")), bstack11ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᵤ"))
  bstack1111l1l1l11_opy_ = os.path.join(bstack11l111llll_opy_, bstack11ll11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧᵥ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack1111lll11ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11ll11_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪᵦ")):
      cls.instance = super(bstack1111l1l1l1l_opy_, cls).__new__(cls)
      cls.instance.bstack1111l1l11l1_opy_()
    return cls.instance
  def bstack1111l1l11l1_opy_(self):
    try:
      with open(self.bstack1111l1l1l11_opy_, bstack11ll11_opy_ (u"ࠩࡵࠫᵧ")) as bstack111ll1l11l_opy_:
        bstack1111l1l111l_opy_ = bstack111ll1l11l_opy_.read()
        data = json.loads(bstack1111l1l111l_opy_)
        if bstack11ll11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᵨ") in data:
          self.bstack1l1l111l11l_opy_(data[bstack11ll11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᵩ")])
        if bstack11ll11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱࠫᵪ") in data:
          self.bstack1111l1l11ll_opy_(data[bstack11ll11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲࠬᵫ")])
        if bstack11ll11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᵬ") in data:
          self.bstack1ll1ll1l1_opy_(data[bstack11ll11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᵭ")])
        if bstack11ll11_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵮ") in data:
          self.bstack1111l1l1111_opy_(data[bstack11ll11_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᵯ")])
    except:
      pass
  def bstack1111l1l1111_opy_(self, bstack1111lll11ll_opy_):
    if bstack1111lll11ll_opy_ != None:
      self.bstack1111lll11ll_opy_ = bstack1111lll11ll_opy_
  def bstack1ll1ll1l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᵰ"),bstack11ll11_opy_ (u"ࠬ࠭ᵱ"))
      self.get_results = scripts.get(bstack11ll11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᵲ"),bstack11ll11_opy_ (u"ࠧࠨᵳ"))
      self.get_results_summary = scripts.get(bstack11ll11_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᵴ"),bstack11ll11_opy_ (u"ࠩࠪᵵ"))
      self.save_test_results = scripts.get(bstack11ll11_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᵶ"),bstack11ll11_opy_ (u"ࠫࠬᵷ"))
  def bstack1l1l111l11l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack1111l1l11ll_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack1111l1l1l11_opy_, bstack11ll11_opy_ (u"ࠬࡽࠧᵸ")) as file:
        json.dump({
          bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᵹ"): self.commands_to_wrap,
          bstack11ll11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࡕࡱࡕࡹࡳࠨᵺ"): self.scripts_to_run,
          bstack11ll11_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤᵻ"): {
            bstack11ll11_opy_ (u"ࠤࡶࡧࡦࡴࠢᵼ"): self.perform_scan,
            bstack11ll11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᵽ"): self.get_results,
            bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᵾ"): self.get_results_summary,
            bstack11ll11_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᵿ"): self.save_test_results
          },
          bstack11ll11_opy_ (u"ࠨ࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠥᶀ"): self.bstack1111lll11ll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᶁ").format(e))
      pass
  def bstack1l1l1lll_opy_(self, command_name):
    try:
      return any(command.get(bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᶂ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack1111l1l1l1l_opy_()