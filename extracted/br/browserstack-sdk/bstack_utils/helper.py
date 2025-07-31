# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
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
from bstack_utils.constants import (bstack11l11111_opy_, bstack1llll1llll_opy_, bstack1l111111ll_opy_,
                                    bstack11l1lllll1l_opy_, bstack11l1lll1lll_opy_, bstack11l1ll11ll1_opy_, bstack11l1ll1l111_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11ll1111_opy_, bstack11l1l11111_opy_
from bstack_utils.proxy import bstack1lll1lll1_opy_, bstack1l1111l1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1ll11lll_opy_
from bstack_utils.bstack1ll11l1l1_opy_ import bstack11lll11l1l_opy_
from browserstack_sdk._version import __version__
bstack11l11llll_opy_ = Config.bstack11l111llll_opy_()
logger = bstack1l1ll11lll_opy_.get_logger(__name__, bstack1l1ll11lll_opy_.bstack1ll1lll11l1_opy_())
def bstack11ll1l1l1l1_opy_(config):
    return config[bstack1l11l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᫯")]
def bstack11ll1l11111_opy_(config):
    return config[bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᫰")]
def bstack11l11ll1ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11lll111_opy_(obj):
    values = []
    bstack11l111l1ll1_opy_ = re.compile(bstack1l11l11_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨ᫱"), re.I)
    for key in obj.keys():
        if bstack11l111l1ll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11l11lll_opy_(config):
    tags = []
    tags.extend(bstack11l11lll111_opy_(os.environ))
    tags.extend(bstack11l11lll111_opy_(config))
    return tags
def bstack111ll1l1lll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111lllll1ll_opy_(bstack111llllll1l_opy_):
    if not bstack111llllll1l_opy_:
        return bstack1l11l11_opy_ (u"ࠪࠫ᫲")
    return bstack1l11l11_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧ᫳").format(bstack111llllll1l_opy_.name, bstack111llllll1l_opy_.email)
def bstack11lll1111l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l111111ll_opy_ = repo.common_dir
        info = {
            bstack1l11l11_opy_ (u"ࠧࡹࡨࡢࠤ᫴"): repo.head.commit.hexsha,
            bstack1l11l11_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤ᫵"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l11l11_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢ᫶"): repo.active_branch.name,
            bstack1l11l11_opy_ (u"ࠣࡶࡤ࡫ࠧ᫷"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l11l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧ᫸"): bstack111lllll1ll_opy_(repo.head.commit.committer),
            bstack1l11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦ᫹"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l11l11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦ᫺"): bstack111lllll1ll_opy_(repo.head.commit.author),
            bstack1l11l11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥ᫻"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l11l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᫼"): repo.head.commit.message,
            bstack1l11l11_opy_ (u"ࠢࡳࡱࡲࡸࠧ᫽"): repo.git.rev_parse(bstack1l11l11_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥ᫾")),
            bstack1l11l11_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥ᫿"): bstack11l111111ll_opy_,
            bstack1l11l11_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᬀ"): subprocess.check_output([bstack1l11l11_opy_ (u"ࠦ࡬࡯ࡴࠣᬁ"), bstack1l11l11_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣᬂ"), bstack1l11l11_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤᬃ")]).strip().decode(
                bstack1l11l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᬄ")),
            bstack1l11l11_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᬅ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l11l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᬆ"): repo.git.rev_list(
                bstack1l11l11_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥᬇ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111lll1ll1l_opy_ = []
        for remote in remotes:
            bstack111llll1111_opy_ = {
                bstack1l11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᬈ"): remote.name,
                bstack1l11l11_opy_ (u"ࠧࡻࡲ࡭ࠤᬉ"): remote.url,
            }
            bstack111lll1ll1l_opy_.append(bstack111llll1111_opy_)
        bstack111ll1l1l11_opy_ = {
            bstack1l11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬊ"): bstack1l11l11_opy_ (u"ࠢࡨ࡫ࡷࠦᬋ"),
            **info,
            bstack1l11l11_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤᬌ"): bstack111lll1ll1l_opy_
        }
        bstack111ll1l1l11_opy_ = bstack111llll11l1_opy_(bstack111ll1l1l11_opy_)
        return bstack111ll1l1l11_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᬍ").format(err))
        return {}
def bstack11l1111lll1_opy_(bstack111ll1lll1l_opy_=None):
    bstack1l11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࡢ࡮࡯ࡽࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤࡺࡹࡥࠡࡥࡤࡷࡪࡹࠠࡧࡱࡵࠤࡪࡧࡣࡩࠢࡩࡳࡱࡪࡥࡳࠢ࡬ࡲࠥࡺࡨࡦࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࠨ࡭࡫ࡶࡸ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡵࡧࡴࡩࡵࠣࡸࡴࠦࡥࡹࡶࡵࡥࡨࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡳࡱࡰ࠲ࠥࡊࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣ࡟ࡴࡹ࠮ࡨࡧࡷࡧࡼࡪࠨࠪ࡟࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡩ࡯ࡣࡵࡵ࠯ࠤࡪࡧࡣࡩࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡤࠤ࡫ࡵ࡬ࡥࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᬎ")
    if bstack111ll1lll1l_opy_ is None:
        bstack111ll1lll1l_opy_ = [os.getcwd()]
    results = []
    for folder in bstack111ll1lll1l_opy_:
        try:
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l11l11_opy_ (u"ࠦࡵࡸࡉࡥࠤᬏ"): bstack1l11l11_opy_ (u"ࠧࠨᬐ"),
                bstack1l11l11_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᬑ"): [],
                bstack1l11l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᬒ"): [],
                bstack1l11l11_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣᬓ"): bstack1l11l11_opy_ (u"ࠤࠥᬔ"),
                bstack1l11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦᬕ"): [],
                bstack1l11l11_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᬖ"): bstack1l11l11_opy_ (u"ࠧࠨᬗ"),
                bstack1l11l11_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨᬘ"): bstack1l11l11_opy_ (u"ࠢࠣᬙ"),
                bstack1l11l11_opy_ (u"ࠣࡲࡵࡖࡦࡽࡄࡪࡨࡩࠦᬚ"): bstack1l11l11_opy_ (u"ࠤࠥᬛ")
            }
            bstack11l11l1ll1l_opy_ = repo.active_branch.name
            bstack111lll1l11l_opy_ = repo.head.commit
            result[bstack1l11l11_opy_ (u"ࠥࡴࡷࡏࡤࠣᬜ")] = bstack111lll1l11l_opy_.hexsha
            bstack111lll1lll1_opy_ = _111lll11lll_opy_(repo)
            logger.debug(bstack1l11l11_opy_ (u"ࠦࡇࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠽ࠤࠧᬝ") + str(bstack111lll1lll1_opy_) + bstack1l11l11_opy_ (u"ࠧࠨᬞ"))
            if bstack111lll1lll1_opy_:
                try:
                    bstack11l1111l11l_opy_ = repo.git.diff(bstack1l11l11_opy_ (u"ࠨ࠭࠮ࡰࡤࡱࡪ࠳࡯࡯࡮ࡼࠦᬟ"), bstack1ll1ll111l1_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦᬠ")).split(bstack1l11l11_opy_ (u"ࠨ࡞ࡱࠫᬡ"))
                    logger.debug(bstack1l11l11_opy_ (u"ࠤࡆ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡥࡩࡹࡽࡥࡦࡰࠣࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿࠣࡥࡳࡪࠠࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿ࠽ࠤࠧᬢ") + str(bstack11l1111l11l_opy_) + bstack1l11l11_opy_ (u"ࠥࠦᬣ"))
                    result[bstack1l11l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᬤ")] = [f.strip() for f in bstack11l1111l11l_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1ll111l1_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᬥ")))
                except Exception:
                    logger.debug(bstack1l11l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠯ࠢࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡷ࡫ࡣࡦࡰࡷࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠨᬦ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l11l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᬧ")] = _11l111l11ll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l11l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᬨ")] = _11l111l11ll_opy_(commits[:5])
            bstack11l11l11ll1_opy_ = set()
            bstack11l111ll11l_opy_ = []
            for commit in commits:
                logger.debug(bstack1l11l11_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰ࡭ࡹࡀࠠࠣᬩ") + str(commit.message) + bstack1l11l11_opy_ (u"ࠥࠦᬪ"))
                bstack111llll11ll_opy_ = commit.author.name if commit.author else bstack1l11l11_opy_ (u"࡚ࠦࡴ࡫࡯ࡱࡺࡲࠧᬫ")
                bstack11l11l11ll1_opy_.add(bstack111llll11ll_opy_)
                bstack11l111ll11l_opy_.append({
                    bstack1l11l11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᬬ"): commit.message.strip(),
                    bstack1l11l11_opy_ (u"ࠨࡵࡴࡧࡵࠦᬭ"): bstack111llll11ll_opy_
                })
            result[bstack1l11l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᬮ")] = list(bstack11l11l11ll1_opy_)
            result[bstack1l11l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᬯ")] = bstack11l111ll11l_opy_
            result[bstack1l11l11_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᬰ")] = bstack111lll1l11l_opy_.committed_datetime.strftime(bstack1l11l11_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨࠧᬱ"))
            if (not result[bstack1l11l11_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᬲ")] or result[bstack1l11l11_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᬳ")].strip() == bstack1l11l11_opy_ (u"ࠨ᬴ࠢ")) and bstack111lll1l11l_opy_.message:
                bstack11l11l1ll11_opy_ = bstack111lll1l11l_opy_.message.strip().split(bstack1l11l11_opy_ (u"ࠧ࡝ࡰࠪᬵ"))
                result[bstack1l11l11_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤᬶ")] = bstack11l11l1ll11_opy_[0] if bstack11l11l1ll11_opy_ else bstack1l11l11_opy_ (u"ࠤࠥᬷ")
                if len(bstack11l11l1ll11_opy_) > 2:
                    result[bstack1l11l11_opy_ (u"ࠥࡴࡷࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥᬸ")] = bstack1l11l11_opy_ (u"ࠫࡡࡴࠧᬹ").join(bstack11l11l1ll11_opy_[2:]).strip()
            results.append(result)
        except git.InvalidGitRepositoryError:
            results.append({
                bstack1l11l11_opy_ (u"ࠧࡶࡲࡊࡦࠥᬺ"): bstack1l11l11_opy_ (u"ࠨࠢᬻ"),
                bstack1l11l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᬼ"): [],
                bstack1l11l11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᬽ"): [],
                bstack1l11l11_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᬾ"): bstack1l11l11_opy_ (u"ࠥࠦᬿ"),
                bstack1l11l11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧᭀ"): [],
                bstack1l11l11_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᭁ"): bstack1l11l11_opy_ (u"ࠨࠢᭂ"),
                bstack1l11l11_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢᭃ"): bstack1l11l11_opy_ (u"ࠣࠤ᭄"),
                bstack1l11l11_opy_ (u"ࠤࡳࡶࡗࡧࡷࡅ࡫ࡩࡪࠧᭅ"): bstack1l11l11_opy_ (u"ࠥࠦᭆ")
            })
        except Exception as err:
            logger.error(bstack1l11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࠫࡪࡴࡲࡤࡦࡴ࠽ࠤࢀ࡬࡯࡭ࡦࡨࡶࢂ࠯࠺ࠡࠤᭇ") + str(err) + bstack1l11l11_opy_ (u"ࠧࠨᭈ"))
            results.append({
                bstack1l11l11_opy_ (u"ࠨࡰࡳࡋࡧࠦᭉ"): bstack1l11l11_opy_ (u"ࠢࠣᭊ"),
                bstack1l11l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᭋ"): [],
                bstack1l11l11_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᭌ"): [],
                bstack1l11l11_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥ᭍"): bstack1l11l11_opy_ (u"ࠦࠧ᭎"),
                bstack1l11l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨ᭏"): [],
                bstack1l11l11_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢ᭐"): bstack1l11l11_opy_ (u"ࠢࠣ᭑"),
                bstack1l11l11_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣ᭒"): bstack1l11l11_opy_ (u"ࠤࠥ᭓"),
                bstack1l11l11_opy_ (u"ࠥࡴࡷࡘࡡࡸࡆ࡬ࡪ࡫ࠨ᭔"): bstack1l11l11_opy_ (u"ࠦࠧ᭕")
            })
    return results
def _111lll11lll_opy_(repo):
    bstack1l11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡚ࠥࡲࡺࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶ࡫ࡩࠥࡨࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࠬࡲࡧࡩ࡯࠮ࠣࡱࡦࡹࡴࡦࡴ࠯ࠤࡩ࡫ࡶࡦ࡮ࡲࡴ࠱ࠦࡥࡵࡥ࠱࠭ࠏࠦࠠࠡࠢࠥࠦࠧ᭖")
    try:
        bstack11l11l1llll_opy_ = [bstack1l11l11_opy_ (u"࠭࡭ࡢ࡫ࡱࠫ᭗"), bstack1l11l11_opy_ (u"ࠧ࡮ࡣࡶࡸࡪࡸࠧ᭘"), bstack1l11l11_opy_ (u"ࠨࡦࡨࡺࡪࡲ࡯ࡱࠩ᭙"), bstack1l11l11_opy_ (u"ࠩࡧࡩࡻ࠭᭚")]
        for branch_name in bstack11l11l1llll_opy_:
            try:
                repo.heads[branch_name]
                return branch_name
            except IndexError:
                try:
                    repo.remotes.origin.refs[branch_name]
                    return bstack1l11l11_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰ࠲ࡿࢂࠨ᭛").format(branch_name)
                except (AttributeError, IndexError):
                    continue
    except Exception:
        pass
    return None
def _11l111l11ll_opy_(commits):
    bstack1l11l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡢࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᭜")
    bstack11l1111l11l_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111lllllll1_opy_ in diff:
                        if bstack111lllllll1_opy_.a_path:
                            bstack11l1111l11l_opy_.add(bstack111lllllll1_opy_.a_path)
                        if bstack111lllllll1_opy_.b_path:
                            bstack11l1111l11l_opy_.add(bstack111lllllll1_opy_.b_path)
    except Exception:
        pass
    return list(bstack11l1111l11l_opy_)
def bstack111llll11l1_opy_(bstack111ll1l1l11_opy_):
    bstack11l11ll1ll1_opy_ = bstack11l11lll11l_opy_(bstack111ll1l1l11_opy_)
    if bstack11l11ll1ll1_opy_ and bstack11l11ll1ll1_opy_ > bstack11l1lllll1l_opy_:
        bstack11l11lll1l1_opy_ = bstack11l11ll1ll1_opy_ - bstack11l1lllll1l_opy_
        bstack11l1111ll11_opy_ = bstack11l11111l11_opy_(bstack111ll1l1l11_opy_[bstack1l11l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᭝")], bstack11l11lll1l1_opy_)
        bstack111ll1l1l11_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᭞")] = bstack11l1111ll11_opy_
        logger.info(bstack1l11l11_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤ᭟")
                    .format(bstack11l11lll11l_opy_(bstack111ll1l1l11_opy_) / 1024))
    return bstack111ll1l1l11_opy_
def bstack11l11lll11l_opy_(bstack11l11l1l1l_opy_):
    try:
        if bstack11l11l1l1l_opy_:
            bstack111ll1lll11_opy_ = json.dumps(bstack11l11l1l1l_opy_)
            bstack111lll111l1_opy_ = sys.getsizeof(bstack111ll1lll11_opy_)
            return bstack111lll111l1_opy_
    except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣ᭠").format(e))
    return -1
def bstack11l11111l11_opy_(field, bstack11l11ll1lll_opy_):
    try:
        bstack11l11l11111_opy_ = len(bytes(bstack11l1lll1lll_opy_, bstack1l11l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᭡")))
        bstack111llll1lll_opy_ = bytes(field, bstack1l11l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᭢"))
        bstack11l1111111l_opy_ = len(bstack111llll1lll_opy_)
        bstack11l111l1111_opy_ = ceil(bstack11l1111111l_opy_ - bstack11l11ll1lll_opy_ - bstack11l11l11111_opy_)
        if bstack11l111l1111_opy_ > 0:
            bstack11l11111lll_opy_ = bstack111llll1lll_opy_[:bstack11l111l1111_opy_].decode(bstack1l11l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᭣"), errors=bstack1l11l11_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬ᭤")) + bstack11l1lll1lll_opy_
            return bstack11l11111lll_opy_
    except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦ᭥").format(e))
    return field
def bstack1ll1ll1l_opy_():
    env = os.environ
    if (bstack1l11l11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᭦") in env and len(env[bstack1l11l11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ᭧")]) > 0) or (
            bstack1l11l11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᭨") in env and len(env[bstack1l11l11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᭩")]) > 0):
        return {
            bstack1l11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭪"): bstack1l11l11_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨ᭫"),
            bstack1l11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᭬"): env.get(bstack1l11l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᭭")),
            bstack1l11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᭮"): env.get(bstack1l11l11_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦ᭯")),
            bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭰"): env.get(bstack1l11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᭱"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠧࡉࡉࠣ᭲")) == bstack1l11l11_opy_ (u"ࠨࡴࡳࡷࡨࠦ᭳") and bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ᭴"))):
        return {
            bstack1l11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭵"): bstack1l11l11_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦ᭶"),
            bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᭷"): env.get(bstack1l11l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᭸")),
            bstack1l11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᭹"): env.get(bstack1l11l11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥ᭺")),
            bstack1l11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᭻"): env.get(bstack1l11l11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦ᭼"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠤࡆࡍࠧ᭽")) == bstack1l11l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ᭾") and bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦ᭿"))):
        return {
            bstack1l11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᮀ"): bstack1l11l11_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᮁ"),
            bstack1l11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮂ"): env.get(bstack1l11l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᮃ")),
            bstack1l11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᮄ"): env.get(bstack1l11l11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᮅ")),
            bstack1l11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᮆ"): env.get(bstack1l11l11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᮇ"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠨࡃࡊࠤᮈ")) == bstack1l11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᮉ") and env.get(bstack1l11l11_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᮊ")) == bstack1l11l11_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᮋ"):
        return {
            bstack1l11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᮌ"): bstack1l11l11_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᮍ"),
            bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮎ"): None,
            bstack1l11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᮏ"): None,
            bstack1l11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮐ"): None
        }
    if env.get(bstack1l11l11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᮑ")) and env.get(bstack1l11l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᮒ")):
        return {
            bstack1l11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᮓ"): bstack1l11l11_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᮔ"),
            bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮕ"): env.get(bstack1l11l11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᮖ")),
            bstack1l11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮗ"): None,
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮘ"): env.get(bstack1l11l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᮙ"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠥࡇࡎࠨᮚ")) == bstack1l11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᮛ") and bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᮜ"))):
        return {
            bstack1l11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᮝ"): bstack1l11l11_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᮞ"),
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮟ"): env.get(bstack1l11l11_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᮠ")),
            bstack1l11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮡ"): None,
            bstack1l11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᮢ"): env.get(bstack1l11l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᮣ"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠨࡃࡊࠤᮤ")) == bstack1l11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᮥ") and bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᮦ"))):
        return {
            bstack1l11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮧ"): bstack1l11l11_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᮨ"),
            bstack1l11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᮩ"): env.get(bstack1l11l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏ᮪ࠦ")),
            bstack1l11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᮫ࠣ"): env.get(bstack1l11l11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᮬ")),
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮭ"): env.get(bstack1l11l11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᮮ"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠥࡇࡎࠨᮯ")) == bstack1l11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ᮰") and bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣ᮱"))):
        return {
            bstack1l11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᮲"): bstack1l11l11_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢ᮳"),
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᮴"): env.get(bstack1l11l11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨ᮵")),
            bstack1l11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᮶"): env.get(bstack1l11l11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᮷")),
            bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᮸"): env.get(bstack1l11l11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤ᮹"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠢࡄࡋࠥᮺ")) == bstack1l11l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᮻ") and bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᮼ"))):
        return {
            bstack1l11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᮽ"): bstack1l11l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᮾ"),
            bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮿ"): env.get(bstack1l11l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᯀ")),
            bstack1l11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᯁ"): env.get(bstack1l11l11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᯂ")) or env.get(bstack1l11l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᯃ")),
            bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᯄ"): env.get(bstack1l11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᯅ"))
        }
    if bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᯆ"))):
        return {
            bstack1l11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᯇ"): bstack1l11l11_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᯈ"),
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᯉ"): bstack1l11l11_opy_ (u"ࠤࡾࢁࢀࢃࠢᯊ").format(env.get(bstack1l11l11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᯋ")), env.get(bstack1l11l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᯌ"))),
            bstack1l11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᯍ"): env.get(bstack1l11l11_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᯎ")),
            bstack1l11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᯏ"): env.get(bstack1l11l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᯐ"))
        }
    if bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᯑ"))):
        return {
            bstack1l11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᯒ"): bstack1l11l11_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᯓ"),
            bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯔ"): bstack1l11l11_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᯕ").format(env.get(bstack1l11l11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ᯖ")), env.get(bstack1l11l11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᯗ")), env.get(bstack1l11l11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᯘ")), env.get(bstack1l11l11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᯙ"))),
            bstack1l11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᯚ"): env.get(bstack1l11l11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᯛ")),
            bstack1l11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᯜ"): env.get(bstack1l11l11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᯝ"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᯞ")) and env.get(bstack1l11l11_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᯟ")):
        return {
            bstack1l11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᯠ"): bstack1l11l11_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᯡ"),
            bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯢ"): bstack1l11l11_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᯣ").format(env.get(bstack1l11l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᯤ")), env.get(bstack1l11l11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ᯥ")), env.get(bstack1l11l11_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅ᯦ࠩ"))),
            bstack1l11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᯧ"): env.get(bstack1l11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᯨ")),
            bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᯩ"): env.get(bstack1l11l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᯪ"))
        }
    if any([env.get(bstack1l11l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᯫ")), env.get(bstack1l11l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᯬ")), env.get(bstack1l11l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᯭ"))]):
        return {
            bstack1l11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᯮ"): bstack1l11l11_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᯯ"),
            bstack1l11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯰ"): env.get(bstack1l11l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᯱ")),
            bstack1l11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᯲"): env.get(bstack1l11l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᯳")),
            bstack1l11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᯴"): env.get(bstack1l11l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᯵"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ᯶")):
        return {
            bstack1l11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᯷"): bstack1l11l11_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨ᯸"),
            bstack1l11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᯹"): env.get(bstack1l11l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥ᯺")),
            bstack1l11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᯻"): env.get(bstack1l11l11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤ᯼")),
            bstack1l11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᯽"): env.get(bstack1l11l11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ᯾"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢ᯿")) or env.get(bstack1l11l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᰀ")):
        return {
            bstack1l11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᰁ"): bstack1l11l11_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᰂ"),
            bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᰃ"): env.get(bstack1l11l11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᰄ")),
            bstack1l11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᰅ"): bstack1l11l11_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᰆ") if env.get(bstack1l11l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᰇ")) else None,
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰈ"): env.get(bstack1l11l11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᰉ"))
        }
    if any([env.get(bstack1l11l11_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᰊ")), env.get(bstack1l11l11_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᰋ")), env.get(bstack1l11l11_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᰌ"))]):
        return {
            bstack1l11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰍ"): bstack1l11l11_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᰎ"),
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰏ"): None,
            bstack1l11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᰐ"): env.get(bstack1l11l11_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᰑ")),
            bstack1l11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᰒ"): env.get(bstack1l11l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᰓ"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᰔ")):
        return {
            bstack1l11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᰕ"): bstack1l11l11_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦᰖ"),
            bstack1l11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᰗ"): env.get(bstack1l11l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᰘ")),
            bstack1l11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᰙ"): bstack1l11l11_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᰚ").format(env.get(bstack1l11l11_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᰛ"))) if env.get(bstack1l11l11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᰜ")) else None,
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰝ"): env.get(bstack1l11l11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᰞ"))
        }
    if bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᰟ"))):
        return {
            bstack1l11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᰠ"): bstack1l11l11_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᰡ"),
            bstack1l11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᰢ"): env.get(bstack1l11l11_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦᰣ")),
            bstack1l11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᰤ"): env.get(bstack1l11l11_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧᰥ")),
            bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰦ"): env.get(bstack1l11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᰧ"))
        }
    if bstack11lll11ll1_opy_(env.get(bstack1l11l11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᰨ"))):
        return {
            bstack1l11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰩ"): bstack1l11l11_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᰪ"),
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰫ"): bstack1l11l11_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᰬ").format(env.get(bstack1l11l11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᰭ")), env.get(bstack1l11l11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᰮ")), env.get(bstack1l11l11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᰯ"))),
            bstack1l11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᰰ"): env.get(bstack1l11l11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᰱ")),
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰲ"): env.get(bstack1l11l11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᰳ"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠥࡇࡎࠨᰴ")) == bstack1l11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᰵ") and env.get(bstack1l11l11_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᰶ")) == bstack1l11l11_opy_ (u"ࠨ࠱᰷ࠣ"):
        return {
            bstack1l11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᰸"): bstack1l11l11_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣ᰹"),
            bstack1l11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᰺"): bstack1l11l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨ᰻").format(env.get(bstack1l11l11_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨ᰼"))),
            bstack1l11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᰽"): None,
            bstack1l11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᰾"): None,
        }
    if env.get(bstack1l11l11_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ᰿")):
        return {
            bstack1l11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᱀"): bstack1l11l11_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦ᱁"),
            bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᱂"): None,
            bstack1l11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᱃"): env.get(bstack1l11l11_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨ᱄")),
            bstack1l11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᱅"): env.get(bstack1l11l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᱆"))
        }
    if any([env.get(bstack1l11l11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦ᱇")), env.get(bstack1l11l11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤ᱈")), env.get(bstack1l11l11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣ᱉")), env.get(bstack1l11l11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧ᱊"))]):
        return {
            bstack1l11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᱋"): bstack1l11l11_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤ᱌"),
            bstack1l11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᱍ"): None,
            bstack1l11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᱎ"): env.get(bstack1l11l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᱏ")) or None,
            bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᱐"): env.get(bstack1l11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᱑"), 0)
        }
    if env.get(bstack1l11l11_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᱒")):
        return {
            bstack1l11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᱓"): bstack1l11l11_opy_ (u"ࠢࡈࡱࡆࡈࠧ᱔"),
            bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᱕"): None,
            bstack1l11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᱖"): env.get(bstack1l11l11_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᱗")),
            bstack1l11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᱘"): env.get(bstack1l11l11_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦ᱙"))
        }
    if env.get(bstack1l11l11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᱚ")):
        return {
            bstack1l11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᱛ"): bstack1l11l11_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᱜ"),
            bstack1l11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᱝ"): env.get(bstack1l11l11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᱞ")),
            bstack1l11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᱟ"): env.get(bstack1l11l11_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᱠ")),
            bstack1l11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᱡ"): env.get(bstack1l11l11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᱢ"))
        }
    return {bstack1l11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᱣ"): None}
def get_host_info():
    return {
        bstack1l11l11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᱤ"): platform.node(),
        bstack1l11l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᱥ"): platform.system(),
        bstack1l11l11_opy_ (u"ࠦࡹࡿࡰࡦࠤᱦ"): platform.machine(),
        bstack1l11l11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᱧ"): platform.version(),
        bstack1l11l11_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᱨ"): platform.architecture()[0]
    }
def bstack1l11l1l1ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111ll1l11l1_opy_():
    if bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᱩ")):
        return bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᱪ")
    return bstack1l11l11_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᱫ")
def bstack11l11ll1l11_opy_(driver):
    info = {
        bstack1l11l11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᱬ"): driver.capabilities,
        bstack1l11l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᱭ"): driver.session_id,
        bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᱮ"): driver.capabilities.get(bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᱯ"), None),
        bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᱰ"): driver.capabilities.get(bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᱱ"), None),
        bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᱲ"): driver.capabilities.get(bstack1l11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᱳ"), None),
        bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᱴ"):driver.capabilities.get(bstack1l11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᱵ"), None),
    }
    if bstack111ll1l11l1_opy_() == bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᱶ"):
        if bstack1ll111ll11_opy_():
            info[bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᱷ")] = bstack1l11l11_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᱸ")
        elif driver.capabilities.get(bstack1l11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᱹ"), {}).get(bstack1l11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᱺ"), False):
            info[bstack1l11l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᱻ")] = bstack1l11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᱼ")
        else:
            info[bstack1l11l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᱽ")] = bstack1l11l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ᱾")
    return info
