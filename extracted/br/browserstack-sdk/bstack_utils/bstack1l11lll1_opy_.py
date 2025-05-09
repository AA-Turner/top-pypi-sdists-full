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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1lllll1_opy_, bstack11ll1l1ll1l_opy_
import tempfile
import json
bstack11l111ll1ll_opy_ = os.getenv(bstack11lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧ᯽"), None) or os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢ᯾"))
bstack11l1111llll_opy_ = os.path.join(bstack11lll_opy_ (u"ࠨ࡬ࡰࡩࠥ᯿"), bstack11lll_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᰀ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11lll_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᰁ"),
      datefmt=bstack11lll_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧᰂ"),
      stream=sys.stdout
    )
  return logger
def bstack1ll1lllllll_opy_():
  bstack11l111l11l1_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣᰃ"), bstack11lll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᰄ"))
  return logging.DEBUG if bstack11l111l11l1_opy_.lower() == bstack11lll_opy_ (u"ࠧࡺࡲࡶࡧࠥᰅ") else logging.INFO
def bstack1ll111ll1l1_opy_():
  global bstack11l111ll1ll_opy_
  if os.path.exists(bstack11l111ll1ll_opy_):
    os.remove(bstack11l111ll1ll_opy_)
  if os.path.exists(bstack11l1111llll_opy_):
    os.remove(bstack11l1111llll_opy_)
