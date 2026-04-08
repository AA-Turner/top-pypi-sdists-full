# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1111l1l1l11_opy_(object):
  bstack1lll11lll1_opy_ = os.path.join(os.path.expanduser(bstack111l_opy_ (u"ࠫࢃ࠭ᵢ")), bstack111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᵣ"))
  bstack1111l1l11ll_opy_ = os.path.join(bstack1lll11lll1_opy_, bstack111l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ࠭ᵤ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack1111ll1ll1l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111l_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩᵥ")):
      cls.instance = super(bstack1111l1l1l11_opy_, cls).__new__(cls)
      cls.instance.bstack1111l1l11l1_opy_()
    return cls.instance
  def bstack1111l1l11l1_opy_(self):
    try:
      with open(self.bstack1111l1l11ll_opy_, bstack111l_opy_ (u"ࠨࡴࠪᵦ")) as bstack1l1llll11_opy_:
        bstack1111l1l1l1l_opy_ = bstack1l1llll11_opy_.read()
        data = json.loads(bstack1111l1l1l1l_opy_)
        if bstack111l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᵧ") in data:
          self.bstack1l11l11l1l1_opy_(data[bstack111l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᵨ")])
        if bstack111l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷ࡙ࡵࡒࡶࡰࠪᵩ") in data:
          self.bstack1111l1l111l_opy_(data[bstack111l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱࠫᵪ")])
        if bstack111l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᵫ") in data:
          self.bstack1l11l1l1_opy_(data[bstack111l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᵬ")])
        if bstack111l_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵭ") in data:
          self.bstack1111l1l1ll1_opy_(data[bstack111l_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵮ")])
    except:
      pass
  def bstack1111l1l1ll1_opy_(self, bstack1111ll1ll1l_opy_):
    if bstack1111ll1ll1l_opy_ != None:
      self.bstack1111ll1ll1l_opy_ = bstack1111ll1ll1l_opy_
  def bstack1l11l1l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack111l_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᵯ"),bstack111l_opy_ (u"ࠫࠬᵰ"))
      self.get_results = scripts.get(bstack111l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᵱ"),bstack111l_opy_ (u"࠭ࠧᵲ"))
      self.get_results_summary = scripts.get(bstack111l_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᵳ"),bstack111l_opy_ (u"ࠨࠩᵴ"))
      self.save_test_results = scripts.get(bstack111l_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧᵵ"),bstack111l_opy_ (u"ࠪࠫᵶ"))
  def bstack1l11l11l1l1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack1111l1l111l_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack1111l1l11ll_opy_, bstack111l_opy_ (u"ࠫࡼ࠭ᵷ")) as file:
        json.dump({
          bstack111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢᵸ"): self.commands_to_wrap,
          bstack111l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲࠧᵹ"): self.scripts_to_run,
          bstack111l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣᵺ"): {
            bstack111l_opy_ (u"ࠣࡵࡦࡥࡳࠨᵻ"): self.perform_scan,
            bstack111l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᵼ"): self.get_results,
            bstack111l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᵽ"): self.get_results_summary,
            bstack111l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᵾ"): self.save_test_results
          },
          bstack111l_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤᵿ"): self.bstack1111ll1ll1l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᶀ").format(e))
      pass
  def bstack111l11l1_opy_(self, command_name):
    try:
      return any(command.get(bstack111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᶁ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack1111l1l1l11_opy_()