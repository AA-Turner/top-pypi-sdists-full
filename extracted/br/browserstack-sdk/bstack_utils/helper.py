# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import collections
import copy
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
from math import ceil
from unittest import result
import urllib
from urllib.parse import urlparse
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111llllll_opy_, bstack1l1llll1l1_opy_, bstack11lll111ll_opy_,
                                    bstack11111l11l11_opy_, bstack111111l111l_opy_, bstack111111l11l1_opy_, bstack11111l1l1ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111111l1l1_opy_, bstack1lllllllll1_opy_
from bstack_utils.proxy import bstack11l1ll1l_opy_, bstack1ll11111l_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11l11111l_opy_ import bstack11111l1ll_opy_
from browserstack_sdk._version import __version__
global_config = Config.bstack1lllll1lll1_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack1111l1ll1ll_opy_(config):
    return config[bstack111ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ↏")]
def bstack1111ll1l1l1_opy_(config):
    return config[bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭←")]
def bstack1l1l11111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def is_robot_playwright_installed():
    try:
        import Browser
        return True
    except ImportError:
        return False
def bstack1llll111ll11_opy_(obj):
    values = []
    bstack1lll1llllll1_opy_ = re.compile(bstack111ll11_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣ↑"), re.I)
    for key in obj.keys():
        if bstack1lll1llllll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1llll111l111_opy_(config):
    tags = []
    tags.extend(bstack1llll111ll11_opy_(os.environ))
    tags.extend(bstack1llll111ll11_opy_(config))
    return tags
def bstack1llllll1l111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1llll1111111_opy_(bstack1llllll11ll1_opy_):
    if not bstack1llllll11ll1_opy_:
        return bstack111ll11_opy_ (u"ࠬ࠭→")
    return bstack111ll11_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢ↓").format(bstack1llllll11ll1_opy_.name, bstack1llllll11ll1_opy_.email)
def bstack1111l1lllll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1lllll1lllll_opy_ = repo.common_dir
        info = {
            bstack111ll11_opy_ (u"ࠢࡴࡪࡤࠦ↔"): repo.head.commit.hexsha,
            bstack111ll11_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦ↕"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111ll11_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤ↖"): repo.active_branch.name,
            bstack111ll11_opy_ (u"ࠥࡸࡦ࡭ࠢ↗"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111ll11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢ↘"): bstack1llll1111111_opy_(repo.head.commit.committer),
            bstack111ll11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨ↙"): repo.head.commit.committed_datetime.isoformat(),
            bstack111ll11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨ↚"): bstack1llll1111111_opy_(repo.head.commit.author),
            bstack111ll11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧ↛"): repo.head.commit.authored_datetime.isoformat(),
            bstack111ll11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ↜"): repo.head.commit.message,
            bstack111ll11_opy_ (u"ࠤࡵࡳࡴࡺࠢ↝"): repo.git.rev_parse(bstack111ll11_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧ↞")),
            bstack111ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ↟"): bstack1lllll1lllll_opy_,
            bstack111ll11_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ↠"): subprocess.check_output([bstack111ll11_opy_ (u"ࠨࡧࡪࡶࠥ↡"), bstack111ll11_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥ↢"), bstack111ll11_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦ↣")]).strip().decode(
                bstack111ll11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ↤")),
            bstack111ll11_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ↥"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111ll11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ↦"): repo.git.rev_list(
                bstack111ll11_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧ↧").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1llll111lll1_opy_ = []
        for remote in remotes:
            bstack1llll1lllll1_opy_ = {
                bstack111ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ↨"): remote.name,
                bstack111ll11_opy_ (u"ࠢࡶࡴ࡯ࠦ↩"): remote.url,
            }
            bstack1llll111lll1_opy_.append(bstack1llll1lllll1_opy_)
        bstack1llllll1llll_opy_ = {
            bstack111ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ↪"): bstack111ll11_opy_ (u"ࠤࡪ࡭ࡹࠨ↫"),
            **info,
            bstack111ll11_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦ↬"): bstack1llll111lll1_opy_
        }
        bstack1llllll1llll_opy_ = bstack1lll1lllll11_opy_(bstack1llllll1llll_opy_)
        return bstack1llllll1llll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ↭").format(err))
        return {}
def bstack1llll11ll111_opy_(bstack1llll1l1ll11_opy_=None):
    bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࡤࡰࡱࡿࠠࡧࡱࡵࡱࡦࡺࡴࡦࡦࠣࡪࡴࡸࠠࡂࡋࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࡵࡴࡧࠣࡧࡦࡹࡥࡴࠢࡩࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫ࡵ࡬ࡥࡧࡵࠤ࡮ࡴࠠࡵࡪࡨࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡎࡰࡰࡨ࠾ࠥࡓ࡯࡯ࡱ࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪ࠯ࠤࡺࡹࡥࡴࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࡛ࠦࡰࡵ࠱࡫ࡪࡺࡣࡸࡦࠫ࠭ࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡅ࡮ࡲࡷࡽࠥࡲࡩࡴࡶࠣ࡟ࡢࡀࠠࡎࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡳࡵࠠࡴࡱࡸࡶࡨ࡫ࡳࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨ࠱ࠦࡲࡦࡶࡸࡶࡳࡹࠠ࡜࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠽ࠤࡒࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪࠣࡻ࡮ࡺࡨࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࠣࡪࡴࡲࡤࡦࡴࡶࠤࡹࡵࠠࡢࡰࡤࡰࡾࢀࡥࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡮࡬ࡷࡹࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡦ࡬ࡧࡹࡹࠬࠡࡧࡤࡧ࡭ࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡡࠡࡨࡲࡰࡩ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ↮")
    if bstack1llll1l1ll11_opy_ is None:
        bstack1llll1l1ll11_opy_ = [os.getcwd()]
    elif isinstance(bstack1llll1l1ll11_opy_, list) and len(bstack1llll1l1ll11_opy_) == 0:
        return []
    results = []
    for folder in bstack1llll1l1ll11_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack111ll11_opy_ (u"ࠨࡆࡰ࡮ࡧࡩࡷࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦ↯").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack111ll11_opy_ (u"ࠢࡱࡴࡌࡨࠧ↰"): bstack111ll11_opy_ (u"ࠣࠤ↱"),
                bstack111ll11_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ↲"): [],
                bstack111ll11_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦ↳"): [],
                bstack111ll11_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦ↴"): bstack111ll11_opy_ (u"ࠧࠨ↵"),
                bstack111ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢ↶"): [],
                bstack111ll11_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣ↷"): bstack111ll11_opy_ (u"ࠣࠤ↸"),
                bstack111ll11_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤ↹"): bstack111ll11_opy_ (u"ࠥࠦ↺"),
                bstack111ll11_opy_ (u"ࠦࡵࡸࡒࡢࡹࡇ࡭࡫࡬ࠢ↻"): bstack111ll11_opy_ (u"ࠧࠨ↼")
            }
            bstack1lll1lll1l1l_opy_ = repo.active_branch.name
            bstack1lllll1ll11l_opy_ = repo.head.commit
            result[bstack111ll11_opy_ (u"ࠨࡰࡳࡋࡧࠦ↽")] = bstack1lllll1ll11l_opy_.hexsha
            bstack1llllll1l1ll_opy_ = _1llll1ll1lll_opy_(repo)
            logger.debug(bstack111ll11_opy_ (u"ࠢࡃࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳࡀࠠࠣ↾") + str(bstack1llllll1l1ll_opy_) + bstack111ll11_opy_ (u"ࠣࠤ↿"))
            if bstack1llllll1l1ll_opy_:
                try:
                    bstack1lllll1l1l11_opy_ = repo.git.diff(bstack111ll11_opy_ (u"ࠤ࠰࠱ࡳࡧ࡭ࡦ࠯ࡲࡲࡱࡿࠢ⇀"), bstack1l1ll1111ll_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲࠳ࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽࠣ⇁")).split(bstack111ll11_opy_ (u"ࠫࡡࡴࠧ⇂"))
                    logger.debug(bstack111ll11_opy_ (u"ࠧࡉࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥࡨࡥࡵࡹࡨࡩࡳࠦࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂࠦࡡ࡯ࡦࠣࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࡀࠠࠣ⇃") + str(bstack1lllll1l1l11_opy_) + bstack111ll11_opy_ (u"ࠨࠢ⇄"))
                    result[bstack111ll11_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨ⇅")] = [f.strip() for f in bstack1lllll1l1l11_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1l1ll1111ll_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧ⇆")))
                except Exception:
                    logger.debug(bstack111ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡣࡴࡤࡲࡨ࡮ࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠲ࠥࡌࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡳࡧࡦࡩࡳࡺࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠤ⇇"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack111ll11_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤ⇈")] = _1lllll11l11l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack111ll11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ⇉")] = _1lllll11l11l_opy_(commits[:5])
            bstack1llll1llllll_opy_ = set()
            bstack1llll11l111l_opy_ = []
            for commit in commits:
                logger.debug(bstack111ll11_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡩࡵ࠼ࠣࠦ⇊") + str(commit.message) + bstack111ll11_opy_ (u"ࠨࠢ⇋"))
                bstack1lllllll1111_opy_ = commit.author.name if commit.author else bstack111ll11_opy_ (u"ࠢࡖࡰ࡮ࡲࡴࡽ࡮ࠣ⇌")
                bstack1llll1llllll_opy_.add(bstack1lllllll1111_opy_)
                bstack1llll11l111l_opy_.append({
                    bstack111ll11_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ⇍"): commit.message.strip(),
                    bstack111ll11_opy_ (u"ࠤࡸࡷࡪࡸࠢ⇎"): bstack1lllllll1111_opy_
                })
            result[bstack111ll11_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦ⇏")] = list(bstack1llll1llllll_opy_)
            result[bstack111ll11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧ⇐")] = bstack1llll11l111l_opy_
            result[bstack111ll11_opy_ (u"ࠧࡶࡲࡅࡣࡷࡩࠧ⇑")] = bstack1lllll1ll11l_opy_.committed_datetime.strftime(bstack111ll11_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࠣ⇒"))
            if (not result[bstack111ll11_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣ⇓")] or result[bstack111ll11_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ⇔")].strip() == bstack111ll11_opy_ (u"ࠤࠥ⇕")) and bstack1lllll1ll11l_opy_.message:
                bstack1lllllll111l_opy_ = bstack1lllll1ll11l_opy_.message.strip().splitlines()
                result[bstack111ll11_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦ⇖")] = bstack1lllllll111l_opy_[0] if bstack1lllllll111l_opy_ else bstack111ll11_opy_ (u"ࠦࠧ⇗")
                if len(bstack1lllllll111l_opy_) > 2:
                    result[bstack111ll11_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧ⇘")] = bstack111ll11_opy_ (u"࠭࡜࡯ࠩ⇙").join(bstack1lllllll111l_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack111ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࠮ࡦࡰ࡮ࡧࡩࡷࡀࠠࡼࡿࠬ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ⇚").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1lllll1l1l1l_opy_ = [
        result
        for result in results
        if _1llll1ll11ll_opy_(result)
    ]
    return bstack1lllll1l1l1l_opy_
def _1llll1ll11ll_opy_(result):
    bstack111ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡨࡰࡵ࡫ࡲࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡡࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡶࡹࡱࡺࠠࡪࡵࠣࡺࡦࡲࡩࡥࠢࠫࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠦࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠥࡧ࡮ࡥࠢࡤࡹࡹ࡮࡯ࡳࡵࠬ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⇛")
    return (
        isinstance(result.get(bstack111ll11_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ⇜"), None), list)
        and len(result[bstack111ll11_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤ⇝")]) > 0
        and isinstance(result.get(bstack111ll11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧ⇞"), None), list)
        and len(result[bstack111ll11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ⇟")]) > 0
    )
def _1llll1ll1lll_opy_(repo):
    bstack111ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡔࡳࡻࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷ࡬ࡪࠦࡢࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡷ࡫ࡰࡰࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣ࡬ࡦࡸࡤࡤࡱࡧࡩࡩࠦ࡮ࡢ࡯ࡨࡷࠥࡧ࡮ࡥࠢࡺࡳࡷࡱࠠࡸ࡫ࡷ࡬ࠥࡧ࡬࡭࡙ࠢࡇࡘࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡲࡴ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡪࡥࡧࡣࡸࡰࡹࠦࡢࡳࡣࡱࡧ࡭ࠦࡩࡧࠢࡳࡳࡸࡹࡩࡣ࡮ࡨ࠰ࠥ࡫࡬ࡴࡧࠣࡒࡴࡴࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ⇠")
    try:
        try:
            origin = repo.remotes.origin
            bstack1lll1lll1ll1_opy_ = origin.refs[bstack111ll11_opy_ (u"ࠧࡉࡇࡄࡈࠬ⇡")]
            target = bstack1lll1lll1ll1_opy_.reference.name
            if target.startswith(bstack111ll11_opy_ (u"ࠨࡱࡵ࡭࡬࡯࡮࠰ࠩ⇢")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack111ll11_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪ⇣")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1lllll11l11l_opy_(commits):
    bstack111ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡡࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⇤")
    bstack1lllll1l1l11_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1llll11lllll_opy_ in diff:
                        if bstack1llll11lllll_opy_.a_path:
                            bstack1lllll1l1l11_opy_.add(bstack1llll11lllll_opy_.a_path)
                        if bstack1llll11lllll_opy_.b_path:
                            bstack1lllll1l1l11_opy_.add(bstack1llll11lllll_opy_.b_path)
    except Exception:
        pass
    return list(bstack1lllll1l1l11_opy_)
def bstack1lll1lllll11_opy_(bstack1llllll1llll_opy_):
    bstack1llll111111l_opy_ = bstack1llll11ll1ll_opy_(bstack1llllll1llll_opy_)
    if bstack1llll111111l_opy_ and bstack1llll111111l_opy_ > bstack11111l11l11_opy_:
        bstack1llll11l1lll_opy_ = bstack1llll111111l_opy_ - bstack11111l11l11_opy_
        bstack1lllll1lll11_opy_ = bstack1lllll1ll111_opy_(bstack1llllll1llll_opy_[bstack111ll11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ⇥")], bstack1llll11l1lll_opy_)
        bstack1llllll1llll_opy_[bstack111ll11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ⇦")] = bstack1lllll1lll11_opy_
        logger.info(bstack111ll11_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣ⇧")
                    .format(bstack1llll11ll1ll_opy_(bstack1llllll1llll_opy_) / 1024))
    return bstack1llllll1llll_opy_
def bstack1llll11ll1ll_opy_(json_data):
    try:
        if json_data:
            bstack1lllll1l11ll_opy_ = json.dumps(json_data)
            bstack1llll1l1lll1_opy_ = sys.getsizeof(bstack1lllll1l11ll_opy_)
            return bstack1llll1l1lll1_opy_
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢ⇨").format(e))
    return -1
def bstack1lllll1ll111_opy_(field, bstack1llll1l11l11_opy_):
    try:
        bstack1llllll1l1l1_opy_ = len(bytes(bstack111111l111l_opy_, bstack111ll11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ⇩")))
        bstack1llll11111ll_opy_ = bytes(field, bstack111ll11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ⇪"))
        bstack1llll1l1l1ll_opy_ = len(bstack1llll11111ll_opy_)
        bstack1lll1lll1lll_opy_ = ceil(bstack1llll1l1l1ll_opy_ - bstack1llll1l11l11_opy_ - bstack1llllll1l1l1_opy_)
        if bstack1lll1lll1lll_opy_ > 0:
            bstack1llllll1lll1_opy_ = bstack1llll11111ll_opy_[:bstack1lll1lll1lll_opy_].decode(bstack111ll11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⇫"), errors=bstack111ll11_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫ⇬")) + bstack111111l111l_opy_
            return bstack1llllll1lll1_opy_
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥ⇭").format(e))
    return field
def bstack1l11111lll_opy_():
    env = os.environ
    if (bstack111ll11_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ⇮") in env and len(env[bstack111ll11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ⇯")]) > 0) or (
            bstack111ll11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ⇰") in env and len(env[bstack111ll11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ⇱")]) > 0):
        return {
            bstack111ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ⇲"): bstack111ll11_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧ⇳"),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⇴"): env.get(bstack111ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ⇵")),
            bstack111ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⇶"): env.get(bstack111ll11_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥ⇷")),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⇸"): env.get(bstack111ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ⇹"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠦࡈࡏࠢ⇺")) == bstack111ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ⇻") and bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣ⇼"))):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⇽"): bstack111ll11_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥ⇾"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⇿"): env.get(bstack111ll11_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ∀")),
            bstack111ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ∁"): env.get(bstack111ll11_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤ∂")),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ∃"): env.get(bstack111ll11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥ∄"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠣࡅࡌࠦ∅")) == bstack111ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ∆") and bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥ∇"))):
        return {
            bstack111ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ∈"): bstack111ll11_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣ∉"),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ∊"): env.get(bstack111ll11_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢ∋")),
            bstack111ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ∌"): env.get(bstack111ll11_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ∍")),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ∎"): env.get(bstack111ll11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ∏"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠧࡉࡉࠣ∐")) == bstack111ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ∑") and env.get(bstack111ll11_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣ−")) == bstack111ll11_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ∓"):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ∔"): bstack111ll11_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧ∕"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ∖"): None,
            bstack111ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ∗"): None,
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ∘"): None
        }
    if env.get(bstack111ll11_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥ∙")) and env.get(bstack111ll11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦ√")):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ∛"): bstack111ll11_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨ∜"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ∝"): env.get(bstack111ll11_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥ∞")),
            bstack111ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ∟"): None,
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ∠"): env.get(bstack111ll11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ∡"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠤࡆࡍࠧ∢")) == bstack111ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣ∣") and bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥ∤"))):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ∥"): bstack111ll11_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧ∦"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ∧"): env.get(bstack111ll11_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦ∨")),
            bstack111ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ∩"): None,
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ∪"): env.get(bstack111ll11_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ∫"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠧࡉࡉࠣ∬")) == bstack111ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ∭") and bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥ∮"))):
        return {
            bstack111ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ∯"): bstack111ll11_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧ∰"),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ∱"): env.get(bstack111ll11_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥ∲")),
            bstack111ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ∳"): env.get(bstack111ll11_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ∴")),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ∵"): env.get(bstack111ll11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦ∶"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠤࡆࡍࠧ∷")) == bstack111ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣ∸") and bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢ∹"))):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ∺"): bstack111ll11_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨ∻"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ∼"): env.get(bstack111ll11_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧ∽")),
            bstack111ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ∾"): env.get(bstack111ll11_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ∿")),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ≀"): env.get(bstack111ll11_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣ≁"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠨࡃࡊࠤ≂")) == bstack111ll11_opy_ (u"ࠢࡵࡴࡸࡩࠧ≃") and bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦ≄"))):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ≅"): bstack111ll11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨ≆"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ≇"): env.get(bstack111ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ≈")),
            bstack111ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ≉"): env.get(bstack111ll11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤ≊")) or env.get(bstack111ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦ≋")),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ≌"): env.get(bstack111ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ≍"))
        }
    if bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ≎"))):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ≏"): bstack111ll11_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨ≐"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ≑"): bstack111ll11_opy_ (u"ࠣࡽࢀࡿࢂࠨ≒").format(env.get(bstack111ll11_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬ≓")), env.get(bstack111ll11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪ≔"))),
            bstack111ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ≕"): env.get(bstack111ll11_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦ≖")),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ≗"): env.get(bstack111ll11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ≘"))
        }
    if bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥ≙"))):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ≚"): bstack111ll11_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧ≛"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ≜"): bstack111ll11_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦ≝").format(env.get(bstack111ll11_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬ≞")), env.get(bstack111ll11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨ≟")), env.get(bstack111ll11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩ≠")), env.get(bstack111ll11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭≡"))),
            bstack111ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ≢"): env.get(bstack111ll11_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ≣")),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ≤"): env.get(bstack111ll11_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ≥"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣ≦")) and env.get(bstack111ll11_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥ≧")):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ≨"): bstack111ll11_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧ≩"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ≪"): bstack111ll11_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣ≫").format(env.get(bstack111ll11_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩ≬")), env.get(bstack111ll11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬ≭")), env.get(bstack111ll11_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨ≮"))),
            bstack111ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ≯"): env.get(bstack111ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ≰")),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ≱"): env.get(bstack111ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ≲"))
        }
    if any([env.get(bstack111ll11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ≳")), env.get(bstack111ll11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ≴")), env.get(bstack111ll11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ≵"))]):
        return {
            bstack111ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ≶"): bstack111ll11_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥ≷"),
            bstack111ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ≸"): env.get(bstack111ll11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ≹")),
            bstack111ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ≺"): env.get(bstack111ll11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ≻")),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ≼"): env.get(bstack111ll11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ≽"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ≾")):
        return {
            bstack111ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≿"): bstack111ll11_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧ⊀"),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⊁"): env.get(bstack111ll11_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤ⊂")),
            bstack111ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⊃"): env.get(bstack111ll11_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣ⊄")),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⊅"): env.get(bstack111ll11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ⊆"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨ⊇")) or env.get(bstack111ll11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ⊈")):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⊉"): bstack111ll11_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤ⊊"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⊋"): env.get(bstack111ll11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ⊌")),
            bstack111ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⊍"): bstack111ll11_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧ⊎") if env.get(bstack111ll11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ⊏")) else None,
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⊐"): env.get(bstack111ll11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ⊑"))
        }
    if any([env.get(bstack111ll11_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ⊒")), env.get(bstack111ll11_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ⊓")), env.get(bstack111ll11_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ⊔"))]):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⊕"): bstack111ll11_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧ⊖"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⊗"): None,
            bstack111ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⊘"): env.get(bstack111ll11_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨ⊙")),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⊚"): env.get(bstack111ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⊛"))
        }
    if env.get(bstack111ll11_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣ⊜")):
        return {
            bstack111ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⊝"): bstack111ll11_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥ⊞"),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⊟"): env.get(bstack111ll11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ⊠")),
            bstack111ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⊡"): bstack111ll11_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧ⊢").format(env.get(bstack111ll11_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨ⊣"))) if env.get(bstack111ll11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤ⊤")) else None,
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⊥"): env.get(bstack111ll11_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ⊦"))
        }
    if bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥ⊧"))):
        return {
            bstack111ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ⊨"): bstack111ll11_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧ⊩"),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⊪"): env.get(bstack111ll11_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥ⊫")),
            bstack111ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⊬"): env.get(bstack111ll11_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦ⊭")),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⊮"): env.get(bstack111ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ⊯"))
        }
    if bstack1111l11lll_opy_(env.get(bstack111ll11_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧ⊰"))):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⊱"): bstack111ll11_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢ⊲"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⊳"): bstack111ll11_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤ⊴").format(env.get(bstack111ll11_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭⊵")), env.get(bstack111ll11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧ⊶")), env.get(bstack111ll11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫ⊷"))),
            bstack111ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⊸"): env.get(bstack111ll11_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣ⊹")),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⊺"): env.get(bstack111ll11_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣ⊻"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠤࡆࡍࠧ⊼")) == bstack111ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣ⊽") and env.get(bstack111ll11_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦ⊾")) == bstack111ll11_opy_ (u"ࠧ࠷ࠢ⊿"):
        return {
            bstack111ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⋀"): bstack111ll11_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢ⋁"),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⋂"): bstack111ll11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧ⋃").format(env.get(bstack111ll11_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧ⋄"))),
            bstack111ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⋅"): None,
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⋆"): None,
        }
    if env.get(bstack111ll11_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ⋇")):
        return {
            bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⋈"): bstack111ll11_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥ⋉"),
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⋊"): None,
            bstack111ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⋋"): env.get(bstack111ll11_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧ⋌")),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⋍"): env.get(bstack111ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ⋎"))
        }
    if any([env.get(bstack111ll11_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥ⋏")), env.get(bstack111ll11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣ⋐")), env.get(bstack111ll11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢ⋑")), env.get(bstack111ll11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦ⋒"))]):
        return {
            bstack111ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⋓"): bstack111ll11_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣ⋔"),
            bstack111ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⋕"): None,
            bstack111ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⋖"): env.get(bstack111ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ⋗")) or None,
            bstack111ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⋘"): env.get(bstack111ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ⋙"), 0)
        }
    if env.get(bstack111ll11_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ⋚")):
        return {
            bstack111ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⋛"): bstack111ll11_opy_ (u"ࠨࡇࡰࡅࡇࠦ⋜"),
            bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⋝"): None,
            bstack111ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⋞"): env.get(bstack111ll11_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ⋟")),
            bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⋠"): env.get(bstack111ll11_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ⋡"))
        }
    if env.get(bstack111ll11_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⋢")):
        return {
            bstack111ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⋣"): bstack111ll11_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥ⋤"),
            bstack111ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⋥"): env.get(bstack111ll11_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ⋦")),
            bstack111ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⋧"): env.get(bstack111ll11_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ⋨")),
            bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⋩"): env.get(bstack111ll11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⋪"))
        }
    return {bstack111ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⋫"): None}
def get_host_info():
    return {
        bstack111ll11_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥ⋬"): platform.node(),
        bstack111ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ⋭"): platform.system(),
        bstack111ll11_opy_ (u"ࠥࡸࡾࡶࡥࠣ⋮"): platform.machine(),
        bstack111ll11_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ⋯"): platform.version(),
        bstack111ll11_opy_ (u"ࠧࡧࡲࡤࡪࠥ⋰"): platform.architecture()[0]
    }
def bstack11l11lllll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1llll11lll11_opy_():
    if global_config.get_property(bstack111ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ⋱")):
        return bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⋲")
    return bstack111ll11_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧ⋳")
def bstack1ll1lll1lll_opy_(driver):
    info = {
        bstack111ll11_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ⋴"): driver.capabilities,
        bstack111ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧ⋵"): driver.session_id,
        bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ⋶"): driver.capabilities.get(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ⋷"), None),
        bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⋸"): driver.capabilities.get(bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⋹"), None),
        bstack111ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⋺"): driver.capabilities.get(bstack111ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ⋻"), None),
        bstack111ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⋼"):driver.capabilities.get(bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⋽"), None),
    }
    if bstack1llll11lll11_opy_() == bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⋾"):
        if bstack1lllllllll_opy_():
            info[bstack111ll11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ⋿")] = bstack111ll11_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⌀")
        elif driver.capabilities.get(bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⌁"), {}).get(bstack111ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⌂"), False):
            info[bstack111ll11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ⌃")] = bstack111ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⌄")
        else:
            info[bstack111ll11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭⌅")] = bstack111ll11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⌆")
    return info
