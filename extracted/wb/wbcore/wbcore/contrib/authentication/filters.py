from wbcore import filters as wb_filters
from wbcore.filters.defaults import current_month_date_range

from .models import UserActivity


class UserActivityChartFilter(wb_filters.FilterSet):
    date = wb_filters.DateTimeRangeFilter(
        label="Date Range",
        required=True,
        clearable=False,
        initial=current_month_date_range,
    )

    class Meta:
        model = UserActivity
        fields = {}
