# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111ll1111l1_opy_(object):
  bstack1lll111ll_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠫࢃ࠭᭪")), bstack1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᭫"))
  bstack111ll111ll1_opy_ = os.path.join(bstack1lll111ll_opy_, bstack1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ᭬࠭"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack111lll1l1ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩ᭭")):
      cls.instance = super(bstack111ll1111l1_opy_, cls).__new__(cls)
      cls.instance.bstack111ll111lll_opy_()
    return cls.instance
  def bstack111ll111lll_opy_(self):
    try:
      with open(self.bstack111ll111ll1_opy_, bstack1l1_opy_ (u"ࠨࡴࠪ᭮")) as bstack1l11ll1l_opy_:
        bstack111ll111l1l_opy_ = bstack1l11ll1l_opy_.read()
        data = json.loads(bstack111ll111l1l_opy_)
        if bstack1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ᭯") in data:
          self.bstack111llll11l1_opy_(data[bstack1l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ᭰")])
        if bstack1l1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷ࡙ࡵࡒࡶࡰࠪ᭱") in data:
          self.bstack111ll1111ll_opy_(data[bstack1l1_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱࠫ᭲")])
        if bstack1l1_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ᭳") in data:
          self.bstack1llll11ll_opy_(data[bstack1l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ᭴")])
        if bstack1l1_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭵") in data:
          self.bstack111ll111l11_opy_(data[bstack1l1_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᭶")])
    except:
      pass
  def bstack111ll111l11_opy_(self, bstack111lll1l1ll_opy_):
    if bstack111lll1l1ll_opy_ != None:
      self.bstack111lll1l1ll_opy_ = bstack111lll1l1ll_opy_
  def bstack1llll11ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ᭷"),bstack1l1_opy_ (u"ࠫࠬ᭸"))
      self.get_results = scripts.get(bstack1l1_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩ᭹"),bstack1l1_opy_ (u"࠭ࠧ᭺"))
      self.get_results_summary = scripts.get(bstack1l1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫ᭻"),bstack1l1_opy_ (u"ࠨࠩ᭼"))
      self.save_test_results = scripts.get(bstack1l1_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧ᭽"),bstack1l1_opy_ (u"ࠪࠫ᭾"))
  def bstack111llll11l1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack111ll1111ll_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack111ll111ll1_opy_, bstack1l1_opy_ (u"ࠫࡼ࠭᭿")) as file:
        json.dump({
          bstack1l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢᮀ"): self.commands_to_wrap,
          bstack1l1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲࠧᮁ"): self.scripts_to_run,
          bstack1l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣᮂ"): {
            bstack1l1_opy_ (u"ࠣࡵࡦࡥࡳࠨᮃ"): self.perform_scan,
            bstack1l1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᮄ"): self.get_results,
            bstack1l1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᮅ"): self.get_results_summary,
            bstack1l1_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᮆ"): self.save_test_results
          },
          bstack1l1_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤᮇ"): self.bstack111lll1l1ll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᮈ").format(e))
      pass
  def bstack1lll1l1ll1_opy_(self, command_name):
    try:
      return any(command.get(bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᮉ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack111ll1111l1_opy_()