import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

FRAMEWORKS_FRONTEND_TASKS = [
    ("TS-REACT-01", "React Redux Toolkit charts dashboard with dark mode for TS-REACT-01"),
    ("TS-NG-02", "Angular Kanban Board drag and drop layout with RxJS for TS-NG-02"),
    ("JS-VUE-03", "Vue Pinia PWA offline tasks app with workbox for JS-VUE-03"),
    ("DART-FLUT-04", "Flutter 3 secure local notes editor with AES-GCM for DART-FLUT-04"),
    ("KOT-COM-05", "Kotlin Compose Multiplatform budgeting transaction dashboard for KOT-COM-05"),
    ("SWIFT-UI-06", "macOS Swift Menubar SwiftUI Combine CPU activity monitor for SWIFT-UI-06")
]
@pytest.mark.parametrize("task_id, prompt", FRAMEWORKS_FRONTEND_TASKS)
def test_frameworks_frontend_sms(task_id, prompt, tmp_path):
    """Verify complex frontend framework tasks via SMS."""
    verify_sms_with_rubric(prompt, tmp_path)
