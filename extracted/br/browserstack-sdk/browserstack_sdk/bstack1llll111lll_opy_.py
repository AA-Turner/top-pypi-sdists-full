# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
bstack1ll111_opy_ (u"ࠧࠨࠢࠋࡒࡼࡸࡪࡹࡴࠡࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣ࡬ࡪࡲࡰࡦࡴࠣࡹࡸ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࠢࡳࡽࡹ࡫ࡳࡵࠢ࡫ࡳࡴࡱࡳ࠯ࠌࠥࠦࠧᅾ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1llll111l1l_opy_(bstack1llll11lll1_opy_=None, bstack1llll11ll1l_opy_=None):
    bstack1ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡃࡰ࡮࡯ࡩࡨࡺࠠࡱࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࡸࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠬࡹࠠࡪࡰࡷࡩࡷࡴࡡ࡭ࠢࡄࡔࡎࡹ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡥࡷ࡭ࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡲࡼࡸࡪࡹࡴࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࡣ࡭ࡷࡧ࡭ࡳ࡭ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡪࡱࡧࡧࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘࡦࡱࡥࡴࠢࡳࡶࡪࡩࡥࡥࡧࡱࡧࡪࠦ࡯ࡷࡧࡵࠤࡹ࡫ࡳࡵࡡࡳࡥࡹ࡮ࡳࠡ࡫ࡩࠤࡧࡵࡴࡩࠢࡤࡶࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࠩ࡮࡬ࡷࡹࠦ࡯ࡳࠢࡶࡸࡷ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤ࡙࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠨࡴࠫ࠲ࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠮ࡩࡦࡵࠬࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡨࡵࡳࡲ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡅࡤࡲࠥࡨࡥࠡࡣࠣࡷ࡮ࡴࡧ࡭ࡧࠣࡴࡦࡺࡨࠡࡵࡷࡶ࡮ࡴࡧࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡶࡡࡵࡪࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡉࡨࡰࡲࡶࡪࡪࠠࡪࡨࠣࡸࡪࡹࡴࡠࡣࡵ࡫ࡸࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺ࡭ࡹ࡮ࠠ࡬ࡧࡼࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡳࡶࡥࡦࡩࡸࡹࠠࠩࡤࡲࡳࡱ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡤࡱࡸࡲࡹࠦࠨࡪࡰࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡴ࡯ࡥࡧ࡬ࡨࡸࠦࠨ࡭࡫ࡶࡸ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠣࠬࡱ࡯ࡳࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡩࡷࡸ࡯ࡳࠢࠫࡷࡹࡸࠩࠋࠢࠣࠤࠥࠨࠢࠣᅿ")
    try:
        bstack1llll11llll_opy_ = os.getenv(bstack1ll111_opy_ (u"ࠢࡑ࡛ࡗࡉࡘ࡚࡟ࡄࡗࡕࡖࡊࡔࡔࡠࡖࡈࡗ࡙ࠨᆀ")) is not None
        if bstack1llll11lll1_opy_ is not None:
            args = list(bstack1llll11lll1_opy_)
        elif bstack1llll11ll1l_opy_ is not None:
            if isinstance(bstack1llll11ll1l_opy_, str):
                args = [bstack1llll11ll1l_opy_]
            elif isinstance(bstack1llll11ll1l_opy_, list):
                args = list(bstack1llll11ll1l_opy_)
            else:
                args = [bstack1ll111_opy_ (u"ࠣ࠰ࠥᆁ")]
        else:
            args = [bstack1ll111_opy_ (u"ࠤ࠱ࠦᆂ")]
        if bstack1llll11llll_opy_:
            return _1llll111ll1_opy_(args)
        bstack1llll11l1ll_opy_ = args + [
            bstack1ll111_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦᆃ"),
            bstack1ll111_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧᆄ")
        ]
        class bstack1llll11l111_opy_:
            bstack1ll111_opy_ (u"ࠧࠨࠢࡑࡻࡷࡩࡸࡺࠠࡱ࡮ࡸ࡫࡮ࡴࠠࡵࡪࡤࡸࠥࡩࡡࡱࡶࡸࡶࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡸࡪࡹࡴࠡ࡫ࡷࡩࡲࡹ࠮ࠣࠤࠥᆅ")
            def __init__(self):
                self.bstack1llll11ll11_opy_ = []
                self.test_files = set()
                self.bstack1llll11l11l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1ll111_opy_ (u"ࠨࠢࠣࡊࡲࡳࡰࠦࡣࡢ࡮࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠮ࠣࠤࠥᆆ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1llll11ll11_opy_.append(nodeid)
                        if bstack1ll111_opy_ (u"ࠢ࠻࠼ࠥᆇ") in nodeid:
                            file_path = nodeid.split(bstack1ll111_opy_ (u"ࠣ࠼࠽ࠦᆈ"), 1)[0]
                            if file_path.endswith(bstack1ll111_opy_ (u"ࠩ࠱ࡴࡾ࠭ᆉ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1llll11l11l_opy_ = str(e)
        collector = bstack1llll11l111_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1llll11l1ll_opy_, plugins=[collector])
        if collector.bstack1llll11l11l_opy_:
            return {bstack1ll111_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᆊ"): False, bstack1ll111_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥᆋ"): 0, bstack1ll111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨᆌ"): [], bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥᆍ"): [], bstack1ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᆎ"): bstack1ll111_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᆏ").format(collector.bstack1llll11l11l_opy_)}
        return {
            bstack1ll111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᆐ"): True,
            bstack1ll111_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤᆑ"): len(collector.bstack1llll11ll11_opy_),
            bstack1ll111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧᆒ"): collector.bstack1llll11ll11_opy_,
            bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤᆓ"): sorted(collector.test_files),
            bstack1ll111_opy_ (u"ࠨࡥࡹ࡫ࡷࡣࡨࡵࡤࡦࠤᆔ"): exit_code
        }
    except Exception as e:
        return {bstack1ll111_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᆕ"): False, bstack1ll111_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢᆖ"): 0, bstack1ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥᆗ"): [], bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢᆘ"): [], bstack1ll111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᆙ"): bstack1ll111_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᆚ").format(e)}
