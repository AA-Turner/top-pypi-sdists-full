# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
bstack11l1ll1_opy_ (u"ࠧࠨࠢࠋࡒࡼࡸࡪࡹࡴࠡࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣ࡬ࡪࡲࡰࡦࡴࠣࡹࡸ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࠢࡳࡽࡹ࡫ࡳࡵࠢ࡫ࡳࡴࡱࡳ࠯ࠌࠥࠦࠧႺ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1llllll11l1_opy_(bstack1llllll1l1l_opy_=None, bstack1llllll11ll_opy_=None):
    bstack11l1ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡃࡰ࡮࡯ࡩࡨࡺࠠࡱࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࡸࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠬࡹࠠࡪࡰࡷࡩࡷࡴࡡ࡭ࠢࡄࡔࡎࡹ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡥࡷ࡭ࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡲࡼࡸࡪࡹࡴࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࡣ࡭ࡷࡧ࡭ࡳ࡭ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡪࡱࡧࡧࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘࡦࡱࡥࡴࠢࡳࡶࡪࡩࡥࡥࡧࡱࡧࡪࠦ࡯ࡷࡧࡵࠤࡹ࡫ࡳࡵࡡࡳࡥࡹ࡮ࡳࠡ࡫ࡩࠤࡧࡵࡴࡩࠢࡤࡶࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࠩ࡮࡬ࡷࡹࠦ࡯ࡳࠢࡶࡸࡷ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤ࡙࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠨࡴࠫ࠲ࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠮ࡩࡦࡵࠬࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡨࡵࡳࡲ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡅࡤࡲࠥࡨࡥࠡࡣࠣࡷ࡮ࡴࡧ࡭ࡧࠣࡴࡦࡺࡨࠡࡵࡷࡶ࡮ࡴࡧࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡶࡡࡵࡪࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡉࡨࡰࡲࡶࡪࡪࠠࡪࡨࠣࡸࡪࡹࡴࡠࡣࡵ࡫ࡸࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺ࡭ࡹ࡮ࠠ࡬ࡧࡼࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡳࡶࡥࡦࡩࡸࡹࠠࠩࡤࡲࡳࡱ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡤࡱࡸࡲࡹࠦࠨࡪࡰࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡴ࡯ࡥࡧ࡬ࡨࡸࠦࠨ࡭࡫ࡶࡸ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠣࠬࡱ࡯ࡳࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡩࡷࡸ࡯ࡳࠢࠫࡷࡹࡸࠩࠋࠢࠣࠤࠥࠨࠢࠣႻ")
    try:
        bstack1llllll1ll1_opy_ = os.getenv(bstack11l1ll1_opy_ (u"ࠢࡑ࡛ࡗࡉࡘ࡚࡟ࡄࡗࡕࡖࡊࡔࡔࡠࡖࡈࡗ࡙ࠨႼ")) is not None
        if bstack1llllll1l1l_opy_ is not None:
            args = list(bstack1llllll1l1l_opy_)
        elif bstack1llllll11ll_opy_ is not None:
            if isinstance(bstack1llllll11ll_opy_, str):
                args = [bstack1llllll11ll_opy_]
            elif isinstance(bstack1llllll11ll_opy_, list):
                args = list(bstack1llllll11ll_opy_)
            else:
                args = [bstack11l1ll1_opy_ (u"ࠣ࠰ࠥႽ")]
        else:
            args = [bstack11l1ll1_opy_ (u"ࠤ࠱ࠦႾ")]
        if bstack1llllll1ll1_opy_:
            return _1llllll1111_opy_(args)
        bstack1lllll1llll_opy_ = args + [
            bstack11l1ll1_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦႿ"),
            bstack11l1ll1_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧჀ")
        ]
        class bstack1llllll111l_opy_:
            bstack11l1ll1_opy_ (u"ࠧࠨࠢࡑࡻࡷࡩࡸࡺࠠࡱ࡮ࡸ࡫࡮ࡴࠠࡵࡪࡤࡸࠥࡩࡡࡱࡶࡸࡶࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡸࡪࡹࡴࠡ࡫ࡷࡩࡲࡹ࠮ࠣࠤࠥჁ")
            def __init__(self):
                self.bstack1llllll1l11_opy_ = []
                self.test_files = set()
                self.bstack1lllll1lll1_opy_ = None
            def pytest_collection_finish(self, session):
                bstack11l1ll1_opy_ (u"ࠨࠢࠣࡊࡲࡳࡰࠦࡣࡢ࡮࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠮ࠣࠤࠥჂ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1llllll1l11_opy_.append(nodeid)
                        if bstack11l1ll1_opy_ (u"ࠢ࠻࠼ࠥჃ") in nodeid:
                            file_path = nodeid.split(bstack11l1ll1_opy_ (u"ࠣ࠼࠽ࠦჄ"), 1)[0]
                            if file_path.endswith(bstack11l1ll1_opy_ (u"ࠩ࠱ࡴࡾ࠭Ⴥ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lllll1lll1_opy_ = str(e)
        collector = bstack1llllll111l_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1lllll1llll_opy_, plugins=[collector])
        if collector.bstack1lllll1lll1_opy_:
            return {bstack11l1ll1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ჆"): False, bstack11l1ll1_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥჇ"): 0, bstack11l1ll1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨ჈"): [], bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥ჉"): [], bstack11l1ll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ჊"): bstack11l1ll1_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ჋").format(collector.bstack1lllll1lll1_opy_)}
        return {
            bstack11l1ll1_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥ჌"): True,
            bstack11l1ll1_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤჍ"): len(collector.bstack1llllll1l11_opy_),
            bstack11l1ll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧ჎"): collector.bstack1llllll1l11_opy_,
            bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤ჏"): sorted(collector.test_files),
            bstack11l1ll1_opy_ (u"ࠨࡥࡹ࡫ࡷࡣࡨࡵࡤࡦࠤა"): exit_code
        }
    except Exception as e:
        return {bstack11l1ll1_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣბ"): False, bstack11l1ll1_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢგ"): 0, bstack11l1ll1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥდ"): [], bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢე"): [], bstack11l1ll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥვ"): bstack11l1ll1_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥზ").format(e)}
