# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
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
from bstack_utils.helper import bstack1l1ll1ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l1l111l1_opy_ import bstack1111l1lll_opy_
class bstack1111l11l_opy_:
  working_dir = os.getcwd()
  bstack111l1111_opy_ = False
  config = {}
  bstack11l11ll1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠫࠬẝ")
  binary_path = bstack1l11ll1_opy_ (u"ࠬ࠭ẞ")
  bstack1111l1ll111_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧẟ")
  bstack11ll11ll1l_opy_ = False
  bstack11111l111ll_opy_ = None
  bstack11111ll11ll_opy_ = {}
  bstack11111l1llll_opy_ = 300
  bstack111111lllll_opy_ = False
  logger = None
  bstack11111l11lll_opy_ = False
  bstack1ll11ll1l_opy_ = False
  percy_build_id = None
  bstack11111l11ll1_opy_ = bstack1l11ll1_opy_ (u"ࠧࠨẠ")
  bstack1111l11ll1l_opy_ = {
    bstack1l11ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨạ") : 1,
    bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪẢ") : 2,
    bstack1l11ll1_opy_ (u"ࠪࡩࡩ࡭ࡥࠨả") : 3,
    bstack1l11ll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫẤ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1111l1111ll_opy_(self):
    bstack11111ll1l11_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠭ấ")
    bstack1111l11ll11_opy_ = sys.platform
    bstack1111l1111l1_opy_ = bstack1l11ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬẦ")
    if re.match(bstack1l11ll1_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢầ"), bstack1111l11ll11_opy_) != None:
      bstack11111ll1l11_opy_ = bstack11l1l1llll1_opy_ + bstack1l11ll1_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤẨ")
      self.bstack11111l11ll1_opy_ = bstack1l11ll1_opy_ (u"ࠩࡰࡥࡨ࠭ẩ")
    elif re.match(bstack1l11ll1_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣẪ"), bstack1111l11ll11_opy_) != None:
      bstack11111ll1l11_opy_ = bstack11l1l1llll1_opy_ + bstack1l11ll1_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧẫ")
      bstack1111l1111l1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣẬ")
      self.bstack11111l11ll1_opy_ = bstack1l11ll1_opy_ (u"࠭ࡷࡪࡰࠪậ")
    else:
      bstack11111ll1l11_opy_ = bstack11l1l1llll1_opy_ + bstack1l11ll1_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥẮ")
      self.bstack11111l11ll1_opy_ = bstack1l11ll1_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧắ")
    return bstack11111ll1l11_opy_, bstack1111l1111l1_opy_
  def bstack11111l1lll1_opy_(self):
    try:
      bstack11111llllll_opy_ = [os.path.join(expanduser(bstack1l11ll1_opy_ (u"ࠤࢁࠦẰ")), bstack1l11ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪằ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11111llllll_opy_:
        if(self.bstack1111l1l1ll1_opy_(path)):
          return path
      raise bstack1l11ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣẲ")
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢẳ").format(e))
  def bstack1111l1l1ll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11111ll1111_opy_(self, bstack11111ll1ll1_opy_):
    return os.path.join(bstack11111ll1ll1_opy_, self.bstack11l11ll1ll1_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠮ࡦࡶࡤ࡫ࠧẴ"))
  def bstack1111l111l11_opy_(self, bstack11111ll1ll1_opy_, bstack11111l1l11l_opy_):
    if not bstack11111l1l11l_opy_: return
    try:
      bstack1111l1lll1l_opy_ = self.bstack11111ll1111_opy_(bstack11111ll1ll1_opy_)
      with open(bstack1111l1lll1l_opy_, bstack1l11ll1_opy_ (u"ࠢࡸࠤẵ")) as f:
        f.write(bstack11111l1l11l_opy_)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡕࡤࡺࡪࡪࠠ࡯ࡧࡺࠤࡊ࡚ࡡࡨࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠧẶ"))
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡸ࡭࡫ࠠࡦࡶࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤặ").format(e))
  def bstack1111l111lll_opy_(self, bstack11111ll1ll1_opy_):
    try:
      bstack1111l1lll1l_opy_ = self.bstack11111ll1111_opy_(bstack11111ll1ll1_opy_)
      if os.path.exists(bstack1111l1lll1l_opy_):
        with open(bstack1111l1lll1l_opy_, bstack1l11ll1_opy_ (u"ࠥࡶࠧẸ")) as f:
          bstack11111l1l11l_opy_ = f.read().strip()
          return bstack11111l1l11l_opy_ if bstack11111l1l11l_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡋࡔࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢẹ").format(e))
  def bstack11111l11l11_opy_(self, bstack11111ll1ll1_opy_, bstack11111ll1l11_opy_):
    bstack11111lll11l_opy_ = self.bstack1111l111lll_opy_(bstack11111ll1ll1_opy_)
    if bstack11111lll11l_opy_:
      try:
        bstack11111l1l111_opy_ = self.bstack11111l1ll11_opy_(bstack11111lll11l_opy_, bstack11111ll1l11_opy_)
        if not bstack11111l1l111_opy_:
          self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡹࠠࡶࡲࠣࡸࡴࠦࡤࡢࡶࡨࠤ࠭ࡋࡔࡢࡩࠣࡹࡳࡩࡨࡢࡰࡪࡩࡩ࠯ࠢẺ"))
          return True
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡎࡦࡹࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷࡩࠧẻ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l11ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡳࡷࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨẼ").format(e))
    return False
  def bstack11111l1ll11_opy_(self, bstack11111lll11l_opy_, bstack11111ll1l11_opy_):
    try:
      headers = {
        bstack1l11ll1_opy_ (u"ࠣࡋࡩ࠱ࡓࡵ࡮ࡦ࠯ࡐࡥࡹࡩࡨࠣẽ"): bstack11111lll11l_opy_
      }
      response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠩࡊࡉ࡙࠭Ế"), bstack11111ll1l11_opy_, {}, {bstack1l11ll1_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦế"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l11ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠼ࠣࡿࢂࠨỀ").format(e))
  @measure(event_name=EVENTS.bstack11l1llll1l1_opy_, stage=STAGE.bstack11lllll111_opy_)
  def bstack1111l11l11l_opy_(self, bstack11111ll1l11_opy_, bstack1111l1111l1_opy_):
    try:
      bstack1111l11l111_opy_ = self.bstack11111l1lll1_opy_()
      bstack1111ll11111_opy_ = os.path.join(bstack1111l11l111_opy_, bstack1l11ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨề"))
      bstack11111l11111_opy_ = os.path.join(bstack1111l11l111_opy_, bstack1111l1111l1_opy_)
      if self.bstack11111l11l11_opy_(bstack1111l11l111_opy_, bstack11111ll1l11_opy_): # if bstack1111l1lllll_opy_, bstack1l1l111ll11_opy_ bstack11111l1l11l_opy_ is bstack1111l11lll1_opy_ to bstack11l111lllll_opy_ version available (response 304)
        if os.path.exists(bstack11111l11111_opy_):
          self.logger.info(bstack1l11ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣỂ").format(bstack11111l11111_opy_))
          return bstack11111l11111_opy_
        if os.path.exists(bstack1111ll11111_opy_):
          self.logger.info(bstack1l11ll1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧể").format(bstack1111ll11111_opy_))
          return self.bstack11111ll1lll_opy_(bstack1111ll11111_opy_, bstack1111l1111l1_opy_)
      self.logger.info(bstack1l11ll1_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨỄ").format(bstack11111ll1l11_opy_))
      response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠩࡊࡉ࡙࠭ễ"), bstack11111ll1l11_opy_, {}, {})
      if response.status_code == 200:
        bstack11111l1111l_opy_ = response.headers.get(bstack1l11ll1_opy_ (u"ࠥࡉ࡙ࡧࡧࠣỆ"), bstack1l11ll1_opy_ (u"ࠦࠧệ"))
        if bstack11111l1111l_opy_:
          self.bstack1111l111l11_opy_(bstack1111l11l111_opy_, bstack11111l1111l_opy_)
        with open(bstack1111ll11111_opy_, bstack1l11ll1_opy_ (u"ࠬࡽࡢࠨỈ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11ll1_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࢀࠦỉ").format(bstack1111ll11111_opy_))
        return self.bstack11111ll1lll_opy_(bstack1111ll11111_opy_, bstack1111l1111l1_opy_)
      else:
        raise(bstack1l11ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡿࠥỊ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤị").format(e))
  def bstack1111l1llll1_opy_(self, bstack11111ll1l11_opy_, bstack1111l1111l1_opy_):
    try:
      retry = 2
      bstack11111l11111_opy_ = None
      bstack1111l11111l_opy_ = False
      while retry > 0:
        bstack11111l11111_opy_ = self.bstack1111l11l11l_opy_(bstack11111ll1l11_opy_, bstack1111l1111l1_opy_)
        bstack1111l11111l_opy_ = self.bstack11111llll1l_opy_(bstack11111ll1l11_opy_, bstack1111l1111l1_opy_, bstack11111l11111_opy_)
        if bstack1111l11111l_opy_:
          break
        retry -= 1
      return bstack11111l11111_opy_, bstack1111l11111l_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨỌ").format(e))
    return bstack11111l11111_opy_, False
  def bstack11111llll1l_opy_(self, bstack11111ll1l11_opy_, bstack1111l1111l1_opy_, bstack11111l11111_opy_, bstack1111l111l1l_opy_ = 0):
    if bstack1111l111l1l_opy_ > 1:
      return False
    if bstack11111l11111_opy_ == None or os.path.exists(bstack11111l11111_opy_) == False:
      self.logger.warn(bstack1l11ll1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣọ"))
      return False
    bstack11111lllll1_opy_ = bstack1l11ll1_opy_ (u"ࡶࠧࡤ࠮ࠫࡂࡳࡩࡷࡩࡹ࠰ࡥ࡯࡭ࠥࡢࡤࠬ࡞࠱ࡠࡩ࠱࡜࠯࡞ࡧ࠯ࠧỎ")
    command = bstack1l11ll1_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫỏ").format(bstack11111l11111_opy_)
    bstack1111l1l1lll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11111lllll1_opy_, bstack1111l1l1lll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧỐ"))
      return False
  def bstack11111ll1lll_opy_(self, bstack1111ll11111_opy_, bstack1111l1111l1_opy_):
    try:
      working_dir = os.path.dirname(bstack1111ll11111_opy_)
      shutil.unpack_archive(bstack1111ll11111_opy_, working_dir)
      bstack11111l11111_opy_ = os.path.join(working_dir, bstack1111l1111l1_opy_)
      os.chmod(bstack11111l11111_opy_, 0o755)
      return bstack11111l11111_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣố"))
  def bstack11111llll11_opy_(self):
    try:
      bstack11111l111l1_opy_ = self.config.get(bstack1l11ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧỒ"))
      bstack11111llll11_opy_ = bstack11111l111l1_opy_ or (bstack11111l111l1_opy_ is None and self.bstack111l1111_opy_)
      if not bstack11111llll11_opy_ or self.config.get(bstack1l11ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬồ"), None) not in bstack11l1llll1ll_opy_:
        return False
      self.bstack11ll11ll1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧỔ").format(e))
  def bstack1111l111ll1_opy_(self):
    try:
      bstack1111l111ll1_opy_ = self.percy_capture_mode
      return bstack1111l111ll1_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧổ").format(e))
  def init(self, bstack111l1111_opy_, config, logger):
    self.bstack111l1111_opy_ = bstack111l1111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11111llll11_opy_():
      return
    self.bstack11111ll11ll_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫỖ"), {})
    self.percy_capture_mode = config.get(bstack1l11ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩỗ"))
    try:
      bstack11111ll1l11_opy_, bstack1111l1111l1_opy_ = self.bstack1111l1111ll_opy_()
      self.bstack11l11ll1ll1_opy_ = bstack1111l1111l1_opy_
      bstack11111l11111_opy_, bstack1111l11111l_opy_ = self.bstack1111l1llll1_opy_(bstack11111ll1l11_opy_, bstack1111l1111l1_opy_)
      if bstack1111l11111l_opy_:
        self.binary_path = bstack11111l11111_opy_
        thread = Thread(target=self.bstack11111l1l1ll_opy_)
        thread.start()
      else:
        self.bstack11111l11lll_opy_ = True
        self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦỘ").format(bstack11111l11111_opy_))
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤộ").format(e))
  def bstack11111ll111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11ll1_opy_ (u"ࠩ࡯ࡳ࡬࠭Ớ"), bstack1l11ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭ớ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣỜ").format(logfile))
      self.bstack1111l1ll111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨờ").format(e))
  @measure(event_name=EVENTS.bstack11l1ll1l1ll_opy_, stage=STAGE.bstack11lllll111_opy_)
  def bstack11111l1l1ll_opy_(self):
    bstack1111l1l1111_opy_ = self.bstack11111lll111_opy_()
    if bstack1111l1l1111_opy_ == None:
      self.bstack11111l11lll_opy_ = True
      self.logger.error(bstack1l11ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤỞ"))
      return False
    bstack1111l1l11ll_opy_ = [bstack1l11ll1_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣở") if self.bstack111l1111_opy_ else bstack1l11ll1_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬỠ")]
    bstack111l1l1l1l1_opy_ = self.bstack11111ll1l1l_opy_()
    if bstack111l1l1l1l1_opy_ != None:
      bstack1111l1l11ll_opy_.append(bstack1l11ll1_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣỡ").format(bstack111l1l1l1l1_opy_))
    env = os.environ.copy()
    env[bstack1l11ll1_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣỢ")] = bstack1111l1l1111_opy_
    env[bstack1l11ll1_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦợ")] = os.environ.get(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪỤ"), bstack1l11ll1_opy_ (u"࠭ࠧụ"))
    bstack1111l1l1l11_opy_ = [self.binary_path]
    self.bstack11111ll111l_opy_()
    self.bstack11111l111ll_opy_ = self.bstack1111l11llll_opy_(bstack1111l1l1l11_opy_ + bstack1111l1l11ll_opy_, env)
    self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣỦ"))
    bstack1111l111l1l_opy_ = 0
    while self.bstack11111l111ll_opy_.poll() == None:
      bstack1111l1ll1ll_opy_ = self.bstack1111l1ll1l1_opy_()
      if bstack1111l1ll1ll_opy_:
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦủ"))
        self.bstack111111lllll_opy_ = True
        return True
      bstack1111l111l1l_opy_ += 1
      self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧỨ").format(bstack1111l111l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣứ").format(bstack1111l111l1l_opy_))
    self.bstack11111l11lll_opy_ = True
    return False
  def bstack1111l1ll1l1_opy_(self, bstack1111l111l1l_opy_ = 0):
    if bstack1111l111l1l_opy_ > 10:
      return False
    try:
      bstack1111l1ll11l_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫỪ"), bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭ừ"))
      bstack1111l1l111l_opy_ = bstack1111l1ll11l_opy_ + bstack11l1lll1l1l_opy_
      response = requests.get(bstack1111l1l111l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬỬ"), {}).get(bstack1l11ll1_opy_ (u"ࠧࡪࡦࠪử"), None)
      return True
    except:
      self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢ࡮ࡷ࡬ࠥࡩࡨࡦࡥ࡮ࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨỮ"))
      return False
  def bstack11111lll111_opy_(self):
    bstack1111l1l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠩࡤࡴࡵ࠭ữ") if self.bstack111l1111_opy_ else bstack1l11ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬỰ")
    bstack1111l1l1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢự") if self.config.get(bstack1l11ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫỲ")) is None else True
    bstack11ll11l111l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠫࡶࡥࡳࡥࡼࡁࢀࢃࠢỳ").format(self.config[bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬỴ")], bstack1111l1l11l1_opy_, bstack1111l1l1l1l_opy_)
    if self.percy_capture_mode:
      bstack11ll11l111l_opy_ += bstack1l11ll1_opy_ (u"ࠣࠨࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫࠽ࡼࡿࠥỵ").format(self.percy_capture_mode)
    uri = bstack1111l1lll_opy_(bstack11ll11l111l_opy_)
    try:
      response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠩࡊࡉ࡙࠭Ỷ"), uri, {}, {bstack1l11ll1_opy_ (u"ࠪࡥࡺࡺࡨࠨỷ"): (self.config[bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ỹ")], self.config[bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨỹ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11ll11ll1l_opy_ = data.get(bstack1l11ll1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧỺ"))
        self.percy_capture_mode = data.get(bstack1l11ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࠬỻ"))
        os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭Ỽ")] = str(self.bstack11ll11ll1l_opy_)
        os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ỽ")] = str(self.percy_capture_mode)
        if bstack1111l1l1l1l_opy_ == bstack1l11ll1_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨỾ") and str(self.bstack11ll11ll1l_opy_).lower() == bstack1l11ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤỿ"):
          self.bstack1ll11ll1l_opy_ = True
        if bstack1l11ll1_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦἀ") in data:
          return data[bstack1l11ll1_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧἁ")]
        else:
          raise bstack1l11ll1_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧἂ").format(data)
      else:
        raise bstack1l11ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣἃ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥἄ").format(e))
  def bstack11111ll1l1l_opy_(self):
    bstack1111l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨἅ"))
    try:
      if bstack1l11ll1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬἆ") not in self.bstack11111ll11ll_opy_:
        self.bstack11111ll11ll_opy_[bstack1l11ll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ἇ")] = 2
      with open(bstack1111l11l1l1_opy_, bstack1l11ll1_opy_ (u"࠭ࡷࠨἈ")) as fp:
        json.dump(self.bstack11111ll11ll_opy_, fp)
      return bstack1111l11l1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢἉ").format(e))
  def bstack1111l11llll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11111l11ll1_opy_ == bstack1l11ll1_opy_ (u"ࠨࡹ࡬ࡲࠬἊ"):
        bstack11111l1ll1l_opy_ = [bstack1l11ll1_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪἋ"), bstack1l11ll1_opy_ (u"ࠪ࠳ࡨ࠭Ἄ")]
        cmd = bstack11111l1ll1l_opy_ + cmd
      cmd = bstack1l11ll1_opy_ (u"ࠫࠥ࠭Ἅ").join(cmd)
      self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤἎ").format(cmd))
      with open(self.bstack1111l1ll111_opy_, bstack1l11ll1_opy_ (u"ࠨࡡࠣἏ")) as bstack11111l11l1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11111l11l1l_opy_, text=True, stderr=bstack11111l11l1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11111l11lll_opy_ = True
      self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤἐ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111111lllll_opy_:
        self.logger.info(bstack1l11ll1_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤἑ"))
        cmd = [self.binary_path, bstack1l11ll1_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧἒ")]
        self.bstack1111l11llll_opy_(cmd)
        self.bstack111111lllll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥἓ").format(cmd, e))
  def bstack11l1l1llll_opy_(self):
    if not self.bstack11ll11ll1l_opy_:
      return
    try:
      bstack11111lll1ll_opy_ = 0
      while not self.bstack111111lllll_opy_ and bstack11111lll1ll_opy_ < self.bstack11111l1llll_opy_:
        if self.bstack11111l11lll_opy_:
          self.logger.info(bstack1l11ll1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤἔ"))
          return
        time.sleep(1)
        bstack11111lll1ll_opy_ += 1
      os.environ[bstack1l11ll1_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫἕ")] = str(self.bstack1111l11l1ll_opy_())
      self.logger.info(bstack1l11ll1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢ἖"))
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ἗").format(e))
  def bstack1111l11l1ll_opy_(self):
    if self.bstack111l1111_opy_:
      return
    try:
      bstack1111l1lll11_opy_ = [platform[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭Ἐ")].lower() for platform in self.config.get(bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬἙ"), [])]
      bstack11111ll11l1_opy_ = sys.maxsize
      bstack11111lll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠪࠫἚ")
      for browser in bstack1111l1lll11_opy_:
        if browser in self.bstack1111l11ll1l_opy_:
          bstack1111ll1111l_opy_ = self.bstack1111l11ll1l_opy_[browser]
        if bstack1111ll1111l_opy_ < bstack11111ll11l1_opy_:
          bstack11111ll11l1_opy_ = bstack1111ll1111l_opy_
          bstack11111lll1l1_opy_ = browser
      return bstack11111lll1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l11ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧἛ").format(e))
  @classmethod
  def bstack1ll1l11111_opy_(self):
    return os.getenv(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪἜ"), bstack1l11ll1_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬἝ")).lower()
  @classmethod
  def bstack11l1111l11_opy_(self):
    return os.getenv(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫ἞"), bstack1l11ll1_opy_ (u"ࠨࠩ἟"))
  @classmethod
  def bstack1l1l11lllll_opy_(cls, value):
    cls.bstack1ll11ll1l_opy_ = value
  @classmethod
  def bstack11111l1l1l1_opy_(cls):
    return cls.bstack1ll11ll1l_opy_
  @classmethod
  def bstack1l1l1l111ll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1111l111111_opy_(cls):
    return cls.percy_build_id