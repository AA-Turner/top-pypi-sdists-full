from timeout import sleep_timer

sleep_timer = sleep_timer('1pm', '2pm')
print(sleep_timer.during_active_time())
# start_time = f'13:{sleep_timer.random_minute_to_start_at}'
# end_time = f'14:{sleep_timer.random_minute_to_end_at}'
# current_time('Start time:', start_time)
# current_time('End time:', end_time)
# during_active_time = sleep_timer.during_active_time
# printed_active = False
# while True:
#     if during_active_time() and not printed_active:
#         current_time('Started')
#         printed_active = True
#     if not during_active_time and printed_active():
#         current_time('Stopped')
#         exit()