def bstack1ll111ll11_opy_():
    if bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᱿")):
        return True
    if bstack11lll11ll1_opy_(os.environ.get(bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᲀ"), None)):
        return True
    return False
def bstack1l11lllll_opy_(bstack11l1111l1l1_opy_, url, data, config):
    headers = config.get(bstack1l11l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᲁ"), None)
    proxies = bstack1lll1lll1_opy_(config, url)
    auth = config.get(bstack1l11l11_opy_ (u"ࠫࡦࡻࡴࡩࠩᲂ"), None)
    response = requests.request(
            bstack11l1111l1l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll1l11ll1_opy_(bstack1111111l1_opy_, size):
    bstack11ll1lllll_opy_ = []
    while len(bstack1111111l1_opy_) > size:
        bstack1lllll11l1_opy_ = bstack1111111l1_opy_[:size]
        bstack11ll1lllll_opy_.append(bstack1lllll11l1_opy_)
        bstack1111111l1_opy_ = bstack1111111l1_opy_[size:]
    bstack11ll1lllll_opy_.append(bstack1111111l1_opy_)
    return bstack11ll1lllll_opy_
def bstack111llll1l11_opy_(message, bstack11l1l1111ll_opy_=False):
    os.write(1, bytes(message, bstack1l11l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᲃ")))
    os.write(1, bytes(bstack1l11l11_opy_ (u"࠭࡜࡯ࠩᲄ"), bstack1l11l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᲅ")))
    if bstack11l1l1111ll_opy_:
        with open(bstack1l11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧᲆ") + os.environ[bstack1l11l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᲇ")] + bstack1l11l11_opy_ (u"ࠪ࠲ࡱࡵࡧࠨᲈ"), bstack1l11l11_opy_ (u"ࠫࡦ࠭Ᲊ")) as f:
            f.write(message + bstack1l11l11_opy_ (u"ࠬࡢ࡮ࠨᲊ"))
def bstack1l1l1lll111_opy_():
    return os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ᲋")].lower() == bstack1l11l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ᲌")
def bstack1ll11ll11l_opy_():
    return bstack1111ll1111_opy_().replace(tzinfo=None).isoformat() + bstack1l11l11_opy_ (u"ࠨ࡜ࠪ᲍")
def bstack11l111lll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l11l11_opy_ (u"ࠩ࡝ࠫ᲎"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l11l11_opy_ (u"ࠪ࡞ࠬ᲏")))).total_seconds() * 1000
def bstack111lll1l1ll_opy_(timestamp):
    return bstack11l1l1111l1_opy_(timestamp).isoformat() + bstack1l11l11_opy_ (u"ࠫ࡟࠭Ა")
def bstack11l11l1l111_opy_(bstack111llllll11_opy_):
    date_format = bstack1l11l11_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᲑ")
    bstack11l11llll1l_opy_ = datetime.datetime.strptime(bstack111llllll11_opy_, date_format)
    return bstack11l11llll1l_opy_.isoformat() + bstack1l11l11_opy_ (u"࡚࠭ࠨᲒ")
def bstack11l11l1l1ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᲓ")
    else:
        return bstack1l11l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᲔ")
def bstack11lll11ll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l11l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᲕ")
def bstack11l11lll1ll_opy_(val):
    return val.__str__().lower() == bstack1l11l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᲖ")
def bstack111l1l1l11_opy_(bstack11l11ll1l1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11ll1l1l_opy_ as e:
                print(bstack1l11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᲗ").format(func.__name__, bstack11l11ll1l1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111lllll111_opy_(bstack11l11ll11ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11ll11ll_opy_(cls, *args, **kwargs)
            except bstack11l11ll1l1l_opy_ as e:
                print(bstack1l11l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᲘ").format(bstack11l11ll11ll_opy_.__name__, bstack11l11ll1l1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111lllll111_opy_
    else:
        return decorator
def bstack1ll111llll_opy_(bstack11111llll1_opy_):
    if os.getenv(bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᲙ")) is not None:
        return bstack11lll11ll1_opy_(os.getenv(bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᲚ")))
    if bstack1l11l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲛ") in bstack11111llll1_opy_ and bstack11l11lll1ll_opy_(bstack11111llll1_opy_[bstack1l11l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ნ")]):
        return False
    if bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲝ") in bstack11111llll1_opy_ and bstack11l11lll1ll_opy_(bstack11111llll1_opy_[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Პ")]):
        return False
    return True
def bstack1l1l11ll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l111111l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᲟ"), None)
        return bstack11l111111l1_opy_ is None or bstack11l111111l1_opy_ == bstack1l11l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᲠ")
    except Exception as e:
        return False
def bstack1l11ll1lll_opy_(hub_url, CONFIG):
    if bstack11l1l111_opy_() <= version.parse(bstack1l11l11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᲡ")):
        if hub_url:
            return bstack1l11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᲢ") + hub_url + bstack1l11l11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᲣ")
        return bstack1llll1llll_opy_
    if hub_url:
        return bstack1l11l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᲤ") + hub_url + bstack1l11l11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᲥ")
    return bstack1l111111ll_opy_
def bstack111llll1l1l_opy_():
    return isinstance(os.getenv(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᲦ")), str)
def bstack1ll11llll_opy_(url):
    return urlparse(url).hostname
def bstack11lll111l1_opy_(hostname):
    for bstack111lll11l_opy_ in bstack11l11111_opy_:
        regex = re.compile(bstack111lll11l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l111llll1_opy_(bstack11l111lll11_opy_, file_name, logger):
    bstack1l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"࠭ࡾࠨᲧ")), bstack11l111lll11_opy_)
    try:
        if not os.path.exists(bstack1l111l1l_opy_):
            os.makedirs(bstack1l111l1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠧࡿࠩᲨ")), bstack11l111lll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l11l11_opy_ (u"ࠨࡹࠪᲩ")):
                pass
            with open(file_path, bstack1l11l11_opy_ (u"ࠤࡺ࠯ࠧᲪ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11ll1111_opy_.format(str(e)))
def bstack111lll11l1l_opy_(file_name, key, value, logger):
    file_path = bstack11l111llll1_opy_(bstack1l11l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᲫ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11l11ll_opy_ = json.load(open(file_path, bstack1l11l11_opy_ (u"ࠫࡷࡨࠧᲬ")))
        else:
            bstack1l11l11ll_opy_ = {}
        bstack1l11l11ll_opy_[key] = value
        with open(file_path, bstack1l11l11_opy_ (u"ࠧࡽࠫࠣᲭ")) as outfile:
            json.dump(bstack1l11l11ll_opy_, outfile)
def bstack1l1111111_opy_(file_name, logger):
    file_path = bstack11l111llll1_opy_(bstack1l11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ხ"), file_name, logger)
    bstack1l11l11ll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l11l11_opy_ (u"ࠧࡳࠩᲯ")) as bstack1l1ll1l1_opy_:
            bstack1l11l11ll_opy_ = json.load(bstack1l1ll1l1_opy_)
    return bstack1l11l11ll_opy_
def bstack11l11ll1l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬᲰ") + file_path + bstack1l11l11_opy_ (u"ࠩࠣࠫᲱ") + str(e))
def bstack11l1l111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l11l11_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧᲲ")
def bstack1l11llllll_opy_(config):
    if bstack1l11l11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᲳ") in config:
        del (config[bstack1l11l11_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᲴ")])
        return False
    if bstack11l1l111_opy_() < version.parse(bstack1l11l11_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬᲵ")):
        return False
    if bstack11l1l111_opy_() >= version.parse(bstack1l11l11_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭Ჶ")):
        return True
    if bstack1l11l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᲷ") in config and config[bstack1l11l11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᲸ")] is False:
        return False
    else:
        return True
def bstack11ll11l1l1_opy_(args_list, bstack11l11111111_opy_):
    index = -1
    for value in bstack11l11111111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1l1l11l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1l1l11l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111ll11l11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111ll11l11_opy_ = bstack111ll11l11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᲹ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᲺ"), exception=exception)
    def bstack111111ll1l_opy_(self):
        if self.result != bstack1l11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᲻"):
            return None
        if isinstance(self.exception_type, str) and bstack1l11l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ᲼") in self.exception_type:
            return bstack1l11l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᲽ")
        return bstack1l11l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᲾ")
    def bstack11l111l1l11_opy_(self):
        if self.result != bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᲿ"):
            return None
        if self.bstack111ll11l11_opy_:
            return self.bstack111ll11l11_opy_
        return bstack111lll11l11_opy_(self.exception)
def bstack111lll11l11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l111l1l1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l111ll111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11lll111_opy_(config, logger):
    try:
        import playwright
        bstack111llll111l_opy_ = playwright.__file__
        bstack11l11l111l1_opy_ = os.path.split(bstack111llll111l_opy_)
        bstack11l1l111111_opy_ = bstack11l11l111l1_opy_[0] + bstack1l11l11_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭᳀")
        os.environ[bstack1l11l11_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧ᳁")] = bstack1l1111l1_opy_(config)
        with open(bstack11l1l111111_opy_, bstack1l11l11_opy_ (u"ࠬࡸࠧ᳂")) as f:
            bstack111l1l1ll_opy_ = f.read()
            bstack11l11l1lll1_opy_ = bstack1l11l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ᳃")
            bstack111lll1ll11_opy_ = bstack111l1l1ll_opy_.find(bstack11l11l1lll1_opy_)
            if bstack111lll1ll11_opy_ == -1:
              process = subprocess.Popen(bstack1l11l11_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦ᳄"), shell=True, cwd=bstack11l11l111l1_opy_[0])
              process.wait()
              bstack111llllllll_opy_ = bstack1l11l11_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨ᳅")
              bstack11l11l111ll_opy_ = bstack1l11l11_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨ᳆")
              bstack111lllll1l1_opy_ = bstack111l1l1ll_opy_.replace(bstack111llllllll_opy_, bstack11l11l111ll_opy_)
              with open(bstack11l1l111111_opy_, bstack1l11l11_opy_ (u"ࠪࡻࠬ᳇")) as f:
                f.write(bstack111lllll1l1_opy_)
    except Exception as e:
        logger.error(bstack11l1l11111_opy_.format(str(e)))
def bstack11l1l1111l_opy_():
  try:
    bstack111lll1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ᳈"))
    bstack11l11ll111l_opy_ = []
    if os.path.exists(bstack111lll1llll_opy_):
      with open(bstack111lll1llll_opy_) as f:
        bstack11l11ll111l_opy_ = json.load(f)
      os.remove(bstack111lll1llll_opy_)
    return bstack11l11ll111l_opy_
  except:
    pass
  return []
def bstack1l1l1ll11l_opy_(bstack1l111lll_opy_):
  try:
    bstack11l11ll111l_opy_ = []
    bstack111lll1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬ᳉"))
    if os.path.exists(bstack111lll1llll_opy_):
      with open(bstack111lll1llll_opy_) as f:
        bstack11l11ll111l_opy_ = json.load(f)
    bstack11l11ll111l_opy_.append(bstack1l111lll_opy_)
    with open(bstack111lll1llll_opy_, bstack1l11l11_opy_ (u"࠭ࡷࠨ᳊")) as f:
        json.dump(bstack11l11ll111l_opy_, f)
  except:
    pass
def bstack1l1l1l111_opy_(logger, bstack11l1111l1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l11l11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ᳋"), bstack1l11l11_opy_ (u"ࠨࠩ᳌"))
    if test_name == bstack1l11l11_opy_ (u"ࠩࠪ᳍"):
        test_name = threading.current_thread().__dict__.get(bstack1l11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩ᳎"), bstack1l11l11_opy_ (u"ࠫࠬ᳏"))
    bstack111ll1ll11l_opy_ = bstack1l11l11_opy_ (u"ࠬ࠲ࠠࠨ᳐").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1111l1ll_opy_:
        bstack11lll1l11l_opy_ = os.environ.get(bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᳑"), bstack1l11l11_opy_ (u"ࠧ࠱ࠩ᳒"))
        bstack1l1l1l11l1_opy_ = {bstack1l11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭᳓"): test_name, bstack1l11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᳔"): bstack111ll1ll11l_opy_, bstack1l11l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹ᳕ࠩ"): bstack11lll1l11l_opy_}
        bstack11l111l11l1_opy_ = []
        bstack111ll1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰ᳖ࠪ"))
        if os.path.exists(bstack111ll1ll111_opy_):
            with open(bstack111ll1ll111_opy_) as f:
                bstack11l111l11l1_opy_ = json.load(f)
        bstack11l111l11l1_opy_.append(bstack1l1l1l11l1_opy_)
        with open(bstack111ll1ll111_opy_, bstack1l11l11_opy_ (u"ࠬࡽ᳗ࠧ")) as f:
            json.dump(bstack11l111l11l1_opy_, f)
    else:
        bstack1l1l1l11l1_opy_ = {bstack1l11l11_opy_ (u"࠭࡮ࡢ࡯ࡨ᳘ࠫ"): test_name, bstack1l11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ᳙࠭"): bstack111ll1ll11l_opy_, bstack1l11l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᳚"): str(multiprocessing.current_process().name)}
        if bstack1l11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭᳛") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l1l11l1_opy_)
  except Exception as e:
      logger.warn(bstack1l11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃ᳜ࠢ").format(e))
def bstack1l111111l1_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11l11_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹ᳝ࠧ"))
    try:
      bstack11l11ll11l1_opy_ = []
      bstack1l1l1l11l1_opy_ = {bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧ᳞ࠪ"): test_name, bstack1l11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶ᳟ࠬ"): error_message, bstack1l11l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭᳠"): index}
      bstack111ll1ll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ᳡"))
      if os.path.exists(bstack111ll1ll1l1_opy_):
          with open(bstack111ll1ll1l1_opy_) as f:
              bstack11l11ll11l1_opy_ = json.load(f)
      bstack11l11ll11l1_opy_.append(bstack1l1l1l11l1_opy_)
      with open(bstack111ll1ll1l1_opy_, bstack1l11l11_opy_ (u"ࠩࡺ᳢ࠫ")) as f:
          json.dump(bstack11l11ll11l1_opy_, f)
    except Exception as e:
      logger.warn(bstack1l11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ᳣").format(e))
    return
  bstack11l11ll11l1_opy_ = []
  bstack1l1l1l11l1_opy_ = {bstack1l11l11_opy_ (u"ࠫࡳࡧ࡭ࡦ᳤ࠩ"): test_name, bstack1l11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵ᳥ࠫ"): error_message, bstack1l11l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ᳦ࠬ"): index}
  bstack111ll1ll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ᳧"))
  lock_file = bstack111ll1ll1l1_opy_ + bstack1l11l11_opy_ (u"ࠨ࠰࡯ࡳࡨࡱ᳨ࠧ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111ll1ll1l1_opy_):
          with open(bstack111ll1ll1l1_opy_, bstack1l11l11_opy_ (u"ࠩࡵࠫᳩ")) as f:
              content = f.read().strip()
              if content:
                  bstack11l11ll11l1_opy_ = json.load(open(bstack111ll1ll1l1_opy_))
      bstack11l11ll11l1_opy_.append(bstack1l1l1l11l1_opy_)
      with open(bstack111ll1ll1l1_opy_, bstack1l11l11_opy_ (u"ࠪࡻࠬᳪ")) as f:
          json.dump(bstack11l11ll11l1_opy_, f)
  except Exception as e:
    logger.warn(bstack1l11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦᳫ").format(e))
def bstack111111l11_opy_(bstack1llllll11_opy_, name, logger):
  try:
    bstack1l1l1l11l1_opy_ = {bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᳬ"): name, bstack1l11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶ᳭ࠬ"): bstack1llllll11_opy_, bstack1l11l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᳮ"): str(threading.current_thread()._name)}
    return bstack1l1l1l11l1_opy_
  except Exception as e:
    logger.warn(bstack1l11l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᳯ").format(e))
  return
def bstack11l1l11111l_opy_():
    return platform.system() == bstack1l11l11_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪᳰ")
def bstack11l11l1ll_opy_(bstack111lll111ll_opy_, config, logger):
    bstack111llll1ll1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111lll111ll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᳱ").format(e))
    return bstack111llll1ll1_opy_
def bstack111lll1111l_opy_(bstack111lll11ll1_opy_, bstack11l11ll1111_opy_):
    bstack11l11llll11_opy_ = version.parse(bstack111lll11ll1_opy_)
    bstack11l11l1111l_opy_ = version.parse(bstack11l11ll1111_opy_)
    if bstack11l11llll11_opy_ > bstack11l11l1111l_opy_:
        return 1
    elif bstack11l11llll11_opy_ < bstack11l11l1111l_opy_:
        return -1
    else:
        return 0
def bstack1111ll1111_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1111l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11llllll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll111ll_opy_(options, framework, config, bstack1lll11l111_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l11l11_opy_ (u"ࠫ࡬࡫ࡴࠨᳲ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1lll1l_opy_ = caps.get(bstack1l11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᳳ"))
    bstack111ll1ll1ll_opy_ = True
    bstack1ll1l1l11l_opy_ = os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᳴")]
    bstack1ll1111l1ll_opy_ = config.get(bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᳵ"), False)
    if bstack1ll1111l1ll_opy_:
        bstack1llll1111l1_opy_ = config.get(bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᳶ"), {})
        bstack1llll1111l1_opy_[bstack1l11l11_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ᳷")] = os.getenv(bstack1l11l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᳸"))
        bstack11ll1ll1ll1_opy_ = json.loads(os.getenv(bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᳹"), bstack1l11l11_opy_ (u"ࠬࢁࡽࠨᳺ"))).get(bstack1l11l11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᳻"))
    if bstack11l11lll1ll_opy_(caps.get(bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭᳼"))) or bstack11l11lll1ll_opy_(caps.get(bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨ᳽"))):
        bstack111ll1ll1ll_opy_ = False
    if bstack1l11llllll_opy_({bstack1l11l11_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ᳾"): bstack111ll1ll1ll_opy_}):
        bstack1l1lll1l_opy_ = bstack1l1lll1l_opy_ or {}
        bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᳿")] = bstack11l11llllll_opy_(framework)
        bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᴀ")] = bstack1l1l1lll111_opy_()
        bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᴁ")] = bstack1ll1l1l11l_opy_
        bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᴂ")] = bstack1lll11l111_opy_
        if bstack1ll1111l1ll_opy_:
            bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴃ")] = bstack1ll1111l1ll_opy_
            bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᴄ")] = bstack1llll1111l1_opy_
            bstack1l1lll1l_opy_[bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴅ")][bstack1l11l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᴆ")] = bstack11ll1ll1ll1_opy_
        if getattr(options, bstack1l11l11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᴇ"), None):
            options.set_capability(bstack1l11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᴈ"), bstack1l1lll1l_opy_)
        else:
            options[bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᴉ")] = bstack1l1lll1l_opy_
    else:
        if getattr(options, bstack1l11l11_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᴊ"), None):
            options.set_capability(bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴋ"), bstack11l11llllll_opy_(framework))
            options.set_capability(bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴌ"), bstack1l1l1lll111_opy_())
            options.set_capability(bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴍ"), bstack1ll1l1l11l_opy_)
            options.set_capability(bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴎ"), bstack1lll11l111_opy_)
            if bstack1ll1111l1ll_opy_:
                options.set_capability(bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴏ"), bstack1ll1111l1ll_opy_)
                options.set_capability(bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᴐ"), bstack1llll1111l1_opy_)
                options.set_capability(bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᴑ"), bstack11ll1ll1ll1_opy_)
        else:
            options[bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴒ")] = bstack11l11llllll_opy_(framework)
            options[bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴓ")] = bstack1l1l1lll111_opy_()
            options[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴔ")] = bstack1ll1l1l11l_opy_
            options[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴕ")] = bstack1lll11l111_opy_
            if bstack1ll1111l1ll_opy_:
                options[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴖ")] = bstack1ll1111l1ll_opy_
                options[bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᴗ")] = bstack1llll1111l1_opy_
                options[bstack1l11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴘ")][bstack1l11l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᴙ")] = bstack11ll1ll1ll1_opy_
    return options
def bstack11l11111l1l_opy_(bstack11l11111ll1_opy_, framework):
    bstack1lll11l111_opy_ = bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᴚ"))
    if bstack11l11111ll1_opy_ and len(bstack11l11111ll1_opy_.split(bstack1l11l11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᴛ"))) > 1:
        ws_url = bstack11l11111ll1_opy_.split(bstack1l11l11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᴜ"))[0]
        if bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᴝ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111lllll11l_opy_ = json.loads(urllib.parse.unquote(bstack11l11111ll1_opy_.split(bstack1l11l11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᴞ"))[1]))
            bstack111lllll11l_opy_ = bstack111lllll11l_opy_ or {}
            bstack1ll1l1l11l_opy_ = os.environ[bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᴟ")]
            bstack111lllll11l_opy_[bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴠ")] = str(framework) + str(__version__)
            bstack111lllll11l_opy_[bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴡ")] = bstack1l1l1lll111_opy_()
            bstack111lllll11l_opy_[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴢ")] = bstack1ll1l1l11l_opy_
            bstack111lllll11l_opy_[bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴣ")] = bstack1lll11l111_opy_
            bstack11l11111ll1_opy_ = bstack11l11111ll1_opy_.split(bstack1l11l11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᴤ"))[0] + bstack1l11l11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᴥ") + urllib.parse.quote(json.dumps(bstack111lllll11l_opy_))
    return bstack11l11111ll1_opy_
def bstack1l1ll111l1_opy_():
    global bstack111lll111_opy_
    from playwright._impl._browser_type import BrowserType
    bstack111lll111_opy_ = BrowserType.connect
    return bstack111lll111_opy_
def bstack1ll1llll_opy_(framework_name):
    global bstack1ll1l111ll_opy_
    bstack1ll1l111ll_opy_ = framework_name
    return framework_name
def bstack11llllll11_opy_(self, *args, **kwargs):
    global bstack111lll111_opy_
    try:
        global bstack1ll1l111ll_opy_
        if bstack1l11l11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᴦ") in kwargs:
            kwargs[bstack1l11l11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᴧ")] = bstack11l11111l1l_opy_(
                kwargs.get(bstack1l11l11_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᴨ"), None),
                bstack1ll1l111ll_opy_
            )
    except Exception as e:
        logger.error(bstack1l11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᴩ").format(str(e)))
    return bstack111lll111_opy_(self, *args, **kwargs)
def bstack11l111l111l_opy_(bstack11l1111ll1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lll1lll1_opy_(bstack11l1111ll1l_opy_, bstack1l11l11_opy_ (u"ࠦࠧᴪ"))
        if proxies and proxies.get(bstack1l11l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᴫ")):
            parsed_url = urlparse(proxies.get(bstack1l11l11_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᴬ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l11l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᴭ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᴮ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᴯ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᴰ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll1ll1l1_opy_(bstack11l1111ll1l_opy_):
    bstack111lll1l111_opy_ = {
        bstack11l1ll1l111_opy_[bstack11l111l1lll_opy_]: bstack11l1111ll1l_opy_[bstack11l111l1lll_opy_]
        for bstack11l111l1lll_opy_ in bstack11l1111ll1l_opy_
        if bstack11l111l1lll_opy_ in bstack11l1ll1l111_opy_
    }
    bstack111lll1l111_opy_[bstack1l11l11_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᴱ")] = bstack11l111l111l_opy_(bstack11l1111ll1l_opy_, bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᴲ")))
    bstack11l111lllll_opy_ = [element.lower() for element in bstack11l1ll11ll1_opy_]
    bstack11l11l11l1l_opy_(bstack111lll1l111_opy_, bstack11l111lllll_opy_)
    return bstack111lll1l111_opy_
def bstack11l11l11l1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l11l11_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᴳ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l11l11l1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l11l11l1l_opy_(item, keys)
def bstack1l1l1ll11l1_opy_():
    bstack11l11l11l11_opy_ = [os.environ.get(bstack1l11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤᴴ")), os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"ࠣࢀࠥᴵ")), bstack1l11l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᴶ")), os.path.join(bstack1l11l11_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᴷ"), bstack1l11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᴸ"))]
    for path in bstack11l11l11l11_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l11l11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᴹ") + str(path) + bstack1l11l11_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤᴺ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l11l11_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦᴻ") + str(path) + bstack1l11l11_opy_ (u"ࠣࠩࠥᴼ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l11l11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᴽ") + str(path) + bstack1l11l11_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣᴾ"))
            else:
                logger.debug(bstack1l11l11_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨᴿ") + str(path) + bstack1l11l11_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤᵀ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l11l11_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦᵁ") + str(path) + bstack1l11l11_opy_ (u"ࠢࠨ࠰ࠥᵂ"))
            return path
        except Exception as e:
            logger.debug(bstack1l11l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨᵃ") + str(e) + bstack1l11l11_opy_ (u"ࠤࠥᵄ"))
    logger.debug(bstack1l11l11_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢᵅ"))
    return None
@measure(event_name=EVENTS.bstack11l1l1ll1ll_opy_, stage=STAGE.bstack1lll11l1_opy_)
def bstack1llll1l1111_opy_(binary_path, bstack1ll1l1l1l1l_opy_, bs_config):
    logger.debug(bstack1l11l11_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥᵆ").format(binary_path))
    bstack11l1111l111_opy_ = bstack1l11l11_opy_ (u"ࠬ࠭ᵇ")
    bstack11l111ll1ll_opy_ = {
        bstack1l11l11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᵈ"): __version__,
        bstack1l11l11_opy_ (u"ࠢࡰࡵࠥᵉ"): platform.system(),
        bstack1l11l11_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤᵊ"): platform.machine(),
        bstack1l11l11_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᵋ"): bstack1l11l11_opy_ (u"ࠪ࠴ࠬᵌ"),
        bstack1l11l11_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥᵍ"): bstack1l11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᵎ")
    }
    bstack111ll1lllll_opy_(bstack11l111ll1ll_opy_)
    try:
        if binary_path:
            bstack11l111ll1ll_opy_[bstack1l11l11_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᵏ")] = subprocess.check_output([binary_path, bstack1l11l11_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᵐ")]).strip().decode(bstack1l11l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᵑ"))
        response = requests.request(
            bstack1l11l11_opy_ (u"ࠩࡊࡉ࡙࠭ᵒ"),
            url=bstack11lll11l1l_opy_(bstack11l1ll1lll1_opy_),
            headers=None,
            auth=(bs_config[bstack1l11l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᵓ")], bs_config[bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᵔ")]),
            json=None,
            params=bstack11l111ll1ll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l11l11_opy_ (u"ࠬࡻࡲ࡭ࠩᵕ") in data.keys() and bstack1l11l11_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᵖ") in data.keys():
            logger.debug(bstack1l11l11_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣᵗ").format(bstack11l111ll1ll_opy_[bstack1l11l11_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᵘ")]))
            if bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬᵙ") in os.environ:
                logger.debug(bstack1l11l11_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡢࡵࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑࠦࡩࡴࠢࡶࡩࡹࠨᵚ"))
                data[bstack1l11l11_opy_ (u"ࠫࡺࡸ࡬ࠨᵛ")] = os.environ[bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨᵜ")]
            bstack11l11l1l1l1_opy_ = bstack111lll1l1l1_opy_(data[bstack1l11l11_opy_ (u"࠭ࡵࡳ࡮ࠪᵝ")], bstack1ll1l1l1l1l_opy_)
            bstack11l1111l111_opy_ = os.path.join(bstack1ll1l1l1l1l_opy_, bstack11l11l1l1l1_opy_)
            os.chmod(bstack11l1111l111_opy_, 0o777) # bstack111ll1llll1_opy_ permission
            return bstack11l1111l111_opy_
    except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢᵞ").format(e))
    return binary_path
def bstack111ll1lllll_opy_(bstack11l111ll1ll_opy_):
    try:
        if bstack1l11l11_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᵟ") not in bstack11l111ll1ll_opy_[bstack1l11l11_opy_ (u"ࠩࡲࡷࠬᵠ")].lower():
            return
        if os.path.exists(bstack1l11l11_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᵡ")):
            with open(bstack1l11l11_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨᵢ"), bstack1l11l11_opy_ (u"ࠧࡸࠢᵣ")) as f:
                bstack11l11l1l11l_opy_ = {}
                for line in f:
                    if bstack1l11l11_opy_ (u"ࠨ࠽ࠣᵤ") in line:
                        key, value = line.rstrip().split(bstack1l11l11_opy_ (u"ࠢ࠾ࠤᵥ"), 1)
                        bstack11l11l1l11l_opy_[key] = value.strip(bstack1l11l11_opy_ (u"ࠨࠤ࡟ࠫࠬᵦ"))
                bstack11l111ll1ll_opy_[bstack1l11l11_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩᵧ")] = bstack11l11l1l11l_opy_.get(bstack1l11l11_opy_ (u"ࠥࡍࡉࠨᵨ"), bstack1l11l11_opy_ (u"ࠦࠧᵩ"))
        elif os.path.exists(bstack1l11l11_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡥࡱࡶࡩ࡯ࡧ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᵪ")):
            bstack11l111ll1ll_opy_[bstack1l11l11_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭ᵫ")] = bstack1l11l11_opy_ (u"ࠧࡢ࡮ࡳ࡭ࡳ࡫ࠧᵬ")
    except Exception as e:
        logger.debug(bstack1l11l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡦ࡬ࡷࡹࡸ࡯ࠡࡱࡩࠤࡱ࡯࡮ࡶࡺࠥᵭ") + e)
@measure(event_name=EVENTS.bstack11l1llll1ll_opy_, stage=STAGE.bstack1lll11l1_opy_)
def bstack111lll1l1l1_opy_(bstack11l1111llll_opy_, bstack111ll1l1l1l_opy_):
    logger.debug(bstack1l11l11_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦᵮ") + str(bstack11l1111llll_opy_) + bstack1l11l11_opy_ (u"ࠥࠦᵯ"))
    zip_path = os.path.join(bstack111ll1l1l1l_opy_, bstack1l11l11_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥᵰ"))
    bstack11l11l1l1l1_opy_ = bstack1l11l11_opy_ (u"ࠬ࠭ᵱ")
    with requests.get(bstack11l1111llll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l11l11_opy_ (u"ࠨࡷࡣࠤᵲ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l11l11_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤᵳ"))
    with zipfile.ZipFile(zip_path, bstack1l11l11_opy_ (u"ࠨࡴࠪᵴ")) as zip_ref:
        bstack111ll1l11ll_opy_ = zip_ref.namelist()
        if len(bstack111ll1l11ll_opy_) > 0:
            bstack11l11l1l1l1_opy_ = bstack111ll1l11ll_opy_[0] # bstack111ll1l1ll1_opy_ bstack11l1lll1l1l_opy_ will be bstack11l111ll1l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111ll1l1l1l_opy_)
        logger.debug(bstack1l11l11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣᵵ") + str(bstack111ll1l1l1l_opy_) + bstack1l11l11_opy_ (u"ࠥࠫࠧᵶ"))
    os.remove(zip_path)
    return bstack11l11l1l1l1_opy_
def get_cli_dir():
    bstack11l111ll111_opy_ = bstack1l1l1ll11l1_opy_()
    if bstack11l111ll111_opy_:
        bstack1ll1l1l1l1l_opy_ = os.path.join(bstack11l111ll111_opy_, bstack1l11l11_opy_ (u"ࠦࡨࡲࡩࠣᵷ"))
        if not os.path.exists(bstack1ll1l1l1l1l_opy_):
            os.makedirs(bstack1ll1l1l1l1l_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l1l1l1l_opy_
    else:
        raise FileNotFoundError(bstack1l11l11_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠣᵸ"))
def bstack1lll1111ll1_opy_(bstack1ll1l1l1l1l_opy_):
    bstack1l11l11_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤࠥᵹ")
    bstack111lll11111_opy_ = [
        os.path.join(bstack1ll1l1l1l1l_opy_, f)
        for f in os.listdir(bstack1ll1l1l1l1l_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l1l1l1l_opy_, f)) and f.startswith(bstack1l11l11_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣᵺ"))
    ]
    if len(bstack111lll11111_opy_) > 0:
        return max(bstack111lll11111_opy_, key=os.path.getmtime) # get bstack11l11lllll1_opy_ binary
    return bstack1l11l11_opy_ (u"ࠣࠤᵻ")
def bstack11ll1ll1l11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll111ll1ll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll111ll1ll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l111l11_opy_(data, keys, default=None):
    bstack1l11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡥ࡫࡫࡬ࡺࠢࡪࡩࡹࠦࡡࠡࡰࡨࡷࡹ࡫ࡤࠡࡸࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡦࡺࡡ࠻ࠢࡗ࡬ࡪࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡹࡵࠠࡵࡴࡤࡺࡪࡸࡳࡦ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠ࡬ࡧࡼࡷ࠿ࠦࡁࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢ࡮ࡩࡾࡹ࠯ࡪࡰࡧ࡭ࡨ࡫ࡳࠡࡴࡨࡴࡷ࡫ࡳࡦࡰࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡧࡩࡥࡺࡲࡴ࠻࡙ࠢࡥࡱࡻࡥࠡࡶࡲࠤࡷ࡫ࡴࡶࡴࡱࠤ࡮࡬ࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡵࡩࡹࡻࡲ࡯࠼ࠣࡘ࡭࡫ࠠࡷࡣ࡯ࡹࡪࠦࡡࡵࠢࡷ࡬ࡪࠦ࡮ࡦࡵࡷࡩࡩࠦࡰࡢࡶ࡫࠰ࠥࡵࡲࠡࡦࡨࡪࡦࡻ࡬ࡵࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᵼ")
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