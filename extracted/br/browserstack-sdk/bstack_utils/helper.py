# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
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
from bstack_utils.constants import (bstack11ll111ll_opy_, bstack1ll1l11l1_opy_, HTTPS_HUB,
                                    bstack111l111111l_opy_, bstack111l1l111l1_opy_, bstack1111lllllll_opy_, bstack111l11l11l1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l111111_opy_, bstack11l1l1l1l1_opy_
from bstack_utils.proxy import bstack11l11ll1ll_opy_, bstack111l111ll1_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack111111111_opy_ import bstack1l11l1ll_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack111lll111ll_opy_(config):
    return config[bstack1ll1lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᾉ")]
def bstack111ll111lll_opy_(config):
    return config[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᾊ")]
def bstack11l11111l1_opy_():
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
def bstack1111l1lll1l_opy_(obj):
    values = []
    bstack111111ll111_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣᾋ"), re.I)
    for key in obj.keys():
        if bstack111111ll111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111111lll1_opy_(config):
    tags = []
    tags.extend(bstack1111l1lll1l_opy_(os.environ))
    tags.extend(bstack1111l1lll1l_opy_(config))
    return tags
def bstack1llllll1ll11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111111ll11l_opy_(bstack11111l1l111_opy_):
    if not bstack11111l1l111_opy_:
        return bstack1ll1lll_opy_ (u"ࠬ࠭ᾌ")
    return bstack1ll1lll_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢᾍ").format(bstack11111l1l111_opy_.name, bstack11111l1l111_opy_.email)
def bstack111ll1l1ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111l111ll1_opy_ = repo.common_dir
        info = {
            bstack1ll1lll_opy_ (u"ࠢࡴࡪࡤࠦᾎ"): repo.head.commit.hexsha,
            bstack1ll1lll_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦᾏ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll1lll_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤᾐ"): repo.active_branch.name,
            bstack1ll1lll_opy_ (u"ࠥࡸࡦ࡭ࠢᾑ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢᾒ"): bstack111111ll11l_opy_(repo.head.commit.committer),
            bstack1ll1lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨᾓ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll1lll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨᾔ"): bstack111111ll11l_opy_(repo.head.commit.author),
            bstack1ll1lll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧᾕ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll1lll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᾖ"): repo.head.commit.message,
            bstack1ll1lll_opy_ (u"ࠤࡵࡳࡴࡺࠢᾗ"): repo.git.rev_parse(bstack1ll1lll_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧᾘ")),
            bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᾙ"): bstack1111l111ll1_opy_,
            bstack1ll1lll_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᾚ"): subprocess.check_output([bstack1ll1lll_opy_ (u"ࠨࡧࡪࡶࠥᾛ"), bstack1ll1lll_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᾜ"), bstack1ll1lll_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦᾝ")]).strip().decode(
                bstack1ll1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᾞ")),
            bstack1ll1lll_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᾟ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᾠ"): repo.git.rev_list(
                bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧᾡ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11111ll1l11_opy_ = []
        for remote in remotes:
            bstack1111ll1111l_opy_ = {
                bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᾢ"): remote.name,
                bstack1ll1lll_opy_ (u"ࠢࡶࡴ࡯ࠦᾣ"): remote.url,
            }
            bstack11111ll1l11_opy_.append(bstack1111ll1111l_opy_)
        bstack1111l11lll1_opy_ = {
            bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᾤ"): bstack1ll1lll_opy_ (u"ࠤࡪ࡭ࡹࠨᾥ"),
            **info,
            bstack1ll1lll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᾦ"): bstack11111ll1l11_opy_
        }
        bstack1111l11lll1_opy_ = bstack1111l1lll11_opy_(bstack1111l11lll1_opy_)
        return bstack1111l11lll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᾧ").format(err))
        return {}
def bstack1111l1l1l11_opy_(bstack111111111l1_opy_=None):
    bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࡤࡰࡱࡿࠠࡧࡱࡵࡱࡦࡺࡴࡦࡦࠣࡪࡴࡸࠠࡂࡋࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࡵࡴࡧࠣࡧࡦࡹࡥࡴࠢࡩࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫ࡵ࡬ࡥࡧࡵࠤ࡮ࡴࠠࡵࡪࡨࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡎࡰࡰࡨ࠾ࠥࡓ࡯࡯ࡱ࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪ࠯ࠤࡺࡹࡥࡴࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࡛ࠦࡰࡵ࠱࡫ࡪࡺࡣࡸࡦࠫ࠭ࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡅ࡮ࡲࡷࡽࠥࡲࡩࡴࡶࠣ࡟ࡢࡀࠠࡎࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡳࡵࠠࡴࡱࡸࡶࡨ࡫ࡳࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨ࠱ࠦࡲࡦࡶࡸࡶࡳࡹࠠ࡜࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠽ࠤࡒࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪࠣࡻ࡮ࡺࡨࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࠣࡪࡴࡲࡤࡦࡴࡶࠤࡹࡵࠠࡢࡰࡤࡰࡾࢀࡥࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡮࡬ࡷࡹࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡦ࡬ࡧࡹࡹࠬࠡࡧࡤࡧ࡭ࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡡࠡࡨࡲࡰࡩ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᾨ")
    if bstack111111111l1_opy_ is None:
        bstack111111111l1_opy_ = [os.getcwd()]
    elif isinstance(bstack111111111l1_opy_, list) and len(bstack111111111l1_opy_) == 0:
        return []
    results = []
    for folder in bstack111111111l1_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1ll1lll_opy_ (u"ࠨࡆࡰ࡮ࡧࡩࡷࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦᾩ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1ll1lll_opy_ (u"ࠢࡱࡴࡌࡨࠧᾪ"): bstack1ll1lll_opy_ (u"ࠣࠤᾫ"),
                bstack1ll1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᾬ"): [],
                bstack1ll1lll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᾭ"): [],
                bstack1ll1lll_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦᾮ"): bstack1ll1lll_opy_ (u"ࠧࠨᾯ"),
                bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢᾰ"): [],
                bstack1ll1lll_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᾱ"): bstack1ll1lll_opy_ (u"ࠣࠤᾲ"),
                bstack1ll1lll_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤᾳ"): bstack1ll1lll_opy_ (u"ࠥࠦᾴ"),
                bstack1ll1lll_opy_ (u"ࠦࡵࡸࡒࡢࡹࡇ࡭࡫࡬ࠢ᾵"): bstack1ll1lll_opy_ (u"ࠧࠨᾶ")
            }
            bstack11111l11l11_opy_ = repo.active_branch.name
            bstack11111llllll_opy_ = repo.head.commit
            result[bstack1ll1lll_opy_ (u"ࠨࡰࡳࡋࡧࠦᾷ")] = bstack11111llllll_opy_.hexsha
            bstack1lllllll111l_opy_ = _1111l111l1l_opy_(repo)
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡃࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳࡀࠠࠣᾸ") + str(bstack1lllllll111l_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤᾹ"))
            if bstack1lllllll111l_opy_:
                try:
                    bstack1111l11ll11_opy_ = repo.git.diff(bstack1ll1lll_opy_ (u"ࠤ࠰࠱ࡳࡧ࡭ࡦ࠯ࡲࡲࡱࡿࠢᾺ"), bstack1ll11l1ll11_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲࠳ࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽࠣΆ")).split(bstack1ll1lll_opy_ (u"ࠫࡡࡴࠧᾼ"))
                    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡉࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥࡨࡥࡵࡹࡨࡩࡳࠦࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂࠦࡡ࡯ࡦࠣࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࡀࠠࠣ᾽") + str(bstack1111l11ll11_opy_) + bstack1ll1lll_opy_ (u"ࠨࠢι"))
                    result[bstack1ll1lll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨ᾿")] = [f.strip() for f in bstack1111l11ll11_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll11l1ll11_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧ῀")))
                except Exception:
                    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡣࡴࡤࡲࡨ࡮ࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠲ࠥࡌࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡳࡧࡦࡩࡳࡺࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠤ῁"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1ll1lll_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤῂ")] = _111111lll1l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1ll1lll_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥῃ")] = _111111lll1l_opy_(commits[:5])
            bstack11111l11111_opy_ = set()
            bstack1lllllll1111_opy_ = []
            for commit in commits:
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡩࡵ࠼ࠣࠦῄ") + str(commit.message) + bstack1ll1lll_opy_ (u"ࠨࠢ῅"))
                bstack11111l1lll1_opy_ = commit.author.name if commit.author else bstack1ll1lll_opy_ (u"ࠢࡖࡰ࡮ࡲࡴࡽ࡮ࠣῆ")
                bstack11111l11111_opy_.add(bstack11111l1lll1_opy_)
                bstack1lllllll1111_opy_.append({
                    bstack1ll1lll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤῇ"): commit.message.strip(),
                    bstack1ll1lll_opy_ (u"ࠤࡸࡷࡪࡸࠢῈ"): bstack11111l1lll1_opy_
                })
            result[bstack1ll1lll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦΈ")] = list(bstack11111l11111_opy_)
            result[bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧῊ")] = bstack1lllllll1111_opy_
            result[bstack1ll1lll_opy_ (u"ࠧࡶࡲࡅࡣࡷࡩࠧΉ")] = bstack11111llllll_opy_.committed_datetime.strftime(bstack1ll1lll_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࠣῌ"))
            if (not result[bstack1ll1lll_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣ῍")] or result[bstack1ll1lll_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ῎")].strip() == bstack1ll1lll_opy_ (u"ࠤࠥ῏")) and bstack11111llllll_opy_.message:
                bstack11111l111ll_opy_ = bstack11111llllll_opy_.message.strip().splitlines()
                result[bstack1ll1lll_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦῐ")] = bstack11111l111ll_opy_[0] if bstack11111l111ll_opy_ else bstack1ll1lll_opy_ (u"ࠦࠧῑ")
                if len(bstack11111l111ll_opy_) > 2:
                    result[bstack1ll1lll_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧῒ")] = bstack1ll1lll_opy_ (u"࠭࡜࡯ࠩΐ").join(bstack11111l111ll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࠮ࡦࡰ࡮ࡧࡩࡷࡀࠠࡼࡿࠬ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ῔").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1lllllll1lll_opy_ = [
        result
        for result in results
        if _1111l1l1ll1_opy_(result)
    ]
    return bstack1lllllll1lll_opy_
def _1111l1l1ll1_opy_(result):
    bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡨࡰࡵ࡫ࡲࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡡࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡶࡹࡱࡺࠠࡪࡵࠣࡺࡦࡲࡩࡥࠢࠫࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠦࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠥࡧ࡮ࡥࠢࡤࡹࡹ࡮࡯ࡳࡵࠬ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ῕")
    return (
        isinstance(result.get(bstack1ll1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣῖ"), None), list)
        and len(result[bstack1ll1lll_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤῗ")]) > 0
        and isinstance(result.get(bstack1ll1lll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧῘ"), None), list)
        and len(result[bstack1ll1lll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨῙ")]) > 0
    )
def _1111l111l1l_opy_(repo):
    bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡔࡳࡻࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷ࡬ࡪࠦࡢࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡷ࡫ࡰࡰࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣ࡬ࡦࡸࡤࡤࡱࡧࡩࡩࠦ࡮ࡢ࡯ࡨࡷࠥࡧ࡮ࡥࠢࡺࡳࡷࡱࠠࡸ࡫ࡷ࡬ࠥࡧ࡬࡭࡙ࠢࡇࡘࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡲࡴ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡪࡥࡧࡣࡸࡰࡹࠦࡢࡳࡣࡱࡧ࡭ࠦࡩࡧࠢࡳࡳࡸࡹࡩࡣ࡮ࡨ࠰ࠥ࡫࡬ࡴࡧࠣࡒࡴࡴࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤῚ")
    try:
        try:
            origin = repo.remotes.origin
            bstack1111l1l1lll_opy_ = origin.refs[bstack1ll1lll_opy_ (u"ࠧࡉࡇࡄࡈࠬΊ")]
            target = bstack1111l1l1lll_opy_.reference.name
            if target.startswith(bstack1ll1lll_opy_ (u"ࠨࡱࡵ࡭࡬࡯࡮࠰ࠩ῜")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1ll1lll_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪ῝")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _111111lll1l_opy_(commits):
    bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡡࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ῞")
    bstack1111l11ll11_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1111ll11l11_opy_ in diff:
                        if bstack1111ll11l11_opy_.a_path:
                            bstack1111l11ll11_opy_.add(bstack1111ll11l11_opy_.a_path)
                        if bstack1111ll11l11_opy_.b_path:
                            bstack1111l11ll11_opy_.add(bstack1111ll11l11_opy_.b_path)
    except Exception:
        pass
    return list(bstack1111l11ll11_opy_)
def bstack1111l1lll11_opy_(bstack1111l11lll1_opy_):
    bstack1111l1llll1_opy_ = bstack111111l1lll_opy_(bstack1111l11lll1_opy_)
    if bstack1111l1llll1_opy_ and bstack1111l1llll1_opy_ > bstack111l111111l_opy_:
        bstack111111l1111_opy_ = bstack1111l1llll1_opy_ - bstack111l111111l_opy_
        bstack1111l1ll1l1_opy_ = bstack1lllllll1ll1_opy_(bstack1111l11lll1_opy_[bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ῟")], bstack111111l1111_opy_)
        bstack1111l11lll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨῠ")] = bstack1111l1ll1l1_opy_
        logger.info(bstack1ll1lll_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣῡ")
                    .format(bstack111111l1lll_opy_(bstack1111l11lll1_opy_) / 1024))
    return bstack1111l11lll1_opy_
def bstack111111l1lll_opy_(json_data):
    try:
        if json_data:
            bstack11111111111_opy_ = json.dumps(json_data)
            bstack1111l11ll1l_opy_ = sys.getsizeof(bstack11111111111_opy_)
            return bstack1111l11ll1l_opy_
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢῢ").format(e))
    return -1
def bstack1lllllll1ll1_opy_(field, bstack111111l1ll1_opy_):
    try:
        bstack1llllllll111_opy_ = len(bytes(bstack111l1l111l1_opy_, bstack1ll1lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧΰ")))
        bstack11111lllll1_opy_ = bytes(field, bstack1ll1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨῤ"))
        bstack1111l11l1ll_opy_ = len(bstack11111lllll1_opy_)
        bstack111111l1l11_opy_ = ceil(bstack1111l11l1ll_opy_ - bstack111111l1ll1_opy_ - bstack1llllllll111_opy_)
        if bstack111111l1l11_opy_ > 0:
            bstack1111l1ll11l_opy_ = bstack11111lllll1_opy_[:bstack111111l1l11_opy_].decode(bstack1ll1lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩῥ"), errors=bstack1ll1lll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫῦ")) + bstack111l1l111l1_opy_
            return bstack1111l1ll11l_opy_
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥῧ").format(e))
    return field
def bstack1ll11l1l11_opy_():
    env = os.environ
    if (bstack1ll1lll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦῨ") in env and len(env[bstack1ll1lll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧῩ")]) > 0) or (
            bstack1ll1lll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢῪ") in env and len(env[bstack1ll1lll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣΎ")]) > 0):
        return {
            bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣῬ"): bstack1ll1lll_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧ῭"),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ΅"): env.get(bstack1ll1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ`")),
            bstack1ll1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ῰"): env.get(bstack1ll1lll_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥ῱")),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣῲ"): env.get(bstack1ll1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤῳ"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠦࡈࡏࠢῴ")) == bstack1ll1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ῵") and bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣῶ"))):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧῷ"): bstack1ll1lll_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥῸ"),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧΌ"): env.get(bstack1ll1lll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨῺ")),
            bstack1ll1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨΏ"): env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤῼ")),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ´"): env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥ῾"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠣࡅࡌࠦ῿")) == bstack1ll1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ ") and bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥ "))):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ "): bstack1ll1lll_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣ "),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ "): env.get(bstack1ll1lll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢ ")),
            bstack1ll1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ "): env.get(bstack1ll1lll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ ")),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ "): env.get(bstack1ll1lll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ "))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡉࠣ ")) == bstack1ll1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦ​") and env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣ‌")) == bstack1ll1lll_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ‍"):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ‎"): bstack1ll1lll_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧ‏"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ‐"): None,
            bstack1ll1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ‑"): None,
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ‒"): None
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥ–")) and env.get(bstack1ll1lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦ—")):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ―"): bstack1ll1lll_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨ‖"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ‗"): env.get(bstack1ll1lll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥ‘")),
            bstack1ll1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ’"): None,
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ‚"): env.get(bstack1ll1lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ‛"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡍࠧ“")) == bstack1ll1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ”") and bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥ„"))):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ‟"): bstack1ll1lll_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧ†"),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ‡"): env.get(bstack1ll1lll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦ•")),
            bstack1ll1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ‣"): None,
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ․"): env.get(bstack1ll1lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ‥"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡉࠣ…")) == bstack1ll1lll_opy_ (u"ࠨࡴࡳࡷࡨࠦ‧") and bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥ "))):
        return {
            bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ "): bstack1ll1lll_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧ‪"),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ‫"): env.get(bstack1ll1lll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥ‬")),
            bstack1ll1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ‭"): env.get(bstack1ll1lll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ‮")),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ "): env.get(bstack1ll1lll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦ‰"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡍࠧ‱")) == bstack1ll1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ′") and bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢ″"))):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ‴"): bstack1ll1lll_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨ‵"),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ‶"): env.get(bstack1ll1lll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧ‷")),
            bstack1ll1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ‸"): env.get(bstack1ll1lll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ‹")),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ›"): env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣ※"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠨࡃࡊࠤ‼")) == bstack1ll1lll_opy_ (u"ࠢࡵࡴࡸࡩࠧ‽") and bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦ‾"))):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ‿"): bstack1ll1lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨ⁀"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁁"): env.get(bstack1ll1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ⁂")),
            bstack1ll1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⁃"): env.get(bstack1ll1lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤ⁄")) or env.get(bstack1ll1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦ⁅")),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⁆"): env.get(bstack1ll1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ⁇"))
        }
    if bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ⁈"))):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⁉"): bstack1ll1lll_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨ⁊"),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⁋"): bstack1ll1lll_opy_ (u"ࠣࡽࢀࡿࢂࠨ⁌").format(env.get(bstack1ll1lll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬ⁍")), env.get(bstack1ll1lll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪ⁎"))),
            bstack1ll1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⁏"): env.get(bstack1ll1lll_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦ⁐")),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⁑"): env.get(bstack1ll1lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ⁒"))
        }
    if bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥ⁓"))):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⁔"): bstack1ll1lll_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧ⁕"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁖"): bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦ⁗").format(env.get(bstack1ll1lll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬ⁘")), env.get(bstack1ll1lll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨ⁙")), env.get(bstack1ll1lll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩ⁚")), env.get(bstack1ll1lll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭⁛"))),
            bstack1ll1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⁜"): env.get(bstack1ll1lll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ⁝")),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⁞"): env.get(bstack1ll1lll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ "))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣ⁠")) and env.get(bstack1ll1lll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥ⁡")):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⁢"): bstack1ll1lll_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧ⁣"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁤"): bstack1ll1lll_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣ⁥").format(env.get(bstack1ll1lll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩ⁦")), env.get(bstack1ll1lll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬ⁧")), env.get(bstack1ll1lll_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨ⁨"))),
            bstack1ll1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⁩"): env.get(bstack1ll1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ⁪")),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⁫"): env.get(bstack1ll1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ⁬"))
        }
    if any([env.get(bstack1ll1lll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⁭")), env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ⁮")), env.get(bstack1ll1lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ⁯"))]):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⁰"): bstack1ll1lll_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥⁱ"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁲"): env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ⁳")),
            bstack1ll1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⁴"): env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ⁵")),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⁶"): env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ⁷"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ⁸")):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⁹"): bstack1ll1lll_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧ⁺"),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⁻"): env.get(bstack1ll1lll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤ⁼")),
            bstack1ll1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⁽"): env.get(bstack1ll1lll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣ⁾")),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤⁿ"): env.get(bstack1ll1lll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ₀"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨ₁")) or env.get(bstack1ll1lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ₂")):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ₃"): bstack1ll1lll_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤ₄"),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ₅"): env.get(bstack1ll1lll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ₆")),
            bstack1ll1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ₇"): bstack1ll1lll_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧ₈") if env.get(bstack1ll1lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ₉")) else None,
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ₊"): env.get(bstack1ll1lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ₋"))
        }
    if any([env.get(bstack1ll1lll_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ₌")), env.get(bstack1ll1lll_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ₍")), env.get(bstack1ll1lll_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ₎"))]):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ₏"): bstack1ll1lll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧₐ"),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥₑ"): None,
            bstack1ll1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥₒ"): env.get(bstack1ll1lll_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨₓ")),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤₔ"): env.get(bstack1ll1lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨₕ"))
        }
    if env.get(bstack1ll1lll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣₖ")):
        return {
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦₗ"): bstack1ll1lll_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥₘ"),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦₙ"): env.get(bstack1ll1lll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣₚ")),
            bstack1ll1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧₛ"): bstack1ll1lll_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧₜ").format(env.get(bstack1ll1lll_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨ₝"))) if env.get(bstack1ll1lll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤ₞")) else None,
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ₟"): env.get(bstack1ll1lll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ₠"))
        }
    if bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥ₡"))):
        return {
            bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ₢"): bstack1ll1lll_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧ₣"),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ₤"): env.get(bstack1ll1lll_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥ₥")),
            bstack1ll1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ₦"): env.get(bstack1ll1lll_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦ₧")),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ₨"): env.get(bstack1ll1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ₩"))
        }
    if bstack1l11l11111_opy_(env.get(bstack1ll1lll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧ₪"))):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ₫"): bstack1ll1lll_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢ€"),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ₭"): bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤ₮").format(env.get(bstack1ll1lll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭₯")), env.get(bstack1ll1lll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧ₰")), env.get(bstack1ll1lll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫ₱"))),
            bstack1ll1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ₲"): env.get(bstack1ll1lll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣ₳")),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ₴"): env.get(bstack1ll1lll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣ₵"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡍࠧ₶")) == bstack1ll1lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ₷") and env.get(bstack1ll1lll_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦ₸")) == bstack1ll1lll_opy_ (u"ࠧ࠷ࠢ₹"):
        return {
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ₺"): bstack1ll1lll_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢ₻"),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ₼"): bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧ₽").format(env.get(bstack1ll1lll_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧ₾"))),
            bstack1ll1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ₿"): None,
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⃀"): None,
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ⃁")):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⃂"): bstack1ll1lll_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥ⃃"),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⃄"): None,
            bstack1ll1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⃅"): env.get(bstack1ll1lll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧ⃆")),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⃇"): env.get(bstack1ll1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ⃈"))
        }
    if any([env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥ⃉")), env.get(bstack1ll1lll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣ⃊")), env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢ⃋")), env.get(bstack1ll1lll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦ⃌"))]):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⃍"): bstack1ll1lll_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣ⃎"),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⃏"): None,
            bstack1ll1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⃐"): env.get(bstack1ll1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ⃑")) or None,
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲ⃒ࠣ"): env.get(bstack1ll1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈ⃓ࠧ"), 0)
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ⃔")):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⃕"): bstack1ll1lll_opy_ (u"ࠨࡇࡰࡅࡇࠦ⃖"),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⃗"): None,
            bstack1ll1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧ⃘ࠥ"): env.get(bstack1ll1lll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋ⃙ࠢ")),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⃚"): env.get(bstack1ll1lll_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ⃛"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⃜")):
        return {
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⃝"): bstack1ll1lll_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥ⃞"),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⃟"): env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ⃠")),
            bstack1ll1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⃡"): env.get(bstack1ll1lll_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ⃢")),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⃣"): env.get(bstack1ll1lll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⃤"))
        }
    return {bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⃥"): None}
def get_host_info():
    return {
        bstack1ll1lll_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧ⃦ࠥ"): platform.node(),
        bstack1ll1lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ⃧"): platform.system(),
        bstack1ll1lll_opy_ (u"ࠥࡸࡾࡶࡥ⃨ࠣ"): platform.machine(),
        bstack1ll1lll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ⃩"): platform.version(),
        bstack1ll1lll_opy_ (u"ࠧࡧࡲࡤࡪ⃪ࠥ"): platform.architecture()[0]
    }
def bstack1lllllll1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111111l11l1_opy_():
    if global_config.get_property(bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ⃫ࠧ")):
        return bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ⃬࠭")
    return bstack1ll1lll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪ⃭ࠧ")
def bstack111111l11ll_opy_(driver):
    info = {
        bstack1ll1lll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ⃮"): driver.capabilities,
        bstack1ll1lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ⃯ࠧ"): driver.session_id,
        bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ⃰"): driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ⃱"), None),
        bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⃲"): driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⃳"), None),
        bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⃴"): driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ⃵"), None),
        bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⃶"):driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⃷"), None),
    }
    if bstack111111l11l1_opy_() == bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⃸"):
        if bstack1l11l11l1l_opy_():
            info[bstack1ll1lll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ⃹")] = bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⃺")
        elif driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⃻"), {}).get(bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⃼"), False):
            info[bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ⃽")] = bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⃾")
        else:
            info[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭⃿")] = bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ℀")
    return info
