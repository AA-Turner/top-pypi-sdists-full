# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
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
from unittest import result
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll11ll1l_opy_, bstack1ll1ll11l_opy_, bstack1l1ll1111l_opy_,
                                    bstack11l1lll1111_opy_, bstack11l1ll11111_opy_, bstack11l1ll1ll11_opy_, bstack11l1ll11lll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1ll11l1_opy_, bstack1ll1l1111_opy_
from bstack_utils.proxy import bstack11l1l111ll_opy_, bstack1l11l11ll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack11l1111l1_opy_
from bstack_utils.bstack1llll111ll_opy_ import bstack11l11l11_opy_
from browserstack_sdk._version import __version__
bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
logger = bstack11l1111l1_opy_.get_logger(__name__, bstack11l1111l1_opy_.bstack1lll11llll1_opy_())
def bstack11ll1ll11l1_opy_(config):
    return config[bstack1111l1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᬂ")]
def bstack11lll11111l_opy_(config):
    return config[bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᬃ")]
def bstack11llll111l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111ll1ll1l1_opy_(obj):
    values = []
    bstack11l11ll11l1_opy_ = re.compile(bstack1111l1l_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦᬄ"), re.I)
    for key in obj.keys():
        if bstack11l11ll11l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111llll111l_opy_(config):
    tags = []
    tags.extend(bstack111ll1ll1l1_opy_(os.environ))
    tags.extend(bstack111ll1ll1l1_opy_(config))
    return tags
def bstack111lll111l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1111l111_opy_(bstack11l111111l1_opy_):
    if not bstack11l111111l1_opy_:
        return bstack1111l1l_opy_ (u"ࠨࠩᬅ")
    return bstack1111l1l_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥᬆ").format(bstack11l111111l1_opy_.name, bstack11l111111l1_opy_.email)
def bstack11ll1l1lll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111ll1l1111_opy_ = repo.common_dir
        info = {
            bstack1111l1l_opy_ (u"ࠥࡷ࡭ࡧࠢᬇ"): repo.head.commit.hexsha,
            bstack1111l1l_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢᬈ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1111l1l_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧᬉ"): repo.active_branch.name,
            bstack1111l1l_opy_ (u"ࠨࡴࡢࡩࠥᬊ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1111l1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥᬋ"): bstack11l1111l111_opy_(repo.head.commit.committer),
            bstack1111l1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤᬌ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1111l1l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤᬍ"): bstack11l1111l111_opy_(repo.head.commit.author),
            bstack1111l1l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣᬎ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1111l1l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᬏ"): repo.head.commit.message,
            bstack1111l1l_opy_ (u"ࠧࡸ࡯ࡰࡶࠥᬐ"): repo.git.rev_parse(bstack1111l1l_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣᬑ")),
            bstack1111l1l_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᬒ"): bstack111ll1l1111_opy_,
            bstack1111l1l_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᬓ"): subprocess.check_output([bstack1111l1l_opy_ (u"ࠤࡪ࡭ࡹࠨᬔ"), bstack1111l1l_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨᬕ"), bstack1111l1l_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢᬖ")]).strip().decode(
                bstack1111l1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᬗ")),
            bstack1111l1l_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᬘ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1111l1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤᬙ"): repo.git.rev_list(
                bstack1111l1l_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣᬚ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l11l1ll1l_opy_ = []
        for remote in remotes:
            bstack111ll1lllll_opy_ = {
                bstack1111l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬛ"): remote.name,
                bstack1111l1l_opy_ (u"ࠥࡹࡷࡲࠢᬜ"): remote.url,
            }
            bstack11l11l1ll1l_opy_.append(bstack111ll1lllll_opy_)
        bstack11l11ll111l_opy_ = {
            bstack1111l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᬝ"): bstack1111l1l_opy_ (u"ࠧ࡭ࡩࡵࠤᬞ"),
            **info,
            bstack1111l1l_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢᬟ"): bstack11l11l1ll1l_opy_
        }
        bstack11l11ll111l_opy_ = bstack111ll1l1lll_opy_(bstack11l11ll111l_opy_)
        return bstack11l11ll111l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1111l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᬠ").format(err))
        return {}
def bstack11l11l1ll11_opy_(bstack11l11l11ll1_opy_=None):
    bstack1111l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࡧ࡬࡭ࡻࠣࡪࡴࡸ࡭ࡢࡶࡷࡩࡩࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡸࡷࡪࠦࡣࡢࡵࡨࡷࠥ࡬࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧࡱ࡯ࡨࡪࡸࠠࡪࡰࠣࡸ࡭࡫ࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡪࡴࡲࡤࡦࡴࡶࠤ࠭ࡲࡩࡴࡶ࠯ࠤࡴࡶࡴࡪࡱࡱࡥࡱ࠯࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡩࡳࡱࡪࡥࡳࠢࡳࡥࡹ࡮ࡳࠡࡶࡲࠤࡪࡾࡴࡳࡣࡦࡸࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡸ࡯࡮࠰ࠣࡈࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡ࡝ࡲࡷ࠳࡭ࡥࡵࡥࡺࡨ࠭࠯࡝࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡯࡭ࡸࡺ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡧ࡭ࡨࡺࡳ࠭ࠢࡨࡥࡨ࡮ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡪࡴࡸࠠࡢࠢࡩࡳࡱࡪࡥࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᬡ")
    if not bstack11l11l11ll1_opy_: # bstack11l11l1l11l_opy_ for bstack111ll1l1ll1_opy_-repo
        bstack11l11l11ll1_opy_ = [os.getcwd()]
    results = []
    for folder in bstack11l11l11ll1_opy_:
        try:
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1111l1l_opy_ (u"ࠤࡳࡶࡎࡪࠢᬢ"): bstack1111l1l_opy_ (u"ࠥࠦᬣ"),
                bstack1111l1l_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᬤ"): [],
                bstack1111l1l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨᬥ"): [],
                bstack1111l1l_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨᬦ"): bstack1111l1l_opy_ (u"ࠢࠣᬧ"),
                bstack1111l1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᬨ"): [],
                bstack1111l1l_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᬩ"): bstack1111l1l_opy_ (u"ࠥࠦᬪ"),
                bstack1111l1l_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦᬫ"): bstack1111l1l_opy_ (u"ࠧࠨᬬ"),
                bstack1111l1l_opy_ (u"ࠨࡰࡳࡔࡤࡻࡉ࡯ࡦࡧࠤᬭ"): bstack1111l1l_opy_ (u"ࠢࠣᬮ")
            }
            bstack11l111llll1_opy_ = repo.active_branch.name
            bstack111lll11l11_opy_ = repo.head.commit
            result[bstack1111l1l_opy_ (u"ࠣࡲࡵࡍࡩࠨᬯ")] = bstack111lll11l11_opy_.hexsha
            bstack11l11l1llll_opy_ = _11l11ll11ll_opy_(repo)
            logger.debug(bstack1111l1l_opy_ (u"ࠤࡅࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠻ࠢࠥᬰ") + str(bstack11l11l1llll_opy_) + bstack1111l1l_opy_ (u"ࠥࠦᬱ"))
            if bstack11l11l1llll_opy_:
                try:
                    bstack111ll1lll11_opy_ = repo.git.diff(bstack1111l1l_opy_ (u"ࠦ࠲࠳࡮ࡢ࡯ࡨ࠱ࡴࡴ࡬ࡺࠤᬲ"), bstack1lll11lll1l_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᬳ")).split(bstack1111l1l_opy_ (u"࠭࡜࡯᬴ࠩ"))
                    logger.debug(bstack1111l1l_opy_ (u"ࠢࡄࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡣࡧࡷࡻࡪ࡫࡮ࠡࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽࠡࡣࡱࡨࠥࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠻ࠢࠥᬵ") + str(bstack111ll1lll11_opy_) + bstack1111l1l_opy_ (u"ࠣࠤᬶ"))
                    result[bstack1111l1l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᬷ")] = [f.strip() for f in bstack111ll1lll11_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1lll11lll1l_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢᬸ")))
                except Exception:
                    logger.debug(bstack1111l1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡦࡴࡣࡩࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳ࠴ࠠࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡵࡩࡨ࡫࡮ࡵࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠦᬹ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1111l1l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᬺ")] = _11l111ll11l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1111l1l_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᬻ")] = _11l111ll11l_opy_(commits[:5])
            bstack11l11l1l1l1_opy_ = set()
            bstack111llll11ll_opy_ = []
            for commit in commits:
                logger.debug(bstack1111l1l_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮࡫ࡷ࠾ࠥࠨᬼ") + str(commit.message) + bstack1111l1l_opy_ (u"ࠣࠤᬽ"))
                bstack11l11lll1l1_opy_ = commit.author.name if commit.author else bstack1111l1l_opy_ (u"ࠤࡘࡲࡰࡴ࡯ࡸࡰࠥᬾ")
                bstack11l11l1l1l1_opy_.add(bstack11l11lll1l1_opy_)
                bstack111llll11ll_opy_.append({
                    bstack1111l1l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᬿ"): commit.message.strip(),
                    bstack1111l1l_opy_ (u"ࠦࡺࡹࡥࡳࠤᭀ"): bstack11l11lll1l1_opy_
                })
            result[bstack1111l1l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨᭁ")] = list(bstack11l11l1l1l1_opy_)
            result[bstack1111l1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢᭂ")] = bstack111llll11ll_opy_
            result[bstack1111l1l_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢᭃ")] = bstack111lll11l11_opy_.committed_datetime.strftime(bstack1111l1l_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦ᭄ࠥ"))
            if (not result[bstack1111l1l_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᭅ")] or result[bstack1111l1l_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦᭆ")].strip() == bstack1111l1l_opy_ (u"ࠦࠧᭇ")) and bstack111lll11l11_opy_.message:
                bstack11l1111111l_opy_ = bstack111lll11l11_opy_.message.strip().splitlines()
                result[bstack1111l1l_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᭈ")] = bstack11l1111111l_opy_[0] if bstack11l1111111l_opy_ else bstack1111l1l_opy_ (u"ࠨࠢᭉ")
                if len(bstack11l1111111l_opy_) > 2:
                    result[bstack1111l1l_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢᭊ")] = bstack1111l1l_opy_ (u"ࠨ࡞ࡱࠫᭋ").join(bstack11l1111111l_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1111l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࠩࡨࡲࡰࡩ࡫ࡲ࠻ࠢࡾࡪࡴࡲࡤࡦࡴࢀ࠭࠿ࠦࠢᭌ") + str(err) + bstack1111l1l_opy_ (u"ࠥࠦ᭍"))
    filtered_results = [
        r
        for r in results
        if _111ll1ll1ll_opy_(r)
    ]
    return filtered_results
def _111ll1ll1ll_opy_(result):
    bstack1111l1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡍ࡫࡬ࡱࡧࡵࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡩࡧࠢࡤࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡹࡵ࡭ࡶࠣ࡭ࡸࠦࡶࡢ࡮࡬ࡨࠥ࠮࡮ࡰࡰ࠰ࡩࡲࡶࡴࡺࠢࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠡࡣࡱࡨࠥࡧࡵࡵࡪࡲࡶࡸ࠯࠮ࠋࠢࠣࠤࠥࠨࠢࠣ᭎")
    return (
        isinstance(result.get(bstack1111l1l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ᭏"), None), list)
        and len(result[bstack1111l1l_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧ᭐")]) > 0
        and isinstance(result.get(bstack1111l1l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣ᭑"), None), list)
        and len(result[bstack1111l1l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤ᭒")]) > 0
    )
def _11l11ll11ll_opy_(repo):
    bstack1111l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡗࡶࡾࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡨࡦࠢࡥࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡳࡧࡳࡳࠥࡽࡩࡵࡪࡲࡹࡹࠦࡨࡢࡴࡧࡧࡴࡪࡥࡥࠢࡱࡥࡲ࡫ࡳࠡࡣࡱࡨࠥࡽ࡯ࡳ࡭ࠣࡻ࡮ࡺࡨࠡࡣ࡯ࡰࠥ࡜ࡃࡔࠢࡳࡶࡴࡼࡩࡥࡧࡵࡷ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡥࡶࡦࡴࡣࡩࠢ࡬ࡪࠥࡶ࡯ࡴࡵ࡬ࡦࡱ࡫ࠬࠡࡧ࡯ࡷࡪࠦࡎࡰࡰࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᭓")
    try:
        try:
            origin = repo.remotes.origin
            bstack11l11l11l11_opy_ = origin.refs[bstack1111l1l_opy_ (u"ࠪࡌࡊࡇࡄࠨ᭔")]
            target = bstack11l11l11l11_opy_.reference.name
            if target.startswith(bstack1111l1l_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬ᭕")):
                return target
        except Exception:
            pass
        if repo.heads:
            return repo.heads[0].name
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1111l1l_opy_ (u"ࠬࡵࡲࡪࡩ࡬ࡲ࠴࠭᭖")):
                    return ref.name
    except Exception:
        pass
    return None
def _11l111ll11l_opy_(commits):
    bstack1111l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ᭗")
    bstack111ll1lll11_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11l11lll111_opy_ in diff:
                        if bstack11l11lll111_opy_.a_path:
                            bstack111ll1lll11_opy_.add(bstack11l11lll111_opy_.a_path)
                        if bstack11l11lll111_opy_.b_path:
                            bstack111ll1lll11_opy_.add(bstack11l11lll111_opy_.b_path)
    except Exception:
        pass
    return list(bstack111ll1lll11_opy_)
def bstack111ll1l1lll_opy_(bstack11l11ll111l_opy_):
    bstack111ll11lll1_opy_ = bstack11l11llllll_opy_(bstack11l11ll111l_opy_)
    if bstack111ll11lll1_opy_ and bstack111ll11lll1_opy_ > bstack11l1lll1111_opy_:
        bstack11l11ll1ll1_opy_ = bstack111ll11lll1_opy_ - bstack11l1lll1111_opy_
        bstack11l1111l11l_opy_ = bstack11l11llll1l_opy_(bstack11l11ll111l_opy_[bstack1111l1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᭘")], bstack11l11ll1ll1_opy_)
        bstack11l11ll111l_opy_[bstack1111l1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ᭙")] = bstack11l1111l11l_opy_
        logger.info(bstack1111l1l_opy_ (u"ࠤࡗ࡬ࡪࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡨࡢࡵࠣࡦࡪ࡫࡮ࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧ࠲࡙ࠥࡩࡻࡧࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡡࡧࡶࡨࡶࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥࢁࡽࠡࡍࡅࠦ᭚")
                    .format(bstack11l11llllll_opy_(bstack11l11ll111l_opy_) / 1024))
    return bstack11l11ll111l_opy_
def bstack11l11llllll_opy_(bstack1l1ll111l1_opy_):
    try:
        if bstack1l1ll111l1_opy_:
            bstack11l1111lll1_opy_ = json.dumps(bstack1l1ll111l1_opy_)
            bstack111lllllll1_opy_ = sys.getsizeof(bstack11l1111lll1_opy_)
            return bstack111lllllll1_opy_
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡦࡥࡱࡩࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡌࡖࡓࡓࠦ࡯ࡣ࡬ࡨࡧࡹࡀࠠࡼࡿࠥ᭛").format(e))
    return -1
def bstack11l11llll1l_opy_(field, bstack111llll1l11_opy_):
    try:
        bstack11l11111lll_opy_ = len(bytes(bstack11l1ll11111_opy_, bstack1111l1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᭜")))
        bstack111ll1l1l11_opy_ = bytes(field, bstack1111l1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᭝"))
        bstack11l111l11ll_opy_ = len(bstack111ll1l1l11_opy_)
        bstack11l11l111l1_opy_ = ceil(bstack11l111l11ll_opy_ - bstack111llll1l11_opy_ - bstack11l11111lll_opy_)
        if bstack11l11l111l1_opy_ > 0:
            bstack111lllll11l_opy_ = bstack111ll1l1l11_opy_[:bstack11l11l111l1_opy_].decode(bstack1111l1l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᭞"), errors=bstack1111l1l_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࠧ᭟")) + bstack11l1ll11111_opy_
            return bstack111lllll11l_opy_
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡴࡳࡷࡱࡧࡦࡺࡩ࡯ࡩࠣࡪ࡮࡫࡬ࡥ࠮ࠣࡲࡴࡺࡨࡪࡰࡪࠤࡼࡧࡳࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧࠤ࡭࡫ࡲࡦ࠼ࠣࡿࢂࠨ᭠").format(e))
    return field
def bstack1ll111ll_opy_():
    env = os.environ
    if (bstack1111l1l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢ᭡") in env and len(env[bstack1111l1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣ᭢")]) > 0) or (
            bstack1111l1l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ᭣") in env and len(env[bstack1111l1l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦ᭤")]) > 0):
        return {
            bstack1111l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᭥"): bstack1111l1l_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣ᭦"),
            bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᭧"): env.get(bstack1111l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᭨")),
            bstack1111l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭩"): env.get(bstack1111l1l_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨ᭪")),
            bstack1111l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᭫"): env.get(bstack1111l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ᭬ࠧ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠢࡄࡋࠥ᭭")) == bstack1111l1l_opy_ (u"ࠣࡶࡵࡹࡪࠨ᭮") and bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦ᭯"))):
        return {
            bstack1111l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᭰"): bstack1111l1l_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨ᭱"),
            bstack1111l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᭲"): env.get(bstack1111l1l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᭳")),
            bstack1111l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᭴"): env.get(bstack1111l1l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧ᭵")),
            bstack1111l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᭶"): env.get(bstack1111l1l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨ᭷"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠦࡈࡏࠢ᭸")) == bstack1111l1l_opy_ (u"ࠧࡺࡲࡶࡧࠥ᭹") and bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨ᭺"))):
        return {
            bstack1111l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭻"): bstack1111l1l_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦ᭼"),
            bstack1111l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭽"): env.get(bstack1111l1l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥ᭾")),
            bstack1111l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᭿"): env.get(bstack1111l1l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᮀ")),
            bstack1111l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᮁ"): env.get(bstack1111l1l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᮂ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠣࡅࡌࠦᮃ")) == bstack1111l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᮄ") and env.get(bstack1111l1l_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦᮅ")) == bstack1111l1l_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨᮆ"):
        return {
            bstack1111l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᮇ"): bstack1111l1l_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣᮈ"),
            bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮉ"): None,
            bstack1111l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮊ"): None,
            bstack1111l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᮋ"): None
        }
    if env.get(bstack1111l1l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨᮌ")) and env.get(bstack1111l1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᮍ")):
        return {
            bstack1111l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᮎ"): bstack1111l1l_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤᮏ"),
            bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮐ"): env.get(bstack1111l1l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨᮑ")),
            bstack1111l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᮒ"): None,
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮓ"): env.get(bstack1111l1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᮔ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠧࡉࡉࠣᮕ")) == bstack1111l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᮖ") and bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨᮗ"))):
        return {
            bstack1111l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᮘ"): bstack1111l1l_opy_ (u"ࠤࡇࡶࡴࡴࡥࠣᮙ"),
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮚ"): env.get(bstack1111l1l_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢᮛ")),
            bstack1111l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᮜ"): None,
            bstack1111l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᮝ"): env.get(bstack1111l1l_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᮞ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠣࡅࡌࠦᮟ")) == bstack1111l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᮠ") and bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨᮡ"))):
        return {
            bstack1111l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᮢ"): bstack1111l1l_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣᮣ"),
            bstack1111l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᮤ"): env.get(bstack1111l1l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨᮥ")),
            bstack1111l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮦ"): env.get(bstack1111l1l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᮧ")),
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮨ"): env.get(bstack1111l1l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᮩ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠧࡉࡉ᮪ࠣ")) == bstack1111l1l_opy_ (u"ࠨࡴࡳࡷࡨ᮫ࠦ") and bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥᮬ"))):
        return {
            bstack1111l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᮭ"): bstack1111l1l_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤᮮ"),
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮯ"): env.get(bstack1111l1l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣ᮰")),
            bstack1111l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᮱"): env.get(bstack1111l1l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᮲")),
            bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᮳"): env.get(bstack1111l1l_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦ᮴"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠤࡆࡍࠧ᮵")) == bstack1111l1l_opy_ (u"ࠥࡸࡷࡻࡥࠣ᮶") and bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢ᮷"))):
        return {
            bstack1111l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᮸"): bstack1111l1l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤ᮹"),
            bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮺ"): env.get(bstack1111l1l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᮻ")),
            bstack1111l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᮼ"): env.get(bstack1111l1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧᮽ")) or env.get(bstack1111l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᮾ")),
            bstack1111l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᮿ"): env.get(bstack1111l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᯀ"))
        }
    if bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤᯁ"))):
        return {
            bstack1111l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᯂ"): bstack1111l1l_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤᯃ"),
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᯄ"): bstack1111l1l_opy_ (u"ࠦࢀࢃࡻࡾࠤᯅ").format(env.get(bstack1111l1l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨᯆ")), env.get(bstack1111l1l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭ᯇ"))),
            bstack1111l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᯈ"): env.get(bstack1111l1l_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊࠢᯉ")),
            bstack1111l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᯊ"): env.get(bstack1111l1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᯋ"))
        }
    if bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨᯌ"))):
        return {
            bstack1111l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯍ"): bstack1111l1l_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲࠣᯎ"),
            bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᯏ"): bstack1111l1l_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠢᯐ").format(env.get(bstack1111l1l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨᯑ")), env.get(bstack1111l1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫᯒ")), env.get(bstack1111l1l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬᯓ")), env.get(bstack1111l1l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩᯔ"))),
            bstack1111l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᯕ"): env.get(bstack1111l1l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᯖ")),
            bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᯗ"): env.get(bstack1111l1l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᯘ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦᯙ")) and env.get(bstack1111l1l_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᯚ")):
        return {
            bstack1111l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯛ"): bstack1111l1l_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉࠣᯜ"),
            bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᯝ"): bstack1111l1l_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦᯞ").format(env.get(bstack1111l1l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᯟ")), env.get(bstack1111l1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨᯠ")), env.get(bstack1111l1l_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫᯡ"))),
            bstack1111l1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᯢ"): env.get(bstack1111l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᯣ")),
            bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᯤ"): env.get(bstack1111l1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᯥ"))
        }
    if any([env.get(bstack1111l1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊ᯦ࠢ")), env.get(bstack1111l1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᯧ")), env.get(bstack1111l1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᯨ"))]):
        return {
            bstack1111l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯩ"): bstack1111l1l_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨᯪ"),
            bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᯫ"): env.get(bstack1111l1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᯬ")),
            bstack1111l1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᯭ"): env.get(bstack1111l1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᯮ")),
            bstack1111l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᯯ"): env.get(bstack1111l1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᯰ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦᯱ")):
        return {
            bstack1111l1l_opy_ (u"ࠢ࡯ࡣࡰࡩ᯲ࠧ"): bstack1111l1l_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯᯳ࠣ"),
            bstack1111l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᯴"): env.get(bstack1111l1l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧ᯵")),
            bstack1111l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᯶"): env.get(bstack1111l1l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦ᯷")),
            bstack1111l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᯸"): env.get(bstack1111l1l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧ᯹"))
        }
    if env.get(bstack1111l1l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤ᯺")) or env.get(bstack1111l1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ᯻")):
        return {
            bstack1111l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᯼"): bstack1111l1l_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶࠧ᯽"),
            bstack1111l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᯾"): env.get(bstack1111l1l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᯿")),
            bstack1111l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᰀ"): bstack1111l1l_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣᰁ") if env.get(bstack1111l1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦᰂ")) else None,
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰃ"): env.get(bstack1111l1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤᰄ"))
        }
    if any([env.get(bstack1111l1l_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥᰅ")), env.get(bstack1111l1l_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᰆ")), env.get(bstack1111l1l_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᰇ"))]):
        return {
            bstack1111l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᰈ"): bstack1111l1l_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣᰉ"),
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᰊ"): None,
            bstack1111l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᰋ"): env.get(bstack1111l1l_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤᰌ")),
            bstack1111l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᰍ"): env.get(bstack1111l1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᰎ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦᰏ")):
        return {
            bstack1111l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᰐ"): bstack1111l1l_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨᰑ"),
            bstack1111l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᰒ"): env.get(bstack1111l1l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᰓ")),
            bstack1111l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᰔ"): bstack1111l1l_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣᰕ").format(env.get(bstack1111l1l_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫᰖ"))) if env.get(bstack1111l1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧᰗ")) else None,
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰘ"): env.get(bstack1111l1l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᰙ"))
        }
    if bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨᰚ"))):
        return {
            bstack1111l1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰛ"): bstack1111l1l_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹࠣᰜ"),
            bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰝ"): env.get(bstack1111l1l_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨᰞ")),
            bstack1111l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᰟ"): env.get(bstack1111l1l_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢᰠ")),
            bstack1111l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᰡ"): env.get(bstack1111l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᰢ"))
        }
    if bstack1lll1l11l_opy_(env.get(bstack1111l1l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣᰣ"))):
        return {
            bstack1111l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᰤ"): bstack1111l1l_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥᰥ"),
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᰦ"): bstack1111l1l_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧᰧ").format(env.get(bstack1111l1l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩᰨ")), env.get(bstack1111l1l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪᰩ")), env.get(bstack1111l1l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧᰪ"))),
            bstack1111l1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᰫ"): env.get(bstack1111l1l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦᰬ")),
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰭ"): env.get(bstack1111l1l_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦᰮ"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠧࡉࡉࠣᰯ")) == bstack1111l1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᰰ") and env.get(bstack1111l1l_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢᰱ")) == bstack1111l1l_opy_ (u"ࠣ࠳ࠥᰲ"):
        return {
            bstack1111l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᰳ"): bstack1111l1l_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥᰴ"),
            bstack1111l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᰵ"): bstack1111l1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣᰶ").format(env.get(bstack1111l1l_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎ᰷ࠪ"))),
            bstack1111l1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᰸"): None,
            bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᰹"): None,
        }
    if env.get(bstack1111l1l_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ᰺")):
        return {
            bstack1111l1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᰻"): bstack1111l1l_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨ᰼"),
            bstack1111l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᰽"): None,
            bstack1111l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᰾"): env.get(bstack1111l1l_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣ᰿")),
            bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᱀"): env.get(bstack1111l1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᱁"))
        }
    if any([env.get(bstack1111l1l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨ᱂")), env.get(bstack1111l1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦ᱃")), env.get(bstack1111l1l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥ᱄")), env.get(bstack1111l1l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓࠢ᱅"))]):
        return {
            bstack1111l1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᱆"): bstack1111l1l_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦ᱇"),
            bstack1111l1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᱈"): None,
            bstack1111l1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᱉"): env.get(bstack1111l1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᱊")) or None,
            bstack1111l1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᱋"): env.get(bstack1111l1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ᱌"), 0)
        }
    if env.get(bstack1111l1l_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᱍ")):
        return {
            bstack1111l1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᱎ"): bstack1111l1l_opy_ (u"ࠤࡊࡳࡈࡊࠢᱏ"),
            bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᱐"): None,
            bstack1111l1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᱑"): env.get(bstack1111l1l_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᱒")),
            bstack1111l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᱓"): env.get(bstack1111l1l_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨ᱔"))
        }
    if env.get(bstack1111l1l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᱕")):
        return {
            bstack1111l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᱖"): bstack1111l1l_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨ᱗"),
            bstack1111l1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᱘"): env.get(bstack1111l1l_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᱙")),
            bstack1111l1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᱚ"): env.get(bstack1111l1l_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥᱛ")),
            bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᱜ"): env.get(bstack1111l1l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᱝ"))
        }
    return {bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᱞ"): None}
def get_host_info():
    return {
        bstack1111l1l_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨᱟ"): platform.node(),
        bstack1111l1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢᱠ"): platform.system(),
        bstack1111l1l_opy_ (u"ࠨࡴࡺࡲࡨࠦᱡ"): platform.machine(),
        bstack1111l1l_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᱢ"): platform.version(),
        bstack1111l1l_opy_ (u"ࠣࡣࡵࡧ࡭ࠨᱣ"): platform.architecture()[0]
    }
def bstack1l11l111l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1111ll1l_opy_():
    if bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪᱤ")):
        return bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᱥ")
    return bstack1111l1l_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪᱦ")
def bstack111ll1ll111_opy_(driver):
    info = {
        bstack1111l1l_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᱧ"): driver.capabilities,
        bstack1111l1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪᱨ"): driver.session_id,
        bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᱩ"): driver.capabilities.get(bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᱪ"), None),
        bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᱫ"): driver.capabilities.get(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᱬ"), None),
        bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭ᱭ"): driver.capabilities.get(bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᱮ"), None),
        bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᱯ"):driver.capabilities.get(bstack1111l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᱰ"), None),
    }
    if bstack11l1111ll1l_opy_() == bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᱱ"):
        if bstack111l1lll_opy_():
            info[bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᱲ")] = bstack1111l1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩᱳ")
        elif driver.capabilities.get(bstack1111l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᱴ"), {}).get(bstack1111l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᱵ"), False):
            info[bstack1111l1l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᱶ")] = bstack1111l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᱷ")
        else:
            info[bstack1111l1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᱸ")] = bstack1111l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᱹ")
    return info
