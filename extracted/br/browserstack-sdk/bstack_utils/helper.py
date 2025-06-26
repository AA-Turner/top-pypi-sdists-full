# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
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
from bstack_utils.constants import (bstack1l1l1l11l_opy_, bstack1lll111lll_opy_, bstack1ll11l111l_opy_,
                                    bstack11ll111l111_opy_, bstack11l1lll11l1_opy_, bstack11ll11111l1_opy_, bstack11l1lll111l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l11l11lll_opy_, bstack11ll1l1l1_opy_
from bstack_utils.proxy import bstack1lll11l11l_opy_, bstack1l1ll11l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack11l1l1l111_opy_
from bstack_utils.bstack11ll111l1l_opy_ import bstack111l11ll_opy_
from browserstack_sdk._version import __version__
bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
logger = bstack11l1l1l111_opy_.get_logger(__name__, bstack11l1l1l111_opy_.bstack1llll11l1ll_opy_())
def bstack11lll1111l1_opy_(config):
    return config[bstack11ll1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᪱")]
def bstack11ll1llll11_opy_(config):
    return config[bstack11ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᪲")]
def bstack11l1ll1lll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111lll1ll11_opy_(obj):
    values = []
    bstack111llllll1l_opy_ = re.compile(bstack11ll1l1_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢ᪳"), re.I)
    for key in obj.keys():
        if bstack111llllll1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11ll111l_opy_(config):
    tags = []
    tags.extend(bstack111lll1ll11_opy_(os.environ))
    tags.extend(bstack111lll1ll11_opy_(config))
    return tags
def bstack11l11l1l1ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11lll11l_opy_(bstack11l1111l1ll_opy_):
    if not bstack11l1111l1ll_opy_:
        return bstack11ll1l1_opy_ (u"ࠫࠬ᪴")
    return bstack11ll1l1_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨ᪵").format(bstack11l1111l1ll_opy_.name, bstack11l1111l1ll_opy_.email)
def bstack11ll1l1l11l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l111l111l_opy_ = repo.common_dir
        info = {
            bstack11ll1l1_opy_ (u"ࠨࡳࡩࡣ᪶ࠥ"): repo.head.commit.hexsha,
            bstack11ll1l1_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣ᪷ࠥ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11ll1l1_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨ᪸ࠣ"): repo.active_branch.name,
            bstack11ll1l1_opy_ (u"ࠤࡷࡥ࡬ࠨ᪹"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11ll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨ᪺"): bstack11l11lll11l_opy_(repo.head.commit.committer),
            bstack11ll1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧ᪻"): repo.head.commit.committed_datetime.isoformat(),
            bstack11ll1l1_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧ᪼"): bstack11l11lll11l_opy_(repo.head.commit.author),
            bstack11ll1l1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨ᪽ࠦ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11ll1l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᪾"): repo.head.commit.message,
            bstack11ll1l1_opy_ (u"ࠣࡴࡲࡳࡹࠨᪿ"): repo.git.rev_parse(bstack11ll1l1_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ᫀࠦ")),
            bstack11ll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦ᫁"): bstack11l111l111l_opy_,
            bstack11ll1l1_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ᫂"): subprocess.check_output([bstack11ll1l1_opy_ (u"ࠧ࡭ࡩࡵࠤ᫃"), bstack11ll1l1_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤ᫄"), bstack11ll1l1_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥ᫅")]).strip().decode(
                bstack11ll1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᫆")),
            bstack11ll1l1_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦ᫇"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11ll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ᫈"): repo.git.rev_list(
                bstack11ll1l1_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦ᫉").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l11ll11l1_opy_ = []
        for remote in remotes:
            bstack11l1111l11l_opy_ = {
                bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧ᫊ࠥ"): remote.name,
                bstack11ll1l1_opy_ (u"ࠨࡵࡳ࡮ࠥ᫋"): remote.url,
            }
            bstack11l11ll11l1_opy_.append(bstack11l1111l11l_opy_)
        bstack111llll11ll_opy_ = {
            bstack11ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᫌ"): bstack11ll1l1_opy_ (u"ࠣࡩ࡬ࡸࠧᫍ"),
            **info,
            bstack11ll1l1_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᫎ"): bstack11l11ll11l1_opy_
        }
        bstack111llll11ll_opy_ = bstack11l11ll1lll_opy_(bstack111llll11ll_opy_)
        return bstack111llll11ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11ll1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ᫏").format(err))
        return {}
def bstack11l11ll1lll_opy_(bstack111llll11ll_opy_):
    bstack11l111l1l1l_opy_ = bstack11l11111l11_opy_(bstack111llll11ll_opy_)
    if bstack11l111l1l1l_opy_ and bstack11l111l1l1l_opy_ > bstack11ll111l111_opy_:
        bstack11l1l11111l_opy_ = bstack11l111l1l1l_opy_ - bstack11ll111l111_opy_
        bstack11l11l11ll1_opy_ = bstack11l1l11l111_opy_(bstack111llll11ll_opy_[bstack11ll1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ᫐")], bstack11l1l11111l_opy_)
        bstack111llll11ll_opy_[bstack11ll1l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᫑")] = bstack11l11l11ll1_opy_
        logger.info(bstack11ll1l1_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣ᫒")
                    .format(bstack11l11111l11_opy_(bstack111llll11ll_opy_) / 1024))
    return bstack111llll11ll_opy_
def bstack11l11111l11_opy_(bstack1lll11ll11_opy_):
    try:
        if bstack1lll11ll11_opy_:
            bstack11l1l111l11_opy_ = json.dumps(bstack1lll11ll11_opy_)
            bstack111lllll1l1_opy_ = sys.getsizeof(bstack11l1l111l11_opy_)
            return bstack111lllll1l1_opy_
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢ᫓").format(e))
    return -1
def bstack11l1l11l111_opy_(field, bstack11l111l11ll_opy_):
    try:
        bstack11l111l11l1_opy_ = len(bytes(bstack11l1lll11l1_opy_, bstack11ll1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᫔")))
        bstack111lllllll1_opy_ = bytes(field, bstack11ll1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᫕"))
        bstack11l11ll1ll1_opy_ = len(bstack111lllllll1_opy_)
        bstack11l11111l1l_opy_ = ceil(bstack11l11ll1ll1_opy_ - bstack11l111l11ll_opy_ - bstack11l111l11l1_opy_)
        if bstack11l11111l1l_opy_ > 0:
            bstack11l1111111l_opy_ = bstack111lllllll1_opy_[:bstack11l11111l1l_opy_].decode(bstack11ll1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᫖"), errors=bstack11ll1l1_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫ᫗")) + bstack11l1lll11l1_opy_
            return bstack11l1111111l_opy_
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥ᫘").format(e))
    return field
def bstack1l1l1l111l_opy_():
    env = os.environ
    if (bstack11ll1l1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ᫙") in env and len(env[bstack11ll1l1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᫚")]) > 0) or (
            bstack11ll1l1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ᫛") in env and len(env[bstack11ll1l1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᫜")]) > 0):
        return {
            bstack11ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫝"): bstack11ll1l1_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧ᫞"),
            bstack11ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᫟"): env.get(bstack11ll1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᫠")),
            bstack11ll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᫡"): env.get(bstack11ll1l1_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥ᫢")),
            bstack11ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᫣"): env.get(bstack11ll1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᫤"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠦࡈࡏࠢ᫥")) == bstack11ll1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ᫦") and bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣ᫧"))):
        return {
            bstack11ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᫨"): bstack11ll1l1_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥ᫩"),
            bstack11ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᫪"): env.get(bstack11ll1l1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᫫")),
            bstack11ll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫬"): env.get(bstack11ll1l1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤ᫭")),
            bstack11ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᫮"): env.get(bstack11ll1l1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥ᫯"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠣࡅࡌࠦ᫰")) == bstack11ll1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᫱") and bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥ᫲"))):
        return {
            bstack11ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫳"): bstack11ll1l1_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣ᫴"),
            bstack11ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫵"): env.get(bstack11ll1l1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢ᫶")),
            bstack11ll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫷"): env.get(bstack11ll1l1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᫸")),
            bstack11ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫹"): env.get(bstack11ll1l1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᫺"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠧࡉࡉࠣ᫻")) == bstack11ll1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ᫼") and env.get(bstack11ll1l1_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣ᫽")) == bstack11ll1l1_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ᫾"):
        return {
            bstack11ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫿"): bstack11ll1l1_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧᬀ"),
            bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᬁ"): None,
            bstack11ll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬂ"): None,
            bstack11ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᬃ"): None
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥᬄ")) and env.get(bstack11ll1l1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦᬅ")):
        return {
            bstack11ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬆ"): bstack11ll1l1_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨᬇ"),
            bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᬈ"): env.get(bstack11ll1l1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥᬉ")),
            bstack11ll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᬊ"): None,
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬋ"): env.get(bstack11ll1l1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᬌ"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠤࡆࡍࠧᬍ")) == bstack11ll1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᬎ") and bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᬏ"))):
        return {
            bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬐ"): bstack11ll1l1_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧᬑ"),
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬒ"): env.get(bstack11ll1l1_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦᬓ")),
            bstack11ll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᬔ"): None,
            bstack11ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᬕ"): env.get(bstack11ll1l1_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᬖ"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠧࡉࡉࠣᬗ")) == bstack11ll1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦᬘ") and bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥᬙ"))):
        return {
            bstack11ll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᬚ"): bstack11ll1l1_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧᬛ"),
            bstack11ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬜ"): env.get(bstack11ll1l1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᬝ")),
            bstack11ll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬞ"): env.get(bstack11ll1l1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᬟ")),
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬠ"): env.get(bstack11ll1l1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦᬡ"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠤࡆࡍࠧᬢ")) == bstack11ll1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᬣ") and bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᬤ"))):
        return {
            bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬥ"): bstack11ll1l1_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨᬦ"),
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬧ"): env.get(bstack11ll1l1_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧᬨ")),
            bstack11ll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᬩ"): env.get(bstack11ll1l1_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᬪ")),
            bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᬫ"): env.get(bstack11ll1l1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᬬ"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠨࡃࡊࠤᬭ")) == bstack11ll1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧᬮ") and bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᬯ"))):
        return {
            bstack11ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬰ"): bstack11ll1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᬱ"),
            bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᬲ"): env.get(bstack11ll1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᬳ")),
            bstack11ll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᬴ࠣ"): env.get(bstack11ll1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᬵ")) or env.get(bstack11ll1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᬶ")),
            bstack11ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᬷ"): env.get(bstack11ll1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᬸ"))
        }
    if bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᬹ"))):
        return {
            bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬺ"): bstack11ll1l1_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᬻ"),
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬼ"): bstack11ll1l1_opy_ (u"ࠣࡽࢀࡿࢂࠨᬽ").format(env.get(bstack11ll1l1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᬾ")), env.get(bstack11ll1l1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᬿ"))),
            bstack11ll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᭀ"): env.get(bstack11ll1l1_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᭁ")),
            bstack11ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᭂ"): env.get(bstack11ll1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᭃ"))
        }
    if bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔ᭄ࠥ"))):
        return {
            bstack11ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᭅ"): bstack11ll1l1_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᭆ"),
            bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᭇ"): bstack11ll1l1_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᭈ").format(env.get(bstack11ll1l1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᭉ")), env.get(bstack11ll1l1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᭊ")), env.get(bstack11ll1l1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᭋ")), env.get(bstack11ll1l1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᭌ"))),
            bstack11ll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭍"): env.get(bstack11ll1l1_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᭎")),
            bstack11ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᭏"): env.get(bstack11ll1l1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᭐"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣ᭑")) and env.get(bstack11ll1l1_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥ᭒")):
        return {
            bstack11ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᭓"): bstack11ll1l1_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧ᭔"),
            bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᭕"): bstack11ll1l1_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣ᭖").format(env.get(bstack11ll1l1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩ᭗")), env.get(bstack11ll1l1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬ᭘")), env.get(bstack11ll1l1_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨ᭙"))),
            bstack11ll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᭚"): env.get(bstack11ll1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ᭛")),
            bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᭜"): env.get(bstack11ll1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ᭝"))
        }
    if any([env.get(bstack11ll1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᭞")), env.get(bstack11ll1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᭟")), env.get(bstack11ll1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ᭠"))]):
        return {
            bstack11ll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᭡"): bstack11ll1l1_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥ᭢"),
            bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᭣"): env.get(bstack11ll1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᭤")),
            bstack11ll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᭥"): env.get(bstack11ll1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᭦")),
            bstack11ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᭧"): env.get(bstack11ll1l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᭨"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ᭩")):
        return {
            bstack11ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭪"): bstack11ll1l1_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧ᭫"),
            bstack11ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᭬"): env.get(bstack11ll1l1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤ᭭")),
            bstack11ll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᭮"): env.get(bstack11ll1l1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣ᭯")),
            bstack11ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭰"): env.get(bstack11ll1l1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ᭱"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨ᭲")) or env.get(bstack11ll1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ᭳")):
        return {
            bstack11ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭴"): bstack11ll1l1_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤ᭵"),
            bstack11ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭶"): env.get(bstack11ll1l1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᭷")),
            bstack11ll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᭸"): bstack11ll1l1_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧ᭹") if env.get(bstack11ll1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ᭺")) else None,
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᭻"): env.get(bstack11ll1l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ᭼"))
        }
    if any([env.get(bstack11ll1l1_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ᭽")), env.get(bstack11ll1l1_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ᭾")), env.get(bstack11ll1l1_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ᭿"))]):
        return {
            bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᮀ"): bstack11ll1l1_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧᮁ"),
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮂ"): None,
            bstack11ll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮃ"): env.get(bstack11ll1l1_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨᮄ")),
            bstack11ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮅ"): env.get(bstack11ll1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᮆ"))
        }
    if env.get(bstack11ll1l1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣᮇ")):
        return {
            bstack11ll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᮈ"): bstack11ll1l1_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥᮉ"),
            bstack11ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮊ"): env.get(bstack11ll1l1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᮋ")),
            bstack11ll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮌ"): bstack11ll1l1_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧᮍ").format(env.get(bstack11ll1l1_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨᮎ"))) if env.get(bstack11ll1l1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤᮏ")) else None,
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮐ"): env.get(bstack11ll1l1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᮑ"))
        }
    if bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥᮒ"))):
        return {
            bstack11ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᮓ"): bstack11ll1l1_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧᮔ"),
            bstack11ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮕ"): env.get(bstack11ll1l1_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥᮖ")),
            bstack11ll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮗ"): env.get(bstack11ll1l1_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦᮘ")),
            bstack11ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᮙ"): env.get(bstack11ll1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᮚ"))
        }
    if bstack11l1l111ll_opy_(env.get(bstack11ll1l1_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧᮛ"))):
        return {
            bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᮜ"): bstack11ll1l1_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢᮝ"),
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮞ"): bstack11ll1l1_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤᮟ").format(env.get(bstack11ll1l1_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ᮠ")), env.get(bstack11ll1l1_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧᮡ")), env.get(bstack11ll1l1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫᮢ"))),
            bstack11ll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᮣ"): env.get(bstack11ll1l1_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣᮤ")),
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮥ"): env.get(bstack11ll1l1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣᮦ"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠤࡆࡍࠧᮧ")) == bstack11ll1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᮨ") and env.get(bstack11ll1l1_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦᮩ")) == bstack11ll1l1_opy_ (u"ࠧ࠷᮪ࠢ"):
        return {
            bstack11ll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᮫ࠦ"): bstack11ll1l1_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢᮬ"),
            bstack11ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮭ"): bstack11ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧᮮ").format(env.get(bstack11ll1l1_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧᮯ"))),
            bstack11ll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᮰"): None,
            bstack11ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᮱"): None,
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ᮲")):
        return {
            bstack11ll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᮳"): bstack11ll1l1_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥ᮴"),
            bstack11ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᮵"): None,
            bstack11ll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᮶"): env.get(bstack11ll1l1_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧ᮷")),
            bstack11ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᮸"): env.get(bstack11ll1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᮹"))
        }
    if any([env.get(bstack11ll1l1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥᮺ")), env.get(bstack11ll1l1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣᮻ")), env.get(bstack11ll1l1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢᮼ")), env.get(bstack11ll1l1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦᮽ"))]):
        return {
            bstack11ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᮾ"): bstack11ll1l1_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣᮿ"),
            bstack11ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯀ"): None,
            bstack11ll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᯁ"): env.get(bstack11ll1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᯂ")) or None,
            bstack11ll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᯃ"): env.get(bstack11ll1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᯄ"), 0)
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᯅ")):
        return {
            bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯆ"): bstack11ll1l1_opy_ (u"ࠨࡇࡰࡅࡇࠦᯇ"),
            bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᯈ"): None,
            bstack11ll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᯉ"): env.get(bstack11ll1l1_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᯊ")),
            bstack11ll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᯋ"): env.get(bstack11ll1l1_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥᯌ"))
        }
    if env.get(bstack11ll1l1_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᯍ")):
        return {
            bstack11ll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᯎ"): bstack11ll1l1_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥᯏ"),
            bstack11ll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᯐ"): env.get(bstack11ll1l1_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᯑ")),
            bstack11ll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᯒ"): env.get(bstack11ll1l1_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᯓ")),
            bstack11ll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᯔ"): env.get(bstack11ll1l1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᯕ"))
        }
    return {bstack11ll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᯖ"): None}
def get_host_info():
    return {
        bstack11ll1l1_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥᯗ"): platform.node(),
        bstack11ll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦᯘ"): platform.system(),
        bstack11ll1l1_opy_ (u"ࠥࡸࡾࡶࡥࠣᯙ"): platform.machine(),
        bstack11ll1l1_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᯚ"): platform.version(),
        bstack11ll1l1_opy_ (u"ࠧࡧࡲࡤࡪࠥᯛ"): platform.architecture()[0]
    }
def bstack1ll1ll1l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l111ll11l_opy_():
    if bstack1111ll111_opy_.get_property(bstack11ll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᯜ")):
        return bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᯝ")
    return bstack11ll1l1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧᯞ")
def bstack11l111lll1l_opy_(driver):
    info = {
        bstack11ll1l1_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᯟ"): driver.capabilities,
        bstack11ll1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧᯠ"): driver.session_id,
        bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᯡ"): driver.capabilities.get(bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᯢ"), None),
        bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᯣ"): driver.capabilities.get(bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᯤ"), None),
        bstack11ll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᯥ"): driver.capabilities.get(bstack11ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᯦"), None),
        bstack11ll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᯧ"):driver.capabilities.get(bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᯨ"), None),
    }
    if bstack11l111ll11l_opy_() == bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᯩ"):
        if bstack1llll1l1l1_opy_():
            info[bstack11ll1l1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᯪ")] = bstack11ll1l1_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᯫ")
        elif driver.capabilities.get(bstack11ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᯬ"), {}).get(bstack11ll1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᯭ"), False):
            info[bstack11ll1l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᯮ")] = bstack11ll1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᯯ")
        else:
            info[bstack11ll1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᯰ")] = bstack11ll1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᯱ")
    return info
