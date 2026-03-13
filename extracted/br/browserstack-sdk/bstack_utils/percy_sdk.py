from percy import percy_screenshot
from bstack_utils.constants import STAGE, EVENTS
from bstack_utils import logger_utils
from bstack_utils.measure import measure
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
class PercySDK:
  @staticmethod
  def _get_command_executor_url(driver):
    command_executor = getattr(driver, 'command_executor', None)
    url = getattr(command_executor, '_url', None)
    if url:
      return url
    client_config = getattr(command_executor, 'client_config', None)
    if client_config is None:
      client_config = getattr(command_executor, '_client_config', None)
    if client_config is not None:
      remote_server_addr = getattr(client_config, 'remote_server_addr', None)
      if remote_server_addr:
        return remote_server_addr
    for attr in ['remote_server_addr', '_remote_server_addr']:
      remote_server_addr = getattr(command_executor, attr, None)
      if remote_server_addr:
        return remote_server_addr
    return None
  @classmethod
  def _ensure_legacy_command_executor_url(cls, driver):
    command_executor = getattr(driver, 'command_executor', None)
    if command_executor is None:
      error_message = 'Percy screenshot aborted: driver.command_executor is unavailable'
      logger.error(error_message)
      raise RuntimeError(error_message)
    if getattr(command_executor, '_url', None):
      return
    command_executor_url = cls._get_command_executor_url(driver)
    if command_executor_url is None:
      error_message = 'Percy screenshot aborted: unable to resolve command executor URL'
      logger.error(error_message)
      raise RuntimeError(error_message)
    try:
      setattr(command_executor, '_url', command_executor_url)
    except Exception as e:
      error_message = f'Percy screenshot aborted: failed to set command_executor._url: {str(e)}'
      logger.error(error_message)
      raise RuntimeError(error_message) from e
  @classmethod
  def screenshot(cls,driver, name, **kwargs):
    cls._ensure_legacy_command_executor_url(driver)
    percy_screenshot(driver, name, **kwargs)
