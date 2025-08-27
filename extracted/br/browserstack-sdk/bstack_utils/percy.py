# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l11l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1l111l1ll1_opy_ import bstack1ll11l11l1_opy_
class bstack1llllllll_opy_:
  working_dir = os.getcwd()
  bstack11111l11_opy_ = False
  config = {}
  bstack11l1111ll11_opy_ = bstack1111lll_opy_ (u"ࠨࠩẚ")
  binary_path = bstack1111lll_opy_ (u"ࠩࠪẛ")
  bstack11111l1llll_opy_ = bstack1111lll_opy_ (u"ࠪࠫẜ")
  bstack11ll11lll1_opy_ = False
  bstack1111l1lllll_opy_ = None
  bstack1111l1l1l1l_opy_ = {}
  bstack1111l111ll1_opy_ = 300
  bstack1111l1l1111_opy_ = False
  logger = None
  bstack1111ll111l1_opy_ = False
  bstack1lll1l11l_opy_ = False
  percy_build_id = None
  bstack1111ll11ll1_opy_ = bstack1111lll_opy_ (u"ࠫࠬẝ")
  bstack11111lll1l1_opy_ = {
    bstack1111lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬẞ") : 1,
    bstack1111lll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧẟ") : 2,
    bstack1111lll_opy_ (u"ࠧࡦࡦࡪࡩࠬẠ") : 3,
    bstack1111lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨạ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11111ll1ll1_opy_(self):
    bstack11111l11lll_opy_ = bstack1111lll_opy_ (u"ࠩࠪẢ")
    bstack11111l1l1ll_opy_ = sys.platform
    bstack11111l1l1l1_opy_ = bstack1111lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩả")
    if re.match(bstack1111lll_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦẤ"), bstack11111l1l1ll_opy_) != None:
      bstack11111l11lll_opy_ = bstack11l1ll1ll1l_opy_ + bstack1111lll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨấ")
      self.bstack1111ll11ll1_opy_ = bstack1111lll_opy_ (u"࠭࡭ࡢࡥࠪẦ")
    elif re.match(bstack1111lll_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧầ"), bstack11111l1l1ll_opy_) != None:
      bstack11111l11lll_opy_ = bstack11l1ll1ll1l_opy_ + bstack1111lll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤẨ")
      bstack11111l1l1l1_opy_ = bstack1111lll_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧẩ")
      self.bstack1111ll11ll1_opy_ = bstack1111lll_opy_ (u"ࠪࡻ࡮ࡴࠧẪ")
    else:
      bstack11111l11lll_opy_ = bstack11l1ll1ll1l_opy_ + bstack1111lll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢẫ")
      self.bstack1111ll11ll1_opy_ = bstack1111lll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫẬ")
    return bstack11111l11lll_opy_, bstack11111l1l1l1_opy_
  def bstack11111lll111_opy_(self):
    try:
      bstack1111l11llll_opy_ = [os.path.join(expanduser(bstack1111lll_opy_ (u"ࠨࡾࠣậ")), bstack1111lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧẮ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111l11llll_opy_:
        if(self.bstack11111l1l11l_opy_(path)):
          return path
      raise bstack1111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧắ")
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦẰ").format(e))
  def bstack11111l1l11l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111l111l11_opy_(self, bstack1111l111l1l_opy_):
    return os.path.join(bstack1111l111l1l_opy_, self.bstack11l1111ll11_opy_ + bstack1111lll_opy_ (u"ࠥ࠲ࡪࡺࡡࡨࠤằ"))
  def bstack1111ll11l11_opy_(self, bstack1111l111l1l_opy_, bstack11111lllll1_opy_):
    if not bstack11111lllll1_opy_: return
    try:
      bstack11111l1ll1l_opy_ = self.bstack1111l111l11_opy_(bstack1111l111l1l_opy_)
      with open(bstack11111l1ll1l_opy_, bstack1111lll_opy_ (u"ࠦࡼࠨẲ")) as f:
        f.write(bstack11111lllll1_opy_)
        self.logger.debug(bstack1111lll_opy_ (u"࡙ࠧࡡࡷࡧࡧࠤࡳ࡫ࡷࠡࡇࡗࡥ࡬ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠤẳ"))
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡵࡪࡨࠤࡪࡺࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨẴ").format(e))
  def bstack11111llllll_opy_(self, bstack1111l111l1l_opy_):
    try:
      bstack11111l1ll1l_opy_ = self.bstack1111l111l11_opy_(bstack1111l111l1l_opy_)
      if os.path.exists(bstack11111l1ll1l_opy_):
        with open(bstack11111l1ll1l_opy_, bstack1111lll_opy_ (u"ࠢࡳࠤẵ")) as f:
          bstack11111lllll1_opy_ = f.read().strip()
          return bstack11111lllll1_opy_ if bstack11111lllll1_opy_ else None
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡ࡮ࡲࡥࡩ࡯࡮ࡨࠢࡈࡘࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦẶ").format(e))
  def bstack1111l1l11l1_opy_(self, bstack1111l111l1l_opy_, bstack11111l11lll_opy_):
    bstack1111l111lll_opy_ = self.bstack11111llllll_opy_(bstack1111l111l1l_opy_)
    if bstack1111l111lll_opy_:
      try:
        bstack11111ll1111_opy_ = self.bstack1111l1lll1l_opy_(bstack1111l111lll_opy_, bstack11111l11lll_opy_)
        if not bstack11111ll1111_opy_:
          self.logger.debug(bstack1111lll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡶࠤࡺࡶࠠࡵࡱࠣࡨࡦࡺࡥࠡࠪࡈࡘࡦ࡭ࠠࡶࡰࡦ࡬ࡦࡴࡧࡦࡦࠬࠦặ"))
          return True
        self.logger.debug(bstack1111lll_opy_ (u"ࠥࡒࡪࡽࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡦࠤẸ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1111lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡦࡰࡴࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠰ࠥࡻࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥẹ").format(e))
    return False
  def bstack1111l1lll1l_opy_(self, bstack1111l111lll_opy_, bstack11111l11lll_opy_):
    try:
      headers = {
        bstack1111lll_opy_ (u"ࠧࡏࡦ࠮ࡐࡲࡲࡪ࠳ࡍࡢࡶࡦ࡬ࠧẺ"): bstack1111l111lll_opy_
      }
      response = bstack1l11l1l1_opy_(bstack1111lll_opy_ (u"࠭ࡇࡆࡖࠪẻ"), bstack11111l11lll_opy_, {}, {bstack1111lll_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣẼ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸࡀࠠࡼࡿࠥẽ").format(e))
  @measure(event_name=EVENTS.bstack11l1ll11l1l_opy_, stage=STAGE.bstack11111lll_opy_)
  def bstack11111ll1l1l_opy_(self, bstack11111l11lll_opy_, bstack11111l1l1l1_opy_):
    try:
      bstack11111ll1lll_opy_ = self.bstack11111lll111_opy_()
      bstack1111l1l111l_opy_ = os.path.join(bstack11111ll1lll_opy_, bstack1111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬẾ"))
      bstack11111lll1ll_opy_ = os.path.join(bstack11111ll1lll_opy_, bstack11111l1l1l1_opy_)
      if self.bstack1111l1l11l1_opy_(bstack11111ll1lll_opy_, bstack11111l11lll_opy_): # if bstack11111l1ll11_opy_, bstack1l1l11l111l_opy_ bstack11111lllll1_opy_ is bstack1111l11l1l1_opy_ to bstack11l1111lll1_opy_ version available (response 304)
        if os.path.exists(bstack11111lll1ll_opy_):
          self.logger.info(bstack1111lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧế").format(bstack11111lll1ll_opy_))
          return bstack11111lll1ll_opy_
        if os.path.exists(bstack1111l1l111l_opy_):
          self.logger.info(bstack1111lll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤỀ").format(bstack1111l1l111l_opy_))
          return self.bstack1111l1111ll_opy_(bstack1111l1l111l_opy_, bstack11111l1l1l1_opy_)
      self.logger.info(bstack1111lll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥề").format(bstack11111l11lll_opy_))
      response = bstack1l11l1l1_opy_(bstack1111lll_opy_ (u"࠭ࡇࡆࡖࠪỂ"), bstack11111l11lll_opy_, {}, {})
      if response.status_code == 200:
        bstack1111l1llll1_opy_ = response.headers.get(bstack1111lll_opy_ (u"ࠢࡆࡖࡤ࡫ࠧể"), bstack1111lll_opy_ (u"ࠣࠤỄ"))
        if bstack1111l1llll1_opy_:
          self.bstack1111ll11l11_opy_(bstack11111ll1lll_opy_, bstack1111l1llll1_opy_)
        with open(bstack1111l1l111l_opy_, bstack1111lll_opy_ (u"ࠩࡺࡦࠬễ")) as file:
          file.write(response.content)
        self.logger.info(bstack1111lll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣỆ").format(bstack1111l1l111l_opy_))
        return self.bstack1111l1111ll_opy_(bstack1111l1l111l_opy_, bstack11111l1l1l1_opy_)
      else:
        raise(bstack1111lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢệ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨỈ").format(e))
  def bstack11111llll1l_opy_(self, bstack11111l11lll_opy_, bstack11111l1l1l1_opy_):
    try:
      retry = 2
      bstack11111lll1ll_opy_ = None
      bstack1111l1lll11_opy_ = False
      while retry > 0:
        bstack11111lll1ll_opy_ = self.bstack11111ll1l1l_opy_(bstack11111l11lll_opy_, bstack11111l1l1l1_opy_)
        bstack1111l1lll11_opy_ = self.bstack11111lll11l_opy_(bstack11111l11lll_opy_, bstack11111l1l1l1_opy_, bstack11111lll1ll_opy_)
        if bstack1111l1lll11_opy_:
          break
        retry -= 1
      return bstack11111lll1ll_opy_, bstack1111l1lll11_opy_
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥỉ").format(e))
    return bstack11111lll1ll_opy_, False
  def bstack11111lll11l_opy_(self, bstack11111l11lll_opy_, bstack11111l1l1l1_opy_, bstack11111lll1ll_opy_, bstack1111l11111l_opy_ = 0):
    if bstack1111l11111l_opy_ > 1:
      return False
    if bstack11111lll1ll_opy_ == None or os.path.exists(bstack11111lll1ll_opy_) == False:
      self.logger.warn(bstack1111lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧỊ"))
      return False
    bstack1111l11l111_opy_ = bstack1111lll_opy_ (u"ࡳࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࡠ࠳ࡢࡤࠬࠤị")
    command = bstack1111lll_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨỌ").format(bstack11111lll1ll_opy_)
    bstack11111ll111l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111l11l111_opy_, bstack11111ll111l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1111lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤọ"))
      return False
  def bstack1111l1111ll_opy_(self, bstack1111l1l111l_opy_, bstack11111l1l1l1_opy_):
    try:
      working_dir = os.path.dirname(bstack1111l1l111l_opy_)
      shutil.unpack_archive(bstack1111l1l111l_opy_, working_dir)
      bstack11111lll1ll_opy_ = os.path.join(working_dir, bstack11111l1l1l1_opy_)
      os.chmod(bstack11111lll1ll_opy_, 0o755)
      return bstack11111lll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧỎ"))
  def bstack1111l1ll1ll_opy_(self):
    try:
      bstack1111l1l1l11_opy_ = self.config.get(bstack1111lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫỏ"))
      bstack1111l1ll1ll_opy_ = bstack1111l1l1l11_opy_ or (bstack1111l1l1l11_opy_ is None and self.bstack11111l11_opy_)
      if not bstack1111l1ll1ll_opy_ or self.config.get(bstack1111lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩỐ"), None) not in bstack11l1llll11l_opy_:
        return False
      self.bstack11ll11lll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤố").format(e))
  def bstack11111l11ll1_opy_(self):
    try:
      bstack11111l11ll1_opy_ = self.percy_capture_mode
      return bstack11111l11ll1_opy_
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤỒ").format(e))
  def init(self, bstack11111l11_opy_, config, logger):
    self.bstack11111l11_opy_ = bstack11111l11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111l1ll1ll_opy_():
      return
    self.bstack1111l1l1l1l_opy_ = config.get(bstack1111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨồ"), {})
    self.percy_capture_mode = config.get(bstack1111lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭Ổ"))
    try:
      bstack11111l11lll_opy_, bstack11111l1l1l1_opy_ = self.bstack11111ll1ll1_opy_()
      self.bstack11l1111ll11_opy_ = bstack11111l1l1l1_opy_
      bstack11111lll1ll_opy_, bstack1111l1lll11_opy_ = self.bstack11111llll1l_opy_(bstack11111l11lll_opy_, bstack11111l1l1l1_opy_)
      if bstack1111l1lll11_opy_:
        self.binary_path = bstack11111lll1ll_opy_
        thread = Thread(target=self.bstack11111l1lll1_opy_)
        thread.start()
      else:
        self.bstack1111ll111l1_opy_ = True
        self.logger.error(bstack1111lll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣổ").format(bstack11111lll1ll_opy_))
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨỖ").format(e))
  def bstack1111l11l11l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1111lll_opy_ (u"࠭࡬ࡰࡩࠪỗ"), bstack1111lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩࠪỘ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1111lll_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁࠧộ").format(logfile))
      self.bstack11111l1llll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥỚ").format(e))
  @measure(event_name=EVENTS.bstack11l1lll11ll_opy_, stage=STAGE.bstack11111lll_opy_)
  def bstack11111l1lll1_opy_(self):
    bstack11111ll1l11_opy_ = self.bstack11111ll11l1_opy_()
    if bstack11111ll1l11_opy_ == None:
      self.bstack1111ll111l1_opy_ = True
      self.logger.error(bstack1111lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨớ"))
      return False
    bstack1111l1l1lll_opy_ = [bstack1111lll_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧỜ") if self.bstack11111l11_opy_ else bstack1111lll_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩờ")]
    bstack111l1l1l1ll_opy_ = self.bstack11111l1l111_opy_()
    if bstack111l1l1l1ll_opy_ != None:
      bstack1111l1l1lll_opy_.append(bstack1111lll_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧỞ").format(bstack111l1l1l1ll_opy_))
    env = os.environ.copy()
    env[bstack1111lll_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧở")] = bstack11111ll1l11_opy_
    env[bstack1111lll_opy_ (u"ࠣࡖࡋࡣࡇ࡛ࡉࡍࡆࡢ࡙࡚ࡏࡄࠣỠ")] = os.environ.get(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧỡ"), bstack1111lll_opy_ (u"ࠪࠫỢ"))
    bstack11111l11l1l_opy_ = [self.binary_path]
    self.bstack1111l11l11l_opy_()
    self.bstack1111l1lllll_opy_ = self.bstack1111ll111ll_opy_(bstack11111l11l1l_opy_ + bstack1111l1l1lll_opy_, env)
    self.logger.debug(bstack1111lll_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧợ"))
    bstack1111l11111l_opy_ = 0
    while self.bstack1111l1lllll_opy_.poll() == None:
      bstack1111ll1111l_opy_ = self.bstack1111l11ll1l_opy_()
      if bstack1111ll1111l_opy_:
        self.logger.debug(bstack1111lll_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣỤ"))
        self.bstack1111l1l1111_opy_ = True
        return True
      bstack1111l11111l_opy_ += 1
      self.logger.debug(bstack1111lll_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤụ").format(bstack1111l11111l_opy_))
      time.sleep(2)
    self.logger.error(bstack1111lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧỦ").format(bstack1111l11111l_opy_))
    self.bstack1111ll111l1_opy_ = True
    return False
  def bstack1111l11ll1l_opy_(self, bstack1111l11111l_opy_ = 0):
    if bstack1111l11111l_opy_ > 10:
      return False
    try:
      bstack11111llll11_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨủ"), bstack1111lll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪỨ"))
      bstack1111l1ll1l1_opy_ = bstack11111llll11_opy_ + bstack11ll111111l_opy_
      response = requests.get(bstack1111l1ll1l1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࠩứ"), {}).get(bstack1111lll_opy_ (u"ࠫ࡮ࡪࠧỪ"), None)
      return True
    except:
      self.logger.debug(bstack1111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡲࡴࡩࠢࡦ࡬ࡪࡩ࡫ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥừ"))
      return False
  def bstack11111ll11l1_opy_(self):
    bstack1111l111111_opy_ = bstack1111lll_opy_ (u"࠭ࡡࡱࡲࠪỬ") if self.bstack11111l11_opy_ else bstack1111lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩử")
    bstack1111ll11111_opy_ = bstack1111lll_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦỮ") if self.config.get(bstack1111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨữ")) is None else True
    bstack11ll11ll111_opy_ = bstack1111lll_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠨࡳࡩࡷࡩࡹ࠾ࡽࢀࠦỰ").format(self.config[bstack1111lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩự")], bstack1111l111111_opy_, bstack1111ll11111_opy_)
    if self.percy_capture_mode:
      bstack11ll11ll111_opy_ += bstack1111lll_opy_ (u"ࠧࠬࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࡁࢀࢃࠢỲ").format(self.percy_capture_mode)
    uri = bstack1ll11l11l1_opy_(bstack11ll11ll111_opy_)
    try:
      response = bstack1l11l1l1_opy_(bstack1111lll_opy_ (u"࠭ࡇࡆࡖࠪỳ"), uri, {}, {bstack1111lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬỴ"): (self.config[bstack1111lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪỵ")], self.config[bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬỶ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11ll11lll1_opy_ = data.get(bstack1111lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫỷ"))
        self.percy_capture_mode = data.get(bstack1111lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦࠩỸ"))
        os.environ[bstack1111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪỹ")] = str(self.bstack11ll11lll1_opy_)
        os.environ[bstack1111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪỺ")] = str(self.percy_capture_mode)
        if bstack1111ll11111_opy_ == bstack1111lll_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥỻ") and str(self.bstack11ll11lll1_opy_).lower() == bstack1111lll_opy_ (u"ࠣࡶࡵࡹࡪࠨỼ"):
          self.bstack1lll1l11l_opy_ = True
        if bstack1111lll_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣỽ") in data:
          return data[bstack1111lll_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤỾ")]
        else:
          raise bstack1111lll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫỿ").format(data)
      else:
        raise bstack1111lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧἀ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢἁ").format(e))
  def bstack11111l1l111_opy_(self):
    bstack1111l1ll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥἂ"))
    try:
      if bstack1111lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩἃ") not in self.bstack1111l1l1l1l_opy_:
        self.bstack1111l1l1l1l_opy_[bstack1111lll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪἄ")] = 2
      with open(bstack1111l1ll11l_opy_, bstack1111lll_opy_ (u"ࠪࡻࠬἅ")) as fp:
        json.dump(self.bstack1111l1l1l1l_opy_, fp)
      return bstack1111l1ll11l_opy_
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦἆ").format(e))
  def bstack1111ll111ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111ll11ll1_opy_ == bstack1111lll_opy_ (u"ࠬࡽࡩ࡯ࠩἇ"):
        bstack1111l1l1ll1_opy_ = [bstack1111lll_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧἈ"), bstack1111lll_opy_ (u"ࠧ࠰ࡥࠪἉ")]
        cmd = bstack1111l1l1ll1_opy_ + cmd
      cmd = bstack1111lll_opy_ (u"ࠨࠢࠪἊ").join(cmd)
      self.logger.debug(bstack1111lll_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨἋ").format(cmd))
      with open(self.bstack11111l1llll_opy_, bstack1111lll_opy_ (u"ࠥࡥࠧἌ")) as bstack1111l1l11ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111l1l11ll_opy_, text=True, stderr=bstack1111l1l11ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111ll111l1_opy_ = True
      self.logger.error(bstack1111lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨἍ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111l1l1111_opy_:
        self.logger.info(bstack1111lll_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨἎ"))
        cmd = [self.binary_path, bstack1111lll_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤἏ")]
        self.bstack1111ll111ll_opy_(cmd)
        self.bstack1111l1l1111_opy_ = False
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢἐ").format(cmd, e))
  def bstack1ll1ll11_opy_(self):
    if not self.bstack11ll11lll1_opy_:
      return
    try:
      bstack1111ll11lll_opy_ = 0
      while not self.bstack1111l1l1111_opy_ and bstack1111ll11lll_opy_ < self.bstack1111l111ll1_opy_:
        if self.bstack1111ll111l1_opy_:
          self.logger.info(bstack1111lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨἑ"))
          return
        time.sleep(1)
        bstack1111ll11lll_opy_ += 1
      os.environ[bstack1111lll_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨἒ")] = str(self.bstack1111l11l1ll_opy_())
      self.logger.info(bstack1111lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦἓ"))
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧἔ").format(e))
  def bstack1111l11l1ll_opy_(self):
    if self.bstack11111l11_opy_:
      return
    try:
      bstack1111ll11l1l_opy_ = [platform[bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪἕ")].lower() for platform in self.config.get(bstack1111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ἖"), [])]
      bstack1111l1ll111_opy_ = sys.maxsize
      bstack1111l11lll1_opy_ = bstack1111lll_opy_ (u"ࠧࠨ἗")
      for browser in bstack1111ll11l1l_opy_:
        if browser in self.bstack11111lll1l1_opy_:
          bstack11111ll11ll_opy_ = self.bstack11111lll1l1_opy_[browser]
        if bstack11111ll11ll_opy_ < bstack1111l1ll111_opy_:
          bstack1111l1ll111_opy_ = bstack11111ll11ll_opy_
          bstack1111l11lll1_opy_ = browser
      return bstack1111l11lll1_opy_
    except Exception as e:
      self.logger.error(bstack1111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤἘ").format(e))
  @classmethod
  def bstack11l1ll11l1_opy_(self):
    return os.getenv(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧἙ"), bstack1111lll_opy_ (u"ࠪࡊࡦࡲࡳࡦࠩἚ")).lower()
  @classmethod
  def bstack11l1lll1_opy_(self):
    return os.getenv(bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨἛ"), bstack1111lll_opy_ (u"ࠬ࠭Ἔ"))
  @classmethod
  def bstack1l1l1l1ll1l_opy_(cls, value):
    cls.bstack1lll1l11l_opy_ = value
  @classmethod
  def bstack1111l1111l1_opy_(cls):
    return cls.bstack1lll1l11l_opy_
  @classmethod
  def bstack1l1l1l1l11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1111l11ll11_opy_(cls):
    return cls.percy_build_id