def _1llll111ll1_opy_(args):
    bstack1ll111_opy_ (u"ࠨࠢࠣࡋࡶࡳࡱࡧࡴࡦࡦࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡥࡥࠢ࡬ࡲࠥࡧࠠࡴࡧࡳࡥࡷࡧࡴࡦࠢࡓࡽࡹ࡮࡯࡯ࠢࡳࡶࡴࡩࡥࡴࡵࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠥࡴࡥࡴࡶࡨࡨࠥࡶࡹࡵࡧࡶࡸࠥ࡯ࡳࡴࡷࡨࡷ࠳ࠨࠢࠣᆛ")
    bstack1llll11l1l1_opy_ = [sys.executable, bstack1ll111_opy_ (u"ࠢ࠮࡯ࠥᆜ"), bstack1ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᆝ"), bstack1ll111_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥᆞ"), bstack1ll111_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦᆟ")]
    bstack1llll1l1111_opy_ = [a for a in args if a not in (bstack1ll111_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧᆠ"), bstack1ll111_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨᆡ"), bstack1ll111_opy_ (u"ࠨ࠭ࡲࠤᆢ"))]
    cmd = bstack1llll11l1l1_opy_ + bstack1llll1l1111_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1llll11ll11_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1ll111_opy_ (u"ࠢࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦᆣ") in line.lower():
                continue
            if bstack1ll111_opy_ (u"ࠣ࠼࠽ࠦᆤ") in line:
                bstack1llll11ll11_opy_.append(line)
                file_path = line.split(bstack1ll111_opy_ (u"ࠤ࠽࠾ࠧᆥ"), 1)[0]
                if file_path.endswith(bstack1ll111_opy_ (u"ࠪ࠲ࡵࡿࠧᆦ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1ll111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᆧ"): success,
            bstack1ll111_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦᆨ"): len(bstack1llll11ll11_opy_),
            bstack1ll111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢᆩ"): bstack1llll11ll11_opy_,
            bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦᆪ"): sorted(test_files),
            bstack1ll111_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠦᆫ"): proc.returncode,
            bstack1ll111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᆬ"): None if success else bstack1ll111_opy_ (u"ࠥࡗࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࠭࡫ࡸࡪࡶࠣࡿࢂ࠯ࠢᆭ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1ll111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᆮ"): False, bstack1ll111_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦᆯ"): 0, bstack1ll111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢᆰ"): [], bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦᆱ"): [], bstack1ll111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᆲ"): bstack1ll111_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᆳ").format(e)}