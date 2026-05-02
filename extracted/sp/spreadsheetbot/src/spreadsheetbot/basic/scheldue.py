import asyncio
from telegram.ext import Application
from telegram.constants import ParseMode

from spreadsheetbot.sheets.settings import Settings
from spreadsheetbot.sheets.groups import Groups
from spreadsheetbot.sheets.users import Users
from spreadsheetbot.sheets.notifications import Notifications

from spreadsheetbot.basic.log import Log

def PerformAndScheldueNotifications(app: Application):
    app.create_task(
        _perform_notifications(app, False),
        {
            'action': 'Perform first notifications'
        }
    )
    ScheldueNotifications(app)

def ScheldueNotifications(app: Application) -> None:
    app.create_task(
        _scheldue_and_perform_notification(app),
        {
            'action': 'Perform scheldued notifications'
        }
    )

async def _scheldue_and_perform_notification(app: Application) -> None:
    await asyncio.sleep(Settings.notifications_update_time)
    ScheldueNotifications(app)
    await _perform_notifications(app, True)

async def _perform_notifications(app: Application, update_df: bool) -> None:
    Log.info("Start performing notification")
    if update_df:
        await Notifications._update_df()
        Log.info("Updated notification whole df")
    
    for idx,notification in Notifications.iterate_over_notifications_to_plan():
        superadmin_group_text = \
            Settings.notification_planned_admin_groups_template.format(notification=notification) if notification.condition in ['', None] \
            else Settings.notification_planned_admin_groups_condition_template.format(notification=notification)
        Groups.send_to_all_superadmin_groups(app, superadmin_group_text, ParseMode.MARKDOWN, notification.send_picture)
        await Notifications.set_planned(idx)
    Log.info("Planned new notifications")

    for idx,notification in Notifications.iterate_over_planned_notifications():
        Users.send_notification_to_all_users(
            app, notification.text_markdown, ParseMode.MARKDOWN, notification.send_picture, notification.state, notification.condition
        )
        if notification.state == "":
            Groups.send_to_all_normal_groups(app, notification.text_markdown, ParseMode.MARKDOWN, notification.send_picture)
        admin_group_text = \
            Settings.notification_admin_groups_template.format(notification=notification) if notification.condition in ['', None] \
            else Settings.notification_admin_groups_condition_template.format(notification=notification)
        Groups.send_to_all_admin_groups(app, admin_group_text, ParseMode.MARKDOWN, notification.send_picture)
        await Notifications.set_done(idx)
    Log.info("Done performing notification")