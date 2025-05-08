# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll1l1ll1l_opy_, bstack11ll1l11l1_opy_, bstack11l1lll11_opy_, bstack1l1llll1l_opy_,
                                    bstack11ll1l11l11_opy_, bstack11ll1l1lll1_opy_, bstack11ll1l1l1ll_opy_, bstack11ll11lll1l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1l1ll1ll_opy_, bstack11111l1l1_opy_
from bstack_utils.proxy import bstack11ll1l11l_opy_, bstack1ll11lll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1ll1l111l1_opy_
from browserstack_sdk._version import __version__
bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
logger = bstack1ll1l111l1_opy_.get_logger(__name__, bstack1ll1l111l1_opy_.bstack1lllll11lll_opy_())
def bstack11lllll1lll_opy_(config):
    return config[bstack1l1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᦮")]
def bstack11llll1l1ll_opy_(config):
    return config[bstack1l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᦯")]
def bstack11ll11l1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l1llll1_opy_(obj):
    values = []
    bstack11ll1111l1l_opy_ = re.compile(bstack1l1lll_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᦰ"), re.I)
    for key in obj.keys():
        if bstack11ll1111l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1l11111l_opy_(config):
    tags = []
    tags.extend(bstack11l1l1llll1_opy_(os.environ))
    tags.extend(bstack11l1l1llll1_opy_(config))
    return tags
def bstack11l1lll11ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11lll1ll_opy_(bstack11l1ll11111_opy_):
    if not bstack11l1ll11111_opy_:
        return bstack1l1lll_opy_ (u"ࠫࠬᦱ")
    return bstack1l1lll_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᦲ").format(bstack11l1ll11111_opy_.name, bstack11l1ll11111_opy_.email)
def bstack11lll1lllll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lllllll_opy_ = repo.common_dir
        info = {
            bstack1l1lll_opy_ (u"ࠨࡳࡩࡣࠥᦳ"): repo.head.commit.hexsha,
            bstack1l1lll_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᦴ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1lll_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᦵ"): repo.active_branch.name,
            bstack1l1lll_opy_ (u"ࠤࡷࡥ࡬ࠨᦶ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᦷ"): bstack11l11lll1ll_opy_(repo.head.commit.committer),
            bstack1l1lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᦸ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1lll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᦹ"): bstack11l11lll1ll_opy_(repo.head.commit.author),
            bstack1l1lll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᦺ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1lll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᦻ"): repo.head.commit.message,
            bstack1l1lll_opy_ (u"ࠣࡴࡲࡳࡹࠨᦼ"): repo.git.rev_parse(bstack1l1lll_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᦽ")),
            bstack1l1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᦾ"): bstack11l1lllllll_opy_,
            bstack1l1lll_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᦿ"): subprocess.check_output([bstack1l1lll_opy_ (u"ࠧ࡭ࡩࡵࠤᧀ"), bstack1l1lll_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᧁ"), bstack1l1lll_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᧂ")]).strip().decode(
                bstack1l1lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᧃ")),
            bstack1l1lll_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᧄ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᧅ"): repo.git.rev_list(
                bstack1l1lll_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᧆ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11ll1111111_opy_ = []
        for remote in remotes:
            bstack11l1l1l11ll_opy_ = {
                bstack1l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᧇ"): remote.name,
                bstack1l1lll_opy_ (u"ࠨࡵࡳ࡮ࠥᧈ"): remote.url,
            }
            bstack11ll1111111_opy_.append(bstack11l1l1l11ll_opy_)
        bstack11l11lllll1_opy_ = {
            bstack1l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᧉ"): bstack1l1lll_opy_ (u"ࠣࡩ࡬ࡸࠧ᧊"),
            **info,
            bstack1l1lll_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥ᧋"): bstack11ll1111111_opy_
        }
        bstack11l11lllll1_opy_ = bstack11l1l11ll11_opy_(bstack11l11lllll1_opy_)
        return bstack11l11lllll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ᧌").format(err))
        return {}
def bstack11l1l11ll11_opy_(bstack11l11lllll1_opy_):
    bstack11l11lll111_opy_ = bstack11l1lll111l_opy_(bstack11l11lllll1_opy_)
    if bstack11l11lll111_opy_ and bstack11l11lll111_opy_ > bstack11ll1l11l11_opy_:
        bstack11ll1111lll_opy_ = bstack11l11lll111_opy_ - bstack11ll1l11l11_opy_
        bstack11l1l11lll1_opy_ = bstack11l1lll1111_opy_(bstack11l11lllll1_opy_[bstack1l1lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ᧍")], bstack11ll1111lll_opy_)
        bstack11l11lllll1_opy_[bstack1l1lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᧎")] = bstack11l1l11lll1_opy_
        logger.info(bstack1l1lll_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣ᧏")
                    .format(bstack11l1lll111l_opy_(bstack11l11lllll1_opy_) / 1024))
    return bstack11l11lllll1_opy_
def bstack11l1lll111l_opy_(bstack1l1111ll1l_opy_):
    try:
        if bstack1l1111ll1l_opy_:
            bstack11ll11l1ll1_opy_ = json.dumps(bstack1l1111ll1l_opy_)
            bstack11ll111l111_opy_ = sys.getsizeof(bstack11ll11l1ll1_opy_)
            return bstack11ll111l111_opy_
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢ᧐").format(e))
    return -1
def bstack11l1lll1111_opy_(field, bstack11ll111l1ll_opy_):
    try:
        bstack11ll1111ll1_opy_ = len(bytes(bstack11ll1l1lll1_opy_, bstack1l1lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᧑")))
        bstack11l1ll1ll11_opy_ = bytes(field, bstack1l1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᧒"))
        bstack11ll111111l_opy_ = len(bstack11l1ll1ll11_opy_)
        bstack11ll111l11l_opy_ = ceil(bstack11ll111111l_opy_ - bstack11ll111l1ll_opy_ - bstack11ll1111ll1_opy_)
        if bstack11ll111l11l_opy_ > 0:
            bstack11ll11ll111_opy_ = bstack11l1ll1ll11_opy_[:bstack11ll111l11l_opy_].decode(bstack1l1lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᧓"), errors=bstack1l1lll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫ᧔")) + bstack11ll1l1lll1_opy_
            return bstack11ll11ll111_opy_
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥ᧕").format(e))
    return field
def bstack1l1l1ll1l_opy_():
    env = os.environ
    if (bstack1l1lll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ᧖") in env and len(env[bstack1l1lll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᧗")]) > 0) or (
            bstack1l1lll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ᧘") in env and len(env[bstack1l1lll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᧙")]) > 0):
        return {
            bstack1l1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᧚"): bstack1l1lll_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧ᧛"),
            bstack1l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᧜"): env.get(bstack1l1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᧝")),
            bstack1l1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᧞"): env.get(bstack1l1lll_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥ᧟")),
            bstack1l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᧠"): env.get(bstack1l1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᧡"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠦࡈࡏࠢ᧢")) == bstack1l1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᧣") and bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣ᧤"))):
        return {
            bstack1l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧥"): bstack1l1lll_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥ᧦"),
            bstack1l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧧"): env.get(bstack1l1lll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᧨")),
            bstack1l1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᧩"): env.get(bstack1l1lll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤ᧪")),
            bstack1l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᧫"): env.get(bstack1l1lll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥ᧬"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠣࡅࡌࠦ᧭")) == bstack1l1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᧮") and bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥ᧯"))):
        return {
            bstack1l1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧰"): bstack1l1lll_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣ᧱"),
            bstack1l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᧲"): env.get(bstack1l1lll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢ᧳")),
            bstack1l1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᧴"): env.get(bstack1l1lll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᧵")),
            bstack1l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᧶"): env.get(bstack1l1lll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᧷"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠧࡉࡉࠣ᧸")) == bstack1l1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦ᧹") and env.get(bstack1l1lll_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣ᧺")) == bstack1l1lll_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ᧻"):
        return {
            bstack1l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧼"): bstack1l1lll_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧ᧽"),
            bstack1l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧾"): None,
            bstack1l1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧿"): None,
            bstack1l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨀ"): None
        }
    if env.get(bstack1l1lll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥᨁ")) and env.get(bstack1l1lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦᨂ")):
        return {
            bstack1l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨃ"): bstack1l1lll_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨᨄ"),
            bstack1l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨅ"): env.get(bstack1l1lll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥᨆ")),
            bstack1l1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨇ"): None,
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨈ"): env.get(bstack1l1lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᨉ"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠤࡆࡍࠧᨊ")) == bstack1l1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᨋ") and bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᨌ"))):
        return {
            bstack1l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨍ"): bstack1l1lll_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧᨎ"),
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨏ"): env.get(bstack1l1lll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦᨐ")),
            bstack1l1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᨑ"): None,
            bstack1l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᨒ"): env.get(bstack1l1lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᨓ"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠧࡉࡉࠣᨔ")) == bstack1l1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦᨕ") and bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥᨖ"))):
        return {
            bstack1l1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᨗ"): bstack1l1lll_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩᨘࠧ"),
            bstack1l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᨙ"): env.get(bstack1l1lll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᨚ")),
            bstack1l1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᨛ"): env.get(bstack1l1lll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᨜")),
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᨝"): env.get(bstack1l1lll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦ᨞"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠤࡆࡍࠧ᨟")) == bstack1l1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᨠ") and bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᨡ"))):
        return {
            bstack1l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨢ"): bstack1l1lll_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨᨣ"),
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨤ"): env.get(bstack1l1lll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧᨥ")),
            bstack1l1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᨦ"): env.get(bstack1l1lll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᨧ")),
            bstack1l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨨ"): env.get(bstack1l1lll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᨩ"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠨࡃࡊࠤᨪ")) == bstack1l1lll_opy_ (u"ࠢࡵࡴࡸࡩࠧᨫ") and bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᨬ"))):
        return {
            bstack1l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨭ"): bstack1l1lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᨮ"),
            bstack1l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨯ"): env.get(bstack1l1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᨰ")),
            bstack1l1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨱ"): env.get(bstack1l1lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᨲ")) or env.get(bstack1l1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᨳ")),
            bstack1l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨴ"): env.get(bstack1l1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᨵ"))
        }
    if bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᨶ"))):
        return {
            bstack1l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨷ"): bstack1l1lll_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᨸ"),
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨹ"): bstack1l1lll_opy_ (u"ࠣࡽࢀࡿࢂࠨᨺ").format(env.get(bstack1l1lll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᨻ")), env.get(bstack1l1lll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᨼ"))),
            bstack1l1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨽ"): env.get(bstack1l1lll_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᨾ")),
            bstack1l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨿ"): env.get(bstack1l1lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᩀ"))
        }
    if bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᩁ"))):
        return {
            bstack1l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩂ"): bstack1l1lll_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᩃ"),
            bstack1l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩄ"): bstack1l1lll_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᩅ").format(env.get(bstack1l1lll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᩆ")), env.get(bstack1l1lll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᩇ")), env.get(bstack1l1lll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᩈ")), env.get(bstack1l1lll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᩉ"))),
            bstack1l1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩊ"): env.get(bstack1l1lll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᩋ")),
            bstack1l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩌ"): env.get(bstack1l1lll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᩍ"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᩎ")) and env.get(bstack1l1lll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᩏ")):
        return {
            bstack1l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩐ"): bstack1l1lll_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧᩑ"),
            bstack1l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩒ"): bstack1l1lll_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣᩓ").format(env.get(bstack1l1lll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᩔ")), env.get(bstack1l1lll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬᩕ")), env.get(bstack1l1lll_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨᩖ"))),
            bstack1l1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᩗ"): env.get(bstack1l1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᩘ")),
            bstack1l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᩙ"): env.get(bstack1l1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᩚ"))
        }
    if any([env.get(bstack1l1lll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᩛ")), env.get(bstack1l1lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᩜ")), env.get(bstack1l1lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᩝ"))]):
        return {
            bstack1l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩞ"): bstack1l1lll_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥ᩟"),
            bstack1l1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲ᩠ࠢ"): env.get(bstack1l1lll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᩡ")),
            bstack1l1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩢ"): env.get(bstack1l1lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᩣ")),
            bstack1l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᩤ"): env.get(bstack1l1lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᩥ"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᩦ")):
        return {
            bstack1l1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩧ"): bstack1l1lll_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧᩨ"),
            bstack1l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩩ"): env.get(bstack1l1lll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤᩪ")),
            bstack1l1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩫ"): env.get(bstack1l1lll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣᩬ")),
            bstack1l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᩭ"): env.get(bstack1l1lll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᩮ"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨᩯ")) or env.get(bstack1l1lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᩰ")):
        return {
            bstack1l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩱ"): bstack1l1lll_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᩲ"),
            bstack1l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩳ"): env.get(bstack1l1lll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᩴ")),
            bstack1l1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᩵"): bstack1l1lll_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧ᩶") if env.get(bstack1l1lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ᩷")) else None,
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᩸"): env.get(bstack1l1lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ᩹"))
        }
    if any([env.get(bstack1l1lll_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ᩺")), env.get(bstack1l1lll_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ᩻")), env.get(bstack1l1lll_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ᩼"))]):
        return {
            bstack1l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᩽"): bstack1l1lll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧ᩾"),
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᩿ࠥ"): None,
            bstack1l1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪀"): env.get(bstack1l1lll_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨ᪁")),
            bstack1l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪂"): env.get(bstack1l1lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᪃"))
        }
    if env.get(bstack1l1lll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣ᪄")):
        return {
            bstack1l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪅"): bstack1l1lll_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥ᪆"),
            bstack1l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪇"): env.get(bstack1l1lll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᪈")),
            bstack1l1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪉"): bstack1l1lll_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧ᪊").format(env.get(bstack1l1lll_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨ᪋"))) if env.get(bstack1l1lll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤ᪌")) else None,
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪍"): env.get(bstack1l1lll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᪎"))
        }
    if bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥ᪏"))):
        return {
            bstack1l1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪐"): bstack1l1lll_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧ᪑"),
            bstack1l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪒"): env.get(bstack1l1lll_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥ᪓")),
            bstack1l1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪔"): env.get(bstack1l1lll_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦ᪕")),
            bstack1l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪖"): env.get(bstack1l1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᪗"))
        }
    if bstack11l11llll1_opy_(env.get(bstack1l1lll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧ᪘"))):
        return {
            bstack1l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪙"): bstack1l1lll_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢ᪚"),
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪛"): bstack1l1lll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤ᪜").format(env.get(bstack1l1lll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭᪝")), env.get(bstack1l1lll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧ᪞")), env.get(bstack1l1lll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫ᪟"))),
            bstack1l1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪠"): env.get(bstack1l1lll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣ᪡")),
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪢"): env.get(bstack1l1lll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣ᪣"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠤࡆࡍࠧ᪤")) == bstack1l1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᪥") and env.get(bstack1l1lll_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦ᪦")) == bstack1l1lll_opy_ (u"ࠧ࠷ࠢᪧ"):
        return {
            bstack1l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪨"): bstack1l1lll_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢ᪩"),
            bstack1l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪪"): bstack1l1lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧ᪫").format(env.get(bstack1l1lll_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧ᪬"))),
            bstack1l1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪭"): None,
            bstack1l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪮"): None,
        }
    if env.get(bstack1l1lll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ᪯")):
        return {
            bstack1l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪰"): bstack1l1lll_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥ᪱"),
            bstack1l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪲"): None,
            bstack1l1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪳"): env.get(bstack1l1lll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧ᪴")),
            bstack1l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᪵ࠦ"): env.get(bstack1l1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ᪶ࠧ"))
        }
    if any([env.get(bstack1l1lll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇ᪷ࠥ")), env.get(bstack1l1lll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌ᪸ࠣ")), env.get(bstack1l1lll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋ᪹ࠢ")), env.get(bstack1l1lll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐ᪺ࠦ"))]):
        return {
            bstack1l1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪻"): bstack1l1lll_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣ᪼"),
            bstack1l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪽"): None,
            bstack1l1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪾"): env.get(bstack1l1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᪿ")) or None,
            bstack1l1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲᫀࠣ"): env.get(bstack1l1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᫁"), 0)
        }
    if env.get(bstack1l1lll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᫂")):
        return {
            bstack1l1lll_opy_ (u"ࠧࡴࡡ࡮ࡧ᫃ࠥ"): bstack1l1lll_opy_ (u"ࠨࡇࡰࡅࡇ᫄ࠦ"),
            bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᫅"): None,
            bstack1l1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫆"): env.get(bstack1l1lll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᫇")),
            bstack1l1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫈"): env.get(bstack1l1lll_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ᫉"))
        }
    if env.get(bstack1l1lll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆ᫊ࠥ")):
        return {
            bstack1l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᫋"): bstack1l1lll_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥᫌ"),
            bstack1l1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᫍ"): env.get(bstack1l1lll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᫎ")),
            bstack1l1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫏"): env.get(bstack1l1lll_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ᫐")),
            bstack1l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫑"): env.get(bstack1l1lll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᫒"))
        }
    return {bstack1l1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫓"): None}
def get_host_info():
    return {
        bstack1l1lll_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥ᫔"): platform.node(),
        bstack1l1lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ᫕"): platform.system(),
        bstack1l1lll_opy_ (u"ࠥࡸࡾࡶࡥࠣ᫖"): platform.machine(),
        bstack1l1lll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ᫗"): platform.version(),
        bstack1l1lll_opy_ (u"ࠧࡧࡲࡤࡪࠥ᫘"): platform.architecture()[0]
    }
def bstack1ll1l1l11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1l1l1l1l_opy_():
    if bstack11l1l1l1l_opy_.get_property(bstack1l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ᫙")):
        return bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᫚")
    return bstack1l1lll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧ᫛")
def bstack11l1l1ll1ll_opy_(driver):
    info = {
        bstack1l1lll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᫜"): driver.capabilities,
        bstack1l1lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧ᫝"): driver.session_id,
        bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ᫞"): driver.capabilities.get(bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᫟"), None),
        bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᫠"): driver.capabilities.get(bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᫡"), None),
        bstack1l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᫢"): driver.capabilities.get(bstack1l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᫣"), None),
        bstack1l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᫤"):driver.capabilities.get(bstack1l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᫥"), None),
    }
    if bstack11l1l1l1l1l_opy_() == bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᫦"):
        if bstack1llll11ll_opy_():
            info[bstack1l1lll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ᫧")] = bstack1l1lll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᫨")
        elif driver.capabilities.get(bstack1l1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᫩"), {}).get(bstack1l1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭᫪"), False):
            info[bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᫫")] = bstack1l1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ᫬")
        else:
            info[bstack1l1lll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᫭")] = bstack1l1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫮")
    return info
