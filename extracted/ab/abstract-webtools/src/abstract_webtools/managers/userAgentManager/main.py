from .src import *
def get_ua_mgr(
         operating_system=None,
         browser=None,
         version=None,
         user_agent=None,
         randomAll=False,
         randomOperatingSystem=False,
         randomBrowser=False,
         ua_mgr=None
         ):
    return ua_mgr or UserAgentManager(
        operating_system=operating_system,
         browser=browser,
         version=version,
         user_agent=user_agent,
         randomAll=randomAll,
         randomOperatingSystem=randomOperatingSystem,
         randomBrowser=randomBrowser)
def get_user_agent_headers(
         operating_system=None,
         browser=None,
         version=None,
         user_agent=None,
         randomAll=False,
         randomOperatingSystem=False,
         randomBrowser=False,
         ua_mgr=None
         ):
    
    ua_mgr = ua_mgr or get_ua_mgr(
        operating_system=operating_system,
         browser=browser,
         version=version,
         user_agent=user_agent,
         randomAll=randomAll,
         randomOperatingSystem=randomOperatingSystem,
         randomBrowser=randomBrowser)
    return ua_mgr.get_user_agent_headers()
