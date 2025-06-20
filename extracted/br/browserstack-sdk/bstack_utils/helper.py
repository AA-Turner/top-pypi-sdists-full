# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
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
from bstack_utils.constants import (bstack11ll1l111ll_opy_, bstack11ll1l111l_opy_, bstack11l1l11l11_opy_, bstack11llll1lll_opy_,
                                    bstack11l1lllll11_opy_, bstack11l1lllll1l_opy_, bstack11l1ll1llll_opy_, bstack11ll111111l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1llll1ll_opy_, bstack11ll1111l_opy_
from bstack_utils.proxy import bstack1l1ll111_opy_, bstack1l111111l1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1111l1ll1_opy_
from bstack_utils.bstack11l1111ll1_opy_ import bstack11ll11l1ll_opy_
from browserstack_sdk._version import __version__
bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
logger = bstack1111l1ll1_opy_.get_logger(__name__, bstack1111l1ll1_opy_.bstack1lll1lll1ll_opy_())
def bstack11ll1l1ll1l_opy_(config):
    return config[bstack11ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᪐")]
def bstack11ll1ll11ll_opy_(config):
    return config[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᪑")]
def bstack11lll11111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l11llll_opy_(obj):
    values = []
    bstack11l1l11l11l_opy_ = re.compile(bstack11ll11_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤ᪒"), re.I)
    for key in obj.keys():
        if bstack11l1l11l11l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11l1lll1_opy_(config):
    tags = []
    tags.extend(bstack11l1l11llll_opy_(os.environ))
    tags.extend(bstack11l1l11llll_opy_(config))
    return tags
def bstack11l11l1111l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1111l1ll_opy_(bstack111lllll11l_opy_):
    if not bstack111lllll11l_opy_:
        return bstack11ll11_opy_ (u"࠭ࠧ᪓")
    return bstack11ll11_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣ᪔").format(bstack111lllll11l_opy_.name, bstack111lllll11l_opy_.email)
def bstack11ll1ll1111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1l11ll1l_opy_ = repo.common_dir
        info = {
            bstack11ll11_opy_ (u"ࠣࡵ࡫ࡥࠧ᪕"): repo.head.commit.hexsha,
            bstack11ll11_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧ᪖"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11ll11_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥ᪗"): repo.active_branch.name,
            bstack11ll11_opy_ (u"ࠦࡹࡧࡧࠣ᪘"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11ll11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣ᪙"): bstack11l1111l1ll_opy_(repo.head.commit.committer),
            bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢ᪚"): repo.head.commit.committed_datetime.isoformat(),
            bstack11ll11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢ᪛"): bstack11l1111l1ll_opy_(repo.head.commit.author),
            bstack11ll11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨ᪜"): repo.head.commit.authored_datetime.isoformat(),
            bstack11ll11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥ᪝"): repo.head.commit.message,
            bstack11ll11_opy_ (u"ࠥࡶࡴࡵࡴࠣ᪞"): repo.git.rev_parse(bstack11ll11_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨ᪟")),
            bstack11ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨ᪠"): bstack11l1l11ll1l_opy_,
            bstack11ll11_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤ᪡"): subprocess.check_output([bstack11ll11_opy_ (u"ࠢࡨ࡫ࡷࠦ᪢"), bstack11ll11_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦ᪣"), bstack11ll11_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧ᪤")]).strip().decode(
                bstack11ll11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᪥")),
            bstack11ll11_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ᪦"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11ll11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᪧ"): repo.git.rev_list(
                bstack11ll11_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨ᪨").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l111ll111_opy_ = []
        for remote in remotes:
            bstack11l11l1ll11_opy_ = {
                bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪩"): remote.name,
                bstack11ll11_opy_ (u"ࠣࡷࡵࡰࠧ᪪"): remote.url,
            }
            bstack11l111ll111_opy_.append(bstack11l11l1ll11_opy_)
        bstack11l11l111l1_opy_ = {
            bstack11ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪫"): bstack11ll11_opy_ (u"ࠥ࡫࡮ࡺࠢ᪬"),
            **info,
            bstack11ll11_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧ᪭"): bstack11l111ll111_opy_
        }
        bstack11l11l111l1_opy_ = bstack11l11llllll_opy_(bstack11l11l111l1_opy_)
        return bstack11l11l111l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ᪮").format(err))
        return {}
def bstack11l11llllll_opy_(bstack11l11l111l1_opy_):
    bstack11l111ll11l_opy_ = bstack11l11l1l11l_opy_(bstack11l11l111l1_opy_)
    if bstack11l111ll11l_opy_ and bstack11l111ll11l_opy_ > bstack11l1lllll11_opy_:
        bstack11l111l1lll_opy_ = bstack11l111ll11l_opy_ - bstack11l1lllll11_opy_
        bstack111llllll11_opy_ = bstack11l11lllll1_opy_(bstack11l11l111l1_opy_[bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᪯")], bstack11l111l1lll_opy_)
        bstack11l11l111l1_opy_[bstack11ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᪰")] = bstack111llllll11_opy_
        logger.info(bstack11ll11_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥ᪱")
                    .format(bstack11l11l1l11l_opy_(bstack11l11l111l1_opy_) / 1024))
    return bstack11l11l111l1_opy_
def bstack11l11l1l11l_opy_(bstack1l1l11l1ll_opy_):
    try:
        if bstack1l1l11l1ll_opy_:
            bstack11l111l1ll1_opy_ = json.dumps(bstack1l1l11l1ll_opy_)
            bstack11l1l11111l_opy_ = sys.getsizeof(bstack11l111l1ll1_opy_)
            return bstack11l1l11111l_opy_
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤ᪲").format(e))
    return -1
def bstack11l11lllll1_opy_(field, bstack111llll1111_opy_):
    try:
        bstack111lllll1l1_opy_ = len(bytes(bstack11l1lllll1l_opy_, bstack11ll11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᪳")))
        bstack11l11ll1lll_opy_ = bytes(field, bstack11ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᪴"))
        bstack11l11lll1l1_opy_ = len(bstack11l11ll1lll_opy_)
        bstack11l11ll1ll1_opy_ = ceil(bstack11l11lll1l1_opy_ - bstack111llll1111_opy_ - bstack111lllll1l1_opy_)
        if bstack11l11ll1ll1_opy_ > 0:
            bstack11l11l11ll1_opy_ = bstack11l11ll1lll_opy_[:bstack11l11ll1ll1_opy_].decode(bstack11ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻᪵ࠫ"), errors=bstack11ll11_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ᪶࠭")) + bstack11l1lllll1l_opy_
            return bstack11l11l11ll1_opy_
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁ᪷ࠧ").format(e))
    return field
def bstack11l1l1l1l_opy_():
    env = os.environ
    if (bstack11ll11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ᪸") in env and len(env[bstack11ll11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒ᪹ࠢ")]) > 0) or (
            bstack11ll11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᪺") in env and len(env[bstack11ll11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ᪻")]) > 0):
        return {
            bstack11ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪼"): bstack11ll11_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹ᪽ࠢ"),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪾"): env.get(bstack11ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏᪿࠦ")),
            bstack11ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨᫀࠦ"): env.get(bstack11ll11_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᫁")),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫂"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕ᫃ࠦ"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠨࡃࡊࠤ᫄")) == bstack11ll11_opy_ (u"ࠢࡵࡴࡸࡩࠧ᫅") and bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ᫆"))):
        return {
            bstack11ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫇"): bstack11ll11_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧ᫈"),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᫉"): env.get(bstack11ll11_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌ᫊ࠣ")),
            bstack11ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᫋"): env.get(bstack11ll11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦᫌ")),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᫍ"): env.get(bstack11ll11_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧᫎ"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠥࡇࡎࠨ᫏")) == bstack11ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤ᫐") and bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧ᫑"))):
        return {
            bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᫒"): bstack11ll11_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥ᫓"),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᫔"): env.get(bstack11ll11_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤ᫕")),
            bstack11ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫖"): env.get(bstack11ll11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᫗")),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫘"): env.get(bstack11ll11_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᫙"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡄࡋࠥ᫚")) == bstack11ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ᫛") and env.get(bstack11ll11_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥ᫜")) == bstack11ll11_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧ᫝"):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫞"): bstack11ll11_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢ᫟"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫠"): None,
            bstack11ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᫡"): None,
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᫢"): None
        }
    if env.get(bstack11ll11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧ᫣")) and env.get(bstack11ll11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ᫤")):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫥"): bstack11ll11_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣ᫦"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫧"): env.get(bstack11ll11_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧ᫨")),
            bstack11ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫩"): None,
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᫪"): env.get(bstack11ll11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᫫"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠦࡈࡏࠢ᫬")) == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ᫭") and bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧ᫮"))):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᫯"): bstack11ll11_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢ᫰"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᫱"): env.get(bstack11ll11_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨ᫲")),
            bstack11ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫳"): None,
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫴"): env.get(bstack11ll11_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᫵"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡄࡋࠥ᫶")) == bstack11ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ᫷") and bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧ᫸"))):
        return {
            bstack11ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫹"): bstack11ll11_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢ᫺"),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᫻"): env.get(bstack11ll11_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧ᫼")),
            bstack11ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᫽"): env.get(bstack11ll11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᫾")),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᫿"): env.get(bstack11ll11_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨᬀ"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠦࡈࡏࠢᬁ")) == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥᬂ") and bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤᬃ"))):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬄ"): bstack11ll11_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣᬅ"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᬆ"): env.get(bstack11ll11_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢᬇ")),
            bstack11ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᬈ"): env.get(bstack11ll11_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᬉ")),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᬊ"): env.get(bstack11ll11_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥᬋ"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠣࡅࡌࠦᬌ")) == bstack11ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᬍ") and bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨᬎ"))):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᬏ"): bstack11ll11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣᬐ"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᬑ"): env.get(bstack11ll11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᬒ")),
            bstack11ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᬓ"): env.get(bstack11ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦᬔ")) or env.get(bstack11ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᬕ")),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᬖ"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᬗ"))
        }
    if bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᬘ"))):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬙ"): bstack11ll11_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣᬚ"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᬛ"): bstack11ll11_opy_ (u"ࠥࡿࢂࢁࡽࠣᬜ").format(env.get(bstack11ll11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᬝ")), env.get(bstack11ll11_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬᬞ"))),
            bstack11ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᬟ"): env.get(bstack11ll11_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨᬠ")),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᬡ"): env.get(bstack11ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᬢ"))
        }
    if bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧᬣ"))):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᬤ"): bstack11ll11_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢᬥ"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᬦ"): bstack11ll11_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨᬧ").format(env.get(bstack11ll11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧᬨ")), env.get(bstack11ll11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪᬩ")), env.get(bstack11ll11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫᬪ")), env.get(bstack11ll11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨᬫ"))),
            bstack11ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬬ"): env.get(bstack11ll11_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᬭ")),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬮ"): env.get(bstack11ll11_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᬯ"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥᬰ")) and env.get(bstack11ll11_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᬱ")):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᬲ"): bstack11ll11_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢᬳ"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᬴"): bstack11ll11_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥᬵ").format(env.get(bstack11ll11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᬶ")), env.get(bstack11ll11_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧᬷ")), env.get(bstack11ll11_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪᬸ"))),
            bstack11ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᬹ"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᬺ")),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᬻ"): env.get(bstack11ll11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᬼ"))
        }
    if any([env.get(bstack11ll11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᬽ")), env.get(bstack11ll11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᬾ")), env.get(bstack11ll11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᬿ"))]):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᭀ"): bstack11ll11_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧᭁ"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᭂ"): env.get(bstack11ll11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᭃ")),
            bstack11ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧ᭄ࠥ"): env.get(bstack11ll11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᭅ")),
            bstack11ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᭆ"): env.get(bstack11ll11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᭇ"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᭈ")):
        return {
            bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᭉ"): bstack11ll11_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢᭊ"),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᭋ"): env.get(bstack11ll11_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦᭌ")),
            bstack11ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭍"): env.get(bstack11ll11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ᭎")),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᭏"): env.get(bstack11ll11_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ᭐"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣ᭑")) or env.get(bstack11ll11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ᭒")):
        return {
            bstack11ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᭓"): bstack11ll11_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦ᭔"),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᭕"): env.get(bstack11ll11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᭖")),
            bstack11ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᭗"): bstack11ll11_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢ᭘") if env.get(bstack11ll11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ᭙")) else None,
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᭚"): env.get(bstack11ll11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣ᭛"))
        }
    if any([env.get(bstack11ll11_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤ᭜")), env.get(bstack11ll11_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᭝")), env.get(bstack11ll11_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᭞"))]):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭟"): bstack11ll11_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢ᭠"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭡"): None,
            bstack11ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭢"): env.get(bstack11ll11_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣ᭣")),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᭤"): env.get(bstack11ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ᭥"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥ᭦")):
        return {
            bstack11ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭧"): bstack11ll11_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧ᭨"),
            bstack11ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᭩"): env.get(bstack11ll11_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᭪")),
            bstack11ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᭫"): bstack11ll11_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃ᭬ࠢ").format(env.get(bstack11ll11_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ᭭"))) if env.get(bstack11ll11_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦ᭮")) else None,
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᭯"): env.get(bstack11ll11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᭰"))
        }
    if bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧ᭱"))):
        return {
            bstack11ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᭲"): bstack11ll11_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢ᭳"),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᭴"): env.get(bstack11ll11_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧ᭵")),
            bstack11ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᭶"): env.get(bstack11ll11_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨ᭷")),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᭸"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᭹"))
        }
    if bstack1l111ll1l_opy_(env.get(bstack11ll11_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ᭺"))):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭻"): bstack11ll11_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤ᭼"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭽"): bstack11ll11_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦ᭾").format(env.get(bstack11ll11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨ᭿")), env.get(bstack11ll11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩᮀ")), env.get(bstack11ll11_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ᮁ"))),
            bstack11ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮂ"): env.get(bstack11ll11_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥᮃ")),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᮄ"): env.get(bstack11ll11_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥᮅ"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠦࡈࡏࠢᮆ")) == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥᮇ") and env.get(bstack11ll11_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨᮈ")) == bstack11ll11_opy_ (u"ࠢ࠲ࠤᮉ"):
        return {
            bstack11ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᮊ"): bstack11ll11_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤᮋ"),
            bstack11ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮌ"): bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢᮍ").format(env.get(bstack11ll11_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩᮎ"))),
            bstack11ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᮏ"): None,
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮐ"): None,
        }
    if env.get(bstack11ll11_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᮑ")):
        return {
            bstack11ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮒ"): bstack11ll11_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧᮓ"),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᮔ"): None,
            bstack11ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᮕ"): env.get(bstack11ll11_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢᮖ")),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮗ"): env.get(bstack11ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᮘ"))
        }
    if any([env.get(bstack11ll11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧᮙ")), env.get(bstack11ll11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥᮚ")), env.get(bstack11ll11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤᮛ")), env.get(bstack11ll11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨᮜ"))]):
        return {
            bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᮝ"): bstack11ll11_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥᮞ"),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮟ"): None,
            bstack11ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᮠ"): env.get(bstack11ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᮡ")) or None,
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᮢ"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᮣ"), 0)
        }
    if env.get(bstack11ll11_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᮤ")):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮥ"): bstack11ll11_opy_ (u"ࠣࡉࡲࡇࡉࠨᮦ"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮧ"): None,
            bstack11ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮨ"): env.get(bstack11ll11_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᮩ")),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᮪ࠦ"): env.get(bstack11ll11_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖ᮫ࠧ"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᮬ")):
        return {
            bstack11ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᮭ"): bstack11ll11_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧᮮ"),
            bstack11ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮯ"): env.get(bstack11ll11_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᮰")),
            bstack11ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᮱"): env.get(bstack11ll11_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ᮲")),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᮳"): env.get(bstack11ll11_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᮴"))
        }
    return {bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᮵"): None}
def get_host_info():
    return {
        bstack11ll11_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ᮶"): platform.node(),
        bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ᮷"): platform.system(),
        bstack11ll11_opy_ (u"ࠧࡺࡹࡱࡧࠥ᮸"): platform.machine(),
        bstack11ll11_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ᮹"): platform.version(),
        bstack11ll11_opy_ (u"ࠢࡢࡴࡦ࡬ࠧᮺ"): platform.architecture()[0]
    }
def bstack1111llll1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111llll11l1_opy_():
    if bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩᮻ")):
        return bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᮼ")
    return bstack11ll11_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩᮽ")
def bstack111llll1lll_opy_(driver):
    info = {
        bstack11ll11_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᮾ"): driver.capabilities,
        bstack11ll11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩᮿ"): driver.session_id,
        bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᯀ"): driver.capabilities.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᯁ"), None),
        bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᯂ"): driver.capabilities.get(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᯃ"), None),
        bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬᯄ"): driver.capabilities.get(bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᯅ"), None),
        bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᯆ"):driver.capabilities.get(bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᯇ"), None),
    }
    if bstack111llll11l1_opy_() == bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᯈ"):
        if bstack1lll1l111l_opy_():
            info[bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᯉ")] = bstack11ll11_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᯊ")
        elif driver.capabilities.get(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᯋ"), {}).get(bstack11ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᯌ"), False):
            info[bstack11ll11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᯍ")] = bstack11ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᯎ")
        else:
            info[bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᯏ")] = bstack11ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᯐ")
    return info
