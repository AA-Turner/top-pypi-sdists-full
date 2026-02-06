# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
bstack11lllll_opy_ (u"ࠧࠨࠢࠋࡒࡼࡸࡪࡹࡴࠡࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣ࡬ࡪࡲࡰࡦࡴࠣࡹࡸ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࠢࡳࡽࡹ࡫ࡳࡵࠢ࡫ࡳࡴࡱࡳ࠯ࠌࠥࠦࠧႺ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1llllll11l1_opy_(bstack1llllll111l_opy_=None, bstack1llllll1ll1_opy_=None):
    bstack11lllll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡃࡰ࡮࡯ࡩࡨࡺࠠࡱࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࡸࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠬࡹࠠࡪࡰࡷࡩࡷࡴࡡ࡭ࠢࡄࡔࡎࡹ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡥࡷ࡭ࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡲࡼࡸࡪࡹࡴࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࡣ࡭ࡷࡧ࡭ࡳ࡭ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡪࡱࡧࡧࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘࡦࡱࡥࡴࠢࡳࡶࡪࡩࡥࡥࡧࡱࡧࡪࠦ࡯ࡷࡧࡵࠤࡹ࡫ࡳࡵࡡࡳࡥࡹ࡮ࡳࠡ࡫ࡩࠤࡧࡵࡴࡩࠢࡤࡶࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࠩ࡮࡬ࡷࡹࠦ࡯ࡳࠢࡶࡸࡷ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤ࡙࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠨࡴࠫ࠲ࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠮ࡩࡦࡵࠬࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡨࡵࡳࡲ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡅࡤࡲࠥࡨࡥࠡࡣࠣࡷ࡮ࡴࡧ࡭ࡧࠣࡴࡦࡺࡨࠡࡵࡷࡶ࡮ࡴࡧࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡶࡡࡵࡪࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡉࡨࡰࡲࡶࡪࡪࠠࡪࡨࠣࡸࡪࡹࡴࡠࡣࡵ࡫ࡸࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺ࡭ࡹ࡮ࠠ࡬ࡧࡼࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡳࡶࡥࡦࡩࡸࡹࠠࠩࡤࡲࡳࡱ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡤࡱࡸࡲࡹࠦࠨࡪࡰࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡴ࡯ࡥࡧ࡬ࡨࡸࠦࠨ࡭࡫ࡶࡸ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠣࠬࡱ࡯ࡳࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡩࡷࡸ࡯ࡳࠢࠫࡷࡹࡸࠩࠋࠢࠣࠤࠥࠨࠢࠣႻ")
    try:
        bstack1llllll1111_opy_ = os.getenv(bstack11lllll_opy_ (u"ࠢࡑ࡛ࡗࡉࡘ࡚࡟ࡄࡗࡕࡖࡊࡔࡔࡠࡖࡈࡗ࡙ࠨႼ")) is not None
        if bstack1llllll111l_opy_ is not None:
            args = list(bstack1llllll111l_opy_)
        elif bstack1llllll1ll1_opy_ is not None:
            if isinstance(bstack1llllll1ll1_opy_, str):
                args = [bstack1llllll1ll1_opy_]
            elif isinstance(bstack1llllll1ll1_opy_, list):
                args = list(bstack1llllll1ll1_opy_)
            else:
                args = [bstack11lllll_opy_ (u"ࠣ࠰ࠥႽ")]
        else:
            args = [bstack11lllll_opy_ (u"ࠤ࠱ࠦႾ")]
        if bstack1llllll1111_opy_:
            return _1llllll1lll_opy_(args)
        bstack1llllll11ll_opy_ = args + [
            bstack11lllll_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦႿ"),
            bstack11lllll_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧჀ")
        ]
        class bstack1lllllll111_opy_:
            bstack11lllll_opy_ (u"ࠧࠨࠢࡑࡻࡷࡩࡸࡺࠠࡱ࡮ࡸ࡫࡮ࡴࠠࡵࡪࡤࡸࠥࡩࡡࡱࡶࡸࡶࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡸࡪࡹࡴࠡ࡫ࡷࡩࡲࡹ࠮ࠣࠤࠥჁ")
            def __init__(self):
                self.bstack1lllllll1l1_opy_ = []
                self.test_files = set()
                self.bstack1lllll1llll_opy_ = None
            def pytest_collection_finish(self, session):
                bstack11lllll_opy_ (u"ࠨࠢࠣࡊࡲࡳࡰࠦࡣࡢ࡮࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠮ࠣࠤࠥჂ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1lllllll1l1_opy_.append(nodeid)
                        if bstack11lllll_opy_ (u"ࠢ࠻࠼ࠥჃ") in nodeid:
                            file_path = nodeid.split(bstack11lllll_opy_ (u"ࠣ࠼࠽ࠦჄ"), 1)[0]
                            if file_path.endswith(bstack11lllll_opy_ (u"ࠩ࠱ࡴࡾ࠭Ⴥ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lllll1llll_opy_ = str(e)
        collector = bstack1lllllll111_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1llllll11ll_opy_, plugins=[collector])
        if collector.bstack1lllll1llll_opy_:
            return {bstack11lllll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ჆"): False, bstack11lllll_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥჇ"): 0, bstack11lllll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨ჈"): [], bstack11lllll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥ჉"): [], bstack11lllll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ჊"): bstack11lllll_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ჋").format(collector.bstack1lllll1llll_opy_)}
        return {
            bstack11lllll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥ჌"): True,
            bstack11lllll_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤჍ"): len(collector.bstack1lllllll1l1_opy_),
            bstack11lllll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧ჎"): collector.bstack1lllllll1l1_opy_,
            bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤ჏"): sorted(collector.test_files),
            bstack11lllll_opy_ (u"ࠨࡥࡹ࡫ࡷࡣࡨࡵࡤࡦࠤა"): exit_code
        }
    except Exception as e:
        return {bstack11lllll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣბ"): False, bstack11lllll_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢგ"): 0, bstack11lllll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥდ"): [], bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢე"): [], bstack11lllll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥვ"): bstack11lllll_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥზ").format(e)}
