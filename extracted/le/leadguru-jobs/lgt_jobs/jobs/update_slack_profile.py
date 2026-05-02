import logging as log
from abc import ABC

from pydantic import BaseModel

from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob
from lgt_jobs.lgt_common.slack_client.slack_client import SlackClient
from lgt_jobs.lgt_common.slack_client.web_client import SlackFilesClient
from lgt_jobs.lgt_data.enums import SourceType
from lgt_jobs.lgt_data.models.external.slack.user import SlackUser
from lgt_jobs.lgt_data.models.people.profile import Profile
from lgt_jobs.lgt_data.mongo_repository import UserMongoRepository, DedicatedBotRepository


class UpdateExternalUserProfileJobData(BaseBackgroundJobData, BaseModel):
    user_id: str


class UpdateExternalUserProfileJob(BaseBackgroundJob, ABC):

    @property
    def job_data_type(self) -> type:
        return UpdateExternalUserProfileJobData

    def exec(self, data: UpdateExternalUserProfileJobData):
        user = UserMongoRepository().get(data.user_id)
        main_profile = None
        active_users = [slack_user for slack_user in user.slack_users if not slack_user.deleted]
        if active_users and active_users[0].profile.main:
            main_profile = active_users[0].profile
        bots = DedicatedBotRepository().get_all(user_id=data.user_id, only_valid=True, include_deleted=False, source_type=SourceType.SLACK)
        for bot in bots:
            current_user: SlackUser = next(filter(lambda x: x.email == bot.user_name, user.slack_users), None)
            profile = main_profile if main_profile else current_user.profile
            if bot.source.source_type == SourceType.SLACK:
                slack = SlackClient(bot.token, bot.cookies)
                log.info(f'Updating profile in {bot.source.source_name}:{bot.source.source_id}')
                UpdateExternalUserProfileJob.__update_slack_profile(slack, profile)

    @staticmethod
    def __update_slack_profile(slack: SlackClient, profile: Profile = None):
        slack.update_profile(profile.to_dic())
        if profile.photo_url:
            photo_url = SlackFilesClient().get_file_url(profile.photo_url)
            slack.update_profile_photo(photo_url)

        team_profile = slack.get_team_profile()
        title_section_id = None
        title_field_id = None
        skype_section_id = None
        for field_data in team_profile.get('profile', {}).get('fields', []):
            if field_data.get('field_name') == 'title':
                title_section_id = field_data.get('section_id')
                title_field_id = field_data.get('id')
                break
        if title_field_id and title_section_id:
            for section_data in team_profile.get('profile', {}).get('sections', []):
                if section_data.get('section_type') == 'additional_info':
                    skype_section_id = section_data.get('id')
                    break

            auth = slack.test_auth().json()
            user_id = auth.get('user_id')
            title_element_id = title_field_id.replace(title_field_id[:2], 'Pe')
            response = slack.update_section(user_id, title_section_id, title_element_id, profile.title)
            sections = response['result']['data']['setProfileSection']['profileSections']
            elements = []
            for section in sections:
                if section['type'] == 'ADDITIONAL_INFO':
                    elements = section['profileElements']
                    break
            skype_element_id = None
            for element in elements:
                if element['label'] == 'Skype':
                    skype_element_id = element['elementId']
                    break
            slack.update_section(user_id, skype_section_id, skype_element_id, profile.skype)
