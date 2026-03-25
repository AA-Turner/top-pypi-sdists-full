# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
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
from bstack_utils.constants import (bstack11llll1l1l_opy_, bstack1l1l11ll11_opy_, HTTPS_HUB,
                                    bstack111l11llll1_opy_, bstack111l1l1l111_opy_, bstack111l11l111l_opy_, bstack111l1111ll1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l11l11lll_opy_, bstack11l1llllll_opy_
from bstack_utils.proxy import bstack1l111ll1l_opy_, bstack1l1l11111l_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1111l11l1_opy_ import bstack11l11l1l1l_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack111ll1ll111_opy_(config):
    return config[bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫὭ")]
def bstack111ll1lll1l_opy_(config):
    return config[bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭Ὦ")]
def bstack111l1111l1_opy_():
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
def bstack1111ll1l1ll_opy_(obj):
    values = []
    bstack11111ll111l_opy_ = re.compile(bstack1l1_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣὯ"), re.I)
    for key in obj.keys():
        if bstack11111ll111l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11111llll11_opy_(config):
    tags = []
    tags.extend(bstack1111ll1l1ll_opy_(os.environ))
    tags.extend(bstack1111ll1l1ll_opy_(config))
    return tags
def bstack1111l1l111l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11111111111_opy_(bstack111111lll11_opy_):
    if not bstack111111lll11_opy_:
        return bstack1l1_opy_ (u"ࠬ࠭ὰ")
    return bstack1l1_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢά").format(bstack111111lll11_opy_.name, bstack111111lll11_opy_.email)
def bstack111ll11l1l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111l111ll1_opy_ = repo.common_dir
        info = {
            bstack1l1_opy_ (u"ࠢࡴࡪࡤࠦὲ"): repo.head.commit.hexsha,
            bstack1l1_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦέ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤὴ"): repo.active_branch.name,
            bstack1l1_opy_ (u"ࠥࡸࡦ࡭ࠢή"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢὶ"): bstack11111111111_opy_(repo.head.commit.committer),
            bstack1l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨί"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨὸ"): bstack11111111111_opy_(repo.head.commit.author),
            bstack1l1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧό"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤὺ"): repo.head.commit.message,
            bstack1l1_opy_ (u"ࠤࡵࡳࡴࡺࠢύ"): repo.git.rev_parse(bstack1l1_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧὼ")),
            bstack1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧώ"): bstack1111l111ll1_opy_,
            bstack1l1_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ὾"): subprocess.check_output([bstack1l1_opy_ (u"ࠨࡧࡪࡶࠥ὿"), bstack1l1_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᾀ"), bstack1l1_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦᾁ")]).strip().decode(
                bstack1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᾂ")),
            bstack1l1_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᾃ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᾄ"): repo.git.rev_list(
                bstack1l1_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧᾅ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11111l11lll_opy_ = []
        for remote in remotes:
            bstack11111ll1111_opy_ = {
                bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᾆ"): remote.name,
                bstack1l1_opy_ (u"ࠢࡶࡴ࡯ࠦᾇ"): remote.url,
            }
            bstack11111l11lll_opy_.append(bstack11111ll1111_opy_)
        bstack1lllllll1ll1_opy_ = {
            bstack1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᾈ"): bstack1l1_opy_ (u"ࠤࡪ࡭ࡹࠨᾉ"),
            **info,
            bstack1l1_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᾊ"): bstack11111l11lll_opy_
        }
        bstack1lllllll1ll1_opy_ = bstack1111l111l11_opy_(bstack1lllllll1ll1_opy_)
        return bstack1lllllll1ll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᾋ").format(err))
        return {}
def bstack1111l1llll1_opy_(bstack1111l11111l_opy_=None):
    bstack1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࡤࡰࡱࡿࠠࡧࡱࡵࡱࡦࡺࡴࡦࡦࠣࡪࡴࡸࠠࡂࡋࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࡵࡴࡧࠣࡧࡦࡹࡥࡴࠢࡩࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫ࡵ࡬ࡥࡧࡵࠤ࡮ࡴࠠࡵࡪࡨࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡎࡰࡰࡨ࠾ࠥࡓ࡯࡯ࡱ࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪ࠯ࠤࡺࡹࡥࡴࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࡛ࠦࡰࡵ࠱࡫ࡪࡺࡣࡸࡦࠫ࠭ࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡅ࡮ࡲࡷࡽࠥࡲࡩࡴࡶࠣ࡟ࡢࡀࠠࡎࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡳࡵࠠࡴࡱࡸࡶࡨ࡫ࡳࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨ࠱ࠦࡲࡦࡶࡸࡶࡳࡹࠠ࡜࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠽ࠤࡒࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪࠣࡻ࡮ࡺࡨࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࠣࡪࡴࡲࡤࡦࡴࡶࠤࡹࡵࠠࡢࡰࡤࡰࡾࢀࡥࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡮࡬ࡷࡹࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡦ࡬ࡧࡹࡹࠬࠡࡧࡤࡧ࡭ࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡡࠡࡨࡲࡰࡩ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᾌ")
    if bstack1111l11111l_opy_ is None:
        bstack1111l11111l_opy_ = [os.getcwd()]
    elif isinstance(bstack1111l11111l_opy_, list) and len(bstack1111l11111l_opy_) == 0:
        return []
    results = []
    for folder in bstack1111l11111l_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1l1_opy_ (u"ࠨࡆࡰ࡮ࡧࡩࡷࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦᾍ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l1_opy_ (u"ࠢࡱࡴࡌࡨࠧᾎ"): bstack1l1_opy_ (u"ࠣࠤᾏ"),
                bstack1l1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᾐ"): [],
                bstack1l1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᾑ"): [],
                bstack1l1_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦᾒ"): bstack1l1_opy_ (u"ࠧࠨᾓ"),
                bstack1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢᾔ"): [],
                bstack1l1_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᾕ"): bstack1l1_opy_ (u"ࠣࠤᾖ"),
                bstack1l1_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤᾗ"): bstack1l1_opy_ (u"ࠥࠦᾘ"),
                bstack1l1_opy_ (u"ࠦࡵࡸࡒࡢࡹࡇ࡭࡫࡬ࠢᾙ"): bstack1l1_opy_ (u"ࠧࠨᾚ")
            }
            bstack1111ll11l1l_opy_ = repo.active_branch.name
            bstack1111l1l11l1_opy_ = repo.head.commit
            result[bstack1l1_opy_ (u"ࠨࡰࡳࡋࡧࠦᾛ")] = bstack1111l1l11l1_opy_.hexsha
            bstack1llllllll11l_opy_ = _11111ll1lll_opy_(repo)
            logger.debug(bstack1l1_opy_ (u"ࠢࡃࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳࡀࠠࠣᾜ") + str(bstack1llllllll11l_opy_) + bstack1l1_opy_ (u"ࠣࠤᾝ"))
            if bstack1llllllll11l_opy_:
                try:
                    bstack11111lll11l_opy_ = repo.git.diff(bstack1l1_opy_ (u"ࠤ࠰࠱ࡳࡧ࡭ࡦ࠯ࡲࡲࡱࡿࠢᾞ"), bstack1ll11l111l1_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲࠳ࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽࠣᾟ")).split(bstack1l1_opy_ (u"ࠫࡡࡴࠧᾠ"))
                    logger.debug(bstack1l1_opy_ (u"ࠧࡉࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥࡨࡥࡵࡹࡨࡩࡳࠦࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂࠦࡡ࡯ࡦࠣࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࡀࠠࠣᾡ") + str(bstack11111lll11l_opy_) + bstack1l1_opy_ (u"ࠨࠢᾢ"))
                    result[bstack1l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᾣ")] = [f.strip() for f in bstack11111lll11l_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll11l111l1_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧᾤ")))
                except Exception:
                    logger.debug(bstack1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡣࡴࡤࡲࡨ࡮ࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠲ࠥࡌࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡳࡧࡦࡩࡳࡺࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠤᾥ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l1_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᾦ")] = _1111111l111_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᾧ")] = _1111111l111_opy_(commits[:5])
            bstack1111l1l1l1l_opy_ = set()
            bstack111111ll1l1_opy_ = []
            for commit in commits:
                logger.debug(bstack1l1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡩࡵ࠼ࠣࠦᾨ") + str(commit.message) + bstack1l1_opy_ (u"ࠨࠢᾩ"))
                bstack11111l1lll1_opy_ = commit.author.name if commit.author else bstack1l1_opy_ (u"ࠢࡖࡰ࡮ࡲࡴࡽ࡮ࠣᾪ")
                bstack1111l1l1l1l_opy_.add(bstack11111l1lll1_opy_)
                bstack111111ll1l1_opy_.append({
                    bstack1l1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᾫ"): commit.message.strip(),
                    bstack1l1_opy_ (u"ࠤࡸࡷࡪࡸࠢᾬ"): bstack11111l1lll1_opy_
                })
            result[bstack1l1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᾭ")] = list(bstack1111l1l1l1l_opy_)
            result[bstack1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧᾮ")] = bstack111111ll1l1_opy_
            result[bstack1l1_opy_ (u"ࠧࡶࡲࡅࡣࡷࡩࠧᾯ")] = bstack1111l1l11l1_opy_.committed_datetime.strftime(bstack1l1_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࠣᾰ"))
            if (not result[bstack1l1_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᾱ")] or result[bstack1l1_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤᾲ")].strip() == bstack1l1_opy_ (u"ࠤࠥᾳ")) and bstack1111l1l11l1_opy_.message:
                bstack11111l11111_opy_ = bstack1111l1l11l1_opy_.message.strip().splitlines()
                result[bstack1l1_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦᾴ")] = bstack11111l11111_opy_[0] if bstack11111l11111_opy_ else bstack1l1_opy_ (u"ࠦࠧ᾵")
                if len(bstack11111l11111_opy_) > 2:
                    result[bstack1l1_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧᾶ")] = bstack1l1_opy_ (u"࠭࡜࡯ࠩᾷ").join(bstack11111l11111_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࠮ࡦࡰ࡮ࡧࡩࡷࡀࠠࡼࡿࠬ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨᾸ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack111111lll1l_opy_ = [
        result
        for result in results
        if _1111ll11ll1_opy_(result)
    ]
    return bstack111111lll1l_opy_
def _1111ll11ll1_opy_(result):
    bstack1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡨࡰࡵ࡫ࡲࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡡࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡶࡹࡱࡺࠠࡪࡵࠣࡺࡦࡲࡩࡥࠢࠫࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠦࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠥࡧ࡮ࡥࠢࡤࡹࡹ࡮࡯ࡳࡵࠬ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᾹ")
    return (
        isinstance(result.get(bstack1l1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᾺ"), None), list)
        and len(result[bstack1l1_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤΆ")]) > 0
        and isinstance(result.get(bstack1l1_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧᾼ"), None), list)
        and len(result[bstack1l1_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ᾽")]) > 0
    )
def _11111ll1lll_opy_(repo):
    bstack1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡔࡳࡻࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷ࡬ࡪࠦࡢࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡷ࡫ࡰࡰࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣ࡬ࡦࡸࡤࡤࡱࡧࡩࡩࠦ࡮ࡢ࡯ࡨࡷࠥࡧ࡮ࡥࠢࡺࡳࡷࡱࠠࡸ࡫ࡷ࡬ࠥࡧ࡬࡭࡙ࠢࡇࡘࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡲࡴ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡪࡥࡧࡣࡸࡰࡹࠦࡢࡳࡣࡱࡧ࡭ࠦࡩࡧࠢࡳࡳࡸࡹࡩࡣ࡮ࡨ࠰ࠥ࡫࡬ࡴࡧࠣࡒࡴࡴࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤι")
    try:
        try:
            origin = repo.remotes.origin
            bstack111111ll111_opy_ = origin.refs[bstack1l1_opy_ (u"ࠧࡉࡇࡄࡈࠬ᾿")]
            target = bstack111111ll111_opy_.reference.name
            if target.startswith(bstack1l1_opy_ (u"ࠨࡱࡵ࡭࡬࡯࡮࠰ࠩ῀")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1l1_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪ῁")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1111111l111_opy_(commits):
    bstack1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡡࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠎࠥࠦࠠࠡࠤࠥࠦῂ")
    bstack11111lll11l_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11111lllll1_opy_ in diff:
                        if bstack11111lllll1_opy_.a_path:
                            bstack11111lll11l_opy_.add(bstack11111lllll1_opy_.a_path)
                        if bstack11111lllll1_opy_.b_path:
                            bstack11111lll11l_opy_.add(bstack11111lllll1_opy_.b_path)
    except Exception:
        pass
    return list(bstack11111lll11l_opy_)
def bstack1111l111l11_opy_(bstack1lllllll1ll1_opy_):
    bstack11111l1l11l_opy_ = bstack11111111lll_opy_(bstack1lllllll1ll1_opy_)
    if bstack11111l1l11l_opy_ and bstack11111l1l11l_opy_ > bstack111l11llll1_opy_:
        bstack1111l11l111_opy_ = bstack11111l1l11l_opy_ - bstack111l11llll1_opy_
        bstack1111l1l1111_opy_ = bstack111111111ll_opy_(bstack1lllllll1ll1_opy_[bstack1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧῃ")], bstack1111l11l111_opy_)
        bstack1lllllll1ll1_opy_[bstack1l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨῄ")] = bstack1111l1l1111_opy_
        logger.info(bstack1l1_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣ῅")
                    .format(bstack11111111lll_opy_(bstack1lllllll1ll1_opy_) / 1024))
    return bstack1lllllll1ll1_opy_
def bstack11111111lll_opy_(json_data):
    try:
        if json_data:
            bstack1111111111l_opy_ = json.dumps(json_data)
            bstack11111l1l111_opy_ = sys.getsizeof(bstack1111111111l_opy_)
            return bstack11111l1l111_opy_
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢῆ").format(e))
    return -1
def bstack111111111ll_opy_(field, bstack111111l1l11_opy_):
    try:
        bstack111111lllll_opy_ = len(bytes(bstack111l1l1l111_opy_, bstack1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧῇ")))
        bstack1111l1111l1_opy_ = bytes(field, bstack1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨῈ"))
        bstack111111llll1_opy_ = len(bstack1111l1111l1_opy_)
        bstack11111ll1l11_opy_ = ceil(bstack111111llll1_opy_ - bstack111111l1l11_opy_ - bstack111111lllll_opy_)
        if bstack11111ll1l11_opy_ > 0:
            bstack1111ll1l111_opy_ = bstack1111l1111l1_opy_[:bstack11111ll1l11_opy_].decode(bstack1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩΈ"), errors=bstack1l1_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫῊ")) + bstack111l1l1l111_opy_
            return bstack1111ll1l111_opy_
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥΉ").format(e))
    return field
def bstack11l1l111ll_opy_():
    env = os.environ
    if (bstack1l1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦῌ") in env and len(env[bstack1l1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ῍")]) > 0) or (
            bstack1l1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ῎") in env and len(env[bstack1l1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ῏")]) > 0):
        return {
            bstack1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣῐ"): bstack1l1_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧῑ"),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣῒ"): env.get(bstack1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤΐ")),
            bstack1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ῔"): env.get(bstack1l1_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥ῕")),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣῖ"): env.get(bstack1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤῗ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠦࡈࡏࠢῘ")) == bstack1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥῙ") and bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣῚ"))):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧΊ"): bstack1l1_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥ῜"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ῝"): env.get(bstack1l1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ῞")),
            bstack1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ῟"): env.get(bstack1l1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤῠ")),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧῡ"): env.get(bstack1l1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥῢ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠣࡅࡌࠦΰ")) == bstack1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢῤ") and bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥῥ"))):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤῦ"): bstack1l1_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣῧ"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤῨ"): env.get(bstack1l1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢῩ")),
            bstack1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥῪ"): env.get(bstack1l1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦΎ")),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤῬ"): env.get(bstack1l1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ῭"))
        }
    if env.get(bstack1l1_opy_ (u"ࠧࡉࡉࠣ΅")) == bstack1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ`") and env.get(bstack1l1_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣ῰")) == bstack1l1_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ῱"):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢῲ"): bstack1l1_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧῳ"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢῴ"): None,
            bstack1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ῵"): None,
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧῶ"): None
        }
    if env.get(bstack1l1_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥῷ")) and env.get(bstack1l1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦῸ")):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢΌ"): bstack1l1_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨῺ"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢΏ"): env.get(bstack1l1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥῼ")),
            bstack1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ´"): None,
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ῾"): env.get(bstack1l1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ῿"))
        }
    if env.get(bstack1l1_opy_ (u"ࠤࡆࡍࠧ ")) == bstack1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣ ") and bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥ "))):
        return {
            bstack1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ "): bstack1l1_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧ "),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ "): env.get(bstack1l1_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦ ")),
            bstack1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ "): None,
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ "): env.get(bstack1l1_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ "))
        }
    if env.get(bstack1l1_opy_ (u"ࠧࡉࡉࠣ ")) == bstack1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ​") and bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥ‌"))):
        return {
            bstack1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ‍"): bstack1l1_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧ‎"),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ‏"): env.get(bstack1l1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥ‐")),
            bstack1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ‑"): env.get(bstack1l1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ‒")),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ–"): env.get(bstack1l1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦ—"))
        }
    if env.get(bstack1l1_opy_ (u"ࠤࡆࡍࠧ―")) == bstack1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣ‖") and bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢ‗"))):
        return {
            bstack1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ‘"): bstack1l1_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨ’"),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ‚"): env.get(bstack1l1_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧ‛")),
            bstack1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ“"): env.get(bstack1l1_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ”")),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ„"): env.get(bstack1l1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣ‟"))
        }
    if env.get(bstack1l1_opy_ (u"ࠨࡃࡊࠤ†")) == bstack1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ‡") and bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦ•"))):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ‣"): bstack1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨ․"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ‥"): env.get(bstack1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ…")),
            bstack1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ‧"): env.get(bstack1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤ ")) or env.get(bstack1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦ ")),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ‪"): env.get(bstack1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ‫"))
        }
    if bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ‬"))):
        return {
            bstack1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ‭"): bstack1l1_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨ‮"),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ "): bstack1l1_opy_ (u"ࠣࡽࢀࡿࢂࠨ‰").format(env.get(bstack1l1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬ‱")), env.get(bstack1l1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪ′"))),
            bstack1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ″"): env.get(bstack1l1_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦ‴")),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ‵"): env.get(bstack1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ‶"))
        }
    if bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥ‷"))):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ‸"): bstack1l1_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧ‹"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ›"): bstack1l1_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦ※").format(env.get(bstack1l1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬ‼")), env.get(bstack1l1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨ‽")), env.get(bstack1l1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩ‾")), env.get(bstack1l1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭‿"))),
            bstack1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⁀"): env.get(bstack1l1_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ⁁")),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⁂"): env.get(bstack1l1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ⁃"))
        }
    if env.get(bstack1l1_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣ⁄")) and env.get(bstack1l1_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥ⁅")):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⁆"): bstack1l1_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧ⁇"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁈"): bstack1l1_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣ⁉").format(env.get(bstack1l1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩ⁊")), env.get(bstack1l1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬ⁋")), env.get(bstack1l1_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨ⁌"))),
            bstack1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⁍"): env.get(bstack1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ⁎")),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⁏"): env.get(bstack1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ⁐"))
        }
    if any([env.get(bstack1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⁑")), env.get(bstack1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ⁒")), env.get(bstack1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ⁓"))]):
        return {
            bstack1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⁔"): bstack1l1_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥ⁕"),
            bstack1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁖"): env.get(bstack1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ⁗")),
            bstack1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⁘"): env.get(bstack1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ⁙")),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⁚"): env.get(bstack1l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ⁛"))
        }
    if env.get(bstack1l1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ⁜")):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⁝"): bstack1l1_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧ⁞"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ "): env.get(bstack1l1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤ⁠")),
            bstack1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⁡"): env.get(bstack1l1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣ⁢")),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⁣"): env.get(bstack1l1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ⁤"))
        }
    if env.get(bstack1l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨ⁥")) or env.get(bstack1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ⁦")):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⁧"): bstack1l1_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤ⁨"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⁩"): env.get(bstack1l1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ⁪")),
            bstack1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⁫"): bstack1l1_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧ⁬") if env.get(bstack1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ⁭")) else None,
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⁮"): env.get(bstack1l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ⁯"))
        }
    if any([env.get(bstack1l1_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ⁰")), env.get(bstack1l1_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦⁱ")), env.get(bstack1l1_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ⁲"))]):
        return {
            bstack1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⁳"): bstack1l1_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧ⁴"),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⁵"): None,
            bstack1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⁶"): env.get(bstack1l1_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨ⁷")),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⁸"): env.get(bstack1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⁹"))
        }
    if env.get(bstack1l1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣ⁺")):
        return {
            bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⁻"): bstack1l1_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥ⁼"),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⁽"): env.get(bstack1l1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ⁾")),
            bstack1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧⁿ"): bstack1l1_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧ₀").format(env.get(bstack1l1_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨ₁"))) if env.get(bstack1l1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤ₂")) else None,
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ₃"): env.get(bstack1l1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ₄"))
        }
    if bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥ₅"))):
        return {
            bstack1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ₆"): bstack1l1_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧ₇"),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ₈"): env.get(bstack1l1_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥ₉")),
            bstack1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ₊"): env.get(bstack1l1_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦ₋")),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ₌"): env.get(bstack1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ₍"))
        }
    if bstack1l11llll_opy_(env.get(bstack1l1_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧ₎"))):
        return {
            bstack1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ₏"): bstack1l1_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢₐ"),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥₑ"): bstack1l1_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤₒ").format(env.get(bstack1l1_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ₓ")), env.get(bstack1l1_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧₔ")), env.get(bstack1l1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫₕ"))),
            bstack1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢₖ"): env.get(bstack1l1_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣₗ")),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨₘ"): env.get(bstack1l1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣₙ"))
        }
    if env.get(bstack1l1_opy_ (u"ࠤࡆࡍࠧₚ")) == bstack1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣₛ") and env.get(bstack1l1_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦₜ")) == bstack1l1_opy_ (u"ࠧ࠷ࠢ₝"):
        return {
            bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ₞"): bstack1l1_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢ₟"),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ₠"): bstack1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧ₡").format(env.get(bstack1l1_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧ₢"))),
            bstack1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ₣"): None,
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ₤"): None,
        }
    if env.get(bstack1l1_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ₥")):
        return {
            bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ₦"): bstack1l1_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥ₧"),
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ₨"): None,
            bstack1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ₩"): env.get(bstack1l1_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧ₪")),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ₫"): env.get(bstack1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ€"))
        }
    if any([env.get(bstack1l1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥ₭")), env.get(bstack1l1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣ₮")), env.get(bstack1l1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢ₯")), env.get(bstack1l1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦ₰"))]):
        return {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ₱"): bstack1l1_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣ₲"),
            bstack1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ₳"): None,
            bstack1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ₴"): env.get(bstack1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ₵")) or None,
            bstack1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ₶"): env.get(bstack1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ₷"), 0)
        }
    if env.get(bstack1l1_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ₸")):
        return {
            bstack1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ₹"): bstack1l1_opy_ (u"ࠨࡇࡰࡅࡇࠦ₺"),
            bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ₻"): None,
            bstack1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ₼"): env.get(bstack1l1_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ₽")),
            bstack1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ₾"): env.get(bstack1l1_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ₿"))
        }
    if env.get(bstack1l1_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⃀")):
        return {
            bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⃁"): bstack1l1_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥ⃂"),
            bstack1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⃃"): env.get(bstack1l1_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ⃄")),
            bstack1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⃅"): env.get(bstack1l1_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ⃆")),
            bstack1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⃇"): env.get(bstack1l1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⃈"))
        }
    return {bstack1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⃉"): None}
def get_host_info():
    return {
        bstack1l1_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥ⃊"): platform.node(),
        bstack1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ⃋"): platform.system(),
        bstack1l1_opy_ (u"ࠥࡸࡾࡶࡥࠣ⃌"): platform.machine(),
        bstack1l1_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ⃍"): platform.version(),
        bstack1l1_opy_ (u"ࠧࡧࡲࡤࡪࠥ⃎"): platform.architecture()[0]
    }
def bstack11l111ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111l1ll1ll_opy_():
    if global_config.get_property(bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ⃏")):
        return bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⃐")
    return bstack1l1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧ⃑")
def bstack111111ll11l_opy_(driver):
    info = {
        bstack1l1_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ⃒"): driver.capabilities,
        bstack1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ⃓ࠧ"): driver.session_id,
        bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ⃔"): driver.capabilities.get(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ⃕"), None),
        bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⃖"): driver.capabilities.get(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⃗"), None),
        bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯⃘ࠪ"): driver.capabilities.get(bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ⃙"), None),
        bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ⃚࠭"):driver.capabilities.get(bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⃛"), None),
    }
    if bstack1111l1ll1ll_opy_() == bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⃜"):
        if bstack1lll1lll1_opy_():
            info[bstack1l1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ⃝")] = bstack1l1_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⃞")
        elif driver.capabilities.get(bstack1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⃟"), {}).get(bstack1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⃠"), False):
            info[bstack1l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ⃡")] = bstack1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⃢")
        else:
            info[bstack1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭⃣")] = bstack1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⃤")
    return info
def bstack1lll1lll1_opy_():
    if global_config.get_property(bstack1l1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ⃥࠭")):
        return True
    if bstack1l11llll_opy_(os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆ⃦ࠩ"), None)):
        return True
    return False
def bstack11111l111l1_opy_(bstack1111111l1ll_opy_, url, response, headers=None, data=None):
    bstack1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡅࡹ࡮ࡲࡤࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡲ࡯ࡨࠢࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠳ࡷ࡫ࡳࡱࡱࡱࡷࡪࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡱࡶࡧࡶࡸࡤࡺࡹࡱࡧ࠽ࠤࡍ࡚ࡔࡑࠢࡰࡩࡹ࡮࡯ࡥࠢࠫࡋࡊ࡚ࠬࠡࡒࡒࡗ࡙࠲ࠠࡦࡶࡦ࠲࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡶࡴ࡯࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡕࡓࡎ࠲ࡩࡳࡪࡰࡰ࡫ࡱࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡴࡨࡪࡦࡥࡷࠤ࡫ࡸ࡯࡮ࠢࡵࡩࡶࡻࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡮ࡥࡢࡦࡨࡶࡸࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡪࡨࡥࡩ࡫ࡲࡴࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩࡧࡴࡢ࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤࡏ࡙ࡏࡏࠢࡧࡥࡹࡧࠠࡰࡴࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡇࡱࡵࡱࡦࡺࡴࡦࡦࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥࠡࡹ࡬ࡸ࡭ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡤࡢࡶࡤࠎࠥࠦࠠࠡࠤࠥࠦ⃧")
    bstack11111l1ll11_opy_ = {
        bstack1l1_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶ⃨ࠦ"): headers,
        bstack1l1_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦ⃩"): bstack1111111l1ll_opy_.upper(),
        bstack1l1_opy_ (u"ࠧࡧࡧࡦࡰࡷ⃪ࠦ"): None,
        bstack1l1_opy_ (u"ࠨࡥ࡯ࡦࡳࡳ࡮ࡴࡴ⃫ࠣ"): url,
        bstack1l1_opy_ (u"ࠢ࡫ࡵࡲࡲ⃬ࠧ"): data
    }
    try:
        bstack1111ll11111_opy_ = response.json()
        if isinstance(bstack1111ll11111_opy_, dict) and bstack1111ll11111_opy_.get(bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃭"), {}).get(bstack1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵ⃮ࠪ"), {}).get(bstack1l1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶ⃯ࠫ")):
            bstack11111ll11l1_opy_ = json.loads(json.dumps(bstack1111ll11111_opy_))
            bstack11111ll11l1_opy_[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃰")][bstack1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⃱")][bstack1l1_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ⃲")] = bstack1l1_opy_ (u"ࠢ࡜ࡴࡨࡨࡦࡩࡴࡦࡦࠣࡪࡴࡸࠠࡣࡴࡨࡺ࡮ࡺࡹ࡞ࠤ⃳")
            bstack1111ll11111_opy_ = bstack11111ll11l1_opy_
    except Exception:
        bstack1111ll11111_opy_ = response.text
    bstack1111l1ll11l_opy_ = {
        bstack1l1_opy_ (u"ࠣࡤࡲࡨࡾࠨ⃴"): bstack1111ll11111_opy_,
        bstack1l1_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࡅࡲࡨࡪࠨ⃵"): response.status_code
    }
    return {
        bstack1l1_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ⃶"): bstack11111l1ll11_opy_,
        bstack1l1_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ⃷"): bstack1111l1ll11l_opy_
    }
def bstack1l111l1111_opy_(bstack1111111l1ll_opy_, url, data, config):
    headers = config.get(bstack1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭⃸"), None)
    proxies = bstack1l111ll1l_opy_(config, url)
    auth = config.get(bstack1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ⃹"), None)
    response = requests.request(
            bstack1111111l1ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack11111l111l1_opy_(bstack1111111l1ll_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1l1_opy_ (u"ࠧ࠭ࠩ⃺"), bstack1l1_opy_ (u"ࠨ࠼ࠪ⃻"))))
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࡼࡿࠥ⃼").format(e))
    return response
def bstack11lll111ll_opy_(bstack11l1ll11l1_opy_, size):
    bstack1lll1lll1l_opy_ = []
    while len(bstack11l1ll11l1_opy_) > size:
        bstack11lll1l1l_opy_ = bstack11l1ll11l1_opy_[:size]
        bstack1lll1lll1l_opy_.append(bstack11lll1l1l_opy_)
        bstack11l1ll11l1_opy_ = bstack11l1ll11l1_opy_[size:]
    bstack1lll1lll1l_opy_.append(bstack11l1ll11l1_opy_)
    return bstack1lll1lll1l_opy_
def bstack11111l1111l_opy_(message, bstack11111ll1l1l_opy_=False):
    os.write(1, bytes(message, bstack1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⃽")))
    os.write(1, bytes(bstack1l1_opy_ (u"ࠫࡡࡴࠧ⃾"), bstack1l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⃿")))
    if bstack11111ll1l1l_opy_:
        with open(bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬ℀") + os.environ[bstack1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭℁")] + bstack1l1_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ℂ"), bstack1l1_opy_ (u"ࠩࡤࠫ℃")) as f:
            f.write(message + bstack1l1_opy_ (u"ࠪࡠࡳ࠭℄"))
def bstack1ll11111l1_opy_():
    return os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ℅")].lower() == bstack1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪ℆")
def current_time():
    return bstack1lllll11ll1_opy_().replace(tzinfo=None).isoformat() + bstack1l1_opy_ (u"࡚࠭ࠨℇ")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1_opy_ (u"࡛ࠧࠩ℈"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1_opy_ (u"ࠨ࡜ࠪ℉")))).total_seconds() * 1000
def bstack1llllllll111_opy_(timestamp):
    return bstack1lllllll1lll_opy_(timestamp).isoformat() + bstack1l1_opy_ (u"ࠩ࡝ࠫℊ")
def bstack11111lll1ll_opy_(bstack111111l11ll_opy_):
    date_format = bstack1l1_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨℋ")
    bstack1111111llll_opy_ = datetime.datetime.strptime(bstack111111l11ll_opy_, date_format)
    return bstack1111111llll_opy_.isoformat() + bstack1l1_opy_ (u"ࠫ࡟࠭ℌ")
def bstack1111111ll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬℍ")
    else:
        return bstack1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ℎ")
def bstack1l11llll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬℏ")
def bstack1111l1ll1l1_opy_(val):
    return val.__str__().lower() == bstack1l1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧℐ")
def error_handler(bstack11111l11l11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11111l11l11_opy_ as e:
                print(bstack1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤℑ").format(func.__name__, bstack11111l11l11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11111l11l1l_opy_(bstack11111l1l1l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111l1l1l1_opy_(cls, *args, **kwargs)
            except bstack11111l11l11_opy_ as e:
                print(bstack1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥℒ").format(bstack11111l1l1l1_opy_.__name__, bstack11111l11l11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11111l11l1l_opy_
    else:
        return decorator
def bstack111l11ll_opy_(bstack1lll11ll1l1_opy_):
    if os.getenv(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧℓ")) is not None:
        return bstack1l11llll_opy_(os.getenv(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ℔")))
    if bstack1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪℕ") in bstack1lll11ll1l1_opy_ and bstack1111l1ll1l1_opy_(bstack1lll11ll1l1_opy_[bstack1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ№")]):
        return False
    if bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ℗") in bstack1lll11ll1l1_opy_ and bstack1111l1ll1l1_opy_(bstack1lll11ll1l1_opy_[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ℘")]):
        return False
    return True
def bstack1111111ll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack1lllllllll1l_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥℙ"), None)
        return bstack1lllllllll1l_opy_ is None or bstack1lllllllll1l_opy_ == bstack1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣℚ")
    except Exception as e:
        return False
def bstack11lll11l1_opy_(hub_url, CONFIG):
    if bstack1lllllll1l_opy_() <= version.parse(bstack1l1_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬℛ")):
        if hub_url:
            return bstack1l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢℜ") + hub_url + bstack1l1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦℝ")
        return bstack1l1l11ll11_opy_
    if hub_url:
        return bstack1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ℞") + hub_url + bstack1l1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ℟")
    return HTTPS_HUB
def bstack11111ll1ll1_opy_():
    return isinstance(os.getenv(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩ℠")), str)
def bstack1llll111l1_opy_(url):
    return urlparse(url).hostname
def bstack1l1ll1111_opy_(hostname):
    for bstack1l11l11ll1_opy_ in bstack11llll1l1l_opy_:
        regex = re.compile(bstack1l11l11ll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1lllllllllll_opy_(bstack1111l11l1l1_opy_, file_name, logger):
    bstack1lll111ll_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠫࢃ࠭℡")), bstack1111l11l1l1_opy_)
    try:
        if not os.path.exists(bstack1lll111ll_opy_):
            os.makedirs(bstack1lll111ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠬࢄࠧ™")), bstack1111l11l1l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1_opy_ (u"࠭ࡷࠨ℣")):
                pass
            with open(file_path, bstack1l1_opy_ (u"ࠢࡸ࠭ࠥℤ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l11l11lll_opy_.format(str(e)))
def bstack1111l1l1lll_opy_(file_name, key, value, logger):
    file_path = bstack1lllllllllll_opy_(bstack1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ℥"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll111l11_opy_ = json.load(open(file_path, bstack1l1_opy_ (u"ࠩࡵࡦࠬΩ")))
        else:
            bstack1ll111l11_opy_ = {}
        bstack1ll111l11_opy_[key] = value
        with open(file_path, bstack1l1_opy_ (u"ࠥࡻ࠰ࠨ℧")) as outfile:
            json.dump(bstack1ll111l11_opy_, outfile)
def bstack11ll111l1l_opy_(file_name, logger):
    file_path = bstack1lllllllllll_opy_(bstack1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫℨ"), file_name, logger)
    bstack1ll111l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1_opy_ (u"ࠬࡸࠧ℩")) as bstack1l11ll1l_opy_:
            bstack1ll111l11_opy_ = json.load(bstack1l11ll1l_opy_)
    return bstack1ll111l11_opy_
def bstack1ll1ll1ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪK") + file_path + bstack1l1_opy_ (u"ࠧࠡࠩÅ") + str(e))
def bstack1lllllll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥℬ")
def bstack1lll1ll1ll_opy_(config):
    if bstack1l1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨℭ") in config:
        del (config[bstack1l1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ℮")])
        return False
    if bstack1lllllll1l_opy_() < version.parse(bstack1l1_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪℯ")):
        return False
    if bstack1lllllll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫℰ")):
        return True
    if bstack1l1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ℱ") in config and config[bstack1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧℲ")] is False:
        return False
    else:
        return True
def bstack1l11lll11_opy_(args_list, bstack1111111l11l_opy_):
    index = -1
    for value in bstack1111111l11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack111lll11lll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack111lll11lll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llllll1l11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨℳ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩℴ"), exception=exception)
    def bstack1ll1llll1ll_opy_(self):
        if self.result != bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪℵ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢℶ") in self.exception_type:
            return bstack1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨℷ")
        return bstack1l1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢℸ")
    def bstack1111l11l11l_opy_(self):
        if self.result != bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧℹ"):
            return None
        if self.bstack1llllll1l11_opy_:
            return self.bstack1llllll1l11_opy_
        return bstack111111l1l1l_opy_(self.exception)
def bstack111111l1l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111111lll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1lll111l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11lllll1l1_opy_(config, logger):
    try:
        import playwright
        bstack11111111ll1_opy_ = playwright.__file__
        bstack11111llll1l_opy_ = os.path.split(bstack11111111ll1_opy_)
        bstack1111l1l11ll_opy_ = bstack11111llll1l_opy_[0] + bstack1l1_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫ℺")
        os.environ[bstack1l1_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬ℻")] = bstack1l1l11111l_opy_(config)
        with open(bstack1111l1l11ll_opy_, bstack1l1_opy_ (u"ࠪࡶࠬℼ")) as f:
            file_content = f.read()
            bstack1lllllll1l11_opy_ = bstack1l1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪℽ")
            bstack1111l1ll111_opy_ = file_content.find(bstack1lllllll1l11_opy_)
            if bstack1111l1ll111_opy_ == -1:
              process = subprocess.Popen(bstack1l1_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤℾ"), shell=True, cwd=bstack11111llll1l_opy_[0])
              process.wait()
              bstack1111ll11lll_opy_ = bstack1l1_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ℿ")
              bstack11111llllll_opy_ = bstack1l1_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦ⅀")
              bstack1111l111l1l_opy_ = file_content.replace(bstack1111ll11lll_opy_, bstack11111llllll_opy_)
              with open(bstack1111l1l11ll_opy_, bstack1l1_opy_ (u"ࠨࡹࠪ⅁")) as f:
                f.write(bstack1111l111l1l_opy_)
    except Exception as e:
        logger.error(bstack11l1llllll_opy_.format(str(e)))
def bstack1ll11ll11l_opy_():
  try:
    bstack111111l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩ⅂"))
    bstack111111l111l_opy_ = []
    if os.path.exists(bstack111111l1111_opy_):
      with open(bstack111111l1111_opy_) as f:
        bstack111111l111l_opy_ = json.load(f)
      os.remove(bstack111111l1111_opy_)
    return bstack111111l111l_opy_
  except:
    pass
  return []
def bstack111lll1ll_opy_(bstack11llll1ll_opy_):
  try:
    bstack111111l111l_opy_ = []
    bstack111111l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ⅃"))
    if os.path.exists(bstack111111l1111_opy_):
      with open(bstack111111l1111_opy_) as f:
        bstack111111l111l_opy_ = json.load(f)
    bstack111111l111l_opy_.append(bstack11llll1ll_opy_)
    with open(bstack111111l1111_opy_, bstack1l1_opy_ (u"ࠫࡼ࠭⅄")) as f:
        json.dump(bstack111111l111l_opy_, f)
  except:
    pass
def bstack11lll1ll11_opy_(logger, bstack1111ll1ll11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨⅅ"), bstack1l1_opy_ (u"࠭ࠧⅆ"))
    if test_name == bstack1l1_opy_ (u"ࠧࠨⅇ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧⅈ"), bstack1l1_opy_ (u"ࠩࠪⅉ"))
    bstack11111l1ll1l_opy_ = bstack1l1_opy_ (u"ࠪ࠰ࠥ࠭⅊").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111ll1ll11_opy_:
        bstack1ll11l11ll_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⅋"), bstack1l1_opy_ (u"ࠬ࠶ࠧ⅌"))
        bstack1111l1l1l_opy_ = {bstack1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⅍"): test_name, bstack1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ⅎ"): bstack11111l1ll1l_opy_, bstack1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⅏"): bstack1ll11l11ll_opy_}
        bstack1llllllllll1_opy_ = []
        bstack1111l11ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⅐"))
        if os.path.exists(bstack1111l11ll11_opy_):
            with open(bstack1111l11ll11_opy_) as f:
                bstack1llllllllll1_opy_ = json.load(f)
        bstack1llllllllll1_opy_.append(bstack1111l1l1l_opy_)
        with open(bstack1111l11ll11_opy_, bstack1l1_opy_ (u"ࠪࡻࠬ⅑")) as f:
            json.dump(bstack1llllllllll1_opy_, f)
    else:
        bstack1111l1l1l_opy_ = {bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⅒"): test_name, bstack1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⅓"): bstack11111l1ll1l_opy_, bstack1l1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⅔"): str(multiprocessing.current_process().name)}
        if bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ⅕") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1111l1l1l_opy_)
  except Exception as e:
      logger.warn(bstack1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ⅖").format(e))
def bstack11ll1ll1l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ⅗"))
    try:
      bstack1llllllll1l1_opy_ = []
      bstack1111l1l1l_opy_ = {bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ⅘"): test_name, bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⅙"): error_message, bstack1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ⅚"): index}
      bstack111111l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ⅛"))
      if os.path.exists(bstack111111l1ll1_opy_):
          with open(bstack111111l1ll1_opy_) as f:
              bstack1llllllll1l1_opy_ = json.load(f)
      bstack1llllllll1l1_opy_.append(bstack1111l1l1l_opy_)
      with open(bstack111111l1ll1_opy_, bstack1l1_opy_ (u"ࠧࡸࠩ⅜")) as f:
          json.dump(bstack1llllllll1l1_opy_, f)
    except Exception as e:
      logger.warn(bstack1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ⅝").format(e))
    return
  bstack1llllllll1l1_opy_ = []
  bstack1111l1l1l_opy_ = {bstack1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⅞"): test_name, bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⅟"): error_message, bstack1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪⅠ"): index}
  bstack111111l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭Ⅱ"))
  lock_file = bstack111111l1ll1_opy_ + bstack1l1_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬⅢ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111111l1ll1_opy_):
          with open(bstack111111l1ll1_opy_, bstack1l1_opy_ (u"ࠧࡳࠩⅣ")) as f:
              content = f.read().strip()
              if content:
                  bstack1llllllll1l1_opy_ = json.load(open(bstack111111l1ll1_opy_))
      bstack1llllllll1l1_opy_.append(bstack1111l1l1l_opy_)
      with open(bstack111111l1ll1_opy_, bstack1l1_opy_ (u"ࠨࡹࠪⅤ")) as f:
          json.dump(bstack1llllllll1l1_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡦࡪ࡮ࡨࠤࡱࡵࡣ࡬࡫ࡱ࡫࠿ࠦࡻࡾࠤⅥ").format(e))
def bstack1llll1l1_opy_(bstack1l11ll1ll1_opy_, name, logger):
  try:
    bstack1111l1l1l_opy_ = {bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨⅦ"): name, bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪⅧ"): bstack1l11ll1ll1_opy_, bstack1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫⅨ"): str(threading.current_thread()._name)}
    return bstack1111l1l1l_opy_
  except Exception as e:
    logger.warn(bstack1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥⅩ").format(e))
  return
def bstack1111111ll11_opy_():
    return platform.system() == bstack1l1_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨⅪ")
def bstack11l11lllll_opy_(bstack111111ll1ll_opy_, config, logger):
    bstack111111l1lll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111111ll1ll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢⅫ").format(e))
    return bstack111111l1lll_opy_
def bstack11111l1llll_opy_(bstack11111lll1l1_opy_, bstack1111ll111l1_opy_):
    bstack11111l1l1ll_opy_ = version.parse(bstack11111lll1l1_opy_)
    bstack11111lll111_opy_ = version.parse(bstack1111ll111l1_opy_)
    if bstack11111l1l1ll_opy_ > bstack11111lll111_opy_:
        return 1
    elif bstack11111l1l1ll_opy_ < bstack11111lll111_opy_:
        return -1
    else:
        return 0
def bstack1lllll11ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1lllllll1lll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l11ll1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l111lll11_opy_(options, framework, config, bstack1l1ll111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1_opy_ (u"ࠩࡪࡩࡹ࠭Ⅼ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1lll1l1l_opy_ = caps.get(bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫⅭ"))
    bstack1111l1111ll_opy_ = True
    bstack1l11ll11l_opy_ = os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩⅮ")]
    bstack1l11ll11111_opy_ = config.get(bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬⅯ"), False)
    if bstack1l11ll11111_opy_:
        bstack1l1l1l1ll11_opy_ = config.get(bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ⅰ"), {})
        bstack1l1l1l1ll11_opy_[bstack1l1_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪⅱ")] = os.getenv(bstack1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ⅲ"))
        bstack11l1l1ll1_opy_ = json.loads(os.getenv(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪⅳ"), bstack1l1_opy_ (u"ࠪࡿࢂ࠭ⅴ"))).get(bstack1l1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬⅵ"))
    if bstack1111l1ll1l1_opy_(caps.get(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫⅶ"))) or bstack1111l1ll1l1_opy_(caps.get(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭ⅷ"))):
        bstack1111l1111ll_opy_ = False
    if bstack1lll1ll1ll_opy_({bstack1l1_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢⅸ"): bstack1111l1111ll_opy_}):
        bstack1lll1l1l_opy_ = bstack1lll1l1l_opy_ or {}
        bstack1lll1l1l_opy_[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪⅹ")] = bstack1111l11ll1l_opy_(framework)
        bstack1lll1l1l_opy_[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫⅺ")] = bstack1ll11111l1_opy_()
        bstack1lll1l1l_opy_[bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ⅻ")] = bstack1l11ll11l_opy_
        bstack1lll1l1l_opy_[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ⅼ")] = bstack1l1ll111l_opy_
        if bstack1l11ll11111_opy_:
            bstack1lll1l1l_opy_[bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬⅽ")] = bstack1l11ll11111_opy_
            bstack1lll1l1l_opy_[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ⅾ")] = bstack1l1l1l1ll11_opy_
            bstack1lll1l1l_opy_[bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧⅿ")][bstack1l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩↀ")] = bstack11l1l1ll1_opy_
        if getattr(options, bstack1l1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪↁ"), None):
            options.set_capability(bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫↂ"), bstack1lll1l1l_opy_)
        else:
            options[bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬↃ")] = bstack1lll1l1l_opy_
    else:
        if getattr(options, bstack1l1_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ↄ"), None):
            options.set_capability(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧↅ"), bstack1111l11ll1l_opy_(framework))
            options.set_capability(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨↆ"), bstack1ll11111l1_opy_())
            options.set_capability(bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪↇ"), bstack1l11ll11l_opy_)
            options.set_capability(bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪↈ"), bstack1l1ll111l_opy_)
            if bstack1l11ll11111_opy_:
                options.set_capability(bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ↉"), bstack1l11ll11111_opy_)
                options.set_capability(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ↊"), bstack1l1l1l1ll11_opy_)
                options.set_capability(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ↋"), bstack11l1l1ll1_opy_)
        else:
            options[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ↌")] = bstack1111l11ll1l_opy_(framework)
            options[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ↍")] = bstack1ll11111l1_opy_()
            options[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ↎")] = bstack1l11ll11l_opy_
            options[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ↏")] = bstack1l1ll111l_opy_
            if bstack1l11ll11111_opy_:
                options[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ←")] = bstack1l11ll11111_opy_
                options[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ↑")] = bstack1l1l1l1ll11_opy_
                options[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ→")][bstack1l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ↓")] = bstack11l1l1ll1_opy_
    return options
def bstack1lllllll1l1l_opy_(ws_endpoint, framework):
    bstack1l1ll111l_opy_ = global_config.get_property(bstack1l1_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ↔"))
    if ws_endpoint and len(ws_endpoint.split(bstack1l1_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ↕"))) > 1:
        ws_url = ws_endpoint.split(bstack1l1_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ↖"))[0]
        if bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭↗") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111l11ll1_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1l1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ↘"))[1]))
            bstack11111l11ll1_opy_ = bstack11111l11ll1_opy_ or {}
            bstack1l11ll11l_opy_ = os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ↙")]
            bstack11111l11ll1_opy_[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ↚")] = str(framework) + str(__version__)
            bstack11111l11ll1_opy_[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ↛")] = bstack1ll11111l1_opy_()
            bstack11111l11ll1_opy_[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ↜")] = bstack1l11ll11l_opy_
            bstack11111l11ll1_opy_[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ↝")] = bstack1l1ll111l_opy_
            ws_endpoint = ws_endpoint.split(bstack1l1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ↞"))[0] + bstack1l1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ↟") + urllib.parse.quote(json.dumps(bstack11111l11ll1_opy_))
    return ws_endpoint
def bstack111l11l111_opy_():
    global bstack11l111l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l111l1_opy_ = BrowserType.connect
    return bstack11l111l1_opy_
def bstack111111l11l1_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1lllll1ll_opy_(self, *args, **kwargs):
    global bstack11l111l1_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1l1_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ↠") in kwargs:
            kwargs[bstack1l1_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪ↡")] = bstack1lllllll1l1l_opy_(
                kwargs.get(bstack1l1_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ↢"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣ↣").format(str(e)))
    return bstack11l111l1_opy_(self, *args, **kwargs)
def bstack1111l1lll11_opy_(bstack1111l111lll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l111ll1l_opy_(bstack1111l111lll_opy_, bstack1l1_opy_ (u"ࠤࠥ↤"))
        if proxies and proxies.get(bstack1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ↥")):
            parsed_url = urlparse(proxies.get(bstack1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ↦")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ↧")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ↨")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ↩")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ↪")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1llll111_opy_(bstack1111l111lll_opy_):
    bstack1111l1l1l11_opy_ = {
        bstack111l1111ll1_opy_[bstack1111l11l1ll_opy_]: bstack1111l111lll_opy_[bstack1111l11l1ll_opy_]
        for bstack1111l11l1ll_opy_ in bstack1111l111lll_opy_
        if bstack1111l11l1ll_opy_ in bstack111l1111ll1_opy_
    }
    bstack1111l1l1l11_opy_[bstack1l1_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤ↫")] = bstack1111l1lll11_opy_(bstack1111l111lll_opy_, global_config.get_property(bstack1l1_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥ↬")))
    bstack1111ll111ll_opy_ = [element.lower() for element in bstack111l11l111l_opy_]
    bstack1111l1lll1l_opy_(bstack1111l1l1l11_opy_, bstack1111ll111ll_opy_)
    return bstack1111l1l1l11_opy_
def bstack1111l1lll1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1_opy_ (u"ࠦ࠯࠰ࠪࠫࠤ↭")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111l1lll1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111l1lll1l_opy_(item, keys)
def bstack1l111ll1111_opy_():
    bstack1111ll1l1l1_opy_ = [os.environ.get(bstack1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢ↮")), os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠨࡾࠣ↯")), bstack1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ↰")), os.path.join(bstack1l1_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭↱"), bstack1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ↲"))]
    for path in bstack1111ll1l1l1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥ↳") + str(path) + bstack1l1_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢ↴"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤ↵") + str(path) + bstack1l1_opy_ (u"ࠨࠧࠣ↶"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢ↷") + str(path) + bstack1l1_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨ↸"))
            else:
                logger.debug(bstack1l1_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦ↹") + str(path) + bstack1l1_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢ↺"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤ↻") + str(path) + bstack1l1_opy_ (u"ࠧ࠭࠮ࠣ↼"))
            return path
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦ↽") + str(e) + bstack1l1_opy_ (u"ࠢࠣ↾"))
    logger.debug(bstack1l1_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧ↿"))
    return None
@measure(event_name=EVENTS.bstack111l11ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack1lll1ll1l1l_opy_(binary_path, bstack1lll1ll111l_opy_, bs_config):
    logger.debug(bstack1l1_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣ⇀").format(binary_path))
    bstack11111l111ll_opy_ = bstack1l1_opy_ (u"ࠪࠫ⇁")
    bstack1111111l1l1_opy_ = {
        bstack1l1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⇂"): __version__,
        bstack1l1_opy_ (u"ࠧࡵࡳࠣ⇃"): platform.system(),
        bstack1l1_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢ⇄"): platform.machine(),
        bstack1l1_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ⇅"): bstack1l1_opy_ (u"ࠨ࠲ࠪ⇆"),
        bstack1l1_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣ⇇"): bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⇈")
    }
    bstack1111l11llll_opy_(bstack1111111l1l1_opy_)
    try:
        if binary_path:
            if bstack1111111ll11_opy_():
                bstack1111111l1l1_opy_[bstack1l1_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⇉")] = subprocess.check_output([binary_path, bstack1l1_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ⇊")]).strip().decode(bstack1l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ⇋"))
            else:
                bstack1111111l1l1_opy_[bstack1l1_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⇌")] = subprocess.check_output([binary_path, bstack1l1_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ⇍")], stderr=subprocess.DEVNULL).strip().decode(bstack1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ⇎"))
        response = requests.request(
            bstack1l1_opy_ (u"ࠪࡋࡊ࡚ࠧ⇏"),
            url=bstack11l11l1l1l_opy_(bstack111l1l111ll_opy_),
            headers=None,
            auth=(bs_config[bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭⇐")], bs_config[bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ⇑")]),
            json=None,
            params=bstack1111111l1l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1_opy_ (u"࠭ࡵࡳ࡮ࠪ⇒") in data.keys() and bstack1l1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⇓") in data.keys():
            logger.debug(bstack1l1_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤ⇔").format(bstack1111111l1l1_opy_[bstack1l1_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⇕")]))
            if bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭⇖") in os.environ:
                logger.debug(bstack1l1_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡣࡶࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠠࡪࡵࠣࡷࡪࡺࠢ⇗"))
                data[bstack1l1_opy_ (u"ࠬࡻࡲ࡭ࠩ⇘")] = os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ⇙")]
            bstack1111ll1l11l_opy_ = bstack1111ll1111l_opy_(data[bstack1l1_opy_ (u"ࠧࡶࡴ࡯ࠫ⇚")], bstack1lll1ll111l_opy_)
            bstack11111l111ll_opy_ = os.path.join(bstack1lll1ll111l_opy_, bstack1111ll1l11l_opy_)
            os.chmod(bstack11111l111ll_opy_, 0o777) # bstack1llllllll1ll_opy_ permission
            return bstack11111l111ll_opy_
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣ⇛").format(e))
    return binary_path
def bstack1111l11llll_opy_(bstack1111111l1l1_opy_):
    try:
        if bstack1l1_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨ⇜") not in bstack1111111l1l1_opy_[bstack1l1_opy_ (u"ࠪࡳࡸ࠭⇝")].lower():
            return
        if os.path.exists(bstack1l1_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ⇞")):
            with open(bstack1l1_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ⇟"), bstack1l1_opy_ (u"ࠨࡲࠣ⇠")) as f:
                bstack1111l1lllll_opy_ = {}
                for line in f:
                    if bstack1l1_opy_ (u"ࠢ࠾ࠤ⇡") in line:
                        key, value = line.rstrip().split(bstack1l1_opy_ (u"ࠣ࠿ࠥ⇢"), 1)
                        bstack1111l1lllll_opy_[key] = value.strip(bstack1l1_opy_ (u"ࠩࠥࡠࠬ࠭⇣"))
                bstack1111111l1l1_opy_[bstack1l1_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪ⇤")] = bstack1111l1lllll_opy_.get(bstack1l1_opy_ (u"ࠦࡎࡊࠢ⇥"), bstack1l1_opy_ (u"ࠧࠨ⇦"))
        elif os.path.exists(bstack1l1_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡦࡲࡰࡪࡰࡨ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧ⇧")):
            bstack1111111l1l1_opy_[bstack1l1_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧ⇨")] = bstack1l1_opy_ (u"ࠨࡣ࡯ࡴ࡮ࡴࡥࠨ⇩")
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡧ࡭ࡸࡺࡲࡰࠢࡲࡪࠥࡲࡩ࡯ࡷࡻࠦ⇪") + e)
@measure(event_name=EVENTS.bstack111l11l11l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack1111ll1111l_opy_(bstack11111ll11ll_opy_, bstack1111l111111_opy_):
    logger.debug(bstack1l1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧ⇫") + str(bstack11111ll11ll_opy_) + bstack1l1_opy_ (u"ࠦࠧ⇬"))
    zip_path = os.path.join(bstack1111l111111_opy_, bstack1l1_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦ⇭"))
    bstack1111ll1l11l_opy_ = bstack1l1_opy_ (u"࠭ࠧ⇮")
    with requests.get(bstack11111ll11ll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1_opy_ (u"ࠢࡸࡤࠥ⇯")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥ⇰"))
    with zipfile.ZipFile(zip_path, bstack1l1_opy_ (u"ࠩࡵࠫ⇱")) as zip_ref:
        bstack11111111l1l_opy_ = zip_ref.namelist()
        if len(bstack11111111l1l_opy_) > 0:
            bstack1111ll1l11l_opy_ = bstack11111111l1l_opy_[0] # bstack1111l11lll1_opy_ bstack111l111llll_opy_ will be bstack11111111l11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1111l111111_opy_)
        logger.debug(bstack1l1_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤ⇲") + str(bstack1111l111111_opy_) + bstack1l1_opy_ (u"ࠦࠬࠨ⇳"))
    os.remove(zip_path)
    return bstack1111ll1l11l_opy_
def get_cli_dir():
    bstack1lllllllll11_opy_ = bstack1l111ll1111_opy_()
    if bstack1lllllllll11_opy_:
        bstack1lll1ll111l_opy_ = os.path.join(bstack1lllllllll11_opy_, bstack1l1_opy_ (u"ࠧࡩ࡬ࡪࠤ⇴"))
        if not os.path.exists(bstack1lll1ll111l_opy_):
            os.makedirs(bstack1lll1ll111l_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1ll111l_opy_
    else:
        raise FileNotFoundError(bstack1l1_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤ⇵"))
def bstack1lll1ll1lll_opy_(bstack1lll1ll111l_opy_):
    bstack1l1_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦ⇶")
    bstack111111111l1_opy_ = [
        os.path.join(bstack1lll1ll111l_opy_, f)
        for f in os.listdir(bstack1lll1ll111l_opy_)
        if os.path.isfile(os.path.join(bstack1lll1ll111l_opy_, f)) and f.startswith(bstack1l1_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤ⇷"))
    ]
    if len(bstack111111111l1_opy_) > 0:
        return max(bstack111111111l1_opy_, key=os.path.getmtime) # get bstack1111ll11l11_opy_ binary
    return bstack1l1_opy_ (u"ࠤࠥ⇸")
def bstack111ll11llll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11ll1llll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l11ll1llll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l1lll11_opy_(data, keys, default=None):
    bstack1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡦ࡬ࡥ࡭ࡻࠣ࡫ࡪࡺࠠࡢࠢࡱࡩࡸࡺࡥࡥࠢࡹࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩࡧࡴࡢ࠼ࠣࡘ࡭࡫ࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸࠥࡺ࡯ࠡࡶࡵࡥࡻ࡫ࡲࡴࡧ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡ࡭ࡨࡽࡸࡀࠠࡂࠢ࡯࡭ࡸࡺࠠࡰࡨࠣ࡯ࡪࡿࡳ࠰࡫ࡱࡨ࡮ࡩࡥࡴࠢࡵࡩࡵࡸࡥࡴࡧࡱࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡨࡪࡦࡻ࡬ࡵ࠼࡚ࠣࡦࡲࡵࡦࠢࡷࡳࠥࡸࡥࡵࡷࡵࡲࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡶࡪࡺࡵࡳࡰ࠽ࠤ࡙࡮ࡥࠡࡸࡤࡰࡺ࡫ࠠࡢࡶࠣࡸ࡭࡫ࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡣࡷ࡬࠱ࠦ࡯ࡳࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ⇹")
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
def bstack1111l111l_opy_(bstack1111l1l1ll1_opy_, key, value):
    bstack1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡺ࡯ࡳࡧࠣࡇࡑࡏࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠡ࡯ࡤࡴࡵ࡯࡮ࡨࠢ࡬ࡲࠥࡺࡨࡦࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣ࡭࡫ࡢࡩࡳࡼ࡟ࡷࡣࡵࡷࡤࡳࡡࡱ࠼ࠣࡈ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠢࡰࡥࡵࡶࡩ࡯ࡩࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡏࡪࡿࠠࡧࡴࡲࡱࠥࡉࡌࡊࡡࡆࡅࡕ࡙࡟ࡕࡑࡢࡇࡔࡔࡆࡊࡉࠍࠤࠥࠦࠠࠡࠢࠣࠤࡻࡧ࡬ࡶࡧ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࡯࡭ࡳ࡫ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠍࠤࠥࠦࠠࠣࠤࠥ⇺")
    if key in bstack1111l1ll11_opy_:
        bstack1l1l1l111_opy_ = bstack1111l1ll11_opy_[key]
        if isinstance(bstack1l1l1l111_opy_, list):
            for env_name in bstack1l1l1l111_opy_:
                bstack1111l1l1ll1_opy_[env_name] = value
        else:
            bstack1111l1l1ll1_opy_[bstack1l1l1l111_opy_] = value