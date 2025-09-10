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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1l11ll1l_opy_, bstack11l1l11lll1_opy_, bstack11l1ll1l1l1_opy_
import tempfile
import json
bstack111l1l1llll_opy_ = os.getenv(bstack1ll11ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡌࡥࡆࡊࡎࡈࠦᶧ"), None) or os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬ࠨᶨ"))
bstack111l11lll1l_opy_ = os.path.join(bstack1ll11ll_opy_ (u"ࠧࡲ࡯ࡨࠤᶩ"), bstack1ll11ll_opy_ (u"࠭ࡳࡥ࡭࠰ࡧࡱ࡯࠭ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠪᶪ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll11ll_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᶫ"),
      datefmt=bstack1ll11ll_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᶬ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1l1ll1l_opy_():
  bstack111l1l11l1l_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡆࡈࡆ࡚ࡍࠢᶭ"), bstack1ll11ll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤᶮ"))
  return logging.DEBUG if bstack111l1l11l1l_opy_.lower() == bstack1ll11ll_opy_ (u"ࠦࡹࡸࡵࡦࠤᶯ") else logging.INFO
def bstack1l1l1ll11l1_opy_():
  global bstack111l1l1llll_opy_
  if os.path.exists(bstack111l1l1llll_opy_):
    os.remove(bstack111l1l1llll_opy_)
  if os.path.exists(bstack111l11lll1l_opy_):
    os.remove(bstack111l11lll1l_opy_)
