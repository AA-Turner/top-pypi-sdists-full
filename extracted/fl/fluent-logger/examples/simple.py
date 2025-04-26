from fluent import event, sender

logger = sender.FluentSender("app", nanosecond_precision=True)

logger.emit(None, {"from": "userA", "to": "userB"})
logger.emit(None, {"from": "userA", "to": "userB"})
logger.emit(None, {"from": "userA", "to": "userB"})
logger.emit(None, {"from": "userA", "to": "userB"})

sender.setup("app.event", nanosecond_precision=True)
event.Event("follow", {"from": "userA", "to": "userB"})
event.Event("follow", {"from": "userA", "to": "userB"})
event.Event("follow", {"from": "userA", "to": "userB"})
event.Event("follow", {"from": "userA", "to": "userB"})

# cur_time = int(time.time())
# logger.emit_with_time(None, cur_time, {'from': 'userA', 'to':'userB'})
