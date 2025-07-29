# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
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
from bstack_utils.helper import bstack11llll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1l111l11_opy_ import bstack1ll1lll11_opy_
class bstack111l1ll1l_opy_:
  working_dir = os.getcwd()
  bstack1llllll111_opy_ = False
  config = {}
  bstack111lll1ll11_opy_ = bstackl_opy_ (u"ࠨࠩḣ")
  binary_path = bstackl_opy_ (u"ࠩࠪḤ")
  bstack1111lll1111_opy_ = bstackl_opy_ (u"ࠪࠫḥ")
  bstack1ll1ll1l11_opy_ = False
  bstack1111l1l1ll1_opy_ = None
  bstack1111l1l111l_opy_ = {}
  bstack1111l1l1lll_opy_ = 300
  bstack1111l11l1l1_opy_ = False
  logger = None
  bstack111l1111ll1_opy_ = False
  bstack111l1l1l_opy_ = False
  percy_build_id = None
  bstack1111ll111l1_opy_ = bstackl_opy_ (u"ࠫࠬḦ")
  bstack111l111111l_opy_ = {
    bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬḧ") : 1,
    bstackl_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧḨ") : 2,
    bstackl_opy_ (u"ࠧࡦࡦࡪࡩࠬḩ") : 3,
    bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨḪ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111l1111lll_opy_(self):
    bstack1111lll1ll1_opy_ = bstackl_opy_ (u"ࠩࠪḫ")
    bstack1111l1llll1_opy_ = sys.platform
    bstack1111llll1ll_opy_ = bstackl_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩḬ")
    if re.match(bstackl_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦḭ"), bstack1111l1llll1_opy_) != None:
      bstack1111lll1ll1_opy_ = bstack11l1llll111_opy_ + bstackl_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨḮ")
      self.bstack1111ll111l1_opy_ = bstackl_opy_ (u"࠭࡭ࡢࡥࠪḯ")
    elif re.match(bstackl_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧḰ"), bstack1111l1llll1_opy_) != None:
      bstack1111lll1ll1_opy_ = bstack11l1llll111_opy_ + bstackl_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤḱ")
      bstack1111llll1ll_opy_ = bstackl_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧḲ")
      self.bstack1111ll111l1_opy_ = bstackl_opy_ (u"ࠪࡻ࡮ࡴࠧḳ")
    else:
      bstack1111lll1ll1_opy_ = bstack11l1llll111_opy_ + bstackl_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢḴ")
      self.bstack1111ll111l1_opy_ = bstackl_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫḵ")
    return bstack1111lll1ll1_opy_, bstack1111llll1ll_opy_
  def bstack1111ll1111l_opy_(self):
    try:
      bstack1111ll1ll1l_opy_ = [os.path.join(expanduser(bstackl_opy_ (u"ࠨࡾࠣḶ")), bstackl_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧḷ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111ll1ll1l_opy_:
        if(self.bstack1111l11llll_opy_(path)):
          return path
      raise bstackl_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧḸ")
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦḹ").format(e))
  def bstack1111l11llll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111lll111l_opy_(self, bstack1111lll1l11_opy_):
    return os.path.join(bstack1111lll1l11_opy_, self.bstack111lll1ll11_opy_ + bstackl_opy_ (u"ࠥ࠲ࡪࡺࡡࡨࠤḺ"))
  def bstack1111ll11l1l_opy_(self, bstack1111lll1l11_opy_, bstack1111ll11ll1_opy_):
    if not bstack1111ll11ll1_opy_: return
    try:
      bstack1111l1l1111_opy_ = self.bstack1111lll111l_opy_(bstack1111lll1l11_opy_)
      with open(bstack1111l1l1111_opy_, bstackl_opy_ (u"ࠦࡼࠨḻ")) as f:
        f.write(bstack1111ll11ll1_opy_)
        self.logger.debug(bstackl_opy_ (u"࡙ࠧࡡࡷࡧࡧࠤࡳ࡫ࡷࠡࡇࡗࡥ࡬ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠤḼ"))
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡵࡪࡨࠤࡪࡺࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨḽ").format(e))
  def bstack111l1111l1l_opy_(self, bstack1111lll1l11_opy_):
    try:
      bstack1111l1l1111_opy_ = self.bstack1111lll111l_opy_(bstack1111lll1l11_opy_)
      if os.path.exists(bstack1111l1l1111_opy_):
        with open(bstack1111l1l1111_opy_, bstackl_opy_ (u"ࠢࡳࠤḾ")) as f:
          bstack1111ll11ll1_opy_ = f.read().strip()
          return bstack1111ll11ll1_opy_ if bstack1111ll11ll1_opy_ else None
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡ࡮ࡲࡥࡩ࡯࡮ࡨࠢࡈࡘࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦḿ").format(e))
  def bstack1111l1ll111_opy_(self, bstack1111lll1l11_opy_, bstack1111lll1ll1_opy_):
    bstack1111l1ll11l_opy_ = self.bstack111l1111l1l_opy_(bstack1111lll1l11_opy_)
    if bstack1111l1ll11l_opy_:
      try:
        bstack1111l1ll1l1_opy_ = self.bstack1111l11l1ll_opy_(bstack1111l1ll11l_opy_, bstack1111lll1ll1_opy_)
        if not bstack1111l1ll1l1_opy_:
          self.logger.debug(bstackl_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡶࠤࡺࡶࠠࡵࡱࠣࡨࡦࡺࡥࠡࠪࡈࡘࡦ࡭ࠠࡶࡰࡦ࡬ࡦࡴࡧࡦࡦࠬࠦṀ"))
          return True
        self.logger.debug(bstackl_opy_ (u"ࠥࡒࡪࡽࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡦࠤṁ"))
        return False
      except Exception as e:
        self.logger.warn(bstackl_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡦࡰࡴࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠰ࠥࡻࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥṂ").format(e))
    return False
  def bstack1111l11l1ll_opy_(self, bstack1111l1ll11l_opy_, bstack1111lll1ll1_opy_):
    try:
      headers = {
        bstackl_opy_ (u"ࠧࡏࡦ࠮ࡐࡲࡲࡪ࠳ࡍࡢࡶࡦ࡬ࠧṃ"): bstack1111l1ll11l_opy_
      }
      response = bstack11llll1l1l_opy_(bstackl_opy_ (u"࠭ࡇࡆࡖࠪṄ"), bstack1111lll1ll1_opy_, {}, {bstackl_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣṅ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸࡀࠠࡼࡿࠥṆ").format(e))
  @measure(event_name=EVENTS.bstack11l1ll11l11_opy_, stage=STAGE.bstack1l1111ll1_opy_)
  def bstack1111llll11l_opy_(self, bstack1111lll1ll1_opy_, bstack1111llll1ll_opy_):
    try:
      bstack1111ll1l111_opy_ = self.bstack1111ll1111l_opy_()
      bstack1111ll1l11l_opy_ = os.path.join(bstack1111ll1l111_opy_, bstackl_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬṇ"))
      bstack1111ll11111_opy_ = os.path.join(bstack1111ll1l111_opy_, bstack1111llll1ll_opy_)
      if self.bstack1111l1ll111_opy_(bstack1111ll1l111_opy_, bstack1111lll1ll1_opy_): # if bstack1111l11l111_opy_, bstack1l1l11l1l11_opy_ bstack1111ll11ll1_opy_ is bstack1111llll1l1_opy_ to bstack111lll11l1l_opy_ version available (response 304)
        if os.path.exists(bstack1111ll11111_opy_):
          self.logger.info(bstackl_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧṈ").format(bstack1111ll11111_opy_))
          return bstack1111ll11111_opy_
        if os.path.exists(bstack1111ll1l11l_opy_):
          self.logger.info(bstackl_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤṉ").format(bstack1111ll1l11l_opy_))
          return self.bstack1111ll1l1l1_opy_(bstack1111ll1l11l_opy_, bstack1111llll1ll_opy_)
      self.logger.info(bstackl_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥṊ").format(bstack1111lll1ll1_opy_))
      response = bstack11llll1l1l_opy_(bstackl_opy_ (u"࠭ࡇࡆࡖࠪṋ"), bstack1111lll1ll1_opy_, {}, {})
      if response.status_code == 200:
        bstack1111l1ll1ll_opy_ = response.headers.get(bstackl_opy_ (u"ࠢࡆࡖࡤ࡫ࠧṌ"), bstackl_opy_ (u"ࠣࠤṍ"))
        if bstack1111l1ll1ll_opy_:
          self.bstack1111ll11l1l_opy_(bstack1111ll1l111_opy_, bstack1111l1ll1ll_opy_)
        with open(bstack1111ll1l11l_opy_, bstackl_opy_ (u"ࠩࡺࡦࠬṎ")) as file:
          file.write(response.content)
        self.logger.info(bstackl_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣṏ").format(bstack1111ll1l11l_opy_))
        return self.bstack1111ll1l1l1_opy_(bstack1111ll1l11l_opy_, bstack1111llll1ll_opy_)
      else:
        raise(bstackl_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢṐ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨṑ").format(e))
  def bstack1111l1l11l1_opy_(self, bstack1111lll1ll1_opy_, bstack1111llll1ll_opy_):
    try:
      retry = 2
      bstack1111ll11111_opy_ = None
      bstack1111l1l1l1l_opy_ = False
      while retry > 0:
        bstack1111ll11111_opy_ = self.bstack1111llll11l_opy_(bstack1111lll1ll1_opy_, bstack1111llll1ll_opy_)
        bstack1111l1l1l1l_opy_ = self.bstack111l1111111_opy_(bstack1111lll1ll1_opy_, bstack1111llll1ll_opy_, bstack1111ll11111_opy_)
        if bstack1111l1l1l1l_opy_:
          break
        retry -= 1
      return bstack1111ll11111_opy_, bstack1111l1l1l1l_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥṒ").format(e))
    return bstack1111ll11111_opy_, False
  def bstack111l1111111_opy_(self, bstack1111lll1ll1_opy_, bstack1111llll1ll_opy_, bstack1111ll11111_opy_, bstack1111l1l1l11_opy_ = 0):
    if bstack1111l1l1l11_opy_ > 1:
      return False
    if bstack1111ll11111_opy_ == None or os.path.exists(bstack1111ll11111_opy_) == False:
      self.logger.warn(bstackl_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧṓ"))
      return False
    bstack1111ll11l11_opy_ = bstackl_opy_ (u"ࡳࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࡠ࠳ࡢࡤࠬࠤṔ")
    command = bstackl_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨṕ").format(bstack1111ll11111_opy_)
    bstack111l111l111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111ll11l11_opy_, bstack111l111l111_opy_) != None:
      return True
    else:
      self.logger.error(bstackl_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤṖ"))
      return False
  def bstack1111ll1l1l1_opy_(self, bstack1111ll1l11l_opy_, bstack1111llll1ll_opy_):
    try:
      working_dir = os.path.dirname(bstack1111ll1l11l_opy_)
      shutil.unpack_archive(bstack1111ll1l11l_opy_, working_dir)
      bstack1111ll11111_opy_ = os.path.join(working_dir, bstack1111llll1ll_opy_)
      os.chmod(bstack1111ll11111_opy_, 0o755)
      return bstack1111ll11111_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧṗ"))
  def bstack1111llll111_opy_(self):
    try:
      bstack111l1111l11_opy_ = self.config.get(bstackl_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫṘ"))
      bstack1111llll111_opy_ = bstack111l1111l11_opy_ or (bstack111l1111l11_opy_ is None and self.bstack1llllll111_opy_)
      if not bstack1111llll111_opy_ or self.config.get(bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩṙ"), None) not in bstack11l1lll11l1_opy_:
        return False
      self.bstack1ll1ll1l11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤṚ").format(e))
  def bstack111l11111l1_opy_(self):
    try:
      bstack111l11111l1_opy_ = self.percy_capture_mode
      return bstack111l11111l1_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤṛ").format(e))
  def init(self, bstack1llllll111_opy_, config, logger):
    self.bstack1llllll111_opy_ = bstack1llllll111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111llll111_opy_():
      return
    self.bstack1111l1l111l_opy_ = config.get(bstackl_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨṜ"), {})
    self.percy_capture_mode = config.get(bstackl_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ṝ"))
    try:
      bstack1111lll1ll1_opy_, bstack1111llll1ll_opy_ = self.bstack111l1111lll_opy_()
      self.bstack111lll1ll11_opy_ = bstack1111llll1ll_opy_
      bstack1111ll11111_opy_, bstack1111l1l1l1l_opy_ = self.bstack1111l1l11l1_opy_(bstack1111lll1ll1_opy_, bstack1111llll1ll_opy_)
      if bstack1111l1l1l1l_opy_:
        self.binary_path = bstack1111ll11111_opy_
        thread = Thread(target=self.bstack1111ll1lll1_opy_)
        thread.start()
      else:
        self.bstack111l1111ll1_opy_ = True
        self.logger.error(bstackl_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣṞ").format(bstack1111ll11111_opy_))
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨṟ").format(e))
  def bstack1111lllll1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstackl_opy_ (u"࠭࡬ࡰࡩࠪṠ"), bstackl_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩࠪṡ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstackl_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁࠧṢ").format(logfile))
      self.bstack1111lll1111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥṣ").format(e))
  @measure(event_name=EVENTS.bstack11l1lllll1l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
  def bstack1111ll1lll1_opy_(self):
    bstack1111l11ll11_opy_ = self.bstack1111l1lll11_opy_()
    if bstack1111l11ll11_opy_ == None:
      self.bstack111l1111ll1_opy_ = True
      self.logger.error(bstackl_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨṤ"))
      return False
    command_args = [bstackl_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧṥ") if self.bstack1llllll111_opy_ else bstackl_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩṦ")]
    bstack111ll11ll11_opy_ = self.bstack1111llllll1_opy_()
    if bstack111ll11ll11_opy_ != None:
      command_args.append(bstackl_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧṧ").format(bstack111ll11ll11_opy_))
    env = os.environ.copy()
    env[bstackl_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧṨ")] = bstack1111l11ll11_opy_
    env[bstackl_opy_ (u"ࠣࡖࡋࡣࡇ࡛ࡉࡍࡆࡢ࡙࡚ࡏࡄࠣṩ")] = os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧṪ"), bstackl_opy_ (u"ࠪࠫṫ"))
    bstack1111l11l11l_opy_ = [self.binary_path]
    self.bstack1111lllll1l_opy_()
    self.bstack1111l1l1ll1_opy_ = self.bstack1111l11ll1l_opy_(bstack1111l11l11l_opy_ + command_args, env)
    self.logger.debug(bstackl_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧṬ"))
    bstack1111l1l1l11_opy_ = 0
    while self.bstack1111l1l1ll1_opy_.poll() == None:
      bstack1111lllll11_opy_ = self.bstack1111l11lll1_opy_()
      if bstack1111lllll11_opy_:
        self.logger.debug(bstackl_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣṭ"))
        self.bstack1111l11l1l1_opy_ = True
        return True
      bstack1111l1l1l11_opy_ += 1
      self.logger.debug(bstackl_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤṮ").format(bstack1111l1l1l11_opy_))
      time.sleep(2)
    self.logger.error(bstackl_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧṯ").format(bstack1111l1l1l11_opy_))
    self.bstack111l1111ll1_opy_ = True
    return False
  def bstack1111l11lll1_opy_(self, bstack1111l1l1l11_opy_ = 0):
    if bstack1111l1l1l11_opy_ > 10:
      return False
    try:
      bstack1111l1lll1l_opy_ = os.environ.get(bstackl_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨṰ"), bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪṱ"))
      bstack1111l111lll_opy_ = bstack1111l1lll1l_opy_ + bstack11ll1111111_opy_
      response = requests.get(bstack1111l111lll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࠩṲ"), {}).get(bstackl_opy_ (u"ࠫ࡮ࡪࠧṳ"), None)
      return True
    except:
      self.logger.debug(bstackl_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡲࡴࡩࠢࡦ࡬ࡪࡩ࡫ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥṴ"))
      return False
  def bstack1111l1lll11_opy_(self):
    bstack1111ll1ll11_opy_ = bstackl_opy_ (u"࠭ࡡࡱࡲࠪṵ") if self.bstack1llllll111_opy_ else bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩṶ")
    bstack1111ll1llll_opy_ = bstackl_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦṷ") if self.config.get(bstackl_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨṸ")) is None else True
    bstack11ll11l1ll1_opy_ = bstackl_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠨࡳࡩࡷࡩࡹ࠾ࡽࢀࠦṹ").format(self.config[bstackl_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩṺ")], bstack1111ll1ll11_opy_, bstack1111ll1llll_opy_)
    if self.percy_capture_mode:
      bstack11ll11l1ll1_opy_ += bstackl_opy_ (u"ࠧࠬࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࡁࢀࢃࠢṻ").format(self.percy_capture_mode)
    uri = bstack1ll1lll11_opy_(bstack11ll11l1ll1_opy_)
    try:
      response = bstack11llll1l1l_opy_(bstackl_opy_ (u"࠭ࡇࡆࡖࠪṼ"), uri, {}, {bstackl_opy_ (u"ࠧࡢࡷࡷ࡬ࠬṽ"): (self.config[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪṾ")], self.config[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬṿ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1ll1ll1l11_opy_ = data.get(bstackl_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫẀ"))
        self.percy_capture_mode = data.get(bstackl_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦࠩẁ"))
        os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪẂ")] = str(self.bstack1ll1ll1l11_opy_)
        os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪẃ")] = str(self.percy_capture_mode)
        if bstack1111ll1llll_opy_ == bstackl_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥẄ") and str(self.bstack1ll1ll1l11_opy_).lower() == bstackl_opy_ (u"ࠣࡶࡵࡹࡪࠨẅ"):
          self.bstack111l1l1l_opy_ = True
        if bstackl_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣẆ") in data:
          return data[bstackl_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤẇ")]
        else:
          raise bstackl_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫẈ").format(data)
      else:
        raise bstackl_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧẉ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢẊ").format(e))
  def bstack1111llllll1_opy_(self):
    bstack1111lll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥẋ"))
    try:
      if bstackl_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩẌ") not in self.bstack1111l1l111l_opy_:
        self.bstack1111l1l111l_opy_[bstackl_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪẍ")] = 2
      with open(bstack1111lll1lll_opy_, bstackl_opy_ (u"ࠪࡻࠬẎ")) as fp:
        json.dump(self.bstack1111l1l111l_opy_, fp)
      return bstack1111lll1lll_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦẏ").format(e))
  def bstack1111l11ll1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111ll111l1_opy_ == bstackl_opy_ (u"ࠬࡽࡩ࡯ࠩẐ"):
        bstack1111lll11ll_opy_ = [bstackl_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧẑ"), bstackl_opy_ (u"ࠧ࠰ࡥࠪẒ")]
        cmd = bstack1111lll11ll_opy_ + cmd
      cmd = bstackl_opy_ (u"ࠨࠢࠪẓ").join(cmd)
      self.logger.debug(bstackl_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨẔ").format(cmd))
      with open(self.bstack1111lll1111_opy_, bstackl_opy_ (u"ࠥࡥࠧẕ")) as bstack1111ll11lll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111ll11lll_opy_, text=True, stderr=bstack1111ll11lll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111l1111ll1_opy_ = True
      self.logger.error(bstackl_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨẖ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111l11l1l1_opy_:
        self.logger.info(bstackl_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨẗ"))
        cmd = [self.binary_path, bstackl_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤẘ")]
        self.bstack1111l11ll1l_opy_(cmd)
        self.bstack1111l11l1l1_opy_ = False
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢẙ").format(cmd, e))
  def bstack1ll1l1ll_opy_(self):
    if not self.bstack1ll1ll1l11_opy_:
      return
    try:
      bstack1111ll111ll_opy_ = 0
      while not self.bstack1111l11l1l1_opy_ and bstack1111ll111ll_opy_ < self.bstack1111l1l1lll_opy_:
        if self.bstack111l1111ll1_opy_:
          self.logger.info(bstackl_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨẚ"))
          return
        time.sleep(1)
        bstack1111ll111ll_opy_ += 1
      os.environ[bstackl_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨẛ")] = str(self.bstack1111lll1l1l_opy_())
      self.logger.info(bstackl_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦẜ"))
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧẝ").format(e))
  def bstack1111lll1l1l_opy_(self):
    if self.bstack1llllll111_opy_:
      return
    try:
      bstack1111lll11l1_opy_ = [platform[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪẞ")].lower() for platform in self.config.get(bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩẟ"), [])]
      bstack1111lllllll_opy_ = sys.maxsize
      bstack1111l1l11ll_opy_ = bstackl_opy_ (u"ࠧࠨẠ")
      for browser in bstack1111lll11l1_opy_:
        if browser in self.bstack111l111111l_opy_:
          bstack1111l1lllll_opy_ = self.bstack111l111111l_opy_[browser]
        if bstack1111l1lllll_opy_ < bstack1111lllllll_opy_:
          bstack1111lllllll_opy_ = bstack1111l1lllll_opy_
          bstack1111l1l11ll_opy_ = browser
      return bstack1111l1l11ll_opy_
    except Exception as e:
      self.logger.error(bstackl_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤạ").format(e))
  @classmethod
  def bstack1l11lll11_opy_(self):
    return os.getenv(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧẢ"), bstackl_opy_ (u"ࠪࡊࡦࡲࡳࡦࠩả")).lower()
  @classmethod
  def bstack1l1l111111_opy_(self):
    return os.getenv(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨẤ"), bstackl_opy_ (u"ࠬ࠭ấ"))
  @classmethod
  def bstack1l1l1l1l1l1_opy_(cls, value):
    cls.bstack111l1l1l_opy_ = value
  @classmethod
  def bstack1111ll1l1ll_opy_(cls):
    return cls.bstack111l1l1l_opy_
  @classmethod
  def bstack1l1l1l1l11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111l11111ll_opy_(cls):
    return cls.percy_build_id