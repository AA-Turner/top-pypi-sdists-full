# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
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
from bstack_utils.helper import bstack1lllll1111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1l1lll11l_opy_ import bstack11ll11111_opy_
class bstack11ll1l1111_opy_:
  working_dir = os.getcwd()
  bstack11ll11ll1l_opy_ = False
  config = {}
  bstack11l11l1l1ll_opy_ = bstack1ll11ll_opy_ (u"ࠪࠫả")
  binary_path = bstack1ll11ll_opy_ (u"ࠫࠬẤ")
  bstack11111l1l1ll_opy_ = bstack1ll11ll_opy_ (u"ࠬ࠭ấ")
  bstack11ll1111l_opy_ = False
  bstack111111llll1_opy_ = None
  bstack1111l11l1ll_opy_ = {}
  bstack111111ll1ll_opy_ = 300
  bstack1111l1111l1_opy_ = False
  logger = None
  bstack11111l1l11l_opy_ = False
  bstack11l11l1lll_opy_ = False
  percy_build_id = None
  bstack111111ll111_opy_ = bstack1ll11ll_opy_ (u"࠭ࠧẦ")
  bstack111111l1lll_opy_ = {
    bstack1ll11ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧầ") : 1,
    bstack1ll11ll_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩẨ") : 2,
    bstack1ll11ll_opy_ (u"ࠩࡨࡨ࡬࡫ࠧẩ") : 3,
    bstack1ll11ll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪẪ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1111l11ll1l_opy_(self):
    bstack11111l1llll_opy_ = bstack1ll11ll_opy_ (u"ࠫࠬẫ")
    bstack11111l1lll1_opy_ = sys.platform
    bstack11111l1ll1l_opy_ = bstack1ll11ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫẬ")
    if re.match(bstack1ll11ll_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨậ"), bstack11111l1lll1_opy_) != None:
      bstack11111l1llll_opy_ = bstack11l1ll11l11_opy_ + bstack1ll11ll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣẮ")
      self.bstack111111ll111_opy_ = bstack1ll11ll_opy_ (u"ࠨ࡯ࡤࡧࠬắ")
    elif re.match(bstack1ll11ll_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢẰ"), bstack11111l1lll1_opy_) != None:
      bstack11111l1llll_opy_ = bstack11l1ll11l11_opy_ + bstack1ll11ll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦằ")
      bstack11111l1ll1l_opy_ = bstack1ll11ll_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢẲ")
      self.bstack111111ll111_opy_ = bstack1ll11ll_opy_ (u"ࠬࡽࡩ࡯ࠩẳ")
    else:
      bstack11111l1llll_opy_ = bstack11l1ll11l11_opy_ + bstack1ll11ll_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤẴ")
      self.bstack111111ll111_opy_ = bstack1ll11ll_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ẵ")
    return bstack11111l1llll_opy_, bstack11111l1ll1l_opy_
  def bstack111111lll11_opy_(self):
    try:
      bstack1111l1l111l_opy_ = [os.path.join(expanduser(bstack1ll11ll_opy_ (u"ࠣࢀࠥẶ")), bstack1ll11ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩặ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111l1l111l_opy_:
        if(self.bstack111111l1l11_opy_(path)):
          return path
      raise bstack1ll11ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢẸ")
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨẹ").format(e))
  def bstack111111l1l11_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111l11l1l1_opy_(self, bstack111111ll1l1_opy_):
    return os.path.join(bstack111111ll1l1_opy_, self.bstack11l11l1l1ll_opy_ + bstack1ll11ll_opy_ (u"ࠧ࠴ࡥࡵࡣࡪࠦẺ"))
  def bstack1111l1l1ll1_opy_(self, bstack111111ll1l1_opy_, bstack11111ll11l1_opy_):
    if not bstack11111ll11l1_opy_: return
    try:
      bstack11111l11l11_opy_ = self.bstack1111l11l1l1_opy_(bstack111111ll1l1_opy_)
      with open(bstack11111l11l11_opy_, bstack1ll11ll_opy_ (u"ࠨࡷࠣẻ")) as f:
        f.write(bstack11111ll11l1_opy_)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡔࡣࡹࡩࡩࠦ࡮ࡦࡹࠣࡉ࡙ࡧࡧࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠦẼ"))
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡷ࡬ࡪࠦࡥࡵࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣẽ").format(e))
  def bstack111111lllll_opy_(self, bstack111111ll1l1_opy_):
    try:
      bstack11111l11l11_opy_ = self.bstack1111l11l1l1_opy_(bstack111111ll1l1_opy_)
      if os.path.exists(bstack11111l11l11_opy_):
        with open(bstack11111l11l11_opy_, bstack1ll11ll_opy_ (u"ࠤࡵࠦẾ")) as f:
          bstack11111ll11l1_opy_ = f.read().strip()
          return bstack11111ll11l1_opy_ if bstack11111ll11l1_opy_ else None
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡰࡴࡧࡤࡪࡰࡪࠤࡊ࡚ࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨế").format(e))
  def bstack11111lll1l1_opy_(self, bstack111111ll1l1_opy_, bstack11111l1llll_opy_):
    bstack1111l1l11l1_opy_ = self.bstack111111lllll_opy_(bstack111111ll1l1_opy_)
    if bstack1111l1l11l1_opy_:
      try:
        bstack1111l111lll_opy_ = self.bstack1111l11lll1_opy_(bstack1111l1l11l1_opy_, bstack11111l1llll_opy_)
        if not bstack1111l111lll_opy_:
          self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡸࠦࡵࡱࠢࡷࡳࠥࡪࡡࡵࡧࠣࠬࡊ࡚ࡡࡨࠢࡸࡲࡨ࡮ࡡ࡯ࡩࡨࡨ࠮ࠨỀ"))
          return True
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡔࡥࡸࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡺࡶࡤࡢࡶࡨࠦề"))
        return False
      except Exception as e:
        self.logger.warn(bstack1ll11ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡲࡶࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧỂ").format(e))
    return False
  def bstack1111l11lll1_opy_(self, bstack1111l1l11l1_opy_, bstack11111l1llll_opy_):
    try:
      headers = {
        bstack1ll11ll_opy_ (u"ࠢࡊࡨ࠰ࡒࡴࡴࡥ࠮ࡏࡤࡸࡨ࡮ࠢể"): bstack1111l1l11l1_opy_
      }
      response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠨࡉࡈࡘࠬỄ"), bstack11111l1llll_opy_, {}, {bstack1ll11ll_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥễ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1ll11ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠻ࠢࡾࢁࠧỆ").format(e))
  @measure(event_name=EVENTS.bstack11l1lll11l1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
  def bstack11111l11l1l_opy_(self, bstack11111l1llll_opy_, bstack11111l1ll1l_opy_):
    try:
      bstack1111l111l11_opy_ = self.bstack111111lll11_opy_()
      bstack1111l1l11ll_opy_ = os.path.join(bstack1111l111l11_opy_, bstack1ll11ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧệ"))
      bstack11111ll111l_opy_ = os.path.join(bstack1111l111l11_opy_, bstack11111l1ll1l_opy_)
      if self.bstack11111lll1l1_opy_(bstack1111l111l11_opy_, bstack11111l1llll_opy_): # if bstack1111l11llll_opy_, bstack1l1l111llll_opy_ bstack11111ll11l1_opy_ is bstack1111l11111l_opy_ to bstack11l11l11lll_opy_ version available (response 304)
        if os.path.exists(bstack11111ll111l_opy_):
          self.logger.info(bstack1ll11ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢỈ").format(bstack11111ll111l_opy_))
          return bstack11111ll111l_opy_
        if os.path.exists(bstack1111l1l11ll_opy_):
          self.logger.info(bstack1ll11ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦỉ").format(bstack1111l1l11ll_opy_))
          return self.bstack11111l11ll1_opy_(bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_)
      self.logger.info(bstack1ll11ll_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧỊ").format(bstack11111l1llll_opy_))
      response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠨࡉࡈࡘࠬị"), bstack11111l1llll_opy_, {}, {})
      if response.status_code == 200:
        bstack11111l1l1l1_opy_ = response.headers.get(bstack1ll11ll_opy_ (u"ࠤࡈࡘࡦ࡭ࠢỌ"), bstack1ll11ll_opy_ (u"ࠥࠦọ"))
        if bstack11111l1l1l1_opy_:
          self.bstack1111l1l1ll1_opy_(bstack1111l111l11_opy_, bstack11111l1l1l1_opy_)
        with open(bstack1111l1l11ll_opy_, bstack1ll11ll_opy_ (u"ࠫࡼࡨࠧỎ")) as file:
          file.write(response.content)
        self.logger.info(bstack1ll11ll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥỏ").format(bstack1111l1l11ll_opy_))
        return self.bstack11111l11ll1_opy_(bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_)
      else:
        raise(bstack1ll11ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤỐ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣố").format(e))
  def bstack111111ll11l_opy_(self, bstack11111l1llll_opy_, bstack11111l1ll1l_opy_):
    try:
      retry = 2
      bstack11111ll111l_opy_ = None
      bstack11111lll111_opy_ = False
      while retry > 0:
        bstack11111ll111l_opy_ = self.bstack11111l11l1l_opy_(bstack11111l1llll_opy_, bstack11111l1ll1l_opy_)
        bstack11111lll111_opy_ = self.bstack11111lll1ll_opy_(bstack11111l1llll_opy_, bstack11111l1ll1l_opy_, bstack11111ll111l_opy_)
        if bstack11111lll111_opy_:
          break
        retry -= 1
      return bstack11111ll111l_opy_, bstack11111lll111_opy_
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧỒ").format(e))
    return bstack11111ll111l_opy_, False
  def bstack11111lll1ll_opy_(self, bstack11111l1llll_opy_, bstack11111l1ll1l_opy_, bstack11111ll111l_opy_, bstack11111ll1ll1_opy_ = 0):
    if bstack11111ll1ll1_opy_ > 1:
      return False
    if bstack11111ll111l_opy_ == None or os.path.exists(bstack11111ll111l_opy_) == False:
      self.logger.warn(bstack1ll11ll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢồ"))
      return False
    bstack1111l1111ll_opy_ = bstack1ll11ll_opy_ (u"ࡵࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬ࠤࡡࡪࠫ࡝࠰࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࠦỔ")
    command = bstack1ll11ll_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪổ").format(bstack11111ll111l_opy_)
    bstack11111l11lll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111l1111ll_opy_, bstack11111l11lll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦỖ"))
      return False
  def bstack11111l11ll1_opy_(self, bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_):
    try:
      working_dir = os.path.dirname(bstack1111l1l11ll_opy_)
      shutil.unpack_archive(bstack1111l1l11ll_opy_, working_dir)
      bstack11111ll111l_opy_ = os.path.join(working_dir, bstack11111l1ll1l_opy_)
      os.chmod(bstack11111ll111l_opy_, 0o755)
      return bstack11111ll111l_opy_
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢỗ"))
  def bstack1111l11l11l_opy_(self):
    try:
      bstack11111l1l111_opy_ = self.config.get(bstack1ll11ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ộ"))
      bstack1111l11l11l_opy_ = bstack11111l1l111_opy_ or (bstack11111l1l111_opy_ is None and self.bstack11ll11ll1l_opy_)
      if not bstack1111l11l11l_opy_ or self.config.get(bstack1ll11ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫộ"), None) not in bstack11l1l1lll1l_opy_:
        return False
      self.bstack11ll1111l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦỚ").format(e))
  def bstack111111lll1l_opy_(self):
    try:
      bstack111111lll1l_opy_ = self.percy_capture_mode
      return bstack111111lll1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦớ").format(e))
  def init(self, bstack11ll11ll1l_opy_, config, logger):
    self.bstack11ll11ll1l_opy_ = bstack11ll11ll1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111l11l11l_opy_():
      return
    self.bstack1111l11l1ll_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪỜ"), {})
    self.percy_capture_mode = config.get(bstack1ll11ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨờ"))
    try:
      bstack11111l1llll_opy_, bstack11111l1ll1l_opy_ = self.bstack1111l11ll1l_opy_()
      self.bstack11l11l1l1ll_opy_ = bstack11111l1ll1l_opy_
      bstack11111ll111l_opy_, bstack11111lll111_opy_ = self.bstack111111ll11l_opy_(bstack11111l1llll_opy_, bstack11111l1ll1l_opy_)
      if bstack11111lll111_opy_:
        self.binary_path = bstack11111ll111l_opy_
        thread = Thread(target=self.bstack11111llllll_opy_)
        thread.start()
      else:
        self.bstack11111l1l11l_opy_ = True
        self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥỞ").format(bstack11111ll111l_opy_))
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣở").format(e))
  def bstack11111ll1l11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll11ll_opy_ (u"ࠨ࡮ࡲ࡫ࠬỠ"), bstack1ll11ll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬỡ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢỢ").format(logfile))
      self.bstack11111l1l1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧợ").format(e))
  @measure(event_name=EVENTS.bstack11l1l1l1ll1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
  def bstack11111llllll_opy_(self):
    bstack1111l1l1l11_opy_ = self.bstack1111l1l1l1l_opy_()
    if bstack1111l1l1l11_opy_ == None:
      self.bstack11111l1l11l_opy_ = True
      self.logger.error(bstack1ll11ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣỤ"))
      return False
    bstack11111ll11ll_opy_ = [bstack1ll11ll_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢụ") if self.bstack11ll11ll1l_opy_ else bstack1ll11ll_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫỦ")]
    bstack111l1l1l1l1_opy_ = self.bstack1111l1l1111_opy_()
    if bstack111l1l1l1l1_opy_ != None:
      bstack11111ll11ll_opy_.append(bstack1ll11ll_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢủ").format(bstack111l1l1l1l1_opy_))
    env = os.environ.copy()
    env[bstack1ll11ll_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢỨ")] = bstack1111l1l1l11_opy_
    env[bstack1ll11ll_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥứ")] = os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩỪ"), bstack1ll11ll_opy_ (u"ࠬ࠭ừ"))
    bstack111111l1ll1_opy_ = [self.binary_path]
    self.bstack11111ll1l11_opy_()
    self.bstack111111llll1_opy_ = self.bstack11111ll1111_opy_(bstack111111l1ll1_opy_ + bstack11111ll11ll_opy_, env)
    self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢỬ"))
    bstack11111ll1ll1_opy_ = 0
    while self.bstack111111llll1_opy_.poll() == None:
      bstack11111ll1lll_opy_ = self.bstack1111l111111_opy_()
      if bstack11111ll1lll_opy_:
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥử"))
        self.bstack1111l1111l1_opy_ = True
        return True
      bstack11111ll1ll1_opy_ += 1
      self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦỮ").format(bstack11111ll1ll1_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢữ").format(bstack11111ll1ll1_opy_))
    self.bstack11111l1l11l_opy_ = True
    return False
  def bstack1111l111111_opy_(self, bstack11111ll1ll1_opy_ = 0):
    if bstack11111ll1ll1_opy_ > 10:
      return False
    try:
      bstack1111l111ll1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪỰ"), bstack1ll11ll_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬự"))
      bstack11111lll11l_opy_ = bstack1111l111ll1_opy_ + bstack11l1l1l111l_opy_
      response = requests.get(bstack11111lll11l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫỲ"), {}).get(bstack1ll11ll_opy_ (u"࠭ࡩࡥࠩỳ"), None)
      return True
    except:
      self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧỴ"))
      return False
  def bstack1111l1l1l1l_opy_(self):
    bstack11111lllll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡣࡳࡴࠬỵ") if self.bstack11ll11ll1l_opy_ else bstack1ll11ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫỶ")
    bstack1111l11l111_opy_ = bstack1ll11ll_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨỷ") if self.config.get(bstack1ll11ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪỸ")) is None else True
    bstack11ll1111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨỹ").format(self.config[bstack1ll11ll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫỺ")], bstack11111lllll1_opy_, bstack1111l11l111_opy_)
    if self.percy_capture_mode:
      bstack11ll1111ll1_opy_ += bstack1ll11ll_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤỻ").format(self.percy_capture_mode)
    uri = bstack11ll11111_opy_(bstack11ll1111ll1_opy_)
    try:
      response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠨࡉࡈࡘࠬỼ"), uri, {}, {bstack1ll11ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧỽ"): (self.config[bstack1ll11ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬỾ")], self.config[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧỿ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11ll1111l_opy_ = data.get(bstack1ll11ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ἀ"))
        self.percy_capture_mode = data.get(bstack1ll11ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫἁ"))
        os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬἂ")] = str(self.bstack11ll1111l_opy_)
        os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬἃ")] = str(self.percy_capture_mode)
        if bstack1111l11l111_opy_ == bstack1ll11ll_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧἄ") and str(self.bstack11ll1111l_opy_).lower() == bstack1ll11ll_opy_ (u"ࠥࡸࡷࡻࡥࠣἅ"):
          self.bstack11l11l1lll_opy_ = True
        if bstack1ll11ll_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥἆ") in data:
          return data[bstack1ll11ll_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦἇ")]
        else:
          raise bstack1ll11ll_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭Ἀ").format(data)
      else:
        raise bstack1ll11ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢἉ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤἊ").format(e))
  def bstack1111l1l1111_opy_(self):
    bstack11111l1ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧἋ"))
    try:
      if bstack1ll11ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫἌ") not in self.bstack1111l11l1ll_opy_:
        self.bstack1111l11l1ll_opy_[bstack1ll11ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬἍ")] = 2
      with open(bstack11111l1ll11_opy_, bstack1ll11ll_opy_ (u"ࠬࡽࠧἎ")) as fp:
        json.dump(self.bstack1111l11l1ll_opy_, fp)
      return bstack11111l1ll11_opy_
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨἏ").format(e))
  def bstack11111ll1111_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111111ll111_opy_ == bstack1ll11ll_opy_ (u"ࠧࡸ࡫ࡱࠫἐ"):
        bstack11111ll1l1l_opy_ = [bstack1ll11ll_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩἑ"), bstack1ll11ll_opy_ (u"ࠩ࠲ࡧࠬἒ")]
        cmd = bstack11111ll1l1l_opy_ + cmd
      cmd = bstack1ll11ll_opy_ (u"ࠪࠤࠬἓ").join(cmd)
      self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣἔ").format(cmd))
      with open(self.bstack11111l1l1ll_opy_, bstack1ll11ll_opy_ (u"ࠧࡧࠢἕ")) as bstack1111l111l1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111l111l1l_opy_, text=True, stderr=bstack1111l111l1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11111l1l11l_opy_ = True
      self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ἖").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111l1111l1_opy_:
        self.logger.info(bstack1ll11ll_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣ἗"))
        cmd = [self.binary_path, bstack1ll11ll_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦἘ")]
        self.bstack11111ll1111_opy_(cmd)
        self.bstack1111l1111l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤἙ").format(cmd, e))
  def bstack1l1ll11l1_opy_(self):
    if not self.bstack11ll1111l_opy_:
      return
    try:
      bstack1111l11ll11_opy_ = 0
      while not self.bstack1111l1111l1_opy_ and bstack1111l11ll11_opy_ < self.bstack111111ll1ll_opy_:
        if self.bstack11111l1l11l_opy_:
          self.logger.info(bstack1ll11ll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣἚ"))
          return
        time.sleep(1)
        bstack1111l11ll11_opy_ += 1
      os.environ[bstack1ll11ll_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪἛ")] = str(self.bstack11111l111ll_opy_())
      self.logger.info(bstack1ll11ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨἜ"))
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢἝ").format(e))
  def bstack11111l111ll_opy_(self):
    if self.bstack11ll11ll1l_opy_:
      return
    try:
      bstack11111l11111_opy_ = [platform[bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ἞")].lower() for platform in self.config.get(bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ἟"), [])]
      bstack11111llll1l_opy_ = sys.maxsize
      bstack11111llll11_opy_ = bstack1ll11ll_opy_ (u"ࠩࠪἠ")
      for browser in bstack11111l11111_opy_:
        if browser in self.bstack111111l1lll_opy_:
          bstack111111l1l1l_opy_ = self.bstack111111l1lll_opy_[browser]
        if bstack111111l1l1l_opy_ < bstack11111llll1l_opy_:
          bstack11111llll1l_opy_ = bstack111111l1l1l_opy_
          bstack11111llll11_opy_ = browser
      return bstack11111llll11_opy_
    except Exception as e:
      self.logger.error(bstack1ll11ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦἡ").format(e))
  @classmethod
  def bstack11ll1ll1l_opy_(self):
    return os.getenv(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩἢ"), bstack1ll11ll_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫἣ")).lower()
  @classmethod
  def bstack1l11ll1ll1_opy_(self):
    return os.getenv(bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪἤ"), bstack1ll11ll_opy_ (u"ࠧࠨἥ"))
  @classmethod
  def bstack1l1l1l11l1l_opy_(cls, value):
    cls.bstack11l11l1lll_opy_ = value
  @classmethod
  def bstack11111l1111l_opy_(cls):
    return cls.bstack11l11l1lll_opy_
  @classmethod
  def bstack1l1l1l1111l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11111l111l1_opy_(cls):
    return cls.percy_build_id