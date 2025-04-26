import calendar

from cstriggers.core import constants
from cstriggers.core.helper import constructed_kwargs, cron_dow_to_calendar, next_unit


def get_nth_weekday(date_pointer=None, nth_day=1):
    """ Finds the first occurring weekday of a month containing a given date. """
    month_calendar = calendar.monthcalendar(date_pointer.year, date_pointer.month)
    nth_day_counter = 0

    for week in month_calendar:
        for day_of_week, day_of_month in enumerate(week):
            if day_of_month == 0 or day_of_week > 4:
                continue

            nth_day_counter += 1
            if nth_day_counter < nth_day:
                continue

            return day_of_month


class CronUnitParserBase(object):
    def __init__(self, unit_name, time_unit_maximum=0):
        valid_units = ["second", "minute", "hour", "day", "month", "year"]
        if unit_name not in valid_units:
            raise ValueError(f"The `unit_name` was not one of: {valid_units}")

        self.unit_name = unit_name
        self.time_unit_maximum = time_unit_maximum
        self._zero_minimum_units = ["second", "minute", "hour"]

    def convert_value(self, value):
        return value.lower()

    def _slash_handler(self, value, current_time_value, ignore_pointer=False, recalculate_parent=False):
        """ Handles Cron Syntax parsing for `/` values. """

        start, skip = value.split("/")
        start, skip = int(start), int(skip)
        pointer = start

        value_of_time, unit_boundary_reached, recalculate_units = None, None, None
        while pointer <= self.time_unit_maximum:
            if current_time_value < pointer <= self.time_unit_maximum:
                value_of_time = pointer
                break

            if ignore_pointer and current_time_value == pointer:
                value_of_time = pointer
                break

            pointer += skip

        if pointer > self.time_unit_maximum:
            value_of_time, unit_boundary_reached, recalculate_units = (
                0 if self.unit_name in self._zero_minimum_units else 1,
                True,
                [self.unit_name]
            )

            if recalculate_parent:
                recalculate_units.append(next_unit(self.unit_name))

        return value_of_time, unit_boundary_reached, recalculate_units

    def _comma_handler(self, date_pointer, value, trigger_secondary):
        """ Handles Cron Syntax parsing for `,` values. """

        value_index = getattr(date_pointer, self.unit_name) % self.time_unit_maximum
        value_index = self.time_unit_maximum if value_index == 0 else value_index

        current_index = None
        values = sorted([int(val) for val in value.split(",")])

        value_of_time, unit_boundary_reached, recalculate_units = None, None, None

        if value_index > max(values):
            current_index = 0
            unit_boundary_reached = True
        else:
            for index, _value in enumerate(values):
                if current_index is None and values[index] > value_index:
                    current_index = index
                    break
                if trigger_secondary and values[index] == value_index:
                    current_index = index
                    recalculate_units = []
                    break

        if current_index is None or value_index == 0:
            if trigger_secondary:
                if value_index == 0:
                    current_index = 0
                    unit_boundary_reached = True
                else:
                    current_index = -1
                recalculate_units = []
            else:
                unit_boundary_reached = True

        value_of_time = values[current_index or 0]

        return value_of_time, unit_boundary_reached, recalculate_units

    def _minus_handler(self, date_pointer, value):
        """ Handles Cron Syntax parsing for `-` values. """
        value_of_time, unit_boundary_reached, recalculate_units = None, None, None

        value_index = getattr(date_pointer, self.unit_name)
        start, end = value.split("-")
        start, end = int(start), int(end)
        values = list(range(start, end + 1))

        current_index = None
        for index, value in enumerate(values):
            if not current_index and values[index] > value_index:
                current_index = index
                break

        if current_index is None:
            unit_boundary_reached = True

        value_of_time = values[current_index or 0]

        return value_of_time, unit_boundary_reached, recalculate_units

    def _asterisk_handler(self, current_time_value):
        """ Handles Cron Syntax parsing for `*` values. """

        value_of_time, unit_boundary_reached, recalculate_units = None, None, None

        values = list(range(current_time_value, self.time_unit_maximum + 1))
        number_of_values = len(values)

        try:
            value_of_time = values[1]
        except IndexError:
            value_of_time = 2 - number_of_values
            unit_boundary_reached = True

        return value_of_time, unit_boundary_reached, recalculate_units

    def _digit_handler(self, date_pointer, value, trigger_secondary):
        """ Handles Cron Syntax parsing for `[0-9]*` values. """
        value_of_time, unit_boundary_reached, recalculate_units = value, None, None

        if trigger_secondary:
            if int(value_of_time) < getattr(date_pointer, self.unit_name):
                unit_boundary_reached = True
        elif int(value_of_time) <= getattr(date_pointer, self.unit_name):
            unit_boundary_reached = True
        else:
            trigger_secondary = True

        return value_of_time, unit_boundary_reached, recalculate_units, trigger_secondary

    def parse(self, date_pointer=None, value=None, ignore_pointer=False, recalculate_parent=False,
              trigger_secondary=False):
        value = self.convert_value(value)
        current_time_value = getattr(date_pointer, self.unit_name)

        _trigger_secondary, trigger_secondary = trigger_secondary, False

        if _trigger_secondary and value in ["*", "?"]:
            return date_pointer, False, [], True

        # TODO: Validate value
        if value.isdigit():
            value_of_time, unit_boundary_reached, recalculate_units, trigger_secondary = \
                self._digit_handler(date_pointer, value, _trigger_secondary)
        elif "/" in value:
            value_of_time, unit_boundary_reached, recalculate_units = self._slash_handler(
                value,
                current_time_value,
                ignore_pointer=ignore_pointer,
                recalculate_parent=recalculate_parent
            )
        elif "," in value:
            value_of_time, unit_boundary_reached, recalculate_units = \
                self._comma_handler(date_pointer, value, _trigger_secondary)
        elif "-" in value:
            value_of_time, unit_boundary_reached, recalculate_units = self._minus_handler(date_pointer, value)
        elif value == "*":
            value_of_time, unit_boundary_reached, recalculate_units = self._asterisk_handler(current_time_value)
        else:
            raise ValueError(f"{value} for the `{self.unit_name}s` unit is not a valid choice.")

        try:
            parsed_date = date_pointer.replace(
                **constructed_kwargs(
                    [self.unit_name],
                    [int(value_of_time)]
                )
            )
        except ValueError:
            parsed_date, unit_boundary_reached, recalculate_units = date_pointer, True, [self.unit_name]

        return parsed_date, unit_boundary_reached, recalculate_units, trigger_secondary