def bstack111l1lll_opy_():
    if bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᱺ")):
        return True
    if bstack1lll1l11l_opy_(os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᱻ"), None)):
        return True
    return False
def bstack1ll111l111_opy_(bstack111ll1l11ll_opy_, url, data, config):
    headers = config.get(bstack1111l1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᱼ"), None)
    proxies = bstack11l1l111ll_opy_(config, url)
    auth = config.get(bstack1111l1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᱽ"), None)
    response = requests.request(
            bstack111ll1l11ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11lll1l1l1_opy_(bstack1lll11111l_opy_, size):
    bstack1ll11l1l_opy_ = []
    while len(bstack1lll11111l_opy_) > size:
        bstack11ll1l1ll1_opy_ = bstack1lll11111l_opy_[:size]
        bstack1ll11l1l_opy_.append(bstack11ll1l1ll1_opy_)
        bstack1lll11111l_opy_ = bstack1lll11111l_opy_[size:]
    bstack1ll11l1l_opy_.append(bstack1lll11111l_opy_)
    return bstack1ll11l1l_opy_
def bstack11l11l1l1ll_opy_(message, bstack11l111l1ll1_opy_=False):
    os.write(1, bytes(message, bstack1111l1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᱾")))
    os.write(1, bytes(bstack1111l1l_opy_ (u"ࠨ࡞ࡱࠫ᱿"), bstack1111l1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᲀ")))
    if bstack11l111l1ll1_opy_:
        with open(bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩᲁ") + os.environ[bstack1111l1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᲂ")] + bstack1111l1l_opy_ (u"ࠬ࠴࡬ࡰࡩࠪᲃ"), bstack1111l1l_opy_ (u"࠭ࡡࠨᲄ")) as f:
            f.write(message + bstack1111l1l_opy_ (u"ࠧ࡝ࡰࠪᲅ"))
def bstack1l1ll1l1l1l_opy_():
    return os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᲆ")].lower() == bstack1111l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᲇ")
def bstack1ll111ll1l_opy_():
    return bstack1111l1lll1_opy_().replace(tzinfo=None).isoformat() + bstack1111l1l_opy_ (u"ࠪ࡞ࠬᲈ")
def bstack111ll1l1l1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1111l1l_opy_ (u"ࠫ࡟࠭Ᲊ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1111l1l_opy_ (u"ࠬࡠࠧᲊ")))).total_seconds() * 1000
def bstack111lll11lll_opy_(timestamp):
    return bstack11l111l1l11_opy_(timestamp).isoformat() + bstack1111l1l_opy_ (u"࡚࠭ࠨ᲋")
def bstack111llll11l1_opy_(bstack11l11l11l1l_opy_):
    date_format = bstack1111l1l_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬ᲌")
    bstack111ll1ll11l_opy_ = datetime.datetime.strptime(bstack11l11l11l1l_opy_, date_format)
    return bstack111ll1ll11l_opy_.isoformat() + bstack1111l1l_opy_ (u"ࠨ࡜ࠪ᲍")
def bstack11l111l111l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1111l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᲎")
    else:
        return bstack1111l1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᲏")
def bstack1lll1l11l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1111l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᲐ")
def bstack11l11ll1111_opy_(val):
    return val.__str__().lower() == bstack1111l1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᲑ")
def error_handler(bstack11l111l1111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l111l1111_opy_ as e:
                print(bstack1111l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᲒ").format(func.__name__, bstack11l111l1111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11111l11_opy_(bstack111ll1l111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111ll1l111l_opy_(cls, *args, **kwargs)
            except bstack11l111l1111_opy_ as e:
                print(bstack1111l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᲓ").format(bstack111ll1l111l_opy_.__name__, bstack11l111l1111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11111l11_opy_
    else:
        return decorator
def bstack111l1l11_opy_(bstack1111l11111_opy_):
    if os.getenv(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᲔ")) is not None:
        return bstack1lll1l11l_opy_(os.getenv(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᲕ")))
    if bstack1111l1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᲖ") in bstack1111l11111_opy_ and bstack11l11ll1111_opy_(bstack1111l11111_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᲗ")]):
        return False
    if bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᲘ") in bstack1111l11111_opy_ and bstack11l11ll1111_opy_(bstack1111l11111_opy_[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᲙ")]):
        return False
    return True
def bstack1ll1l1l1l1_opy_():
    try:
        from pytest_bdd import reporting
        bstack111lll1l1ll_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢᲚ"), None)
        return bstack111lll1l1ll_opy_ is None or bstack111lll1l1ll_opy_ == bstack1111l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᲛ")
    except Exception as e:
        return False
def bstack111llllll1_opy_(hub_url, CONFIG):
    if bstack1ll1l1lll1_opy_() <= version.parse(bstack1111l1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᲜ")):
        if hub_url:
            return bstack1111l1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᲝ") + hub_url + bstack1111l1l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᲞ")
        return bstack1ll1ll11l_opy_
    if hub_url:
        return bstack1111l1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᲟ") + hub_url + bstack1111l1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᲠ")
    return bstack1l1ll1111l_opy_
def bstack111lllll111_opy_():
    return isinstance(os.getenv(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭Ს")), str)
def bstack1l1ll111ll_opy_(url):
    return urlparse(url).hostname
def bstack1l1ll111l_opy_(hostname):
    for bstack11ll1ll111_opy_ in bstack11ll11ll1l_opy_:
        regex = re.compile(bstack11ll1ll111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111lll1ll11_opy_(bstack11l11111ll1_opy_, file_name, logger):
    bstack1lllllll1l_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠨࢀࠪᲢ")), bstack11l11111ll1_opy_)
    try:
        if not os.path.exists(bstack1lllllll1l_opy_):
            os.makedirs(bstack1lllllll1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠩࢁࠫᲣ")), bstack11l11111ll1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1111l1l_opy_ (u"ࠪࡻࠬᲤ")):
                pass
            with open(file_path, bstack1111l1l_opy_ (u"ࠦࡼ࠱ࠢᲥ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1ll11l1_opy_.format(str(e)))
def bstack11l11l1l111_opy_(file_name, key, value, logger):
    file_path = bstack111lll1ll11_opy_(bstack1111l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᲦ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1llll11l1_opy_ = json.load(open(file_path, bstack1111l1l_opy_ (u"࠭ࡲࡣࠩᲧ")))
        else:
            bstack1llll11l1_opy_ = {}
        bstack1llll11l1_opy_[key] = value
        with open(file_path, bstack1111l1l_opy_ (u"ࠢࡸ࠭ࠥᲨ")) as outfile:
            json.dump(bstack1llll11l1_opy_, outfile)
def bstack1l1111lll1_opy_(file_name, logger):
    file_path = bstack111lll1ll11_opy_(bstack1111l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᲩ"), file_name, logger)
    bstack1llll11l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1111l1l_opy_ (u"ࠩࡵࠫᲪ")) as bstack111ll1lll_opy_:
            bstack1llll11l1_opy_ = json.load(bstack111ll1lll_opy_)
    return bstack1llll11l1_opy_
def bstack1lll11111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᲫ") + file_path + bstack1111l1l_opy_ (u"ࠫࠥ࠭Წ") + str(e))
def bstack1ll1l1lll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1111l1l_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᲭ")
def bstack11l1l1l11_opy_(config):
    if bstack1111l1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᲮ") in config:
        del (config[bstack1111l1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭Ჯ")])
        return False
    if bstack1ll1l1lll1_opy_() < version.parse(bstack1111l1l_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᲰ")):
        return False
    if bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᲱ")):
        return True
    if bstack1111l1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᲲ") in config and config[bstack1111l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᲳ")] is False:
        return False
    else:
        return True
def bstack1l1ll1ll1_opy_(args_list, bstack111ll11ll1l_opy_):
    index = -1
    for value in bstack111ll11ll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll11ll11l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll11ll11l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111ll1111l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111ll1111l_opy_ = bstack111ll1111l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1111l1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᲴ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1111l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ჵ"), exception=exception)
    def bstack111111l1ll_opy_(self):
        if self.result != bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᲶ"):
            return None
        if isinstance(self.exception_type, str) and bstack1111l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᲷ") in self.exception_type:
            return bstack1111l1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᲸ")
        return bstack1111l1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᲹ")
    def bstack11l11lll11l_opy_(self):
        if self.result != bstack1111l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᲺ"):
            return None
        if self.bstack111ll1111l_opy_:
            return self.bstack111ll1111l_opy_
        return bstack11l111lllll_opy_(self.exception)
def bstack11l111lllll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l111l1lll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l11l1lll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1111l11_opy_(config, logger):
    try:
        import playwright
        bstack11l11ll1lll_opy_ = playwright.__file__
        bstack111lll1ll1l_opy_ = os.path.split(bstack11l11ll1lll_opy_)
        bstack111lll1111l_opy_ = bstack111lll1ll1l_opy_[0] + bstack1111l1l_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨ᲻")
        os.environ[bstack1111l1l_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩ᲼")] = bstack1l11l11ll_opy_(config)
        with open(bstack111lll1111l_opy_, bstack1111l1l_opy_ (u"ࠧࡳࠩᲽ")) as f:
            bstack1ll11lll11_opy_ = f.read()
            bstack11l1111l1ll_opy_ = bstack1111l1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᲾ")
            bstack11l111l1l1l_opy_ = bstack1ll11lll11_opy_.find(bstack11l1111l1ll_opy_)
            if bstack11l111l1l1l_opy_ == -1:
              process = subprocess.Popen(bstack1111l1l_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᲿ"), shell=True, cwd=bstack111lll1ll1l_opy_[0])
              process.wait()
              bstack11l111ll1ll_opy_ = bstack1111l1l_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪ᳀")
              bstack111llllll1l_opy_ = bstack1111l1l_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣ᳁")
              bstack11l11l11lll_opy_ = bstack1ll11lll11_opy_.replace(bstack11l111ll1ll_opy_, bstack111llllll1l_opy_)
              with open(bstack111lll1111l_opy_, bstack1111l1l_opy_ (u"ࠬࡽࠧ᳂")) as f:
                f.write(bstack11l11l11lll_opy_)
    except Exception as e:
        logger.error(bstack1ll1l1111_opy_.format(str(e)))
def bstack1lllll1lll_opy_():
  try:
    bstack111lll11111_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭᳃"))
    bstack111lll111ll_opy_ = []
    if os.path.exists(bstack111lll11111_opy_):
      with open(bstack111lll11111_opy_) as f:
        bstack111lll111ll_opy_ = json.load(f)
      os.remove(bstack111lll11111_opy_)
    return bstack111lll111ll_opy_
  except:
    pass
  return []
def bstack11lllll1l1_opy_(bstack1lllll1ll1_opy_):
  try:
    bstack111lll111ll_opy_ = []
    bstack111lll11111_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧ᳄"))
    if os.path.exists(bstack111lll11111_opy_):
      with open(bstack111lll11111_opy_) as f:
        bstack111lll111ll_opy_ = json.load(f)
    bstack111lll111ll_opy_.append(bstack1lllll1ll1_opy_)
    with open(bstack111lll11111_opy_, bstack1111l1l_opy_ (u"ࠨࡹࠪ᳅")) as f:
        json.dump(bstack111lll111ll_opy_, f)
  except:
    pass
def bstack111111ll_opy_(logger, bstack11l1111l1l1_opy_ = False):
  try:
    test_name = os.environ.get(bstack1111l1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ᳆"), bstack1111l1l_opy_ (u"ࠪࠫ᳇"))
    if test_name == bstack1111l1l_opy_ (u"ࠫࠬ᳈"):
        test_name = threading.current_thread().__dict__.get(bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫ᳉"), bstack1111l1l_opy_ (u"࠭ࠧ᳊"))
    bstack111lllll1l1_opy_ = bstack1111l1l_opy_ (u"ࠧ࠭ࠢࠪ᳋").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1111l1l1_opy_:
        bstack11lll11l_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᳌"), bstack1111l1l_opy_ (u"ࠩ࠳ࠫ᳍"))
        bstack1lll1lllll_opy_ = {bstack1111l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ᳎"): test_name, bstack1111l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᳏"): bstack111lllll1l1_opy_, bstack1111l1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ᳐"): bstack11lll11l_opy_}
        bstack111lll1l11l_opy_ = []
        bstack111ll1llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ᳑"))
        if os.path.exists(bstack111ll1llll1_opy_):
            with open(bstack111ll1llll1_opy_) as f:
                bstack111lll1l11l_opy_ = json.load(f)
        bstack111lll1l11l_opy_.append(bstack1lll1lllll_opy_)
        with open(bstack111ll1llll1_opy_, bstack1111l1l_opy_ (u"ࠧࡸࠩ᳒")) as f:
            json.dump(bstack111lll1l11l_opy_, f)
    else:
        bstack1lll1lllll_opy_ = {bstack1111l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᳓"): test_name, bstack1111l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᳔"): bstack111lllll1l1_opy_, bstack1111l1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹ᳕ࠩ"): str(multiprocessing.current_process().name)}
        if bstack1111l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ᳖") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1lll1lllll_opy_)
  except Exception as e:
      logger.warn(bstack1111l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ᳗").format(e))
def bstack1l1ll1l1l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111l1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴ᳘ࠩ"))
    try:
      bstack111llllll11_opy_ = []
      bstack1lll1lllll_opy_ = {bstack1111l1l_opy_ (u"ࠧ࡯ࡣࡰࡩ᳙ࠬ"): test_name, bstack1111l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᳚"): error_message, bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ᳛"): index}
      bstack11l11ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱ᳜ࠫ"))
      if os.path.exists(bstack11l11ll1l1l_opy_):
          with open(bstack11l11ll1l1l_opy_) as f:
              bstack111llllll11_opy_ = json.load(f)
      bstack111llllll11_opy_.append(bstack1lll1lllll_opy_)
      with open(bstack11l11ll1l1l_opy_, bstack1111l1l_opy_ (u"ࠫࡼ᳝࠭")) as f:
          json.dump(bstack111llllll11_opy_, f)
    except Exception as e:
      logger.warn(bstack1111l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽ᳞ࠣ").format(e))
    return
  bstack111llllll11_opy_ = []
  bstack1lll1lllll_opy_ = {bstack1111l1l_opy_ (u"࠭࡮ࡢ࡯ࡨ᳟ࠫ"): test_name, bstack1111l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᳠"): error_message, bstack1111l1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᳡"): index}
  bstack11l11ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰ᳢ࠪ"))
  lock_file = bstack11l11ll1l1l_opy_ + bstack1111l1l_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬᳣ࠩ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l11ll1l1l_opy_):
          with open(bstack11l11ll1l1l_opy_, bstack1111l1l_opy_ (u"ࠫࡷ᳤࠭")) as f:
              content = f.read().strip()
              if content:
                  bstack111llllll11_opy_ = json.load(open(bstack11l11ll1l1l_opy_))
      bstack111llllll11_opy_.append(bstack1lll1lllll_opy_)
      with open(bstack11l11ll1l1l_opy_, bstack1111l1l_opy_ (u"ࠬࡽ᳥ࠧ")) as f:
          json.dump(bstack111llllll11_opy_, f)
  except Exception as e:
    logger.warn(bstack1111l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨ࠼ࠣࡿࢂࠨ᳦").format(e))
def bstack1ll1l1l1_opy_(bstack11lllll1l_opy_, name, logger):
  try:
    bstack1lll1lllll_opy_ = {bstack1111l1l_opy_ (u"ࠧ࡯ࡣࡰࡩ᳧ࠬ"): name, bstack1111l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸ᳨ࠧ"): bstack11lllll1l_opy_, bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᳩ"): str(threading.current_thread()._name)}
    return bstack1lll1lllll_opy_
  except Exception as e:
    logger.warn(bstack1111l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᳪ").format(e))
  return
def bstack11l111lll1l_opy_():
    return platform.system() == bstack1111l1l_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬᳫ")
def bstack1l1111ll1l_opy_(bstack11l111ll1l1_opy_, config, logger):
    bstack11l11l1111l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l111ll1l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᳬ").format(e))
    return bstack11l11l1111l_opy_
def bstack111llllllll_opy_(bstack11l11l11111_opy_, bstack11l1l111111_opy_):
    bstack111lll1llll_opy_ = version.parse(bstack11l11l11111_opy_)
    bstack11l11ll1l11_opy_ = version.parse(bstack11l1l111111_opy_)
    if bstack111lll1llll_opy_ > bstack11l11ll1l11_opy_:
        return 1
    elif bstack111lll1llll_opy_ < bstack11l11ll1l11_opy_:
        return -1
    else:
        return 0
def bstack1111l1lll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l111l1l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11l111ll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l11l111l_opy_(options, framework, config, bstack1l1lllll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1111l1l_opy_ (u"࠭ࡧࡦࡶ᳭ࠪ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l11llll_opy_ = caps.get(bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᳮ"))
    bstack11l11111l1l_opy_ = True
    bstack1lll1l1l1_opy_ = os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᳯ")]
    bstack1ll111l1l1l_opy_ = config.get(bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᳰ"), False)
    if bstack1ll111l1l1l_opy_:
        bstack1lll11ll11l_opy_ = config.get(bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᳱ"), {})
        bstack1lll11ll11l_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᳲ")] = os.getenv(bstack1111l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᳳ"))
        bstack11ll1l1llll_opy_ = json.loads(os.getenv(bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ᳴"), bstack1111l1l_opy_ (u"ࠧࡼࡿࠪᳵ"))).get(bstack1111l1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᳶ"))
    if bstack11l11ll1111_opy_(caps.get(bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨ᳷"))) or bstack11l11ll1111_opy_(caps.get(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪ᳸"))):
        bstack11l11111l1l_opy_ = False
    if bstack11l1l1l11_opy_({bstack1111l1l_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦ᳹"): bstack11l11111l1l_opy_}):
        bstack1l11llll_opy_ = bstack1l11llll_opy_ or {}
        bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᳺ")] = bstack11l11l111ll_opy_(framework)
        bstack1l11llll_opy_[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᳻")] = bstack1l1ll1l1l1l_opy_()
        bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᳼")] = bstack1lll1l1l1_opy_
        bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᳽")] = bstack1l1lllll_opy_
        if bstack1ll111l1l1l_opy_:
            bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᳾")] = bstack1ll111l1l1l_opy_
            bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳿")] = bstack1lll11ll11l_opy_
            bstack1l11llll_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᴀ")][bstack1111l1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᴁ")] = bstack11ll1l1llll_opy_
        if getattr(options, bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᴂ"), None):
            options.set_capability(bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᴃ"), bstack1l11llll_opy_)
        else:
            options[bstack1111l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᴄ")] = bstack1l11llll_opy_
    else:
        if getattr(options, bstack1111l1l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᴅ"), None):
            options.set_capability(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᴆ"), bstack11l11l111ll_opy_(framework))
            options.set_capability(bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᴇ"), bstack1l1ll1l1l1l_opy_())
            options.set_capability(bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᴈ"), bstack1lll1l1l1_opy_)
            options.set_capability(bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᴉ"), bstack1l1lllll_opy_)
            if bstack1ll111l1l1l_opy_:
                options.set_capability(bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴊ"), bstack1ll111l1l1l_opy_)
                options.set_capability(bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᴋ"), bstack1lll11ll11l_opy_)
                options.set_capability(bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳ࠯ࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᴌ"), bstack11ll1l1llll_opy_)
        else:
            options[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᴍ")] = bstack11l11l111ll_opy_(framework)
            options[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᴎ")] = bstack1l1ll1l1l1l_opy_()
            options[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᴏ")] = bstack1lll1l1l1_opy_
            options[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᴐ")] = bstack1l1lllll_opy_
            if bstack1ll111l1l1l_opy_:
                options[bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴑ")] = bstack1ll111l1l1l_opy_
                options[bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᴒ")] = bstack1lll11ll11l_opy_
                options[bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᴓ")][bstack1111l1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᴔ")] = bstack11ll1l1llll_opy_
    return options
def bstack111ll1l11l1_opy_(bstack111lllll1ll_opy_, framework):
    bstack1l1lllll_opy_ = bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠦࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡒࡕࡓࡉ࡛ࡃࡕࡡࡐࡅࡕࠨᴕ"))
    if bstack111lllll1ll_opy_ and len(bstack111lllll1ll_opy_.split(bstack1111l1l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᴖ"))) > 1:
        ws_url = bstack111lllll1ll_opy_.split(bstack1111l1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᴗ"))[0]
        if bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᴘ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1111llll_opy_ = json.loads(urllib.parse.unquote(bstack111lllll1ll_opy_.split(bstack1111l1l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᴙ"))[1]))
            bstack11l1111llll_opy_ = bstack11l1111llll_opy_ or {}
            bstack1lll1l1l1_opy_ = os.environ[bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᴚ")]
            bstack11l1111llll_opy_[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᴛ")] = str(framework) + str(__version__)
            bstack11l1111llll_opy_[bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᴜ")] = bstack1l1ll1l1l1l_opy_()
            bstack11l1111llll_opy_[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᴝ")] = bstack1lll1l1l1_opy_
            bstack11l1111llll_opy_[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᴞ")] = bstack1l1lllll_opy_
            bstack111lllll1ll_opy_ = bstack111lllll1ll_opy_.split(bstack1111l1l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᴟ"))[0] + bstack1111l1l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᴠ") + urllib.parse.quote(json.dumps(bstack11l1111llll_opy_))
    return bstack111lllll1ll_opy_
def bstack11l1l1ll1_opy_():
    global bstack1l1l111ll1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l111ll1_opy_ = BrowserType.connect
    return bstack1l1l111ll1_opy_
def bstack1lll111l11_opy_(framework_name):
    global bstack1l111l11l1_opy_
    bstack1l111l11l1_opy_ = framework_name
    return framework_name
def bstack1llll1lll1_opy_(self, *args, **kwargs):
    global bstack1l1l111ll1_opy_
    try:
        global bstack1l111l11l1_opy_
        if bstack1111l1l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᴡ") in kwargs:
            kwargs[bstack1111l1l_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᴢ")] = bstack111ll1l11l1_opy_(
                kwargs.get(bstack1111l1l_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᴣ"), None),
                bstack1l111l11l1_opy_
            )
    except Exception as e:
        logger.error(bstack1111l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧᴤ").format(str(e)))
    return bstack1l1l111ll1_opy_(self, *args, **kwargs)
def bstack11l111ll111_opy_(bstack111ll11llll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l1l111ll_opy_(bstack111ll11llll_opy_, bstack1111l1l_opy_ (u"ࠨࠢᴥ"))
        if proxies and proxies.get(bstack1111l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᴦ")):
            parsed_url = urlparse(proxies.get(bstack1111l1l_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᴧ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬᴨ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1111l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ᴩ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1111l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᴪ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1111l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨᴫ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l1llll11_opy_(bstack111ll11llll_opy_):
    bstack111lll1l1l1_opy_ = {
        bstack11l1ll11lll_opy_[bstack11l1l11111l_opy_]: bstack111ll11llll_opy_[bstack11l1l11111l_opy_]
        for bstack11l1l11111l_opy_ in bstack111ll11llll_opy_
        if bstack11l1l11111l_opy_ in bstack11l1ll11lll_opy_
    }
    bstack111lll1l1l1_opy_[bstack1111l1l_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᴬ")] = bstack11l111ll111_opy_(bstack111ll11llll_opy_, bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢᴭ")))
    bstack11l11l1lll1_opy_ = [element.lower() for element in bstack11l1ll1ll11_opy_]
    bstack111lll11ll1_opy_(bstack111lll1l1l1_opy_, bstack11l11l1lll1_opy_)
    return bstack111lll1l1l1_opy_
def bstack111lll11ll1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1111l1l_opy_ (u"ࠣࠬ࠭࠮࠯ࠨᴮ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111lll11ll1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111lll11ll1_opy_(item, keys)
def bstack1l1ll1l11l1_opy_():
    bstack111llll1111_opy_ = [os.environ.get(bstack1111l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡌࡐࡊ࡙࡟ࡅࡋࡕࠦᴯ")), os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠥࢂࠧᴰ")), bstack1111l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᴱ")), os.path.join(bstack1111l1l_opy_ (u"ࠬ࠵ࡴ࡮ࡲࠪᴲ"), bstack1111l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᴳ"))]
    for path in bstack111llll1111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1111l1l_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢᴴ") + str(path) + bstack1111l1l_opy_ (u"ࠣࠩࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦᴵ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1111l1l_opy_ (u"ࠤࡊ࡭ࡻ࡯࡮ࡨࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠠࡧࡱࡵࠤࠬࠨᴶ") + str(path) + bstack1111l1l_opy_ (u"ࠥࠫࠧᴷ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1111l1l_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦᴸ") + str(path) + bstack1111l1l_opy_ (u"ࠧ࠭ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡪࡤࡷࠥࡺࡨࡦࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴ࠰ࠥᴹ"))
            else:
                logger.debug(bstack1111l1l_opy_ (u"ࠨࡃࡳࡧࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࠦࠧࠣᴺ") + str(path) + bstack1111l1l_opy_ (u"ࠢࠨࠢࡺ࡭ࡹ࡮ࠠࡸࡴ࡬ࡸࡪࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰ࠱ࠦᴻ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1111l1l_opy_ (u"ࠣࡑࡳࡩࡷࡧࡴࡪࡱࡱࠤࡸࡻࡣࡤࡧࡨࡨࡪࡪࠠࡧࡱࡵࠤࠬࠨᴼ") + str(path) + bstack1111l1l_opy_ (u"ࠤࠪ࠲ࠧᴽ"))
            return path
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡹࡵࠦࡦࡪ࡮ࡨࠤࠬࢁࡰࡢࡶ࡫ࢁࠬࡀࠠࠣᴾ") + str(e) + bstack1111l1l_opy_ (u"ࠦࠧᴿ"))
    logger.debug(bstack1111l1l_opy_ (u"ࠧࡇ࡬࡭ࠢࡳࡥࡹ࡮ࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠤᵀ"))
    return None
@measure(event_name=EVENTS.bstack11l1ll1l111_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
def bstack1ll1l1lll1l_opy_(binary_path, bstack1lll11l1l11_opy_, bs_config):
    logger.debug(bstack1111l1l_opy_ (u"ࠨࡃࡶࡴࡵࡩࡳࡺࠠࡄࡎࡌࠤࡕࡧࡴࡩࠢࡩࡳࡺࡴࡤ࠻ࠢࡾࢁࠧᵁ").format(binary_path))
    bstack11l111l11l1_opy_ = bstack1111l1l_opy_ (u"ࠧࠨᵂ")
    bstack111ll1lll1l_opy_ = {
        bstack1111l1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᵃ"): __version__,
        bstack1111l1l_opy_ (u"ࠤࡲࡷࠧᵄ"): platform.system(),
        bstack1111l1l_opy_ (u"ࠥࡳࡸࡥࡡࡳࡥ࡫ࠦᵅ"): platform.machine(),
        bstack1111l1l_opy_ (u"ࠦࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᵆ"): bstack1111l1l_opy_ (u"ࠬ࠶ࠧᵇ"),
        bstack1111l1l_opy_ (u"ࠨࡳࡥ࡭ࡢࡰࡦࡴࡧࡶࡣࡪࡩࠧᵈ"): bstack1111l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᵉ")
    }
    bstack11l111111ll_opy_(bstack111ll1lll1l_opy_)
    try:
        if binary_path:
            bstack111ll1lll1l_opy_[bstack1111l1l_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᵊ")] = subprocess.check_output([binary_path, bstack1111l1l_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥᵋ")]).strip().decode(bstack1111l1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᵌ"))
        response = requests.request(
            bstack1111l1l_opy_ (u"ࠫࡌࡋࡔࠨᵍ"),
            url=bstack11l11l11_opy_(bstack11l1lll1l1l_opy_),
            headers=None,
            auth=(bs_config[bstack1111l1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᵎ")], bs_config[bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᵏ")]),
            json=None,
            params=bstack111ll1lll1l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1111l1l_opy_ (u"ࠧࡶࡴ࡯ࠫᵐ") in data.keys() and bstack1111l1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥࡡࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᵑ") in data.keys():
            logger.debug(bstack1111l1l_opy_ (u"ࠤࡑࡩࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡦ࡮ࡴࡡࡳࡻ࠯ࠤࡨࡻࡲࡳࡧࡱࡸࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥᵒ").format(bstack111ll1lll1l_opy_[bstack1111l1l_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᵓ")]))
            if bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧᵔ") in os.environ:
                logger.debug(bstack1111l1l_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡤࡷࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠡ࡫ࡶࠤࡸ࡫ࡴࠣᵕ"))
                data[bstack1111l1l_opy_ (u"࠭ࡵࡳ࡮ࠪᵖ")] = os.environ[bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪᵗ")]
            bstack111lll1l111_opy_ = bstack11l11llll11_opy_(data[bstack1111l1l_opy_ (u"ࠨࡷࡵࡰࠬᵘ")], bstack1lll11l1l11_opy_)
            bstack11l111l11l1_opy_ = os.path.join(bstack1lll11l1l11_opy_, bstack111lll1l111_opy_)
            os.chmod(bstack11l111l11l1_opy_, 0o777) # bstack111lll11l1l_opy_ permission
            return bstack11l111l11l1_opy_
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡖࡈࡐࠦࡻࡾࠤᵙ").format(e))
    return binary_path
def bstack11l111111ll_opy_(bstack111ll1lll1l_opy_):
    try:
        if bstack1111l1l_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩᵚ") not in bstack111ll1lll1l_opy_[bstack1111l1l_opy_ (u"ࠫࡴࡹࠧᵛ")].lower():
            return
        if os.path.exists(bstack1111l1l_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢᵜ")):
            with open(bstack1111l1l_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣᵝ"), bstack1111l1l_opy_ (u"ࠢࡳࠤᵞ")) as f:
                bstack111llll1ll1_opy_ = {}
                for line in f:
                    if bstack1111l1l_opy_ (u"ࠣ࠿ࠥᵟ") in line:
                        key, value = line.rstrip().split(bstack1111l1l_opy_ (u"ࠤࡀࠦᵠ"), 1)
                        bstack111llll1ll1_opy_[key] = value.strip(bstack1111l1l_opy_ (u"ࠪࠦࡡ࠭ࠧᵡ"))
                bstack111ll1lll1l_opy_[bstack1111l1l_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫᵢ")] = bstack111llll1ll1_opy_.get(bstack1111l1l_opy_ (u"ࠧࡏࡄࠣᵣ"), bstack1111l1l_opy_ (u"ࠨࠢᵤ"))
        elif os.path.exists(bstack1111l1l_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡧ࡬ࡱ࡫ࡱࡩ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨᵥ")):
            bstack111ll1lll1l_opy_[bstack1111l1l_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨᵦ")] = bstack1111l1l_opy_ (u"ࠩࡤࡰࡵ࡯࡮ࡦࠩᵧ")
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡨ࡮ࡹࡴࡳࡱࠣࡳ࡫ࠦ࡬ࡪࡰࡸࡼࠧᵨ") + e)
@measure(event_name=EVENTS.bstack11l1ll11l1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
def bstack11l11llll11_opy_(bstack111llll1l1l_opy_, bstack111llll1lll_opy_):
    logger.debug(bstack1111l1l_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰ࠾ࠥࠨᵩ") + str(bstack111llll1l1l_opy_) + bstack1111l1l_opy_ (u"ࠧࠨᵪ"))
    zip_path = os.path.join(bstack111llll1lll_opy_, bstack1111l1l_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡢࡪ࡮ࡲࡥ࠯ࡼ࡬ࡴࠧᵫ"))
    bstack111lll1l111_opy_ = bstack1111l1l_opy_ (u"ࠧࠨᵬ")
    with requests.get(bstack111llll1l1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1111l1l_opy_ (u"ࠣࡹࡥࠦᵭ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1111l1l_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠦᵮ"))
    with zipfile.ZipFile(zip_path, bstack1111l1l_opy_ (u"ࠪࡶࠬᵯ")) as zip_ref:
        bstack11l11lllll1_opy_ = zip_ref.namelist()
        if len(bstack11l11lllll1_opy_) > 0:
            bstack111lll1l111_opy_ = bstack11l11lllll1_opy_[0] # bstack11l11lll1ll_opy_ bstack11l1l1lllll_opy_ will be bstack111lll1lll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111llll1lll_opy_)
        logger.debug(bstack1111l1l_opy_ (u"ࠦࡋ࡯࡬ࡦࡵࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡨࡼࡹࡸࡡࡤࡶࡨࡨࠥࡺ࡯ࠡࠩࠥᵰ") + str(bstack111llll1lll_opy_) + bstack1111l1l_opy_ (u"ࠧ࠭ࠢᵱ"))
    os.remove(zip_path)
    return bstack111lll1l111_opy_
def get_cli_dir():
    bstack11l11111111_opy_ = bstack1l1ll1l11l1_opy_()
    if bstack11l11111111_opy_:
        bstack1lll11l1l11_opy_ = os.path.join(bstack11l11111111_opy_, bstack1111l1l_opy_ (u"ࠨࡣ࡭࡫ࠥᵲ"))
        if not os.path.exists(bstack1lll11l1l11_opy_):
            os.makedirs(bstack1lll11l1l11_opy_, mode=0o777, exist_ok=True)
        return bstack1lll11l1l11_opy_
    else:
        raise FileNotFoundError(bstack1111l1l_opy_ (u"ࠢࡏࡱࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠥᵳ"))
def bstack1ll1l1l1lll_opy_(bstack1lll11l1l11_opy_):
    bstack1111l1l_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡩ࡯ࠢࡤࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠥࠦࠧᵴ")
    bstack11l1111ll11_opy_ = [
        os.path.join(bstack1lll11l1l11_opy_, f)
        for f in os.listdir(bstack1lll11l1l11_opy_)
        if os.path.isfile(os.path.join(bstack1lll11l1l11_opy_, f)) and f.startswith(bstack1111l1l_opy_ (u"ࠤࡥ࡭ࡳࡧࡲࡺ࠯ࠥᵵ"))
    ]
    if len(bstack11l1111ll11_opy_) > 0:
        return max(bstack11l1111ll11_opy_, key=os.path.getmtime) # get bstack11l111lll11_opy_ binary
    return bstack1111l1l_opy_ (u"ࠥࠦᵶ")
def bstack11ll11lllll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll11lll11l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll11lll11l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l11lll111_opy_(data, keys, default=None):
    bstack1111l1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡧࡦࡦ࡮ࡼࠤ࡬࡫ࡴࠡࡣࠣࡲࡪࡹࡴࡦࡦࠣࡺࡦࡲࡵࡦࠢࡩࡶࡴࡳࠠࡢࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡡࡵࡣ࠽ࠤ࡙࡮ࡥࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹࠦࡴࡰࠢࡷࡶࡦࡼࡥࡳࡵࡨ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢ࡮ࡩࡾࡹ࠺ࠡࡃࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡰ࡫ࡹࡴ࠱࡬ࡲࡩ࡯ࡣࡦࡵࠣࡶࡪࡶࡲࡦࡵࡨࡲࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡩ࡫ࡧࡵ࡭ࡶ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡸࡴࠦࡲࡦࡶࡸࡶࡳࠦࡩࡧࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡷ࡫ࡴࡶࡴࡱ࠾࡚ࠥࡨࡦࠢࡹࡥࡱࡻࡥࠡࡣࡷࠤࡹ࡮ࡥࠡࡰࡨࡷࡹ࡫ࡤࠡࡲࡤࡸ࡭࠲ࠠࡰࡴࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤ࡮࡬ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᵷ")
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