def bstack1llll1l1l1_opy_():
    if bstack1111ll111_opy_.get_property(bstack11ll1l1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ᯲࠭")):
        return True
    if bstack11l1l111ll_opy_(os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆ᯳ࠩ"), None)):
        return True
    return False
def bstack11lll1111_opy_(bstack111llll1l11_opy_, url, data, config):
    headers = config.get(bstack11ll1l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᯴"), None)
    proxies = bstack1lll11l11l_opy_(config, url)
    auth = config.get(bstack11ll1l1_opy_ (u"ࠪࡥࡺࡺࡨࠨ᯵"), None)
    response = requests.request(
            bstack111llll1l11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11lll1l1l_opy_(bstack1llll1l11_opy_, size):
    bstack1lllll11l1_opy_ = []
    while len(bstack1llll1l11_opy_) > size:
        bstack1l111ll111_opy_ = bstack1llll1l11_opy_[:size]
        bstack1lllll11l1_opy_.append(bstack1l111ll111_opy_)
        bstack1llll1l11_opy_ = bstack1llll1l11_opy_[size:]
    bstack1lllll11l1_opy_.append(bstack1llll1l11_opy_)
    return bstack1lllll11l1_opy_
def bstack111llll111l_opy_(message, bstack111lllll11l_opy_=False):
    os.write(1, bytes(message, bstack11ll1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᯶")))
    os.write(1, bytes(bstack11ll1l1_opy_ (u"ࠬࡢ࡮ࠨ᯷"), bstack11ll1l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᯸")))
    if bstack111lllll11l_opy_:
        with open(bstack11ll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭᯹") + os.environ[bstack11ll1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ᯺")] + bstack11ll1l1_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ᯻"), bstack11ll1l1_opy_ (u"ࠪࡥࠬ᯼")) as f:
            f.write(message + bstack11ll1l1_opy_ (u"ࠫࡡࡴࠧ᯽"))
def bstack1l1lll11111_opy_():
    return os.environ[bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᯾")].lower() == bstack11ll1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫ᯿")
def bstack1ll1l11l11_opy_():
    return bstack111ll111ll_opy_().replace(tzinfo=None).isoformat() + bstack11ll1l1_opy_ (u"࡛ࠧࠩᰀ")
def bstack11l111l1111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11ll1l1_opy_ (u"ࠨ࡜ࠪᰁ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11ll1l1_opy_ (u"ࠩ࡝ࠫᰂ")))).total_seconds() * 1000
def bstack111lll1l11l_opy_(timestamp):
    return bstack111lllll1ll_opy_(timestamp).isoformat() + bstack11ll1l1_opy_ (u"ࠪ࡞ࠬᰃ")
def bstack11l11lll1ll_opy_(bstack11l1l111ll1_opy_):
    date_format = bstack11ll1l1_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩᰄ")
    bstack111lll1l1l1_opy_ = datetime.datetime.strptime(bstack11l1l111ll1_opy_, date_format)
    return bstack111lll1l1l1_opy_.isoformat() + bstack11ll1l1_opy_ (u"ࠬࡠࠧᰅ")
def bstack111lllll111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᰆ")
    else:
        return bstack11ll1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᰇ")
def bstack11l1l111ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11ll1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᰈ")
def bstack11l11l1111l_opy_(val):
    return val.__str__().lower() == bstack11ll1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᰉ")
def bstack111l1llll1_opy_(bstack11l111111l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l111111l1_opy_ as e:
                print(bstack11ll1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᰊ").format(func.__name__, bstack11l111111l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l111l1l_opy_(bstack11l11111lll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11111lll_opy_(cls, *args, **kwargs)
            except bstack11l111111l1_opy_ as e:
                print(bstack11ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᰋ").format(bstack11l11111lll_opy_.__name__, bstack11l111111l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l111l1l_opy_
    else:
        return decorator
def bstack1ll1l1lll1_opy_(bstack1111l1l1l1_opy_):
    if os.getenv(bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᰌ")) is not None:
        return bstack11l1l111ll_opy_(os.getenv(bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᰍ")))
    if bstack11ll1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᰎ") in bstack1111l1l1l1_opy_ and bstack11l11l1111l_opy_(bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᰏ")]):
        return False
    if bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᰐ") in bstack1111l1l1l1_opy_ and bstack11l11l1111l_opy_(bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᰑ")]):
        return False
    return True
def bstack1lll111l_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11111111_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦᰒ"), None)
        return bstack11l11111111_opy_ is None or bstack11l11111111_opy_ == bstack11ll1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᰓ")
    except Exception as e:
        return False
def bstack1ll11l11_opy_(hub_url, CONFIG):
    if bstack11l1ll111_opy_() <= version.parse(bstack11ll1l1_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ᰔ")):
        if hub_url:
            return bstack11ll1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᰕ") + hub_url + bstack11ll1l1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧᰖ")
        return bstack1lll111lll_opy_
    if hub_url:
        return bstack11ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᰗ") + hub_url + bstack11ll1l1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᰘ")
    return bstack1ll11l111l_opy_
def bstack11l11l11lll_opy_():
    return isinstance(os.getenv(bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪᰙ")), str)
def bstack1l1l11l111_opy_(url):
    return urlparse(url).hostname
def bstack1ll111lll_opy_(hostname):
    for bstack11lll1lll_opy_ in bstack1l1l1l11l_opy_:
        regex = re.compile(bstack11lll1lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l111lll_opy_(bstack11l111ll1l1_opy_, file_name, logger):
    bstack11ll1l11_opy_ = os.path.join(os.path.expanduser(bstack11ll1l1_opy_ (u"ࠬࢄࠧᰚ")), bstack11l111ll1l1_opy_)
    try:
        if not os.path.exists(bstack11ll1l11_opy_):
            os.makedirs(bstack11ll1l11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11ll1l1_opy_ (u"࠭ࡾࠨᰛ")), bstack11l111ll1l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11ll1l1_opy_ (u"ࠧࡸࠩᰜ")):
                pass
            with open(file_path, bstack11ll1l1_opy_ (u"ࠣࡹ࠮ࠦᰝ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l11l11lll_opy_.format(str(e)))
def bstack11l11l1l11l_opy_(file_name, key, value, logger):
    file_path = bstack11l1l111lll_opy_(bstack11ll1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᰞ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack111l1l1l_opy_ = json.load(open(file_path, bstack11ll1l1_opy_ (u"ࠪࡶࡧ࠭ᰟ")))
        else:
            bstack111l1l1l_opy_ = {}
        bstack111l1l1l_opy_[key] = value
        with open(file_path, bstack11ll1l1_opy_ (u"ࠦࡼ࠱ࠢᰠ")) as outfile:
            json.dump(bstack111l1l1l_opy_, outfile)
def bstack1111lll11_opy_(file_name, logger):
    file_path = bstack11l1l111lll_opy_(bstack11ll1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᰡ"), file_name, logger)
    bstack111l1l1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11ll1l1_opy_ (u"࠭ࡲࠨᰢ")) as bstack1ll1lll1ll_opy_:
            bstack111l1l1l_opy_ = json.load(bstack1ll1lll1ll_opy_)
    return bstack111l1l1l_opy_
def bstack1llll1l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫᰣ") + file_path + bstack11ll1l1_opy_ (u"ࠨࠢࠪᰤ") + str(e))
def bstack11l1ll111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11ll1l1_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦᰥ")
def bstack1l1ll11l1l_opy_(config):
    if bstack11ll1l1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᰦ") in config:
        del (config[bstack11ll1l1_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᰧ")])
        return False
    if bstack11l1ll111_opy_() < version.parse(bstack11ll1l1_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫᰨ")):
        return False
    if bstack11l1ll111_opy_() >= version.parse(bstack11ll1l1_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬᰩ")):
        return True
    if bstack11ll1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᰪ") in config and config[bstack11ll1l1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᰫ")] is False:
        return False
    else:
        return True
def bstack11l1l11lll_opy_(args_list, bstack111lll1ll1l_opy_):
    index = -1
    for value in bstack111lll1ll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1l1l1l1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1l1l1l1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111lll11l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111lll11l1_opy_ = bstack111lll11l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11ll1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᰬ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᰭ"), exception=exception)
    def bstack11111l1111_opy_(self):
        if self.result != bstack11ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᰮ"):
            return None
        if isinstance(self.exception_type, str) and bstack11ll1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᰯ") in self.exception_type:
            return bstack11ll1l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᰰ")
        return bstack11ll1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᰱ")
    def bstack111llll1111_opy_(self):
        if self.result != bstack11ll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᰲ"):
            return None
        if self.bstack111lll11l1_opy_:
            return self.bstack111lll11l1_opy_
        return bstack111llll1lll_opy_(self.exception)
def bstack111llll1lll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1l11l11l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11111ll1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll11l1l1l_opy_(config, logger):
    try:
        import playwright
        bstack11l111lllll_opy_ = playwright.__file__
        bstack11l11ll1l11_opy_ = os.path.split(bstack11l111lllll_opy_)
        bstack11l111l1ll1_opy_ = bstack11l11ll1l11_opy_[0] + bstack11ll1l1_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬᰳ")
        os.environ[bstack11ll1l1_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ᰴ")] = bstack1l1ll11l_opy_(config)
        with open(bstack11l111l1ll1_opy_, bstack11ll1l1_opy_ (u"ࠫࡷ࠭ᰵ")) as f:
            bstack11l1lllll_opy_ = f.read()
            bstack11l1111ll1l_opy_ = bstack11ll1l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫᰶ")
            bstack11l111l1l11_opy_ = bstack11l1lllll_opy_.find(bstack11l1111ll1l_opy_)
            if bstack11l111l1l11_opy_ == -1:
              process = subprocess.Popen(bstack11ll1l1_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶ᰷ࠥ"), shell=True, cwd=bstack11l11ll1l11_opy_[0])
              process.wait()
              bstack11l1l111111_opy_ = bstack11ll1l1_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧ᰸")
              bstack11l1l11l1l1_opy_ = bstack11ll1l1_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧ᰹")
              bstack11l11ll11ll_opy_ = bstack11l1lllll_opy_.replace(bstack11l1l111111_opy_, bstack11l1l11l1l1_opy_)
              with open(bstack11l111l1ll1_opy_, bstack11ll1l1_opy_ (u"ࠩࡺࠫ᰺")) as f:
                f.write(bstack11l11ll11ll_opy_)
    except Exception as e:
        logger.error(bstack11ll1l1l1_opy_.format(str(e)))
def bstack1ll11ll11_opy_():
  try:
    bstack111lll1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ᰻"))
    bstack11l1l1111l1_opy_ = []
    if os.path.exists(bstack111lll1l111_opy_):
      with open(bstack111lll1l111_opy_) as f:
        bstack11l1l1111l1_opy_ = json.load(f)
      os.remove(bstack111lll1l111_opy_)
    return bstack11l1l1111l1_opy_
  except:
    pass
  return []
def bstack11llllll1_opy_(bstack11lll11ll_opy_):
  try:
    bstack11l1l1111l1_opy_ = []
    bstack111lll1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ᰼"))
    if os.path.exists(bstack111lll1l111_opy_):
      with open(bstack111lll1l111_opy_) as f:
        bstack11l1l1111l1_opy_ = json.load(f)
    bstack11l1l1111l1_opy_.append(bstack11lll11ll_opy_)
    with open(bstack111lll1l111_opy_, bstack11ll1l1_opy_ (u"ࠬࡽࠧ᰽")) as f:
        json.dump(bstack11l1l1111l1_opy_, f)
  except:
    pass
def bstack1llll1l1ll_opy_(logger, bstack11l11l11111_opy_ = False):
  try:
    test_name = os.environ.get(bstack11ll1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ᰾"), bstack11ll1l1_opy_ (u"ࠧࠨ᰿"))
    if test_name == bstack11ll1l1_opy_ (u"ࠨࠩ᱀"):
        test_name = threading.current_thread().__dict__.get(bstack11ll1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨ᱁"), bstack11ll1l1_opy_ (u"ࠪࠫ᱂"))
    bstack11l111l1lll_opy_ = bstack11ll1l1_opy_ (u"ࠫ࠱ࠦࠧ᱃").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11l11111_opy_:
        bstack1l1l111l_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᱄"), bstack11ll1l1_opy_ (u"࠭࠰ࠨ᱅"))
        bstack11111lll_opy_ = {bstack11ll1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᱆"): test_name, bstack11ll1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᱇"): bstack11l111l1lll_opy_, bstack11ll1l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ᱈"): bstack1l1l111l_opy_}
        bstack11l11ll1111_opy_ = []
        bstack111llll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ᱉"))
        if os.path.exists(bstack111llll1l1l_opy_):
            with open(bstack111llll1l1l_opy_) as f:
                bstack11l11ll1111_opy_ = json.load(f)
        bstack11l11ll1111_opy_.append(bstack11111lll_opy_)
        with open(bstack111llll1l1l_opy_, bstack11ll1l1_opy_ (u"ࠫࡼ࠭᱊")) as f:
            json.dump(bstack11l11ll1111_opy_, f)
    else:
        bstack11111lll_opy_ = {bstack11ll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᱋"): test_name, bstack11ll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᱌"): bstack11l111l1lll_opy_, bstack11ll1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᱍ"): str(multiprocessing.current_process().name)}
        if bstack11ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬᱎ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11111lll_opy_)
  except Exception as e:
      logger.warn(bstack11ll1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᱏ").format(e))
def bstack1l111llll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1111lll1_opy_ = []
    bstack11111lll_opy_ = {bstack11ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ᱐"): test_name, bstack11ll1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᱑"): error_message, bstack11ll1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ᱒"): index}
    bstack11l111ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ᱓"))
    if os.path.exists(bstack11l111ll111_opy_):
        with open(bstack11l111ll111_opy_) as f:
            bstack11l1111lll1_opy_ = json.load(f)
    bstack11l1111lll1_opy_.append(bstack11111lll_opy_)
    with open(bstack11l111ll111_opy_, bstack11ll1l1_opy_ (u"ࠧࡸࠩ᱔")) as f:
        json.dump(bstack11l1111lll1_opy_, f)
  except Exception as e:
    logger.warn(bstack11ll1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ᱕").format(e))
def bstack1l1llll1l1_opy_(bstack11l1ll1l_opy_, name, logger):
  try:
    bstack11111lll_opy_ = {bstack11ll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᱖"): name, bstack11ll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᱗"): bstack11l1ll1l_opy_, bstack11ll1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ᱘"): str(threading.current_thread()._name)}
    return bstack11111lll_opy_
  except Exception as e:
    logger.warn(bstack11ll1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ᱙").format(e))
  return
def bstack111lll1l1ll_opy_():
    return platform.system() == bstack11ll1l1_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧᱚ")
def bstack1ll1llll1l_opy_(bstack11l111ll1ll_opy_, config, logger):
    bstack11l111lll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l111ll1ll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨᱛ").format(e))
    return bstack11l111lll11_opy_
def bstack11l1111ll11_opy_(bstack111lll1llll_opy_, bstack111llllllll_opy_):
    bstack11l11llllll_opy_ = version.parse(bstack111lll1llll_opy_)
    bstack11l11ll1l1l_opy_ = version.parse(bstack111llllllll_opy_)
    if bstack11l11llllll_opy_ > bstack11l11ll1l1l_opy_:
        return 1
    elif bstack11l11llllll_opy_ < bstack11l11ll1l1l_opy_:
        return -1
    else:
        return 0
def bstack111ll111ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111lllll1ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11l1l111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1ll1lll1_opy_(options, framework, config, bstack1l1l1ll111_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11ll1l1_opy_ (u"ࠨࡩࡨࡸࠬᱜ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack111111l1l_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᱝ"))
    bstack11l1l1111ll_opy_ = True
    bstack1l1lll111_opy_ = os.environ[bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᱞ")]
    bstack1ll11l1ll1l_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᱟ"), False)
    if bstack1ll11l1ll1l_opy_:
        bstack1lll11l111l_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᱠ"), {})
        bstack1lll11l111l_opy_[bstack11ll1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩᱡ")] = os.getenv(bstack11ll1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᱢ"))
        bstack11ll1l1ll11_opy_ = json.loads(os.getenv(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᱣ"), bstack11ll1l1_opy_ (u"ࠩࡾࢁࠬᱤ"))).get(bstack11ll1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᱥ"))
    if bstack11l11l1111l_opy_(caps.get(bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡗ࠴ࡅࠪᱦ"))) or bstack11l11l1111l_opy_(caps.get(bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᱧ"))):
        bstack11l1l1111ll_opy_ = False
    if bstack1l1ll11l1l_opy_({bstack11ll1l1_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨᱨ"): bstack11l1l1111ll_opy_}):
        bstack111111l1l_opy_ = bstack111111l1l_opy_ or {}
        bstack111111l1l_opy_[bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᱩ")] = bstack11l11l1l111_opy_(framework)
        bstack111111l1l_opy_[bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᱪ")] = bstack1l1lll11111_opy_()
        bstack111111l1l_opy_[bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᱫ")] = bstack1l1lll111_opy_
        bstack111111l1l_opy_[bstack11ll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᱬ")] = bstack1l1l1ll111_opy_
        if bstack1ll11l1ll1l_opy_:
            bstack111111l1l_opy_[bstack11ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᱭ")] = bstack1ll11l1ll1l_opy_
            bstack111111l1l_opy_[bstack11ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᱮ")] = bstack1lll11l111l_opy_
            bstack111111l1l_opy_[bstack11ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᱯ")][bstack11ll1l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᱰ")] = bstack11ll1l1ll11_opy_
        if getattr(options, bstack11ll1l1_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩᱱ"), None):
            options.set_capability(bstack11ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᱲ"), bstack111111l1l_opy_)
        else:
            options[bstack11ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᱳ")] = bstack111111l1l_opy_
    else:
        if getattr(options, bstack11ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᱴ"), None):
            options.set_capability(bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᱵ"), bstack11l11l1l111_opy_(framework))
            options.set_capability(bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᱶ"), bstack1l1lll11111_opy_())
            options.set_capability(bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᱷ"), bstack1l1lll111_opy_)
            options.set_capability(bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᱸ"), bstack1l1l1ll111_opy_)
            if bstack1ll11l1ll1l_opy_:
                options.set_capability(bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᱹ"), bstack1ll11l1ll1l_opy_)
                options.set_capability(bstack11ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᱺ"), bstack1lll11l111l_opy_)
                options.set_capability(bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᱻ"), bstack11ll1l1ll11_opy_)
        else:
            options[bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᱼ")] = bstack11l11l1l111_opy_(framework)
            options[bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᱽ")] = bstack1l1lll11111_opy_()
            options[bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᱾")] = bstack1l1lll111_opy_
            options[bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᱿")] = bstack1l1l1ll111_opy_
            if bstack1ll11l1ll1l_opy_:
                options[bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᲀ")] = bstack1ll11l1ll1l_opy_
                options[bstack11ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲁ")] = bstack1lll11l111l_opy_
                options[bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᲂ")][bstack11ll1l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᲃ")] = bstack11ll1l1ll11_opy_
    return options
def bstack11l11l1l1l1_opy_(bstack11l1111l1l1_opy_, framework):
    bstack1l1l1ll111_opy_ = bstack1111ll111_opy_.get_property(bstack11ll1l1_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣᲄ"))
    if bstack11l1111l1l1_opy_ and len(bstack11l1111l1l1_opy_.split(bstack11ll1l1_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᲅ"))) > 1:
        ws_url = bstack11l1111l1l1_opy_.split(bstack11ll1l1_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᲆ"))[0]
        if bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᲇ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l11111ll1_opy_ = json.loads(urllib.parse.unquote(bstack11l1111l1l1_opy_.split(bstack11ll1l1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᲈ"))[1]))
            bstack11l11111ll1_opy_ = bstack11l11111ll1_opy_ or {}
            bstack1l1lll111_opy_ = os.environ[bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᲉ")]
            bstack11l11111ll1_opy_[bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᲊ")] = str(framework) + str(__version__)
            bstack11l11111ll1_opy_[bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᲋")] = bstack1l1lll11111_opy_()
            bstack11l11111ll1_opy_[bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᲌")] = bstack1l1lll111_opy_
            bstack11l11111ll1_opy_[bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᲍")] = bstack1l1l1ll111_opy_
            bstack11l1111l1l1_opy_ = bstack11l1111l1l1_opy_.split(bstack11ll1l1_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᲎"))[0] + bstack11ll1l1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ᲏") + urllib.parse.quote(json.dumps(bstack11l11111ll1_opy_))
    return bstack11l1111l1l1_opy_
def bstack1lllll1111_opy_():
    global bstack1l11ll1l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l11ll1l_opy_ = BrowserType.connect
    return bstack1l11ll1l_opy_
def bstack11l1lll111_opy_(framework_name):
    global bstack11l11lll11_opy_
    bstack11l11lll11_opy_ = framework_name
    return framework_name
def bstack1l11lll1l_opy_(self, *args, **kwargs):
    global bstack1l11ll1l_opy_
    try:
        global bstack11l11lll11_opy_
        if bstack11ll1l1_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᲐ") in kwargs:
            kwargs[bstack11ll1l1_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᲑ")] = bstack11l11l1l1l1_opy_(
                kwargs.get(bstack11ll1l1_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᲒ"), None),
                bstack11l11lll11_opy_
            )
    except Exception as e:
        logger.error(bstack11ll1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢᲓ").format(str(e)))
    return bstack1l11ll1l_opy_(self, *args, **kwargs)
def bstack11l111111ll_opy_(bstack111llll1ll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lll11l11l_opy_(bstack111llll1ll1_opy_, bstack11ll1l1_opy_ (u"ࠣࠤᲔ"))
        if proxies and proxies.get(bstack11ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᲕ")):
            parsed_url = urlparse(proxies.get(bstack11ll1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᲖ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11ll1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᲗ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11ll1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᲘ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11ll1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᲙ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11ll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᲚ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll111l111_opy_(bstack111llll1ll1_opy_):
    bstack11l11l11l1l_opy_ = {
        bstack11l1lll111l_opy_[bstack11l1l11l1ll_opy_]: bstack111llll1ll1_opy_[bstack11l1l11l1ll_opy_]
        for bstack11l1l11l1ll_opy_ in bstack111llll1ll1_opy_
        if bstack11l1l11l1ll_opy_ in bstack11l1lll111l_opy_
    }
    bstack11l11l11l1l_opy_[bstack11ll1l1_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣᲛ")] = bstack11l111111ll_opy_(bstack111llll1ll1_opy_, bstack1111ll111_opy_.get_property(bstack11ll1l1_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᲜ")))
    bstack11l11l111l1_opy_ = [element.lower() for element in bstack11ll11111l1_opy_]
    bstack11l11llll1l_opy_(bstack11l11l11l1l_opy_, bstack11l11l111l1_opy_)
    return bstack11l11l11l1l_opy_
def bstack11l11llll1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11ll1l1_opy_ (u"ࠥ࠮࠯࠰ࠪࠣᲝ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l11llll1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l11llll1l_opy_(item, keys)
def bstack1l1ll1l11l1_opy_():
    bstack11l11l1lll1_opy_ = [os.environ.get(bstack11ll1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡎࡒࡅࡔࡡࡇࡍࡗࠨᲞ")), os.path.join(os.path.expanduser(bstack11ll1l1_opy_ (u"ࠧࢄࠢᲟ")), bstack11ll1l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Რ")), os.path.join(bstack11ll1l1_opy_ (u"ࠧ࠰ࡶࡰࡴࠬᲡ"), bstack11ll1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᲢ"))]
    for path in bstack11l11l1lll1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11ll1l1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᲣ") + str(path) + bstack11ll1l1_opy_ (u"ࠥࠫࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠨᲤ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11ll1l1_opy_ (u"ࠦࡌ࡯ࡶࡪࡰࡪࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠢࡩࡳࡷࠦࠧࠣᲥ") + str(path) + bstack11ll1l1_opy_ (u"ࠧ࠭ࠢᲦ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11ll1l1_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨᲧ") + str(path) + bstack11ll1l1_opy_ (u"ࠢࠨࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡬ࡦࡹࠠࡵࡪࡨࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶ࠲ࠧᲨ"))
            else:
                logger.debug(bstack11ll1l1_opy_ (u"ࠣࡅࡵࡩࡦࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥࠡࠩࠥᲩ") + str(path) + bstack11ll1l1_opy_ (u"ࠤࠪࠤࡼ࡯ࡴࡩࠢࡺࡶ࡮ࡺࡥࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲ࠳ࠨᲪ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11ll1l1_opy_ (u"ࠥࡓࡵ࡫ࡲࡢࡶ࡬ࡳࡳࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥࠢࡩࡳࡷࠦࠧࠣᲫ") + str(path) + bstack11ll1l1_opy_ (u"ࠦࠬ࠴ࠢᲬ"))
            return path
        except Exception as e:
            logger.debug(bstack11ll1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡻࡰࠡࡨ࡬ࡰࡪࠦࠧࡼࡲࡤࡸ࡭ࢃࠧ࠻ࠢࠥᲭ") + str(e) + bstack11ll1l1_opy_ (u"ࠨࠢᲮ"))
    logger.debug(bstack11ll1l1_opy_ (u"ࠢࡂ࡮࡯ࠤࡵࡧࡴࡩࡵࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠦᲯ"))
    return None
@measure(event_name=EVENTS.bstack11l1ll11ll1_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
def bstack1lll1ll11ll_opy_(binary_path, bstack1lll1l1111l_opy_, bs_config):
    logger.debug(bstack11ll1l1_opy_ (u"ࠣࡅࡸࡶࡷ࡫࡮ࡵࠢࡆࡐࡎࠦࡐࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦ࠽ࠤࢀࢃࠢᲰ").format(binary_path))
    bstack111lll1lll1_opy_ = bstack11ll1l1_opy_ (u"ࠩࠪᲱ")
    bstack11l1111l111_opy_ = {
        bstack11ll1l1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲲ"): __version__,
        bstack11ll1l1_opy_ (u"ࠦࡴࡹࠢᲳ"): platform.system(),
        bstack11ll1l1_opy_ (u"ࠧࡵࡳࡠࡣࡵࡧ࡭ࠨᲴ"): platform.machine(),
        bstack11ll1l1_opy_ (u"ࠨࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠦᲵ"): bstack11ll1l1_opy_ (u"ࠧ࠱ࠩᲶ"),
        bstack11ll1l1_opy_ (u"ࠣࡵࡧ࡯ࡤࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠢᲷ"): bstack11ll1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᲸ")
    }
    bstack111llllll11_opy_(bstack11l1111l111_opy_)
    try:
        if binary_path:
            bstack11l1111l111_opy_[bstack11ll1l1_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲹ")] = subprocess.check_output([binary_path, bstack11ll1l1_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᲺ")]).strip().decode(bstack11ll1l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᲻"))
        response = requests.request(
            bstack11ll1l1_opy_ (u"࠭ࡇࡆࡖࠪ᲼"),
            url=bstack111l11ll_opy_(bstack11ll1111l11_opy_),
            headers=None,
            auth=(bs_config[bstack11ll1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᲽ")], bs_config[bstack11ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᲾ")]),
            json=None,
            params=bstack11l1111l111_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11ll1l1_opy_ (u"ࠩࡸࡶࡱ࠭Ჿ") in data.keys() and bstack11ll1l1_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧࡣࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᳀") in data.keys():
            logger.debug(bstack11ll1l1_opy_ (u"ࠦࡓ࡫ࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡨࡩ࡯ࡣࡵࡽ࠱ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧ᳁").format(bstack11l1111l111_opy_[bstack11ll1l1_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ᳂")]))
            if bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ᳃") in os.environ:
                logger.debug(bstack11ll1l1_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡦࡹࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥ᳄"))
                data[bstack11ll1l1_opy_ (u"ࠨࡷࡵࡰࠬ᳅")] = os.environ[bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬ᳆")]
            bstack11l11llll11_opy_ = bstack11l11lll111_opy_(data[bstack11ll1l1_opy_ (u"ࠪࡹࡷࡲࠧ᳇")], bstack1lll1l1111l_opy_)
            bstack111lll1lll1_opy_ = os.path.join(bstack1lll1l1111l_opy_, bstack11l11llll11_opy_)
            os.chmod(bstack111lll1lll1_opy_, 0o777) # bstack111llll11l1_opy_ permission
            return bstack111lll1lll1_opy_
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦ᳈").format(e))
    return binary_path
def bstack111llllll11_opy_(bstack11l1111l111_opy_):
    try:
        if bstack11ll1l1_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫ᳉") not in bstack11l1111l111_opy_[bstack11ll1l1_opy_ (u"࠭࡯ࡴࠩ᳊")].lower():
            return
        if os.path.exists(bstack11ll1l1_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ᳋")):
            with open(bstack11ll1l1_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ᳌"), bstack11ll1l1_opy_ (u"ࠤࡵࠦ᳍")) as f:
                bstack11l11lll1l1_opy_ = {}
                for line in f:
                    if bstack11ll1l1_opy_ (u"ࠥࡁࠧ᳎") in line:
                        key, value = line.rstrip().split(bstack11ll1l1_opy_ (u"ࠦࡂࠨ᳏"), 1)
                        bstack11l11lll1l1_opy_[key] = value.strip(bstack11ll1l1_opy_ (u"ࠬࠨ࡜ࠨࠩ᳐"))
                bstack11l1111l111_opy_[bstack11ll1l1_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭᳑")] = bstack11l11lll1l1_opy_.get(bstack11ll1l1_opy_ (u"ࠢࡊࡆࠥ᳒"), bstack11ll1l1_opy_ (u"ࠣࠤ᳓"))
        elif os.path.exists(bstack11ll1l1_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥ᳔ࠣ")):
            bstack11l1111l111_opy_[bstack11ll1l1_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱ᳕ࠪ")] = bstack11ll1l1_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨ᳖ࠫ")
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾ᳗ࠢ") + e)
@measure(event_name=EVENTS.bstack11l1ll11l11_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
def bstack11l11lll111_opy_(bstack11l11l111ll_opy_, bstack11l1111llll_opy_):
    logger.debug(bstack11ll1l1_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀ᳘ࠠࠣ") + str(bstack11l11l111ll_opy_) + bstack11ll1l1_opy_ (u"᳙ࠢࠣ"))
    zip_path = os.path.join(bstack11l1111llll_opy_, bstack11ll1l1_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶࠢ᳚"))
    bstack11l11llll11_opy_ = bstack11ll1l1_opy_ (u"ࠩࠪ᳛")
    with requests.get(bstack11l11l111ll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11ll1l1_opy_ (u"ࠥࡻࡧࠨ᳜")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11ll1l1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨ᳝"))
    with zipfile.ZipFile(zip_path, bstack11ll1l1_opy_ (u"ࠬࡸ᳞ࠧ")) as zip_ref:
        bstack11l11l11l11_opy_ = zip_ref.namelist()
        if len(bstack11l11l11l11_opy_) > 0:
            bstack11l11llll11_opy_ = bstack11l11l11l11_opy_[0] # bstack11l11l1llll_opy_ bstack11l1ll11l1l_opy_ will be bstack11l111llll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1111llll_opy_)
        logger.debug(bstack11ll1l1_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱ᳟ࠣࠫࠧ") + str(bstack11l1111llll_opy_) + bstack11ll1l1_opy_ (u"ࠢࠨࠤ᳠"))
    os.remove(zip_path)
    return bstack11l11llll11_opy_
def get_cli_dir():
    bstack11l11l1ll1l_opy_ = bstack1l1ll1l11l1_opy_()
    if bstack11l11l1ll1l_opy_:
        bstack1lll1l1111l_opy_ = os.path.join(bstack11l11l1ll1l_opy_, bstack11ll1l1_opy_ (u"ࠣࡥ࡯࡭ࠧ᳡"))
        if not os.path.exists(bstack1lll1l1111l_opy_):
            os.makedirs(bstack1lll1l1111l_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1l1111l_opy_
    else:
        raise FileNotFoundError(bstack11ll1l1_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲᳢ࠧ"))
def bstack1ll1ll1lll1_opy_(bstack1lll1l1111l_opy_):
    bstack11ll1l1_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨ᳣ࠢ")
    bstack11l11l1ll11_opy_ = [
        os.path.join(bstack1lll1l1111l_opy_, f)
        for f in os.listdir(bstack1lll1l1111l_opy_)
        if os.path.isfile(os.path.join(bstack1lll1l1111l_opy_, f)) and f.startswith(bstack11ll1l1_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱᳤ࠧ"))
    ]
    if len(bstack11l11l1ll11_opy_) > 0:
        return max(bstack11l11l1ll11_opy_, key=os.path.getmtime) # get bstack11l11lllll1_opy_ binary
    return bstack11ll1l1_opy_ (u"ࠧࠨ᳥")
def bstack11ll1l1lll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1l11111l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l11111l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l111lll1_opy_(data, keys, default=None):
    bstack11ll1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡢࡨࡨࡰࡾࠦࡧࡦࡶࠣࡥࠥࡴࡥࡴࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡣࡷࡥ࠿ࠦࡔࡩࡧࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡶࡲࠤࡹࡸࡡࡷࡧࡵࡷࡪ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡰ࡫ࡹࡴ࠼ࠣࡅࠥࡲࡩࡴࡶࠣࡳ࡫ࠦ࡫ࡦࡻࡶ࠳࡮ࡴࡤࡪࡥࡨࡷࠥࡸࡥࡱࡴࡨࡷࡪࡴࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩ࡫ࡦࡢࡷ࡯ࡸ࠿ࠦࡖࡢ࡮ࡸࡩࠥࡺ࡯ࠡࡴࡨࡸࡺࡸ࡮ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡲࡦࡶࡸࡶࡳࡀࠠࡕࡪࡨࠤࡻࡧ࡬ࡶࡧࠣࡥࡹࠦࡴࡩࡧࠣࡲࡪࡹࡴࡦࡦࠣࡴࡦࡺࡨ࠭ࠢࡲࡶࠥࡪࡥࡧࡣࡸࡰࡹࠦࡩࡧࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ᳦")
    if not data:
        return default
    current = data
    try:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError):
        return default