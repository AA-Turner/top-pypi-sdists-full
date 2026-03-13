# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
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
from math import ceil
from unittest import result
import urllib
from urllib.parse import urlparse
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l111l111_opy_, bstack11l1l111l1_opy_, HTTPS_HUB,
                                    bstack111l1l1111l_opy_, bstack111l1ll11l1_opy_, bstack111l1l1l11l_opy_, bstack111l1l111ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1lllll_opy_, bstack111l1lllll_opy_
from bstack_utils.proxy import bstack1l1l111l11_opy_, bstack11ll1lllll_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1lll111l_opy_ import bstack11lll1ll_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack111lll1ll11_opy_(config):
    return config[bstack1111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ἗")]
def bstack111lll11lll_opy_(config):
    return config[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫἘ")]
def bstack1l1l1l1l11_opy_():
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
def bstack1111l11llll_opy_(obj):
    values = []
    bstack1111lll1lll_opy_ = re.compile(bstack1111l_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨἙ"), re.I)
    for key in obj.keys():
        if bstack1111lll1lll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11111llllll_opy_(config):
    tags = []
    tags.extend(bstack1111l11llll_opy_(os.environ))
    tags.extend(bstack1111l11llll_opy_(config))
    return tags
def bstack1111l1l1ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111ll11l11_opy_(bstack11111l111ll_opy_):
    if not bstack11111l111ll_opy_:
        return bstack1111l_opy_ (u"ࠪࠫἚ")
    return bstack1111l_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧἛ").format(bstack11111l111ll_opy_.name, bstack11111l111ll_opy_.email)
def bstack111llll11ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l11111l1_opy_ = repo.common_dir
        info = {
            bstack1111l_opy_ (u"ࠧࡹࡨࡢࠤἜ"): repo.head.commit.hexsha,
            bstack1111l_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤἝ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1111l_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢ἞"): repo.active_branch.name,
            bstack1111l_opy_ (u"ࠣࡶࡤ࡫ࠧ἟"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1111l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧἠ"): bstack1111ll11l11_opy_(repo.head.commit.committer),
            bstack1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦἡ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1111l_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦἢ"): bstack1111ll11l11_opy_(repo.head.commit.author),
            bstack1111l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥἣ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1111l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢἤ"): repo.head.commit.message,
            bstack1111l_opy_ (u"ࠢࡳࡱࡲࡸࠧἥ"): repo.git.rev_parse(bstack1111l_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥἦ")),
            bstack1111l_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥἧ"): bstack111l11111l1_opy_,
            bstack1111l_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨἨ"): subprocess.check_output([bstack1111l_opy_ (u"ࠦ࡬࡯ࡴࠣἩ"), bstack1111l_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣἪ"), bstack1111l_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤἫ")]).strip().decode(
                bstack1111l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭Ἤ")),
            bstack1111l_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥἭ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1111l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦἮ"): repo.git.rev_list(
                bstack1111l_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥἯ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111ll1llll_opy_ = []
        for remote in remotes:
            bstack1111lll1l1l_opy_ = {
                bstack1111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤἰ"): remote.name,
                bstack1111l_opy_ (u"ࠧࡻࡲ࡭ࠤἱ"): remote.url,
            }
            bstack1111ll1llll_opy_.append(bstack1111lll1l1l_opy_)
        bstack111111l1lll_opy_ = {
            bstack1111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦἲ"): bstack1111l_opy_ (u"ࠢࡨ࡫ࡷࠦἳ"),
            **info,
            bstack1111l_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤἴ"): bstack1111ll1llll_opy_
        }
        bstack111111l1lll_opy_ = bstack1111l11l1l1_opy_(bstack111111l1lll_opy_)
        return bstack111111l1lll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧἵ").format(err))
        return {}
def bstack1111lll11l1_opy_(bstack111111ll1l1_opy_=None):
    bstack1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࡢ࡮࡯ࡽࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤࡺࡹࡥࠡࡥࡤࡷࡪࡹࠠࡧࡱࡵࠤࡪࡧࡣࡩࠢࡩࡳࡱࡪࡥࡳࠢ࡬ࡲࠥࡺࡨࡦࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࠨ࡭࡫ࡶࡸ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡓࡵ࡮ࡦ࠼ࠣࡑࡴࡴ࡯࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨ࠭ࠢࡸࡷࡪࡹࠠࡤࡷࡵࡶࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡠࡵࡳ࠯ࡩࡨࡸࡨࡽࡤࠩࠫࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡊࡳࡰࡵࡻࠣࡰ࡮ࡹࡴࠡ࡝ࡠ࠾ࠥࡓࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡱࡳࠥࡹ࡯ࡶࡴࡦࡩࡸࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦ࠯ࠤࡷ࡫ࡴࡶࡴࡱࡷࠥࡡ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡳࡥࡹ࡮ࡳ࠻ࠢࡐࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࡷࡳࠥࡧ࡮ࡢ࡮ࡼࡾࡪࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡤࡪࡥࡷࡷ࠱ࠦࡥࡢࡥ࡫ࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡱࡵࠤࡦࠦࡦࡰ࡮ࡧࡩࡷ࠴ࠊࠡࠢࠣࠤࠧࠨࠢἶ")
    if bstack111111ll1l1_opy_ is None:
        bstack111111ll1l1_opy_ = [os.getcwd()]
    elif isinstance(bstack111111ll1l1_opy_, list) and len(bstack111111ll1l1_opy_) == 0:
        return []
    results = []
    for folder in bstack111111ll1l1_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1111l_opy_ (u"ࠦࡋࡵ࡬ࡥࡧࡵࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠤἷ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1111l_opy_ (u"ࠧࡶࡲࡊࡦࠥἸ"): bstack1111l_opy_ (u"ࠨࠢἹ"),
                bstack1111l_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨἺ"): [],
                bstack1111l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤἻ"): [],
                bstack1111l_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤἼ"): bstack1111l_opy_ (u"ࠥࠦἽ"),
                bstack1111l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧἾ"): [],
                bstack1111l_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨἿ"): bstack1111l_opy_ (u"ࠨࠢὀ"),
                bstack1111l_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢὁ"): bstack1111l_opy_ (u"ࠣࠤὂ"),
                bstack1111l_opy_ (u"ࠤࡳࡶࡗࡧࡷࡅ࡫ࡩࡪࠧὃ"): bstack1111l_opy_ (u"ࠥࠦὄ")
            }
            bstack11111lllll1_opy_ = repo.active_branch.name
            bstack11111l1l111_opy_ = repo.head.commit
            result[bstack1111l_opy_ (u"ࠦࡵࡸࡉࡥࠤὅ")] = bstack11111l1l111_opy_.hexsha
            bstack1111l111l1l_opy_ = _1111lllll11_opy_(repo)
            logger.debug(bstack1111l_opy_ (u"ࠧࡈࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡪࡴࡸࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠾ࠥࠨ὆") + str(bstack1111l111l1l_opy_) + bstack1111l_opy_ (u"ࠨࠢ὇"))
            if bstack1111l111l1l_opy_:
                try:
                    bstack111l11111ll_opy_ = repo.git.diff(bstack1111l_opy_ (u"ࠢ࠮࠯ࡱࡥࡲ࡫࠭ࡰࡰ࡯ࡽࠧὈ"), bstack1ll1l11l1ll_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰࠱ࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࠨὉ")).split(bstack1111l_opy_ (u"ࠩ࡟ࡲࠬὊ"))
                    logger.debug(bstack1111l_opy_ (u"ࠥࡇ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡦࡪࡺࡷࡦࡧࡱࠤࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀࠤࡦࡴࡤࠡࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀ࠾ࠥࠨὋ") + str(bstack111l11111ll_opy_) + bstack1111l_opy_ (u"ࠦࠧὌ"))
                    result[bstack1111l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦὍ")] = [f.strip() for f in bstack111l11111ll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1l11l1ll_opy_ (u"ࠨࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂ࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥ὎")))
                except Exception:
                    logger.debug(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡧࡴࡲࡱࠥࡨࡲࡢࡰࡦ࡬ࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯࠰ࠣࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳࠥࡸࡥࡤࡧࡱࡸࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠢ὏"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1111l_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢὐ")] = _1111l11l1ll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1111l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣὑ")] = _1111l11l1ll_opy_(commits[:5])
            bstack1111l11l111_opy_ = set()
            bstack11111l11lll_opy_ = []
            for commit in commits:
                logger.debug(bstack1111l_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡤࡱࡰࡱ࡮ࡺ࠺ࠡࠤὒ") + str(commit.message) + bstack1111l_opy_ (u"ࠦࠧὓ"))
                bstack1111ll1111l_opy_ = commit.author.name if commit.author else bstack1111l_opy_ (u"࡛ࠧ࡮࡬ࡰࡲࡻࡳࠨὔ")
                bstack1111l11l111_opy_.add(bstack1111ll1111l_opy_)
                bstack11111l11lll_opy_.append({
                    bstack1111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢὕ"): commit.message.strip(),
                    bstack1111l_opy_ (u"ࠢࡶࡵࡨࡶࠧὖ"): bstack1111ll1111l_opy_
                })
            result[bstack1111l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤὗ")] = list(bstack1111l11l111_opy_)
            result[bstack1111l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡏࡨࡷࡸࡧࡧࡦࡵࠥ὘")] = bstack11111l11lll_opy_
            result[bstack1111l_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥὙ")] = bstack11111l1l111_opy_.committed_datetime.strftime(bstack1111l_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩࠨ὚"))
            if (not result[bstack1111l_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨὛ")] or result[bstack1111l_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢ὜")].strip() == bstack1111l_opy_ (u"ࠢࠣὝ")) and bstack11111l1l111_opy_.message:
                bstack111111l111l_opy_ = bstack11111l1l111_opy_.message.strip().splitlines()
                result[bstack1111l_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ὞")] = bstack111111l111l_opy_[0] if bstack111111l111l_opy_ else bstack1111l_opy_ (u"ࠤࠥὟ")
                if len(bstack111111l111l_opy_) > 2:
                    result[bstack1111l_opy_ (u"ࠥࡴࡷࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥὠ")] = bstack1111l_opy_ (u"ࠫࡡࡴࠧὡ").join(bstack111111l111l_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡱࡵࠤࡆࡏࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࠬ࡫ࡵ࡬ࡥࡧࡵ࠾ࠥࢁࡽࠪ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦὢ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1111l111lll_opy_ = [
        result
        for result in results
        if _11111ll1ll1_opy_(result)
    ]
    return bstack1111l111lll_opy_
def _11111ll1ll1_opy_(result):
    bstack1111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡦ࡮ࡳࡩࡷࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡦࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡴࡷ࡯ࡸࠥ࡯ࡳࠡࡸࡤࡰ࡮ࡪࠠࠩࡰࡲࡲ࠲࡫࡭ࡱࡶࡼࠤ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠣࡥࡳࡪࠠࡢࡷࡷ࡬ࡴࡸࡳࠪ࠰ࠍࠤࠥࠦࠠࠣࠤࠥὣ")
    return (
        isinstance(result.get(bstack1111l_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨὤ"), None), list)
        and len(result[bstack1111l_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢὥ")]) > 0
        and isinstance(result.get(bstack1111l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥὦ"), None), list)
        and len(result[bstack1111l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦὧ")]) > 0
    )
def _1111lllll11_opy_(repo):
    bstack1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤ࡙ࡸࡹࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡪࡨࠤࡧࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡵࡩࡵࡵࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡪࡤࡶࡩࡩ࡯ࡥࡧࡧࠤࡳࡧ࡭ࡦࡵࠣࡥࡳࡪࠠࡸࡱࡵ࡯ࠥࡽࡩࡵࡪࠣࡥࡱࡲࠠࡗࡅࡖࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡷࡹ࠮ࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡮࡬ࠠࡱࡱࡶࡷ࡮ࡨ࡬ࡦ࠮ࠣࡩࡱࡹࡥࠡࡐࡲࡲࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢὨ")
    try:
        try:
            origin = repo.remotes.origin
            bstack1111ll1ll1l_opy_ = origin.refs[bstack1111l_opy_ (u"ࠬࡎࡅࡂࡆࠪὩ")]
            target = bstack1111ll1ll1l_opy_.reference.name
            if target.startswith(bstack1111l_opy_ (u"࠭࡯ࡳ࡫ࡪ࡭ࡳ࠵ࠧὪ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1111l_opy_ (u"ࠧࡰࡴ࡬࡫࡮ࡴ࠯ࠨὫ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1111l11l1ll_opy_(commits):
    bstack1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡦࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤὬ")
    bstack111l11111ll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1111l11ll1l_opy_ in diff:
                        if bstack1111l11ll1l_opy_.a_path:
                            bstack111l11111ll_opy_.add(bstack1111l11ll1l_opy_.a_path)
                        if bstack1111l11ll1l_opy_.b_path:
                            bstack111l11111ll_opy_.add(bstack1111l11ll1l_opy_.b_path)
    except Exception:
        pass
    return list(bstack111l11111ll_opy_)
def bstack1111l11l1l1_opy_(bstack111111l1lll_opy_):
    bstack1111llll111_opy_ = bstack1111ll1l1l1_opy_(bstack111111l1lll_opy_)
    if bstack1111llll111_opy_ and bstack1111llll111_opy_ > bstack111l1l1111l_opy_:
        bstack1111l1l11ll_opy_ = bstack1111llll111_opy_ - bstack111l1l1111l_opy_
        bstack1111ll1l11l_opy_ = bstack11111l1l1l1_opy_(bstack111111l1lll_opy_[bstack1111l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥὭ")], bstack1111l1l11ll_opy_)
        bstack111111l1lll_opy_[bstack1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦὮ")] = bstack1111ll1l11l_opy_
        logger.info(bstack1111l_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨὯ")
                    .format(bstack1111ll1l1l1_opy_(bstack111111l1lll_opy_) / 1024))
    return bstack111111l1lll_opy_
def bstack1111ll1l1l1_opy_(json_data):
    try:
        if json_data:
            bstack11111l1ll11_opy_ = json.dumps(json_data)
            bstack1111l1ll11l_opy_ = sys.getsizeof(bstack11111l1ll11_opy_)
            return bstack1111l1ll11l_opy_
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧὰ").format(e))
    return -1
def bstack11111l1l1l1_opy_(field, bstack1111l1l11l1_opy_):
    try:
        bstack1111lll1111_opy_ = len(bytes(bstack111l1ll11l1_opy_, bstack1111l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬά")))
        bstack1111l1lll1l_opy_ = bytes(field, bstack1111l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ὲ"))
        bstack11111l11ll1_opy_ = len(bstack1111l1lll1l_opy_)
        bstack1111l1111ll_opy_ = ceil(bstack11111l11ll1_opy_ - bstack1111l1l11l1_opy_ - bstack1111lll1111_opy_)
        if bstack1111l1111ll_opy_ > 0:
            bstack111111l1l1l_opy_ = bstack1111l1lll1l_opy_[:bstack1111l1111ll_opy_].decode(bstack1111l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧέ"), errors=bstack1111l_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩὴ")) + bstack111l1ll11l1_opy_
            return bstack111111l1l1l_opy_
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣή").format(e))
    return field
def bstack11llll111_opy_():
    env = os.environ
    if (bstack1111l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤὶ") in env and len(env[bstack1111l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥί")]) > 0) or (
            bstack1111l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧὸ") in env and len(env[bstack1111l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨό")]) > 0):
        return {
            bstack1111l_opy_ (u"ࠣࡰࡤࡱࡪࠨὺ"): bstack1111l_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥύ"),
            bstack1111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨὼ"): env.get(bstack1111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢώ")),
            bstack1111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ὾"): env.get(bstack1111l_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣ὿")),
            bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᾀ"): env.get(bstack1111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᾁ"))
        }
    if env.get(bstack1111l_opy_ (u"ࠤࡆࡍࠧᾂ")) == bstack1111l_opy_ (u"ࠥࡸࡷࡻࡥࠣᾃ") and bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨᾄ"))):
        return {
            bstack1111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᾅ"): bstack1111l_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣᾆ"),
            bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᾇ"): env.get(bstack1111l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᾈ")),
            bstack1111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᾉ"): env.get(bstack1111l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢᾊ")),
            bstack1111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᾋ"): env.get(bstack1111l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣᾌ"))
        }
    if env.get(bstack1111l_opy_ (u"ࠨࡃࡊࠤᾍ")) == bstack1111l_opy_ (u"ࠢࡵࡴࡸࡩࠧᾎ") and bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᾏ"))):
        return {
            bstack1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᾐ"): bstack1111l_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᾑ"),
            bstack1111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᾒ"): env.get(bstack1111l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᾓ")),
            bstack1111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᾔ"): env.get(bstack1111l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᾕ")),
            bstack1111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᾖ"): env.get(bstack1111l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᾗ"))
        }
    if env.get(bstack1111l_opy_ (u"ࠥࡇࡎࠨᾘ")) == bstack1111l_opy_ (u"ࠦࡹࡸࡵࡦࠤᾙ") and env.get(bstack1111l_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᾚ")) == bstack1111l_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᾛ"):
        return {
            bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᾜ"): bstack1111l_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᾝ"),
            bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᾞ"): None,
            bstack1111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᾟ"): None,
            bstack1111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᾠ"): None
        }
    if env.get(bstack1111l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᾡ")) and env.get(bstack1111l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᾢ")):
        return {
            bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᾣ"): bstack1111l_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦᾤ"),
            bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᾥ"): env.get(bstack1111l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᾦ")),
            bstack1111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᾧ"): None,
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᾨ"): env.get(bstack1111l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᾩ"))
        }
    if env.get(bstack1111l_opy_ (u"ࠢࡄࡋࠥᾪ")) == bstack1111l_opy_ (u"ࠣࡶࡵࡹࡪࠨᾫ") and bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣᾬ"))):
        return {
            bstack1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᾭ"): bstack1111l_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥᾮ"),
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᾯ"): env.get(bstack1111l_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᾰ")),
            bstack1111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᾱ"): None,
            bstack1111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᾲ"): env.get(bstack1111l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᾳ"))
        }
    if env.get(bstack1111l_opy_ (u"ࠥࡇࡎࠨᾴ")) == bstack1111l_opy_ (u"ࠦࡹࡸࡵࡦࠤ᾵") and bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᾶ"))):
        return {
            bstack1111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᾷ"): bstack1111l_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᾸ"),
            bstack1111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᾹ"): env.get(bstack1111l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᾺ")),
            bstack1111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧΆ"): env.get(bstack1111l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᾼ")),
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᾽"): env.get(bstack1111l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤι"))
        }
    if env.get(bstack1111l_opy_ (u"ࠢࡄࡋࠥ᾿")) == bstack1111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ῀") and bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧ῁"))):
        return {
            bstack1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣῂ"): bstack1111l_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦῃ"),
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣῄ"): env.get(bstack1111l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥ῅")),
            bstack1111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤῆ"): env.get(bstack1111l_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨῇ")),
            bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣῈ"): env.get(bstack1111l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨΈ"))
        }
    if env.get(bstack1111l_opy_ (u"ࠦࡈࡏࠢῊ")) == bstack1111l_opy_ (u"ࠧࡺࡲࡶࡧࠥΉ") and bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤῌ"))):
        return {
            bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ῍"): bstack1111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦ῎"),
            bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ῏"): env.get(bstack1111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤῐ")),
            bstack1111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨῑ"): env.get(bstack1111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢῒ")) or env.get(bstack1111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤΐ")),
            bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ῔"): env.get(bstack1111l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ῕"))
        }
    if bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦῖ"))):
        return {
            bstack1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣῗ"): bstack1111l_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦῘ"),
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣῙ"): bstack1111l_opy_ (u"ࠨࡻࡾࡽࢀࠦῚ").format(env.get(bstack1111l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪΊ")), env.get(bstack1111l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨ῜"))),
            bstack1111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ῝"): env.get(bstack1111l_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤ῞")),
            bstack1111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ῟"): env.get(bstack1111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧῠ"))
        }
    if bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣῡ"))):
        return {
            bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧῢ"): bstack1111l_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥΰ"),
            bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧῤ"): bstack1111l_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤῥ").format(env.get(bstack1111l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪῦ")), env.get(bstack1111l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ῧ")), env.get(bstack1111l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧῨ")), env.get(bstack1111l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫῩ"))),
            bstack1111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥῪ"): env.get(bstack1111l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨΎ")),
            bstack1111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤῬ"): env.get(bstack1111l_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ῭"))
        }
    if env.get(bstack1111l_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨ΅")) and env.get(bstack1111l_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣ`")):
        return {
            bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ῰"): bstack1111l_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥ῱"),
            bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧῲ"): bstack1111l_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨῳ").format(env.get(bstack1111l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧῴ")), env.get(bstack1111l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪ῵")), env.get(bstack1111l_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ῶ"))),
            bstack1111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤῷ"): env.get(bstack1111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣῸ")),
            bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣΌ"): env.get(bstack1111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥῺ"))
        }
    if any([env.get(bstack1111l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤΏ")), env.get(bstack1111l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦῼ")), env.get(bstack1111l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ´"))]):
        return {
            bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ῾"): bstack1111l_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣ῿"),
            bstack1111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ "): env.get(bstack1111l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ ")),
            bstack1111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ "): env.get(bstack1111l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ ")),
            bstack1111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ "): env.get(bstack1111l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ "))
        }
    if env.get(bstack1111l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨ ")):
        return {
            bstack1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ "): bstack1111l_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥ "),
            bstack1111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ "): env.get(bstack1111l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢ ")),
            bstack1111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ​"): env.get(bstack1111l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨ‌")),
            bstack1111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ‍"): env.get(bstack1111l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢ‎"))
        }
    if env.get(bstack1111l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦ‏")) or env.get(bstack1111l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ‐")):
        return {
            bstack1111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ‑"): bstack1111l_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢ‒"),
            bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ–"): env.get(bstack1111l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ—")),
            bstack1111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ―"): bstack1111l_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥ‖") if env.get(bstack1111l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ‗")) else None,
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ‘"): env.get(bstack1111l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦ’"))
        }
    if any([env.get(bstack1111l_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧ‚")), env.get(bstack1111l_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤ‛")), env.get(bstack1111l_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤ“"))]):
        return {
            bstack1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ”"): bstack1111l_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥ„"),
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ‟"): None,
            bstack1111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ†"): env.get(bstack1111l_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦ‡")),
            bstack1111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ•"): env.get(bstack1111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ‣"))
        }
    if env.get(bstack1111l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨ․")):
        return {
            bstack1111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ‥"): bstack1111l_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣ…"),
            bstack1111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ‧"): env.get(bstack1111l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ ")),
            bstack1111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ "): bstack1111l_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥ‪").format(env.get(bstack1111l_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭‫"))) if env.get(bstack1111l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ‬")) else None,
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ‭"): env.get(bstack1111l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ‮"))
        }
    if bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣ "))):
        return {
            bstack1111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ‰"): bstack1111l_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥ‱"),
            bstack1111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ′"): env.get(bstack1111l_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣ″")),
            bstack1111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ‴"): env.get(bstack1111l_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤ‵")),
            bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ‶"): env.get(bstack1111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ‷"))
        }
    if bstack1ll111llll_opy_(env.get(bstack1111l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥ‸"))):
        return {
            bstack1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ‹"): bstack1111l_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧ›"),
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ※"): bstack1111l_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢ‼").format(env.get(bstack1111l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫ‽")), env.get(bstack1111l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬ‾")), env.get(bstack1111l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩ‿"))),
            bstack1111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⁀"): env.get(bstack1111l_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨ⁁")),
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⁂"): env.get(bstack1111l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨ⁃"))
        }
    if env.get(bstack1111l_opy_ (u"ࠢࡄࡋࠥ⁄")) == bstack1111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ⁅") and env.get(bstack1111l_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤ⁆")) == bstack1111l_opy_ (u"ࠥ࠵ࠧ⁇"):
        return {
            bstack1111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⁈"): bstack1111l_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧ⁉"),
            bstack1111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⁊"): bstack1111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥ⁋").format(env.get(bstack1111l_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬ⁌"))),
            bstack1111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⁍"): None,
            bstack1111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⁎"): None,
        }
    if env.get(bstack1111l_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢ⁏")):
        return {
            bstack1111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⁐"): bstack1111l_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣ⁑"),
            bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⁒"): None,
            bstack1111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⁓"): env.get(bstack1111l_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥ⁔")),
            bstack1111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⁕"): env.get(bstack1111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ⁖"))
        }
    if any([env.get(bstack1111l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣ⁗")), env.get(bstack1111l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨ⁘")), env.get(bstack1111l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧ⁙")), env.get(bstack1111l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤ⁚"))]):
        return {
            bstack1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⁛"): bstack1111l_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨ⁜"),
            bstack1111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁝"): None,
            bstack1111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⁞"): env.get(bstack1111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ ")) or None,
            bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⁠"): env.get(bstack1111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⁡"), 0)
        }
    if env.get(bstack1111l_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ⁢")):
        return {
            bstack1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ⁣"): bstack1111l_opy_ (u"ࠦࡌࡵࡃࡅࠤ⁤"),
            bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⁥"): None,
            bstack1111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⁦"): env.get(bstack1111l_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ⁧")),
            bstack1111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⁨"): env.get(bstack1111l_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣ⁩"))
        }
    if env.get(bstack1111l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ⁪")):
        return {
            bstack1111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⁫"): bstack1111l_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣ⁬"),
            bstack1111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⁭"): env.get(bstack1111l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ⁮")),
            bstack1111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⁯"): env.get(bstack1111l_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧ⁰")),
            bstack1111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤⁱ"): env.get(bstack1111l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ⁲"))
        }
    return {bstack1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⁳"): None}
def get_host_info():
    return {
        bstack1111l_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣ⁴"): platform.node(),
        bstack1111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ⁵"): platform.system(),
        bstack1111l_opy_ (u"ࠣࡶࡼࡴࡪࠨ⁶"): platform.machine(),
        bstack1111l_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥ⁷"): platform.version(),
        bstack1111l_opy_ (u"ࠥࡥࡷࡩࡨࠣ⁸"): platform.architecture()[0]
    }
def bstack1l11ll1111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11111lll1ll_opy_():
    if global_config.get_property(bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ⁹")):
        return bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⁺")
    return bstack1111l_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬ⁻")
def bstack1111lll1ll1_opy_(driver):
    info = {
        bstack1111l_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭⁼"): driver.capabilities,
        bstack1111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬ⁽"): driver.session_id,
        bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ⁾"): driver.capabilities.get(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨⁿ"), None),
        bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭₀"): driver.capabilities.get(bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭₁"), None),
        bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨ₂"): driver.capabilities.get(bstack1111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭₃"), None),
        bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ₄"):driver.capabilities.get(bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ₅"), None),
    }
    if bstack11111lll1ll_opy_() == bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ₆"):
        if bstack1lll1ll1l_opy_():
            info[bstack1111l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ₇")] = bstack1111l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ₈")
        elif driver.capabilities.get(bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ₉"), {}).get(bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ₊"), False):
            info[bstack1111l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ₋")] = bstack1111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭₌")
        else:
            info[bstack1111l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ₍")] = bstack1111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭₎")
    return info
