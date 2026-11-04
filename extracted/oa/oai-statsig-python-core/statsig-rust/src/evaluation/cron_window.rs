use chrono::{DateTime, Datelike, NaiveDate, Timelike, Utc};

const MAX_DURATION_SECONDS: i64 = 366 * 24 * 60 * 60;

#[derive(Clone, Debug, Eq, PartialEq)]
pub(crate) struct CronWindow {
    minutes: u64,
    hours: u64,
    days_of_month: u64,
    months: u64,
    days_of_week: u64,
    day_of_month_unrestricted: bool,
    day_of_week_unrestricted: bool,
    duration_millis: i64,
}

#[derive(Clone, Copy)]
enum CronField {
    Minute,
    Hour,
    DayOfMonth,
    Month,
    DayOfWeek,
}

impl CronField {
    fn bounds(self) -> (u32, u32) {
        match self {
            Self::Minute => (0, 59),
            Self::Hour => (0, 23),
            Self::DayOfMonth => (1, 31),
            Self::Month => (1, 12),
            Self::DayOfWeek => (0, 7),
        }
    }

    fn normalize(self, value: u32) -> u32 {
        if matches!(self, Self::DayOfWeek) && value == 7 {
            0
        } else {
            value
        }
    }
}

impl CronWindow {
    pub(crate) fn parse(value: &str) -> Result<Self, &'static str> {
        let (expression, duration) = value
            .rsplit_once('|')
            .ok_or("cron window must contain a duration separator")?;
        if expression.contains('|') {
            return Err("cron window must contain exactly one duration separator");
        }

        let duration_seconds = duration
            .parse::<i64>()
            .map_err(|_| "cron window duration must be an integer")?;
        if !(1..=MAX_DURATION_SECONDS).contains(&duration_seconds) {
            return Err("cron window duration is out of range");
        }

        let fields = expression.split_whitespace().collect::<Vec<_>>();
        if fields.len() != 5 {
            return Err("cron window must use a five-field expression");
        }

        let (minutes, _) = parse_field(fields[0], CronField::Minute)?;
        let (hours, _) = parse_field(fields[1], CronField::Hour)?;
        let (days_of_month, day_of_month_unrestricted) =
            parse_field(fields[2], CronField::DayOfMonth)?;
        let (months, _) = parse_field(fields[3], CronField::Month)?;
        let (days_of_week, day_of_week_unrestricted) =
            parse_field(fields[4], CronField::DayOfWeek)?;

        Ok(Self {
            minutes,
            hours,
            days_of_month,
            months,
            days_of_week,
            day_of_month_unrestricted,
            day_of_week_unrestricted,
            duration_millis: duration_seconds.saturating_mul(1000),
        })
    }

    pub(crate) fn is_active_at_millis(&self, timestamp_millis: i64) -> bool {
        let Some(now) = DateTime::<Utc>::from_timestamp_millis(timestamp_millis) else {
            return false;
        };

        let mut date = now.date_naive();
        let max_lookback_days = self.duration_millis / 86_400_000 + 1;

        for _ in 0..=max_lookback_days {
            if self.date_matches(date) {
                if let Some(occurrence) = self.latest_occurrence_on(date, now) {
                    let elapsed = timestamp_millis.saturating_sub(occurrence.timestamp_millis());
                    return elapsed >= 0 && elapsed < self.duration_millis;
                }
            }

            let Some(previous_date) = date.pred_opt() else {
                return false;
            };
            date = previous_date;
        }

        false
    }

    fn date_matches(&self, date: NaiveDate) -> bool {
        if !contains(self.months, date.month()) {
            return false;
        }

        let day_of_month_matches = contains(self.days_of_month, date.day());
        let day_of_week_matches =
            contains(self.days_of_week, date.weekday().num_days_from_sunday());

        match (
            self.day_of_month_unrestricted,
            self.day_of_week_unrestricted,
        ) {
            (true, true) => true,
            (true, false) => day_of_week_matches,
            (false, true) => day_of_month_matches,
            (false, false) => day_of_month_matches || day_of_week_matches,
        }
    }

    fn latest_occurrence_on(&self, date: NaiveDate, now: DateTime<Utc>) -> Option<DateTime<Utc>> {
        let is_today = date == now.date_naive();

        for hour in (0..=23).rev() {
            if !contains(self.hours, hour) || (is_today && hour > now.hour()) {
                continue;
            }

            let latest_minute = if is_today && hour == now.hour() {
                now.minute()
            } else {
                59
            };

            for minute in (0..=latest_minute).rev() {
                if !contains(self.minutes, minute) {
                    continue;
                }

                let occurrence = date.and_hms_opt(hour, minute, 0)?;
                return Some(DateTime::from_naive_utc_and_offset(occurrence, Utc));
            }
        }

        None
    }
}