def bstack1llll11ll_opy_():
    if bstack11l1l1l1l_opy_.get_property(bstack1l1lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᫯")):
        return True
    if bstack11l11llll1_opy_(os.environ.get(bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᫰"), None)):
        return True
    return False
def bstack11ll1l111l_opy_(bstack11l1lll11l1_opy_, url, data, config):
    headers = config.get(bstack1l1lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᫱"), None)
    proxies = bstack11ll1l11l_opy_(config, url)
    auth = config.get(bstack1l1lll_opy_ (u"ࠪࡥࡺࡺࡨࠨ᫲"), None)
    response = requests.request(
            bstack11l1lll11l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11ll1l1l1_opy_(bstack1lll11lll1_opy_, size):
    bstack11lll11lll_opy_ = []
    while len(bstack1lll11lll1_opy_) > size:
        bstack1ll111l1l_opy_ = bstack1lll11lll1_opy_[:size]
        bstack11lll11lll_opy_.append(bstack1ll111l1l_opy_)
        bstack1lll11lll1_opy_ = bstack1lll11lll1_opy_[size:]
    bstack11lll11lll_opy_.append(bstack1lll11lll1_opy_)
    return bstack11lll11lll_opy_
def bstack11l1l1l111l_opy_(message, bstack11ll11l1lll_opy_=False):
    os.write(1, bytes(message, bstack1l1lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᫳")))
    os.write(1, bytes(bstack1l1lll_opy_ (u"ࠬࡢ࡮ࠨ᫴"), bstack1l1lll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᫵")))
    if bstack11ll11l1lll_opy_:
        with open(bstack1l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭᫶") + os.environ[bstack1l1lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ᫷")] + bstack1l1lll_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ᫸"), bstack1l1lll_opy_ (u"ࠪࡥࠬ᫹")) as f:
            f.write(message + bstack1l1lll_opy_ (u"ࠫࡡࡴࠧ᫺"))
def bstack1ll1111lll1_opy_():
    return os.environ[bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᫻")].lower() == bstack1l1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᫼")
def bstack1ll111ll1_opy_(bstack11ll111ll1l_opy_):
    return bstack1l1lll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭᫽").format(bstack11ll1l1ll1l_opy_, bstack11ll111ll1l_opy_)
def bstack1l1ll1ll_opy_():
    return bstack111l1lll1l_opy_().replace(tzinfo=None).isoformat() + bstack1l1lll_opy_ (u"ࠨ࡜ࠪ᫾")
def bstack11l1l1ll111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1lll_opy_ (u"ࠩ࡝ࠫ᫿"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1lll_opy_ (u"ࠪ࡞ࠬᬀ")))).total_seconds() * 1000
def bstack11l1ll1ll1l_opy_(timestamp):
    return bstack11l1ll1llll_opy_(timestamp).isoformat() + bstack1l1lll_opy_ (u"ࠫ࡟࠭ᬁ")
def bstack11ll1111l11_opy_(bstack11l1ll1111l_opy_):
    date_format = bstack1l1lll_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᬂ")
    bstack11ll111llll_opy_ = datetime.datetime.strptime(bstack11l1ll1111l_opy_, date_format)
    return bstack11ll111llll_opy_.isoformat() + bstack1l1lll_opy_ (u"࡚࠭ࠨᬃ")
def bstack11l1llllll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᬄ")
    else:
        return bstack1l1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᬅ")
def bstack11l11llll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᬆ")
def bstack11l1l1ll1l1_opy_(val):
    return val.__str__().lower() == bstack1l1lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᬇ")
def bstack111ll1ll1l_opy_(bstack11ll11111l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11ll11111l1_opy_ as e:
                print(bstack1l1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᬈ").format(func.__name__, bstack11ll11111l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11ll11111ll_opy_(bstack11l11lll11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11lll11l_opy_(cls, *args, **kwargs)
            except bstack11ll11111l1_opy_ as e:
                print(bstack1l1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᬉ").format(bstack11l11lll11l_opy_.__name__, bstack11ll11111l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11ll11111ll_opy_
    else:
        return decorator
def bstack1lll111l1l_opy_(bstack1111ll1ll1_opy_):
    if os.getenv(bstack1l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᬊ")) is not None:
        return bstack11l11llll1_opy_(os.getenv(bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᬋ")))
    if bstack1l1lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬌ") in bstack1111ll1ll1_opy_ and bstack11l1l1ll1l1_opy_(bstack1111ll1ll1_opy_[bstack1l1lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᬍ")]):
        return False
    if bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬎ") in bstack1111ll1ll1_opy_ and bstack11l1l1ll1l1_opy_(bstack1111ll1ll1_opy_[bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᬏ")]):
        return False
    return True
def bstack111lllll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack11ll11l111l_opy_ = os.environ.get(bstack1l1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᬐ"), None)
        return bstack11ll11l111l_opy_ is None or bstack11ll11l111l_opy_ == bstack1l1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᬑ")
    except Exception as e:
        return False
def bstack1l1ll1llll_opy_(hub_url, CONFIG):
    if bstack11l1ll1l11_opy_() <= version.parse(bstack1l1lll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᬒ")):
        if hub_url:
            return bstack1l1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᬓ") + hub_url + bstack1l1lll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᬔ")
        return bstack11l1lll11_opy_
    if hub_url:
        return bstack1l1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᬕ") + hub_url + bstack1l1lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᬖ")
    return bstack1l1llll1l_opy_
def bstack11l1l11ll1l_opy_():
    return isinstance(os.getenv(bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᬗ")), str)
def bstack11lllllll_opy_(url):
    return urlparse(url).hostname
def bstack11l1l1ll1l_opy_(hostname):
    for bstack11lll1ll_opy_ in bstack11ll1l11l1_opy_:
        regex = re.compile(bstack11lll1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l11l1l1_opy_(bstack11ll111ll11_opy_, file_name, logger):
    bstack1l1l11111_opy_ = os.path.join(os.path.expanduser(bstack1l1lll_opy_ (u"࠭ࡾࠨᬘ")), bstack11ll111ll11_opy_)
    try:
        if not os.path.exists(bstack1l1l11111_opy_):
            os.makedirs(bstack1l1l11111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1lll_opy_ (u"ࠧࡿࠩᬙ")), bstack11ll111ll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1lll_opy_ (u"ࠨࡹࠪᬚ")):
                pass
            with open(file_path, bstack1l1lll_opy_ (u"ࠤࡺ࠯ࠧᬛ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1l1ll1ll_opy_.format(str(e)))
def bstack11l1lllll11_opy_(file_name, key, value, logger):
    file_path = bstack11l1l11l1l1_opy_(bstack1l1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᬜ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1llll111_opy_ = json.load(open(file_path, bstack1l1lll_opy_ (u"ࠫࡷࡨࠧᬝ")))
        else:
            bstack1l1llll111_opy_ = {}
        bstack1l1llll111_opy_[key] = value
        with open(file_path, bstack1l1lll_opy_ (u"ࠧࡽࠫࠣᬞ")) as outfile:
            json.dump(bstack1l1llll111_opy_, outfile)
def bstack1ll111111_opy_(file_name, logger):
    file_path = bstack11l1l11l1l1_opy_(bstack1l1lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᬟ"), file_name, logger)
    bstack1l1llll111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1lll_opy_ (u"ࠧࡳࠩᬠ")) as bstack11l1l111l_opy_:
            bstack1l1llll111_opy_ = json.load(bstack11l1l111l_opy_)
    return bstack1l1llll111_opy_
def bstack11l1ll111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬᬡ") + file_path + bstack1l1lll_opy_ (u"ࠩࠣࠫᬢ") + str(e))
def bstack11l1ll1l11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1lll_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧᬣ")
def bstack1llll1l1l_opy_(config):
    if bstack1l1lll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᬤ") in config:
        del (config[bstack1l1lll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᬥ")])
        return False
    if bstack11l1ll1l11_opy_() < version.parse(bstack1l1lll_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬᬦ")):
        return False
    if bstack11l1ll1l11_opy_() >= version.parse(bstack1l1lll_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ᬧ")):
        return True
    if bstack1l1lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᬨ") in config and config[bstack1l1lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᬩ")] is False:
        return False
    else:
        return True
def bstack1l11l11111_opy_(args_list, bstack11l1ll11l1l_opy_):
    index = -1
    for value in bstack11l1ll11l1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l1111l1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l1111l1l_opy_ = bstack11l1111l1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᬪ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᬫ"), exception=exception)
    def bstack1111ll1111_opy_(self):
        if self.result != bstack1l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᬬ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᬭ") in self.exception_type:
            return bstack1l1lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᬮ")
        return bstack1l1lll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᬯ")
    def bstack11l1l1l1ll1_opy_(self):
        if self.result != bstack1l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᬰ"):
            return None
        if self.bstack11l1111l1l_opy_:
            return self.bstack11l1111l1l_opy_
        return bstack11l1l11l1ll_opy_(self.exception)
def bstack11l1l11l1ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1llll1l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l111l11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l111l1_opy_(config, logger):
    try:
        import playwright
        bstack11l1l11llll_opy_ = playwright.__file__
        bstack11l1l1l1l11_opy_ = os.path.split(bstack11l1l11llll_opy_)
        bstack11ll11ll11l_opy_ = bstack11l1l1l1l11_opy_[0] + bstack1l1lll_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭ᬱ")
        os.environ[bstack1l1lll_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧᬲ")] = bstack1ll11lll_opy_(config)
        with open(bstack11ll11ll11l_opy_, bstack1l1lll_opy_ (u"ࠬࡸࠧᬳ")) as f:
            bstack1l11lll11l_opy_ = f.read()
            bstack11l1ll1l111_opy_ = bstack1l1lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸ᬴ࠬ")
            bstack11l11llll1l_opy_ = bstack1l11lll11l_opy_.find(bstack11l1ll1l111_opy_)
            if bstack11l11llll1l_opy_ == -1:
              process = subprocess.Popen(bstack1l1lll_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦᬵ"), shell=True, cwd=bstack11l1l1l1l11_opy_[0])
              process.wait()
              bstack11l1lllll1l_opy_ = bstack1l1lll_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨᬶ")
              bstack11l1lll1lll_opy_ = bstack1l1lll_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨᬷ")
              bstack11l1l11l11l_opy_ = bstack1l11lll11l_opy_.replace(bstack11l1lllll1l_opy_, bstack11l1lll1lll_opy_)
              with open(bstack11ll11ll11l_opy_, bstack1l1lll_opy_ (u"ࠪࡻࠬᬸ")) as f:
                f.write(bstack11l1l11l11l_opy_)
    except Exception as e:
        logger.error(bstack11111l1l1_opy_.format(str(e)))
def bstack1ll1ll1l1l_opy_():
  try:
    bstack11l1l111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᬹ"))
    bstack11l1l1111l1_opy_ = []
    if os.path.exists(bstack11l1l111lll_opy_):
      with open(bstack11l1l111lll_opy_) as f:
        bstack11l1l1111l1_opy_ = json.load(f)
      os.remove(bstack11l1l111lll_opy_)
    return bstack11l1l1111l1_opy_
  except:
    pass
  return []
def bstack11llllllll_opy_(bstack1l1111ll_opy_):
  try:
    bstack11l1l1111l1_opy_ = []
    bstack11l1l111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᬺ"))
    if os.path.exists(bstack11l1l111lll_opy_):
      with open(bstack11l1l111lll_opy_) as f:
        bstack11l1l1111l1_opy_ = json.load(f)
    bstack11l1l1111l1_opy_.append(bstack1l1111ll_opy_)
    with open(bstack11l1l111lll_opy_, bstack1l1lll_opy_ (u"࠭ࡷࠨᬻ")) as f:
        json.dump(bstack11l1l1111l1_opy_, f)
  except:
    pass
def bstack11lllll11_opy_(logger, bstack11l1l1lll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᬼ"), bstack1l1lll_opy_ (u"ࠨࠩᬽ"))
    if test_name == bstack1l1lll_opy_ (u"ࠩࠪᬾ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᬿ"), bstack1l1lll_opy_ (u"ࠫࠬᭀ"))
    bstack11ll11ll1l1_opy_ = bstack1l1lll_opy_ (u"ࠬ࠲ࠠࠨᭁ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l1lll1l_opy_:
        bstack11l11l1l1l_opy_ = os.environ.get(bstack1l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᭂ"), bstack1l1lll_opy_ (u"ࠧ࠱ࠩᭃ"))
        bstack11llll1ll1_opy_ = {bstack1l1lll_opy_ (u"ࠨࡰࡤࡱࡪ᭄࠭"): test_name, bstack1l1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᭅ"): bstack11ll11ll1l1_opy_, bstack1l1lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᭆ"): bstack11l11l1l1l_opy_}
        bstack11l1l1l11l1_opy_ = []
        bstack11l1ll1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᭇ"))
        if os.path.exists(bstack11l1ll1l1l1_opy_):
            with open(bstack11l1ll1l1l1_opy_) as f:
                bstack11l1l1l11l1_opy_ = json.load(f)
        bstack11l1l1l11l1_opy_.append(bstack11llll1ll1_opy_)
        with open(bstack11l1ll1l1l1_opy_, bstack1l1lll_opy_ (u"ࠬࡽࠧᭈ")) as f:
            json.dump(bstack11l1l1l11l1_opy_, f)
    else:
        bstack11llll1ll1_opy_ = {bstack1l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᭉ"): test_name, bstack1l1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᭊ"): bstack11ll11ll1l1_opy_, bstack1l1lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᭋ"): str(multiprocessing.current_process().name)}
        if bstack1l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ᭌ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11llll1ll1_opy_)
  except Exception as e:
      logger.warn(bstack1l1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ᭍").format(e))
def bstack111l1l11l_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1ll11l11_opy_ = []
    bstack11llll1ll1_opy_ = {bstack1l1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᭎"): test_name, bstack1l1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᭏"): error_message, bstack1l1lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ᭐"): index}
    bstack11l1l111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ᭑"))
    if os.path.exists(bstack11l1l111111_opy_):
        with open(bstack11l1l111111_opy_) as f:
            bstack11l1ll11l11_opy_ = json.load(f)
    bstack11l1ll11l11_opy_.append(bstack11llll1ll1_opy_)
    with open(bstack11l1l111111_opy_, bstack1l1lll_opy_ (u"ࠨࡹࠪ᭒")) as f:
        json.dump(bstack11l1ll11l11_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ᭓").format(e))
def bstack1l11l1l1_opy_(bstack1lll1l11l1_opy_, name, logger):
  try:
    bstack11llll1ll1_opy_ = {bstack1l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᭔"): name, bstack1l1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᭕"): bstack1lll1l11l1_opy_, bstack1l1lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ᭖"): str(threading.current_thread()._name)}
    return bstack11llll1ll1_opy_
  except Exception as e:
    logger.warn(bstack1l1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ᭗").format(e))
  return
def bstack11l1ll111l1_opy_():
    return platform.system() == bstack1l1lll_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨ᭘")
def bstack1l1l1l1l1l_opy_(bstack11ll11l1l11_opy_, config, logger):
    bstack11l11llllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11ll11l1l11_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ᭙").format(e))
    return bstack11l11llllll_opy_
def bstack11l1l11l111_opy_(bstack11ll111lll1_opy_, bstack11l1llll111_opy_):
    bstack11l1lll1ll1_opy_ = version.parse(bstack11ll111lll1_opy_)
    bstack11l1l1l1111_opy_ = version.parse(bstack11l1llll111_opy_)
    if bstack11l1lll1ll1_opy_ > bstack11l1l1l1111_opy_:
        return 1
    elif bstack11l1lll1ll1_opy_ < bstack11l1l1l1111_opy_:
        return -1
    else:
        return 0
def bstack111l1lll1l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1ll1llll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1llll11l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111ll1l1_opy_(options, framework, bstack1ll1l11ll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1lll_opy_ (u"ࠩࡪࡩࡹ࠭᭚"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11llll111l_opy_ = caps.get(bstack1l1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᭛"))
    bstack11ll11l1l1l_opy_ = True
    bstack1ll1l1ll1l_opy_ = os.environ[bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᭜")]
    if bstack11l1l1ll1l1_opy_(caps.get(bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫ᭝"))) or bstack11l1l1ll1l1_opy_(caps.get(bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭᭞"))):
        bstack11ll11l1l1l_opy_ = False
    if bstack1llll1l1l_opy_({bstack1l1lll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ᭟"): bstack11ll11l1l1l_opy_}):
        bstack11llll111l_opy_ = bstack11llll111l_opy_ or {}
        bstack11llll111l_opy_[bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭠")] = bstack11l1llll11l_opy_(framework)
        bstack11llll111l_opy_[bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭡")] = bstack1ll1111lll1_opy_()
        bstack11llll111l_opy_[bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭢")] = bstack1ll1l1ll1l_opy_
        bstack11llll111l_opy_[bstack1l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭣")] = bstack1ll1l11ll_opy_
        if getattr(options, bstack1l1lll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭᭤"), None):
            options.set_capability(bstack1l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᭥"), bstack11llll111l_opy_)
        else:
            options[bstack1l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᭦")] = bstack11llll111l_opy_
    else:
        if getattr(options, bstack1l1lll_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᭧"), None):
            options.set_capability(bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭨"), bstack11l1llll11l_opy_(framework))
            options.set_capability(bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭩"), bstack1ll1111lll1_opy_())
            options.set_capability(bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭪"), bstack1ll1l1ll1l_opy_)
            options.set_capability(bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭫"), bstack1ll1l11ll_opy_)
        else:
            options[bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑ᭬ࠧ")] = bstack11l1llll11l_opy_(framework)
            options[bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭭")] = bstack1ll1111lll1_opy_()
            options[bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭮")] = bstack1ll1l1ll1l_opy_
            options[bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭯")] = bstack1ll1l11ll_opy_
    return options
def bstack11ll11l11l1_opy_(bstack11l1l111ll1_opy_, framework):
    bstack1ll1l11ll_opy_ = bstack11l1l1l1l_opy_.get_property(bstack1l1lll_opy_ (u"ࠥࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡑࡔࡒࡈ࡚ࡉࡔࡠࡏࡄࡔࠧ᭰"))
    if bstack11l1l111ll1_opy_ and len(bstack11l1l111ll1_opy_.split(bstack1l1lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᭱"))) > 1:
        ws_url = bstack11l1l111ll1_opy_.split(bstack1l1lll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ᭲"))[0]
        if bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ᭳") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1lll1l1l_opy_ = json.loads(urllib.parse.unquote(bstack11l1l111ll1_opy_.split(bstack1l1lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭴"))[1]))
            bstack11l1lll1l1l_opy_ = bstack11l1lll1l1l_opy_ or {}
            bstack1ll1l1ll1l_opy_ = os.environ[bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᭵")]
            bstack11l1lll1l1l_opy_[bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭶")] = str(framework) + str(__version__)
            bstack11l1lll1l1l_opy_[bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭷")] = bstack1ll1111lll1_opy_()
            bstack11l1lll1l1l_opy_[bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭸")] = bstack1ll1l1ll1l_opy_
            bstack11l1lll1l1l_opy_[bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭹")] = bstack1ll1l11ll_opy_
            bstack11l1l111ll1_opy_ = bstack11l1l111ll1_opy_.split(bstack1l1lll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ᭺"))[0] + bstack1l1lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭻") + urllib.parse.quote(json.dumps(bstack11l1lll1l1l_opy_))
    return bstack11l1l111ll1_opy_
def bstack1lll1l1l_opy_():
    global bstack1ll11l1ll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll11l1ll_opy_ = BrowserType.connect
    return bstack1ll11l1ll_opy_
def bstack11l11lll_opy_(framework_name):
    global bstack11l11l1l_opy_
    bstack11l11l1l_opy_ = framework_name
    return framework_name
def bstack11ll111lll_opy_(self, *args, **kwargs):
    global bstack1ll11l1ll_opy_
    try:
        global bstack11l11l1l_opy_
        if bstack1l1lll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ᭼") in kwargs:
            kwargs[bstack1l1lll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭᭽")] = bstack11ll11l11l1_opy_(
                kwargs.get(bstack1l1lll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ᭾"), None),
                bstack11l11l1l_opy_
            )
    except Exception as e:
        logger.error(bstack1l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦ᭿").format(str(e)))
    return bstack1ll11l1ll_opy_(self, *args, **kwargs)
def bstack11ll111l1l1_opy_(bstack11l1ll111ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11ll1l11l_opy_(bstack11l1ll111ll_opy_, bstack1l1lll_opy_ (u"ࠧࠨᮀ"))
        if proxies and proxies.get(bstack1l1lll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᮁ")):
            parsed_url = urlparse(proxies.get(bstack1l1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᮂ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᮃ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᮄ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᮅ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᮆ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l11lll11_opy_(bstack11l1ll111ll_opy_):
    bstack11l1l1111ll_opy_ = {
        bstack11ll11lll1l_opy_[bstack11l11llll11_opy_]: bstack11l1ll111ll_opy_[bstack11l11llll11_opy_]
        for bstack11l11llll11_opy_ in bstack11l1ll111ll_opy_
        if bstack11l11llll11_opy_ in bstack11ll11lll1l_opy_
    }
    bstack11l1l1111ll_opy_[bstack1l1lll_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᮇ")] = bstack11ll111l1l1_opy_(bstack11l1ll111ll_opy_, bstack11l1l1l1l_opy_.get_property(bstack1l1lll_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᮈ")))
    bstack11ll11l11ll_opy_ = [element.lower() for element in bstack11ll1l1l1ll_opy_]
    bstack11l1l111l11_opy_(bstack11l1l1111ll_opy_, bstack11ll11l11ll_opy_)
    return bstack11l1l1111ll_opy_
def bstack11l1l111l11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1lll_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᮉ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l1l111l11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l1l111l11_opy_(item, keys)
def bstack1l1lll1111l_opy_():
    bstack11l1l1l1lll_opy_ = [os.environ.get(bstack1l1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡋࡏࡉࡘࡥࡄࡊࡔࠥᮊ")), os.path.join(os.path.expanduser(bstack1l1lll_opy_ (u"ࠤࢁࠦᮋ")), bstack1l1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᮌ")), os.path.join(bstack1l1lll_opy_ (u"ࠫ࠴ࡺ࡭ࡱࠩᮍ"), bstack1l1lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᮎ"))]
    for path in bstack11l1l1l1lll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1lll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨᮏ") + str(path) + bstack1l1lll_opy_ (u"ࠢࠨࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥᮐ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1lll_opy_ (u"ࠣࡉ࡬ࡺ࡮ࡴࡧࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸࠦࡦࡰࡴࠣࠫࠧᮑ") + str(path) + bstack1l1lll_opy_ (u"ࠤࠪࠦᮒ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᮓ") + str(path) + bstack1l1lll_opy_ (u"ࠦࠬࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳ࠯ࠤᮔ"))
            else:
                logger.debug(bstack1l1lll_opy_ (u"ࠧࡉࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥ࠭ࠢᮕ") + str(path) + bstack1l1lll_opy_ (u"ࠨࠧࠡࡹ࡬ࡸ࡭ࠦࡷࡳ࡫ࡷࡩࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯࠰ࠥᮖ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1lll_opy_ (u"ࠢࡐࡲࡨࡶࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩࠦࡦࡰࡴࠣࠫࠧᮗ") + str(path) + bstack1l1lll_opy_ (u"ࠣࠩ࠱ࠦᮘ"))
            return path
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡸࡴࠥ࡬ࡩ࡭ࡧࠣࠫࢀࡶࡡࡵࡪࢀࠫ࠿ࠦࠢᮙ") + str(e) + bstack1l1lll_opy_ (u"ࠥࠦᮚ"))
    logger.debug(bstack1l1lll_opy_ (u"ࠦࡆࡲ࡬ࠡࡲࡤࡸ࡭ࡹࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠣᮛ"))
    return None
@measure(event_name=EVENTS.bstack11ll1lll11l_opy_, stage=STAGE.bstack1111lll1_opy_)
def bstack1llll111111_opy_(binary_path, bstack1lllll111l1_opy_, bs_config):
    logger.debug(bstack1l1lll_opy_ (u"ࠧࡉࡵࡳࡴࡨࡲࡹࠦࡃࡍࡋࠣࡔࡦࡺࡨࠡࡨࡲࡹࡳࡪ࠺ࠡࡽࢀࠦᮜ").format(binary_path))
    bstack11l1l111l1l_opy_ = bstack1l1lll_opy_ (u"࠭ࠧᮝ")
    bstack11l1ll1l11l_opy_ = {
        bstack1l1lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᮞ"): __version__,
        bstack1l1lll_opy_ (u"ࠣࡱࡶࠦᮟ"): platform.system(),
        bstack1l1lll_opy_ (u"ࠤࡲࡷࡤࡧࡲࡤࡪࠥᮠ"): platform.machine(),
        bstack1l1lll_opy_ (u"ࠥࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᮡ"): bstack1l1lll_opy_ (u"ࠫ࠵࠭ᮢ"),
        bstack1l1lll_opy_ (u"ࠧࡹࡤ࡬ࡡ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠦᮣ"): bstack1l1lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᮤ")
    }
    bstack11l1ll1lll1_opy_(bstack11l1ll1l11l_opy_)
    try:
        if binary_path:
            bstack11l1ll1l11l_opy_[bstack1l1lll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᮥ")] = subprocess.check_output([binary_path, bstack1l1lll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᮦ")]).strip().decode(bstack1l1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᮧ"))
        response = requests.request(
            bstack1l1lll_opy_ (u"ࠪࡋࡊ࡚ࠧᮨ"),
            url=bstack1ll111ll1_opy_(bstack11ll1lllll1_opy_),
            headers=None,
            auth=(bs_config[bstack1l1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᮩ")], bs_config[bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᮪")]),
            json=None,
            params=bstack11l1ll1l11l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1lll_opy_ (u"࠭ࡵࡳ࡮᮫ࠪ") in data.keys() and bstack1l1lll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᮬ") in data.keys():
            logger.debug(bstack1l1lll_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤᮭ").format(bstack11l1ll1l11l_opy_[bstack1l1lll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᮮ")]))
            bstack11ll11ll1ll_opy_ = bstack11l1l1lllll_opy_(data[bstack1l1lll_opy_ (u"ࠪࡹࡷࡲࠧᮯ")], bstack1lllll111l1_opy_)
            bstack11l1l111l1l_opy_ = os.path.join(bstack1lllll111l1_opy_, bstack11ll11ll1ll_opy_)
            os.chmod(bstack11l1l111l1l_opy_, 0o777) # bstack11l1llll1ll_opy_ permission
            return bstack11l1l111l1l_opy_
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦ᮰").format(e))
    return binary_path
def bstack11l1ll1lll1_opy_(bstack11l1ll1l11l_opy_):
    try:
        if bstack1l1lll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫ᮱") not in bstack11l1ll1l11l_opy_[bstack1l1lll_opy_ (u"࠭࡯ࡴࠩ᮲")].lower():
            return
        if os.path.exists(bstack1l1lll_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ᮳")):
            with open(bstack1l1lll_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ᮴"), bstack1l1lll_opy_ (u"ࠤࡵࠦ᮵")) as f:
                bstack11l1ll11lll_opy_ = {}
                for line in f:
                    if bstack1l1lll_opy_ (u"ࠥࡁࠧ᮶") in line:
                        key, value = line.rstrip().split(bstack1l1lll_opy_ (u"ࠦࡂࠨ᮷"), 1)
                        bstack11l1ll11lll_opy_[key] = value.strip(bstack1l1lll_opy_ (u"ࠬࠨ࡜ࠨࠩ᮸"))
                bstack11l1ll1l11l_opy_[bstack1l1lll_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭᮹")] = bstack11l1ll11lll_opy_.get(bstack1l1lll_opy_ (u"ࠢࡊࡆࠥᮺ"), bstack1l1lll_opy_ (u"ࠣࠤᮻ"))
        elif os.path.exists(bstack1l1lll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣᮼ")):
            bstack11l1ll1l11l_opy_[bstack1l1lll_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪᮽ")] = bstack1l1lll_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨࠫᮾ")
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾࠢᮿ") + e)
@measure(event_name=EVENTS.bstack11ll1ll1l1l_opy_, stage=STAGE.bstack1111lll1_opy_)
def bstack11l1l1lllll_opy_(bstack11ll11l1111_opy_, bstack11l11lll1l1_opy_):
    logger.debug(bstack1l1lll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣᯀ") + str(bstack11ll11l1111_opy_) + bstack1l1lll_opy_ (u"ࠢࠣᯁ"))
    zip_path = os.path.join(bstack11l11lll1l1_opy_, bstack1l1lll_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶࠢᯂ"))
    bstack11ll11ll1ll_opy_ = bstack1l1lll_opy_ (u"ࠩࠪᯃ")
    with requests.get(bstack11ll11l1111_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1lll_opy_ (u"ࠥࡻࡧࠨᯄ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1lll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨᯅ"))
    with zipfile.ZipFile(zip_path, bstack1l1lll_opy_ (u"ࠬࡸࠧᯆ")) as zip_ref:
        bstack11l1l1ll11l_opy_ = zip_ref.namelist()
        if len(bstack11l1l1ll11l_opy_) > 0:
            bstack11ll11ll1ll_opy_ = bstack11l1l1ll11l_opy_[0] # bstack11l1l1lll11_opy_ bstack11ll1ll1l11_opy_ will be bstack11l1lll1l11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l11lll1l1_opy_)
        logger.debug(bstack1l1lll_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱࠣࠫࠧᯇ") + str(bstack11l11lll1l1_opy_) + bstack1l1lll_opy_ (u"ࠢࠨࠤᯈ"))
    os.remove(zip_path)
    return bstack11ll11ll1ll_opy_
def get_cli_dir():
    bstack11l1ll11ll1_opy_ = bstack1l1lll1111l_opy_()
    if bstack11l1ll11ll1_opy_:
        bstack1lllll111l1_opy_ = os.path.join(bstack11l1ll11ll1_opy_, bstack1l1lll_opy_ (u"ࠣࡥ࡯࡭ࠧᯉ"))
        if not os.path.exists(bstack1lllll111l1_opy_):
            os.makedirs(bstack1lllll111l1_opy_, mode=0o777, exist_ok=True)
        return bstack1lllll111l1_opy_
    else:
        raise FileNotFoundError(bstack1l1lll_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠧᯊ"))
def bstack1lll11l1l11_opy_(bstack1lllll111l1_opy_):
    bstack1l1lll_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨࠢᯋ")
    bstack11l1ll1l1ll_opy_ = [
        os.path.join(bstack1lllll111l1_opy_, f)
        for f in os.listdir(bstack1lllll111l1_opy_)
        if os.path.isfile(os.path.join(bstack1lllll111l1_opy_, f)) and f.startswith(bstack1l1lll_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱ࠧᯌ"))
    ]
    if len(bstack11l1ll1l1ll_opy_) > 0:
        return max(bstack11l1ll1l1ll_opy_, key=os.path.getmtime) # get bstack11ll11lll11_opy_ binary
    return bstack1l1lll_opy_ (u"ࠧࠨᯍ")
def bstack1ll11lll1l1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll11lll1l1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d