def bstack1l11l11l1l_opy_():
    if global_config.get_property(bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭℁")):
        return True
    if bstack1l11l11111_opy_(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩℂ"), None)):
        return True
    return False
def bstack111111lll11_opy_(bstack11111l1111l_opy_, url, response, headers=None, data=None):
    bstack1ll1lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡅࡹ࡮ࡲࡤࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡲ࡯ࡨࠢࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠳ࡷ࡫ࡳࡱࡱࡱࡷࡪࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡱࡶࡧࡶࡸࡤࡺࡹࡱࡧ࠽ࠤࡍ࡚ࡔࡑࠢࡰࡩࡹ࡮࡯ࡥࠢࠫࡋࡊ࡚ࠬࠡࡒࡒࡗ࡙࠲ࠠࡦࡶࡦ࠲࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡶࡴ࡯࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡕࡓࡎ࠲ࡩࡳࡪࡰࡰ࡫ࡱࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡴࡨࡪࡦࡥࡷࠤ࡫ࡸ࡯࡮ࠢࡵࡩࡶࡻࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡮ࡥࡢࡦࡨࡶࡸࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡪࡨࡥࡩ࡫ࡲࡴࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩࡧࡴࡢ࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤࡏ࡙ࡏࡏࠢࡧࡥࡹࡧࠠࡰࡴࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡇࡱࡵࡱࡦࡺࡴࡦࡦࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥࠡࡹ࡬ࡸ࡭ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡤࡢࡶࡤࠎࠥࠦࠠࠡࠤࠥࠦ℃")
    bstack1111l1lllll_opy_ = {
        bstack1ll1lll_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ℄"): headers,
        bstack1ll1lll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦ℅"): bstack11111l1111l_opy_.upper(),
        bstack1ll1lll_opy_ (u"ࠧࡧࡧࡦࡰࡷࠦ℆"): None,
        bstack1ll1lll_opy_ (u"ࠨࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠣℇ"): url,
        bstack1ll1lll_opy_ (u"ࠢ࡫ࡵࡲࡲࠧ℈"): data
    }
    try:
        bstack111111ll1ll_opy_ = response.json()
        if isinstance(bstack111111ll1ll_opy_, dict) and bstack111111ll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ℉"), {}).get(bstack1ll1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪℊ"), {}).get(bstack1ll1lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫℋ")):
            bstack1lllllllllll_opy_ = json.loads(json.dumps(bstack111111ll1ll_opy_))
            bstack1lllllllllll_opy_[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫℌ")][bstack1ll1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ℍ")][bstack1ll1lll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧℎ")] = bstack1ll1lll_opy_ (u"ࠢ࡜ࡴࡨࡨࡦࡩࡴࡦࡦࠣࡪࡴࡸࠠࡣࡴࡨࡺ࡮ࡺࡹ࡞ࠤℏ")
            bstack111111ll1ll_opy_ = bstack1lllllllllll_opy_
    except Exception:
        bstack111111ll1ll_opy_ = response.text
    bstack1111l111lll_opy_ = {
        bstack1ll1lll_opy_ (u"ࠣࡤࡲࡨࡾࠨℐ"): bstack111111ll1ll_opy_,
        bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࡅࡲࡨࡪࠨℑ"): response.status_code
    }
    return {
        bstack1ll1lll_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦℒ"): bstack1111l1lllll_opy_,
        bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨℓ"): bstack1111l111lll_opy_
    }
def bstack111lll1l11_opy_(bstack11111l1111l_opy_, url, data, config):
    headers = config.get(bstack1ll1lll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭℔"), None)
    proxies = bstack11l11ll1ll_opy_(config, url)
    auth = config.get(bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫℕ"), None)
    response = requests.request(
            bstack11111l1111l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack111111lll11_opy_(bstack11111l1111l_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1ll1lll_opy_ (u"ࠧ࠭ࠩ№"), bstack1ll1lll_opy_ (u"ࠨ࠼ࠪ℗"))))
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࡼࡿࠥ℘").format(e))
    return response
def bstack1l1lllll11_opy_(bstack111l111l_opy_, size):
    bstack1ll1l1111_opy_ = []
    while len(bstack111l111l_opy_) > size:
        bstack11ll11l1ll_opy_ = bstack111l111l_opy_[:size]
        bstack1ll1l1111_opy_.append(bstack11ll11l1ll_opy_)
        bstack111l111l_opy_ = bstack111l111l_opy_[size:]
    bstack1ll1l1111_opy_.append(bstack111l111l_opy_)
    return bstack1ll1l1111_opy_
def bstack1111l1ll111_opy_(message, bstack1111l11l1l1_opy_=False):
    os.write(1, bytes(message, bstack1ll1lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩℙ")))
    os.write(1, bytes(bstack1ll1lll_opy_ (u"ࠫࡡࡴࠧℚ"), bstack1ll1lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫℛ")))
    if bstack1111l11l1l1_opy_:
        with open(bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬℜ") + os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ℝ")] + bstack1ll1lll_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭℞"), bstack1ll1lll_opy_ (u"ࠩࡤࠫ℟")) as f:
            f.write(message + bstack1ll1lll_opy_ (u"ࠪࡠࡳ࠭℠"))
def bstack11lll11l1_opy_():
    return os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ℡")].lower() == bstack1ll1lll_opy_ (u"ࠬࡺࡲࡶࡧࠪ™")
def current_time():
    return bstack1llll1l1111_opy_().replace(tzinfo=None).isoformat() + bstack1ll1lll_opy_ (u"࡚࠭ࠨ℣")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll1lll_opy_ (u"࡛ࠧࠩℤ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll1lll_opy_ (u"ࠨ࡜ࠪ℥")))).total_seconds() * 1000
def bstack1111111ll1l_opy_(timestamp):
    return bstack1111l1l11ll_opy_(timestamp).isoformat() + bstack1ll1lll_opy_ (u"ࠩ࡝ࠫΩ")
def bstack1111111ll11_opy_(bstack11111ll1lll_opy_):
    date_format = bstack1ll1lll_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨ℧")
    bstack11111l1l1ll_opy_ = datetime.datetime.strptime(bstack11111ll1lll_opy_, date_format)
    return bstack11111l1l1ll_opy_.isoformat() + bstack1ll1lll_opy_ (u"ࠫ࡟࠭ℨ")
def bstack1llllll1lll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ℩")
    else:
        return bstack1ll1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭K")
def bstack1l11l11111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll1lll_opy_ (u"ࠧࡵࡴࡸࡩࠬÅ")
def bstack1llllll1ll1l_opy_(val):
    return val.__str__().lower() == bstack1ll1lll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧℬ")
def error_handler(bstack1111111l111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111111l111_opy_ as e:
                print(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤℭ").format(func.__name__, bstack1111111l111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11111lll1l1_opy_(bstack1111111llll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1111111llll_opy_(cls, *args, **kwargs)
            except bstack1111111l111_opy_ as e:
                print(bstack1ll1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ℮").format(bstack1111111llll_opy_.__name__, bstack1111111l111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11111lll1l1_opy_
    else:
        return decorator
def bstack1111111l11_opy_(bstack1lllllll11l_opy_):
    if os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧℯ")) is not None:
        return bstack1l11l11111_opy_(os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨℰ")))
    if bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪℱ") in bstack1lllllll11l_opy_ and bstack1llllll1ll1l_opy_(bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫℲ")]):
        return False
    if bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪℳ") in bstack1lllllll11l_opy_ and bstack1llllll1ll1l_opy_(bstack1lllllll11l_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫℴ")]):
        return False
    return True
def bstack1111ll11_opy_():
    try:
        from pytest_bdd import reporting
        bstack11111ll11l1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥℵ"), None)
        return bstack11111ll11l1_opy_ is None or bstack11111ll11l1_opy_ == bstack1ll1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣℶ")
    except Exception as e:
        return False
def bstack11llll1l1l_opy_(hub_url, CONFIG):
    if bstack1l1l11l1l1_opy_() <= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬℷ")):
        if hub_url:
            return bstack1ll1lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢℸ") + hub_url + bstack1ll1lll_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦℹ")
        return bstack1ll1l11l1_opy_
    if hub_url:
        return bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ℺") + hub_url + bstack1ll1lll_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ℻")
    return HTTPS_HUB
def bstack11111l1ll1l_opy_():
    return isinstance(os.getenv(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩℼ")), str)
def bstack1l11111l1l_opy_(url):
    return urlparse(url).hostname
def bstack1l111lllll_opy_(hostname):
    for bstack1l1l1ll1l1_opy_ in bstack11ll111ll_opy_:
        regex = re.compile(bstack1l1l1ll1l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111111l111l_opy_(bstack11111111l11_opy_, file_name, logger):
    bstack1ll11ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠫࢃ࠭ℽ")), bstack11111111l11_opy_)
    try:
        if not os.path.exists(bstack1ll11ll1ll_opy_):
            os.makedirs(bstack1ll11ll1ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠬࢄࠧℾ")), bstack11111111l11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll1lll_opy_ (u"࠭ࡷࠨℿ")):
                pass
            with open(file_path, bstack1ll1lll_opy_ (u"ࠢࡸ࠭ࠥ⅀")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l111111_opy_.format(str(e)))
def bstack1111l11llll_opy_(file_name, key, value, logger):
    file_path = bstack111111l111l_opy_(bstack1ll1lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⅁"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1111l11ll1_opy_ = json.load(open(file_path, bstack1ll1lll_opy_ (u"ࠩࡵࡦࠬ⅂")))
        else:
            bstack1111l11ll1_opy_ = {}
        bstack1111l11ll1_opy_[key] = value
        with open(file_path, bstack1ll1lll_opy_ (u"ࠥࡻ࠰ࠨ⅃")) as outfile:
            json.dump(bstack1111l11ll1_opy_, outfile)
def bstack1l111llll1_opy_(file_name, logger):
    file_path = bstack111111l111l_opy_(bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⅄"), file_name, logger)
    bstack1111l11ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll1lll_opy_ (u"ࠬࡸࠧⅅ")) as bstack1llll1lll_opy_:
            bstack1111l11ll1_opy_ = json.load(bstack1llll1lll_opy_)
    return bstack1111l11ll1_opy_
def bstack1l1ll1l111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪⅆ") + file_path + bstack1ll1lll_opy_ (u"ࠧࠡࠩⅇ") + str(e))
def bstack1l1l11l1l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll1lll_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥⅈ")
def bstack1ll1ll11ll_opy_(config):
    if bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨⅉ") in config:
        del (config[bstack1ll1lll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ⅊")])
        return False
    if bstack1l1l11l1l1_opy_() < version.parse(bstack1ll1lll_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪ⅋")):
        return False
    if bstack1l1l11l1l1_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫ⅌")):
        return True
    if bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭⅍") in config and config[bstack1ll1lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧⅎ")] is False:
        return False
    else:
        return True
def bstack1l1111llll_opy_(args_list, bstack11111lll111_opy_):
    index = -1
    for value in bstack11111lll111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack111ll111ll1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack111ll111ll1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llll1llll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llll1llll1_opy_ = bstack1llll1llll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⅏"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⅐"), exception=exception)
    def bstack1ll1lll11ll_opy_(self):
        if self.result != bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⅑"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll1lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ⅒") in self.exception_type:
            return bstack1ll1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ⅓")
        return bstack1ll1lll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ⅔")
    def bstack1111l1l111l_opy_(self):
        if self.result != bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⅕"):
            return None
        if self.bstack1llll1llll1_opy_:
            return self.bstack1llll1llll1_opy_
        return bstack1111111l1ll_opy_(self.exception)
def bstack1111111l1ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111111lllll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l11lll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1llllll11l_opy_(config, logger):
    try:
        import playwright
        bstack11111ll111l_opy_ = playwright.__file__
        bstack11111l1ll11_opy_ = os.path.split(bstack11111ll111l_opy_)
        bstack11111l11ll1_opy_ = bstack11111l1ll11_opy_[0] + bstack1ll1lll_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫ⅖")
        os.environ[bstack1ll1lll_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬ⅗")] = bstack111l111ll1_opy_(config)
        with open(bstack11111l11ll1_opy_, bstack1ll1lll_opy_ (u"ࠪࡶࠬ⅘")) as f:
            file_content = f.read()
            bstack1111l1111l1_opy_ = bstack1ll1lll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ⅙")
            bstack11111l1l11l_opy_ = file_content.find(bstack1111l1111l1_opy_)
            if bstack11111l1l11l_opy_ == -1:
              process = subprocess.Popen(bstack1ll1lll_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤ⅚"), shell=True, cwd=bstack11111l1ll11_opy_[0])
              process.wait()
              bstack11111l1llll_opy_ = bstack1ll1lll_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭⅛")
              bstack1111l11l111_opy_ = bstack1ll1lll_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦ⅜")
              bstack11111ll11ll_opy_ = file_content.replace(bstack11111l1llll_opy_, bstack1111l11l111_opy_)
              with open(bstack11111l11ll1_opy_, bstack1ll1lll_opy_ (u"ࠨࡹࠪ⅝")) as f:
                f.write(bstack11111ll11ll_opy_)
    except Exception as e:
        logger.error(bstack11l1l1l1l1_opy_.format(str(e)))
def bstack1l1l111111_opy_():
  try:
    bstack1111ll11111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩ⅞"))
    bstack1lllllllll1l_opy_ = []
    if os.path.exists(bstack1111ll11111_opy_):
      with open(bstack1111ll11111_opy_) as f:
        bstack1lllllllll1l_opy_ = json.load(f)
      os.remove(bstack1111ll11111_opy_)
    return bstack1lllllllll1l_opy_
  except:
    pass
  return []
def bstack1lll1ll111_opy_(bstack11l1ll11_opy_):
  try:
    bstack1lllllllll1l_opy_ = []
    bstack1111ll11111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ⅟"))
    if os.path.exists(bstack1111ll11111_opy_):
      with open(bstack1111ll11111_opy_) as f:
        bstack1lllllllll1l_opy_ = json.load(f)
    bstack1lllllllll1l_opy_.append(bstack11l1ll11_opy_)
    with open(bstack1111ll11111_opy_, bstack1ll1lll_opy_ (u"ࠫࡼ࠭Ⅰ")) as f:
        json.dump(bstack1lllllllll1l_opy_, f)
  except:
    pass
def bstack1ll1llll1_opy_(logger, bstack11111l111l1_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨⅡ"), bstack1ll1lll_opy_ (u"࠭ࠧⅢ"))
    if test_name == bstack1ll1lll_opy_ (u"ࠧࠨⅣ"):
        test_name = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧⅤ"), bstack1ll1lll_opy_ (u"ࠩࠪⅥ"))
    bstack11111llll1l_opy_ = bstack1ll1lll_opy_ (u"ࠪ࠰ࠥ࠭Ⅶ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11111l111l1_opy_:
        bstack11111lll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫⅧ"), bstack1ll1lll_opy_ (u"ࠬ࠶ࠧⅨ"))
        bstack1llllll1l_opy_ = {bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫⅩ"): test_name, bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ⅺ"): bstack11111llll1l_opy_, bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧⅫ"): bstack11111lll_opy_}
        bstack1111l11111l_opy_ = []
        bstack1111l11l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨⅬ"))
        if os.path.exists(bstack1111l11l11l_opy_):
            with open(bstack1111l11l11l_opy_) as f:
                bstack1111l11111l_opy_ = json.load(f)
        bstack1111l11111l_opy_.append(bstack1llllll1l_opy_)
        with open(bstack1111l11l11l_opy_, bstack1ll1lll_opy_ (u"ࠪࡻࠬⅭ")) as f:
            json.dump(bstack1111l11111l_opy_, f)
    else:
        bstack1llllll1l_opy_ = {bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩⅮ"): test_name, bstack1ll1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫⅯ"): bstack11111llll1l_opy_, bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬⅰ"): str(multiprocessing.current_process().name)}
        if bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫⅱ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1llllll1l_opy_)
  except Exception as e:
      logger.warn(bstack1ll1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧⅲ").format(e))
def bstack11l1ll1lll_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬⅳ"))
    try:
      bstack1llllllll1l1_opy_ = []
      bstack1llllll1l_opy_ = {bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨⅴ"): test_name, bstack1ll1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪⅵ"): error_message, bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫⅶ"): index}
      bstack111111111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧⅷ"))
      if os.path.exists(bstack111111111ll_opy_):
          with open(bstack111111111ll_opy_) as f:
              bstack1llllllll1l1_opy_ = json.load(f)
      bstack1llllllll1l1_opy_.append(bstack1llllll1l_opy_)
      with open(bstack111111111ll_opy_, bstack1ll1lll_opy_ (u"ࠧࡸࠩⅸ")) as f:
          json.dump(bstack1llllllll1l1_opy_, f)
    except Exception as e:
      logger.warn(bstack1ll1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦⅹ").format(e))
    return
  bstack1llllllll1l1_opy_ = []
  bstack1llllll1l_opy_ = {bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧⅺ"): test_name, bstack1ll1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩⅻ"): error_message, bstack1ll1lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪⅼ"): index}
  bstack111111111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ⅽ"))
  lock_file = bstack111111111ll_opy_ + bstack1ll1lll_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬⅾ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111111111ll_opy_):
          with open(bstack111111111ll_opy_, bstack1ll1lll_opy_ (u"ࠧࡳࠩⅿ")) as f:
              content = f.read().strip()
              if content:
                  bstack1llllllll1l1_opy_ = json.load(open(bstack111111111ll_opy_))
      bstack1llllllll1l1_opy_.append(bstack1llllll1l_opy_)
      with open(bstack111111111ll_opy_, bstack1ll1lll_opy_ (u"ࠨࡹࠪↀ")) as f:
          json.dump(bstack1llllllll1l1_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡦࡪ࡮ࡨࠤࡱࡵࡣ࡬࡫ࡱ࡫࠿ࠦࡻࡾࠤↁ").format(e))
def bstack11lll1llll_opy_(bstack1ll11111_opy_, name, logger):
  try:
    bstack1llllll1l_opy_ = {bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨↂ"): name, bstack1ll1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪↃ"): bstack1ll11111_opy_, bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫↄ"): str(threading.current_thread()._name)}
    return bstack1llllll1l_opy_
  except Exception as e:
    logger.warn(bstack1ll1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥↅ").format(e))
  return
def bstack1111l1l1111_opy_():
    return platform.system() == bstack1ll1lll_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨↆ")
def bstack111l1lll11_opy_(bstack1111111111l_opy_, config, logger):
    bstack11111111l1l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111111111l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢↇ").format(e))
    return bstack11111111l1l_opy_
def bstack111111llll1_opy_(bstack1111111l1l1_opy_, bstack1lllllll11ll_opy_):
    bstack11111ll1111_opy_ = version.parse(bstack1111111l1l1_opy_)
    bstack1lllllll11l1_opy_ = version.parse(bstack1lllllll11ll_opy_)
    if bstack11111ll1111_opy_ > bstack1lllllll11l1_opy_:
        return 1
    elif bstack11111ll1111_opy_ < bstack1lllllll11l1_opy_:
        return -1
    else:
        return 0
def bstack1llll1l1111_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l1l11ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11111llll11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1ll111_opy_(options, framework, config, bstack11l1ll1l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll1lll_opy_ (u"ࠩࡪࡩࡹ࠭ↈ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1lll1111l1_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ↉"))
    bstack11111111lll_opy_ = True
    bstack111l1ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ↊")]
    bstack1l11l1lll11_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ↋"), False)
    if bstack1l11l1lll11_opy_:
        bstack1l1l1lll1ll_opy_ = config.get(bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭↌"), {})
        bstack1l1l1lll1ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ↍")] = os.getenv(bstack1ll1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭↎"))
        bstack11111l11_opy_ = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ↏"), bstack1ll1lll_opy_ (u"ࠪࡿࢂ࠭←"))).get(bstack1ll1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ↑"))
    if bstack1llllll1ll1l_opy_(caps.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫ→"))) or bstack1llllll1ll1l_opy_(caps.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭↓"))):
        bstack11111111lll_opy_ = False
    if bstack1ll1ll11ll_opy_({bstack1ll1lll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ↔"): bstack11111111lll_opy_}):
        bstack1lll1111l1_opy_ = bstack1lll1111l1_opy_ or {}
        bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ↕")] = bstack11111llll11_opy_(framework)
        bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ↖")] = bstack11lll11l1_opy_()
        bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭↗")] = bstack111l1ll11l_opy_
        bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭↘")] = bstack11l1ll1l11_opy_
        if bstack1l11l1lll11_opy_:
            bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ↙")] = bstack1l11l1lll11_opy_
            bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭↚")] = bstack1l1l1lll1ll_opy_
            bstack1lll1111l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ↛")][bstack1ll1lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ↜")] = bstack11111l11_opy_
        if getattr(options, bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ↝"), None):
            options.set_capability(bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ↞"), bstack1lll1111l1_opy_)
        else:
            options[bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ↟")] = bstack1lll1111l1_opy_
    else:
        if getattr(options, bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭↠"), None):
            options.set_capability(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ↡"), bstack11111llll11_opy_(framework))
            options.set_capability(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ↢"), bstack11lll11l1_opy_())
            options.set_capability(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ↣"), bstack111l1ll11l_opy_)
            options.set_capability(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ↤"), bstack11l1ll1l11_opy_)
            if bstack1l11l1lll11_opy_:
                options.set_capability(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ↥"), bstack1l11l1lll11_opy_)
                options.set_capability(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ↦"), bstack1l1l1lll1ll_opy_)
                options.set_capability(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ↧"), bstack11111l11_opy_)
        else:
            options[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ↨")] = bstack11111llll11_opy_(framework)
            options[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ↩")] = bstack11lll11l1_opy_()
            options[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ↪")] = bstack111l1ll11l_opy_
            options[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ↫")] = bstack11l1ll1l11_opy_
            if bstack1l11l1lll11_opy_:
                options[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ↬")] = bstack1l11l1lll11_opy_
                options[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ↭")] = bstack1l1l1lll1ll_opy_
                options[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ↮")][bstack1ll1lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ↯")] = bstack11111l11_opy_
    return options
def bstack11111l11l1l_opy_(ws_endpoint, framework):
    bstack11l1ll1l11_opy_ = global_config.get_property(bstack1ll1lll_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ↰"))
    if ws_endpoint and len(ws_endpoint.split(bstack1ll1lll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ↱"))) > 1:
        ws_url = ws_endpoint.split(bstack1ll1lll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ↲"))[0]
        if bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭↳") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111ll1ll1_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1ll1lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ↴"))[1]))
            bstack11111ll1ll1_opy_ = bstack11111ll1ll1_opy_ or {}
            bstack111l1ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ↵")]
            bstack11111ll1ll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ↶")] = str(framework) + str(__version__)
            bstack11111ll1ll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ↷")] = bstack11lll11l1_opy_()
            bstack11111ll1ll1_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ↸")] = bstack111l1ll11l_opy_
            bstack11111ll1ll1_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ↹")] = bstack11l1ll1l11_opy_
            ws_endpoint = ws_endpoint.split(bstack1ll1lll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ↺"))[0] + bstack1ll1lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ↻") + urllib.parse.quote(json.dumps(bstack11111ll1ll1_opy_))
    return ws_endpoint
def bstack1llllll1l1_opy_():
    global bstack111l11ll1l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack111l11ll1l_opy_ = BrowserType.connect
    return bstack111l11ll1l_opy_
def bstack1lllllllll11_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1ll1111l1l1_opy_(self, *args, **kwargs):
    global bstack111l11ll1l_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1ll1lll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ↼") in kwargs:
            kwargs[bstack1ll1lll_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪ↽")] = bstack11111l11l1l_opy_(
                kwargs.get(bstack1ll1lll_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ↾"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣ↿").format(str(e)))
    return bstack111l11ll1l_opy_(self, *args, **kwargs)
def bstack11111l1l1l1_opy_(bstack1lllllll1l1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l11ll1ll_opy_(bstack1lllllll1l1l_opy_, bstack1ll1lll_opy_ (u"ࠤࠥ⇀"))
        if proxies and proxies.get(bstack1ll1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ⇁")):
            parsed_url = urlparse(proxies.get(bstack1ll1lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ⇂")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ⇃")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll1lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ⇄")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ⇅")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ⇆")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1111l11lll_opy_(bstack1lllllll1l1l_opy_):
    bstack1llllllll1ll_opy_ = {
        bstack111l11l11l1_opy_[bstack1111l111l11_opy_]: bstack1lllllll1l1l_opy_[bstack1111l111l11_opy_]
        for bstack1111l111l11_opy_ in bstack1lllllll1l1l_opy_
        if bstack1111l111l11_opy_ in bstack111l11l11l1_opy_
    }
    bstack1llllllll1ll_opy_[bstack1ll1lll_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤ⇇")] = bstack11111l1l1l1_opy_(bstack1lllllll1l1l_opy_, global_config.get_property(bstack1ll1lll_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥ⇈")))
    bstack1111ll111ll_opy_ = [element.lower() for element in bstack1111lllllll_opy_]
    bstack1lllllll1l11_opy_(bstack1llllllll1ll_opy_, bstack1111ll111ll_opy_)
    return bstack1llllllll1ll_opy_
def bstack1lllllll1l11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll1lll_opy_ (u"ࠦ࠯࠰ࠪࠫࠤ⇉")
    for value in d.values():
        if isinstance(value, dict):
            bstack1lllllll1l11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1lllllll1l11_opy_(item, keys)
def bstack1l1111l1lll_opy_():
    bstack11111lll1ll_opy_ = [os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢ⇊")), os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠨࡾࠣ⇋")), bstack1ll1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⇌")), os.path.join(bstack1ll1lll_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭⇍"), bstack1ll1lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⇎"))]
    for path in bstack11111lll1ll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥ⇏") + str(path) + bstack1ll1lll_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢ⇐"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤ⇑") + str(path) + bstack1ll1lll_opy_ (u"ࠨࠧࠣ⇒"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll1lll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢ⇓") + str(path) + bstack1ll1lll_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨ⇔"))
            else:
                logger.debug(bstack1ll1lll_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦ⇕") + str(path) + bstack1ll1lll_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢ⇖"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤ⇗") + str(path) + bstack1ll1lll_opy_ (u"ࠧ࠭࠮ࠣ⇘"))
            return path
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦ⇙") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣ⇚"))
    logger.debug(bstack1ll1lll_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧ⇛"))
    return None
@measure(event_name=EVENTS.bstack111l11l1111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
def bstack1lll1l11l11_opy_(binary_path, bstack1lll1l1l1l1_opy_, bs_config):
    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣ⇜").format(binary_path))
    bstack1111111l11l_opy_ = bstack1ll1lll_opy_ (u"ࠪࠫ⇝")
    bstack1111l1111ll_opy_ = {
        bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⇞"): __version__,
        bstack1ll1lll_opy_ (u"ࠧࡵࡳࠣ⇟"): platform.system(),
        bstack1ll1lll_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢ⇠"): platform.machine(),
        bstack1ll1lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ⇡"): bstack1ll1lll_opy_ (u"ࠨ࠲ࠪ⇢"),
        bstack1ll1lll_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣ⇣"): bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⇤")
    }
    bstack1111l111111_opy_(bstack1111l1111ll_opy_)
    try:
        if binary_path:
            if bstack1111l1l1111_opy_():
                bstack1111l1111ll_opy_[bstack1ll1lll_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⇥")] = subprocess.check_output([binary_path, bstack1ll1lll_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ⇦")]).strip().decode(bstack1ll1lll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ⇧"))
            else:
                bstack1111l1111ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⇨")] = subprocess.check_output([binary_path, bstack1ll1lll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ⇩")], stderr=subprocess.DEVNULL).strip().decode(bstack1ll1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ⇪"))
        response = requests.request(
            bstack1ll1lll_opy_ (u"ࠪࡋࡊ࡚ࠧ⇫"),
            url=bstack1l11l1ll_opy_(bstack111l111llll_opy_),
            headers=None,
            auth=(bs_config[bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭⇬")], bs_config[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ⇭")]),
            json=None,
            params=bstack1111l1111ll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll1lll_opy_ (u"࠭ࡵࡳ࡮ࠪ⇮") in data.keys() and bstack1ll1lll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⇯") in data.keys():
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤ⇰").format(bstack1111l1111ll_opy_[bstack1ll1lll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⇱")]))
            if bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭⇲") in os.environ:
                logger.debug(bstack1ll1lll_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡣࡶࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠠࡪࡵࠣࡷࡪࡺࠢ⇳"))
                data[bstack1ll1lll_opy_ (u"ࠬࡻࡲ࡭ࠩ⇴")] = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ⇵")]
            bstack1111l1l11l1_opy_ = bstack1llllll1llll_opy_(data[bstack1ll1lll_opy_ (u"ࠧࡶࡴ࡯ࠫ⇶")], bstack1lll1l1l1l1_opy_)
            bstack1111111l11l_opy_ = os.path.join(bstack1lll1l1l1l1_opy_, bstack1111l1l11l1_opy_)
            os.chmod(bstack1111111l11l_opy_, 0o777) # bstack1llllllllll1_opy_ permission
            return bstack1111111l11l_opy_
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣ⇷").format(e))
    return binary_path
def bstack1111l111111_opy_(bstack1111l1111ll_opy_):
    try:
        if bstack1ll1lll_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨ⇸") not in bstack1111l1111ll_opy_[bstack1ll1lll_opy_ (u"ࠪࡳࡸ࠭⇹")].lower():
            return
        if os.path.exists(bstack1ll1lll_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ⇺")):
            with open(bstack1ll1lll_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ⇻"), bstack1ll1lll_opy_ (u"ࠨࡲࠣ⇼")) as f:
                bstack11111lll11l_opy_ = {}
                for line in f:
                    if bstack1ll1lll_opy_ (u"ࠢ࠾ࠤ⇽") in line:
                        key, value = line.rstrip().split(bstack1ll1lll_opy_ (u"ࠣ࠿ࠥ⇾"), 1)
                        bstack11111lll11l_opy_[key] = value.strip(bstack1ll1lll_opy_ (u"ࠩࠥࡠࠬ࠭⇿"))
                bstack1111l1111ll_opy_[bstack1ll1lll_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪ∀")] = bstack11111lll11l_opy_.get(bstack1ll1lll_opy_ (u"ࠦࡎࡊࠢ∁"), bstack1ll1lll_opy_ (u"ࠧࠨ∂"))
        elif os.path.exists(bstack1ll1lll_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡦࡲࡰࡪࡰࡨ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧ∃")):
            bstack1111l1111ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧ∄")] = bstack1ll1lll_opy_ (u"ࠨࡣ࡯ࡴ࡮ࡴࡥࠨ∅")
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡧ࡭ࡸࡺࡲࡰࠢࡲࡪࠥࡲࡩ࡯ࡷࡻࠦ∆") + e)
@measure(event_name=EVENTS.bstack111l111lll1_opy_, stage=STAGE.bstack1111l1ll1_opy_)
def bstack1llllll1llll_opy_(bstack11111ll1l1l_opy_, bstack111111ll1l1_opy_):
    logger.debug(bstack1ll1lll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧ∇") + str(bstack11111ll1l1l_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧ∈"))
    zip_path = os.path.join(bstack111111ll1l1_opy_, bstack1ll1lll_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦ∉"))
    bstack1111l1l11l1_opy_ = bstack1ll1lll_opy_ (u"࠭ࠧ∊")
    with requests.get(bstack11111ll1l1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll1lll_opy_ (u"ࠢࡸࡤࠥ∋")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥ∌"))
    with zipfile.ZipFile(zip_path, bstack1ll1lll_opy_ (u"ࠩࡵࠫ∍")) as zip_ref:
        bstack1111l1ll1ll_opy_ = zip_ref.namelist()
        if len(bstack1111l1ll1ll_opy_) > 0:
            bstack1111l1l11l1_opy_ = bstack1111l1ll1ll_opy_[0] # bstack1llllllll11l_opy_ bstack111l111l111_opy_ will be bstack111111l1l1l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111111ll1l1_opy_)
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤ∎") + str(bstack111111ll1l1_opy_) + bstack1ll1lll_opy_ (u"ࠦࠬࠨ∏"))
    os.remove(zip_path)
    return bstack1111l1l11l1_opy_
def get_cli_dir():
    bstack11111l11lll_opy_ = bstack1l1111l1lll_opy_()
    if bstack11111l11lll_opy_:
        bstack1lll1l1l1l1_opy_ = os.path.join(bstack11111l11lll_opy_, bstack1ll1lll_opy_ (u"ࠧࡩ࡬ࡪࠤ∐"))
        if not os.path.exists(bstack1lll1l1l1l1_opy_):
            os.makedirs(bstack1lll1l1l1l1_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1l1l1l1_opy_
    else:
        raise FileNotFoundError(bstack1ll1lll_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤ∑"))
def bstack1lll1l11lll_opy_(bstack1lll1l1l1l1_opy_):
    bstack1ll1lll_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦ−")
    bstack1111l1l1l1l_opy_ = [
        os.path.join(bstack1lll1l1l1l1_opy_, f)
        for f in os.listdir(bstack1lll1l1l1l1_opy_)
        if os.path.isfile(os.path.join(bstack1lll1l1l1l1_opy_, f)) and f.startswith(bstack1ll1lll_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤ∓"))
    ]
    if len(bstack1111l1l1l1l_opy_) > 0:
        return max(bstack1111l1l1l1l_opy_, key=os.path.getmtime) # get bstack11111111ll1_opy_ binary
    return bstack1ll1lll_opy_ (u"ࠤࠥ∔")
def bstack111ll1lll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11l1llll1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l11l1llll1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l11l11ll_opy_(data, keys, default=None):
    bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡦ࡬ࡥ࡭ࡻࠣ࡫ࡪࡺࠠࡢࠢࡱࡩࡸࡺࡥࡥࠢࡹࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩࡧࡴࡢ࠼ࠣࡘ࡭࡫ࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸࠥࡺ࡯ࠡࡶࡵࡥࡻ࡫ࡲࡴࡧ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡ࡭ࡨࡽࡸࡀࠠࡂࠢ࡯࡭ࡸࡺࠠࡰࡨࠣ࡯ࡪࡿࡳ࠰࡫ࡱࡨ࡮ࡩࡥࡴࠢࡵࡩࡵࡸࡥࡴࡧࡱࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡨࡪࡦࡻ࡬ࡵ࠼࡚ࠣࡦࡲࡵࡦࠢࡷࡳࠥࡸࡥࡵࡷࡵࡲࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡶࡪࡺࡵࡳࡰ࠽ࠤ࡙࡮ࡥࠡࡸࡤࡰࡺ࡫ࠠࡢࡶࠣࡸ࡭࡫ࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡣࡷ࡬࠱ࠦ࡯ࡳࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ∕")
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
def bstack111l1lll_opy_(bstack1111ll111l1_opy_, key, value):
    bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡺ࡯ࡳࡧࠣࡇࡑࡏࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠡ࡯ࡤࡴࡵ࡯࡮ࡨࠢ࡬ࡲࠥࡺࡨࡦࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣ࡭࡫ࡢࡩࡳࡼ࡟ࡷࡣࡵࡷࡤࡳࡡࡱ࠼ࠣࡈ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠢࡰࡥࡵࡶࡩ࡯ࡩࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡏࡪࡿࠠࡧࡴࡲࡱࠥࡉࡌࡊࡡࡆࡅࡕ࡙࡟ࡕࡑࡢࡇࡔࡔࡆࡊࡉࠍࠤࠥࠦࠠࠡࠢࠣࠤࡻࡧ࡬ࡶࡧ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࡯࡭ࡳ࡫ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠍࠤࠥࠦࠠࠣࠤࠥ∖")
    if key in bstack1l11lllll_opy_:
        bstack111ll11lll_opy_ = bstack1l11lllll_opy_[key]
        if isinstance(bstack111ll11lll_opy_, list):
            for env_name in bstack111ll11lll_opy_:
                bstack1111ll111l1_opy_[env_name] = value
        else:
            bstack1111ll111l1_opy_[bstack111ll11lll_opy_] = value