# stdlib
import sys

# this package
from notify_rs import TIMEOUT_DEFAULT, URGENCY_CRITICAL, Notification, ServerInformation, get_server_information

n = Notification().summary("The summary").body("The body").urgency(URGENCY_CRITICAL)

n.icon("firefox")
assert n.get_summary() == "The summary"
assert n.get_body() == "The body"
assert n.get_subtitle() is None
# No method for this; it's in hints, which isn't implemented
# assert n.get_urgency() == URGENCY_CRITICAL
assert n.get_timeout() == TIMEOUT_DEFAULT

if sys.platform == "win32":
	slf = n.show()
	assert slf is n
else:
	# this package
	from notify_rs import NotificationHandle

	handle = n.show()

	assert isinstance(handle, NotificationHandle)
	handle.id()

server_info = get_server_information()
assert isinstance(server_info, ServerInformation)

print(f"{server_info.name=}")
print(f"{server_info.vendor=}")
print(f"{server_info.version=}")
print(f"{server_info.spec_version=}")