fn parse_field(value: &str, field: CronField) -> Result<(u64, bool), &'static str> {
    if value.is_empty() {
        return Err("cron field cannot be empty");
    }

    let (minimum, maximum) = field.bounds();
    let mut bits = 0_u64;

    for item in value.split(',') {
        if item.is_empty() {
            return Err("cron list item cannot be empty");
        }

        let mut step_parts = item.split('/');
        let range = step_parts.next().unwrap_or_default();
        let step = match step_parts.next() {
            Some(raw_step) => {
                let parsed = raw_step
                    .parse::<u64>()
                    .map_err(|_| "cron step must be a positive integer")?;
                if parsed == 0 {
                    return Err("cron step must be a positive integer");
                }
                u32::try_from(parsed).map_err(|_| "cron step is out of range")?
            }
            None => 1,
        };
        if step_parts.next().is_some() {
            return Err("cron field contains too many step separators");
        }

        let (start, end) = if range == "*" {
            (minimum, maximum)
        } else if let Some((raw_start, raw_end)) = range.split_once('-') {
            let start = parse_bounded_value(raw_start, minimum, maximum)?;
            let end = parse_bounded_value(raw_end, minimum, maximum)?;
            if start > end {
                return Err("cron ranges cannot wrap");
            }
            (start, end)
        } else {
            if step != 1 {
                return Err("cron steps require a wildcard or range");
            }
            let single = parse_bounded_value(range, minimum, maximum)?;
            (single, single)
        };

        for candidate in (start..=end).step_by(step as usize) {
            bits |= 1_u64 << field.normalize(candidate);
        }
    }

    if bits == 0 {
        return Err("cron field has no values");
    }

    let full_domain_bits = (minimum..=maximum).fold(0_u64, |all, candidate| {
        all | (1_u64 << field.normalize(candidate))
    });

    Ok((bits, bits == full_domain_bits))
}

fn parse_bounded_value(value: &str, minimum: u32, maximum: u32) -> Result<u32, &'static str> {
    let parsed = value
        .parse::<u32>()
        .map_err(|_| "cron field contains an invalid value")?;
    if !(minimum..=maximum).contains(&parsed) {
        return Err("cron field value is out of range");
    }
    Ok(parsed)
}

fn contains(bits: u64, value: u32) -> bool {
    bits & (1_u64 << value) != 0
}

#[cfg(test)]
mod tests {
    use chrono::{TimeZone, Utc};

    use super::CronWindow;

    fn millis(year: i32, month: u32, day: u32, hour: u32, minute: u32, second: u32) -> i64 {
        Utc.with_ymd_and_hms(year, month, day, hour, minute, second)
            .single()
            .unwrap()
            .timestamp_millis()
    }

    #[test]
    fn evaluates_daily_window_across_midnight() {
        let window = CronWindow::parse("0 22 * * *|43200").unwrap();

        assert!(!window.is_active_at_millis(millis(2026, 9, 18, 21, 59, 59)));
        assert!(window.is_active_at_millis(millis(2026, 9, 18, 22, 0, 0)));
        assert!(window.is_active_at_millis(millis(2026, 9, 19, 9, 59, 59)));
        assert!(!window.is_active_at_millis(millis(2026, 9, 19, 10, 0, 0)));
    }

    #[test]
    fn supports_numeric_lists_ranges_and_steps() {
        let window = CronWindow::parse("*/15 9-17 * 1,3 1-5|60").unwrap();

        assert!(window.is_active_at_millis(millis(2026, 3, 2, 9, 15, 30)));
        assert!(!window.is_active_at_millis(millis(2026, 3, 2, 9, 16, 0)));
        assert!(!window.is_active_at_millis(millis(2026, 2, 2, 9, 15, 30)));
        assert!(!window.is_active_at_millis(millis(2026, 3, 1, 9, 15, 30)));
    }

    #[test]
    fn uses_unsigned_32_bit_step_bound() {
        // These fixtures mirror DCS generation/parser parity coverage.
        assert!(CronWindow::parse("*/4294967295 * * * *|60").is_ok());
        assert_eq!(
            CronWindow::parse("*/4294967296 * * * *|60"),
            Err("cron step is out of range")
        );
    }

    #[test]
    fn uses_posix_or_semantics_for_restricted_days() {
        let window = CronWindow::parse("0 0 1 * 1|60").unwrap();

        assert!(window.is_active_at_millis(millis(2026, 9, 1, 0, 0, 30)));
        assert!(window.is_active_at_millis(millis(2026, 9, 7, 0, 0, 30)));
        assert!(!window.is_active_at_millis(millis(2026, 9, 8, 0, 0, 30)));
    }

    #[test]
    fn treats_full_day_domains_as_unrestricted() {
        // These fixtures mirror DCS generation/parser parity coverage. Tuesday
        // must not match a Monday-only DOW when DOM covers its complete domain.
        for expression in ["0 0 */1 * 1|60", "0 0 1-31 * 1|60"] {
            let window = CronWindow::parse(expression).unwrap();

            assert!(window.day_of_month_unrestricted, "{expression}");
            assert!(window.is_active_at_millis(millis(2026, 9, 7, 0, 0, 30)));
            assert!(!window.is_active_at_millis(millis(2026, 9, 8, 0, 0, 30)));
        }
    }

    #[test]
    fn rejects_invalid_encoding() {
        assert!(CronWindow::parse("0 22 * * *").is_err());
        assert!(CronWindow::parse("0 22 * * *|0").is_err());
        assert!(CronWindow::parse("0 22 * * *|31622401").is_err());
        assert!(CronWindow::parse("0 22 * * * *|60").is_err());
        assert!(CronWindow::parse("60 22 * * *|60").is_err());
        assert!(CronWindow::parse("0 22 * JAN *|60").is_err());
        assert!(CronWindow::parse("0 22 * * MON|60").is_err());
        assert!(CronWindow::parse("0 22 * * FUNDAY|60").is_err());
    }
}
