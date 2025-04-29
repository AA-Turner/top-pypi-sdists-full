# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1l1ll11_opy_, bstack11ll1lllll1_opy_
import tempfile
import json
bstack11l111ll111_opy_ = os.getenv(bstack1llllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇࠥ᯴"), None) or os.path.join(tempfile.gettempdir(), bstack1llllll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠧ᯵"))
bstack11l111lllll_opy_ = os.path.join(bstack1llllll_opy_ (u"ࠦࡱࡵࡧࠣ᯶"), bstack1llllll_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩ᯷"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1llllll_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ᯸"),
      datefmt=bstack1llllll_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬ᯹"),
      stream=sys.stdout
    )
  return logger
def bstack1llll11llll_opy_():
  bstack11l111l11ll_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡅࡇࡅ࡙ࡌࠨ᯺"), bstack1llllll_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣ᯻"))
  return logging.DEBUG if bstack11l111l11ll_opy_.lower() == bstack1llllll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᯼") else logging.INFO
def bstack1l1llll1ll1_opy_():
  global bstack11l111ll111_opy_
  if os.path.exists(bstack11l111ll111_opy_):
    os.remove(bstack11l111ll111_opy_)
  if os.path.exists(bstack11l111lllll_opy_):
    os.remove(bstack11l111lllll_opy_)
