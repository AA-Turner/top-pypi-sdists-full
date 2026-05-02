from plyer import notification


def task_bar_toast(title: str, message: str, app_name: str, timeout: int = 2):

    notification.notify(
        title=title, message=message, app_name=app_name, timeout=timeout
    )

