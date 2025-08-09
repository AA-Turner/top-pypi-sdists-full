# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
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
from bstack_utils.helper import bstack1l11l1l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11ll1lllll_opy_ import bstack1111l1l11_opy_
class bstack11111111_opy_:
  working_dir = os.getcwd()
  bstack1l11l11lll_opy_ = False
  config = {}
  bstack11l1111ll11_opy_ = bstack11l1_opy_ (u"ࠧࠨẠ")
  binary_path = bstack11l1_opy_ (u"ࠨࠩạ")
  bstack1111ll111ll_opy_ = bstack11l1_opy_ (u"ࠩࠪẢ")
  bstack1lllll1111_opy_ = False
  bstack1111ll1111l_opy_ = None
  bstack1111l1l1111_opy_ = {}
  bstack11111ll111l_opy_ = 300
  bstack11111ll11ll_opy_ = False
  logger = None
  bstack1111ll11lll_opy_ = False
  bstack1l1ll1l1l1_opy_ = False
  percy_build_id = None
  bstack1111l1l11l1_opy_ = bstack11l1_opy_ (u"ࠪࠫả")
  bstack1111l1ll1l1_opy_ = {
    bstack11l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫẤ") : 1,
    bstack11l1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ấ") : 2,
    bstack11l1_opy_ (u"࠭ࡥࡥࡩࡨࠫẦ") : 3,
    bstack11l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧầ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11111llll1l_opy_(self):
    bstack1111l11111l_opy_ = bstack11l1_opy_ (u"ࠨࠩẨ")
    bstack11111ll1lll_opy_ = sys.platform
    bstack1111l1l1l1l_opy_ = bstack11l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨẩ")
    if re.match(bstack11l1_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥẪ"), bstack11111ll1lll_opy_) != None:
      bstack1111l11111l_opy_ = bstack11ll11111l1_opy_ + bstack11l1_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧẫ")
      self.bstack1111l1l11l1_opy_ = bstack11l1_opy_ (u"ࠬࡳࡡࡤࠩẬ")
    elif re.match(bstack11l1_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦậ"), bstack11111ll1lll_opy_) != None:
      bstack1111l11111l_opy_ = bstack11ll11111l1_opy_ + bstack11l1_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣẮ")
      bstack1111l1l1l1l_opy_ = bstack11l1_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦắ")
      self.bstack1111l1l11l1_opy_ = bstack11l1_opy_ (u"ࠩࡺ࡭ࡳ࠭Ằ")
    else:
      bstack1111l11111l_opy_ = bstack11ll11111l1_opy_ + bstack11l1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨằ")
      self.bstack1111l1l11l1_opy_ = bstack11l1_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪẲ")
    return bstack1111l11111l_opy_, bstack1111l1l1l1l_opy_
  def bstack1111l1111ll_opy_(self):
    try:
      bstack11111lll1l1_opy_ = [os.path.join(expanduser(bstack11l1_opy_ (u"ࠧࢄࠢẳ")), bstack11l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ẵ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11111lll1l1_opy_:
        if(self.bstack1111l111111_opy_(path)):
          return path
      raise bstack11l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦẵ")
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥẶ").format(e))
  def bstack1111l111111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111ll1l1ll_opy_(self, bstack1111ll11ll1_opy_):
    return os.path.join(bstack1111ll11ll1_opy_, self.bstack11l1111ll11_opy_ + bstack11l1_opy_ (u"ࠤ࠱ࡩࡹࡧࡧࠣặ"))
  def bstack1111l11l1l1_opy_(self, bstack1111ll11ll1_opy_, bstack1111l1ll111_opy_):
    if not bstack1111l1ll111_opy_: return
    try:
      bstack11111lll1ll_opy_ = self.bstack1111ll1l1ll_opy_(bstack1111ll11ll1_opy_)
      with open(bstack11111lll1ll_opy_, bstack11l1_opy_ (u"ࠥࡻࠧẸ")) as f:
        f.write(bstack1111l1ll111_opy_)
        self.logger.debug(bstack11l1_opy_ (u"ࠦࡘࡧࡶࡦࡦࠣࡲࡪࡽࠠࡆࡖࡤ࡫ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠣẹ"))
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡴࡩࡧࠣࡩࡹࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧẺ").format(e))
  def bstack1111l111l11_opy_(self, bstack1111ll11ll1_opy_):
    try:
      bstack11111lll1ll_opy_ = self.bstack1111ll1l1ll_opy_(bstack1111ll11ll1_opy_)
      if os.path.exists(bstack11111lll1ll_opy_):
        with open(bstack11111lll1ll_opy_, bstack11l1_opy_ (u"ࠨࡲࠣẻ")) as f:
          bstack1111l1ll111_opy_ = f.read().strip()
          return bstack1111l1ll111_opy_ if bstack1111l1ll111_opy_ else None
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠ࡭ࡱࡤࡨ࡮ࡴࡧࠡࡇࡗࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥẼ").format(e))
  def bstack11111llllll_opy_(self, bstack1111ll11ll1_opy_, bstack1111l11111l_opy_):
    bstack1111l1ll1ll_opy_ = self.bstack1111l111l11_opy_(bstack1111ll11ll1_opy_)
    if bstack1111l1ll1ll_opy_:
      try:
        bstack11111lll11l_opy_ = self.bstack11111lllll1_opy_(bstack1111l1ll1ll_opy_, bstack1111l11111l_opy_)
        if not bstack11111lll11l_opy_:
          self.logger.debug(bstack11l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡵࠣࡹࡵࠦࡴࡰࠢࡧࡥࡹ࡫ࠠࠩࡇࡗࡥ࡬ࠦࡵ࡯ࡥ࡫ࡥࡳ࡭ࡥࡥࠫࠥẽ"))
          return True
        self.logger.debug(bstack11l1_opy_ (u"ࠤࡑࡩࡼࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡥࠣẾ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡬࡯ࡳࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤế").format(e))
    return False
  def bstack11111lllll1_opy_(self, bstack1111l1ll1ll_opy_, bstack1111l11111l_opy_):
    try:
      headers = {
        bstack11l1_opy_ (u"ࠦࡎ࡬࠭ࡏࡱࡱࡩ࠲ࡓࡡࡵࡥ࡫ࠦỀ"): bstack1111l1ll1ll_opy_
      }
      response = bstack1l11l1l1l1_opy_(bstack11l1_opy_ (u"ࠬࡍࡅࡕࠩề"), bstack1111l11111l_opy_, {}, {bstack11l1_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢỂ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠿ࠦࡻࡾࠤể").format(e))
  @measure(event_name=EVENTS.bstack11l1lll1l11_opy_, stage=STAGE.bstack11lll1l1_opy_)
  def bstack1111ll111l1_opy_(self, bstack1111l11111l_opy_, bstack1111l1l1l1l_opy_):
    try:
      bstack11111lll111_opy_ = self.bstack1111l1111ll_opy_()
      bstack1111ll1lll1_opy_ = os.path.join(bstack11111lll111_opy_, bstack11l1_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫỄ"))
      bstack11111ll1ll1_opy_ = os.path.join(bstack11111lll111_opy_, bstack1111l1l1l1l_opy_)
      if self.bstack11111llllll_opy_(bstack11111lll111_opy_, bstack1111l11111l_opy_): # if bstack1111ll1llll_opy_, bstack1l1l11l1l1l_opy_ bstack1111l1ll111_opy_ is bstack1111l1ll11l_opy_ to bstack11l111llll1_opy_ version available (response 304)
        if os.path.exists(bstack11111ll1ll1_opy_):
          self.logger.info(bstack11l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦễ").format(bstack11111ll1ll1_opy_))
          return bstack11111ll1ll1_opy_
        if os.path.exists(bstack1111ll1lll1_opy_):
          self.logger.info(bstack11l1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣỆ").format(bstack1111ll1lll1_opy_))
          return self.bstack1111ll1l11l_opy_(bstack1111ll1lll1_opy_, bstack1111l1l1l1l_opy_)
      self.logger.info(bstack11l1_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤệ").format(bstack1111l11111l_opy_))
      response = bstack1l11l1l1l1_opy_(bstack11l1_opy_ (u"ࠬࡍࡅࡕࠩỈ"), bstack1111l11111l_opy_, {}, {})
      if response.status_code == 200:
        bstack1111ll11l1l_opy_ = response.headers.get(bstack11l1_opy_ (u"ࠨࡅࡕࡣࡪࠦỉ"), bstack11l1_opy_ (u"ࠢࠣỊ"))
        if bstack1111ll11l1l_opy_:
          self.bstack1111l11l1l1_opy_(bstack11111lll111_opy_, bstack1111ll11l1l_opy_)
        with open(bstack1111ll1lll1_opy_, bstack11l1_opy_ (u"ࠨࡹࡥࠫị")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢỌ").format(bstack1111ll1lll1_opy_))
        return self.bstack1111ll1l11l_opy_(bstack1111ll1lll1_opy_, bstack1111l1l1l1l_opy_)
      else:
        raise(bstack11l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨọ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧỎ").format(e))
  def bstack1111l1l111l_opy_(self, bstack1111l11111l_opy_, bstack1111l1l1l1l_opy_):
    try:
      retry = 2
      bstack11111ll1ll1_opy_ = None
      bstack1111l1l1ll1_opy_ = False
      while retry > 0:
        bstack11111ll1ll1_opy_ = self.bstack1111ll111l1_opy_(bstack1111l11111l_opy_, bstack1111l1l1l1l_opy_)
        bstack1111l1l1ll1_opy_ = self.bstack11111ll1l1l_opy_(bstack1111l11111l_opy_, bstack1111l1l1l1l_opy_, bstack11111ll1ll1_opy_)
        if bstack1111l1l1ll1_opy_:
          break
        retry -= 1
      return bstack11111ll1ll1_opy_, bstack1111l1l1ll1_opy_
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤỏ").format(e))
    return bstack11111ll1ll1_opy_, False
  def bstack11111ll1l1l_opy_(self, bstack1111l11111l_opy_, bstack1111l1l1l1l_opy_, bstack11111ll1ll1_opy_, bstack1111l1l11ll_opy_ = 0):
    if bstack1111l1l11ll_opy_ > 1:
      return False
    if bstack11111ll1ll1_opy_ == None or os.path.exists(bstack11111ll1ll1_opy_) == False:
      self.logger.warn(bstack11l1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦỐ"))
      return False
    bstack1111lll1111_opy_ = bstack11l1_opy_ (u"ࡲࠣࡠ࠱࠮ࡅࡶࡥࡳࡥࡼ࠳ࡨࡲࡩࠡ࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭࡟࠲ࡡࡪࠫࠣố")
    command = bstack11l1_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧỒ").format(bstack11111ll1ll1_opy_)
    bstack1111ll11l11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111lll1111_opy_, bstack1111ll11l11_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣồ"))
      return False
  def bstack1111ll1l11l_opy_(self, bstack1111ll1lll1_opy_, bstack1111l1l1l1l_opy_):
    try:
      working_dir = os.path.dirname(bstack1111ll1lll1_opy_)
      shutil.unpack_archive(bstack1111ll1lll1_opy_, working_dir)
      bstack11111ll1ll1_opy_ = os.path.join(working_dir, bstack1111l1l1l1l_opy_)
      os.chmod(bstack11111ll1ll1_opy_, 0o755)
      return bstack11111ll1ll1_opy_
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦỔ"))
  def bstack1111l11ll11_opy_(self):
    try:
      bstack1111l1lllll_opy_ = self.config.get(bstack11l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪổ"))
      bstack1111l11ll11_opy_ = bstack1111l1lllll_opy_ or (bstack1111l1lllll_opy_ is None and self.bstack1l11l11lll_opy_)
      if not bstack1111l11ll11_opy_ or self.config.get(bstack11l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨỖ"), None) not in bstack11l1lllll11_opy_:
        return False
      self.bstack1lllll1111_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣỗ").format(e))
  def bstack11111llll11_opy_(self):
    try:
      bstack11111llll11_opy_ = self.percy_capture_mode
      return bstack11111llll11_opy_
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣỘ").format(e))
  def init(self, bstack1l11l11lll_opy_, config, logger):
    self.bstack1l11l11lll_opy_ = bstack1l11l11lll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111l11ll11_opy_():
      return
    self.bstack1111l1l1111_opy_ = config.get(bstack11l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧộ"), {})
    self.percy_capture_mode = config.get(bstack11l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬỚ"))
    try:
      bstack1111l11111l_opy_, bstack1111l1l1l1l_opy_ = self.bstack11111llll1l_opy_()
      self.bstack11l1111ll11_opy_ = bstack1111l1l1l1l_opy_
      bstack11111ll1ll1_opy_, bstack1111l1l1ll1_opy_ = self.bstack1111l1l111l_opy_(bstack1111l11111l_opy_, bstack1111l1l1l1l_opy_)
      if bstack1111l1l1ll1_opy_:
        self.binary_path = bstack11111ll1ll1_opy_
        thread = Thread(target=self.bstack1111ll11111_opy_)
        thread.start()
      else:
        self.bstack1111ll11lll_opy_ = True
        self.logger.error(bstack11l1_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢớ").format(bstack11111ll1ll1_opy_))
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧỜ").format(e))
  def bstack1111lll111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1_opy_ (u"ࠬࡲ࡯ࡨࠩờ"), bstack11l1_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩỞ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦở").format(logfile))
      self.bstack1111ll111ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤỠ").format(e))
  @measure(event_name=EVENTS.bstack11l1ll1l11l_opy_, stage=STAGE.bstack11lll1l1_opy_)
  def bstack1111ll11111_opy_(self):
    bstack1111l11l1ll_opy_ = self.bstack1111ll1ll11_opy_()
    if bstack1111l11l1ll_opy_ == None:
      self.bstack1111ll11lll_opy_ = True
      self.logger.error(bstack11l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧỡ"))
      return False
    bstack1111l1l1l11_opy_ = [bstack11l1_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦỢ") if self.bstack1l11l11lll_opy_ else bstack11l1_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨợ")]
    bstack111ll1111l1_opy_ = self.bstack1111ll1l1l1_opy_()
    if bstack111ll1111l1_opy_ != None:
      bstack1111l1l1l11_opy_.append(bstack11l1_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦỤ").format(bstack111ll1111l1_opy_))
    env = os.environ.copy()
    env[bstack11l1_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦụ")] = bstack1111l11l1ll_opy_
    env[bstack11l1_opy_ (u"ࠢࡕࡊࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠢỦ")] = os.environ.get(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ủ"), bstack11l1_opy_ (u"ࠩࠪỨ"))
    bstack11111ll1l11_opy_ = [self.binary_path]
    self.bstack1111lll111l_opy_()
    self.bstack1111ll1111l_opy_ = self.bstack1111l11lll1_opy_(bstack11111ll1l11_opy_ + bstack1111l1l1l11_opy_, env)
    self.logger.debug(bstack11l1_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦứ"))
    bstack1111l1l11ll_opy_ = 0
    while self.bstack1111ll1111l_opy_.poll() == None:
      bstack1111l11llll_opy_ = self.bstack1111l11l111_opy_()
      if bstack1111l11llll_opy_:
        self.logger.debug(bstack11l1_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢỪ"))
        self.bstack11111ll11ll_opy_ = True
        return True
      bstack1111l1l11ll_opy_ += 1
      self.logger.debug(bstack11l1_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣừ").format(bstack1111l1l11ll_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦỬ").format(bstack1111l1l11ll_opy_))
    self.bstack1111ll11lll_opy_ = True
    return False
  def bstack1111l11l111_opy_(self, bstack1111l1l11ll_opy_ = 0):
    if bstack1111l1l11ll_opy_ > 10:
      return False
    try:
      bstack1111l1llll1_opy_ = os.environ.get(bstack11l1_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧử"), bstack11l1_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩỮ"))
      bstack1111l1lll1l_opy_ = bstack1111l1llll1_opy_ + bstack11l1ll1ll11_opy_
      response = requests.get(bstack1111l1lll1l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨữ"), {}).get(bstack11l1_opy_ (u"ࠪ࡭ࡩ࠭Ự"), None)
      return True
    except:
      self.logger.debug(bstack11l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡪࡨࡥࡱࡺࡨࠡࡥ࡫ࡩࡨࡱࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤự"))
      return False
  def bstack1111ll1ll11_opy_(self):
    bstack1111l111ll1_opy_ = bstack11l1_opy_ (u"ࠬࡧࡰࡱࠩỲ") if self.bstack1l11l11lll_opy_ else bstack11l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨỳ")
    bstack1111l1l1lll_opy_ = bstack11l1_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥỴ") if self.config.get(bstack11l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧỵ")) is None else True
    bstack11ll11ll11l_opy_ = bstack11l1_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠧࡲࡨࡶࡨࡿ࠽ࡼࡿࠥỶ").format(self.config[bstack11l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨỷ")], bstack1111l111ll1_opy_, bstack1111l1l1lll_opy_)
    if self.percy_capture_mode:
      bstack11ll11ll11l_opy_ += bstack11l1_opy_ (u"ࠦࠫࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࡀࡿࢂࠨỸ").format(self.percy_capture_mode)
    uri = bstack1111l1l11_opy_(bstack11ll11ll11l_opy_)
    try:
      response = bstack1l11l1l1l1_opy_(bstack11l1_opy_ (u"ࠬࡍࡅࡕࠩỹ"), uri, {}, {bstack11l1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫỺ"): (self.config[bstack11l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩỻ")], self.config[bstack11l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫỼ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1lllll1111_opy_ = data.get(bstack11l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪỽ"))
        self.percy_capture_mode = data.get(bstack11l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥࠨỾ"))
        os.environ[bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩỿ")] = str(self.bstack1lllll1111_opy_)
        os.environ[bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩἀ")] = str(self.percy_capture_mode)
        if bstack1111l1l1lll_opy_ == bstack11l1_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤἁ") and str(self.bstack1lllll1111_opy_).lower() == bstack11l1_opy_ (u"ࠢࡵࡴࡸࡩࠧἂ"):
          self.bstack1l1ll1l1l1_opy_ = True
        if bstack11l1_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢἃ") in data:
          return data[bstack11l1_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣἄ")]
        else:
          raise bstack11l1_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪἅ").format(data)
      else:
        raise bstack11l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦἆ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨἇ").format(e))
  def bstack1111ll1l1l1_opy_(self):
    bstack1111l1lll11_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤἈ"))
    try:
      if bstack11l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨἉ") not in self.bstack1111l1l1111_opy_:
        self.bstack1111l1l1111_opy_[bstack11l1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩἊ")] = 2
      with open(bstack1111l1lll11_opy_, bstack11l1_opy_ (u"ࠩࡺࠫἋ")) as fp:
        json.dump(self.bstack1111l1l1111_opy_, fp)
      return bstack1111l1lll11_opy_
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥἌ").format(e))
  def bstack1111l11lll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111l1l11l1_opy_ == bstack11l1_opy_ (u"ࠫࡼ࡯࡮ࠨἍ"):
        bstack11111ll1111_opy_ = [bstack11l1_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭Ἆ"), bstack11l1_opy_ (u"࠭࠯ࡤࠩἏ")]
        cmd = bstack11111ll1111_opy_ + cmd
      cmd = bstack11l1_opy_ (u"ࠧࠡࠩἐ").join(cmd)
      self.logger.debug(bstack11l1_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧἑ").format(cmd))
      with open(self.bstack1111ll111ll_opy_, bstack11l1_opy_ (u"ࠤࡤࠦἒ")) as bstack1111lll11l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111lll11l1_opy_, text=True, stderr=bstack1111lll11l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111ll11lll_opy_ = True
      self.logger.error(bstack11l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧἓ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11111ll11ll_opy_:
        self.logger.info(bstack11l1_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧἔ"))
        cmd = [self.binary_path, bstack11l1_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣἕ")]
        self.bstack1111l11lll1_opy_(cmd)
        self.bstack11111ll11ll_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ἖").format(cmd, e))
  def bstack11lll1ll1l_opy_(self):
    if not self.bstack1lllll1111_opy_:
      return
    try:
      bstack1111l1111l1_opy_ = 0
      while not self.bstack11111ll11ll_opy_ and bstack1111l1111l1_opy_ < self.bstack11111ll111l_opy_:
        if self.bstack1111ll11lll_opy_:
          self.logger.info(bstack11l1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧ἗"))
          return
        time.sleep(1)
        bstack1111l1111l1_opy_ += 1
      os.environ[bstack11l1_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧἘ")] = str(self.bstack11111ll11l1_opy_())
      self.logger.info(bstack11l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥἙ"))
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦἚ").format(e))
  def bstack11111ll11l1_opy_(self):
    if self.bstack1l11l11lll_opy_:
      return
    try:
      bstack1111l11ll1l_opy_ = [platform[bstack11l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩἛ")].lower() for platform in self.config.get(bstack11l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨἜ"), [])]
      bstack1111ll1ll1l_opy_ = sys.maxsize
      bstack1111l111l1l_opy_ = bstack11l1_opy_ (u"࠭ࠧἝ")
      for browser in bstack1111l11ll1l_opy_:
        if browser in self.bstack1111l1ll1l1_opy_:
          bstack1111l11l11l_opy_ = self.bstack1111l1ll1l1_opy_[browser]
        if bstack1111l11l11l_opy_ < bstack1111ll1ll1l_opy_:
          bstack1111ll1ll1l_opy_ = bstack1111l11l11l_opy_
          bstack1111l111l1l_opy_ = browser
      return bstack1111l111l1l_opy_
    except Exception as e:
      self.logger.error(bstack11l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ἞").format(e))
  @classmethod
  def bstack11lll1l11_opy_(self):
    return os.getenv(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭἟"), bstack11l1_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨἠ")).lower()
  @classmethod
  def bstack1111llll1_opy_(self):
    return os.getenv(bstack11l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧἡ"), bstack11l1_opy_ (u"ࠫࠬἢ"))
  @classmethod
  def bstack1l1l1l1ll1l_opy_(cls, value):
    cls.bstack1l1ll1l1l1_opy_ = value
  @classmethod
  def bstack1111ll1l111_opy_(cls):
    return cls.bstack1l1ll1l1l1_opy_
  @classmethod
  def bstack1l1l1l11l1l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1111l111lll_opy_(cls):
    return cls.percy_build_id