def bstack11llll1ll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11ll11ll_opy_(config, log_level):
  bstack11l111l1l11_opy_ = log_level
  if bstack1llllll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭᯽") in config and config[bstack1llllll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ᯾")] in bstack11ll1l1ll11_opy_:
    bstack11l111l1l11_opy_ = bstack11ll1l1ll11_opy_[config[bstack1llllll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ᯿")]]
  if config.get(bstack1llllll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᰀ"), False):
    logging.getLogger().setLevel(bstack11l111l1l11_opy_)
    return bstack11l111l1l11_opy_
  global bstack11l111ll111_opy_
  bstack11llll1ll1_opy_()
  bstack11l111lll1l_opy_ = logging.Formatter(
    fmt=bstack1llllll_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᰁ"),
    datefmt=bstack1llllll_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧᰂ"),
  )
  bstack11l11l11lll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111ll111_opy_)
  file_handler.setFormatter(bstack11l111lll1l_opy_)
  bstack11l11l11lll_opy_.setFormatter(bstack11l111lll1l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l11l11lll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1llllll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬᰃ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l11l11lll_opy_.setLevel(bstack11l111l1l11_opy_)
  logging.getLogger().addHandler(bstack11l11l11lll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l111l1l11_opy_
def bstack11l11l11l1l_opy_(config):
  try:
    bstack11l111l111l_opy_ = set(bstack11ll1lllll1_opy_)
    bstack11l11l111ll_opy_ = bstack1llllll_opy_ (u"ࠫࠬᰄ")
    with open(bstack1llllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᰅ")) as bstack11l111l11l1_opy_:
      bstack11l11l11111_opy_ = bstack11l111l11l1_opy_.read()
      bstack11l11l111ll_opy_ = re.sub(bstack1llllll_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧᰆ"), bstack1llllll_opy_ (u"ࠧࠨᰇ"), bstack11l11l11111_opy_, flags=re.M)
      bstack11l11l111ll_opy_ = re.sub(
        bstack1llllll_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫᰈ") + bstack1llllll_opy_ (u"ࠩࡿࠫᰉ").join(bstack11l111l111l_opy_) + bstack1llllll_opy_ (u"ࠪ࠭࠳࠰ࠤࠨᰊ"),
        bstack1llllll_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ᰋ"),
        bstack11l11l111ll_opy_, flags=re.M | re.I
      )
    def bstack11l11l11ll1_opy_(dic):
      bstack11l111ll11l_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l111l111l_opy_:
          bstack11l111ll11l_opy_[key] = bstack1llllll_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᰌ")
        else:
          if isinstance(value, dict):
            bstack11l111ll11l_opy_[key] = bstack11l11l11ll1_opy_(value)
          else:
            bstack11l111ll11l_opy_[key] = value
      return bstack11l111ll11l_opy_
    bstack11l111ll11l_opy_ = bstack11l11l11ll1_opy_(config)
    return {
      bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᰍ"): bstack11l11l111ll_opy_,
      bstack1llllll_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᰎ"): json.dumps(bstack11l111ll11l_opy_)
    }
  except Exception as e:
    return {}
def bstack11l11l1111l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1llllll_opy_ (u"ࠨ࡮ࡲ࡫ࠬᰏ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l111l1ll1_opy_ = os.path.join(log_dir, bstack1llllll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵࠪᰐ"))
  if not os.path.exists(bstack11l111l1ll1_opy_):
    bstack11l111ll1l1_opy_ = {
      bstack1llllll_opy_ (u"ࠥ࡭ࡳ࡯ࡰࡢࡶ࡫ࠦᰑ"): str(inipath),
      bstack1llllll_opy_ (u"ࠦࡷࡵ࡯ࡵࡲࡤࡸ࡭ࠨᰒ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1llllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫᰓ")), bstack1llllll_opy_ (u"࠭ࡷࠨᰔ")) as bstack11l111l1l1l_opy_:
      bstack11l111l1l1l_opy_.write(json.dumps(bstack11l111ll1l1_opy_))
def bstack11l111llll1_opy_():
  try:
    bstack11l111l1ll1_opy_ = os.path.join(os.getcwd(), bstack1llllll_opy_ (u"ࠧ࡭ࡱࡪࠫᰕ"), bstack1llllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᰖ"))
    if os.path.exists(bstack11l111l1ll1_opy_):
      with open(bstack11l111l1ll1_opy_, bstack1llllll_opy_ (u"ࠩࡵࠫᰗ")) as bstack11l111l1l1l_opy_:
        bstack11l111ll1ll_opy_ = json.load(bstack11l111l1l1l_opy_)
      return bstack11l111ll1ll_opy_.get(bstack1llllll_opy_ (u"ࠪ࡭ࡳ࡯ࡰࡢࡶ࡫ࠫᰘ"), bstack1llllll_opy_ (u"ࠫࠬᰙ")), bstack11l111ll1ll_opy_.get(bstack1llllll_opy_ (u"ࠬࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠧᰚ"), bstack1llllll_opy_ (u"࠭ࠧᰛ"))
  except:
    pass
  return None, None
def bstack11l111l1lll_opy_():
  try:
    bstack11l111l1ll1_opy_ = os.path.join(os.getcwd(), bstack1llllll_opy_ (u"ࠧ࡭ࡱࡪࠫᰜ"), bstack1llllll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᰝ"))
    if os.path.exists(bstack11l111l1ll1_opy_):
      os.remove(bstack11l111l1ll1_opy_)
  except:
    pass
def bstack11lll11l1l_opy_(config):
  from bstack_utils.helper import bstack1l1ll1l1l1_opy_
  global bstack11l111ll111_opy_
  try:
    if config.get(bstack1llllll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᰞ"), False):
      return
    uuid = os.getenv(bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᰟ")) if os.getenv(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᰠ")) else bstack1l1ll1l1l1_opy_.get_property(bstack1llllll_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢᰡ"))
    if not uuid or uuid == bstack1llllll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᰢ"):
      return
    bstack11l11l111l1_opy_ = [bstack1llllll_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪᰣ"), bstack1llllll_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩᰤ"), bstack1llllll_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪᰥ"), bstack11l111ll111_opy_, bstack11l111lllll_opy_]
    bstack11l11l11l11_opy_, root_path = bstack11l111llll1_opy_()
    if bstack11l11l11l11_opy_ != None:
      bstack11l11l111l1_opy_.append(bstack11l11l11l11_opy_)
    if root_path != None:
      bstack11l11l111l1_opy_.append(os.path.join(root_path, bstack1llllll_opy_ (u"ࠪࡧࡴࡴࡦࡵࡧࡶࡸ࠳ࡶࡹࠨᰦ")))
    bstack11llll1ll1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1llllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪᰧ") + uuid + bstack1llllll_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭ᰨ"))
    with tarfile.open(output_file, bstack1llllll_opy_ (u"ࠨࡷ࠻ࡩࡽࠦᰩ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l11l111l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l11l11l1l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l111lll11_opy_ = data.encode()
        tarinfo.size = len(bstack11l111lll11_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l111lll11_opy_))
    bstack11l11ll1_opy_ = MultipartEncoder(
      fields= {
        bstack1llllll_opy_ (u"ࠧࡥࡣࡷࡥࠬᰪ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1llllll_opy_ (u"ࠨࡴࡥࠫᰫ")), bstack1llllll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧᰬ")),
        bstack1llllll_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᰭ"): uuid
      }
    )
    response = requests.post(
      bstack1llllll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨᰮ"),
      data=bstack11l11ll1_opy_,
      headers={bstack1llllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᰯ"): bstack11l11ll1_opy_.content_type},
      auth=(config[bstack1llllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᰰ")], config[bstack1llllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᰱ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1llllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧᰲ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1llllll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨᰳ") + str(e))
  finally:
    try:
      bstack1l1llll1ll1_opy_()
      bstack11l111l1lll_opy_()
    except:
      pass