class CronSecondParser(CronUnitParserBase):
    def __init__(self):
        super().__init__("second", 59)


class CronMinuteParser(CronUnitParserBase):
    def __init__(self):
        super().__init__("minute", 59)


class CronHourParser(CronUnitParserBase):
    def __init__(self):
        super().__init__("hour", 23)


class CronDayParser(CronUnitParserBase):
    def __init__(self):
        super().__init__("day", 31)

    @staticmethod
    def _questionmark_handler(date_pointer):
        """ Handles Cron Syntax parsing for `?` values. """

        parsed_date = date_pointer
        unit_boundary_reached = True

        return parsed_date, unit_boundary_reached

    @staticmethod
    def _last_subtractive_handler(date_pointer, value):
        """ Handles Cron Syntax parsing for `L-x` values. """
        value_of_time, unit_boundary_reached, recalculate_units = None, None, None

        subtractive_days = value.split("l-")[1]
        days_in_month = calendar.monthrange(date_pointer.year, date_pointer.month)[1]
        value_of_time = days_in_month - subtractive_days
        if value_of_time <= date_pointer.day:
            unit_boundary_reached = True

        parsed_date = date_pointer.replace(day=value_of_time)

        return parsed_date, value_of_time, unit_boundary_reached, recalculate_units

    def _last_handler(self, date_pointer):
        """ Handles Cron Syntax parsing for `L` values. """
        value_of_time, unit_boundary_reached, recalculate_units = None, None, None

        value_of_time = calendar.monthrange(date_pointer.year, date_pointer.month)[1]
        if value_of_time == date_pointer.day:
            unit_boundary_reached, recalculate_units, value_of_time = True, [self.unit_name], 1
        parsed_date = date_pointer.replace(day=value_of_time)

        return parsed_date, value_of_time, unit_boundary_reached, recalculate_units

    def _last_weekday_handler(self, date_pointer):
        """ Handles Cron Syntax parsing for `W` values. """
        value_of_time, unit_boundary_reached, recalculate_units = None, None, None

        days_in_month = calendar.monthrange(date_pointer.year, date_pointer.month)[1]
        value_of_time = days_in_month

        delta = date_pointer.replace(day=value_of_time).weekday() - 4 if \
            date_pointer.replace(day=value_of_time).weekday() > 4 else 0

        if value_of_time - delta == date_pointer.day:
            unit_boundary_reached, recalculate_units, value_of_time = True, [self.unit_name], 2

        parsed_date = date_pointer.replace(day=value_of_time - delta)

        return parsed_date, value_of_time, unit_boundary_reached, recalculate_units

    def _variable_weekday_handler(self, date_pointer, value, ignore_pointer=None):
        """ Handles Cron Syntax parsing for `xW` values. """
        value_of_time, unit_boundary_reached, recalculate_units = None, None, None

        nth_day = int(value.split("w")[0])
        nth_weekday = get_nth_weekday(date_pointer=date_pointer, nth_day=nth_day)
        if date_pointer.day >= nth_weekday and not ignore_pointer:
            unit_boundary_reached, recalculate_units = True, [self.unit_name]

        parsed_date = date_pointer.replace(day=nth_weekday)

        return parsed_date, value_of_time, unit_boundary_reached, recalculate_units

    def parse(self, date_pointer=None, value=None, ignore_pointer=False, recalculate_parent=False,
              trigger_secondary=False):
        value = self.convert_value(value)
        _trigger_secondary, trigger_secondary = trigger_secondary, False

        if _trigger_secondary and not value.isdigit():
            return date_pointer, False, [], True

        if value == "?":
            parsed_date, unit_boundary_reached = self._questionmark_handler(date_pointer)
            unit_boundary_reached = True
            recalculate_units = []
        elif "l-" in value:
            parsed_date, value_of_time, unit_boundary_reached, recalculate_units = \
                self._last_subtractive_handler(date_pointer, value)
        elif value == "l":
            parsed_date, value_of_time, unit_boundary_reached, recalculate_units = self._last_handler(date_pointer)
        elif value == "lw":
            parsed_date, value_of_time, unit_boundary_reached, recalculate_units = \
                self._last_weekday_handler(date_pointer)
        elif len(value.split("w")) > 1 and value.split("w")[0].isdigit():
            parsed_date, value_of_time, unit_boundary_reached, recalculate_units = \
                self._variable_weekday_handler(date_pointer, value, ignore_pointer=ignore_pointer)
        else:
            parsed_date, unit_boundary_reached, recalculate_units, trigger_secondary = super().parse(
                date_pointer=date_pointer,
                value=value,
                ignore_pointer=ignore_pointer,
                recalculate_parent=recalculate_parent,
                trigger_secondary=_trigger_secondary
            )

        return parsed_date or date_pointer, unit_boundary_reached, recalculate_units, trigger_secondary


