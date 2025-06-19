# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
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
from bstack_utils.constants import (bstack11ll1ll11ll_opy_, bstack1ll1l111l1_opy_, bstack11ll1lll_opy_, bstack1l1ll1ll_opy_,
                                    bstack11ll11lll11_opy_, bstack11ll111l11l_opy_, bstack11ll111lll1_opy_, bstack11ll11l11l1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1l1llll_opy_, bstack1l1l111ll1_opy_
from bstack_utils.proxy import bstack1llll1ll11_opy_, bstack11l1l1lll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1111ll111_opy_
from bstack_utils.bstack11l111l1_opy_ import bstack11l1l111_opy_
from browserstack_sdk._version import __version__
bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
logger = bstack1111ll111_opy_.get_logger(__name__, bstack1111ll111_opy_.bstack1lllll1l11l_opy_())
def bstack11lll111111_opy_(config):
    return config[bstack111lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᪁")]
def bstack11llll111ll_opy_(config):
    return config[bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᪂")]
def bstack1l1ll1l1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11l1l1l1_opy_(obj):
    values = []
    bstack11l111lll11_opy_ = re.compile(bstack111lll_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣ᪃"), re.I)
    for key in obj.keys():
        if bstack11l111lll11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11l1ll11_opy_(config):
    tags = []
    tags.extend(bstack11l11l1l1l1_opy_(os.environ))
    tags.extend(bstack11l11l1l1l1_opy_(config))
    return tags
def bstack11l111111l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1l1llll1_opy_(bstack11l111ll111_opy_):
    if not bstack11l111ll111_opy_:
        return bstack111lll_opy_ (u"ࠬ࠭᪄")
    return bstack111lll_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢ᪅").format(bstack11l111ll111_opy_.name, bstack11l111ll111_opy_.email)
def bstack11lll11l1ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l111lll1l_opy_ = repo.common_dir
        info = {
            bstack111lll_opy_ (u"ࠢࡴࡪࡤࠦ᪆"): repo.head.commit.hexsha,
            bstack111lll_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦ᪇"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111lll_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤ᪈"): repo.active_branch.name,
            bstack111lll_opy_ (u"ࠥࡸࡦ࡭ࠢ᪉"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢ᪊"): bstack11l1l1llll1_opy_(repo.head.commit.committer),
            bstack111lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨ᪋"): repo.head.commit.committed_datetime.isoformat(),
            bstack111lll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨ᪌"): bstack11l1l1llll1_opy_(repo.head.commit.author),
            bstack111lll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧ᪍"): repo.head.commit.authored_datetime.isoformat(),
            bstack111lll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ᪎"): repo.head.commit.message,
            bstack111lll_opy_ (u"ࠤࡵࡳࡴࡺࠢ᪏"): repo.git.rev_parse(bstack111lll_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧ᪐")),
            bstack111lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ᪑"): bstack11l111lll1l_opy_,
            bstack111lll_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ᪒"): subprocess.check_output([bstack111lll_opy_ (u"ࠨࡧࡪࡶࠥ᪓"), bstack111lll_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥ᪔"), bstack111lll_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦ᪕")]).strip().decode(
                bstack111lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᪖")),
            bstack111lll_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ᪗"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ᪘"): repo.git.rev_list(
                bstack111lll_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧ᪙").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1l11ll11_opy_ = []
        for remote in remotes:
            bstack11l111ll11l_opy_ = {
                bstack111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪚"): remote.name,
                bstack111lll_opy_ (u"ࠢࡶࡴ࡯ࠦ᪛"): remote.url,
            }
            bstack11l1l11ll11_opy_.append(bstack11l111ll11l_opy_)
        bstack11l11l1l111_opy_ = {
            bstack111lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪜"): bstack111lll_opy_ (u"ࠤࡪ࡭ࡹࠨ᪝"),
            **info,
            bstack111lll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦ᪞"): bstack11l1l11ll11_opy_
        }
        bstack11l11l1l111_opy_ = bstack11l1l111ll1_opy_(bstack11l11l1l111_opy_)
        return bstack11l11l1l111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ᪟").format(err))
        return {}
def bstack11l1l111ll1_opy_(bstack11l11l1l111_opy_):
    bstack11l1111llll_opy_ = bstack11l11l11l11_opy_(bstack11l11l1l111_opy_)
    if bstack11l1111llll_opy_ and bstack11l1111llll_opy_ > bstack11ll11lll11_opy_:
        bstack11l11ll1lll_opy_ = bstack11l1111llll_opy_ - bstack11ll11lll11_opy_
        bstack11l111ll1l1_opy_ = bstack11l1111ll11_opy_(bstack11l11l1l111_opy_[bstack111lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᪠")], bstack11l11ll1lll_opy_)
        bstack11l11l1l111_opy_[bstack111lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᪡")] = bstack11l111ll1l1_opy_
        logger.info(bstack111lll_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤ᪢")
                    .format(bstack11l11l11l11_opy_(bstack11l11l1l111_opy_) / 1024))
    return bstack11l11l1l111_opy_
def bstack11l11l11l11_opy_(bstack11l1l1111l_opy_):
    try:
        if bstack11l1l1111l_opy_:
            bstack11l1l1l111l_opy_ = json.dumps(bstack11l1l1111l_opy_)
            bstack11l11llll1l_opy_ = sys.getsizeof(bstack11l1l1l111l_opy_)
            return bstack11l11llll1l_opy_
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣ᪣").format(e))
    return -1
def bstack11l1111ll11_opy_(field, bstack11l11l111ll_opy_):
    try:
        bstack11l1l1ll111_opy_ = len(bytes(bstack11ll111l11l_opy_, bstack111lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᪤")))
        bstack11l1l11111l_opy_ = bytes(field, bstack111lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᪥"))
        bstack11l1l1l1l1l_opy_ = len(bstack11l1l11111l_opy_)
        bstack11l11l111l1_opy_ = ceil(bstack11l1l1l1l1l_opy_ - bstack11l11l111ll_opy_ - bstack11l1l1ll111_opy_)
        if bstack11l11l111l1_opy_ > 0:
            bstack11l11111l1l_opy_ = bstack11l1l11111l_opy_[:bstack11l11l111l1_opy_].decode(bstack111lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᪦"), errors=bstack111lll_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬᪧ")) + bstack11ll111l11l_opy_
            return bstack11l11111l1l_opy_
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦ᪨").format(e))
    return field
def bstack1lll111lll_opy_():
    env = os.environ
    if (bstack111lll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᪩") in env and len(env[bstack111lll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ᪪")]) > 0) or (
            bstack111lll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᪫") in env and len(env[bstack111lll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᪬")]) > 0):
        return {
            bstack111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪭"): bstack111lll_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨ᪮"),
            bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪯"): env.get(bstack111lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᪰")),
            bstack111lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪱"): env.get(bstack111lll_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦ᪲")),
            bstack111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪳"): env.get(bstack111lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᪴"))
        }
    if env.get(bstack111lll_opy_ (u"ࠧࡉࡉ᪵ࠣ")) == bstack111lll_opy_ (u"ࠨࡴࡳࡷࡨ᪶ࠦ") and bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ᪷"))):
        return {
            bstack111lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪸"): bstack111lll_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌ᪹ࠦ"),
            bstack111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪺"): env.get(bstack111lll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᪻")),
            bstack111lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪼"): env.get(bstack111lll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄ᪽ࠥ")),
            bstack111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪾"): env.get(bstack111lll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐᪿࠦ"))
        }
    if env.get(bstack111lll_opy_ (u"ࠤࡆࡍᫀࠧ")) == bstack111lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᫁") and bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦ᫂"))):
        return {
            bstack111lll_opy_ (u"ࠧࡴࡡ࡮ࡧ᫃ࠥ"): bstack111lll_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤ᫄"),
            bstack111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᫅"): env.get(bstack111lll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣ᫆")),
            bstack111lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᫇"): env.get(bstack111lll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᫈")),
            bstack111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫉"): env.get(bstack111lll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕ᫊ࠦ"))
        }
    if env.get(bstack111lll_opy_ (u"ࠨࡃࡊࠤ᫋")) == bstack111lll_opy_ (u"ࠢࡵࡴࡸࡩࠧᫌ") and env.get(bstack111lll_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᫍ")) == bstack111lll_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᫎ"):
        return {
            bstack111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫏"): bstack111lll_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨ᫐"),
            bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᫑"): None,
            bstack111lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᫒"): None,
            bstack111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫓"): None
        }
    if env.get(bstack111lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ᫔")) and env.get(bstack111lll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧ᫕")):
        return {
            bstack111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫖"): bstack111lll_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ᫗"),
            bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᫘"): env.get(bstack111lll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ᫙")),
            bstack111lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᫚"): None,
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᫛"): env.get(bstack111lll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᫜"))
        }
    if env.get(bstack111lll_opy_ (u"ࠥࡇࡎࠨ᫝")) == bstack111lll_opy_ (u"ࠦࡹࡸࡵࡦࠤ᫞") and bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦ᫟"))):
        return {
            bstack111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᫠"): bstack111lll_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ᫡"),
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᫢"): env.get(bstack111lll_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧ᫣")),
            bstack111lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫤"): None,
            bstack111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫥"): env.get(bstack111lll_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᫦"))
        }
    if env.get(bstack111lll_opy_ (u"ࠨࡃࡊࠤ᫧")) == bstack111lll_opy_ (u"ࠢࡵࡴࡸࡩࠧ᫨") and bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦ᫩"))):
        return {
            bstack111lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫪"): bstack111lll_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨ᫫"),
            bstack111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᫬"): env.get(bstack111lll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦ᫭")),
            bstack111lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᫮"): env.get(bstack111lll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᫯")),
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᫰"): env.get(bstack111lll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧ᫱"))
        }
    if env.get(bstack111lll_opy_ (u"ࠥࡇࡎࠨ᫲")) == bstack111lll_opy_ (u"ࠦࡹࡸࡵࡦࠤ᫳") and bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣ᫴"))):
        return {
            bstack111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᫵"): bstack111lll_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢ᫶"),
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᫷"): env.get(bstack111lll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨ᫸")),
            bstack111lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫹"): env.get(bstack111lll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᫺")),
            bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫻"): env.get(bstack111lll_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤ᫼"))
        }
    if env.get(bstack111lll_opy_ (u"ࠢࡄࡋࠥ᫽")) == bstack111lll_opy_ (u"ࠣࡶࡵࡹࡪࠨ᫾") and bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧ᫿"))):
        return {
            bstack111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᬀ"): bstack111lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᬁ"),
            bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᬂ"): env.get(bstack111lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᬃ")),
            bstack111lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᬄ"): env.get(bstack111lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᬅ")) or env.get(bstack111lll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᬆ")),
            bstack111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᬇ"): env.get(bstack111lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᬈ"))
        }
    if bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᬉ"))):
        return {
            bstack111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬊ"): bstack111lll_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᬋ"),
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᬌ"): bstack111lll_opy_ (u"ࠤࡾࢁࢀࢃࠢᬍ").format(env.get(bstack111lll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᬎ")), env.get(bstack111lll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᬏ"))),
            bstack111lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬐ"): env.get(bstack111lll_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᬑ")),
            bstack111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬒ"): env.get(bstack111lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᬓ"))
        }
    if bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᬔ"))):
        return {
            bstack111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᬕ"): bstack111lll_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᬖ"),
            bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᬗ"): bstack111lll_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᬘ").format(env.get(bstack111lll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ᬙ")), env.get(bstack111lll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᬚ")), env.get(bstack111lll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᬛ")), env.get(bstack111lll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᬜ"))),
            bstack111lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᬝ"): env.get(bstack111lll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᬞ")),
            bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᬟ"): env.get(bstack111lll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᬠ"))
        }
    if env.get(bstack111lll_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᬡ")) and env.get(bstack111lll_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᬢ")):
        return {
            bstack111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᬣ"): bstack111lll_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᬤ"),
            bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᬥ"): bstack111lll_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᬦ").format(env.get(bstack111lll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᬧ")), env.get(bstack111lll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ᬨ")), env.get(bstack111lll_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᬩ"))),
            bstack111lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᬪ"): env.get(bstack111lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᬫ")),
            bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᬬ"): env.get(bstack111lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᬭ"))
        }
    if any([env.get(bstack111lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᬮ")), env.get(bstack111lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᬯ")), env.get(bstack111lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᬰ"))]):
        return {
            bstack111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᬱ"): bstack111lll_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᬲ"),
            bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᬳ"): env.get(bstack111lll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐ᬴ࠧ")),
            bstack111lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᬵ"): env.get(bstack111lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᬶ")),
            bstack111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᬷ"): env.get(bstack111lll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᬸ"))
        }
    if env.get(bstack111lll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᬹ")):
        return {
            bstack111lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬺ"): bstack111lll_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᬻ"),
            bstack111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬼ"): env.get(bstack111lll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᬽ")),
            bstack111lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᬾ"): env.get(bstack111lll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᬿ")),
            bstack111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᭀ"): env.get(bstack111lll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᭁ"))
        }
    if env.get(bstack111lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᭂ")) or env.get(bstack111lll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᭃ")):
        return {
            bstack111lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭄"): bstack111lll_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᭅ"),
            bstack111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᭆ"): env.get(bstack111lll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᭇ")),
            bstack111lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᭈ"): bstack111lll_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᭉ") if env.get(bstack111lll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᭊ")) else None,
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᭋ"): env.get(bstack111lll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᭌ"))
        }
    if any([env.get(bstack111lll_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣ᭍")), env.get(bstack111lll_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧ᭎")), env.get(bstack111lll_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧ᭏"))]):
        return {
            bstack111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᭐"): bstack111lll_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨ᭑"),
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᭒"): None,
            bstack111lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᭓"): env.get(bstack111lll_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢ᭔")),
            bstack111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᭕"): env.get(bstack111lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᭖"))
        }
    if env.get(bstack111lll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤ᭗")):
        return {
            bstack111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭘"): bstack111lll_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦ᭙"),
            bstack111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭚"): env.get(bstack111lll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᭛")),
            bstack111lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᭜"): bstack111lll_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨ᭝").format(env.get(bstack111lll_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩ᭞"))) if env.get(bstack111lll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ᭟")) else None,
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᭠"): env.get(bstack111lll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᭡"))
        }
    if bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦ᭢"))):
        return {
            bstack111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭣"): bstack111lll_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨ᭤"),
            bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᭥"): env.get(bstack111lll_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦ᭦")),
            bstack111lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᭧"): env.get(bstack111lll_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧ᭨")),
            bstack111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭩"): env.get(bstack111lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᭪"))
        }
    if bstack1ll111ll1_opy_(env.get(bstack111lll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨ᭫"))):
        return {
            bstack111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᭬ࠦ"): bstack111lll_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣ᭭"),
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᭮"): bstack111lll_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥ᭯").format(env.get(bstack111lll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧ᭰")), env.get(bstack111lll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨ᭱")), env.get(bstack111lll_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬ᭲"))),
            bstack111lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᭳"): env.get(bstack111lll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤ᭴")),
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᭵"): env.get(bstack111lll_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤ᭶"))
        }
    if env.get(bstack111lll_opy_ (u"ࠥࡇࡎࠨ᭷")) == bstack111lll_opy_ (u"ࠦࡹࡸࡵࡦࠤ᭸") and env.get(bstack111lll_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧ᭹")) == bstack111lll_opy_ (u"ࠨ࠱ࠣ᭺"):
        return {
            bstack111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭻"): bstack111lll_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣ᭼"),
            bstack111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭽"): bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨ᭾").format(env.get(bstack111lll_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨ᭿"))),
            bstack111lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᮀ"): None,
            bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᮁ"): None,
        }
    if env.get(bstack111lll_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᮂ")):
        return {
            bstack111lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᮃ"): bstack111lll_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᮄ"),
            bstack111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮅ"): None,
            bstack111lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᮆ"): env.get(bstack111lll_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᮇ")),
            bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᮈ"): env.get(bstack111lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᮉ"))
        }
    if any([env.get(bstack111lll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᮊ")), env.get(bstack111lll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᮋ")), env.get(bstack111lll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᮌ")), env.get(bstack111lll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᮍ"))]):
        return {
            bstack111lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᮎ"): bstack111lll_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᮏ"),
            bstack111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮐ"): None,
            bstack111lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮑ"): env.get(bstack111lll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᮒ")) or None,
            bstack111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮓ"): env.get(bstack111lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᮔ"), 0)
        }
    if env.get(bstack111lll_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᮕ")):
        return {
            bstack111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᮖ"): bstack111lll_opy_ (u"ࠢࡈࡱࡆࡈࠧᮗ"),
            bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮘ"): None,
            bstack111lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᮙ"): env.get(bstack111lll_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᮚ")),
            bstack111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᮛ"): env.get(bstack111lll_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᮜ"))
        }
    if env.get(bstack111lll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᮝ")):
        return {
            bstack111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮞ"): bstack111lll_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᮟ"),
            bstack111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮠ"): env.get(bstack111lll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᮡ")),
            bstack111lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᮢ"): env.get(bstack111lll_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᮣ")),
            bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᮤ"): env.get(bstack111lll_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᮥ"))
        }
    return {bstack111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮦ"): None}
def get_host_info():
    return {
        bstack111lll_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᮧ"): platform.node(),
        bstack111lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᮨ"): platform.system(),
        bstack111lll_opy_ (u"ࠦࡹࡿࡰࡦࠤᮩ"): platform.machine(),
        bstack111lll_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ᮪"): platform.version(),
        bstack111lll_opy_ (u"ࠨࡡࡳࡥ࡫᮫ࠦ"): platform.architecture()[0]
    }
def bstack1l1l1l1l1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1l1ll1ll_opy_():
    if bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᮬ")):
        return bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᮭ")
    return bstack111lll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᮮ")
def bstack11l1l11lll1_opy_(driver):
    info = {
        bstack111lll_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᮯ"): driver.capabilities,
        bstack111lll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ᮰"): driver.session_id,
        bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭᮱"): driver.capabilities.get(bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ᮲"), None),
        bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᮳"): driver.capabilities.get(bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᮴"), None),
        bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫ᮵"): driver.capabilities.get(bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ᮶"), None),
        bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᮷"):driver.capabilities.get(bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᮸"), None),
    }
    if bstack11l1l1ll1ll_opy_() == bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᮹"):
        if bstack1111l1lll_opy_():
            info[bstack111lll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᮺ")] = bstack111lll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᮻ")
        elif driver.capabilities.get(bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᮼ"), {}).get(bstack111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᮽ"), False):
            info[bstack111lll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᮾ")] = bstack111lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᮿ")
        else:
            info[bstack111lll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᯀ")] = bstack111lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᯁ")
    return info
