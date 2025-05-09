# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
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
from bstack_utils.helper import bstack11llll11_opy_, bstack1lll1ll11l_opy_
from bstack_utils.measure import measure
class bstack1lll1l11ll_opy_:
  working_dir = os.getcwd()
  bstack1ll1ll11ll_opy_ = False
  config = {}
  bstack11ll1111111_opy_ = bstack11lll_opy_ (u"ࠬ࠭ᲊ")
  binary_path = bstack11lll_opy_ (u"࠭ࠧ᲋")
  bstack111llllll11_opy_ = bstack11lll_opy_ (u"ࠧࠨ᲌")
  bstack11l11l11l_opy_ = False
  bstack111llll1111_opy_ = None
  bstack11l11111l11_opy_ = {}
  bstack111llll11l1_opy_ = 300
  bstack11l111111l1_opy_ = False
  logger = None
  bstack111ll11ll1l_opy_ = False
  bstack1ll1lll1l1_opy_ = False
  percy_build_id = None
  bstack111lll1l111_opy_ = bstack11lll_opy_ (u"ࠨࠩ᲍")
  bstack111llll1ll1_opy_ = {
    bstack11lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ᲎") : 1,
    bstack11lll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ᲏") : 2,
    bstack11lll_opy_ (u"ࠫࡪࡪࡧࡦࠩᲐ") : 3,
    bstack11lll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬᲑ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111lll11ll1_opy_(self):
    bstack111ll1lll1l_opy_ = bstack11lll_opy_ (u"࠭ࠧᲒ")
    bstack111lll11l11_opy_ = sys.platform
    bstack111lllllll1_opy_ = bstack11lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Დ")
    if re.match(bstack11lll_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣᲔ"), bstack111lll11l11_opy_) != None:
      bstack111ll1lll1l_opy_ = bstack11ll1l11l1l_opy_ + bstack11lll_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥᲕ")
      self.bstack111lll1l111_opy_ = bstack11lll_opy_ (u"ࠪࡱࡦࡩࠧᲖ")
    elif re.match(bstack11lll_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤᲗ"), bstack111lll11l11_opy_) != None:
      bstack111ll1lll1l_opy_ = bstack11ll1l11l1l_opy_ + bstack11lll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨᲘ")
      bstack111lllllll1_opy_ = bstack11lll_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤᲙ")
      self.bstack111lll1l111_opy_ = bstack11lll_opy_ (u"ࠧࡸ࡫ࡱࠫᲚ")
    else:
      bstack111ll1lll1l_opy_ = bstack11ll1l11l1l_opy_ + bstack11lll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦᲛ")
      self.bstack111lll1l111_opy_ = bstack11lll_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨᲜ")
    return bstack111ll1lll1l_opy_, bstack111lllllll1_opy_
  def bstack111lll1l1l1_opy_(self):
    try:
      bstack111lll11111_opy_ = [os.path.join(expanduser(bstack11lll_opy_ (u"ࠥࢂࠧᲝ")), bstack11lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᲞ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111lll11111_opy_:
        if(self.bstack111llll1l11_opy_(path)):
          return path
      raise bstack11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᲟ")
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣᲠ").format(e))
  def bstack111llll1l11_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111lllll1ll_opy_(self, bstack111lllll111_opy_):
    return os.path.join(bstack111lllll111_opy_, self.bstack11ll1111111_opy_ + bstack11lll_opy_ (u"ࠢ࠯ࡧࡷࡥ࡬ࠨᲡ"))
  def bstack111ll1lll11_opy_(self, bstack111lllll111_opy_, bstack111lll1ll11_opy_):
    if not bstack111lll1ll11_opy_: return
    try:
      bstack111ll11llll_opy_ = self.bstack111lllll1ll_opy_(bstack111lllll111_opy_)
      with open(bstack111ll11llll_opy_, bstack11lll_opy_ (u"ࠣࡹࠥᲢ")) as f:
        f.write(bstack111lll1ll11_opy_)
        self.logger.debug(bstack11lll_opy_ (u"ࠤࡖࡥࡻ࡫ࡤࠡࡰࡨࡻࠥࡋࡔࡢࡩࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠨᲣ"))
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡹ࡮ࡥࠡࡧࡷࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᲤ").format(e))
  def bstack111lll1llll_opy_(self, bstack111lllll111_opy_):
    try:
      bstack111ll11llll_opy_ = self.bstack111lllll1ll_opy_(bstack111lllll111_opy_)
      if os.path.exists(bstack111ll11llll_opy_):
        with open(bstack111ll11llll_opy_, bstack11lll_opy_ (u"ࠦࡷࠨᲥ")) as f:
          bstack111lll1ll11_opy_ = f.read().strip()
          return bstack111lll1ll11_opy_ if bstack111lll1ll11_opy_ else None
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡅࡕࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᲦ").format(e))
  def bstack111ll11l1ll_opy_(self, bstack111lllll111_opy_, bstack111ll1lll1l_opy_):
    bstack111ll1l11l1_opy_ = self.bstack111lll1llll_opy_(bstack111lllll111_opy_)
    if bstack111ll1l11l1_opy_:
      try:
        bstack111lll111ll_opy_ = self.bstack111ll1ll111_opy_(bstack111ll1l11l1_opy_, bstack111ll1lll1l_opy_)
        if not bstack111lll111ll_opy_:
          self.logger.debug(bstack11lll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡳࠡࡷࡳࠤࡹࡵࠠࡥࡣࡷࡩࠥ࠮ࡅࡕࡣࡪࠤࡺࡴࡣࡩࡣࡱ࡫ࡪࡪࠩࠣᲧ"))
          return True
        self.logger.debug(bstack11lll_opy_ (u"ࠢࡏࡧࡺࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡵࡱࡦࡤࡸࡪࠨᲨ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡴࡸࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢᲩ").format(e))
    return False
  def bstack111ll1ll111_opy_(self, bstack111ll1l11l1_opy_, bstack111ll1lll1l_opy_):
    try:
      headers = {
        bstack11lll_opy_ (u"ࠤࡌࡪ࠲ࡔ࡯࡯ࡧ࠰ࡑࡦࡺࡣࡩࠤᲪ"): bstack111ll1l11l1_opy_
      }
      response = bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠪࡋࡊ࡚ࠧᲫ"), bstack111ll1lll1l_opy_, {}, {bstack11lll_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧᲬ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠽ࠤࢀࢃࠢᲭ").format(e))
  @measure(event_name=EVENTS.bstack11ll1lll11l_opy_, stage=STAGE.bstack11l111ll_opy_)
  def bstack111llllll1l_opy_(self, bstack111ll1lll1l_opy_, bstack111lllllll1_opy_):
    try:
      bstack11l1111l11l_opy_ = self.bstack111lll1l1l1_opy_()
      bstack111llllllll_opy_ = os.path.join(bstack11l1111l11l_opy_, bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩᲮ"))
      bstack11l111111ll_opy_ = os.path.join(bstack11l1111l11l_opy_, bstack111lllllll1_opy_)
      if self.bstack111ll11l1ll_opy_(bstack11l1111l11l_opy_, bstack111ll1lll1l_opy_):
        if os.path.exists(bstack11l111111ll_opy_):
          self.logger.info(bstack11lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᲯ").format(bstack11l111111ll_opy_))
          return bstack11l111111ll_opy_
        if os.path.exists(bstack111llllllll_opy_):
          self.logger.info(bstack11lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨᲰ").format(bstack111llllllll_opy_))
          return self.bstack111lllll11l_opy_(bstack111llllllll_opy_, bstack111lllllll1_opy_)
      self.logger.info(bstack11lll_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢᲱ").format(bstack111ll1lll1l_opy_))
      response = bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠪࡋࡊ࡚ࠧᲲ"), bstack111ll1lll1l_opy_, {}, {})
      if response.status_code == 200:
        bstack111ll1l1111_opy_ = response.headers.get(bstack11lll_opy_ (u"ࠦࡊ࡚ࡡࡨࠤᲳ"), bstack11lll_opy_ (u"ࠧࠨᲴ"))
        if bstack111ll1l1111_opy_:
          self.bstack111ll1lll11_opy_(bstack11l1111l11l_opy_, bstack111ll1l1111_opy_)
        with open(bstack111llllllll_opy_, bstack11lll_opy_ (u"࠭ࡷࡣࠩᲵ")) as file:
          file.write(response.content)
        self.logger.info(bstack11lll_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࢁࠧᲶ").format(bstack111llllllll_opy_))
        return self.bstack111lllll11l_opy_(bstack111llllllll_opy_, bstack111lllllll1_opy_)
      else:
        raise(bstack11lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࢀࠦᲷ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥᲸ").format(e))
  def bstack111ll1l111l_opy_(self, bstack111ll1lll1l_opy_, bstack111lllllll1_opy_):
    try:
      retry = 2
      bstack11l111111ll_opy_ = None
      bstack111lll11lll_opy_ = False
      while retry > 0:
        bstack11l111111ll_opy_ = self.bstack111llllll1l_opy_(bstack111ll1lll1l_opy_, bstack111lllllll1_opy_)
        bstack111lll11lll_opy_ = self.bstack111lll1ll1l_opy_(bstack111ll1lll1l_opy_, bstack111lllllll1_opy_, bstack11l111111ll_opy_)
        if bstack111lll11lll_opy_:
          break
        retry -= 1
      return bstack11l111111ll_opy_, bstack111lll11lll_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢᲹ").format(e))
    return bstack11l111111ll_opy_, False
  def bstack111lll1ll1l_opy_(self, bstack111ll1lll1l_opy_, bstack111lllllll1_opy_, bstack11l111111ll_opy_, bstack111lll111l1_opy_ = 0):
    if bstack111lll111l1_opy_ > 1:
      return False
    if bstack11l111111ll_opy_ == None or os.path.exists(bstack11l111111ll_opy_) == False:
      self.logger.warn(bstack11lll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᲺ"))
      return False
    bstack111ll1l1l11_opy_ = bstack11lll_opy_ (u"ࠧࡤ࠮ࠫࡂࡳࡩࡷࡩࡹ࡝࠱ࡦࡰ࡮ࠦ࡜ࡥ࠰࡟ࡨ࠰࠴࡜ࡥ࠭ࠥ᲻")
    command = bstack11lll_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᲼").format(bstack11l111111ll_opy_)
    bstack111lll1l1ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111ll1l1l11_opy_, bstack111lll1l1ll_opy_) != None:
      return True
    else:
      self.logger.error(bstack11lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨᲽ"))
      return False
  def bstack111lllll11l_opy_(self, bstack111llllllll_opy_, bstack111lllllll1_opy_):
    try:
      working_dir = os.path.dirname(bstack111llllllll_opy_)
      shutil.unpack_archive(bstack111llllllll_opy_, working_dir)
      bstack11l111111ll_opy_ = os.path.join(working_dir, bstack111lllllll1_opy_)
      os.chmod(bstack11l111111ll_opy_, 0o755)
      return bstack11l111111ll_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᲾ"))
  def bstack111llll111l_opy_(self):
    try:
      bstack111ll1ll11l_opy_ = self.config.get(bstack11lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᲿ"))
      bstack111llll111l_opy_ = bstack111ll1ll11l_opy_ or (bstack111ll1ll11l_opy_ is None and self.bstack1ll1ll11ll_opy_)
      if not bstack111llll111l_opy_ or self.config.get(bstack11lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭᳀"), None) not in bstack11ll1lll1ll_opy_:
        return False
      self.bstack11l11l11l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᳁").format(e))
  def bstack111ll1llll1_opy_(self):
    try:
      bstack111ll1llll1_opy_ = self.percy_capture_mode
      return bstack111ll1llll1_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠠࡤࡣࡳࡸࡺࡸࡥࠡ࡯ࡲࡨࡪ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᳂").format(e))
  def init(self, bstack1ll1ll11ll_opy_, config, logger):
    self.bstack1ll1ll11ll_opy_ = bstack1ll1ll11ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111llll111l_opy_():
      return
    self.bstack11l11111l11_opy_ = config.get(bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬ᳃"), {})
    self.percy_capture_mode = config.get(bstack11lll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ᳄"))
    try:
      bstack111ll1lll1l_opy_, bstack111lllllll1_opy_ = self.bstack111lll11ll1_opy_()
      self.bstack11ll1111111_opy_ = bstack111lllllll1_opy_
      bstack11l111111ll_opy_, bstack111lll11lll_opy_ = self.bstack111ll1l111l_opy_(bstack111ll1lll1l_opy_, bstack111lllllll1_opy_)
      if bstack111lll11lll_opy_:
        self.binary_path = bstack11l111111ll_opy_
        thread = Thread(target=self.bstack111llll11ll_opy_)
        thread.start()
      else:
        self.bstack111ll11ll1l_opy_ = True
        self.logger.error(bstack11lll_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦࡦࡰࡷࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤ࡚ࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡐࡦࡴࡦࡽࠧ᳅").format(bstack11l111111ll_opy_))
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ᳆").format(e))
  def bstack111lllll1l1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11lll_opy_ (u"ࠪࡰࡴ࡭ࠧ᳇"), bstack11lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡰࡴ࡭ࠧ᳈"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11lll_opy_ (u"ࠧࡖࡵࡴࡪ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࡵࠣࡥࡹࠦࡻࡾࠤ᳉").format(logfile))
      self.bstack111llllll11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࠢࡳࡥࡹ࡮ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ᳊").format(e))
  @measure(event_name=EVENTS.bstack11ll1ll11ll_opy_, stage=STAGE.bstack11l111ll_opy_)
  def bstack111llll11ll_opy_(self):
    bstack11l1111l111_opy_ = self.bstack111llll1l1l_opy_()
    if bstack11l1111l111_opy_ == None:
      self.bstack111ll11ll1l_opy_ = True
      self.logger.error(bstack11lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠥ᳋"))
      return False
    command_args = [bstack11lll_opy_ (u"ࠣࡣࡳࡴ࠿࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠤ᳌") if self.bstack1ll1ll11ll_opy_ else bstack11lll_opy_ (u"ࠩࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹ࠭᳍")]
    bstack11l11l11l1l_opy_ = self.bstack111ll1ll1l1_opy_()
    if bstack11l11l11l1l_opy_ != None:
      command_args.append(bstack11lll_opy_ (u"ࠥ࠱ࡨࠦࡻࡾࠤ᳎").format(bstack11l11l11l1l_opy_))
    env = os.environ.copy()
    env[bstack11lll_opy_ (u"ࠦࡕࡋࡒࡄ࡛ࡢࡘࡔࡑࡅࡏࠤ᳏")] = bstack11l1111l111_opy_
    env[bstack11lll_opy_ (u"࡚ࠧࡈࡠࡄࡘࡍࡑࡊ࡟ࡖࡗࡌࡈࠧ᳐")] = os.environ.get(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᳑"), bstack11lll_opy_ (u"ࠧࠨ᳒"))
    bstack111ll1l1lll_opy_ = [self.binary_path]
    self.bstack111lllll1l1_opy_()
    self.bstack111llll1111_opy_ = self.bstack111ll11l1l1_opy_(bstack111ll1l1lll_opy_ + command_args, env)
    self.logger.debug(bstack11lll_opy_ (u"ࠣࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠤ᳓"))
    bstack111lll111l1_opy_ = 0
    while self.bstack111llll1111_opy_.poll() == None:
      bstack111ll11ll11_opy_ = self.bstack111lll1lll1_opy_()
      if bstack111ll11ll11_opy_:
        self.logger.debug(bstack11lll_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰ᳔ࠧ"))
        self.bstack11l111111l1_opy_ = True
        return True
      bstack111lll111l1_opy_ += 1
      self.logger.debug(bstack11lll_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡕࡩࡹࡸࡹࠡ࠯ࠣࡿࢂࠨ᳕").format(bstack111lll111l1_opy_))
      time.sleep(2)
    self.logger.error(bstack11lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡌࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࢀࢃࠠࡢࡶࡷࡩࡲࡶࡴࡴࠤ᳖").format(bstack111lll111l1_opy_))
    self.bstack111ll11ll1l_opy_ = True
    return False
  def bstack111lll1lll1_opy_(self, bstack111lll111l1_opy_ = 0):
    if bstack111lll111l1_opy_ > 10:
      return False
    try:
      bstack111ll1l1l1l_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡘࡋࡒࡗࡇࡕࡣࡆࡊࡄࡓࡇࡖࡗ᳗ࠬ"), bstack11lll_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵ࠼࠸࠷࠸࠾᳘ࠧ"))
      bstack11l1111111l_opy_ = bstack111ll1l1l1l_opy_ + bstack11ll11llll1_opy_
      response = requests.get(bstack11l1111111l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ᳙࠭"), {}).get(bstack11lll_opy_ (u"ࠨ࡫ࡧࠫ᳚"), None)
      return True
    except:
      self.logger.debug(bstack11lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡨࡦࡣ࡯ࡸ࡭ࠦࡣࡩࡧࡦ࡯ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ᳛"))
      return False
  def bstack111llll1l1l_opy_(self):
    bstack11l11111l1l_opy_ = bstack11lll_opy_ (u"ࠪࡥࡵࡶ᳜ࠧ") if self.bstack1ll1ll11ll_opy_ else bstack11lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ᳝࠭")
    bstack111ll1ll1ll_opy_ = bstack11lll_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ᳞ࠣ") if self.config.get(bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽ᳟ࠬ")) is None else True
    bstack11ll1111l1l_opy_ = bstack11lll_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠬࡰࡦࡴࡦࡽࡂࢁࡽࠣ᳠").format(self.config[bstack11lll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᳡")], bstack11l11111l1l_opy_, bstack111ll1ll1ll_opy_)
    if self.percy_capture_mode:
      bstack11ll1111l1l_opy_ += bstack11lll_opy_ (u"ࠤࠩࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥ࠾ࡽࢀ᳢ࠦ").format(self.percy_capture_mode)
    uri = bstack11llll11_opy_(bstack11ll1111l1l_opy_)
    try:
      response = bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠪࡋࡊ᳣࡚ࠧ"), uri, {}, {bstack11lll_opy_ (u"ࠫࡦࡻࡴࡩ᳤ࠩ"): (self.config[bstack11lll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫᳥ࠧ")], self.config[bstack11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺ᳦ࠩ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l11l11l_opy_ = data.get(bstack11lll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ᳧"))
        self.percy_capture_mode = data.get(bstack11lll_opy_ (u"ࠨࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪ᳨࠭"))
        os.environ[bstack11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧᳩ")] = str(self.bstack11l11l11l_opy_)
        os.environ[bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧᳪ")] = str(self.percy_capture_mode)
        if bstack111ll1ll1ll_opy_ == bstack11lll_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢᳫ") and str(self.bstack11l11l11l_opy_).lower() == bstack11lll_opy_ (u"ࠧࡺࡲࡶࡧࠥᳬ"):
          self.bstack1ll1lll1l1_opy_ = True
        if bstack11lll_opy_ (u"ࠨࡴࡰ࡭ࡨࡲ᳭ࠧ") in data:
          return data[bstack11lll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᳮ")]
        else:
          raise bstack11lll_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨᳯ").format(data)
      else:
        raise bstack11lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤᳰ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦᳱ").format(e))
  def bstack111ll1ll1l1_opy_(self):
    bstack111lll11l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢᳲ"))
    try:
      if bstack11lll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᳳ") not in self.bstack11l11111l11_opy_:
        self.bstack11l11111l11_opy_[bstack11lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᳴")] = 2
      with open(bstack111lll11l1l_opy_, bstack11lll_opy_ (u"ࠧࡸࠩᳵ")) as fp:
        json.dump(self.bstack11l11111l11_opy_, fp)
      return bstack111lll11l1l_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᳶ").format(e))
  def bstack111ll11l1l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lll1l111_opy_ == bstack11lll_opy_ (u"ࠩࡺ࡭ࡳ࠭᳷"):
        bstack111llll1lll_opy_ = [bstack11lll_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨࠫ᳸"), bstack11lll_opy_ (u"ࠫ࠴ࡩࠧ᳹")]
        cmd = bstack111llll1lll_opy_ + cmd
      cmd = bstack11lll_opy_ (u"ࠬࠦࠧᳺ").join(cmd)
      self.logger.debug(bstack11lll_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿࠥ᳻").format(cmd))
      with open(self.bstack111llllll11_opy_, bstack11lll_opy_ (u"ࠢࡢࠤ᳼")) as bstack111ll1l11ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111ll1l11ll_opy_, text=True, stderr=bstack111ll1l11ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111ll11ll1l_opy_ = True
      self.logger.error(bstack11lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥ᳽").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l111111l1_opy_:
        self.logger.info(bstack11lll_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥ᳾"))
        cmd = [self.binary_path, bstack11lll_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨ᳿")]
        self.bstack111ll11l1l1_opy_(cmd)
        self.bstack11l111111l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᴀ").format(cmd, e))
  def bstack1ll11llll_opy_(self):
    if not self.bstack11l11l11l_opy_:
      return
    try:
      bstack111lll1111l_opy_ = 0
      while not self.bstack11l111111l1_opy_ and bstack111lll1111l_opy_ < self.bstack111llll11l1_opy_:
        if self.bstack111ll11ll1l_opy_:
          self.logger.info(bstack11lll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦࠥᴁ"))
          return
        time.sleep(1)
        bstack111lll1111l_opy_ += 1
      os.environ[bstack11lll_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᴂ")] = str(self.bstack111ll1lllll_opy_())
      self.logger.info(bstack11lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣᴃ"))
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᴄ").format(e))
  def bstack111ll1lllll_opy_(self):
    if self.bstack1ll1ll11ll_opy_:
      return
    try:
      bstack111ll1l1ll1_opy_ = [platform[bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᴅ")].lower() for platform in self.config.get(bstack11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᴆ"), [])]
      bstack111ll11lll1_opy_ = sys.maxsize
      bstack111lll1l11l_opy_ = bstack11lll_opy_ (u"ࠫࠬᴇ")
      for browser in bstack111ll1l1ll1_opy_:
        if browser in self.bstack111llll1ll1_opy_:
          bstack11l11111ll1_opy_ = self.bstack111llll1ll1_opy_[browser]
        if bstack11l11111ll1_opy_ < bstack111ll11lll1_opy_:
          bstack111ll11lll1_opy_ = bstack11l11111ll1_opy_
          bstack111lll1l11l_opy_ = browser
      return bstack111lll1l11l_opy_
    except Exception as e:
      self.logger.error(bstack11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᴈ").format(e))
  @classmethod
  def bstack1l111lll11_opy_(self):
    return os.getenv(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫᴉ"), bstack11lll_opy_ (u"ࠧࡇࡣ࡯ࡷࡪ࠭ᴊ")).lower()
  @classmethod
  def bstack1ll1l11ll1_opy_(self):
    return os.getenv(bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᴋ"), bstack11lll_opy_ (u"ࠩࠪᴌ"))
  @classmethod
  def bstack1l1ll1l1lll_opy_(cls, value):
    cls.bstack1ll1lll1l1_opy_ = value
  @classmethod
  def bstack11l11111111_opy_(cls):
    return cls.bstack1ll1lll1l1_opy_
  @classmethod
  def bstack1l1ll11llll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11l11111lll_opy_(cls):
    return cls.percy_build_id