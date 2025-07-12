# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
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
from bstack_utils.bstack1l1lll1l1l_opy_ import bstack11111111_opy_
class bstack11ll11l111_opy_:
  working_dir = os.getcwd()
  bstack1l1ll1ll1_opy_ = False
  config = {}
  bstack11l1l1l1ll1_opy_ = bstack11l1111_opy_ (u"ࠨࠩᙃ")
  binary_path = bstack11l1111_opy_ (u"ࠩࠪᙄ")
  bstack11l1l1l11ll_opy_ = bstack11l1111_opy_ (u"ࠪࠫᙅ")
  bstack11ll1111l1_opy_ = False
  bstack11ll11ll111_opy_ = None
  bstack11l1lll1l1l_opy_ = {}
  bstack11l1ll1ll11_opy_ = 300
  bstack11l1lllllll_opy_ = False
  logger = None
  bstack11ll111lll1_opy_ = False
  bstack1lllll11ll_opy_ = False
  percy_build_id = None
  bstack11l1lllll1l_opy_ = bstack11l1111_opy_ (u"ࠫࠬᙆ")
  bstack11l1lll1ll1_opy_ = {
    bstack11l1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᙇ") : 1,
    bstack11l1111_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᙈ") : 2,
    bstack11l1111_opy_ (u"ࠧࡦࡦࡪࡩࠬᙉ") : 3,
    bstack11l1111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᙊ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11l1l1llll1_opy_(self):
    bstack11l1ll1l1ll_opy_ = bstack11l1111_opy_ (u"ࠩࠪᙋ")
    bstack11ll1111l1l_opy_ = sys.platform
    bstack11ll1111l11_opy_ = bstack11l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᙌ")
    if re.match(bstack11l1111_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᙍ"), bstack11ll1111l1l_opy_) != None:
      bstack11l1ll1l1ll_opy_ = bstack11l1ll1l1l1_opy_ + bstack11l1111_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᙎ")
      self.bstack11l1lllll1l_opy_ = bstack11l1111_opy_ (u"࠭࡭ࡢࡥࠪᙏ")
    elif re.match(bstack11l1111_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᙐ"), bstack11ll1111l1l_opy_) != None:
      bstack11l1ll1l1ll_opy_ = bstack11l1ll1l1l1_opy_ + bstack11l1111_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᙑ")
      bstack11ll1111l11_opy_ = bstack11l1111_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᙒ")
      self.bstack11l1lllll1l_opy_ = bstack11l1111_opy_ (u"ࠪࡻ࡮ࡴࠧᙓ")
    else:
      bstack11l1ll1l1ll_opy_ = bstack11l1ll1l1l1_opy_ + bstack11l1111_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᙔ")
      self.bstack11l1lllll1l_opy_ = bstack11l1111_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᙕ")
    return bstack11l1ll1l1ll_opy_, bstack11ll1111l11_opy_
  def bstack11ll11l11ll_opy_(self):
    try:
      bstack11l1l1lll1l_opy_ = [os.path.join(expanduser(bstack11l1111_opy_ (u"ࠨࡾࠣᙖ")), bstack11l1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᙗ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l1l1lll1l_opy_:
        if(self.bstack11l1l1lll11_opy_(path)):
          return path
      raise bstack11l1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᙘ")
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᙙ").format(e))
  def bstack11l1l1lll11_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11l1llll11l_opy_(self, bstack11ll1111111_opy_):
    return os.path.join(bstack11ll1111111_opy_, self.bstack11l1l1l1ll1_opy_ + bstack11l1111_opy_ (u"ࠥ࠲ࡪࡺࡡࡨࠤᙚ"))
  def bstack11l1l1l1l11_opy_(self, bstack11ll1111111_opy_, bstack11l1l11llll_opy_):
    if not bstack11l1l11llll_opy_: return
    try:
      bstack11ll111111l_opy_ = self.bstack11l1llll11l_opy_(bstack11ll1111111_opy_)
      with open(bstack11ll111111l_opy_, bstack11l1111_opy_ (u"ࠦࡼࠨᙛ")) as f:
        f.write(bstack11l1l11llll_opy_)
        self.logger.debug(bstack11l1111_opy_ (u"࡙ࠧࡡࡷࡧࡧࠤࡳ࡫ࡷࠡࡇࡗࡥ࡬ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠤᙜ"))
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡵࡪࡨࠤࡪࡺࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᙝ").format(e))
  def bstack11l1llllll1_opy_(self, bstack11ll1111111_opy_):
    try:
      bstack11ll111111l_opy_ = self.bstack11l1llll11l_opy_(bstack11ll1111111_opy_)
      if os.path.exists(bstack11ll111111l_opy_):
        with open(bstack11ll111111l_opy_, bstack11l1111_opy_ (u"ࠢࡳࠤᙞ")) as f:
          bstack11l1l11llll_opy_ = f.read().strip()
          return bstack11l1l11llll_opy_ if bstack11l1l11llll_opy_ else None
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡ࡮ࡲࡥࡩ࡯࡮ࡨࠢࡈࡘࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᙟ").format(e))
  def bstack11l1ll1l11l_opy_(self, bstack11ll1111111_opy_, bstack11l1ll1l1ll_opy_):
    bstack11ll11l1111_opy_ = self.bstack11l1llllll1_opy_(bstack11ll1111111_opy_)
    if bstack11ll11l1111_opy_:
      try:
        bstack11ll111l1l1_opy_ = self.bstack11l1l1l1lll_opy_(bstack11ll11l1111_opy_, bstack11l1ll1l1ll_opy_)
        if not bstack11ll111l1l1_opy_:
          self.logger.debug(bstack11l1111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡶࠤࡺࡶࠠࡵࡱࠣࡨࡦࡺࡥࠡࠪࡈࡘࡦ࡭ࠠࡶࡰࡦ࡬ࡦࡴࡧࡦࡦࠬࠦᙠ"))
          return True
        self.logger.debug(bstack11l1111_opy_ (u"ࠥࡒࡪࡽࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡦࠤᙡ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11l1111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡦࡰࡴࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠰ࠥࡻࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥᙢ").format(e))
    return False
  def bstack11l1l1l1lll_opy_(self, bstack11ll11l1111_opy_, bstack11l1ll1l1ll_opy_):
    try:
      headers = {
        bstack11l1111_opy_ (u"ࠧࡏࡦ࠮ࡐࡲࡲࡪ࠳ࡍࡢࡶࡦ࡬ࠧᙣ"): bstack11ll11l1111_opy_
      }
      response = bstack1lllll1111_opy_(bstack11l1111_opy_ (u"࠭ࡇࡆࡖࠪᙤ"), bstack11l1ll1l1ll_opy_, {}, {bstack11l1111_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣᙥ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸࡀࠠࡼࡿࠥᙦ").format(e))
  @measure(event_name=EVENTS.bstack11l1ll1l111_opy_, stage=STAGE.bstack1111llll1_opy_)
  def bstack11l1llll1ll_opy_(self, bstack11l1ll1l1ll_opy_, bstack11ll1111l11_opy_):
    try:
      bstack11l1l1l11l1_opy_ = self.bstack11ll11l11ll_opy_()
      bstack11ll11111ll_opy_ = os.path.join(bstack11l1l1l11l1_opy_, bstack11l1111_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᙧ"))
      bstack11l1l1ll11l_opy_ = os.path.join(bstack11l1l1l11l1_opy_, bstack11ll1111l11_opy_)
      if self.bstack11l1ll1l11l_opy_(bstack11l1l1l11l1_opy_, bstack11l1ll1l1ll_opy_): # if bstack11ll11l11l1_opy_, bstack1ll1l1lll1l_opy_ bstack11l1l11llll_opy_ is bstack11ll11111l1_opy_ to bstack11l1lll111l_opy_ version available (response 304)
        if os.path.exists(bstack11l1l1ll11l_opy_):
          self.logger.info(bstack11l1111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᙨ").format(bstack11l1l1ll11l_opy_))
          return bstack11l1l1ll11l_opy_
        if os.path.exists(bstack11ll11111ll_opy_):
          self.logger.info(bstack11l1111_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᙩ").format(bstack11ll11111ll_opy_))
          return self.bstack11l1ll11l11_opy_(bstack11ll11111ll_opy_, bstack11ll1111l11_opy_)
      self.logger.info(bstack11l1111_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᙪ").format(bstack11l1ll1l1ll_opy_))
      response = bstack1lllll1111_opy_(bstack11l1111_opy_ (u"࠭ࡇࡆࡖࠪᙫ"), bstack11l1ll1l1ll_opy_, {}, {})
      if response.status_code == 200:
        bstack11l1l1l1111_opy_ = response.headers.get(bstack11l1111_opy_ (u"ࠢࡆࡖࡤ࡫ࠧᙬ"), bstack11l1111_opy_ (u"ࠣࠤ᙭"))
        if bstack11l1l1l1111_opy_:
          self.bstack11l1l1l1l11_opy_(bstack11l1l1l11l1_opy_, bstack11l1l1l1111_opy_)
        with open(bstack11ll11111ll_opy_, bstack11l1111_opy_ (u"ࠩࡺࡦࠬ᙮")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1111_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣᙯ").format(bstack11ll11111ll_opy_))
        return self.bstack11l1ll11l11_opy_(bstack11ll11111ll_opy_, bstack11ll1111l11_opy_)
      else:
        raise(bstack11l1111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢᙰ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨᙱ").format(e))
  def bstack11l1llll1l1_opy_(self, bstack11l1ll1l1ll_opy_, bstack11ll1111l11_opy_):
    try:
      retry = 2
      bstack11l1l1ll11l_opy_ = None
      bstack11ll1111ll1_opy_ = False
      while retry > 0:
        bstack11l1l1ll11l_opy_ = self.bstack11l1llll1ll_opy_(bstack11l1ll1l1ll_opy_, bstack11ll1111l11_opy_)
        bstack11ll1111ll1_opy_ = self.bstack11l1lll1l11_opy_(bstack11l1ll1l1ll_opy_, bstack11ll1111l11_opy_, bstack11l1l1ll11l_opy_)
        if bstack11ll1111ll1_opy_:
          break
        retry -= 1
      return bstack11l1l1ll11l_opy_, bstack11ll1111ll1_opy_
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥᙲ").format(e))
    return bstack11l1l1ll11l_opy_, False
  def bstack11l1lll1l11_opy_(self, bstack11l1ll1l1ll_opy_, bstack11ll1111l11_opy_, bstack11l1l1ll11l_opy_, bstack11ll11l1lll_opy_ = 0):
    if bstack11ll11l1lll_opy_ > 1:
      return False
    if bstack11l1l1ll11l_opy_ == None or os.path.exists(bstack11l1l1ll11l_opy_) == False:
      self.logger.warn(bstack11l1111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᙳ"))
      return False
    bstack11ll1111lll_opy_ = bstack11l1111_opy_ (u"ࡳࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࡠ࠳ࡢࡤࠬࠤᙴ")
    command = bstack11l1111_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᙵ").format(bstack11l1l1ll11l_opy_)
    bstack11l1ll1111l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11ll1111lll_opy_, bstack11l1ll1111l_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l1111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤᙶ"))
      return False
  def bstack11l1ll11l11_opy_(self, bstack11ll11111ll_opy_, bstack11ll1111l11_opy_):
    try:
      working_dir = os.path.dirname(bstack11ll11111ll_opy_)
      shutil.unpack_archive(bstack11ll11111ll_opy_, working_dir)
      bstack11l1l1ll11l_opy_ = os.path.join(working_dir, bstack11ll1111l11_opy_)
      os.chmod(bstack11l1l1ll11l_opy_, 0o755)
      return bstack11l1l1ll11l_opy_
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᙷ"))
  def bstack11l1lll11l1_opy_(self):
    try:
      bstack11l1lll1lll_opy_ = self.config.get(bstack11l1111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᙸ"))
      bstack11l1lll11l1_opy_ = bstack11l1lll1lll_opy_ or (bstack11l1lll1lll_opy_ is None and self.bstack1l1ll1ll1_opy_)
      if not bstack11l1lll11l1_opy_ or self.config.get(bstack11l1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᙹ"), None) not in bstack11ll11l1ll1_opy_:
        return False
      self.bstack11ll1111l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᙺ").format(e))
  def bstack11ll111l111_opy_(self):
    try:
      bstack11ll111l111_opy_ = self.percy_capture_mode
      return bstack11ll111l111_opy_
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᙻ").format(e))
  def init(self, bstack1l1ll1ll1_opy_, config, logger):
    self.bstack1l1ll1ll1_opy_ = bstack1l1ll1ll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l1lll11l1_opy_():
      return
    self.bstack11l1lll1l1l_opy_ = config.get(bstack11l1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᙼ"), {})
    self.percy_capture_mode = config.get(bstack11l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ᙽ"))
    try:
      bstack11l1ll1l1ll_opy_, bstack11ll1111l11_opy_ = self.bstack11l1l1llll1_opy_()
      self.bstack11l1l1l1ll1_opy_ = bstack11ll1111l11_opy_
      bstack11l1l1ll11l_opy_, bstack11ll1111ll1_opy_ = self.bstack11l1llll1l1_opy_(bstack11l1ll1l1ll_opy_, bstack11ll1111l11_opy_)
      if bstack11ll1111ll1_opy_:
        self.binary_path = bstack11l1l1ll11l_opy_
        thread = Thread(target=self.bstack11l1l1l111l_opy_)
        thread.start()
      else:
        self.bstack11ll111lll1_opy_ = True
        self.logger.error(bstack11l1111_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣᙾ").format(bstack11l1l1ll11l_opy_))
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᙿ").format(e))
  def bstack11l1lll11ll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1111_opy_ (u"࠭࡬ࡰࡩࠪ "), bstack11l1111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩࠪᚁ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1111_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁࠧᚂ").format(logfile))
      self.bstack11l1l1l11ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᚃ").format(e))
  @measure(event_name=EVENTS.bstack11l1llll111_opy_, stage=STAGE.bstack1111llll1_opy_)
  def bstack11l1l1l111l_opy_(self):
    bstack11ll11l1l11_opy_ = self.bstack11l1l1l1l1l_opy_()
    if bstack11ll11l1l11_opy_ == None:
      self.bstack11ll111lll1_opy_ = True
      self.logger.error(bstack11l1111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨᚄ"))
      return False
    command_args = [bstack11l1111_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧᚅ") if self.bstack1l1ll1ll1_opy_ else bstack11l1111_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩᚆ")]
    bstack11l1l1ll1l1_opy_ = self.bstack11l1l1lllll_opy_()
    if bstack11l1l1ll1l1_opy_ != None:
      command_args.append(bstack11l1111_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧᚇ").format(bstack11l1l1ll1l1_opy_))
    env = os.environ.copy()
    env[bstack11l1111_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧᚈ")] = bstack11ll11l1l11_opy_
    env[bstack11l1111_opy_ (u"ࠣࡖࡋࡣࡇ࡛ࡉࡍࡆࡢ࡙࡚ࡏࡄࠣᚉ")] = os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᚊ"), bstack11l1111_opy_ (u"ࠪࠫᚋ"))
    bstack11ll111ll1l_opy_ = [self.binary_path]
    self.bstack11l1lll11ll_opy_()
    self.bstack11ll11ll111_opy_ = self.bstack11l1ll11lll_opy_(bstack11ll111ll1l_opy_ + command_args, env)
    self.logger.debug(bstack11l1111_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧᚌ"))
    bstack11ll11l1lll_opy_ = 0
    while self.bstack11ll11ll111_opy_.poll() == None:
      bstack11l1ll111l1_opy_ = self.bstack11l1ll11ll1_opy_()
      if bstack11l1ll111l1_opy_:
        self.logger.debug(bstack11l1111_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣᚍ"))
        self.bstack11l1lllllll_opy_ = True
        return True
      bstack11ll11l1lll_opy_ += 1
      self.logger.debug(bstack11l1111_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤᚎ").format(bstack11ll11l1lll_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧᚏ").format(bstack11ll11l1lll_opy_))
    self.bstack11ll111lll1_opy_ = True
    return False
  def bstack11l1ll11ll1_opy_(self, bstack11ll11l1lll_opy_ = 0):
    if bstack11ll11l1lll_opy_ > 10:
      return False
    try:
      bstack11l1ll11l1l_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨᚐ"), bstack11l1111_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪᚑ"))
      bstack11l1l11lll1_opy_ = bstack11l1ll11l1l_opy_ + bstack11l1ll1lll1_opy_
      response = requests.get(bstack11l1l11lll1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࠩᚒ"), {}).get(bstack11l1111_opy_ (u"ࠫ࡮ࡪࠧᚓ"), None)
      return True
    except:
      self.logger.debug(bstack11l1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡲࡴࡩࠢࡦ࡬ࡪࡩ࡫ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥᚔ"))
      return False
  def bstack11l1l1l1l1l_opy_(self):
    bstack11l1l1ll1ll_opy_ = bstack11l1111_opy_ (u"࠭ࡡࡱࡲࠪᚕ") if self.bstack1l1ll1ll1_opy_ else bstack11l1111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᚖ")
    bstack11l1ll111ll_opy_ = bstack11l1111_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦᚗ") if self.config.get(bstack11l1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᚘ")) is None else True
    bstack11ll111ll11_opy_ = bstack11l1111_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠨࡳࡩࡷࡩࡹ࠾ࡽࢀࠦᚙ").format(self.config[bstack11l1111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᚚ")], bstack11l1l1ll1ll_opy_, bstack11l1ll111ll_opy_)
    if self.percy_capture_mode:
      bstack11ll111ll11_opy_ += bstack11l1111_opy_ (u"ࠧࠬࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࡁࢀࢃࠢ᚛").format(self.percy_capture_mode)
    uri = bstack11111111_opy_(bstack11ll111ll11_opy_)
    try:
      response = bstack1lllll1111_opy_(bstack11l1111_opy_ (u"࠭ࡇࡆࡖࠪ᚜"), uri, {}, {bstack11l1111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ᚝"): (self.config[bstack11l1111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᚞")], self.config[bstack11l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᚟")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11ll1111l1_opy_ = data.get(bstack11l1111_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᚠ"))
        self.percy_capture_mode = data.get(bstack11l1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦࠩᚡ"))
        os.environ[bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪᚢ")] = str(self.bstack11ll1111l1_opy_)
        os.environ[bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᚣ")] = str(self.percy_capture_mode)
        if bstack11l1ll111ll_opy_ == bstack11l1111_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥᚤ") and str(self.bstack11ll1111l1_opy_).lower() == bstack11l1111_opy_ (u"ࠣࡶࡵࡹࡪࠨᚥ"):
          self.bstack1lllll11ll_opy_ = True
        if bstack11l1111_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣᚦ") in data:
          return data[bstack11l1111_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤᚧ")]
        else:
          raise bstack11l1111_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫᚨ").format(data)
      else:
        raise bstack11l1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧᚩ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢᚪ").format(e))
  def bstack11l1l1lllll_opy_(self):
    bstack11l1ll1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥᚫ"))
    try:
      if bstack11l1111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᚬ") not in self.bstack11l1lll1l1l_opy_:
        self.bstack11l1lll1l1l_opy_[bstack11l1111_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪᚭ")] = 2
      with open(bstack11l1ll1llll_opy_, bstack11l1111_opy_ (u"ࠪࡻࠬᚮ")) as fp:
        json.dump(self.bstack11l1lll1l1l_opy_, fp)
      return bstack11l1ll1llll_opy_
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᚯ").format(e))
  def bstack11l1ll11lll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11l1lllll1l_opy_ == bstack11l1111_opy_ (u"ࠬࡽࡩ࡯ࠩᚰ"):
        bstack11ll11l1l1l_opy_ = [bstack11l1111_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧᚱ"), bstack11l1111_opy_ (u"ࠧ࠰ࡥࠪᚲ")]
        cmd = bstack11ll11l1l1l_opy_ + cmd
      cmd = bstack11l1111_opy_ (u"ࠨࠢࠪᚳ").join(cmd)
      self.logger.debug(bstack11l1111_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨᚴ").format(cmd))
      with open(self.bstack11l1l1l11ll_opy_, bstack11l1111_opy_ (u"ࠥࡥࠧᚵ")) as bstack11l1ll11111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l1ll11111_opy_, text=True, stderr=bstack11l1ll11111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11ll111lll1_opy_ = True
      self.logger.error(bstack11l1111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᚶ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l1lllllll_opy_:
        self.logger.info(bstack11l1111_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨᚷ"))
        cmd = [self.binary_path, bstack11l1111_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤᚸ")]
        self.bstack11l1ll11lll_opy_(cmd)
        self.bstack11l1lllllll_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᚹ").format(cmd, e))
  def bstack1l1ll1111_opy_(self):
    if not self.bstack11ll1111l1_opy_:
      return
    try:
      bstack11ll11l111l_opy_ = 0
      while not self.bstack11l1lllllll_opy_ and bstack11ll11l111l_opy_ < self.bstack11l1ll1ll11_opy_:
        if self.bstack11ll111lll1_opy_:
          self.logger.info(bstack11l1111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨᚺ"))
          return
        time.sleep(1)
        bstack11ll11l111l_opy_ += 1
      os.environ[bstack11l1111_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨᚻ")] = str(self.bstack11l1l1ll111_opy_())
      self.logger.info(bstack11l1111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦᚼ"))
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᚽ").format(e))
  def bstack11l1l1ll111_opy_(self):
    if self.bstack1l1ll1ll1_opy_:
      return
    try:
      bstack11ll111l11l_opy_ = [platform[bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᚾ")].lower() for platform in self.config.get(bstack11l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᚿ"), [])]
      bstack11l1lll1111_opy_ = sys.maxsize
      bstack11l1lllll11_opy_ = bstack11l1111_opy_ (u"ࠧࠨᛀ")
      for browser in bstack11ll111l11l_opy_:
        if browser in self.bstack11l1lll1ll1_opy_:
          bstack11l1ll1ll1l_opy_ = self.bstack11l1lll1ll1_opy_[browser]
        if bstack11l1ll1ll1l_opy_ < bstack11l1lll1111_opy_:
          bstack11l1lll1111_opy_ = bstack11l1ll1ll1l_opy_
          bstack11l1lllll11_opy_ = browser
      return bstack11l1lllll11_opy_
    except Exception as e:
      self.logger.error(bstack11l1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᛁ").format(e))
  @classmethod
  def bstack111ll1l1l_opy_(self):
    return os.getenv(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧᛂ"), bstack11l1111_opy_ (u"ࠪࡊࡦࡲࡳࡦࠩᛃ")).lower()
  @classmethod
  def bstack11ll111ll_opy_(self):
    return os.getenv(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᛄ"), bstack11l1111_opy_ (u"ࠬ࠭ᛅ"))
  @classmethod
  def bstack1lll11l1l11_opy_(cls, value):
    cls.bstack1lllll11ll_opy_ = value
  @classmethod
  def bstack11ll111llll_opy_(cls):
    return cls.bstack1lllll11ll_opy_
  @classmethod
  def bstack1lll11llll1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11ll111l1ll_opy_(cls):
    return cls.percy_build_id