def bstack11l11l1ll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1ll1l11111_opy_(config, log_level):
  bstack11l11l11111_opy_ = log_level
  if bstack11lll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᰆ") in config and config[bstack11lll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᰇ")] in bstack11ll1lllll1_opy_:
    bstack11l11l11111_opy_ = bstack11ll1lllll1_opy_[config[bstack11lll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᰈ")]]
  if config.get(bstack11lll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᰉ"), False):
    logging.getLogger().setLevel(bstack11l11l11111_opy_)
    return bstack11l11l11111_opy_
  global bstack11l111ll1ll_opy_
  bstack11l11l1ll_opy_()
  bstack11l111l111l_opy_ = logging.Formatter(
    fmt=bstack11lll_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᰊ"),
    datefmt=bstack11lll_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩᰋ"),
  )
  bstack11l11l11l11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111ll1ll_opy_)
  file_handler.setFormatter(bstack11l111l111l_opy_)
  bstack11l11l11l11_opy_.setFormatter(bstack11l111l111l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l11l11l11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11lll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧᰌ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l11l11l11_opy_.setLevel(bstack11l11l11111_opy_)
  logging.getLogger().addHandler(bstack11l11l11l11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l11l11111_opy_
def bstack11l11l1111l_opy_(config):
  try:
    bstack11l111l1111_opy_ = set(bstack11ll1l1ll1l_opy_)
    bstack11l111l1l1l_opy_ = bstack11lll_opy_ (u"࠭ࠧᰍ")
    with open(bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᰎ")) as bstack11l111ll1l1_opy_:
      bstack11l111l1l11_opy_ = bstack11l111ll1l1_opy_.read()
      bstack11l111l1l1l_opy_ = re.sub(bstack11lll_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩᰏ"), bstack11lll_opy_ (u"ࠩࠪᰐ"), bstack11l111l1l11_opy_, flags=re.M)
      bstack11l111l1l1l_opy_ = re.sub(
        bstack11lll_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭ᰑ") + bstack11lll_opy_ (u"ࠫࢁ࠭ᰒ").join(bstack11l111l1111_opy_) + bstack11lll_opy_ (u"ࠬ࠯࠮ࠫࠦࠪᰓ"),
        bstack11lll_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᰔ"),
        bstack11l111l1l1l_opy_, flags=re.M | re.I
      )
    def bstack11l111ll11l_opy_(dic):
      bstack11l111lll1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l111l1111_opy_:
          bstack11l111lll1l_opy_[key] = bstack11lll_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᰕ")
        else:
          if isinstance(value, dict):
            bstack11l111lll1l_opy_[key] = bstack11l111ll11l_opy_(value)
          else:
            bstack11l111lll1l_opy_[key] = value
      return bstack11l111lll1l_opy_
    bstack11l111lll1l_opy_ = bstack11l111ll11l_opy_(config)
    return {
      bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᰖ"): bstack11l111l1l1l_opy_,
      bstack11lll_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᰗ"): json.dumps(bstack11l111lll1l_opy_)
    }
  except Exception as e:
    return {}
def bstack11l111llll1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11lll_opy_ (u"ࠪࡰࡴ࡭ࠧᰘ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l11l11l1l_opy_ = os.path.join(log_dir, bstack11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬᰙ"))
  if not os.path.exists(bstack11l11l11l1l_opy_):
    bstack11l111l11ll_opy_ = {
      bstack11lll_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨᰚ"): str(inipath),
      bstack11lll_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣᰛ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᰜ")), bstack11lll_opy_ (u"ࠨࡹࠪᰝ")) as bstack11l111lll11_opy_:
      bstack11l111lll11_opy_.write(json.dumps(bstack11l111l11ll_opy_))
def bstack11l11l111ll_opy_():
  try:
    bstack11l11l11l1l_opy_ = os.path.join(os.getcwd(), bstack11lll_opy_ (u"ࠩ࡯ࡳ࡬࠭ᰞ"), bstack11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᰟ"))
    if os.path.exists(bstack11l11l11l1l_opy_):
      with open(bstack11l11l11l1l_opy_, bstack11lll_opy_ (u"ࠫࡷ࠭ᰠ")) as bstack11l111lll11_opy_:
        bstack11l11l111l1_opy_ = json.load(bstack11l111lll11_opy_)
      return bstack11l11l111l1_opy_.get(bstack11lll_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭ᰡ"), bstack11lll_opy_ (u"࠭ࠧᰢ")), bstack11l11l111l1_opy_.get(bstack11lll_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩᰣ"), bstack11lll_opy_ (u"ࠨࠩᰤ"))
  except:
    pass
  return None, None
def bstack11l111lllll_opy_():
  try:
    bstack11l11l11l1l_opy_ = os.path.join(os.getcwd(), bstack11lll_opy_ (u"ࠩ࡯ࡳ࡬࠭ᰥ"), bstack11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᰦ"))
    if os.path.exists(bstack11l11l11l1l_opy_):
      os.remove(bstack11l11l11l1l_opy_)
  except:
    pass
def bstack11l1l1ll11_opy_(config):
  from bstack_utils.helper import bstack1llllll11_opy_
  global bstack11l111ll1ll_opy_
  try:
    if config.get(bstack11lll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᰧ"), False):
      return
    uuid = os.getenv(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᰨ")) if os.getenv(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᰩ")) else bstack1llllll11_opy_.get_property(bstack11lll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤᰪ"))
    if not uuid or uuid == bstack11lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᰫ"):
      return
    bstack11l111l1lll_opy_ = [bstack11lll_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬᰬ"), bstack11lll_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫᰭ"), bstack11lll_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬᰮ"), bstack11l111ll1ll_opy_, bstack11l1111llll_opy_]
    bstack11l111ll111_opy_, root_path = bstack11l11l111ll_opy_()
    if bstack11l111ll111_opy_ != None:
      bstack11l111l1lll_opy_.append(bstack11l111ll111_opy_)
    if root_path != None:
      bstack11l111l1lll_opy_.append(os.path.join(root_path, bstack11lll_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪᰯ")))
    bstack11l11l1ll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬᰰ") + uuid + bstack11lll_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᰱ"))
    with tarfile.open(output_file, bstack11lll_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᰲ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l111l1lll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l11l1111l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l111l1ll1_opy_ = data.encode()
        tarinfo.size = len(bstack11l111l1ll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l111l1ll1_opy_))
    bstack11l1l1l11l_opy_ = MultipartEncoder(
      fields= {
        bstack11lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᰳ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11lll_opy_ (u"ࠪࡶࡧ࠭ᰴ")), bstack11lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩᰵ")),
        bstack11lll_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᰶ"): uuid
      }
    )
    response = requests.post(
      bstack11lll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡶࡲ࡯ࡳࡦࡪ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤ᰷ࠣ"),
      data=bstack11l1l1l11l_opy_,
      headers={bstack11lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭᰸"): bstack11l1l1l11l_opy_.content_type},
      auth=(config[bstack11lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᰹")], config[bstack11lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᰺")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩ᰻") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪ᰼") + str(e))
  finally:
    try:
      bstack1ll111ll1l1_opy_()
      bstack11l111lllll_opy_()
    except:
      pass