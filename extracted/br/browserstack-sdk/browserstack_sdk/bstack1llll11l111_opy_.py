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
bstack1111l_opy_ (u"ࠥࠦࠧࠐࡐࡺࡶࡨࡷࡹࠦࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡪࡨࡰࡵ࡫ࡲࠡࡷࡶ࡭ࡳ࡭ࠠࡥ࡫ࡵࡩࡨࡺࠠࡱࡻࡷࡩࡸࡺࠠࡩࡱࡲ࡯ࡸ࠴ࠊࠣࠤࠥᆴ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1llll11l1ll_opy_(bstack1llll1111l1_opy_=None, bstack1llll11l11l_opy_=None):
    bstack1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡈࡵ࡬࡭ࡧࡦࡸࠥࡶࡹࡵࡧࡶࡸࠥࡺࡥࡴࡶࡶࠤࡺࡹࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠪࡷࠥ࡯࡮ࡵࡧࡵࡲࡦࡲࠠࡂࡒࡌࡷ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡣࡵ࡫ࡸࠦࠨ࡭࡫ࡶࡸ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡇࡴࡳࡰ࡭ࡧࡷࡩࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡰࡺࡶࡨࡷࡹࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢ࡬ࡲࡨࡲࡵࡥ࡫ࡱ࡫ࠥࡶࡡࡵࡪࡶࠤࡦࡴࡤࠡࡨ࡯ࡥ࡬ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖࡤ࡯ࡪࡹࠠࡱࡴࡨࡧࡪࡪࡥ࡯ࡥࡨࠤࡴࡼࡥࡳࠢࡷࡩࡸࡺ࡟ࡱࡣࡷ࡬ࡸࠦࡩࡧࠢࡥࡳࡹ࡮ࠠࡢࡴࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡰࡢࡶ࡫ࡷࠥ࠮࡬ࡪࡵࡷࠤࡴࡸࠠࡴࡶࡵ࠰ࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠩ࠻ࠢࡗࡩࡸࡺࠠࡧ࡫࡯ࡩ࠭ࡹࠩ࠰ࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠬ࡮࡫ࡳࠪࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡦࡳࡱࡰ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡃࡢࡰࠣࡦࡪࠦࡡࠡࡵ࡬ࡲ࡬ࡲࡥࠡࡲࡤࡸ࡭ࠦࡳࡵࡴ࡬ࡲ࡬ࠦ࡯ࡳࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡴࡦࡺࡨࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡎ࡭࡮ࡰࡴࡨࡨࠥ࡯ࡦࠡࡶࡨࡷࡹࡥࡡࡳࡩࡶࠤ࡮ࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡱࡥࡺࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡸࡻࡣࡤࡧࡶࡷࠥ࠮ࡢࡰࡱ࡯࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡩ࡯ࡶࡰࡷࠤ࠭࡯࡮ࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡲࡴࡪࡥࡪࡦࡶࠤ࠭ࡲࡩࡴࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠡࠪ࡯࡭ࡸࡺࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡧࡵࡶࡴࡸࠠࠩࡵࡷࡶ࠮ࠐࠠࠡࠢࠣࠦࠧࠨᆵ")
    try:
        bstack1llll111ll1_opy_ = os.getenv(bstack1111l_opy_ (u"ࠧࡖ࡙ࡕࡇࡖࡘࡤࡉࡕࡓࡔࡈࡒ࡙ࡥࡔࡆࡕࡗࠦᆶ")) is not None
        if bstack1llll1111l1_opy_ is not None:
            args = list(bstack1llll1111l1_opy_)
        elif bstack1llll11l11l_opy_ is not None:
            if isinstance(bstack1llll11l11l_opy_, str):
                args = [bstack1llll11l11l_opy_]
            elif isinstance(bstack1llll11l11l_opy_, list):
                args = list(bstack1llll11l11l_opy_)
            else:
                args = [bstack1111l_opy_ (u"ࠨ࠮ࠣᆷ")]
        else:
            args = [bstack1111l_opy_ (u"ࠢ࠯ࠤᆸ")]
        if bstack1llll111ll1_opy_:
            return _1llll11ll11_opy_(args)
        bstack1llll11l1l1_opy_ = args + [
            bstack1111l_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤᆹ"),
            bstack1111l_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥᆺ")
        ]
        class bstack1llll11111l_opy_:
            bstack1111l_opy_ (u"ࠥࠦࠧࡖࡹࡵࡧࡶࡸࠥࡶ࡬ࡶࡩ࡬ࡲࠥࡺࡨࡢࡶࠣࡧࡦࡶࡴࡶࡴࡨࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠡࡶࡨࡷࡹࠦࡩࡵࡧࡰࡷ࠳ࠨࠢࠣᆻ")
            def __init__(self):
                self.bstack1llll111lll_opy_ = []
                self.test_files = set()
                self.bstack1llll111l1l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1111l_opy_ (u"ࠦࠧࠨࡈࡰࡱ࡮ࠤࡨࡧ࡬࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡪࡵࠣࡪ࡮ࡴࡩࡴࡪࡨࡨ࠳ࠨࠢࠣᆼ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1llll111lll_opy_.append(nodeid)
                        if bstack1111l_opy_ (u"ࠧࡀ࠺ࠣᆽ") in nodeid:
                            file_path = nodeid.split(bstack1111l_opy_ (u"ࠨ࠺࠻ࠤᆾ"), 1)[0]
                            if file_path.endswith(bstack1111l_opy_ (u"ࠧ࠯ࡲࡼࠫᆿ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1llll111l1l_opy_ = str(e)
        collector = bstack1llll11111l_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1llll11l1l1_opy_, plugins=[collector])
        if collector.bstack1llll111l1l_opy_:
            return {bstack1111l_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᇀ"): False, bstack1111l_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣᇁ"): 0, bstack1111l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦᇂ"): [], bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣᇃ"): [], bstack1111l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᇄ"): bstack1111l_opy_ (u"ࠨࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᇅ").format(collector.bstack1llll111l1l_opy_)}
        return {
            bstack1111l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᇆ"): True,
            bstack1111l_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢᇇ"): len(collector.bstack1llll111lll_opy_),
            bstack1111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥᇈ"): collector.bstack1llll111lll_opy_,
            bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢᇉ"): sorted(collector.test_files),
            bstack1111l_opy_ (u"ࠦࡪࡾࡩࡵࡡࡦࡳࡩ࡫ࠢᇊ"): exit_code
        }
    except Exception as e:
        return {bstack1111l_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᇋ"): False, bstack1111l_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧᇌ"): 0, bstack1111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣᇍ"): [], bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧᇎ"): [], bstack1111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᇏ"): bstack1111l_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᇐ").format(e)}