def bstack1lll1l111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111l1l111ll_opy_ = log_level
  if bstack1ll11ll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᶰ") in config and config[bstack1ll11ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᶱ")] in bstack11l1l11lll1_opy_:
    bstack111l1l111ll_opy_ = bstack11l1l11lll1_opy_[config[bstack1ll11ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᶲ")]]
  if config.get(bstack1ll11ll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᶳ"), False):
    logging.getLogger().setLevel(bstack111l1l111ll_opy_)
    return bstack111l1l111ll_opy_
  global bstack111l1l1llll_opy_
  bstack1lll1l111_opy_()
  bstack111l1l111l1_opy_ = logging.Formatter(
    fmt=bstack1ll11ll_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬᶴ"),
    datefmt=bstack1ll11ll_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨᶵ"),
  )
  bstack111l11ll11l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l1l1llll_opy_)
  file_handler.setFormatter(bstack111l1l111l1_opy_)
  bstack111l11ll11l_opy_.setFormatter(bstack111l1l111l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l11ll11l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll11ll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ᶶ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l11ll11l_opy_.setLevel(bstack111l1l111ll_opy_)
  logging.getLogger().addHandler(bstack111l11ll11l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l1l111ll_opy_
def bstack111l1l1l111_opy_(config):
  try:
    bstack111l1l1ll1l_opy_ = set(bstack11l1ll1l1l1_opy_)
    bstack111l1l1111l_opy_ = bstack1ll11ll_opy_ (u"ࠬ࠭ᶷ")
    with open(bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᶸ")) as bstack111l11lllll_opy_:
      bstack111l11lll11_opy_ = bstack111l11lllll_opy_.read()
      bstack111l1l1111l_opy_ = re.sub(bstack1ll11ll_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨᶹ"), bstack1ll11ll_opy_ (u"ࠨࠩᶺ"), bstack111l11lll11_opy_, flags=re.M)
      bstack111l1l1111l_opy_ = re.sub(
        bstack1ll11ll_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬᶻ") + bstack1ll11ll_opy_ (u"ࠪࢀࠬᶼ").join(bstack111l1l1ll1l_opy_) + bstack1ll11ll_opy_ (u"ࠫ࠮࠴ࠪࠥࠩᶽ"),
        bstack1ll11ll_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᶾ"),
        bstack111l1l1111l_opy_, flags=re.M | re.I
      )
    def bstack111l1l11l11_opy_(dic):
      bstack111l1ll1111_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l1l1ll1l_opy_:
          bstack111l1ll1111_opy_[key] = bstack1ll11ll_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᶿ")
        else:
          if isinstance(value, dict):
            bstack111l1ll1111_opy_[key] = bstack111l1l11l11_opy_(value)
          else:
            bstack111l1ll1111_opy_[key] = value
      return bstack111l1ll1111_opy_
    bstack111l1ll1111_opy_ = bstack111l1l11l11_opy_(config)
    return {
      bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ᷀"): bstack111l1l1111l_opy_,
      bstack1ll11ll_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ᷁"): json.dumps(bstack111l1ll1111_opy_)
    }
  except Exception as e:
    return {}
def bstack111l1l1lll1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1ll11ll_opy_ (u"ࠩ࡯ࡳ࡬᷂࠭"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111l1l1l1l1_opy_ = os.path.join(log_dir, bstack1ll11ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶࠫ᷃"))
  if not os.path.exists(bstack111l1l1l1l1_opy_):
    bstack111l1l1ll11_opy_ = {
      bstack1ll11ll_opy_ (u"ࠦ࡮ࡴࡩࡱࡣࡷ࡬ࠧ᷄"): str(inipath),
      bstack1ll11ll_opy_ (u"ࠧࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠢ᷅"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1ll11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬ᷆")), bstack1ll11ll_opy_ (u"ࠧࡸࠩ᷇")) as bstack111l1l11ll1_opy_:
      bstack111l1l11ll1_opy_.write(json.dumps(bstack111l1l1ll11_opy_))
def bstack111l11llll1_opy_():
  try:
    bstack111l1l1l1l1_opy_ = os.path.join(os.getcwd(), bstack1ll11ll_opy_ (u"ࠨ࡮ࡲ࡫ࠬ᷈"), bstack1ll11ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ᷉"))
    if os.path.exists(bstack111l1l1l1l1_opy_):
      with open(bstack111l1l1l1l1_opy_, bstack1ll11ll_opy_ (u"ࠪࡶ᷊ࠬ")) as bstack111l1l11ll1_opy_:
        bstack111l1l11lll_opy_ = json.load(bstack111l1l11ll1_opy_)
      return bstack111l1l11lll_opy_.get(bstack1ll11ll_opy_ (u"ࠫ࡮ࡴࡩࡱࡣࡷ࡬ࠬ᷋"), bstack1ll11ll_opy_ (u"ࠬ࠭᷌")), bstack111l1l11lll_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡲࡰࡱࡷࡴࡦࡺࡨࠨ᷍"), bstack1ll11ll_opy_ (u"ࠧࠨ᷎"))
  except:
    pass
  return None, None
def bstack111l1l11111_opy_():
  try:
    bstack111l1l1l1l1_opy_ = os.path.join(os.getcwd(), bstack1ll11ll_opy_ (u"ࠨ࡮ࡲ࡫᷏ࠬ"), bstack1ll11ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ᷐"))
    if os.path.exists(bstack111l1l1l1l1_opy_):
      os.remove(bstack111l1l1l1l1_opy_)
  except:
    pass
def bstack11lllll11l_opy_(config):
  try:
    from bstack_utils.helper import bstack1l111111l1_opy_, bstack1111lllll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111l1l1llll_opy_
    if config.get(bstack1ll11ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ᷑"), False):
      return
    uuid = os.getenv(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᷒")) if os.getenv(bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᷓ")) else bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣᷔ"))
    if not uuid or uuid == bstack1ll11ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᷕ"):
      return
    bstack111l1l1l1ll_opy_ = [bstack1ll11ll_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫᷖ"), bstack1ll11ll_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪᷗ"), bstack1ll11ll_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫᷘ"), bstack111l1l1llll_opy_, bstack111l11lll1l_opy_]
    bstack111l11ll1l1_opy_, root_path = bstack111l11llll1_opy_()
    if bstack111l11ll1l1_opy_ != None:
      bstack111l1l1l1ll_opy_.append(bstack111l11ll1l1_opy_)
    if root_path != None:
      bstack111l1l1l1ll_opy_.append(os.path.join(root_path, bstack1ll11ll_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩᷙ")))
    bstack1lll1l111_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡲ࡯ࡨࡵ࠰ࠫᷚ") + uuid + bstack1ll11ll_opy_ (u"࠭࠮ࡵࡣࡵ࠲࡬ࢀࠧᷛ"))
    with tarfile.open(output_file, bstack1ll11ll_opy_ (u"ࠢࡸ࠼ࡪࡾࠧᷜ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l1l1l1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l1l1l111_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l1l1l11l_opy_ = data.encode()
        tarinfo.size = len(bstack111l1l1l11l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l1l1l11l_opy_))
    bstack11llll11l_opy_ = MultipartEncoder(
      fields= {
        bstack1ll11ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᷝ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll11ll_opy_ (u"ࠩࡵࡦࠬᷞ")), bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰࡫ࡿ࡯ࡰࠨᷟ")),
        bstack1ll11ll_opy_ (u"ࠫࡨࡲࡩࡦࡰࡷࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᷠ"): uuid
      }
    )
    bstack111l11ll1ll_opy_ = bstack1111lllll_opy_(cli.config, [bstack1ll11ll_opy_ (u"ࠧࡧࡰࡪࡵࠥᷡ"), bstack1ll11ll_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨᷢ"), bstack1ll11ll_opy_ (u"ࠢࡶࡲ࡯ࡳࡦࡪࠢᷣ")], bstack11l1l11ll1l_opy_)
    response = requests.post(
      bstack1ll11ll_opy_ (u"ࠣࡽࢀ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤᷤ").format(bstack111l11ll1ll_opy_),
      data=bstack11llll11l_opy_,
      headers={bstack1ll11ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᷥ"): bstack11llll11l_opy_.content_type},
      auth=(config[bstack1ll11ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᷦ")], config[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᷧ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll11ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶ࡬ࡰࡣࡧࠤࡱࡵࡧࡴ࠼ࠣࠫᷨ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll11ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠬᷩ") + str(e))
  finally:
    try:
      bstack1l1l1ll11l1_opy_()
      bstack111l1l11111_opy_()
    except:
      pass