def bstack1lllllllll_opy_():
    if global_config.get_property(bstack111ll11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⌇")):
        return True
    if bstack1111l11lll_opy_(os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ⌈"), None)):
        return True
    return False
_1llll1llll11_opy_ = re.compile(
    bstack111ll11_opy_ (u"ࡴࠪࠬࡡࡢ࠿ࠣࠪࡂ࠾ࠬ⌉") + bstack111ll11_opy_ (u"ࠪࢀࠬ⌊").join(re.escape(k) for k in bstack111111l11l1_opy_) + bstack111ll11_opy_ (u"ࡶࠬ࠯࡜࡝ࡁࠥࡠࡸ࠰࠺࡝ࡵ࠭ࡠࡡࡅࠢࠪࠪ࡞ࡢࠧࡢ࡜࡞ࠬࠬࠬࡡࡢ࠿ࠣࠫࠪ⌋"),
    re.IGNORECASE,
)
_1llll11l1l1l_opy_ = re.compile(
    bstack111ll11_opy_ (u"ࡷ࠭ࠨࠦ࠴࠵ࠬࡄࡀࠧ⌌") + bstack111ll11_opy_ (u"࠭ࡼࠨ⌍").join(re.escape(k) for k in bstack111111l11l1_opy_) + bstack111ll11_opy_ (u"ࡲࠨࠫࠨ࠶࠷ࠫ࠳ࡂࠪࡂ࠾ࠪ࠸࠰ࠪࡁࠨ࠶࠷࠯ࠨ࠯ࠬࡂ࠭࠭ࠫ࠲࠳ࠫࠪ⌎"),
    re.IGNORECASE,
)
def _1lllll1111ll_opy_(s):
    s = _1llll1llll11_opy_.sub(lambda m: m.group(1) + bstack111ll11_opy_ (u"ࠨࠬ࠭࠮࠯࠭⌏") + m.group(3), s)
    s = _1llll11l1l1l_opy_.sub(lambda m: m.group(1) + bstack111ll11_opy_ (u"ࠩ࠭࠮࠯࠰ࠧ⌐") + m.group(3), s)
    return s
def bstack1llll1l1l111_opy_(obj):
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if isinstance(v, str):
                obj[k] = _1lllll1111ll_opy_(v)
            else:
                bstack1llll1l1l111_opy_(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                obj[i] = _1lllll1111ll_opy_(v)
            else:
                bstack1llll1l1l111_opy_(v)
def bstack1llll11l1111_opy_(bstack1llll1111ll1_opy_, url, response, headers=None, data=None):
    bstack111ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡆࡺ࡯࡬ࡥࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦ࡬ࡰࡩࠣࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠴ࡸࡥࡴࡲࡲࡲࡸ࡫ࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡲࡷࡨࡷࡹࡥࡴࡺࡲࡨ࠾ࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦࠣࠬࡌࡋࡔ࠭ࠢࡓࡓࡘ࡚ࠬࠡࡧࡷࡧ࠳࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡷࡵࡰ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡖࡔࡏ࠳ࡪࡴࡤࡱࡱ࡬ࡲࡹࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡵࡢ࡫ࡧࡦࡸࠥ࡬ࡲࡰ࡯ࠣࡶࡪࡷࡵࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࡨࡦࡣࡧࡩࡷࡹ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢ࡫ࡩࡦࡪࡥࡳࡵࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡡࡵࡣ࠽ࠤࡗ࡫ࡱࡶࡧࡶࡸࠥࡐࡓࡐࡐࠣࡨࡦࡺࡡࠡࡱࡵࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡈࡲࡶࡲࡧࡴࡵࡧࡧࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦࠢࡺ࡭ࡹ࡮ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡥࡣࡷࡥࠏࠦࠠࠡࠢࠥࠦࠧ⌑")
    bstack1llllll11lll_opy_ = [k.lower() for k in bstack111111l11l1_opy_]
    bstack1lllll1lll1l_opy_ = None
    if isinstance(data, dict):
        bstack1lllll1lll1l_opy_ = data
        bstack1llll11111l1_opy_(bstack1lllll1lll1l_opy_, bstack1llllll11lll_opy_)
        bstack1llll1l1l111_opy_(bstack1lllll1lll1l_opy_)
    elif isinstance(data, list):
        bstack1lllll1lll1l_opy_ = data
        for item in bstack1lllll1lll1l_opy_:
            if isinstance(item, dict):
                bstack1llll11111l1_opy_(item, bstack1llllll11lll_opy_)
        bstack1llll1l1l111_opy_(bstack1lllll1lll1l_opy_)
    else:
        bstack1lllll1lll1l_opy_ = data
    bstack1llll111l11l_opy_ = None
    if isinstance(headers, dict):
        bstack1llll111l11l_opy_ = copy.deepcopy(headers)
        bstack1llll11111l1_opy_(bstack1llll111l11l_opy_, bstack1llllll11lll_opy_)
        bstack1llll1l1l111_opy_(bstack1llll111l11l_opy_)
    else:
        bstack1llll111l11l_opy_ = headers
    bstack1llll11l11l1_opy_ = {
        bstack111ll11_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ⌒"): bstack1llll111l11l_opy_,
        bstack111ll11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧ⌓"): bstack1llll1111ll1_opy_.upper(),
        bstack111ll11_opy_ (u"ࠨࡡࡨࡧࡱࡸࠧ⌔"): None,
        bstack111ll11_opy_ (u"ࠢࡦࡰࡧࡴࡴ࡯࡮ࡵࠤ⌕"): url,
        bstack111ll11_opy_ (u"ࠣ࡬ࡶࡳࡳࠨ⌖"): bstack1lllll1lll1l_opy_
    }
    try:
        bstack1lllll1llll1_opy_ = response.json()
        if isinstance(bstack1lllll1llll1_opy_, dict) and bstack1lllll1llll1_opy_.get(bstack111ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⌗"), {}).get(bstack111ll11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⌘"), {}).get(bstack111ll11_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ⌙")):
            bstack1llll1ll1l11_opy_ = json.loads(json.dumps(bstack1lllll1llll1_opy_))
            bstack1llll1ll1l11_opy_[bstack111ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⌚")][bstack111ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⌛")][bstack111ll11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ⌜")] = bstack111ll11_opy_ (u"ࠣ࡝ࡵࡩࡩࡧࡣࡵࡧࡧࠤ࡫ࡵࡲࠡࡤࡵࡩࡻ࡯ࡴࡺ࡟ࠥ⌝")
            bstack1lllll1llll1_opy_ = bstack1llll1ll1l11_opy_
        if isinstance(bstack1lllll1llll1_opy_, dict):
            bstack1llll11111l1_opy_(bstack1lllll1llll1_opy_, bstack1llllll11lll_opy_)
            bstack1llll1l1l111_opy_(bstack1lllll1llll1_opy_)
    except Exception:
        bstack1lllll1llll1_opy_ = response.text
    bstack1lllll1l111l_opy_ = {
        bstack111ll11_opy_ (u"ࠤࡥࡳࡩࡿࠢ⌞"): bstack1lllll1llll1_opy_,
        bstack111ll11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࡆࡳࡩ࡫ࠢ⌟"): response.status_code
    }
    return {
        bstack111ll11_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧ⌠"): bstack1llll11l11l1_opy_,
        bstack111ll11_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ⌡"): bstack1lllll1l111l_opy_
    }
def bstack111l1l1ll1_opy_(bstack1llll1111ll1_opy_, url, data, config):
    headers = config.get(bstack111ll11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ⌢"), None)
    proxies = bstack11l1ll1l_opy_(config, url)
    auth = config.get(bstack111ll11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ⌣"), None)
    response = requests.request(
            bstack1llll1111ll1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1llll11l1111_opy_(bstack1llll1111ll1_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack111ll11_opy_ (u"ࠨ࠮ࠪ⌤"), bstack111ll11_opy_ (u"ࠩ࠽ࠫ⌥"))))
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࡽࢀࠦ⌦").format(e))
    return response
def bstack1ll1l111l_opy_(bstack1lllll1ll1l_opy_, size):
    bstack1llll1ll1_opy_ = []
    while len(bstack1lllll1ll1l_opy_) > size:
        bstack1ll111ll1l_opy_ = bstack1lllll1ll1l_opy_[:size]
        bstack1llll1ll1_opy_.append(bstack1ll111ll1l_opy_)
        bstack1lllll1ll1l_opy_ = bstack1lllll1ll1l_opy_[size:]
    bstack1llll1ll1_opy_.append(bstack1lllll1ll1l_opy_)
    return bstack1llll1ll1_opy_
def bstack1llll1ll111l_opy_(message, bstack1llllll1111l_opy_=False):
    os.write(1, bytes(message, bstack111ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⌧")))
    os.write(1, bytes(bstack111ll11_opy_ (u"ࠬࡢ࡮ࠨ⌨"), bstack111ll11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ〈")))
    if bstack1llllll1111l_opy_:
        with open(bstack111ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭〉") + os.environ[bstack111ll11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ⌫")] + bstack111ll11_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ⌬"), bstack111ll11_opy_ (u"ࠪࡥࠬ⌭")) as f:
            f.write(message + bstack111ll11_opy_ (u"ࠫࡡࡴࠧ⌮"))
def bstack1l111llll1_opy_():
    return os.environ[bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ⌯")].lower() == bstack111ll11_opy_ (u"࠭ࡴࡳࡷࡨࠫ⌰")
def bstack1llllll1l11_opy_():
    return bstack1lll1l1l11l_opy_().replace(tzinfo=None).isoformat() + bstack111ll11_opy_ (u"࡛ࠧࠩ⌱")
def bstack1lll111l11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111ll11_opy_ (u"ࠨ࡜ࠪ⌲"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111ll11_opy_ (u"ࠩ࡝ࠫ⌳")))).total_seconds() * 1000
def bstack1llll1l1111l_opy_(timestamp):
    return bstack1llll1ll1ll1_opy_(timestamp).isoformat() + bstack111ll11_opy_ (u"ࠪ࡞ࠬ⌴")
def bstack1lllll1111l1_opy_(bstack1lllll111lll_opy_):
    date_format = bstack111ll11_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩ⌵")
    bstack1llll1l111ll_opy_ = datetime.datetime.strptime(bstack1lllll111lll_opy_, date_format)
    return bstack1llll1l111ll_opy_.isoformat() + bstack111ll11_opy_ (u"ࠬࡠࠧ⌶")
def bstack1llll1l11lll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⌷")
    else:
        return bstack111ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⌸")
def bstack1111l11lll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭⌹")
def bstack1llll11l1ll1_opy_(val):
    return val.__str__().lower() == bstack111ll11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ⌺")
def error_handler(bstack1llll1l1ll1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1llll1l1ll1l_opy_ as e:
                print(bstack111ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ⌻").format(func.__name__, bstack1llll1l1ll1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1lllll11l1ll_opy_(bstack1lll1llll111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1lll1llll111_opy_(cls, *args, **kwargs)
            except bstack1llll1l1ll1l_opy_ as e:
                print(bstack111ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦ⌼").format(bstack1lll1llll111_opy_.__name__, bstack1llll1l1ll1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1lllll11l1ll_opy_
    else:
        return decorator
def bstack11lll11l11_opy_(bstack1lllll111l1_opy_):
    if os.getenv(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ⌽")) is not None:
        return bstack1111l11lll_opy_(os.getenv(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ⌾")))
    if bstack111ll11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⌿") in bstack1lllll111l1_opy_ and bstack1llll11l1ll1_opy_(bstack1lllll111l1_opy_[bstack111ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⍀")]):
        return False
    if bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⍁") in bstack1lllll111l1_opy_ and bstack1llll11l1ll1_opy_(bstack1lllll111l1_opy_[bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⍂")]):
        return False
    return True
def bstack1ll1l1llll_opy_():
    try:
        from pytest_bdd import reporting
        bstack1lllll1l1lll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦ⍃"), None)
        return bstack1lllll1l1lll_opy_ is None or bstack1lllll1l1lll_opy_ == bstack111ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ⍄")
    except Exception as e:
        return False
def bstack11llll11_opy_(hub_url, CONFIG):
    if bstack11lll1l11_opy_() <= version.parse(bstack111ll11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭⍅")):
        if hub_url:
            return bstack111ll11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⍆") + hub_url + bstack111ll11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ⍇")
        return bstack1l1llll1l1_opy_
    if hub_url:
        return bstack111ll11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ⍈") + hub_url + bstack111ll11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ⍉")
    return bstack11lll111ll_opy_
def bstack1llllll111ll_opy_():
    return isinstance(os.getenv(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ⍊")), str)
def bstack1111lll11_opy_(url):
    return urlparse(url).hostname
def bstack11lll1l1l1_opy_(hostname):
    for bstack1l11ll1ll_opy_ in bstack111llllll_opy_:
        regex = re.compile(bstack1l11ll1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1llll1lll111_opy_(bstack1llll11lll1l_opy_, file_name, logger):
    bstack11l11lll1l_opy_ = os.path.join(os.path.expanduser(bstack111ll11_opy_ (u"ࠬࢄࠧ⍋")), bstack1llll11lll1l_opy_)
    try:
        if not os.path.exists(bstack11l11lll1l_opy_):
            os.makedirs(bstack11l11lll1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111ll11_opy_ (u"࠭ࡾࠨ⍌")), bstack1llll11lll1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111ll11_opy_ (u"ࠧࡸࠩ⍍")):
                pass
            with open(file_path, bstack111ll11_opy_ (u"ࠣࡹ࠮ࠦ⍎")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111111l1l1_opy_.format(str(e)))
def bstack1llll1lll11l_opy_(file_name, key, value, logger):
    file_path = bstack1llll1lll111_opy_(bstack111ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⍏"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack111l1l11_opy_ = json.load(open(file_path, bstack111ll11_opy_ (u"ࠪࡶࡧ࠭⍐")))
        else:
            bstack111l1l11_opy_ = {}
        bstack111l1l11_opy_[key] = value
        with open(file_path, bstack111ll11_opy_ (u"ࠦࡼ࠱ࠢ⍑")) as outfile:
            json.dump(bstack111l1l11_opy_, outfile)
def bstack1lllllll1l1_opy_(file_name, logger):
    file_path = bstack1llll1lll111_opy_(bstack111ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⍒"), file_name, logger)
    bstack111l1l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111ll11_opy_ (u"࠭ࡲࠨ⍓")) as bstack1l11ll111l_opy_:
            bstack111l1l11_opy_ = json.load(bstack1l11ll111l_opy_)
    return bstack111l1l11_opy_
def bstack1lll1111l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫ⍔") + file_path + bstack111ll11_opy_ (u"ࠨࠢࠪ⍕") + str(e))
def bstack11lll1l11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111ll11_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦ⍖")
def bstack1l1l1l11ll_opy_(config):
    if bstack111ll11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ⍗") in config:
        del (config[bstack111ll11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ⍘")])
        return False
    if bstack11lll1l11_opy_() < version.parse(bstack111ll11_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫ⍙")):
        return False
    if bstack11lll1l11_opy_() >= version.parse(bstack111ll11_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬ⍚")):
        return True
    if bstack111ll11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ⍛") in config and config[bstack111ll11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ⍜")] is False:
        return False
    else:
        return True
def bstack1l11l1ll1_opy_(args_list, bstack1llll1l111l1_opy_):
    index = -1
    for value in bstack1llll1l111l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack1111ll11l11_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack1111ll11l11_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llll111lll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llll111lll_opy_ = bstack1llll111lll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⍝"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⍞"), exception=exception)
    def bstack1ll111l1l1l_opy_(self):
        if self.result != bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⍟"):
            return None
        if isinstance(self.exception_type, str) and bstack111ll11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ⍠") in self.exception_type:
            return bstack111ll11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ⍡")
        return bstack111ll11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ⍢")
    def bstack1llllll1ll11_opy_(self):
        if self.result != bstack111ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⍣"):
            return None
        if self.bstack1llll111lll_opy_:
            return self.bstack1llll111lll_opy_
        return bstack1llll1lll1ll_opy_(self.exception)
def bstack1llll1lll1ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1lllll1l11l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111lll1ll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11ll11l1l_opy_(config, logger):
    try:
        import playwright
        bstack1llll1llll1l_opy_ = playwright.__file__
        bstack1lllll11l1l1_opy_ = os.path.split(bstack1llll1llll1l_opy_)
        bstack1lllll11111l_opy_ = bstack1lllll11l1l1_opy_[0] + bstack111ll11_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬ⍤")
        os.environ[bstack111ll11_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭⍥")] = bstack1ll11111l_opy_(config)
        with open(bstack1lllll11111l_opy_, bstack111ll11_opy_ (u"ࠫࡷ࠭⍦")) as f:
            file_content = f.read()
            bstack1lllll1l1111_opy_ = bstack111ll11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ⍧")
            bstack1llll11l1l11_opy_ = file_content.find(bstack1lllll1l1111_opy_)
            if bstack1llll11l1l11_opy_ == -1:
              process = subprocess.Popen(bstack111ll11_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥ⍨"), shell=True, cwd=bstack1lllll11l1l1_opy_[0])
              process.wait()
              bstack1llll1111lll_opy_ = bstack111ll11_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧ⍩")
              bstack1lllll111111_opy_ = bstack111ll11_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧ⍪")
              bstack1llll1l11ll1_opy_ = file_content.replace(bstack1llll1111lll_opy_, bstack1lllll111111_opy_)
              with open(bstack1lllll11111l_opy_, bstack111ll11_opy_ (u"ࠩࡺࠫ⍫")) as f:
                f.write(bstack1llll1l11ll1_opy_)
    except Exception as e:
        logger.error(bstack1lllllllll1_opy_.format(str(e)))
def bstack1l11l11ll1_opy_():
  try:
    bstack1lllll11lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ⍬"))
    bstack1lll1llll11l_opy_ = []
    if os.path.exists(bstack1lllll11lll1_opy_):
      with open(bstack1lllll11lll1_opy_) as f:
        bstack1lll1llll11l_opy_ = json.load(f)
      os.remove(bstack1lllll11lll1_opy_)
    return bstack1lll1llll11l_opy_
  except:
    pass
  return []
def bstack1111llllll_opy_(bstack1l1l1l1lll_opy_):
  try:
    bstack1lll1llll11l_opy_ = []
    bstack1lllll11lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ⍭"))
    if os.path.exists(bstack1lllll11lll1_opy_):
      with open(bstack1lllll11lll1_opy_) as f:
        bstack1lll1llll11l_opy_ = json.load(f)
    bstack1lll1llll11l_opy_.append(bstack1l1l1l1lll_opy_)
    with open(bstack1lllll11lll1_opy_, bstack111ll11_opy_ (u"ࠬࡽࠧ⍮")) as f:
        json.dump(bstack1lll1llll11l_opy_, f)
  except:
    pass
def bstack11llllllll_opy_(logger, bstack1llllll1l11l_opy_ = False):
  try:
    test_name = os.environ.get(bstack111ll11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⍯"), bstack111ll11_opy_ (u"ࠧࠨ⍰"))
    if test_name == bstack111ll11_opy_ (u"ࠨࠩ⍱"):
        test_name = threading.current_thread().__dict__.get(bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨ⍲"), bstack111ll11_opy_ (u"ࠪࠫ⍳"))
    bstack1lll1lllllll_opy_ = bstack111ll11_opy_ (u"ࠫ࠱ࠦࠧ⍴").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1llllll1l11l_opy_:
        bstack1l1ll11l1l_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⍵"), bstack111ll11_opy_ (u"࠭࠰ࠨ⍶"))
        bstack1llll1111l_opy_ = {bstack111ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⍷"): test_name, bstack111ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⍸"): bstack1lll1lllllll_opy_, bstack111ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ⍹"): bstack1l1ll11l1l_opy_}
        bstack1lll1llll1l1_opy_ = []
        bstack1lllllll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⍺"))
        if os.path.exists(bstack1lllllll11l1_opy_):
            with open(bstack1lllllll11l1_opy_) as f:
                bstack1lll1llll1l1_opy_ = json.load(f)
        bstack1lll1llll1l1_opy_.append(bstack1llll1111l_opy_)
        with open(bstack1lllllll11l1_opy_, bstack111ll11_opy_ (u"ࠫࡼ࠭⍻")) as f:
            json.dump(bstack1lll1llll1l1_opy_, f)
    else:
        bstack1llll1111l_opy_ = {bstack111ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⍼"): test_name, bstack111ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⍽"): bstack1lll1lllllll_opy_, bstack111ll11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⍾"): str(multiprocessing.current_process().name)}
        if bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ⍿") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1llll1111l_opy_)
  except Exception as e:
      logger.warn(bstack111ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⎀").format(e))
def bstack1l1111ll1l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111ll11_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭⎁"))
    try:
      bstack1llll111ll1l_opy_ = []
      bstack1llll1111l_opy_ = {bstack111ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⎂"): test_name, bstack111ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⎃"): error_message, bstack111ll11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⎄"): index}
      bstack1llll1l1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⎅"))
      if os.path.exists(bstack1llll1l1l1l1_opy_):
          with open(bstack1llll1l1l1l1_opy_) as f:
              bstack1llll111ll1l_opy_ = json.load(f)
      bstack1llll111ll1l_opy_.append(bstack1llll1111l_opy_)
      with open(bstack1llll1l1l1l1_opy_, bstack111ll11_opy_ (u"ࠨࡹࠪ⎆")) as f:
          json.dump(bstack1llll111ll1l_opy_, f)
    except Exception as e:
      logger.warn(bstack111ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ⎇").format(e))
    return
  bstack1llll111ll1l_opy_ = []
  bstack1llll1111l_opy_ = {bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⎈"): test_name, bstack111ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⎉"): error_message, bstack111ll11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ⎊"): index}
  bstack1llll1l1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ⎋"))
  lock_file = bstack1llll1l1l1l1_opy_ + bstack111ll11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭⎌")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1llll1l1l1l1_opy_):
          with open(bstack1llll1l1l1l1_opy_, bstack111ll11_opy_ (u"ࠨࡴࠪ⎍")) as f:
              content = f.read().strip()
              if content:
                  bstack1llll111ll1l_opy_ = json.load(open(bstack1llll1l1l1l1_opy_))
      bstack1llll111ll1l_opy_.append(bstack1llll1111l_opy_)
      with open(bstack1llll1l1l1l1_opy_, bstack111ll11_opy_ (u"ࠩࡺࠫ⎎")) as f:
          json.dump(bstack1llll111ll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack111ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࡀࠠࡼࡿࠥ⎏").format(e))
def bstack11llll1111_opy_(bstack1ll1ll111l_opy_, name, logger):
  try:
    bstack1llll1111l_opy_ = {bstack111ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⎐"): name, bstack111ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⎑"): bstack1ll1ll111l_opy_, bstack111ll11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⎒"): str(threading.current_thread()._name)}
    return bstack1llll1111l_opy_
  except Exception as e:
    logger.warn(bstack111ll11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡥࡩ࡭ࡧࡶࡦࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ⎓").format(e))
  return
def bstack1lllll111ll1_opy_():
    return platform.system() == bstack111ll11_opy_ (u"ࠨ࡙࡬ࡲࡩࡵࡷࡴࠩ⎔")
def bstack1ll111ll_opy_(bstack1llllll1ll1l_opy_, config, logger):
    bstack1lllll11llll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1llllll1ll1l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡭ࡶࡨࡶࠥࡩ࡯࡯ࡨ࡬࡫ࠥࡱࡥࡺࡵࠣࡦࡾࠦࡲࡦࡩࡨࡼࠥࡳࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⎕").format(e))
    return bstack1lllll11llll_opy_
def bstack1llllll111l1_opy_(bstack1lllll11ll1l_opy_, bstack1lllll111l11_opy_):
    bstack1llllll11l1l_opy_ = version.parse(bstack1lllll11ll1l_opy_)
    bstack1lllll111l1l_opy_ = version.parse(bstack1lllll111l11_opy_)
    if bstack1llllll11l1l_opy_ > bstack1lllll111l1l_opy_:
        return 1
    elif bstack1llllll11l1l_opy_ < bstack1lllll111l1l_opy_:
        return -1
    else:
        return 0
def bstack1lll1l1l11l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll1ll1ll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll1ll1111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11l1l111ll_opy_(options, framework, config, bstack11l11l11ll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack111ll11_opy_ (u"ࠪ࡫ࡪࡺࠧ⎖"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack111l1lll_opy_ = caps.get(bstack111ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⎗"))
    bstack1llll111l1ll_opy_ = True
    bstack1111ll11l1_opy_ = os.environ[bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⎘")]
    bstack1l111l11ll1_opy_ = config.get(bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⎙"), False)
    if bstack1l111l11ll1_opy_:
        bstack1l111lllll1_opy_ = config.get(bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⎚"), {})
        bstack1l111lllll1_opy_[bstack111ll11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ⎛")] = os.getenv(bstack111ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⎜"))
        bstack1l1ll111ll_opy_ = json.loads(os.getenv(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⎝"), bstack111ll11_opy_ (u"ࠫࢀࢃࠧ⎞"))).get(bstack111ll11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⎟"))
    if bstack1llll11l1ll1_opy_(caps.get(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦ࡙࠶ࡇࠬ⎠"))) or bstack1llll11l1ll1_opy_(caps.get(bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧ⎡"))):
        bstack1llll111l1ll_opy_ = False
    if bstack1l1l1l11ll_opy_({bstack111ll11_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ⎢"): bstack1llll111l1ll_opy_}):
        bstack111l1lll_opy_ = bstack111l1lll_opy_ or {}
        bstack111l1lll_opy_[bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⎣")] = bstack1llll1ll1111_opy_(framework)
        bstack111l1lll_opy_[bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⎤")] = bstack1l111llll1_opy_()
        bstack111l1lll_opy_[bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ⎥")] = bstack1111ll11l1_opy_
        bstack111l1lll_opy_[bstack111ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ⎦")] = bstack11l11l11ll_opy_
        if bstack1l111l11ll1_opy_:
            bstack111l1lll_opy_[bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⎧")] = bstack1l111l11ll1_opy_
            bstack111l1lll_opy_[bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⎨")] = bstack1l111lllll1_opy_
            bstack111l1lll_opy_[bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⎩")][bstack111ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⎪")] = bstack1l1ll111ll_opy_
        if getattr(options, bstack111ll11_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ⎫"), None):
            options.set_capability(bstack111ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⎬"), bstack111l1lll_opy_)
        else:
            options[bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⎭")] = bstack111l1lll_opy_
    else:
        if getattr(options, bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧ⎮"), None):
            options.set_capability(bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⎯"), bstack1llll1ll1111_opy_(framework))
            options.set_capability(bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⎰"), bstack1l111llll1_opy_())
            options.set_capability(bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⎱"), bstack1111ll11l1_opy_)
            options.set_capability(bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ⎲"), bstack11l11l11ll_opy_)
            if bstack1l111l11ll1_opy_:
                options.set_capability(bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⎳"), bstack1l111l11ll1_opy_)
                options.set_capability(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⎴"), bstack1l111lllll1_opy_)
                options.set_capability(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ࠳ࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⎵"), bstack1l1ll111ll_opy_)
        else:
            options[bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⎶")] = bstack1llll1ll1111_opy_(framework)
            options[bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⎷")] = bstack1l111llll1_opy_()
            options[bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⎸")] = bstack1111ll11l1_opy_
            options[bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ⎹")] = bstack11l11l11ll_opy_
            if bstack1l111l11ll1_opy_:
                options[bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⎺")] = bstack1l111l11ll1_opy_
                options[bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⎻")] = bstack1l111lllll1_opy_
                options[bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⎼")][bstack111ll11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⎽")] = bstack1l1ll111ll_opy_
    return options
def bstack1llll1111l11_opy_(ws_endpoint, framework):
    bstack11l11l11ll_opy_ = global_config.get_property(bstack111ll11_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥ⎾"))
    if ws_endpoint and len(ws_endpoint.split(bstack111ll11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ⎿"))) > 1:
        ws_url = ws_endpoint.split(bstack111ll11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ⏀"))[0]
        if bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ⏁") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1lllll1l1ll1_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack111ll11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ⏂"))[1]))
            bstack1lllll1l1ll1_opy_ = bstack1lllll1l1ll1_opy_ or {}
            bstack1111ll11l1_opy_ = os.environ[bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⏃")]
            bstack1lllll1l1ll1_opy_[bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⏄")] = str(framework) + str(__version__)
            bstack1lllll1l1ll1_opy_[bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⏅")] = bstack1l111llll1_opy_()
            bstack1lllll1l1ll1_opy_[bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⏆")] = bstack1111ll11l1_opy_
            bstack1lllll1l1ll1_opy_[bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ⏇")] = bstack11l11l11ll_opy_
            ws_endpoint = ws_endpoint.split(bstack111ll11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ⏈"))[0] + bstack111ll11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ⏉") + urllib.parse.quote(json.dumps(bstack1lllll1l1ll1_opy_))
    return ws_endpoint
def bstack1ll1l1l1_opy_():
    global bstack11llll111_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11llll111_opy_ = BrowserType.connect
    return bstack11llll111_opy_
def bstack1lllll11l111_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1l11l1l1l_opy_(self, *args, **kwargs):
    global bstack11llll111_opy_
    try:
        global FRAMEWORK_NAME
        if bstack111ll11_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪ⏊") in kwargs:
            kwargs[bstack111ll11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ⏋")] = bstack1llll1111l11_opy_(
                kwargs.get(bstack111ll11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ⏌"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack111ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤ⏍").format(str(e)))
    return bstack11llll111_opy_(self, *args, **kwargs)
def bstack1llllll11111_opy_(bstack1llll111l1l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l1ll1l_opy_(bstack1llll111l1l1_opy_, bstack111ll11_opy_ (u"ࠥࠦ⏎"))
        if proxies and proxies.get(bstack111ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ⏏")):
            parsed_url = urlparse(proxies.get(bstack111ll11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ⏐")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack111ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩ⏑")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack111ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪ⏒")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack111ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ⏓")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack111ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ⏔")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack111111l11_opy_(bstack1llll111l1l1_opy_):
    bstack1llll11l11ll_opy_ = {
        bstack11111l1l1ll_opy_[bstack1llll1111l1l_opy_]: bstack1llll111l1l1_opy_[bstack1llll1111l1l_opy_]
        for bstack1llll1111l1l_opy_ in bstack1llll111l1l1_opy_
        if bstack1llll1111l1l_opy_ in bstack11111l1l1ll_opy_
    }
    bstack1llll11l11ll_opy_[bstack111ll11_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥ⏕")] = bstack1llllll11111_opy_(bstack1llll111l1l1_opy_, global_config.get_property(bstack111ll11_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦ⏖")))
    bstack1lllll1ll1l1_opy_ = [element.lower() for element in bstack111111l11l1_opy_]
    bstack1llll11111l1_opy_(bstack1llll11l11ll_opy_, bstack1lllll1ll1l1_opy_)
    return bstack1llll11l11ll_opy_
def bstack1llll11111l1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack111ll11_opy_ (u"ࠧ࠰ࠪࠫࠬࠥ⏗")
    for value in d.values():
        if isinstance(value, dict):
            bstack1llll11111l1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1llll11111l1_opy_(item, keys)
def bstack11ll1lll1ll_opy_():
    bstack1lll1lllll1l_opy_ = [os.environ.get(bstack111ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣ⏘")), os.path.join(os.path.expanduser(bstack111ll11_opy_ (u"ࠢࡿࠤ⏙")), bstack111ll11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⏚")), os.path.join(bstack111ll11_opy_ (u"ࠩ࠲ࡸࡲࡶࠧ⏛"), bstack111ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⏜"))]
    for path in bstack1lll1lllll1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack111ll11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦ⏝") + str(path) + bstack111ll11_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣ⏞"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack111ll11_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥ⏟") + str(path) + bstack111ll11_opy_ (u"ࠢࠨࠤ⏠"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack111ll11_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣ⏡") + str(path) + bstack111ll11_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢ⏢"))
            else:
                logger.debug(bstack111ll11_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧ⏣") + str(path) + bstack111ll11_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣ⏤"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack111ll11_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥ⏥") + str(path) + bstack111ll11_opy_ (u"ࠨࠧ࠯ࠤ⏦"))
            return path
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧ⏧") + str(e) + bstack111ll11_opy_ (u"ࠣࠤ⏨"))
    logger.debug(bstack111ll11_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨ⏩"))
    return None
@measure(event_name=EVENTS.bstack11111l11111_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
def bstack1ll1l111l1l_opy_(binary_path, bstack1ll1l11l1l1_opy_, bs_config):
    logger.debug(bstack111ll11_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤ⏪").format(binary_path))
    bstack1llll11ll11l_opy_ = bstack111ll11_opy_ (u"ࠫࠬ⏫")
    bstack1llll1l11111_opy_ = {
        bstack111ll11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⏬"): __version__,
        bstack111ll11_opy_ (u"ࠨ࡯ࡴࠤ⏭"): platform.system(),
        bstack111ll11_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣ⏮"): platform.machine(),
        bstack111ll11_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ⏯"): bstack111ll11_opy_ (u"ࠩ࠳ࠫ⏰"),
        bstack111ll11_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤ⏱"): bstack111ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⏲")
    }
    bstack1lllllll11ll_opy_(bstack1llll1l11111_opy_)
    try:
        if binary_path:
            if bstack1lllll111ll1_opy_():
                bstack1llll1l11111_opy_[bstack111ll11_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ⏳")] = subprocess.check_output([binary_path, bstack111ll11_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ⏴")]).strip().decode(bstack111ll11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭⏵"))
            else:
                bstack1llll1l11111_opy_[bstack111ll11_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⏶")] = subprocess.check_output([binary_path, bstack111ll11_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥ⏷")], stderr=subprocess.DEVNULL).strip().decode(bstack111ll11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⏸"))
        response = requests.request(
            bstack111ll11_opy_ (u"ࠫࡌࡋࡔࠨ⏹"),
            url=bstack11111l1ll_opy_(bstack11111l1111l_opy_),
            headers=None,
            auth=(bs_config[bstack111ll11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ⏺")], bs_config[bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ⏻")]),
            json=None,
            params=bstack1llll1l11111_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack111ll11_opy_ (u"ࠧࡶࡴ࡯ࠫ⏼") in data.keys() and bstack111ll11_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥࡡࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⏽") in data.keys():
            logger.debug(bstack111ll11_opy_ (u"ࠤࡑࡩࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡦ࡮ࡴࡡࡳࡻ࠯ࠤࡨࡻࡲࡳࡧࡱࡸࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥ⏾").format(bstack1llll1l11111_opy_[bstack111ll11_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⏿")]))
            if bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧ␀") in os.environ:
                logger.debug(bstack111ll11_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡤࡷࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠡ࡫ࡶࠤࡸ࡫ࡴࠣ␁"))
                data[bstack111ll11_opy_ (u"࠭ࡵࡳ࡮ࠪ␂")] = os.environ[bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪ␃")]
            bstack1lllll1ll1ll_opy_ = bstack1llll1l1llll_opy_(data[bstack111ll11_opy_ (u"ࠨࡷࡵࡰࠬ␄")], bstack1ll1l11l1l1_opy_)
            bstack1llll11ll11l_opy_ = os.path.join(bstack1ll1l11l1l1_opy_, bstack1lllll1ll1ll_opy_)
            os.chmod(bstack1llll11ll11l_opy_, 0o777) # bstack1llllll11l11_opy_ permission
            return bstack1llll11ll11l_opy_
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡖࡈࡐࠦࡻࡾࠤ␅").format(e))
    return binary_path
def bstack1lllllll11ll_opy_(bstack1llll1l11111_opy_):
    try:
        if bstack111ll11_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩ␆") not in bstack1llll1l11111_opy_[bstack111ll11_opy_ (u"ࠫࡴࡹࠧ␇")].lower():
            return
        if os.path.exists(bstack111ll11_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ␈")):
            with open(bstack111ll11_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ␉"), bstack111ll11_opy_ (u"ࠢࡳࠤ␊")) as f:
                bstack1llll1l1l11l_opy_ = {}
                for line in f:
                    if bstack111ll11_opy_ (u"ࠣ࠿ࠥ␋") in line:
                        key, value = line.rstrip().split(bstack111ll11_opy_ (u"ࠤࡀࠦ␌"), 1)
                        bstack1llll1l1l11l_opy_[key] = value.strip(bstack111ll11_opy_ (u"ࠪࠦࡡ࠭ࠧ␍"))
                bstack1llll1l11111_opy_[bstack111ll11_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫ␎")] = bstack1llll1l1l11l_opy_.get(bstack111ll11_opy_ (u"ࠧࡏࡄࠣ␏"), bstack111ll11_opy_ (u"ࠨࠢ␐"))
        elif os.path.exists(bstack111ll11_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡧ࡬ࡱ࡫ࡱࡩ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ␑")):
            bstack1llll1l11111_opy_[bstack111ll11_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨ␒")] = bstack111ll11_opy_ (u"ࠩࡤࡰࡵ࡯࡮ࡦࠩ␓")
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡨ࡮ࡹࡴࡳࡱࠣࡳ࡫ࠦ࡬ࡪࡰࡸࡼࠧ␔") + e)
@measure(event_name=EVENTS.bstack1111111l1ll_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
def bstack1llll1l1llll_opy_(bstack1llll1l11l1l_opy_, bstack1lllll11ll11_opy_):
    logger.debug(bstack111ll11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰ࠾ࠥࠨ␕") + str(bstack1llll1l11l1l_opy_) + bstack111ll11_opy_ (u"ࠧࠨ␖"))
    zip_path = os.path.join(bstack1lllll11ll11_opy_, bstack111ll11_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡢࡪ࡮ࡲࡥ࠯ࡼ࡬ࡴࠧ␗"))
    bstack1lllll1ll1ll_opy_ = bstack111ll11_opy_ (u"ࠧࠨ␘")
    with requests.get(bstack1llll1l11l1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack111ll11_opy_ (u"ࠣࡹࡥࠦ␙")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack111ll11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠦ␚"))
    with zipfile.ZipFile(zip_path, bstack111ll11_opy_ (u"ࠪࡶࠬ␛")) as zip_ref:
        bstack1llll11ll1l1_opy_ = zip_ref.namelist()
        if len(bstack1llll11ll1l1_opy_) > 0:
            bstack1lllll1ll1ll_opy_ = bstack1llll11ll1l1_opy_[0] # bstack1llll1ll11l1_opy_ bstack11111l111l1_opy_ will be bstack1llll11llll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1lllll11ll11_opy_)
        logger.debug(bstack111ll11_opy_ (u"ࠦࡋ࡯࡬ࡦࡵࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡨࡼࡹࡸࡡࡤࡶࡨࡨࠥࡺ࡯ࠡࠩࠥ␜") + str(bstack1lllll11ll11_opy_) + bstack111ll11_opy_ (u"ࠧ࠭ࠢ␝"))
    os.remove(zip_path)
    return bstack1lllll1ll1ll_opy_
def get_cli_dir():
    bstack1llll1lll1l1_opy_ = bstack11ll1lll1ll_opy_()
    if bstack1llll1lll1l1_opy_:
        bstack1ll1l11l1l1_opy_ = os.path.join(bstack1llll1lll1l1_opy_, bstack111ll11_opy_ (u"ࠨࡣ࡭࡫ࠥ␞"))
        if not os.path.exists(bstack1ll1l11l1l1_opy_):
            os.makedirs(bstack1ll1l11l1l1_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l11l1l1_opy_
    else:
        raise FileNotFoundError(bstack111ll11_opy_ (u"ࠢࡏࡱࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠥ␟"))
def bstack1ll1l11l11l_opy_(bstack1ll1l11l1l1_opy_):
    bstack111ll11_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡩ࡯ࠢࡤࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠥࠦࠧ␠")
    bstack1lll1llll1ll_opy_ = [
        os.path.join(bstack1ll1l11l1l1_opy_, f)
        for f in os.listdir(bstack1ll1l11l1l1_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l11l1l1_opy_, f)) and f.startswith(bstack111ll11_opy_ (u"ࠤࡥ࡭ࡳࡧࡲࡺ࠯ࠥ␡"))
    ]
    if len(bstack1lll1llll1ll_opy_) > 0:
        return max(bstack1lll1llll1ll_opy_, key=os.path.getmtime) # get bstack1llll111llll_opy_ binary
    return bstack111ll11_opy_ (u"ࠥࠦ␢")
def bstack1111l1lll11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11111ll1l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l11111ll1l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11ll1lll11_opy_(data, keys, default=None):
    bstack111ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡧࡦࡦ࡮ࡼࠤ࡬࡫ࡴࠡࡣࠣࡲࡪࡹࡴࡦࡦࠣࡺࡦࡲࡵࡦࠢࡩࡶࡴࡳࠠࡢࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡡࡵࡣ࠽ࠤ࡙࡮ࡥࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹࠦࡴࡰࠢࡷࡶࡦࡼࡥࡳࡵࡨ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢ࡮ࡩࡾࡹ࠺ࠡࡃࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡰ࡫ࡹࡴ࠱࡬ࡲࡩ࡯ࡣࡦࡵࠣࡶࡪࡶࡲࡦࡵࡨࡲࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡩ࡫ࡧࡵ࡭ࡶ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡸࡴࠦࡲࡦࡶࡸࡶࡳࠦࡩࡧࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡷ࡫ࡴࡶࡴࡱ࠾࡚ࠥࡨࡦࠢࡹࡥࡱࡻࡥࠡࡣࡷࠤࡹ࡮ࡥࠡࡰࡨࡷࡹ࡫ࡤࠡࡲࡤࡸ࡭࠲ࠠࡰࡴࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤ࡮࡬ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ␣")
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
def bstack1l1llll1ll_opy_(bstack1llll1ll1l1l_opy_, key, value):
    bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡴࡰࡴࡨࠤࡈࡒࡉࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴࠢࡰࡥࡵࡶࡩ࡯ࡩࠣ࡭ࡳࠦࡴࡩࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤ࡮࡬ࡣࡪࡴࡶࡠࡸࡤࡶࡸࡥ࡭ࡢࡲ࠽ࠤࡉ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣࡱࡦࡶࡰࡪࡰࡪࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡫ࡦࡻ࠽ࠤࡐ࡫ࡹࠡࡨࡵࡳࡲࠦࡃࡍࡋࡢࡇࡆࡖࡓࡠࡖࡒࡣࡈࡕࡎࡇࡋࡊࠎࠥࠦࠠࠡࠢࠣࠤࠥࡼࡡ࡭ࡷࡨ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡰ࡮ࡴࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠎࠥࠦࠠࠡࠤࠥࠦ␤")
    if key in bstack111l11l111_opy_:
        bstack11111l1l1_opy_ = bstack111l11l111_opy_[key]
        if isinstance(bstack11111l1l1_opy_, list):
            for env_name in bstack11111l1l1_opy_:
                bstack1llll1ll1l1l_opy_[env_name] = value
        else:
            bstack1llll1ll1l1l_opy_[bstack11111l1l1_opy_] = value