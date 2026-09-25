"""
flask_security.signals
~~~~~~~~~~~~~~~~~~~~~~

Flask-Security signals module

:copyright: (c) 2012 by Matt Wright.
:copyright: (c) 2019-2026 by J. Christopher Wagner (jwag).
:license: MIT, see LICENSE for more details.
"""

import blinker
from blinker import Namespace, NamedSignal

signals: Namespace = blinker.Namespace()

user_authenticated: NamedSignal = signals.signal("user-authenticated")

user_unauthenticated: NamedSignal = signals.signal("user-unauthenticated")

user_failed_authn: NamedSignal = signals.signal("user-failed-authn")

user_registered: NamedSignal = signals.signal("user-registered")

# For cases of RETURN_GENERIC_RESPONSES with existing email/username
user_not_registered: NamedSignal = signals.signal("user-not-registered")

user_confirmed: NamedSignal = signals.signal("user-confirmed")

confirm_instructions_sent: NamedSignal = signals.signal("confirm-instructions-sent")

login_instructions_sent: NamedSignal = signals.signal("login-instructions-sent")

password_reset: NamedSignal = signals.signal("password-reset")

password_changed: NamedSignal = signals.signal("password-changed")

refresh_tracker_created: NamedSignal = signals.signal("refresh-tracker-created")

refresh_tracker_revoked: NamedSignal = signals.signal("refresh-tracker-revoked")

reset_password_instructions_sent: NamedSignal = signals.signal(
    "password-reset-instructions-sent"
)

tf_code_confirmed: NamedSignal = signals.signal("tf-code-confirmed")

tf_profile_changed: NamedSignal = signals.signal("tf-profile-changed")

tf_security_token_sent: NamedSignal = signals.signal("tf-security-token-sent")

tf_disabled: NamedSignal = signals.signal("tf-disabled")

us_security_token_sent: NamedSignal = signals.signal("us-security-token-sent")

us_profile_changed: NamedSignal = signals.signal("us-profile-changed")

wan_registered: NamedSignal = signals.signal("wan-registered")

wan_deleted: NamedSignal = signals.signal("wan-deleted")

change_email_instructions_sent: NamedSignal = signals.signal(
    "change-email-instructions-sent"
)

change_email_confirmed: NamedSignal = signals.signal("change-email")

username_recovery_email_sent: NamedSignal = signals.signal(
    "username-recovery-email-sent"
)

username_changed: NamedSignal = signals.signal("username-changed")
