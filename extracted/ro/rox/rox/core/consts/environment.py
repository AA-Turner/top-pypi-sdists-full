import os, sys

from enum import Enum
try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
    from urlparse import urlsplit, urlunsplit
   
class ApiType(Enum):
    ROLLOUT = 1
    PLATFORM = 2

class Environment:
    @staticmethod
    def ROXY_INTERNAL_PATH():
        return 'device/request_configuration'
    
    def __init__(self, rox_options, api_type: ApiType):
        self.api_type = api_type 
        if rox_options and rox_options.network_configuration_options:
            self.get_config_cdn_path = rox_options.network_configuration_options.get_config_cloud_endpoint
            self.get_config_api_path = rox_options.network_configuration_options.get_config_api_endpoint
            self.send_state_cdn_path = rox_options.network_configuration_options.send_state_cloud_endpoint
            self.send_state_api_path = rox_options.network_configuration_options.send_state_api_endpoint
            self.analytics_path = rox_options.network_configuration_options.analytics_endpoint
            self.push_notifications_path = rox_options.network_configuration_options.push_notification_endpoint
        else:
            # backwards compatibility (relying on env var)
            rollout_mode = os.getenv('ROLLOUT_MODE', '')
            if rollout_mode == 'QA':
                self.get_config_cdn_path = 'https://qa-conf.rollout.io'
                self.get_config_api_path = 'https://qa-api.rollout.io/device/get_configuration'
                self.send_state_cdn_path = 'https://qa-statestore.rollout.io'
                self.send_state_api_path = 'https://qa-api.rollout.io/device/update_state_store'
                self.analytics_path = 'https://qaanalytic.rollout.io'
                self.push_notifications_path = 'https://qax-push.rollout.io/sse'

            elif rollout_mode == 'LOCAL':
                self.get_config_cdn_path = 'https://development-conf.rollout.io'
                self.get_config_api_path = 'http://127.0.0.1:8557/device/get_configuration'
                self.send_state_cdn_path = 'https://development-statestore.rollout.io'
                self.send_state_api_path = 'http://127.0.0.1:8557/device/update_state_store'
                self.analytics_path = 'http://127.0.0.1:8787'
                self.push_notifications_path = 'http://127.0.0.1:8887/sse'

            elif api_type == ApiType.PLATFORM:
                self.get_config_cdn_path = 'https://rox-conf.cloudbees.io'
                self.get_config_api_path = 'https://api.cloudbees.io/device/get_configuration'
                self.send_state_cdn_path = 'https://rox-state.cloudbees.io'
                self.send_state_api_path = 'https://api.cloudbees.io/device/update_state_store'
                self.analytics_path = 'https://fm-analytics.cloudbees.io'
                self.push_notifications_path = 'https://sdk-notification-service.cloudbees.io/sse'
                
            else:
                self.get_config_cdn_path = 'https://conf.rollout.io'
                self.get_config_api_path = 'https://x-api.rollout.io/device/get_configuration'
                self.send_state_cdn_path = 'https://statestore.rollout.io'
                self.send_state_api_path = 'https://x-api.rollout.io/device/update_state_store'
                self.analytics_path = 'https://analytic.rollout.io'
                self.push_notifications_path = 'https://push.rollout.io/sse'

            if rox_options and rox_options.self_managed_options:
                server_url = rox_options.self_managed_options.server_url
                self.get_config_api_path = '%s/device/get_configuration' % server_url
                self.send_state_api_path = '%s/device/update_state_store' % server_url
                self.analytics_path = rox_options.self_managed_options.analytics_url

    def CDN_PATH(self):
        return self.get_config_cdn_path

    def API_PATH(self):
        return self.get_config_api_path

    def CDN_STATE_PATH(self):
        return self.send_state_cdn_path

    def API_STATE_PATH(self):
        return self.send_state_api_path

    def ANALYTICS_PATH(self):
        return self.analytics_path
        

    def NOTIFICATIONS_PATH(self):
        return self.push_notifications_path

    def add_prefix_to_url(prefix, url):
        list_url = list(urlsplit(url))
        updated_url = '{}-{}'.format(prefix, list_url[1])
        list_url[1] = updated_url
        new_url = urlunsplit(list_url)
        return new_url