def bstack1lll1ll1l_opy_():
    if global_config.get_property(bstack1111l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ₏")):
        return True
    if bstack1ll111llll_opy_(os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧₐ"), None)):
        return True
    return False
def bstack11111l11l1l_opy_(bstack1111l111ll1_opy_, url, response, headers=None, data=None):
    bstack1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡃࡷ࡬ࡰࡩࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡰࡴ࡭ࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࡶࠤ࡫ࡵࡲࠡࡴࡨࡵࡺ࡫ࡳࡵ࠱ࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡶࡻࡥࡴࡶࡢࡸࡾࡶࡥ࠻ࠢࡋࡘ࡙ࡖࠠ࡮ࡧࡷ࡬ࡴࡪࠠࠩࡉࡈࡘ࠱ࠦࡐࡐࡕࡗ࠰ࠥ࡫ࡴࡤ࠰ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࡻࡲ࡭࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡚ࡘࡌ࠰ࡧࡱࡨࡵࡵࡩ࡯ࡶࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡲࡦ࡯࡫ࡣࡵࠢࡩࡶࡴࡳࠠࡳࡧࡴࡹࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡪࡧࡤࡦࡴࡶ࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡨࡦࡣࡧࡩࡷࡹࠠࡰࡴࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧࡥࡹࡧ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡍࡗࡔࡔࠠࡥࡣࡷࡥࠥࡵࡲࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡌ࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪࠦࡷࡪࡶ࡫ࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠌࠣࠤࠥࠦࠢࠣࠤₑ")
    bstack1111ll1l111_opy_ = {
        bstack1111l_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤₒ"): headers,
        bstack1111l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤₓ"): bstack1111l111ll1_opy_.upper(),
        bstack1111l_opy_ (u"ࠥࡥ࡬࡫࡮ࡵࠤₔ"): None,
        bstack1111l_opy_ (u"ࠦࡪࡴࡤࡱࡱ࡬ࡲࡹࠨₕ"): url,
        bstack1111l_opy_ (u"ࠧࡰࡳࡰࡰࠥₖ"): data
    }
    try:
        bstack1111ll1l1ll_opy_ = response.json()
        if isinstance(bstack1111ll1l1ll_opy_, dict) and bstack1111ll1l1ll_opy_.get(bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ₗ"), {}).get(bstack1111l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨₘ"), {}).get(bstack1111l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩₙ")):
            bstack111111ll11l_opy_ = json.loads(json.dumps(bstack1111ll1l1ll_opy_))
            bstack111111ll11l_opy_[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩₚ")][bstack1111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫₛ")][bstack1111l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬₜ")] = bstack1111l_opy_ (u"ࠧࡡࡲࡦࡦࡤࡧࡹ࡫ࡤࠡࡨࡲࡶࠥࡨࡲࡦࡸ࡬ࡸࡾࡣࠢ₝")
            bstack1111ll1l1ll_opy_ = bstack111111ll11l_opy_
    except Exception:
        bstack1111ll1l1ll_opy_ = response.text
    bstack1111ll1ll11_opy_ = {
        bstack1111l_opy_ (u"ࠨࡢࡰࡦࡼࠦ₞"): bstack1111ll1l1ll_opy_,
        bstack1111l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࡃࡰࡦࡨࠦ₟"): response.status_code
    }
    return {
        bstack1111l_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤ₠"): bstack1111ll1l111_opy_,
        bstack1111l_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ₡"): bstack1111ll1ll11_opy_
    }
def bstack1llll1ll1_opy_(bstack1111l111ll1_opy_, url, data, config):
    headers = config.get(bstack1111l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ₢"), None)
    proxies = bstack1l1l111l11_opy_(config, url)
    auth = config.get(bstack1111l_opy_ (u"ࠫࡦࡻࡴࡩࠩ₣"), None)
    response = requests.request(
            bstack1111l111ll1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack11111l11l1l_opy_(bstack1111l111ll1_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1111l_opy_ (u"ࠬ࠲ࠧ₤"), bstack1111l_opy_ (u"࠭࠺ࠨ₥"))))
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࢁࡽࠣ₦").format(e))
    return response
def bstack11llll11l_opy_(bstack11l1l111l_opy_, size):
    bstack1l1l11lll1_opy_ = []
    while len(bstack11l1l111l_opy_) > size:
        bstack1lll11l1_opy_ = bstack11l1l111l_opy_[:size]
        bstack1l1l11lll1_opy_.append(bstack1lll11l1_opy_)
        bstack11l1l111l_opy_ = bstack11l1l111l_opy_[size:]
    bstack1l1l11lll1_opy_.append(bstack11l1l111l_opy_)
    return bstack1l1l11lll1_opy_
def bstack1111l111l11_opy_(message, bstack111l1111ll1_opy_=False):
    os.write(1, bytes(message, bstack1111l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ₧")))
    os.write(1, bytes(bstack1111l_opy_ (u"ࠩ࡟ࡲࠬ₨"), bstack1111l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ₩")))
    if bstack111l1111ll1_opy_:
        with open(bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪ₪") + os.environ[bstack1111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ₫")] + bstack1111l_opy_ (u"࠭࠮࡭ࡱࡪࠫ€"), bstack1111l_opy_ (u"ࠧࡢࠩ₭")) as f:
            f.write(message + bstack1111l_opy_ (u"ࠨ࡞ࡱࠫ₮"))
def bstack111l1ll11l_opy_():
    return os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ₯")].lower() == bstack1111l_opy_ (u"ࠪࡸࡷࡻࡥࠨ₰")
def current_time():
    return bstack1lllll1111l_opy_().replace(tzinfo=None).isoformat() + bstack1111l_opy_ (u"ࠫ࡟࠭₱")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1111l_opy_ (u"ࠬࡠࠧ₲"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1111l_opy_ (u"࡚࠭ࠨ₳")))).total_seconds() * 1000
def bstack11111l1ll1l_opy_(timestamp):
    return bstack11111ll1l1l_opy_(timestamp).isoformat() + bstack1111l_opy_ (u"࡛ࠧࠩ₴")
def bstack1111ll111ll_opy_(bstack11111ll1111_opy_):
    date_format = bstack1111l_opy_ (u"ࠨࠧ࡜ࠩࡲࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫࠭₵")
    bstack11111l1l1ll_opy_ = datetime.datetime.strptime(bstack11111ll1111_opy_, date_format)
    return bstack11111l1l1ll_opy_.isoformat() + bstack1111l_opy_ (u"ࠩ࡝ࠫ₶")
def bstack1111lll1l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ₷")
    else:
        return bstack1111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ₸")
def bstack1ll111llll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪ₹")
def bstack111111l11l1_opy_(val):
    return val.__str__().lower() == bstack1111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ₺")
def error_handler(bstack111l1111l11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l1111l11_opy_ as e:
                print(bstack1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢ₻").format(func.__name__, bstack111l1111l11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11111l1llll_opy_(bstack11111ll11ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111ll11ll_opy_(cls, *args, **kwargs)
            except bstack111l1111l11_opy_ as e:
                print(bstack1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣ₼").format(bstack11111ll11ll_opy_.__name__, bstack111l1111l11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11111l1llll_opy_
    else:
        return decorator
def bstack11l1ll11ll_opy_(bstack1lll1l1111l_opy_):
    if os.getenv(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ₽")) is not None:
        return bstack1ll111llll_opy_(os.getenv(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭₾")))
    if bstack1111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ₿") in bstack1lll1l1111l_opy_ and bstack111111l11l1_opy_(bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⃀")]):
        return False
    if bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⃁") in bstack1lll1l1111l_opy_ and bstack111111l11l1_opy_(bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⃂")]):
        return False
    return True
def bstack111ll11ll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack1111l11ll11_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣ⃃"), None)
        return bstack1111l11ll11_opy_ is None or bstack1111l11ll11_opy_ == bstack1111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ⃄")
    except Exception as e:
        return False
def bstack1ll11l111l_opy_(hub_url, CONFIG):
    if bstack1l1ll1ll1l_opy_() <= version.parse(bstack1111l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪ⃅")):
        if hub_url:
            return bstack1111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ⃆") + hub_url + bstack1111l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ⃇")
        return bstack11l1l111l1_opy_
    if hub_url:
        return bstack1111l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ⃈") + hub_url + bstack1111l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ⃉")
    return HTTPS_HUB
def bstack11111l11l11_opy_():
    return isinstance(os.getenv(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧ⃊")), str)
def bstack11l11ll1l_opy_(url):
    return urlparse(url).hostname
def bstack111ll1l111_opy_(hostname):
    for bstack1lllll1lll_opy_ in bstack1l111l111_opy_:
        regex = re.compile(bstack1lllll1lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11111ll1lll_opy_(bstack111111lllll_opy_, file_name, logger):
    bstack111lll11ll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠩࢁࠫ⃋")), bstack111111lllll_opy_)
    try:
        if not os.path.exists(bstack111lll11ll_opy_):
            os.makedirs(bstack111lll11ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠪࢂࠬ⃌")), bstack111111lllll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1111l_opy_ (u"ࠫࡼ࠭⃍")):
                pass
            with open(file_path, bstack1111l_opy_ (u"ࠧࡽࠫࠣ⃎")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l1lllll_opy_.format(str(e)))
def bstack1111l1ll111_opy_(file_name, key, value, logger):
    file_path = bstack11111ll1lll_opy_(bstack1111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⃏"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lll1ll1_opy_ = json.load(open(file_path, bstack1111l_opy_ (u"ࠧࡳࡤࠪ⃐")))
        else:
            bstack1l1lll1ll1_opy_ = {}
        bstack1l1lll1ll1_opy_[key] = value
        with open(file_path, bstack1111l_opy_ (u"ࠣࡹ࠮ࠦ⃑")) as outfile:
            json.dump(bstack1l1lll1ll1_opy_, outfile)
def bstack11ll111111_opy_(file_name, logger):
    file_path = bstack11111ll1lll_opy_(bstack1111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬⃒ࠩ"), file_name, logger)
    bstack1l1lll1ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1111l_opy_ (u"ࠪࡶ⃓ࠬ")) as bstack111ll1ll1l_opy_:
            bstack1l1lll1ll1_opy_ = json.load(bstack111ll1ll1l_opy_)
    return bstack1l1lll1ll1_opy_
def bstack11ll1l11l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨ⃔") + file_path + bstack1111l_opy_ (u"ࠬࠦࠧ⃕") + str(e))
def bstack1l1ll1ll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1111l_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣ⃖")
def bstack11l1111l_opy_(config):
    if bstack1111l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭⃗") in config:
        del (config[bstack1111l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ⃘ࠧ")])
        return False
    if bstack1l1ll1ll1l_opy_() < version.parse(bstack1111l_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨ⃙")):
        return False
    if bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠪ࠸࠳࠷࠮࠶⃚ࠩ")):
        return True
    if bstack1111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ⃛") in config and config[bstack1111l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ⃜")] is False:
        return False
    else:
        return True
def bstack11lll1lll_opy_(args_list, bstack111111llll1_opy_):
    index = -1
    for value in bstack111111llll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack111lll1lll1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack111lll1lll1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11111l1111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11111l1111_opy_ = bstack11111l1111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⃝"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⃞"), exception=exception)
    def bstack1lll11l1l1l_opy_(self):
        if self.result != bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⃟"):
            return None
        if isinstance(self.exception_type, str) and bstack1111l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ⃠") in self.exception_type:
            return bstack1111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ⃡")
        return bstack1111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ⃢")
    def bstack1111ll11ll1_opy_(self):
        if self.result != bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⃣"):
            return None
        if self.bstack11111l1111_opy_:
            return self.bstack11111l1111_opy_
        return bstack1111l1l111l_opy_(self.exception)
def bstack1111l1l111l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111l1lllll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l11l11l11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l1l11l_opy_(config, logger):
    try:
        import playwright
        bstack11111ll11l1_opy_ = playwright.__file__
        bstack1111llllll1_opy_ = os.path.split(bstack11111ll11l1_opy_)
        bstack11111lll111_opy_ = bstack1111llllll1_opy_[0] + bstack1111l_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩ⃤")
        os.environ[bstack1111l_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ⃥࡙࡛ࠪ")] = bstack11ll1lllll_opy_(config)
        with open(bstack11111lll111_opy_, bstack1111l_opy_ (u"ࠨࡴ⃦ࠪ")) as f:
            file_content = f.read()
            bstack1111ll11l1l_opy_ = bstack1111l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨ⃧")
            bstack1111lllll1l_opy_ = file_content.find(bstack1111ll11l1l_opy_)
            if bstack1111lllll1l_opy_ == -1:
              process = subprocess.Popen(bstack1111l_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺ⃨ࠢ"), shell=True, cwd=bstack1111llllll1_opy_[0])
              process.wait()
              bstack1111lll111l_opy_ = bstack1111l_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫ⃩")
              bstack111l111l11l_opy_ = bstack1111l_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤ⃪")
              bstack11111lll1l1_opy_ = file_content.replace(bstack1111lll111l_opy_, bstack111l111l11l_opy_)
              with open(bstack11111lll111_opy_, bstack1111l_opy_ (u"࠭ࡷࠨ⃫")) as f:
                f.write(bstack11111lll1l1_opy_)
    except Exception as e:
        logger.error(bstack111l1lllll_opy_.format(str(e)))
def bstack1111l111_opy_():
  try:
    bstack1111llll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴ⃬ࠧ"))
    bstack111l1111lll_opy_ = []
    if os.path.exists(bstack1111llll1l1_opy_):
      with open(bstack1111llll1l1_opy_) as f:
        bstack111l1111lll_opy_ = json.load(f)
      os.remove(bstack1111llll1l1_opy_)
    return bstack111l1111lll_opy_
  except:
    pass
  return []
def bstack11ll11111l_opy_(bstack11111l1ll_opy_):
  try:
    bstack111l1111lll_opy_ = []
    bstack1111llll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨ⃭"))
    if os.path.exists(bstack1111llll1l1_opy_):
      with open(bstack1111llll1l1_opy_) as f:
        bstack111l1111lll_opy_ = json.load(f)
    bstack111l1111lll_opy_.append(bstack11111l1ll_opy_)
    with open(bstack1111llll1l1_opy_, bstack1111l_opy_ (u"ࠩࡺ⃮ࠫ")) as f:
        json.dump(bstack111l1111lll_opy_, f)
  except:
    pass
def bstack1111l1ll1_opy_(logger, bstack1111llll1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1111l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ⃯࠭"), bstack1111l_opy_ (u"ࠫࠬ⃰"))
    if test_name == bstack1111l_opy_ (u"ࠬ࠭⃱"):
        test_name = threading.current_thread().__dict__.get(bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬ⃲"), bstack1111l_opy_ (u"ࠧࠨ⃳"))
    bstack1111l1l1111_opy_ = bstack1111l_opy_ (u"ࠨ࠮ࠣࠫ⃴").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111llll1ll_opy_:
        bstack111l11l1ll_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⃵"), bstack1111l_opy_ (u"ࠪ࠴ࠬ⃶"))
        bstack1111lllll1_opy_ = {bstack1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⃷"): test_name, bstack1111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⃸"): bstack1111l1l1111_opy_, bstack1111l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⃹"): bstack111l11l1ll_opy_}
        bstack1111ll11lll_opy_ = []
        bstack111l1111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭⃺"))
        if os.path.exists(bstack111l1111l1l_opy_):
            with open(bstack111l1111l1l_opy_) as f:
                bstack1111ll11lll_opy_ = json.load(f)
        bstack1111ll11lll_opy_.append(bstack1111lllll1_opy_)
        with open(bstack111l1111l1l_opy_, bstack1111l_opy_ (u"ࠨࡹࠪ⃻")) as f:
            json.dump(bstack1111ll11lll_opy_, f)
    else:
        bstack1111lllll1_opy_ = {bstack1111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⃼"): test_name, bstack1111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⃽"): bstack1111l1l1111_opy_, bstack1111l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ⃾"): str(multiprocessing.current_process().name)}
        if bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ⃿") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1111lllll1_opy_)
  except Exception as e:
      logger.warn(bstack1111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ℀").format(e))
def bstack1111ll1ll_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ℁"))
    try:
      bstack1111l11lll1_opy_ = []
      bstack1111lllll1_opy_ = {bstack1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ℂ"): test_name, bstack1111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ℃"): error_message, bstack1111l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ℄"): index}
      bstack111111lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ℅"))
      if os.path.exists(bstack111111lll1l_opy_):
          with open(bstack111111lll1l_opy_) as f:
              bstack1111l11lll1_opy_ = json.load(f)
      bstack1111l11lll1_opy_.append(bstack1111lllll1_opy_)
      with open(bstack111111lll1l_opy_, bstack1111l_opy_ (u"ࠬࡽࠧ℆")) as f:
          json.dump(bstack1111l11lll1_opy_, f)
    except Exception as e:
      logger.warn(bstack1111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤℇ").format(e))
    return
  bstack1111l11lll1_opy_ = []
  bstack1111lllll1_opy_ = {bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ℈"): test_name, bstack1111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ℉"): error_message, bstack1111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨℊ"): index}
  bstack111111lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫℋ"))
  lock_file = bstack111111lll1l_opy_ + bstack1111l_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪℌ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111111lll1l_opy_):
          with open(bstack111111lll1l_opy_, bstack1111l_opy_ (u"ࠬࡸࠧℍ")) as f:
              content = f.read().strip()
              if content:
                  bstack1111l11lll1_opy_ = json.load(open(bstack111111lll1l_opy_))
      bstack1111l11lll1_opy_.append(bstack1111lllll1_opy_)
      with open(bstack111111lll1l_opy_, bstack1111l_opy_ (u"࠭ࡷࠨℎ")) as f:
          json.dump(bstack1111l11lll1_opy_, f)
  except Exception as e:
    logger.warn(bstack1111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩ࠽ࠤࢀࢃࠢℏ").format(e))
def bstack1lll1llll_opy_(bstack11lll11l1_opy_, name, logger):
  try:
    bstack1111lllll1_opy_ = {bstack1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ℐ"): name, bstack1111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨℑ"): bstack11lll11l1_opy_, bstack1111l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩℒ"): str(threading.current_thread()._name)}
    return bstack1111lllll1_opy_
  except Exception as e:
    logger.warn(bstack1111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣℓ").format(e))
  return
def bstack11111l11111_opy_():
    return platform.system() == bstack1111l_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭℔")
def bstack1ll111l1_opy_(bstack111l111l111_opy_, config, logger):
    bstack1111l111111_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l111l111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡱࡺࡥࡳࠢࡦࡳࡳ࡬ࡩࡨࠢ࡮ࡩࡾࡹࠠࡣࡻࠣࡶࡪ࡭ࡥࡹࠢࡰࡥࡹࡩࡨ࠻ࠢࡾࢁࠧℕ").format(e))
    return bstack1111l111111_opy_
def bstack1111ll11111_opy_(bstack111111l11ll_opy_, bstack11111llll1l_opy_):
    bstack1111l1lll11_opy_ = version.parse(bstack111111l11ll_opy_)
    bstack1111l11l11l_opy_ = version.parse(bstack11111llll1l_opy_)
    if bstack1111l1lll11_opy_ > bstack1111l11l11l_opy_:
        return 1
    elif bstack1111l1lll11_opy_ < bstack1111l11l11l_opy_:
        return -1
    else:
        return 0
def bstack1lllll1111l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11111ll1l1l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111lllllll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l111l11_opy_(options, framework, config, bstack11llll11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1111l_opy_ (u"ࠧࡨࡧࡷࠫ№"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11llll11ll_opy_ = caps.get(bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ℗"))
    bstack1111l1l1lll_opy_ = True
    bstack1111l111ll_opy_ = os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ℘")]
    bstack1l11lll1ll1_opy_ = config.get(bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪℙ"), False)
    if bstack1l11lll1ll1_opy_:
        bstack1l1ll11l111_opy_ = config.get(bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫℚ"), {})
        bstack1l1ll11l111_opy_[bstack1111l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨℛ")] = os.getenv(bstack1111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫℜ"))
        bstack1llll111_opy_ = json.loads(os.getenv(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨℝ"), bstack1111l_opy_ (u"ࠨࡽࢀࠫ℞"))).get(bstack1111l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ℟"))
    if bstack111111l11l1_opy_(caps.get(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪ࡝࠳ࡄࠩ℠"))) or bstack111111l11l1_opy_(caps.get(bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫ℡"))):
        bstack1111l1l1lll_opy_ = False
    if bstack11l1111l_opy_({bstack1111l_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧ™"): bstack1111l1l1lll_opy_}):
        bstack11llll11ll_opy_ = bstack11llll11ll_opy_ or {}
        bstack11llll11ll_opy_[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ℣")] = bstack1111lllllll_opy_(framework)
        bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩℤ")] = bstack111l1ll11l_opy_()
        bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ℥")] = bstack1111l111ll_opy_
        bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫΩ")] = bstack11llll11_opy_
        if bstack1l11lll1ll1_opy_:
            bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ℧")] = bstack1l11lll1ll1_opy_
            bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫℨ")] = bstack1l1ll11l111_opy_
            bstack11llll11ll_opy_[bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ℩")][bstack1111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧK")] = bstack1llll111_opy_
        if getattr(options, bstack1111l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨÅ"), None):
            options.set_capability(bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩℬ"), bstack11llll11ll_opy_)
        else:
            options[bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪℭ")] = bstack11llll11ll_opy_
    else:
        if getattr(options, bstack1111l_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ℮"), None):
            options.set_capability(bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬℯ"), bstack1111lllllll_opy_(framework))
            options.set_capability(bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ℰ"), bstack111l1ll11l_opy_())
            options.set_capability(bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨℱ"), bstack1111l111ll_opy_)
            options.set_capability(bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨℲ"), bstack11llll11_opy_)
            if bstack1l11lll1ll1_opy_:
                options.set_capability(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧℳ"), bstack1l11lll1ll1_opy_)
                options.set_capability(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨℴ"), bstack1l1ll11l111_opy_)
                options.set_capability(bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴ࠰ࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪℵ"), bstack1llll111_opy_)
        else:
            options[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬℶ")] = bstack1111lllllll_opy_(framework)
            options[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ℷ")] = bstack111l1ll11l_opy_()
            options[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨℸ")] = bstack1111l111ll_opy_
            options[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨℹ")] = bstack11llll11_opy_
            if bstack1l11lll1ll1_opy_:
                options[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ℺")] = bstack1l11lll1ll1_opy_
                options[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ℻")] = bstack1l1ll11l111_opy_
                options[bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩℼ")][bstack1111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬℽ")] = bstack1llll111_opy_
    return options
def bstack111111ll111_opy_(ws_endpoint, framework):
    bstack11llll11_opy_ = global_config.get_property(bstack1111l_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢℾ"))
    if ws_endpoint and len(ws_endpoint.split(bstack1111l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬℿ"))) > 1:
        ws_url = ws_endpoint.split(bstack1111l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭⅀"))[0]
        if bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ⅁") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1111l1llll1_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1111l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ⅂"))[1]))
            bstack1111l1llll1_opy_ = bstack1111l1llll1_opy_ or {}
            bstack1111l111ll_opy_ = os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⅃")]
            bstack1111l1llll1_opy_[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⅄")] = str(framework) + str(__version__)
            bstack1111l1llll1_opy_[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ⅅ")] = bstack111l1ll11l_opy_()
            bstack1111l1llll1_opy_[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨⅆ")] = bstack1111l111ll_opy_
            bstack1111l1llll1_opy_[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨⅇ")] = bstack11llll11_opy_
            ws_endpoint = ws_endpoint.split(bstack1111l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧⅈ"))[0] + bstack1111l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨⅉ") + urllib.parse.quote(json.dumps(bstack1111l1llll1_opy_))
    return ws_endpoint
def bstack1l11ll1ll_opy_():
    global bstack1l1l1l1l1l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l1l1l1l_opy_ = BrowserType.connect
    return bstack1l1l1l1l1l_opy_
def bstack111111l1ll1_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1ll1111llll_opy_(self, *args, **kwargs):
    global bstack1l1l1l1l1l_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1111l_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ⅊") in kwargs:
            kwargs[bstack1111l_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ⅋")] = bstack111111ll111_opy_(
                kwargs.get(bstack1111l_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ⅌"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨ⅍").format(str(e)))
    return bstack1l1l1l1l1l_opy_(self, *args, **kwargs)
def bstack111l1111111_opy_(bstack11111l1lll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1l111l11_opy_(bstack11111l1lll1_opy_, bstack1111l_opy_ (u"ࠢࠣⅎ"))
        if proxies and proxies.get(bstack1111l_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ⅏")):
            parsed_url = urlparse(proxies.get(bstack1111l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ⅐")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭⅑")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ⅒")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1111l_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ⅓")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ⅔")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll1l11l11_opy_(bstack11111l1lll1_opy_):
    bstack1111l11111l_opy_ = {
        bstack111l1l111ll_opy_[bstack1111lll11ll_opy_]: bstack11111l1lll1_opy_[bstack1111lll11ll_opy_]
        for bstack1111lll11ll_opy_ in bstack11111l1lll1_opy_
        if bstack1111lll11ll_opy_ in bstack111l1l111ll_opy_
    }
    bstack1111l11111l_opy_[bstack1111l_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢ⅕")] = bstack111l1111111_opy_(bstack11111l1lll1_opy_, global_config.get_property(bstack1111l_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣ⅖")))
    bstack1111l1l1l11_opy_ = [element.lower() for element in bstack111l1l1l11l_opy_]
    bstack11111lll11l_opy_(bstack1111l11111l_opy_, bstack1111l1l1l11_opy_)
    return bstack1111l11111l_opy_
def bstack11111lll11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1111l_opy_ (u"ࠤ࠭࠮࠯࠰ࠢ⅗")
    for value in d.values():
        if isinstance(value, dict):
            bstack11111lll11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11111lll11l_opy_(item, keys)
def bstack1l111llll1l_opy_():
    bstack11111ll111l_opy_ = [os.environ.get(bstack1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡍࡑࡋࡓࡠࡆࡌࡖࠧ⅘")), os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠦࢃࠨ⅙")), bstack1111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⅚")), os.path.join(bstack1111l_opy_ (u"࠭࠯ࡵ࡯ࡳࠫ⅛"), bstack1111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⅜"))]
    for path in bstack11111ll111l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1111l_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣ⅝") + str(path) + bstack1111l_opy_ (u"ࠤࠪࠤࡪࡾࡩࡴࡶࡶ࠲ࠧ⅞"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1111l_opy_ (u"ࠥࡋ࡮ࡼࡩ࡯ࡩࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠡࡨࡲࡶࠥ࠭ࠢ⅟") + str(path) + bstack1111l_opy_ (u"ࠦࠬࠨⅠ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1111l_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧⅡ") + str(path) + bstack1111l_opy_ (u"ࠨࠧࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡫ࡥࡸࠦࡴࡩࡧࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵ࠱ࠦⅢ"))
            else:
                logger.debug(bstack1111l_opy_ (u"ࠢࡄࡴࡨࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࠨࠤⅣ") + str(path) + bstack1111l_opy_ (u"ࠣࠩࠣࡻ࡮ࡺࡨࠡࡹࡵ࡭ࡹ࡫ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱ࠲ࠧⅤ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1111l_opy_ (u"ࠤࡒࡴࡪࡸࡡࡵ࡫ࡲࡲࠥࡹࡵࡤࡥࡨࡩࡩ࡫ࡤࠡࡨࡲࡶࠥ࠭ࠢⅥ") + str(path) + bstack1111l_opy_ (u"ࠥࠫ࠳ࠨⅦ"))
            return path
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡺࡶࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡱࡣࡷ࡬ࢂ࠭࠺ࠡࠤⅧ") + str(e) + bstack1111l_opy_ (u"ࠧࠨⅨ"))
    logger.debug(bstack1111l_opy_ (u"ࠨࡁ࡭࡮ࠣࡴࡦࡺࡨࡴࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠥⅩ"))
    return None
@measure(event_name=EVENTS.bstack111l1ll111l_opy_, stage=STAGE.bstack11lll111l_opy_)
def bstack1llll1l111l_opy_(binary_path, bstack1llll1l1111_opy_, bs_config):
    logger.debug(bstack1111l_opy_ (u"ࠢࡄࡷࡵࡶࡪࡴࡴࠡࡅࡏࡍࠥࡖࡡࡵࡪࠣࡪࡴࡻ࡮ࡥ࠼ࠣࡿࢂࠨⅪ").format(binary_path))
    bstack1111llll11l_opy_ = bstack1111l_opy_ (u"ࠨࠩⅫ")
    bstack1111l1l1l1l_opy_ = {
        bstack1111l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧⅬ"): __version__,
        bstack1111l_opy_ (u"ࠥࡳࡸࠨⅭ"): platform.system(),
        bstack1111l_opy_ (u"ࠦࡴࡹ࡟ࡢࡴࡦ࡬ࠧⅮ"): platform.machine(),
        bstack1111l_opy_ (u"ࠧࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠥⅯ"): bstack1111l_opy_ (u"࠭࠰ࠨⅰ"),
        bstack1111l_opy_ (u"ࠢࡴࡦ࡮ࡣࡱࡧ࡮ࡨࡷࡤ࡫ࡪࠨⅱ"): bstack1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨⅲ")
    }
    bstack1111l1ll1l1_opy_(bstack1111l1l1l1l_opy_)
    try:
        if binary_path:
            if bstack11111l11111_opy_():
                bstack1111l1l1l1l_opy_[bstack1111l_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧⅳ")] = subprocess.check_output([binary_path, bstack1111l_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦⅴ")]).strip().decode(bstack1111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪⅵ"))
            else:
                bstack1111l1l1l1l_opy_[bstack1111l_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪⅶ")] = subprocess.check_output([binary_path, bstack1111l_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢⅷ")], stderr=subprocess.DEVNULL).strip().decode(bstack1111l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ⅸ"))
        response = requests.request(
            bstack1111l_opy_ (u"ࠨࡉࡈࡘࠬⅹ"),
            url=bstack11lll1ll_opy_(bstack111l1ll1l11_opy_),
            headers=None,
            auth=(bs_config[bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫⅺ")], bs_config[bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ⅻ")]),
            json=None,
            params=bstack1111l1l1l1l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1111l_opy_ (u"ࠫࡺࡸ࡬ࠨⅼ") in data.keys() and bstack1111l_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩࡥࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫⅽ") in data.keys():
            logger.debug(bstack1111l_opy_ (u"ࠨࡎࡦࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡣ࡫ࡱࡥࡷࡿࠬࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢⅾ").format(bstack1111l1l1l1l_opy_[bstack1111l_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬⅿ")]))
            if bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫↀ") in os.environ:
                logger.debug(bstack1111l_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡡࡴࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠥ࡯ࡳࠡࡵࡨࡸࠧↁ"))
                data[bstack1111l_opy_ (u"ࠪࡹࡷࡲࠧↂ")] = os.environ[bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧↃ")]
            bstack1111l1111l1_opy_ = bstack1111l1ll1ll_opy_(data[bstack1111l_opy_ (u"ࠬࡻࡲ࡭ࠩↄ")], bstack1llll1l1111_opy_)
            bstack1111llll11l_opy_ = os.path.join(bstack1llll1l1111_opy_, bstack1111l1111l1_opy_)
            os.chmod(bstack1111llll11l_opy_, 0o777) # bstack11111l1l11l_opy_ permission
            return bstack1111llll11l_opy_
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨↅ").format(e))
    return binary_path
def bstack1111l1ll1l1_opy_(bstack1111l1l1l1l_opy_):
    try:
        if bstack1111l_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ↆ") not in bstack1111l1l1l1l_opy_[bstack1111l_opy_ (u"ࠨࡱࡶࠫↇ")].lower():
            return
        if os.path.exists(bstack1111l_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦↈ")):
            with open(bstack1111l_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧ↉"), bstack1111l_opy_ (u"ࠦࡷࠨ↊")) as f:
                bstack111l111111l_opy_ = {}
                for line in f:
                    if bstack1111l_opy_ (u"ࠧࡃࠢ↋") in line:
                        key, value = line.rstrip().split(bstack1111l_opy_ (u"ࠨ࠽ࠣ↌"), 1)
                        bstack111l111111l_opy_[key] = value.strip(bstack1111l_opy_ (u"ࠧࠣ࡞ࠪࠫ↍"))
                bstack1111l1l1l1l_opy_[bstack1111l_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨ↎")] = bstack111l111111l_opy_.get(bstack1111l_opy_ (u"ࠤࡌࡈࠧ↏"), bstack1111l_opy_ (u"ࠥࠦ←"))
        elif os.path.exists(bstack1111l_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡤࡰࡵ࡯࡮ࡦ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ↑")):
            bstack1111l1l1l1l_opy_[bstack1111l_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬ→")] = bstack1111l_opy_ (u"࠭ࡡ࡭ࡲ࡬ࡲࡪ࠭↓")
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡥ࡫ࡶࡸࡷࡵࠠࡰࡨࠣࡰ࡮ࡴࡵࡹࠤ↔") + e)
@measure(event_name=EVENTS.bstack111l1llllll_opy_, stage=STAGE.bstack11lll111l_opy_)
def bstack1111l1ll1ll_opy_(bstack111111ll1ll_opy_, bstack11111l111l1_opy_):
    logger.debug(bstack1111l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭࠻ࠢࠥ↕") + str(bstack111111ll1ll_opy_) + bstack1111l_opy_ (u"ࠤࠥ↖"))
    zip_path = os.path.join(bstack11111l111l1_opy_, bstack1111l_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪ࡟ࡧ࡫࡯ࡩ࠳ࢀࡩࡱࠤ↗"))
    bstack1111l1111l1_opy_ = bstack1111l_opy_ (u"ࠫࠬ↘")
    with requests.get(bstack111111ll1ll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1111l_opy_ (u"ࠧࡽࡢࠣ↙")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1111l_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣ↚"))
    with zipfile.ZipFile(zip_path, bstack1111l_opy_ (u"ࠧࡳࠩ↛")) as zip_ref:
        bstack1111ll111l1_opy_ = zip_ref.namelist()
        if len(bstack1111ll111l1_opy_) > 0:
            bstack1111l1111l1_opy_ = bstack1111ll111l1_opy_[0] # bstack11111ll1l11_opy_ bstack111l1l1l1l1_opy_ will be bstack11111llll11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11111l111l1_opy_)
        logger.debug(bstack1111l_opy_ (u"ࠣࡈ࡬ࡰࡪࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡥࡹࡶࡵࡥࡨࡺࡥࡥࠢࡷࡳࠥ࠭ࠢ↜") + str(bstack11111l111l1_opy_) + bstack1111l_opy_ (u"ࠤࠪࠦ↝"))
    os.remove(zip_path)
    return bstack1111l1111l1_opy_
def get_cli_dir():
    bstack111111lll11_opy_ = bstack1l111llll1l_opy_()
    if bstack111111lll11_opy_:
        bstack1llll1l1111_opy_ = os.path.join(bstack111111lll11_opy_, bstack1111l_opy_ (u"ࠥࡧࡱ࡯ࠢ↞"))
        if not os.path.exists(bstack1llll1l1111_opy_):
            os.makedirs(bstack1llll1l1111_opy_, mode=0o777, exist_ok=True)
        return bstack1llll1l1111_opy_
    else:
        raise FileNotFoundError(bstack1111l_opy_ (u"ࠦࡓࡵࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾ࠴ࠢ↟"))
def bstack1llll1l11ll_opy_(bstack1llll1l1111_opy_):
    bstack1111l_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡳࠦࡡࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠢࠣࠤ↠")
    bstack111111l1l11_opy_ = [
        os.path.join(bstack1llll1l1111_opy_, f)
        for f in os.listdir(bstack1llll1l1111_opy_)
        if os.path.isfile(os.path.join(bstack1llll1l1111_opy_, f)) and f.startswith(bstack1111l_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾ࠳ࠢ↡"))
    ]
    if len(bstack111111l1l11_opy_) > 0:
        return max(bstack111111l1l11_opy_, key=os.path.getmtime) # get bstack1111ll1lll1_opy_ binary
    return bstack1111l_opy_ (u"ࠢࠣ↢")
def bstack11l1111111l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l1111l11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1l1111l11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111l1lll1_opy_(data, keys, default=None):
    bstack1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡤࡪࡪࡲࡹࠡࡩࡨࡸࠥࡧࠠ࡯ࡧࡶࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࠦࡦࡳࡱࡰࠤࡦࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡥࡹࡧ࠺ࠡࡖ࡫ࡩࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶࠣࡸࡴࠦࡴࡳࡣࡹࡩࡷࡹࡥ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡫ࡦࡻࡶ࠾ࠥࡇࠠ࡭࡫ࡶࡸࠥࡵࡦࠡ࡭ࡨࡽࡸ࠵ࡩ࡯ࡦ࡬ࡧࡪࡹࠠࡳࡧࡳࡶࡪࡹࡥ࡯ࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡦࡨࡤࡹࡱࡺ࠺ࠡࡘࡤࡰࡺ࡫ࠠࡵࡱࠣࡶࡪࡺࡵࡳࡰࠣ࡭࡫ࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡴࡨࡸࡺࡸ࡮࠻ࠢࡗ࡬ࡪࠦࡶࡢ࡮ࡸࡩࠥࡧࡴࠡࡶ࡫ࡩࠥࡴࡥࡴࡶࡨࡨࠥࡶࡡࡵࡪ࠯ࠤࡴࡸࠠࡥࡧࡩࡥࡺࡲࡴࠡ࡫ࡩࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪ࠮ࠋࠢࠣࠤࠥࠨࠢࠣ↣")
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
def bstack11111ll1_opy_(bstack11111l1111l_opy_, key, value):
    bstack1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡸࡴࡸࡥࠡࡅࡏࡍࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࠠࡪࡰࠣࡸ࡭࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡲࡩࡠࡧࡱࡺࡤࡼࡡࡳࡵࡢࡱࡦࡶ࠺ࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠠ࡮ࡣࡳࡴ࡮ࡴࡧࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡍࡨࡽࠥ࡬ࡲࡰ࡯ࠣࡇࡑࡏ࡟ࡄࡃࡓࡗࡤ࡚ࡏࡠࡅࡒࡒࡋࡏࡇࠋࠢࠣࠤࠥࠦࠠࠡࠢࡹࡥࡱࡻࡥ࠻࡙ࠢࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࡭࡫ࡱࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠋࠢࠣࠤࠥࠨࠢࠣ↤")
    if key in bstack1l11l11lll_opy_:
        bstack1lll11lll1_opy_ = bstack1l11l11lll_opy_[key]
        if isinstance(bstack1lll11lll1_opy_, list):
            for env_name in bstack1lll11lll1_opy_:
                bstack11111l1111l_opy_[env_name] = value
        else:
            bstack11111l1111l_opy_[bstack1lll11lll1_opy_] = value