from ratelimitingfilter import RateLimitingFilter
import logging


if __name__ == '__main__':
    from logging import StreamHandler

    ratelimit = RateLimitingFilter(rate=1, per=1, burst=1)
    handler = StreamHandler()
    handler.addFilter(ratelimit)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('throttled_example')
    logger.addHandler(handler)
    logger.level = logging.DEBUG
    import time

    for _ in range(20):
        logger.info("Example: %s", "text")
        time.sleep(0.2)