def bstack1111l1lll_opy_():
    if bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᯂ")):
        return True
    if bstack1ll111ll1_opy_(os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᯃ"), None)):
        return True
    return False
def bstack1l1ll1l111_opy_(bstack11l1l1lllll_opy_, url, data, config):
    headers = config.get(bstack111lll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᯄ"), None)
    proxies = bstack1llll1ll11_opy_(config, url)
    auth = config.get(bstack111lll_opy_ (u"ࠫࡦࡻࡴࡩࠩᯅ"), None)
    response = requests.request(
            bstack11l1l1lllll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1llll11l_opy_(bstack11l11ll1ll_opy_, size):
    bstack1l1111llll_opy_ = []
    while len(bstack11l11ll1ll_opy_) > size:
        bstack1ll11lllll_opy_ = bstack11l11ll1ll_opy_[:size]
        bstack1l1111llll_opy_.append(bstack1ll11lllll_opy_)
        bstack11l11ll1ll_opy_ = bstack11l11ll1ll_opy_[size:]
    bstack1l1111llll_opy_.append(bstack11l11ll1ll_opy_)
    return bstack1l1111llll_opy_
def bstack11l111111ll_opy_(message, bstack11l11ll1111_opy_=False):
    os.write(1, bytes(message, bstack111lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᯆ")))
    os.write(1, bytes(bstack111lll_opy_ (u"࠭࡜࡯ࠩᯇ"), bstack111lll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᯈ")))
    if bstack11l11ll1111_opy_:
        with open(bstack111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧᯉ") + os.environ[bstack111lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᯊ")] + bstack111lll_opy_ (u"ࠪ࠲ࡱࡵࡧࠨᯋ"), bstack111lll_opy_ (u"ࠫࡦ࠭ᯌ")) as f:
            f.write(message + bstack111lll_opy_ (u"ࠬࡢ࡮ࠨᯍ"))
def bstack1l1ll11l1ll_opy_():
    return os.environ[bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᯎ")].lower() == bstack111lll_opy_ (u"ࠧࡵࡴࡸࡩࠬᯏ")
def bstack1llllllll1_opy_():
    return bstack111l1lll11_opy_().replace(tzinfo=None).isoformat() + bstack111lll_opy_ (u"ࠨ࡜ࠪᯐ")
def bstack11l11l11lll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111lll_opy_ (u"ࠩ࡝ࠫᯑ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111lll_opy_ (u"ࠪ࡞ࠬᯒ")))).total_seconds() * 1000
def bstack11l111l1ll1_opy_(timestamp):
    return bstack11l1l1ll1l1_opy_(timestamp).isoformat() + bstack111lll_opy_ (u"ࠫ࡟࠭ᯓ")
def bstack11l1l1l11ll_opy_(bstack11l1l111l1l_opy_):
    date_format = bstack111lll_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᯔ")
    bstack11l1111l11l_opy_ = datetime.datetime.strptime(bstack11l1l111l1l_opy_, date_format)
    return bstack11l1111l11l_opy_.isoformat() + bstack111lll_opy_ (u"࡚࠭ࠨᯕ")
def bstack11l1l1l1l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᯖ")
    else:
        return bstack111lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᯗ")
def bstack1ll111ll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᯘ")
def bstack11l1l1lll11_opy_(val):
    return val.__str__().lower() == bstack111lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᯙ")
def bstack111l1ll1l1_opy_(bstack11l11ll11ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11ll11ll_opy_ as e:
                print(bstack111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᯚ").format(func.__name__, bstack11l11ll11ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l111lll_opy_(bstack11l1l1l1lll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l1l1lll_opy_(cls, *args, **kwargs)
            except bstack11l11ll11ll_opy_ as e:
                print(bstack111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᯛ").format(bstack11l1l1l1lll_opy_.__name__, bstack11l11ll11ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l111lll_opy_
    else:
        return decorator
def bstack1l1l111l1_opy_(bstack1111l1l1ll_opy_):
    if os.getenv(bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᯜ")) is not None:
        return bstack1ll111ll1_opy_(os.getenv(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᯝ")))
    if bstack111lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᯞ") in bstack1111l1l1ll_opy_ and bstack11l1l1lll11_opy_(bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᯟ")]):
        return False
    if bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᯠ") in bstack1111l1l1ll_opy_ and bstack11l1l1lll11_opy_(bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᯡ")]):
        return False
    return True
def bstack111ll111_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11l11l1l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᯢ"), None)
        return bstack11l11l11l1l_opy_ is None or bstack11l11l11l1l_opy_ == bstack111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᯣ")
    except Exception as e:
        return False
def bstack11llll1l1l_opy_(hub_url, CONFIG):
    if bstack11l1ll1ll_opy_() <= version.parse(bstack111lll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᯤ")):
        if hub_url:
            return bstack111lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᯥ") + hub_url + bstack111lll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ᯦")
        return bstack11ll1lll_opy_
    if hub_url:
        return bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᯧ") + hub_url + bstack111lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᯨ")
    return bstack1l1ll1ll_opy_
def bstack11l11111111_opy_():
    return isinstance(os.getenv(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᯩ")), str)
def bstack1l1l1lll1_opy_(url):
    return urlparse(url).hostname
def bstack11111l1l1_opy_(hostname):
    for bstack11l11ll11l_opy_ in bstack1ll1l111l1_opy_:
        regex = re.compile(bstack11l11ll11l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l11l1l1_opy_(bstack11l111l1111_opy_, file_name, logger):
    bstack11lllllll_opy_ = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"࠭ࡾࠨᯪ")), bstack11l111l1111_opy_)
    try:
        if not os.path.exists(bstack11lllllll_opy_):
            os.makedirs(bstack11lllllll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠧࡿࠩᯫ")), bstack11l111l1111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111lll_opy_ (u"ࠨࡹࠪᯬ")):
                pass
            with open(file_path, bstack111lll_opy_ (u"ࠤࡺ࠯ࠧᯭ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1l1llll_opy_.format(str(e)))
def bstack11l1l111111_opy_(file_name, key, value, logger):
    file_path = bstack11l1l11l1l1_opy_(bstack111lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᯮ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1l1l1_opy_ = json.load(open(file_path, bstack111lll_opy_ (u"ࠫࡷࡨࠧᯯ")))
        else:
            bstack11l1l1l1_opy_ = {}
        bstack11l1l1l1_opy_[key] = value
        with open(file_path, bstack111lll_opy_ (u"ࠧࡽࠫࠣᯰ")) as outfile:
            json.dump(bstack11l1l1l1_opy_, outfile)
def bstack111111l1l_opy_(file_name, logger):
    file_path = bstack11l1l11l1l1_opy_(bstack111lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᯱ"), file_name, logger)
    bstack11l1l1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111lll_opy_ (u"ࠧࡳ᯲ࠩ")) as bstack1l1lll1l_opy_:
            bstack11l1l1l1_opy_ = json.load(bstack1l1lll1l_opy_)
    return bstack11l1l1l1_opy_
def bstack1ll11l11l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤ᯳ࠬ") + file_path + bstack111lll_opy_ (u"ࠩࠣࠫ᯴") + str(e))
def bstack11l1ll1ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111lll_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧ᯵")
def bstack1ll1lll1ll_opy_(config):
    if bstack111lll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ᯶") in config:
        del (config[bstack111lll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ᯷")])
        return False
    if bstack11l1ll1ll_opy_() < version.parse(bstack111lll_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬ᯸")):
        return False
    if bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭᯹")):
        return True
    if bstack111lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ᯺") in config and config[bstack111lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ᯻")] is False:
        return False
    else:
        return True
def bstack1l111ll11_opy_(args_list, bstack11l11llllll_opy_):
    index = -1
    for value in bstack11l11llllll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11lll11111l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11lll11111l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111lll111l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111lll111l_opy_ = bstack111lll111l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᯼"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᯽"), exception=exception)
    def bstack11111lllll_opy_(self):
        if self.result != bstack111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᯾"):
            return None
        if isinstance(self.exception_type, str) and bstack111lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ᯿") in self.exception_type:
            return bstack111lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᰀ")
        return bstack111lll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᰁ")
    def bstack11l1l1l1111_opy_(self):
        if self.result != bstack111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᰂ"):
            return None
        if self.bstack111lll111l_opy_:
            return self.bstack111lll111l_opy_
        return bstack11l1l1l11l1_opy_(self.exception)
def bstack11l1l1l11l1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l11l1lll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll11l1l1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l1l11ll_opy_(config, logger):
    try:
        import playwright
        bstack11l11l1ll1l_opy_ = playwright.__file__
        bstack11l1l1111ll_opy_ = os.path.split(bstack11l11l1ll1l_opy_)
        bstack11l1l1111l1_opy_ = bstack11l1l1111ll_opy_[0] + bstack111lll_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭ᰃ")
        os.environ[bstack111lll_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧᰄ")] = bstack11l1l1lll_opy_(config)
        with open(bstack11l1l1111l1_opy_, bstack111lll_opy_ (u"ࠬࡸࠧᰅ")) as f:
            bstack11l1l11111_opy_ = f.read()
            bstack11l111ll1ll_opy_ = bstack111lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬᰆ")
            bstack11l111lllll_opy_ = bstack11l1l11111_opy_.find(bstack11l111ll1ll_opy_)
            if bstack11l111lllll_opy_ == -1:
              process = subprocess.Popen(bstack111lll_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦᰇ"), shell=True, cwd=bstack11l1l1111ll_opy_[0])
              process.wait()
              bstack11l11111lll_opy_ = bstack111lll_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨᰈ")
              bstack11l11ll111l_opy_ = bstack111lll_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨᰉ")
              bstack11l11ll1ll1_opy_ = bstack11l1l11111_opy_.replace(bstack11l11111lll_opy_, bstack11l11ll111l_opy_)
              with open(bstack11l1l1111l1_opy_, bstack111lll_opy_ (u"ࠪࡻࠬᰊ")) as f:
                f.write(bstack11l11ll1ll1_opy_)
    except Exception as e:
        logger.error(bstack1l1l111ll1_opy_.format(str(e)))
def bstack1lllll111l_opy_():
  try:
    bstack11l111llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᰋ"))
    bstack11l1l11llll_opy_ = []
    if os.path.exists(bstack11l111llll1_opy_):
      with open(bstack11l111llll1_opy_) as f:
        bstack11l1l11llll_opy_ = json.load(f)
      os.remove(bstack11l111llll1_opy_)
    return bstack11l1l11llll_opy_
  except:
    pass
  return []
def bstack111l11lll_opy_(bstack1llll1ll1l_opy_):
  try:
    bstack11l1l11llll_opy_ = []
    bstack11l111llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᰌ"))
    if os.path.exists(bstack11l111llll1_opy_):
      with open(bstack11l111llll1_opy_) as f:
        bstack11l1l11llll_opy_ = json.load(f)
    bstack11l1l11llll_opy_.append(bstack1llll1ll1l_opy_)
    with open(bstack11l111llll1_opy_, bstack111lll_opy_ (u"࠭ࡷࠨᰍ")) as f:
        json.dump(bstack11l1l11llll_opy_, f)
  except:
    pass
def bstack11l111ll1_opy_(logger, bstack11l1ll1111l_opy_ = False):
  try:
    test_name = os.environ.get(bstack111lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᰎ"), bstack111lll_opy_ (u"ࠨࠩᰏ"))
    if test_name == bstack111lll_opy_ (u"ࠩࠪᰐ"):
        test_name = threading.current_thread().__dict__.get(bstack111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᰑ"), bstack111lll_opy_ (u"ࠫࠬᰒ"))
    bstack11l11ll1l11_opy_ = bstack111lll_opy_ (u"ࠬ࠲ࠠࠨᰓ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1ll1111l_opy_:
        bstack1l11l11l1l_opy_ = os.environ.get(bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᰔ"), bstack111lll_opy_ (u"ࠧ࠱ࠩᰕ"))
        bstack11l1l1l1ll_opy_ = {bstack111lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᰖ"): test_name, bstack111lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᰗ"): bstack11l11ll1l11_opy_, bstack111lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᰘ"): bstack1l11l11l1l_opy_}
        bstack11l1l11l11l_opy_ = []
        bstack111llllllll_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᰙ"))
        if os.path.exists(bstack111llllllll_opy_):
            with open(bstack111llllllll_opy_) as f:
                bstack11l1l11l11l_opy_ = json.load(f)
        bstack11l1l11l11l_opy_.append(bstack11l1l1l1ll_opy_)
        with open(bstack111llllllll_opy_, bstack111lll_opy_ (u"ࠬࡽࠧᰚ")) as f:
            json.dump(bstack11l1l11l11l_opy_, f)
    else:
        bstack11l1l1l1ll_opy_ = {bstack111lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᰛ"): test_name, bstack111lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᰜ"): bstack11l11ll1l11_opy_, bstack111lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᰝ"): str(multiprocessing.current_process().name)}
        if bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ᰞ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11l1l1l1ll_opy_)
  except Exception as e:
      logger.warn(bstack111lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᰟ").format(e))
def bstack1l1111lll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l11111ll1_opy_ = []
    bstack11l1l1l1ll_opy_ = {bstack111lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᰠ"): test_name, bstack111lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᰡ"): error_message, bstack111lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᰢ"): index}
    bstack11l111l11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᰣ"))
    if os.path.exists(bstack11l111l11l1_opy_):
        with open(bstack11l111l11l1_opy_) as f:
            bstack11l11111ll1_opy_ = json.load(f)
    bstack11l11111ll1_opy_.append(bstack11l1l1l1ll_opy_)
    with open(bstack11l111l11l1_opy_, bstack111lll_opy_ (u"ࠨࡹࠪᰤ")) as f:
        json.dump(bstack11l11111ll1_opy_, f)
  except Exception as e:
    logger.warn(bstack111lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᰥ").format(e))
def bstack1111ll1ll_opy_(bstack11llll1ll_opy_, name, logger):
  try:
    bstack11l1l1l1ll_opy_ = {bstack111lll_opy_ (u"ࠪࡲࡦࡳࡥࠨᰦ"): name, bstack111lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᰧ"): bstack11llll1ll_opy_, bstack111lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᰨ"): str(threading.current_thread()._name)}
    return bstack11l1l1l1ll_opy_
  except Exception as e:
    logger.warn(bstack111lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᰩ").format(e))
  return
def bstack11l1l1lll1l_opy_():
    return platform.system() == bstack111lll_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨᰪ")
def bstack1ll1l1111_opy_(bstack11l11lll1ll_opy_, config, logger):
    bstack11l111l1l11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l11lll1ll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢᰫ").format(e))
    return bstack11l111l1l11_opy_
def bstack11l11llll11_opy_(bstack11l11ll1l1l_opy_, bstack11l1ll11111_opy_):
    bstack11l1111111l_opy_ = version.parse(bstack11l11ll1l1l_opy_)
    bstack11l11l11111_opy_ = version.parse(bstack11l1ll11111_opy_)
    if bstack11l1111111l_opy_ > bstack11l11l11111_opy_:
        return 1
    elif bstack11l1111111l_opy_ < bstack11l11l11111_opy_:
        return -1
    else:
        return 0
def bstack111l1lll11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1ll1l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11lll11l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1ll11l1lll_opy_(options, framework, config, bstack11ll1ll1ll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack111lll_opy_ (u"ࠩࡪࡩࡹ࠭ᰬ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11ll11l1l_opy_ = caps.get(bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᰭ"))
    bstack11l1l1ll11l_opy_ = True
    bstack11ll1lll11_opy_ = os.environ[bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᰮ")]
    bstack1ll11l1l11l_opy_ = config.get(bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᰯ"), False)
    if bstack1ll11l1l11l_opy_:
        bstack1lll1ll11l1_opy_ = config.get(bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᰰ"), {})
        bstack1lll1ll11l1_opy_[bstack111lll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᰱ")] = os.getenv(bstack111lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᰲ"))
        bstack11lll11l111_opy_ = json.loads(os.getenv(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᰳ"), bstack111lll_opy_ (u"ࠪࡿࢂ࠭ᰴ"))).get(bstack111lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᰵ"))
    if bstack11l1l1lll11_opy_(caps.get(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫᰶ"))) or bstack11l1l1lll11_opy_(caps.get(bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ᰷࠭"))):
        bstack11l1l1ll11l_opy_ = False
    if bstack1ll1lll1ll_opy_({bstack111lll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ᰸"): bstack11l1l1ll11l_opy_}):
        bstack11ll11l1l_opy_ = bstack11ll11l1l_opy_ or {}
        bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᰹")] = bstack11l11lll11l_opy_(framework)
        bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᰺")] = bstack1l1ll11l1ll_opy_()
        bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᰻")] = bstack11ll1lll11_opy_
        bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᰼")] = bstack11ll1ll1ll_opy_
        if bstack1ll11l1l11l_opy_:
            bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᰽")] = bstack1ll11l1l11l_opy_
            bstack11ll11l1l_opy_[bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᰾")] = bstack1lll1ll11l1_opy_
            bstack11ll11l1l_opy_[bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᰿")][bstack111lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᱀")] = bstack11lll11l111_opy_
        if getattr(options, bstack111lll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ᱁"), None):
            options.set_capability(bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᱂"), bstack11ll11l1l_opy_)
        else:
            options[bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᱃")] = bstack11ll11l1l_opy_
    else:
        if getattr(options, bstack111lll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭᱄"), None):
            options.set_capability(bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᱅"), bstack11l11lll11l_opy_(framework))
            options.set_capability(bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᱆"), bstack1l1ll11l1ll_opy_())
            options.set_capability(bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᱇"), bstack11ll1lll11_opy_)
            options.set_capability(bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᱈"), bstack11ll1ll1ll_opy_)
            if bstack1ll11l1l11l_opy_:
                options.set_capability(bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᱉"), bstack1ll11l1l11l_opy_)
                options.set_capability(bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᱊"), bstack1lll1ll11l1_opy_)
                options.set_capability(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᱋"), bstack11lll11l111_opy_)
        else:
            options[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᱌")] = bstack11l11lll11l_opy_(framework)
            options[bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᱍ")] = bstack1l1ll11l1ll_opy_()
            options[bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᱎ")] = bstack11ll1lll11_opy_
            options[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᱏ")] = bstack11ll1ll1ll_opy_
            if bstack1ll11l1l11l_opy_:
                options[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᱐")] = bstack1ll11l1l11l_opy_
                options[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᱑")] = bstack1lll1ll11l1_opy_
                options[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᱒")][bstack111lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᱓")] = bstack11lll11l111_opy_
    return options
def bstack11l1l1l1ll1_opy_(bstack11l1l111l11_opy_, framework):
    bstack11ll1ll1ll_opy_ = bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ᱔"))
    if bstack11l1l111l11_opy_ and len(bstack11l1l111l11_opy_.split(bstack111lll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᱕"))) > 1:
        ws_url = bstack11l1l111l11_opy_.split(bstack111lll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᱖"))[0]
        if bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭᱗") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1111l1l1_opy_ = json.loads(urllib.parse.unquote(bstack11l1l111l11_opy_.split(bstack111lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᱘"))[1]))
            bstack11l1111l1l1_opy_ = bstack11l1111l1l1_opy_ or {}
            bstack11ll1lll11_opy_ = os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᱙")]
            bstack11l1111l1l1_opy_[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᱚ")] = str(framework) + str(__version__)
            bstack11l1111l1l1_opy_[bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᱛ")] = bstack1l1ll11l1ll_opy_()
            bstack11l1111l1l1_opy_[bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᱜ")] = bstack11ll1lll11_opy_
            bstack11l1111l1l1_opy_[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᱝ")] = bstack11ll1ll1ll_opy_
            bstack11l1l111l11_opy_ = bstack11l1l111l11_opy_.split(bstack111lll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᱞ"))[0] + bstack111lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᱟ") + urllib.parse.quote(json.dumps(bstack11l1111l1l1_opy_))
    return bstack11l1l111l11_opy_
def bstack11l1llll1_opy_():
    global bstack1lll1lllll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1lll1lllll_opy_ = BrowserType.connect
    return bstack1lll1lllll_opy_
def bstack1lll11ll11_opy_(framework_name):
    global bstack1lllll11l_opy_
    bstack1lllll11l_opy_ = framework_name
    return framework_name
def bstack1ll1lll11_opy_(self, *args, **kwargs):
    global bstack1lll1lllll_opy_
    try:
        global bstack1lllll11l_opy_
        if bstack111lll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᱠ") in kwargs:
            kwargs[bstack111lll_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᱡ")] = bstack11l1l1l1ll1_opy_(
                kwargs.get(bstack111lll_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᱢ"), None),
                bstack1lllll11l_opy_
            )
    except Exception as e:
        logger.error(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣᱣ").format(str(e)))
    return bstack1lll1lllll_opy_(self, *args, **kwargs)
def bstack11l11l1l11l_opy_(bstack11l11lll1l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1llll1ll11_opy_(bstack11l11lll1l1_opy_, bstack111lll_opy_ (u"ࠤࠥᱤ"))
        if proxies and proxies.get(bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᱥ")):
            parsed_url = urlparse(proxies.get(bstack111lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᱦ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack111lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨᱧ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack111lll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩᱨ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack111lll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᱩ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack111lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᱪ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1lll1ll111_opy_(bstack11l11lll1l1_opy_):
    bstack11l1111l111_opy_ = {
        bstack11ll11l11l1_opy_[bstack11l11ll11l1_opy_]: bstack11l11lll1l1_opy_[bstack11l11ll11l1_opy_]
        for bstack11l11ll11l1_opy_ in bstack11l11lll1l1_opy_
        if bstack11l11ll11l1_opy_ in bstack11ll11l11l1_opy_
    }
    bstack11l1111l111_opy_[bstack111lll_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᱫ")] = bstack11l11l1l11l_opy_(bstack11l11lll1l1_opy_, bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᱬ")))
    bstack11l1111ll1l_opy_ = [element.lower() for element in bstack11ll111lll1_opy_]
    bstack11l11l11ll1_opy_(bstack11l1111l111_opy_, bstack11l1111ll1l_opy_)
    return bstack11l1111l111_opy_
def bstack11l11l11ll1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack111lll_opy_ (u"ࠦ࠯࠰ࠪࠫࠤᱭ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l11l11ll1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l11l11ll1_opy_(item, keys)
def bstack1l1lll111l1_opy_():
    bstack11l1111l1ll_opy_ = [os.environ.get(bstack111lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢᱮ")), os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠨࡾࠣᱯ")), bstack111lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᱰ")), os.path.join(bstack111lll_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭ᱱ"), bstack111lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᱲ"))]
    for path in bstack11l1111l1ll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack111lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᱳ") + str(path) + bstack111lll_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢᱴ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack111lll_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤᱵ") + str(path) + bstack111lll_opy_ (u"ࠨࠧࠣᱶ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack111lll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢᱷ") + str(path) + bstack111lll_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨᱸ"))
            else:
                logger.debug(bstack111lll_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦᱹ") + str(path) + bstack111lll_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢᱺ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack111lll_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤᱻ") + str(path) + bstack111lll_opy_ (u"ࠧ࠭࠮ࠣᱼ"))
            return path
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦᱽ") + str(e) + bstack111lll_opy_ (u"ࠢࠣ᱾"))
    logger.debug(bstack111lll_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧ᱿"))
    return None
@measure(event_name=EVENTS.bstack11ll111l1l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1lll11l11l1_opy_(binary_path, bstack1lll111l1l1_opy_, bs_config):
    logger.debug(bstack111lll_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣᲀ").format(binary_path))
    bstack11l111l111l_opy_ = bstack111lll_opy_ (u"ࠪࠫᲁ")
    bstack11l11111l11_opy_ = {
        bstack111lll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᲂ"): __version__,
        bstack111lll_opy_ (u"ࠧࡵࡳࠣᲃ"): platform.system(),
        bstack111lll_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢᲄ"): platform.machine(),
        bstack111lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᲅ"): bstack111lll_opy_ (u"ࠨ࠲ࠪᲆ"),
        bstack111lll_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣᲇ"): bstack111lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᲈ")
    }
    bstack11l1l11l1ll_opy_(bstack11l11111l11_opy_)
    try:
        if binary_path:
            bstack11l11111l11_opy_[bstack111lll_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᲉ")] = subprocess.check_output([binary_path, bstack111lll_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᲊ")]).strip().decode(bstack111lll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᲋"))
        response = requests.request(
            bstack111lll_opy_ (u"ࠧࡈࡇࡗࠫ᲌"),
            url=bstack11l1l111_opy_(bstack11ll11ll11l_opy_),
            headers=None,
            auth=(bs_config[bstack111lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᲍")], bs_config[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᲎")]),
            json=None,
            params=bstack11l11111l11_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack111lll_opy_ (u"ࠪࡹࡷࡲࠧ᲏") in data.keys() and bstack111lll_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨࡤࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᲐ") in data.keys():
            logger.debug(bstack111lll_opy_ (u"ࠧࡔࡥࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡢࡪࡰࡤࡶࡾ࠲ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨᲑ").format(bstack11l11111l11_opy_[bstack111lll_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᲒ")]))
            if bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪᲓ") in os.environ:
                logger.debug(bstack111lll_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡧࡳࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠤ࡮ࡹࠠࡴࡧࡷࠦᲔ"))
                data[bstack111lll_opy_ (u"ࠩࡸࡶࡱ࠭Ვ")] = os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭Ზ")]
            bstack11l1l11ll1l_opy_ = bstack11l111l11ll_opy_(data[bstack111lll_opy_ (u"ࠫࡺࡸ࡬ࠨᲗ")], bstack1lll111l1l1_opy_)
            bstack11l111l111l_opy_ = os.path.join(bstack1lll111l1l1_opy_, bstack11l1l11ll1l_opy_)
            os.chmod(bstack11l111l111l_opy_, 0o777) # bstack11l1ll111l1_opy_ permission
            return bstack11l111l111l_opy_
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡰࡨࡻ࡙ࠥࡄࡌࠢࡾࢁࠧᲘ").format(e))
    return binary_path
def bstack11l1l11l1ll_opy_(bstack11l11111l11_opy_):
    try:
        if bstack111lll_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᲙ") not in bstack11l11111l11_opy_[bstack111lll_opy_ (u"ࠧࡰࡵࠪᲚ")].lower():
            return
        if os.path.exists(bstack111lll_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᲛ")):
            with open(bstack111lll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᲜ"), bstack111lll_opy_ (u"ࠥࡶࠧᲝ")) as f:
                bstack11l11l1llll_opy_ = {}
                for line in f:
                    if bstack111lll_opy_ (u"ࠦࡂࠨᲞ") in line:
                        key, value = line.rstrip().split(bstack111lll_opy_ (u"ࠧࡃࠢᲟ"), 1)
                        bstack11l11l1llll_opy_[key] = value.strip(bstack111lll_opy_ (u"࠭ࠢ࡝ࠩࠪᲠ"))
                bstack11l11111l11_opy_[bstack111lll_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧᲡ")] = bstack11l11l1llll_opy_.get(bstack111lll_opy_ (u"ࠣࡋࡇࠦᲢ"), bstack111lll_opy_ (u"ࠤࠥᲣ"))
        elif os.path.exists(bstack111lll_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡣ࡯ࡴ࡮ࡴࡥ࠮ࡴࡨࡰࡪࡧࡳࡦࠤᲤ")):
            bstack11l11111l11_opy_[bstack111lll_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫᲥ")] = bstack111lll_opy_ (u"ࠬࡧ࡬ࡱ࡫ࡱࡩࠬᲦ")
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡤࡪࡵࡷࡶࡴࠦ࡯ࡧࠢ࡯࡭ࡳࡻࡸࠣᲧ") + e)
@measure(event_name=EVENTS.bstack11ll11ll1l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack11l111l11ll_opy_(bstack11l11l1111l_opy_, bstack11l1111lll1_opy_):
    logger.debug(bstack111lll_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤᲨ") + str(bstack11l11l1111l_opy_) + bstack111lll_opy_ (u"ࠣࠤᲩ"))
    zip_path = os.path.join(bstack11l1111lll1_opy_, bstack111lll_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣᲪ"))
    bstack11l1l11ll1l_opy_ = bstack111lll_opy_ (u"ࠪࠫᲫ")
    with requests.get(bstack11l11l1111l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack111lll_opy_ (u"ࠦࡼࡨࠢᲬ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack111lll_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢᲭ"))
    with zipfile.ZipFile(zip_path, bstack111lll_opy_ (u"࠭ࡲࠨᲮ")) as zip_ref:
        bstack11l111l1lll_opy_ = zip_ref.namelist()
        if len(bstack11l111l1lll_opy_) > 0:
            bstack11l1l11ll1l_opy_ = bstack11l111l1lll_opy_[0] # bstack11l11lllll1_opy_ bstack11ll111ll11_opy_ will be bstack11l11l1l1ll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1111lll1_opy_)
        logger.debug(bstack111lll_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨᲯ") + str(bstack11l1111lll1_opy_) + bstack111lll_opy_ (u"ࠣࠩࠥᲰ"))
    os.remove(zip_path)
    return bstack11l1l11ll1l_opy_
def get_cli_dir():
    bstack11l11lll111_opy_ = bstack1l1lll111l1_opy_()
    if bstack11l11lll111_opy_:
        bstack1lll111l1l1_opy_ = os.path.join(bstack11l11lll111_opy_, bstack111lll_opy_ (u"ࠤࡦࡰ࡮ࠨᲱ"))
        if not os.path.exists(bstack1lll111l1l1_opy_):
            os.makedirs(bstack1lll111l1l1_opy_, mode=0o777, exist_ok=True)
        return bstack1lll111l1l1_opy_
    else:
        raise FileNotFoundError(bstack111lll_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨᲲ"))
def bstack1lll1lll11l_opy_(bstack1lll111l1l1_opy_):
    bstack111lll_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣᲳ")
    bstack11l111l1l1l_opy_ = [
        os.path.join(bstack1lll111l1l1_opy_, f)
        for f in os.listdir(bstack1lll111l1l1_opy_)
        if os.path.isfile(os.path.join(bstack1lll111l1l1_opy_, f)) and f.startswith(bstack111lll_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨᲴ"))
    ]
    if len(bstack11l111l1l1l_opy_) > 0:
        return max(bstack11l111l1l1l_opy_, key=os.path.getmtime) # get bstack11l1l11l111_opy_ binary
    return bstack111lll_opy_ (u"ࠨࠢᲵ")
def bstack11lll111l1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1l1lllll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l1lllll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111llll1l_opy_(data, keys, default=None):
    bstack111lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡣࡩࡩࡱࡿࠠࡨࡧࡷࠤࡦࠦ࡮ࡦࡵࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡥࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡤࡸࡦࡀࠠࡕࡪࡨࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡷࡳࠥࡺࡲࡢࡸࡨࡶࡸ࡫࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡱࡥࡺࡵ࠽ࠤࡆࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠ࡬ࡧࡼࡷ࠴࡯࡮ࡥ࡫ࡦࡩࡸࠦࡲࡦࡲࡵࡩࡸ࡫࡮ࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡥࡧࡣࡸࡰࡹࡀࠠࡗࡣ࡯ࡹࡪࠦࡴࡰࠢࡵࡩࡹࡻࡲ࡯ࠢ࡬ࡪࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡳࡧࡷࡹࡷࡴ࠺ࠡࡖ࡫ࡩࠥࡼࡡ࡭ࡷࡨࠤࡦࡺࠠࡵࡪࡨࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡧࡴࡩ࠮ࠣࡳࡷࠦࡤࡦࡨࡤࡹࡱࡺࠠࡪࡨࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᲶ")
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