def _1llllll1111_opy_(args):
    bstack11l1ll1_opy_ (u"ࠨࠢࠣࡋࡶࡳࡱࡧࡴࡦࡦࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡥࡥࠢ࡬ࡲࠥࡧࠠࡴࡧࡳࡥࡷࡧࡴࡦࠢࡓࡽࡹ࡮࡯࡯ࠢࡳࡶࡴࡩࡥࡴࡵࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠥࡴࡥࡴࡶࡨࡨࠥࡶࡹࡵࡧࡶࡸࠥ࡯ࡳࡴࡷࡨࡷ࠳ࠨࠢࠣთ")
    bstack1lllllll11l_opy_ = [sys.executable, bstack11l1ll1_opy_ (u"ࠢ࠮࡯ࠥი"), bstack11l1ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣკ"), bstack11l1ll1_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥლ"), bstack11l1ll1_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦმ")]
    bstack1llllll1lll_opy_ = [a for a in args if a not in (bstack11l1ll1_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧნ"), bstack11l1ll1_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨო"), bstack11l1ll1_opy_ (u"ࠨ࠭ࡲࠤპ"))]
    cmd = bstack1lllllll11l_opy_ + bstack1llllll1lll_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1llllll1l11_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack11l1ll1_opy_ (u"ࠢࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦჟ") in line.lower():
                continue
            if bstack11l1ll1_opy_ (u"ࠣ࠼࠽ࠦრ") in line:
                bstack1llllll1l11_opy_.append(line)
                file_path = line.split(bstack11l1ll1_opy_ (u"ࠤ࠽࠾ࠧს"), 1)[0]
                if file_path.endswith(bstack11l1ll1_opy_ (u"ࠪ࠲ࡵࡿࠧტ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack11l1ll1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧუ"): success,
            bstack11l1ll1_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦფ"): len(bstack1llllll1l11_opy_),
            bstack11l1ll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢქ"): bstack1llllll1l11_opy_,
            bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦღ"): sorted(test_files),
            bstack11l1ll1_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠦყ"): proc.returncode,
            bstack11l1ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣშ"): None if success else bstack11l1ll1_opy_ (u"ࠥࡗࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࠭࡫ࡸࡪࡶࠣࡿࢂ࠯ࠢჩ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack11l1ll1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧც"): False, bstack11l1ll1_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦძ"): 0, bstack11l1ll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢწ"): [], bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦჭ"): [], bstack11l1ll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢხ"): bstack11l1ll1_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨჯ").format(e)}