def _1llll11ll11_opy_(args):
    bstack1111l_opy_ (u"ࠦࠧࠨࡉࡴࡱ࡯ࡥࡹ࡫ࡤࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸࡪࡪࠠࡪࡰࠣࡥࠥࡹࡥࡱࡣࡵࡥࡹ࡫ࠠࡑࡻࡷ࡬ࡴࡴࠠࡱࡴࡲࡧࡪࡹࡳࠡࡶࡲࠤࡦࡼ࡯ࡪࡦࠣࡲࡪࡹࡴࡦࡦࠣࡴࡾࡺࡥࡴࡶࠣ࡭ࡸࡹࡵࡦࡵ࠱ࠦࠧࠨᇑ")
    bstack1llll1111ll_opy_ = [sys.executable, bstack1111l_opy_ (u"ࠧ࠳࡭ࠣᇒ"), bstack1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᇓ"), bstack1111l_opy_ (u"ࠢ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠣᇔ"), bstack1111l_opy_ (u"ࠣ࠯࠰ࡵࡺ࡯ࡥࡵࠤᇕ")]
    bstack1llll111l11_opy_ = [a for a in args if a not in (bstack1111l_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥᇖ"), bstack1111l_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦᇗ"), bstack1111l_opy_ (u"ࠦ࠲ࡷࠢᇘ"))]
    cmd = bstack1llll1111ll_opy_ + bstack1llll111l11_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1llll111lll_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1111l_opy_ (u"ࠧࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠤᇙ") in line.lower():
                continue
            if bstack1111l_opy_ (u"ࠨ࠺࠻ࠤᇚ") in line:
                bstack1llll111lll_opy_.append(line)
                file_path = line.split(bstack1111l_opy_ (u"ࠢ࠻࠼ࠥᇛ"), 1)[0]
                if file_path.endswith(bstack1111l_opy_ (u"ࠨ࠰ࡳࡽࠬᇜ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1111l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᇝ"): success,
            bstack1111l_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤᇞ"): len(bstack1llll111lll_opy_),
            bstack1111l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧᇟ"): bstack1llll111lll_opy_,
            bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤᇠ"): sorted(test_files),
            bstack1111l_opy_ (u"ࠨࡥࡹ࡫ࡷࡣࡨࡵࡤࡦࠤᇡ"): proc.returncode,
            bstack1111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᇢ"): None if success else bstack1111l_opy_ (u"ࠣࡕࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࠫࡩࡽ࡯ࡴࠡࡽࢀ࠭ࠧᇣ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1111l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᇤ"): False, bstack1111l_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤᇥ"): 0, bstack1111l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧᇦ"): [], bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤᇧ"): [], bstack1111l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᇨ"): bstack1111l_opy_ (u"ࠢࡔࡷࡥࡴࡷࡵࡣࡦࡵࡶࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᇩ").format(e)}