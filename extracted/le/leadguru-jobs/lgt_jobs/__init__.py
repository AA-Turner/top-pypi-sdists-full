

name = "lgt_jobs"

from .jobs.send_slack_message import SendSlackMessageJob, SendSlackMessageJobData
from .jobs.analytics import (TrackAnalyticsJob, TrackAnalyticsJobData)
from .jobs.connect_sources import (ConnectSourceJobData, ConnectSourceJob)
from .jobs.bot_stats_update import (BotStatsUpdateJob, BotStatsUpdateJobData)
from .jobs.chat_history import (LoadChatHistoryJob, LoadChatHistoryJobData)
from .jobs.update_slack_profile import (UpdateExternalUserProfileJob, UpdateExternalUserProfileJobData)
from .jobs.mass_message import SendMassMessageSlackChannelJob, SendMassMessageSlackChannelJobData
from .basejobs import (BaseBackgroundJobData, BaseBackgroundJob, InvalidJobTypeException)
from .smtp import (SendMailJob, SendMailJobData)
from .runner import (BackgroundJobRunner)
from .simple_job import (SimpleTestJob, SimpleTestJobData)
from .jobs.load_slack_people import (LoadSlackPeopleJob, LoadSlackPeopleJobData)
from .jobs.load_slack_users import LoadSlackUsersJob, LoadSlackUsersJobData
from .jobs.bots_killer import BotsKillerJob, BotsKillerData
from .jobs.send_slack_invites import SendSlackInvitesJob, SendSlackInvitesJobData

jobs_map = {
    "SimpleTestJob": SimpleTestJob,
    "BotStatsUpdateJob": BotStatsUpdateJob,
    "SendMailJob": SendMailJob,
    "TrackAnalyticsJob": TrackAnalyticsJob,
    "LoadChatHistoryJob": LoadChatHistoryJob,
    "UpdateExternalUserProfileJob": UpdateExternalUserProfileJob,
    "SendSlackMessageJob": SendSlackMessageJob,
    "SendMassMessageSlackChannelJob": SendMassMessageSlackChannelJob,
    "ConnectSourceJob": ConnectSourceJob,
    "LoadSlackPeopleJob": LoadSlackPeopleJob,
    "BotsKillerJob": BotsKillerJob,
    "LoadSlackUsersJob": LoadSlackUsersJob,
    "SendSlackInvitesJob": SendSlackInvitesJob
}
__all__ = [
    # Jobs
    SimpleTestJob,
    BotStatsUpdateJob,
    SendMailJob,
    SimpleTestJob,
    LoadChatHistoryJob,
    UpdateExternalUserProfileJob,
    TrackAnalyticsJob,
    SendSlackMessageJob,
    SendMassMessageSlackChannelJob,
    ConnectSourceJob,
    LoadSlackPeopleJob,
    LoadSlackUsersJob,
    BotsKillerJob,
    SendSlackInvitesJob,

    # module classes
    BackgroundJobRunner,
    BaseBackgroundJobData,
    BaseBackgroundJob,
    InvalidJobTypeException,
    BotStatsUpdateJobData,
    SendMailJobData,
    SimpleTestJobData,
    LoadChatHistoryJobData,
    UpdateExternalUserProfileJobData,
    TrackAnalyticsJobData,
    SendSlackMessageJobData,
    SendMassMessageSlackChannelJobData,
    ConnectSourceJobData,
    LoadSlackPeopleJobData,
    LoadSlackUsersJobData,
    BotsKillerData,
    SendSlackInvitesJobData,
    # mapping
    jobs_map
]
