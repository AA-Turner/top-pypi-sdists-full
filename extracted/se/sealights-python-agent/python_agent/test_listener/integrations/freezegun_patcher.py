import logging

log = logging.getLogger(__name__)


class FreezeGunPatcher(object):
    @staticmethod
    def patch():
        try:
            import freezegun as client_freezegun
            from python_agent.packages import freezegun as agent_freezegun

            client_freezegun.freeze_time = agent_freezegun.freeze_time
            log.info("freezegun found and patched")
        except ImportError:
            pass
        except Exception as e:
            log.error(
                "freezegun found and not patched. coverage may be incomplete. Error=%s"
                % str(e)
            )
