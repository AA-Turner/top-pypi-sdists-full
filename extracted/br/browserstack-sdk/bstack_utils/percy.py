# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
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
from bstack_utils.helper import bstack1llll111l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111111ll_opy_ import bstack1ll1l1ll_opy_
class bstack1111l11l1_opy_:
  working_dir = os.getcwd()
  bstack1lll11111_opy_ = False
  config = {}
  bstack11l11111lll_opy_ = bstack111l111_opy_ (u"ࠧࠨḢ")
  binary_path = bstack111l111_opy_ (u"ࠨࠩḣ")
  bstack111l111l111_opy_ = bstack111l111_opy_ (u"ࠩࠪḤ")
  bstack1111l11l_opy_ = False
  bstack1111ll1ll11_opy_ = None
  bstack1111ll1ll1l_opy_ = {}
  bstack1111ll1llll_opy_ = 300
  bstack1111lllllll_opy_ = False
  logger = None
  bstack1111l1ll1l1_opy_ = False
  bstack1ll11llll_opy_ = False
  percy_build_id = None
  bstack1111l1lll1l_opy_ = bstack111l111_opy_ (u"ࠪࠫḥ")
  bstack1111ll1l1l1_opy_ = {
    bstack111l111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫḦ") : 1,
    bstack111l111_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ḧ") : 2,
    bstack111l111_opy_ (u"࠭ࡥࡥࡩࡨࠫḨ") : 3,
    bstack111l111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧḩ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1111l1ll11l_opy_(self):
    bstack1111ll111l1_opy_ = bstack111l111_opy_ (u"ࠨࠩḪ")
    bstack111l1111ll1_opy_ = sys.platform
    bstack1111lll1ll1_opy_ = bstack111l111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨḫ")
    if re.match(bstack111l111_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥḬ"), bstack111l1111ll1_opy_) != None:
      bstack1111ll111l1_opy_ = bstack11l1lll11l1_opy_ + bstack111l111_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧḭ")
      self.bstack1111l1lll1l_opy_ = bstack111l111_opy_ (u"ࠬࡳࡡࡤࠩḮ")
    elif re.match(bstack111l111_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦḯ"), bstack111l1111ll1_opy_) != None:
      bstack1111ll111l1_opy_ = bstack11l1lll11l1_opy_ + bstack111l111_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣḰ")
      bstack1111lll1ll1_opy_ = bstack111l111_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦḱ")
      self.bstack1111l1lll1l_opy_ = bstack111l111_opy_ (u"ࠩࡺ࡭ࡳ࠭Ḳ")
    else:
      bstack1111ll111l1_opy_ = bstack11l1lll11l1_opy_ + bstack111l111_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨḳ")
      self.bstack1111l1lll1l_opy_ = bstack111l111_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪḴ")
    return bstack1111ll111l1_opy_, bstack1111lll1ll1_opy_
  def bstack1111l11l1l1_opy_(self):
    try:
      bstack1111l1l1111_opy_ = [os.path.join(expanduser(bstack111l111_opy_ (u"ࠧࢄࠢḵ")), bstack111l111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ḷ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111l1l1111_opy_:
        if(self.bstack1111lll1lll_opy_(path)):
          return path
      raise bstack111l111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦḷ")
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥḸ").format(e))
  def bstack1111lll1lll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111l11l111_opy_(self, bstack1111ll1l11l_opy_):
    return os.path.join(bstack1111ll1l11l_opy_, self.bstack11l11111lll_opy_ + bstack111l111_opy_ (u"ࠤ࠱ࡩࡹࡧࡧࠣḹ"))
  def bstack1111l11llll_opy_(self, bstack1111ll1l11l_opy_, bstack1111llllll1_opy_):
    if not bstack1111llllll1_opy_: return
    try:
      bstack1111lll1111_opy_ = self.bstack1111l11l111_opy_(bstack1111ll1l11l_opy_)
      with open(bstack1111lll1111_opy_, bstack111l111_opy_ (u"ࠥࡻࠧḺ")) as f:
        f.write(bstack1111llllll1_opy_)
        self.logger.debug(bstack111l111_opy_ (u"ࠦࡘࡧࡶࡦࡦࠣࡲࡪࡽࠠࡆࡖࡤ࡫ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠣḻ"))
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡴࡩࡧࠣࡩࡹࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧḼ").format(e))
  def bstack1111lll11l1_opy_(self, bstack1111ll1l11l_opy_):
    try:
      bstack1111lll1111_opy_ = self.bstack1111l11l111_opy_(bstack1111ll1l11l_opy_)
      if os.path.exists(bstack1111lll1111_opy_):
        with open(bstack1111lll1111_opy_, bstack111l111_opy_ (u"ࠨࡲࠣḽ")) as f:
          bstack1111llllll1_opy_ = f.read().strip()
          return bstack1111llllll1_opy_ if bstack1111llllll1_opy_ else None
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠ࡭ࡱࡤࡨ࡮ࡴࡧࠡࡇࡗࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥḾ").format(e))
  def bstack1111l1llll1_opy_(self, bstack1111ll1l11l_opy_, bstack1111ll111l1_opy_):
    bstack1111lll111l_opy_ = self.bstack1111lll11l1_opy_(bstack1111ll1l11l_opy_)
    if bstack1111lll111l_opy_:
      try:
        bstack1111l11l1ll_opy_ = self.bstack111l1111111_opy_(bstack1111lll111l_opy_, bstack1111ll111l1_opy_)
        if not bstack1111l11l1ll_opy_:
          self.logger.debug(bstack111l111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡵࠣࡹࡵࠦࡴࡰࠢࡧࡥࡹ࡫ࠠࠩࡇࡗࡥ࡬ࠦࡵ࡯ࡥ࡫ࡥࡳ࡭ࡥࡥࠫࠥḿ"))
          return True
        self.logger.debug(bstack111l111_opy_ (u"ࠤࡑࡩࡼࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡥࠣṀ"))
        return False
      except Exception as e:
        self.logger.warn(bstack111l111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡬࡯ࡳࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤṁ").format(e))
    return False
  def bstack111l1111111_opy_(self, bstack1111lll111l_opy_, bstack1111ll111l1_opy_):
    try:
      headers = {
        bstack111l111_opy_ (u"ࠦࡎ࡬࠭ࡏࡱࡱࡩ࠲ࡓࡡࡵࡥ࡫ࠦṂ"): bstack1111lll111l_opy_
      }
      response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠬࡍࡅࡕࠩṃ"), bstack1111ll111l1_opy_, {}, {bstack111l111_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢṄ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack111l111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠿ࠦࡻࡾࠤṅ").format(e))
  @measure(event_name=EVENTS.bstack11l1l1lllll_opy_, stage=STAGE.bstack11l1llll1_opy_)
  def bstack1111llll1l1_opy_(self, bstack1111ll111l1_opy_, bstack1111lll1ll1_opy_):
    try:
      bstack1111l11lll1_opy_ = self.bstack1111l11l1l1_opy_()
      bstack1111l11l11l_opy_ = os.path.join(bstack1111l11lll1_opy_, bstack111l111_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫṆ"))
      bstack1111l1l1lll_opy_ = os.path.join(bstack1111l11lll1_opy_, bstack1111lll1ll1_opy_)
      if self.bstack1111l1llll1_opy_(bstack1111l11lll1_opy_, bstack1111ll111l1_opy_): # if bstack1111l1ll1ll_opy_, bstack1l1l11l1l1l_opy_ bstack1111llllll1_opy_ is bstack1111llll1ll_opy_ to bstack11l11ll1lll_opy_ version available (response 304)
        if os.path.exists(bstack1111l1l1lll_opy_):
          self.logger.info(bstack111l111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦṇ").format(bstack1111l1l1lll_opy_))
          return bstack1111l1l1lll_opy_
        if os.path.exists(bstack1111l11l11l_opy_):
          self.logger.info(bstack111l111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣṈ").format(bstack1111l11l11l_opy_))
          return self.bstack1111lll1l11_opy_(bstack1111l11l11l_opy_, bstack1111lll1ll1_opy_)
      self.logger.info(bstack111l111_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤṉ").format(bstack1111ll111l1_opy_))
      response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠬࡍࡅࡕࠩṊ"), bstack1111ll111l1_opy_, {}, {})
      if response.status_code == 200:
        bstack111l11111l1_opy_ = response.headers.get(bstack111l111_opy_ (u"ࠨࡅࡕࡣࡪࠦṋ"), bstack111l111_opy_ (u"ࠢࠣṌ"))
        if bstack111l11111l1_opy_:
          self.bstack1111l11llll_opy_(bstack1111l11lll1_opy_, bstack111l11111l1_opy_)
        with open(bstack1111l11l11l_opy_, bstack111l111_opy_ (u"ࠨࡹࡥࠫṍ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l111_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢṎ").format(bstack1111l11l11l_opy_))
        return self.bstack1111lll1l11_opy_(bstack1111l11l11l_opy_, bstack1111lll1ll1_opy_)
      else:
        raise(bstack111l111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨṏ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧṐ").format(e))
  def bstack1111lll11ll_opy_(self, bstack1111ll111l1_opy_, bstack1111lll1ll1_opy_):
    try:
      retry = 2
      bstack1111l1l1lll_opy_ = None
      bstack1111l1l1l11_opy_ = False
      while retry > 0:
        bstack1111l1l1lll_opy_ = self.bstack1111llll1l1_opy_(bstack1111ll111l1_opy_, bstack1111lll1ll1_opy_)
        bstack1111l1l1l11_opy_ = self.bstack1111ll11l1l_opy_(bstack1111ll111l1_opy_, bstack1111lll1ll1_opy_, bstack1111l1l1lll_opy_)
        if bstack1111l1l1l11_opy_:
          break
        retry -= 1
      return bstack1111l1l1lll_opy_, bstack1111l1l1l11_opy_
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤṑ").format(e))
    return bstack1111l1l1lll_opy_, False
  def bstack1111ll11l1l_opy_(self, bstack1111ll111l1_opy_, bstack1111lll1ll1_opy_, bstack1111l1l1lll_opy_, bstack1111llll11l_opy_ = 0):
    if bstack1111llll11l_opy_ > 1:
      return False
    if bstack1111l1l1lll_opy_ == None or os.path.exists(bstack1111l1l1lll_opy_) == False:
      self.logger.warn(bstack111l111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦṒ"))
      return False
    bstack111l111111l_opy_ = bstack111l111_opy_ (u"ࡲࠣࡠ࠱࠮ࡅࡶࡥࡳࡥࡼ࠳ࡨࡲࡩࠡ࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭࡟࠲ࡡࡪࠫࠣṓ")
    command = bstack111l111_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧṔ").format(bstack1111l1l1lll_opy_)
    bstack1111lllll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l111111l_opy_, bstack1111lllll11_opy_) != None:
      return True
    else:
      self.logger.error(bstack111l111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣṕ"))
      return False
  def bstack1111lll1l11_opy_(self, bstack1111l11l11l_opy_, bstack1111lll1ll1_opy_):
    try:
      working_dir = os.path.dirname(bstack1111l11l11l_opy_)
      shutil.unpack_archive(bstack1111l11l11l_opy_, working_dir)
      bstack1111l1l1lll_opy_ = os.path.join(working_dir, bstack1111lll1ll1_opy_)
      os.chmod(bstack1111l1l1lll_opy_, 0o755)
      return bstack1111l1l1lll_opy_
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦṖ"))
  def bstack1111l1l111l_opy_(self):
    try:
      bstack1111l1lllll_opy_ = self.config.get(bstack111l111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪṗ"))
      bstack1111l1l111l_opy_ = bstack1111l1lllll_opy_ or (bstack1111l1lllll_opy_ is None and self.bstack1lll11111_opy_)
      if not bstack1111l1l111l_opy_ or self.config.get(bstack111l111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨṘ"), None) not in bstack11l1llll1ll_opy_:
        return False
      self.bstack1111l11l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣṙ").format(e))
  def bstack1111ll1111l_opy_(self):
    try:
      bstack1111ll1111l_opy_ = self.percy_capture_mode
      return bstack1111ll1111l_opy_
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣṚ").format(e))
  def init(self, bstack1lll11111_opy_, config, logger):
    self.bstack1lll11111_opy_ = bstack1lll11111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111l1l111l_opy_():
      return
    self.bstack1111ll1ll1l_opy_ = config.get(bstack111l111_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧṛ"), {})
    self.percy_capture_mode = config.get(bstack111l111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬṜ"))
    try:
      bstack1111ll111l1_opy_, bstack1111lll1ll1_opy_ = self.bstack1111l1ll11l_opy_()
      self.bstack11l11111lll_opy_ = bstack1111lll1ll1_opy_
      bstack1111l1l1lll_opy_, bstack1111l1l1l11_opy_ = self.bstack1111lll11ll_opy_(bstack1111ll111l1_opy_, bstack1111lll1ll1_opy_)
      if bstack1111l1l1l11_opy_:
        self.binary_path = bstack1111l1l1lll_opy_
        thread = Thread(target=self.bstack1111l1l1l1l_opy_)
        thread.start()
      else:
        self.bstack1111l1ll1l1_opy_ = True
        self.logger.error(bstack111l111_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢṝ").format(bstack1111l1l1lll_opy_))
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧṞ").format(e))
  def bstack1111ll11l11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111l111_opy_ (u"ࠬࡲ࡯ࡨࠩṟ"), bstack111l111_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩṠ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111l111_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦṡ").format(logfile))
      self.bstack111l111l111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤṢ").format(e))
  @measure(event_name=EVENTS.bstack11l1llll1l1_opy_, stage=STAGE.bstack11l1llll1_opy_)
  def bstack1111l1l1l1l_opy_(self):
    bstack1111l1lll11_opy_ = self.bstack1111llll111_opy_()
    if bstack1111l1lll11_opy_ == None:
      self.bstack1111l1ll1l1_opy_ = True
      self.logger.error(bstack111l111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧṣ"))
      return False
    command_args = [bstack111l111_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦṤ") if self.bstack1lll11111_opy_ else bstack111l111_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨṥ")]
    bstack111l1lllll1_opy_ = self.bstack1111ll111ll_opy_()
    if bstack111l1lllll1_opy_ != None:
      command_args.append(bstack111l111_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦṦ").format(bstack111l1lllll1_opy_))
    env = os.environ.copy()
    env[bstack111l111_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦṧ")] = bstack1111l1lll11_opy_
    env[bstack111l111_opy_ (u"ࠢࡕࡊࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠢṨ")] = os.environ.get(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ṩ"), bstack111l111_opy_ (u"ࠩࠪṪ"))
    bstack1111lll1l1l_opy_ = [self.binary_path]
    self.bstack1111ll11l11_opy_()
    self.bstack1111ll1ll11_opy_ = self.bstack1111ll1l1ll_opy_(bstack1111lll1l1l_opy_ + command_args, env)
    self.logger.debug(bstack111l111_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦṫ"))
    bstack1111llll11l_opy_ = 0
    while self.bstack1111ll1ll11_opy_.poll() == None:
      bstack1111ll1l111_opy_ = self.bstack1111ll11lll_opy_()
      if bstack1111ll1l111_opy_:
        self.logger.debug(bstack111l111_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢṬ"))
        self.bstack1111lllllll_opy_ = True
        return True
      bstack1111llll11l_opy_ += 1
      self.logger.debug(bstack111l111_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣṭ").format(bstack1111llll11l_opy_))
      time.sleep(2)
    self.logger.error(bstack111l111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦṮ").format(bstack1111llll11l_opy_))
    self.bstack1111l1ll1l1_opy_ = True
    return False
  def bstack1111ll11lll_opy_(self, bstack1111llll11l_opy_ = 0):
    if bstack1111llll11l_opy_ > 10:
      return False
    try:
      bstack1111l1l1ll1_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧṯ"), bstack111l111_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩṰ"))
      bstack1111l1l11ll_opy_ = bstack1111l1l1ll1_opy_ + bstack11l1ll11l1l_opy_
      response = requests.get(bstack1111l1l11ll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨṱ"), {}).get(bstack111l111_opy_ (u"ࠪ࡭ࡩ࠭Ṳ"), None)
      return True
    except:
      self.logger.debug(bstack111l111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡪࡨࡥࡱࡺࡨࠡࡥ࡫ࡩࡨࡱࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤṳ"))
      return False
  def bstack1111llll111_opy_(self):
    bstack111l11111ll_opy_ = bstack111l111_opy_ (u"ࠬࡧࡰࡱࠩṴ") if self.bstack1lll11111_opy_ else bstack111l111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨṵ")
    bstack1111ll11111_opy_ = bstack111l111_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥṶ") if self.config.get(bstack111l111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧṷ")) is None else True
    bstack11ll11l1l11_opy_ = bstack111l111_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠧࡲࡨࡶࡨࡿ࠽ࡼࡿࠥṸ").format(self.config[bstack111l111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨṹ")], bstack111l11111ll_opy_, bstack1111ll11111_opy_)
    if self.percy_capture_mode:
      bstack11ll11l1l11_opy_ += bstack111l111_opy_ (u"ࠦࠫࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࡀࡿࢂࠨṺ").format(self.percy_capture_mode)
    uri = bstack1ll1l1ll_opy_(bstack11ll11l1l11_opy_)
    try:
      response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠬࡍࡅࡕࠩṻ"), uri, {}, {bstack111l111_opy_ (u"࠭ࡡࡶࡶ࡫ࠫṼ"): (self.config[bstack111l111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩṽ")], self.config[bstack111l111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫṾ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1111l11l_opy_ = data.get(bstack111l111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪṿ"))
        self.percy_capture_mode = data.get(bstack111l111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥࠨẀ"))
        os.environ[bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩẁ")] = str(self.bstack1111l11l_opy_)
        os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩẂ")] = str(self.percy_capture_mode)
        if bstack1111ll11111_opy_ == bstack111l111_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤẃ") and str(self.bstack1111l11l_opy_).lower() == bstack111l111_opy_ (u"ࠢࡵࡴࡸࡩࠧẄ"):
          self.bstack1ll11llll_opy_ = True
        if bstack111l111_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢẅ") in data:
          return data[bstack111l111_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣẆ")]
        else:
          raise bstack111l111_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪẇ").format(data)
      else:
        raise bstack111l111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦẈ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨẉ").format(e))
  def bstack1111ll111ll_opy_(self):
    bstack1111ll1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤẊ"))
    try:
      if bstack111l111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨẋ") not in self.bstack1111ll1ll1l_opy_:
        self.bstack1111ll1ll1l_opy_[bstack111l111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩẌ")] = 2
      with open(bstack1111ll1lll1_opy_, bstack111l111_opy_ (u"ࠩࡺࠫẍ")) as fp:
        json.dump(self.bstack1111ll1ll1l_opy_, fp)
      return bstack1111ll1lll1_opy_
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥẎ").format(e))
  def bstack1111ll1l1ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111l1lll1l_opy_ == bstack111l111_opy_ (u"ࠫࡼ࡯࡮ࠨẏ"):
        bstack1111l11ll1l_opy_ = [bstack111l111_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭Ẑ"), bstack111l111_opy_ (u"࠭࠯ࡤࠩẑ")]
        cmd = bstack1111l11ll1l_opy_ + cmd
      cmd = bstack111l111_opy_ (u"ࠧࠡࠩẒ").join(cmd)
      self.logger.debug(bstack111l111_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧẓ").format(cmd))
      with open(self.bstack111l111l111_opy_, bstack111l111_opy_ (u"ࠤࡤࠦẔ")) as bstack111l111l11l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111l111l11l_opy_, text=True, stderr=bstack111l111l11l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111l1ll1l1_opy_ = True
      self.logger.error(bstack111l111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧẕ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111lllllll_opy_:
        self.logger.info(bstack111l111_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧẖ"))
        cmd = [self.binary_path, bstack111l111_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣẗ")]
        self.bstack1111ll1l1ll_opy_(cmd)
        self.bstack1111lllllll_opy_ = False
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨẘ").format(cmd, e))
  def bstack11ll111l1l_opy_(self):
    if not self.bstack1111l11l_opy_:
      return
    try:
      bstack111l1111l1l_opy_ = 0
      while not self.bstack1111lllllll_opy_ and bstack111l1111l1l_opy_ < self.bstack1111ll1llll_opy_:
        if self.bstack1111l1ll1l1_opy_:
          self.logger.info(bstack111l111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧẙ"))
          return
        time.sleep(1)
        bstack111l1111l1l_opy_ += 1
      os.environ[bstack111l111_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧẚ")] = str(self.bstack111l1111l11_opy_())
      self.logger.info(bstack111l111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥẛ"))
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦẜ").format(e))
  def bstack111l1111l11_opy_(self):
    if self.bstack1lll11111_opy_:
      return
    try:
      bstack1111l1l11l1_opy_ = [platform[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩẝ")].lower() for platform in self.config.get(bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨẞ"), [])]
      bstack1111l11ll11_opy_ = sys.maxsize
      bstack1111ll11ll1_opy_ = bstack111l111_opy_ (u"࠭ࠧẟ")
      for browser in bstack1111l1l11l1_opy_:
        if browser in self.bstack1111ll1l1l1_opy_:
          bstack1111l1ll111_opy_ = self.bstack1111ll1l1l1_opy_[browser]
        if bstack1111l1ll111_opy_ < bstack1111l11ll11_opy_:
          bstack1111l11ll11_opy_ = bstack1111l1ll111_opy_
          bstack1111ll11ll1_opy_ = browser
      return bstack1111ll11ll1_opy_
    except Exception as e:
      self.logger.error(bstack111l111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣẠ").format(e))
  @classmethod
  def bstack1l11ll111_opy_(self):
    return os.getenv(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ạ"), bstack111l111_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨẢ")).lower()
  @classmethod
  def bstack1l111llll1_opy_(self):
    return os.getenv(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧả"), bstack111l111_opy_ (u"ࠫࠬẤ"))
  @classmethod
  def bstack1l1l1l111ll_opy_(cls, value):
    cls.bstack1ll11llll_opy_ = value
  @classmethod
  def bstack1111lllll1l_opy_(cls):
    return cls.bstack1ll11llll_opy_
  @classmethod
  def bstack1l1l1l111l1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111l1111lll_opy_(cls):
    return cls.percy_build_id