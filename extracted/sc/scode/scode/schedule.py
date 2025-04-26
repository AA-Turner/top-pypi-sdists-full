def run_everyday_between(start_time: str, end_time: str, job, *args, **kwargs):
    """
    It runs a function between two times every day
    
    :param start_time: str - The time you want the job to start running
    :type start_time: str
    :param end_time: The time you want the job to stop running
    :type end_time: str
    :param job: the function you want to run
    """
    import datetime
    start_hour, start_minute = [int(x.strip()) for x in start_time.split(':')]
    end_hour, end_minute = [int(x.strip()) for x in end_time.split(':')]
    
    while True:
        if datetime.time(start_hour, start_minute) <= datetime.datetime.now().time() <= datetime.time(end_hour, end_minute):
            job(*args, **kwargs)