def bstack1lll1l111l_opy_():
    if bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᯑ")):
        return True
    if bstack1l111ll1l_opy_(os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫᯒ"), None)):
        return True
    return False
def bstack1llll1ll_opy_(bstack11l1111l11l_opy_, url, data, config):
    headers = config.get(bstack11ll11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᯓ"), None)
    proxies = bstack1l1ll111_opy_(config, url)
    auth = config.get(bstack11ll11_opy_ (u"ࠬࡧࡵࡵࡪࠪᯔ"), None)
    response = requests.request(
            bstack11l1111l11l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1l1l11ll_opy_(bstack11l1111111_opy_, size):
    bstack1l1lll1l1l_opy_ = []
    while len(bstack11l1111111_opy_) > size:
        bstack1l111l111_opy_ = bstack11l1111111_opy_[:size]
        bstack1l1lll1l1l_opy_.append(bstack1l111l111_opy_)
        bstack11l1111111_opy_ = bstack11l1111111_opy_[size:]
    bstack1l1lll1l1l_opy_.append(bstack11l1111111_opy_)
    return bstack1l1lll1l1l_opy_
def bstack11l11ll11l1_opy_(message, bstack11l111111l1_opy_=False):
    os.write(1, bytes(message, bstack11ll11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᯕ")))
    os.write(1, bytes(bstack11ll11_opy_ (u"ࠧ࡝ࡰࠪᯖ"), bstack11ll11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᯗ")))
    if bstack11l111111l1_opy_:
        with open(bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨᯘ") + os.environ[bstack11ll11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᯙ")] + bstack11ll11_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩᯚ"), bstack11ll11_opy_ (u"ࠬࡧࠧᯛ")) as f:
            f.write(message + bstack11ll11_opy_ (u"࠭࡜࡯ࠩᯜ"))
def bstack1l1ll111ll1_opy_():
    return os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᯝ")].lower() == bstack11ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᯞ")
def bstack1l11l11ll_opy_():
    return bstack1111llll11_opy_().replace(tzinfo=None).isoformat() + bstack11ll11_opy_ (u"ࠩ࡝ࠫᯟ")
def bstack11l1l11l1ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11ll11_opy_ (u"ࠪ࡞ࠬᯠ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11ll11_opy_ (u"ࠫ࡟࠭ᯡ")))).total_seconds() * 1000
def bstack11l1l11ll11_opy_(timestamp):
    return bstack11l1111llll_opy_(timestamp).isoformat() + bstack11ll11_opy_ (u"ࠬࡠࠧᯢ")
def bstack11l111ll1ll_opy_(bstack11l111ll1l1_opy_):
    date_format = bstack11ll11_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫᯣ")
    bstack11l1l1l1111_opy_ = datetime.datetime.strptime(bstack11l111ll1l1_opy_, date_format)
    return bstack11l1l1l1111_opy_.isoformat() + bstack11ll11_opy_ (u"࡛ࠧࠩᯤ")
def bstack11l11lll1ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᯥ")
    else:
        return bstack11ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥ᯦ࠩ")
def bstack1l111ll1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨᯧ")
def bstack11l1111ll11_opy_(val):
    return val.__str__().lower() == bstack11ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᯨ")
def bstack111l1lll11_opy_(bstack11l11lll111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11lll111_opy_ as e:
                print(bstack11ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᯩ").format(func.__name__, bstack11l11lll111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111llll11ll_opy_(bstack11l1l111l1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l111l1l_opy_(cls, *args, **kwargs)
            except bstack11l11lll111_opy_ as e:
                print(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᯪ").format(bstack11l1l111l1l_opy_.__name__, bstack11l11lll111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111llll11ll_opy_
    else:
        return decorator
def bstack1l111lll1l_opy_(bstack1111ll1l11_opy_):
    if os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᯫ")) is not None:
        return bstack1l111ll1l_opy_(os.getenv(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᯬ")))
    if bstack11ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᯭ") in bstack1111ll1l11_opy_ and bstack11l1111ll11_opy_(bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᯮ")]):
        return False
    if bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᯯ") in bstack1111ll1l11_opy_ and bstack11l1111ll11_opy_(bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᯰ")]):
        return False
    return True
def bstack111ll11l_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l111lll11_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨᯱ"), None)
        return bstack11l111lll11_opy_ is None or bstack11l111lll11_opy_ == bstack11ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧ᯲ࠦ")
    except Exception as e:
        return False
def bstack11ll11l111_opy_(hub_url, CONFIG):
    if bstack1lll1ll1_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ᯳")):
        if hub_url:
            return bstack11ll11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ᯴") + hub_url + bstack11ll11_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ᯵")
        return bstack11l1l11l11_opy_
    if hub_url:
        return bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ᯶") + hub_url + bstack11ll11_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ᯷")
    return bstack11llll1lll_opy_
def bstack11l1l11l1l1_opy_():
    return isinstance(os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ᯸")), str)
def bstack11l1ll1ll1_opy_(url):
    return urlparse(url).hostname
def bstack11l1l11l_opy_(hostname):
    for bstack1l11l11111_opy_ in bstack11ll1l111l_opy_:
        regex = re.compile(bstack1l11l11111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l111111ll_opy_(bstack11l1l1111l1_opy_, file_name, logger):
    bstack1l11l111l1_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠧࡿࠩ᯹")), bstack11l1l1111l1_opy_)
    try:
        if not os.path.exists(bstack1l11l111l1_opy_):
            os.makedirs(bstack1l11l111l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠨࢀࠪ᯺")), bstack11l1l1111l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11ll11_opy_ (u"ࠩࡺࠫ᯻")):
                pass
            with open(file_path, bstack11ll11_opy_ (u"ࠥࡻ࠰ࠨ᯼")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1llll1ll_opy_.format(str(e)))
def bstack11l111l11l1_opy_(file_name, key, value, logger):
    file_path = bstack11l111111ll_opy_(bstack11ll11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᯽"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1l1l1l1_opy_ = json.load(open(file_path, bstack11ll11_opy_ (u"ࠬࡸࡢࠨ᯾")))
        else:
            bstack11l1l1l1l1_opy_ = {}
        bstack11l1l1l1l1_opy_[key] = value
        with open(file_path, bstack11ll11_opy_ (u"ࠨࡷࠬࠤ᯿")) as outfile:
            json.dump(bstack11l1l1l1l1_opy_, outfile)
def bstack1l1l11111l_opy_(file_name, logger):
    file_path = bstack11l111111ll_opy_(bstack11ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᰀ"), file_name, logger)
    bstack11l1l1l1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11ll11_opy_ (u"ࠨࡴࠪᰁ")) as bstack111111l1l_opy_:
            bstack11l1l1l1l1_opy_ = json.load(bstack111111l1l_opy_)
    return bstack11l1l1l1l1_opy_
def bstack1ll11111l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ᰂ") + file_path + bstack11ll11_opy_ (u"ࠪࠤࠬᰃ") + str(e))
def bstack1lll1ll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11ll11_opy_ (u"ࠦࡁࡔࡏࡕࡕࡈࡘࡃࠨᰄ")
def bstack1llll11l1l_opy_(config):
    if bstack11ll11_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᰅ") in config:
        del (config[bstack11ll11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᰆ")])
        return False
    if bstack1lll1ll1_opy_() < version.parse(bstack11ll11_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭ᰇ")):
        return False
    if bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧᰈ")):
        return True
    if bstack11ll11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᰉ") in config and config[bstack11ll11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᰊ")] is False:
        return False
    else:
        return True
def bstack11llllll_opy_(args_list, bstack11l1l111l11_opy_):
    index = -1
    for value in bstack11l1l111l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1ll11l1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1ll11l1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111ll1ll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111ll1ll1l_opy_ = bstack111ll1ll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᰋ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᰌ"), exception=exception)
    def bstack11111l111l_opy_(self):
        if self.result != bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᰍ"):
            return None
        if isinstance(self.exception_type, str) and bstack11ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᰎ") in self.exception_type:
            return bstack11ll11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᰏ")
        return bstack11ll11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᰐ")
    def bstack111lll1llll_opy_(self):
        if self.result != bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᰑ"):
            return None
        if self.bstack111ll1ll1l_opy_:
            return self.bstack111ll1ll1l_opy_
        return bstack11l1l111ll1_opy_(self.exception)
def bstack11l1l111ll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l111llll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111ll1lll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11ll1l1_opy_(config, logger):
    try:
        import playwright
        bstack11l11l1l1l1_opy_ = playwright.__file__
        bstack11l11l111ll_opy_ = os.path.split(bstack11l11l1l1l1_opy_)
        bstack11l1111ll1l_opy_ = bstack11l11l111ll_opy_[0] + bstack11ll11_opy_ (u"ࠫ࠴ࡪࡲࡪࡸࡨࡶ࠴ࡶࡡࡤ࡭ࡤ࡫ࡪ࠵࡬ࡪࡤ࠲ࡧࡱ࡯࠯ࡤ࡮࡬࠲࡯ࡹࠧᰒ")
        os.environ[bstack11ll11_opy_ (u"ࠬࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠨᰓ")] = bstack1l111111l1_opy_(config)
        with open(bstack11l1111ll1l_opy_, bstack11ll11_opy_ (u"࠭ࡲࠨᰔ")) as f:
            bstack1lll1111ll_opy_ = f.read()
            bstack11l11l1l1ll_opy_ = bstack11ll11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ᰕ")
            bstack111llll1l1l_opy_ = bstack1lll1111ll_opy_.find(bstack11l11l1l1ll_opy_)
            if bstack111llll1l1l_opy_ == -1:
              process = subprocess.Popen(bstack11ll11_opy_ (u"ࠣࡰࡳࡱࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠧᰖ"), shell=True, cwd=bstack11l11l111ll_opy_[0])
              process.wait()
              bstack11l11ll111l_opy_ = bstack11ll11_opy_ (u"ࠩࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺࠢ࠼ࠩᰗ")
              bstack11l1l11l111_opy_ = bstack11ll11_opy_ (u"ࠥࠦࠧࠦ࡜ࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࡡࠨ࠻ࠡࡥࡲࡲࡸࡺࠠࡼࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴࠥࢃࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ࠭ࡀࠦࡩࡧࠢࠫࡴࡷࡵࡣࡦࡵࡶ࠲ࡪࡴࡶ࠯ࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜࠭ࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠩࠫ࠾ࠤࠧࠨࠢᰘ")
              bstack111llllllll_opy_ = bstack1lll1111ll_opy_.replace(bstack11l11ll111l_opy_, bstack11l1l11l111_opy_)
              with open(bstack11l1111ll1l_opy_, bstack11ll11_opy_ (u"ࠫࡼ࠭ᰙ")) as f:
                f.write(bstack111llllllll_opy_)
    except Exception as e:
        logger.error(bstack11ll1111l_opy_.format(str(e)))
def bstack11l111l11_opy_():
  try:
    bstack11l1111l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᰚ"))
    bstack11l1l1l11l1_opy_ = []
    if os.path.exists(bstack11l1111l111_opy_):
      with open(bstack11l1111l111_opy_) as f:
        bstack11l1l1l11l1_opy_ = json.load(f)
      os.remove(bstack11l1111l111_opy_)
    return bstack11l1l1l11l1_opy_
  except:
    pass
  return []
def bstack1lll111lll_opy_(bstack111l1l11l_opy_):
  try:
    bstack11l1l1l11l1_opy_ = []
    bstack11l1111l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᰛ"))
    if os.path.exists(bstack11l1111l111_opy_):
      with open(bstack11l1111l111_opy_) as f:
        bstack11l1l1l11l1_opy_ = json.load(f)
    bstack11l1l1l11l1_opy_.append(bstack111l1l11l_opy_)
    with open(bstack11l1111l111_opy_, bstack11ll11_opy_ (u"ࠧࡸࠩᰜ")) as f:
        json.dump(bstack11l1l1l11l1_opy_, f)
  except:
    pass
def bstack1lll1l1l1_opy_(logger, bstack11l11l11l1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack11ll11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᰝ"), bstack11ll11_opy_ (u"ࠩࠪᰞ"))
    if test_name == bstack11ll11_opy_ (u"ࠪࠫᰟ"):
        test_name = threading.current_thread().__dict__.get(bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡆࡩࡪ࡟ࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠪᰠ"), bstack11ll11_opy_ (u"ࠬ࠭ᰡ"))
    bstack11l11ll1l1l_opy_ = bstack11ll11_opy_ (u"࠭ࠬࠡࠩᰢ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11l11l1l_opy_:
        bstack1l111l111l_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᰣ"), bstack11ll11_opy_ (u"ࠨ࠲ࠪᰤ"))
        bstack11l111111_opy_ = {bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᰥ"): test_name, bstack11ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᰦ"): bstack11l11ll1l1l_opy_, bstack11ll11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᰧ"): bstack1l111l111l_opy_}
        bstack11l111lllll_opy_ = []
        bstack11l11111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᰨ"))
        if os.path.exists(bstack11l11111l11_opy_):
            with open(bstack11l11111l11_opy_) as f:
                bstack11l111lllll_opy_ = json.load(f)
        bstack11l111lllll_opy_.append(bstack11l111111_opy_)
        with open(bstack11l11111l11_opy_, bstack11ll11_opy_ (u"࠭ࡷࠨᰩ")) as f:
            json.dump(bstack11l111lllll_opy_, f)
    else:
        bstack11l111111_opy_ = {bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᰪ"): test_name, bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᰫ"): bstack11l11ll1l1l_opy_, bstack11ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᰬ"): str(multiprocessing.current_process().name)}
        if bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧᰭ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11l111111_opy_)
  except Exception as e:
      logger.warn(bstack11ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡰࡺࡶࡨࡷࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᰮ").format(e))
def bstack1lll1l111_opy_(error_message, test_name, index, logger):
  try:
    bstack11l11ll1111_opy_ = []
    bstack11l111111_opy_ = {bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᰯ"): test_name, bstack11ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᰰ"): error_message, bstack11ll11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᰱ"): index}
    bstack11l11111111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᰲ"))
    if os.path.exists(bstack11l11111111_opy_):
        with open(bstack11l11111111_opy_) as f:
            bstack11l11ll1111_opy_ = json.load(f)
    bstack11l11ll1111_opy_.append(bstack11l111111_opy_)
    with open(bstack11l11111111_opy_, bstack11ll11_opy_ (u"ࠩࡺࠫᰳ")) as f:
        json.dump(bstack11l11ll1111_opy_, f)
  except Exception as e:
    logger.warn(bstack11ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᰴ").format(e))
def bstack11llll11l1_opy_(bstack11ll111l1l_opy_, name, logger):
  try:
    bstack11l111111_opy_ = {bstack11ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᰵ"): name, bstack11ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᰶ"): bstack11ll111l1l_opy_, bstack11ll11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ᰷ࠬ"): str(threading.current_thread()._name)}
    return bstack11l111111_opy_
  except Exception as e:
    logger.warn(bstack11ll11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡥࡩ࡭ࡧࡶࡦࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ᰸").format(e))
  return
def bstack11l1111l1l1_opy_():
    return platform.system() == bstack11ll11_opy_ (u"ࠨ࡙࡬ࡲࡩࡵࡷࡴࠩ᰹")
def bstack1111ll1ll_opy_(bstack111llll1ll1_opy_, config, logger):
    bstack11l11lll11l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111llll1ll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡭ࡶࡨࡶࠥࡩ࡯࡯ࡨ࡬࡫ࠥࡱࡥࡺࡵࠣࡦࡾࠦࡲࡦࡩࡨࡼࠥࡳࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ᰺").format(e))
    return bstack11l11lll11l_opy_
def bstack11l1111111l_opy_(bstack11l11l1ll1l_opy_, bstack11l11l1l111_opy_):
    bstack11l1l111lll_opy_ = version.parse(bstack11l11l1ll1l_opy_)
    bstack11l1l1111ll_opy_ = version.parse(bstack11l11l1l111_opy_)
    if bstack11l1l111lll_opy_ > bstack11l1l1111ll_opy_:
        return 1
    elif bstack11l1l111lll_opy_ < bstack11l1l1111ll_opy_:
        return -1
    else:
        return 0
def bstack1111llll11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1111llll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11ll11ll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111111lll_opy_(options, framework, config, bstack1l11111111_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11ll11_opy_ (u"ࠪ࡫ࡪࡺࠧ᰻"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1lllllll11_opy_ = caps.get(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᰼"))
    bstack111lllllll1_opy_ = True
    bstack1ll11l11ll_opy_ = os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᰽")]
    bstack1ll111ll1l1_opy_ = config.get(bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᰾"), False)
    if bstack1ll111ll1l1_opy_:
        bstack1ll1llll1l1_opy_ = config.get(bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᰿"), {})
        bstack1ll1llll1l1_opy_[bstack11ll11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ᱀")] = os.getenv(bstack11ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᱁"))
        bstack11ll1ll1l11_opy_ = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ᱂"), bstack11ll11_opy_ (u"ࠫࢀࢃࠧ᱃"))).get(bstack11ll11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᱄"))
    if bstack11l1111ll11_opy_(caps.get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦ࡙࠶ࡇࠬ᱅"))) or bstack11l1111ll11_opy_(caps.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧ᱆"))):
        bstack111lllllll1_opy_ = False
    if bstack1llll11l1l_opy_({bstack11ll11_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ᱇"): bstack111lllllll1_opy_}):
        bstack1lllllll11_opy_ = bstack1lllllll11_opy_ or {}
        bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ᱈")] = bstack11l11ll11ll_opy_(framework)
        bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᱉")] = bstack1l1ll111ll1_opy_()
        bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ᱊")] = bstack1ll11l11ll_opy_
        bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ᱋")] = bstack1l11111111_opy_
        if bstack1ll111ll1l1_opy_:
            bstack1lllllll11_opy_[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᱌")] = bstack1ll111ll1l1_opy_
            bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᱍ")] = bstack1ll1llll1l1_opy_
            bstack1lllllll11_opy_[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᱎ")][bstack11ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᱏ")] = bstack11ll1ll1l11_opy_
        if getattr(options, bstack11ll11_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ᱐"), None):
            options.set_capability(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᱑"), bstack1lllllll11_opy_)
        else:
            options[bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᱒")] = bstack1lllllll11_opy_
    else:
        if getattr(options, bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧ᱓"), None):
            options.set_capability(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᱔"), bstack11l11ll11ll_opy_(framework))
            options.set_capability(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᱕"), bstack1l1ll111ll1_opy_())
            options.set_capability(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᱖"), bstack1ll11l11ll_opy_)
            options.set_capability(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᱗"), bstack1l11111111_opy_)
            if bstack1ll111ll1l1_opy_:
                options.set_capability(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᱘"), bstack1ll111ll1l1_opy_)
                options.set_capability(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᱙"), bstack1ll1llll1l1_opy_)
                options.set_capability(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ࠳ࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᱚ"), bstack11ll1ll1l11_opy_)
        else:
            options[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᱛ")] = bstack11l11ll11ll_opy_(framework)
            options[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᱜ")] = bstack1l1ll111ll1_opy_()
            options[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᱝ")] = bstack1ll11l11ll_opy_
            options[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᱞ")] = bstack1l11111111_opy_
            if bstack1ll111ll1l1_opy_:
                options[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᱟ")] = bstack1ll111ll1l1_opy_
                options[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᱠ")] = bstack1ll1llll1l1_opy_
                options[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᱡ")][bstack11ll11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᱢ")] = bstack11ll1ll1l11_opy_
    return options
def bstack11l111l1l1l_opy_(bstack111llllll1l_opy_, framework):
    bstack1l11111111_opy_ = bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥᱣ"))
    if bstack111llllll1l_opy_ and len(bstack111llllll1l_opy_.split(bstack11ll11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᱤ"))) > 1:
        ws_url = bstack111llllll1l_opy_.split(bstack11ll11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᱥ"))[0]
        if bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᱦ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l111l1111_opy_ = json.loads(urllib.parse.unquote(bstack111llllll1l_opy_.split(bstack11ll11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᱧ"))[1]))
            bstack11l111l1111_opy_ = bstack11l111l1111_opy_ or {}
            bstack1ll11l11ll_opy_ = os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᱨ")]
            bstack11l111l1111_opy_[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᱩ")] = str(framework) + str(__version__)
            bstack11l111l1111_opy_[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᱪ")] = bstack1l1ll111ll1_opy_()
            bstack11l111l1111_opy_[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᱫ")] = bstack1ll11l11ll_opy_
            bstack11l111l1111_opy_[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᱬ")] = bstack1l11111111_opy_
            bstack111llllll1l_opy_ = bstack111llllll1l_opy_.split(bstack11ll11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᱭ"))[0] + bstack11ll11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᱮ") + urllib.parse.quote(json.dumps(bstack11l111l1111_opy_))
    return bstack111llllll1l_opy_
def bstack1ll1111l_opy_():
    global bstack1ll11ll1l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll11ll1l1_opy_ = BrowserType.connect
    return bstack1ll11ll1l1_opy_
def bstack1l111ll1ll_opy_(framework_name):
    global bstack1lll11l1ll_opy_
    bstack1lll11l1ll_opy_ = framework_name
    return framework_name
def bstack1l1lllll1_opy_(self, *args, **kwargs):
    global bstack1ll11ll1l1_opy_
    try:
        global bstack1lll11l1ll_opy_
        if bstack11ll11_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᱯ") in kwargs:
            kwargs[bstack11ll11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᱰ")] = bstack11l111l1l1l_opy_(
                kwargs.get(bstack11ll11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᱱ"), None),
                bstack1lll11l1ll_opy_
            )
    except Exception as e:
        logger.error(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤᱲ").format(str(e)))
    return bstack1ll11ll1l1_opy_(self, *args, **kwargs)
def bstack11l111l111l_opy_(bstack11l11ll1l11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1ll111_opy_(bstack11l11ll1l11_opy_, bstack11ll11_opy_ (u"ࠥࠦᱳ"))
        if proxies and proxies.get(bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᱴ")):
            parsed_url = urlparse(proxies.get(bstack11ll11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᱵ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᱶ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᱷ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᱸ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᱹ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l1l1l1_opy_(bstack11l11ll1l11_opy_):
    bstack111llll111l_opy_ = {
        bstack11ll111111l_opy_[bstack11l111lll1l_opy_]: bstack11l11ll1l11_opy_[bstack11l111lll1l_opy_]
        for bstack11l111lll1l_opy_ in bstack11l11ll1l11_opy_
        if bstack11l111lll1l_opy_ in bstack11ll111111l_opy_
    }
    bstack111llll111l_opy_[bstack11ll11_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᱺ")] = bstack11l111l111l_opy_(bstack11l11ll1l11_opy_, bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᱻ")))
    bstack111lllll1ll_opy_ = [element.lower() for element in bstack11l1ll1llll_opy_]
    bstack111lllll111_opy_(bstack111llll111l_opy_, bstack111lllll1ll_opy_)
    return bstack111llll111l_opy_
def bstack111lllll111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11ll11_opy_ (u"ࠧ࠰ࠪࠫࠬࠥᱼ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111lllll111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111lllll111_opy_(item, keys)
def bstack1l1lllll111_opy_():
    bstack11l111l1l11_opy_ = [os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣᱽ")), os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠢࡿࠤ᱾")), bstack11ll11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᱿")), os.path.join(bstack11ll11_opy_ (u"ࠩ࠲ࡸࡲࡶࠧᲀ"), bstack11ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᲁ"))]
    for path in bstack11l111l1l11_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11ll11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦᲂ") + str(path) + bstack11ll11_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣᲃ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11ll11_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥᲄ") + str(path) + bstack11ll11_opy_ (u"ࠢࠨࠤᲅ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11ll11_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣᲆ") + str(path) + bstack11ll11_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢᲇ"))
            else:
                logger.debug(bstack11ll11_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧᲈ") + str(path) + bstack11ll11_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣᲉ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11ll11_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥᲊ") + str(path) + bstack11ll11_opy_ (u"ࠨࠧ࠯ࠤ᲋"))
            return path
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧ᲌") + str(e) + bstack11ll11_opy_ (u"ࠣࠤ᲍"))
    logger.debug(bstack11ll11_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨ᲎"))
    return None
@measure(event_name=EVENTS.bstack11l1lll1ll1_opy_, stage=STAGE.bstack1lll11llll_opy_)
def bstack1ll1ll11l1l_opy_(binary_path, bstack1lll1111l11_opy_, bs_config):
    logger.debug(bstack11ll11_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤ᲏").format(binary_path))
    bstack111llll1l11_opy_ = bstack11ll11_opy_ (u"ࠫࠬᲐ")
    bstack11l1l111111_opy_ = {
        bstack11ll11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᲑ"): __version__,
        bstack11ll11_opy_ (u"ࠨ࡯ࡴࠤᲒ"): platform.system(),
        bstack11ll11_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣᲓ"): platform.machine(),
        bstack11ll11_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᲔ"): bstack11ll11_opy_ (u"ࠩ࠳ࠫᲕ"),
        bstack11ll11_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤᲖ"): bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᲗ")
    }
    bstack11l11llll1l_opy_(bstack11l1l111111_opy_)
    try:
        if binary_path:
            bstack11l1l111111_opy_[bstack11ll11_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᲘ")] = subprocess.check_output([binary_path, bstack11ll11_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢᲙ")]).strip().decode(bstack11ll11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭Ლ"))
        response = requests.request(
            bstack11ll11_opy_ (u"ࠨࡉࡈࡘࠬᲛ"),
            url=bstack11ll11l1ll_opy_(bstack11l1ll1ll1l_opy_),
            headers=None,
            auth=(bs_config[bstack11ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᲜ")], bs_config[bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭Ო")]),
            json=None,
            params=bstack11l1l111111_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11ll11_opy_ (u"ࠫࡺࡸ࡬ࠨᲞ") in data.keys() and bstack11ll11_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩࡥࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᲟ") in data.keys():
            logger.debug(bstack11ll11_opy_ (u"ࠨࡎࡦࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡣ࡫ࡱࡥࡷࡿࠬࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢᲠ").format(bstack11l1l111111_opy_[bstack11ll11_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᲡ")]))
            if bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫᲢ") in os.environ:
                logger.debug(bstack11ll11_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡡࡴࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠥ࡯ࡳࠡࡵࡨࡸࠧᲣ"))
                data[bstack11ll11_opy_ (u"ࠪࡹࡷࡲࠧᲤ")] = os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧᲥ")]
            bstack11l1111lll1_opy_ = bstack11l11l11lll_opy_(data[bstack11ll11_opy_ (u"ࠬࡻࡲ࡭ࠩᲦ")], bstack1lll1111l11_opy_)
            bstack111llll1l11_opy_ = os.path.join(bstack1lll1111l11_opy_, bstack11l1111lll1_opy_)
            os.chmod(bstack111llll1l11_opy_, 0o777) # bstack11l11l1llll_opy_ permission
            return bstack111llll1l11_opy_
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨᲧ").format(e))
    return binary_path
def bstack11l11llll1l_opy_(bstack11l1l111111_opy_):
    try:
        if bstack11ll11_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭Შ") not in bstack11l1l111111_opy_[bstack11ll11_opy_ (u"ࠨࡱࡶࠫᲩ")].lower():
            return
        if os.path.exists(bstack11ll11_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᲪ")):
            with open(bstack11ll11_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᲫ"), bstack11ll11_opy_ (u"ࠦࡷࠨᲬ")) as f:
                bstack11l11l11111_opy_ = {}
                for line in f:
                    if bstack11ll11_opy_ (u"ࠧࡃࠢᲭ") in line:
                        key, value = line.rstrip().split(bstack11ll11_opy_ (u"ࠨ࠽ࠣᲮ"), 1)
                        bstack11l11l11111_opy_[key] = value.strip(bstack11ll11_opy_ (u"ࠧࠣ࡞ࠪࠫᲯ"))
                bstack11l1l111111_opy_[bstack11ll11_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨᲰ")] = bstack11l11l11111_opy_.get(bstack11ll11_opy_ (u"ࠤࡌࡈࠧᲱ"), bstack11ll11_opy_ (u"ࠥࠦᲲ"))
        elif os.path.exists(bstack11ll11_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡤࡰࡵ࡯࡮ࡦ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᲳ")):
            bstack11l1l111111_opy_[bstack11ll11_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬᲴ")] = bstack11ll11_opy_ (u"࠭ࡡ࡭ࡲ࡬ࡲࡪ࠭Ჵ")
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡥ࡫ࡶࡸࡷࡵࠠࡰࡨࠣࡰ࡮ࡴࡵࡹࠤᲶ") + e)
@measure(event_name=EVENTS.bstack11ll1111ll1_opy_, stage=STAGE.bstack1lll11llll_opy_)
def bstack11l11l11lll_opy_(bstack11l11l11l11_opy_, bstack11l11111lll_opy_):
    logger.debug(bstack11ll11_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭࠻ࠢࠥᲷ") + str(bstack11l11l11l11_opy_) + bstack11ll11_opy_ (u"ࠤࠥᲸ"))
    zip_path = os.path.join(bstack11l11111lll_opy_, bstack11ll11_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪ࡟ࡧ࡫࡯ࡩ࠳ࢀࡩࡱࠤᲹ"))
    bstack11l1111lll1_opy_ = bstack11ll11_opy_ (u"ࠫࠬᲺ")
    with requests.get(bstack11l11l11l11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11ll11_opy_ (u"ࠧࡽࡢࠣ᲻")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11ll11_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣ᲼"))
    with zipfile.ZipFile(zip_path, bstack11ll11_opy_ (u"ࠧࡳࠩᲽ")) as zip_ref:
        bstack11l1l11lll1_opy_ = zip_ref.namelist()
        if len(bstack11l1l11lll1_opy_) > 0:
            bstack11l1111lll1_opy_ = bstack11l1l11lll1_opy_[0] # bstack11l11111ll1_opy_ bstack11ll11111l1_opy_ will be bstack11l11llll11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l11111lll_opy_)
        logger.debug(bstack11ll11_opy_ (u"ࠣࡈ࡬ࡰࡪࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡥࡹࡶࡵࡥࡨࡺࡥࡥࠢࡷࡳࠥ࠭ࠢᲾ") + str(bstack11l11111lll_opy_) + bstack11ll11_opy_ (u"ࠤࠪࠦᲿ"))
    os.remove(zip_path)
    return bstack11l1111lll1_opy_
def get_cli_dir():
    bstack11l111l11ll_opy_ = bstack1l1lllll111_opy_()
    if bstack11l111l11ll_opy_:
        bstack1lll1111l11_opy_ = os.path.join(bstack11l111l11ll_opy_, bstack11ll11_opy_ (u"ࠥࡧࡱ࡯ࠢ᳀"))
        if not os.path.exists(bstack1lll1111l11_opy_):
            os.makedirs(bstack1lll1111l11_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1111l11_opy_
    else:
        raise FileNotFoundError(bstack11ll11_opy_ (u"ࠦࡓࡵࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾ࠴ࠢ᳁"))
def bstack1ll1llll11l_opy_(bstack1lll1111l11_opy_):
    bstack11ll11_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡳࠦࡡࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠢࠣࠤ᳂")
    bstack11l1l1l111l_opy_ = [
        os.path.join(bstack1lll1111l11_opy_, f)
        for f in os.listdir(bstack1lll1111l11_opy_)
        if os.path.isfile(os.path.join(bstack1lll1111l11_opy_, f)) and f.startswith(bstack11ll11_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾ࠳ࠢ᳃"))
    ]
    if len(bstack11l1l1l111l_opy_) > 0:
        return max(bstack11l1l1l111l_opy_, key=os.path.getmtime) # get bstack11l11111l1l_opy_ binary
    return bstack11ll11_opy_ (u"ࠢࠣ᳄")
def bstack11ll1lll1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1l11l111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l11l111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1l11ll1_opy_(data, keys, default=None):
    bstack11ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡤࡪࡪࡲࡹࠡࡩࡨࡸࠥࡧࠠ࡯ࡧࡶࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࠦࡦࡳࡱࡰࠤࡦࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡥࡹࡧ࠺ࠡࡖ࡫ࡩࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶࠣࡸࡴࠦࡴࡳࡣࡹࡩࡷࡹࡥ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡫ࡦࡻࡶ࠾ࠥࡇࠠ࡭࡫ࡶࡸࠥࡵࡦࠡ࡭ࡨࡽࡸ࠵ࡩ࡯ࡦ࡬ࡧࡪࡹࠠࡳࡧࡳࡶࡪࡹࡥ࡯ࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡦࡨࡤࡹࡱࡺ࠺ࠡࡘࡤࡰࡺ࡫ࠠࡵࡱࠣࡶࡪࡺࡵࡳࡰࠣ࡭࡫ࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡴࡨࡸࡺࡸ࡮࠻ࠢࡗ࡬ࡪࠦࡶࡢ࡮ࡸࡩࠥࡧࡴࠡࡶ࡫ࡩࠥࡴࡥࡴࡶࡨࡨࠥࡶࡡࡵࡪ࠯ࠤࡴࡸࠠࡥࡧࡩࡥࡺࡲࡴࠡ࡫ࡩࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪ࠮ࠋࠢࠣࠤࠥࠨࠢࠣ᳅")
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