class CronMonthParser(CronUnitParserBase):
    def __init__(self):
        super().__init__("month", 12)

    def convert_value(self, cron_value=None):
        """ Translates mappings of jan-dec to 1-12. """
        months = {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,
        }

        cron_value = cron_value.lower()

        for month, index in months.items():
            cron_value = cron_value.replace(month, str(index))

        return cron_value

    def parse(self, date_pointer=None, value=None, ignore_pointer=False, recalculate_parent=False,
              trigger_secondary=False):
        _trigger_secondary, trigger_secondary = trigger_secondary, False

        if _trigger_secondary and value in ["*", "?"]:
            return date_pointer, False, [], True

        value = self.convert_value(value)

        parsed_date, unit_boundary_reached, recalculate_units, trigger_secondary = super().parse(
            date_pointer=date_pointer,
            value=value,
            ignore_pointer=ignore_pointer,
            recalculate_parent=recalculate_parent,
            trigger_secondary=_trigger_secondary
        )

        if recalculate_units is not None:
            _recaculate_units = recalculate_units
        elif _trigger_secondary:
            _recaculate_units = ["day", "day_of_week"]
        else:
            _recaculate_units = []

        return parsed_date, unit_boundary_reached, _recaculate_units, trigger_secondary


class CronDayOfWeekParser(CronUnitParserBase):
    def __init__(self):
        super().__init__("day", 12)

    def convert_value(self, cron_value=None):
        """ Translates mappings of sun-sat to 1-7. """
        days = {
            "sun": 1,
            "mon": 2,
            "tue": 3,
            "wed": 4,
            "thu": 5,
            "fri": 6,
            "sat": 7,
        }

        cron_value = cron_value.lower()

        for month, index in days.items():
            cron_value = cron_value.replace(month, str(index))

        return cron_value

    def _digit_handler(self, value, date_pointer, ignore_pointer=False, trigger_secondary=True):
        """ Handles Cron Syntax parsing for `[0-9]*` values. """

        day_of_week = cron_dow_to_calendar(value)[0]
        month_calendar = calendar.monthcalendar(date_pointer.year, date_pointer.month)
        parsed_date, unit_boundary_reached, recalculate_units = None, False, None

        for week in month_calendar:
            if (week[day_of_week] <= date_pointer.day and not ignore_pointer) or not week[day_of_week]:
                continue
            parsed_date = date_pointer.replace(day=week[day_of_week])
            break

        if not parsed_date:
            recalculate_units = ["day_of_week"]
            unit_boundary_reached = True
            parsed_date = date_pointer.replace(day=1)

        return parsed_date, unit_boundary_reached, recalculate_units

    def _slash_handler(self, date_pointer, value):
        """ Handles Cron Syntax parsing for `x/x` values. """
        parsed_date, unit_boundary_reached, recalculate_units = None, None, None

        start, skip = value.split("/")
        filtered_days = cron_dow_to_calendar(set(range(start, 8, skip)))
        month_calendar = calendar.monthcalendar(date_pointer.year, date_pointer.month)

        parsed_date = None
        for week in month_calendar:
            for day in filtered_days:
                if week[day] <= date_pointer.day:
                    continue
                parsed_date = date_pointer.replace(day=week[day])
                break

        return parsed_date, unit_boundary_reached, recalculate_units

    def _comma_handler(self, date_pointer, value):
        """ Handles Cron Syntax parsing for `,` values. """
        parsed_date, unit_boundary_reached, recalculate_units = None, None, None

        day_values = value.split(",")
        filtered_days = cron_dow_to_calendar(day_values)
        month_calendar = calendar.monthcalendar(date_pointer.year, date_pointer.month)

        parsed_date = None
        for week in month_calendar:
            for day in filtered_days:
                if week[day] <= date_pointer.day:
                    continue
                parsed_date = date_pointer.replace(day=week[day])
                break
            if parsed_date:
                break

        return parsed_date, unit_boundary_reached, recalculate_units

    def _minus_handler(self, date_pointer, value):
        """ Handles Cron Syntax parsing for `-` values. """
        parsed_date, unit_boundary_reached, recalculate_units = None, None, None

        start, end = value.split("-")
        start, end = int(start), int(end)

        if start > end:
            filtered_days = cron_dow_to_calendar(set(constants.DAYS) - set(range(end + 1, start)))
        else:
            filtered_days = cron_dow_to_calendar(set(range(start, end + 1)))

        month_calendar = calendar.monthcalendar(date_pointer.year, date_pointer.month)
        parsed_date = None

        for week in month_calendar:
            for day in filtered_days:
                if week[day] <= date_pointer.day:
                    continue
                parsed_date = date_pointer.replace(day=week[day])
                break
            if parsed_date:
                break

        return parsed_date, unit_boundary_reached, recalculate_units

    @staticmethod
    def _last_handler(date_pointer):
        """ Handles Cron Syntax parsing for `L` values. """
        parsed_date, unit_boundary_reached, recalculate_units = None, None, None

        value_of_time = calendar.monthrange(date_pointer.year, date_pointer.month)[1]

        if value_of_time == date_pointer.day:
            unit_boundary_reached = True

        parsed_date = date_pointer.replace(day=value_of_time)

        return parsed_date, unit_boundary_reached, recalculate_units

    @staticmethod
    def _variable_last_handler(date_pointer, value):
        """ Handles Cron Syntax parsing for `{}L` values. """
        parsed_date, unit_boundary_reached, recalculate_units = None, None, None

        day_of_week = cron_dow_to_calendar(value.split("l")[0])[0]
        month_calendar = calendar.monthcalendar(date_pointer.year, date_pointer.month)

        for week in month_calendar[::-1]:
            if not week[day_of_week]:
                continue
            value_of_time = week[day_of_week]

            if value_of_time <= date_pointer.day:
                recalculate_units, unit_boundary_reached, value_of_time = ["day_of_week"], True, 1

            parsed_date = date_pointer.replace(day=value_of_time)
            break

        return parsed_date, unit_boundary_reached, recalculate_units

    @staticmethod
    def _hash_handler(date_pointer, value):
        """ Handles Cron Syntax parsing for `#` values. """
        parsed_date, unit_boundary_reached, recalculate_units = None, None, None

        day_of_week, ordinal = value.split("#")
        day_of_week, ordinal = int(day_of_week), int(ordinal)
        day_of_week = cron_dow_to_calendar(day_of_week)[0]
        month_calendar = calendar.monthcalendar(date_pointer.year, date_pointer.month)
        offset = 0 if month_calendar[0][day_of_week] != 0 else 1

        try:
            if ordinal + offset > len(month_calendar) or month_calendar[ordinal - 1 + offset][day_of_week] == 0:
                value_of_time, unit_boundary_reached, recalculate_units = 1, True, ["day_of_week"]
            else:
                value_of_time = month_calendar[ordinal - 1 + offset][day_of_week]

            if value_of_time <= date_pointer.day:
                value_of_time, unit_boundary_reached, recalculate_units = 1, True, ["day_of_week"]
        except IndexError:
            value_of_time, unit_boundary_reached, recalculate_units = 1, True, ["day_of_week"]

        parsed_date = date_pointer.replace(day=value_of_time)

        return parsed_date, unit_boundary_reached, recalculate_units

    def parse(self, date_pointer=None, value=None, ignore_pointer=False, recalculate_parent=False,
              trigger_secondary=False):
        value = self.convert_value(value)

        _trigger_secondary, trigger_secondary = trigger_secondary, False

        if _trigger_secondary and not value.isdigit() and "#" not in value:
            return date_pointer, False, [], True

        parsed_date, unit_boundary_reached, recalculate_units = None, False, None

        if value == "?":
            unit_boundary_reached = True
        elif value.isdigit():
            parsed_date, unit_boundary_reached, recalculate_units = self._digit_handler(
                value,
                date_pointer,
                ignore_pointer=ignore_pointer,
                trigger_secondary=_trigger_secondary
            )

        elif "/" in value:
            parsed_date, unit_boundary_reached, recalculate_units = self._slash_handler(date_pointer, value)
        elif "," in value:
            parsed_date, unit_boundary_reached, recalculate_units = self._comma_handler(date_pointer, value)
        elif "-" in value:
            parsed_date, unit_boundary_reached, recalculate_units = self._minus_handler(date_pointer, value)
        elif value == "l":
            parsed_date, unit_boundary_reached, recalculate_units = self._last_handler(date_pointer)
        elif "l" in value and len(value) > 1:
            parsed_date, unit_boundary_reached, recalculate_units = self._variable_last_handler(date_pointer, value)
        elif "#" in value:
            parsed_date, unit_boundary_reached, recalculate_units = self._hash_handler(date_pointer, value)

        return parsed_date or date_pointer, unit_boundary_reached, recalculate_units, trigger_secondary


class CronYearParser(CronUnitParserBase):
    def __init__(self):
        super().__init__("year", 2099)

    def parse(self, date_pointer=None, value=None, ignore_pointer=False, recalculate_parent=False,
              trigger_secondary=False):
        value = self.convert_value(value)
        unit_boundary_reached, recalculate_units = False, None

        _trigger_secondary, trigger_secondary = trigger_secondary, False

        if _trigger_secondary and not value.isdigit():
            return date_pointer, False, [], True

        if value == "":
            return date_pointer, unit_boundary_reached, recalculate_units, trigger_secondary

        return super().parse(
            date_pointer=date_pointer,
            value=value,
            trigger_secondary=trigger_secondary,
            ignore_pointer=ignore_pointer,
            recalculate_parent=recalculate_parent
        )
