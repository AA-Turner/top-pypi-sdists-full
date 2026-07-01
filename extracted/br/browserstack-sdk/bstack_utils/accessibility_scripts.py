# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11111l1ll1l_opy_(object):
  bstack111lll111l_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠩࢁࠫ⁆")), bstack1l1llll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⁇"))
  bstack11111l1l1l1_opy_ = os.path.join(bstack111lll111l_opy_, bstack1l1llll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫ⁈"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack11111ll1lll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1llll_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧ⁉")):
      cls.instance = super(bstack11111l1ll1l_opy_, cls).__new__(cls)
      cls.instance.bstack11111l1l111_opy_()
    return cls.instance
  def bstack11111l1l111_opy_(self):
    try:
      with open(self.bstack11111l1l1l1_opy_, bstack1l1llll_opy_ (u"࠭ࡲࠨ⁊")) as bstack1l111ll1ll_opy_:
        bstack11111l1l11l_opy_ = bstack1l111ll1ll_opy_.read()
        data = json.loads(bstack11111l1l11l_opy_)
        if bstack1l1llll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ⁋") in data:
          self.bstack11lll1l1l1l_opy_(data[bstack1l1llll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ⁌")])
        if bstack1l1llll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࡗࡳࡗࡻ࡮ࠨ⁍") in data:
          self.bstack11111l1ll11_opy_(data[bstack1l1llll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࡘࡴࡘࡵ࡯ࠩ⁎")])
        if bstack1l1llll_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ⁏") in data:
          self.bstack1ll1l1ll1l_opy_(data[bstack1l1llll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭⁐")])
        if bstack1l1llll_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⁑") in data:
          self.bstack11111l1l1ll_opy_(data[bstack1l1llll_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ⁒")])
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵࠣࡎࡘࡕࡎࠡ࡮ࡲࡥࡩࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿ࠽ࠤࢀࢃࠢ⁓").format(type(e).__name__, e), exc_info=True)
  def bstack11111l1l1ll_opy_(self, bstack11111ll1lll_opy_):
    if bstack11111ll1lll_opy_ != None:
      self.bstack11111ll1lll_opy_ = bstack11111ll1lll_opy_
  def bstack1ll1l1ll1l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1llll_opy_ (u"ࠩࡶࡧࡦࡴࠧ⁔"),bstack1l1llll_opy_ (u"ࠪࠫ⁕"))
      self.get_results = scripts.get(bstack1l1llll_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨ⁖"),bstack1l1llll_opy_ (u"ࠬ࠭⁗"))
      self.get_results_summary = scripts.get(bstack1l1llll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪ⁘"),bstack1l1llll_opy_ (u"ࠧࠨ⁙"))
      self.save_test_results = scripts.get(bstack1l1llll_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭⁚"),bstack1l1llll_opy_ (u"ࠩࠪ⁛"))
  def bstack11lll1l1l1l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack11111l1ll11_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack11111l1l1l1_opy_, bstack1l1llll_opy_ (u"ࠪࡻࠬ⁜")) as file:
        json.dump({
          bstack1l1llll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨ⁝"): self.commands_to_wrap,
          bstack1l1llll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱࠦ⁞"): self.scripts_to_run,
          bstack1l1llll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢ "): {
            bstack1l1llll_opy_ (u"ࠢࡴࡥࡤࡲࠧ⁠"): self.perform_scan,
            bstack1l1llll_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ⁡"): self.get_results,
            bstack1l1llll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ⁢"): self.get_results_summary,
            bstack1l1llll_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ⁣"): self.save_test_results
          },
          bstack1l1llll_opy_ (u"ࠦࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠣ⁤"): self.bstack11111ll1lll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥ⁥").format(e))
      pass
  def bstack1ll111ll1l1_opy_(self, command_name):
    try:
      return any(command.get(bstack1l1llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁦")) == command_name for command in self.commands_to_wrap)
    except Exception as e:
      logger.debug(bstack1l1llll_opy_ (u"ࠢࡴࡪࡲࡹࡱࡪ࡟ࡸࡴࡤࡴࡤࡩ࡯࡮࡯ࡤࡲࡩࠦ࡬ࡰࡱ࡮ࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿ࠽ࠤࢀࢃࠢ⁧").format(type(e).__name__, e), exc_info=True)
      return False
accessibility_scripts = bstack11111l1ll1l_opy_()