def _1llllll1lll_opy_(args):
    bstack11lllll_opy_ (u"ࠨࠢࠣࡋࡶࡳࡱࡧࡴࡦࡦࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡥࡥࠢ࡬ࡲࠥࡧࠠࡴࡧࡳࡥࡷࡧࡴࡦࠢࡓࡽࡹ࡮࡯࡯ࠢࡳࡶࡴࡩࡥࡴࡵࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠥࡴࡥࡴࡶࡨࡨࠥࡶࡹࡵࡧࡶࡸࠥ࡯ࡳࡴࡷࡨࡷ࠳ࠨࠢࠣთ")
    bstack1llllll1l11_opy_ = [sys.executable, bstack11lllll_opy_ (u"ࠢ࠮࡯ࠥი"), bstack11lllll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣკ"), bstack11lllll_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥლ"), bstack11lllll_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦმ")]
    bstack1llllll1l1l_opy_ = [a for a in args if a not in (bstack11lllll_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧნ"), bstack11lllll_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨო"), bstack11lllll_opy_ (u"ࠨ࠭ࡲࠤპ"))]
    cmd = bstack1llllll1l11_opy_ + bstack1llllll1l1l_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1lllllll1l1_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack11lllll_opy_ (u"ࠢࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦჟ") in line.lower():
                continue
            if bstack11lllll_opy_ (u"ࠣ࠼࠽ࠦრ") in line:
                bstack1lllllll1l1_opy_.append(line)
                file_path = line.split(bstack11lllll_opy_ (u"ࠤ࠽࠾ࠧს"), 1)[0]
                if file_path.endswith(bstack11lllll_opy_ (u"ࠪ࠲ࡵࡿࠧტ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack11lllll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧუ"): success,
            bstack11lllll_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦფ"): len(bstack1lllllll1l1_opy_),
            bstack11lllll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢქ"): bstack1lllllll1l1_opy_,
            bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦღ"): sorted(test_files),
            bstack11lllll_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠦყ"): proc.returncode,
            bstack11lllll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣშ"): None if success else bstack11lllll_opy_ (u"ࠥࡗࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࠭࡫ࡸࡪࡶࠣࡿࢂ࠯ࠢჩ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack11lllll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧც"): False, bstack11lllll_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦძ"): 0, bstack11lllll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢწ"): [], bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦჭ"): [], bstack11lllll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢხ"): bstack11lllll_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨჯ").format(e)}