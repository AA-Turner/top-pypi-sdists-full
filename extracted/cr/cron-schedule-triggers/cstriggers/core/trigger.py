from collections import OrderedDict
from datetime import datetime, timedelta

from cstriggers.core import parser, constants
from cstriggers.core.helper import dynamic_strp, constructed_kwargs, next_unit


class TriggerMixin(object):
    def __init__(self, schedule_string=None, start_date=None, end_date=None):
        self.schedule_string = schedule_string
        self.schedule_dates = []

        self.start_date, self.end_date = start_date, end_date
        self.end_reached = False
        self.date_pointer = self._init_pointer(self.start_date)

        self.end_date_pointer = self._init_pointer(
            self.end_date,
            fallback=constants.CRON_RANGE_END,
            tzinfo=self.date_pointer.tzinfo
        )

    @staticmethod
    def _init_pointer(date, fallback=None, tzinfo=None):
        """ Initializes a pointer datetime from start_date input. """
        if type(date) == datetime:
            if date.replace(tzinfo=tzinfo) > \
                    datetime.strptime(constants.CRON_RANGE_END, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=tzinfo):
                raise StopIteration(f"End-dates must be below {constants.CRON_RANGE_END}")
            return date
        elif date is None:
            if fallback is None:
                raise TypeError("date, or fallback date should be of type `datetime` or `str`.")
            return dynamic_strp(fallback, constants.DATETIME_FORMATS).replace(tzinfo=tzinfo)

        return dynamic_strp(date, constants.DATETIME_FORMATS).replace(tzinfo=tzinfo)

    def next_triggers(self, number_of_triggers=1, isoformat=False):
        """
            Iterates through a Schedule to generate a series of times according to `number_of_triggers`.
        """

        for _ in range(number_of_triggers):
            try:
                self.schedule_dates.append(self.next_trigger(isoformat=isoformat))
            except StopIteration:
                break

        _schedule_dates = self.schedule_dates
        self.schedule_dates = []

        return _schedule_dates

    def all_triggers(self, isoformat=False):
        while self.date_pointer < self.end_date_pointer:
            try:
                self.schedule_dates.append(self.next_trigger(isoformat=isoformat))
            except StopIteration:
                break

        _schedule_dates = self.schedule_dates
        self.schedule_dates = []

        return _schedule_dates

    def next_trigger(self, isoformat=None):
        raise NotImplementedError

    def last_trigger(self, isoformat=None):
        raise NotImplementedError

    def last_triggers(self, number_of_triggers=1):
        raise NotImplementedError


class Rate(TriggerMixin, object):
    def __init__(self, schedule_string=None, start_date=None, end_date=None):
        super().__init__(schedule_string=schedule_string, start_date=start_date, end_date=end_date)

    @property
    def time_delta(self):
        value, unit_name = self.schedule_string.split()
        delta_key = constants.RATE_DELTAS[unit_name]

        return timedelta(**{delta_key: int(value)})

    def next_trigger(self, isoformat=False):
        self.date_pointer += self.time_delta

        if self.date_pointer > self.end_date_pointer:
            raise StopIteration("This Rate schedule has reached its end-date.")

        return self.date_pointer.isoformat() if isoformat else self.date_pointer

    def last_trigger(self, isoformat=False):
        raise NotImplementedError

    def last_triggers(self, number_of_triggers=1):
        raise NotImplementedError


class QuartzCron(TriggerMixin, object):
    def __init__(self, schedule_string=None, start_date=None, end_date=None):
        super().__init__(schedule_string=schedule_string, start_date=start_date, end_date=end_date)
        self.schedule_string = self.schedule_string.upper()
        schedule_parts = self.schedule_string.split()

        # QuartzCron `year` values are optional.
        if len(schedule_parts) == 6:
            schedule_parts.append("")

        self.time_units = OrderedDict(
            constructed_kwargs(
                ["second", "minute", "hour", "day", "month", "day_of_week", "year"],
                schedule_parts
            )
        )

    @staticmethod
    def _get_parser(time_unit):
        """ Retrieves a parser for a time_unit. """
        return {
            "second": parser.CronSecondParser,
            "minute": parser.CronMinuteParser,
            "hour": parser.CronHourParser,
            "day": parser.CronDayParser,
            "day_of_week": parser.CronDayOfWeekParser,
            "month": parser.CronMonthParser,
            "year": parser.CronYearParser,
        }[time_unit]

    @staticmethod
    def _scale_ordered_unit_names(unit_names):
        """
            Swap the day_of_week and month order so that 'overflow' happens in the right order.
            :returns: unit names in ascending order of scale
        """
        unit_names[4],  unit_names[5] = unit_names[5],  unit_names[4]
        return unit_names

    def _process_time_unit_queue(self, overflow, unit_names, ignore_pointer=False, counter=None,
                                 recalculate_parent=False):
        """
            Space delimited Cron values are parsed in a queue.
            The logic of parsing of those delimited values have dependencies sometimes.
            To fulfill dependencies between delimited values,
            a value may be added back to a 'followup queue' multiple times.
        """
        units, unit_names = unit_names, []
        followup_queue = []
        counter = counter or 0
        trigger_secondary, _day_overflow_cache = False, False
        if recalculate_parent:
            units.append(next_unit(units[-1]))

        for unit_name in units:
            time_unit_value = self.time_units[unit_name]
            _day_overflow_cache = _day_overflow_cache or (unit_name == "day_of_week" and overflow)
            month_overflow = _day_overflow_cache and unit_name == "month"

            if overflow or ignore_pointer or trigger_secondary or (month_overflow and trigger_secondary):
                if overflow:
                    trigger_secondary = False
                self.date_pointer, overflow, recalculate_units, trigger_secondary = self._get_parser(unit_name)().parse(
                    self.date_pointer,
                    time_unit_value,
                    ignore_pointer=ignore_pointer,
                    trigger_secondary=trigger_secondary
                )
                followup_queue += recalculate_units or []
            elif unit_name in ["month", "year"]:
                self.date_pointer, overflow, recalculate_units, trigger_secondary = self._get_parser(unit_name)().parse(
                    self.date_pointer,
                    time_unit_value,
                    ignore_pointer=ignore_pointer,
                    trigger_secondary=True
                )
                followup_queue += recalculate_units or []

        if followup_queue:
            if counter == 0 and not ignore_pointer:
                self._process_time_unit_queue(
                    True,
                    followup_queue,
                    ignore_pointer=True,
                    counter=counter + 1
                )
            elif 12 > counter > 0:
                self._process_time_unit_queue(
                    True,
                    followup_queue,
                    counter=counter + 1,
                    recalculate_parent=True
                )

        return followup_queue

    def next_trigger(self, isoformat=False):
        """ Iterates through Cron Parsers to find the next valid trigger. """
        overflow = True
        unit_names = self._scale_ordered_unit_names(list(self.time_units.keys()))
        start_pointer = self.date_pointer

        self._process_time_unit_queue(overflow, unit_names)

        if self.end_reached or (self.date_pointer < start_pointer) or (self.end_date_pointer < self.date_pointer):
            self.end_reached = True
            raise StopIteration("This cron schedule has reached its end-date.")

        return self.date_pointer.isoformat() if isoformat else self.date_pointer

    def last_trigger(self, isoformat=False):
        raise NotImplementedError

    def last_triggers(self, number_of_triggers=1):
        raise NotImplementedError
