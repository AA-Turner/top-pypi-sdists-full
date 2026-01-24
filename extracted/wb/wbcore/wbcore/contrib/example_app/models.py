from __future__ import annotations

import datetime
from contextlib import suppress
from decimal import Decimal
from pathlib import Path

from celery import current_app, shared_task
from django.contrib.postgres.fields import DateRangeField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition
from psycopg.types.range import TimestamptzRange
from slugify import slugify

from wbcore.contrib.agenda.models import CalendarItem
from wbcore.contrib.authentication.models import User
from wbcore.contrib.color.enums import WBColor
from wbcore.contrib.color.models import ColorField
from wbcore.contrib.directory.models import Company, Person
from wbcore.contrib.geography.models import Geography
from wbcore.contrib.icons import WBIcon
from wbcore.contrib.icons.models import IconField
from wbcore.enums import RequestType
from wbcore.metadata.configs.buttons import ActionButton
from wbcore.models.orderable import OrderableModel
from wbcore.utils.models import ActiveObjectManager, ComplexToStringMixin
from wbcore.workers import Queue


def upload_to_profile_images(instance, filename):
    file_extension = "".join(Path(filename).suffixes)
    return f"example_app/sport_person/profile_images/{instance.id}{file_extension}"


class Role(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name=_("Title"))
    slugify_title = models.CharField(max_length=100, unique=True, null=True, blank=True)

    sport_persons: models.QuerySet[SportPerson]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slugify_title = slugify(self.title, separator=" ")
        super().save(*args, **kwargs)

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:role"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:rolerepresentation-list"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{title}}"

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


class SportPerson(ComplexToStringMixin):
    roles = models.ManyToManyField(to=Role, blank=True, related_name="sport_persons", verbose_name=_("Roles"))
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    profile = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="sport_profile")
    profile_image = models.ImageField(blank=True, null=True, upload_to=upload_to_profile_images, max_length=256)

    coached_team: Team
    commissioned_leagues: models.QuerySet[League]
    refereed_matches: models.QuerySet[Match]
    events: models.QuerySet[Event]

    def str_full(self) -> str:
        """
        Get the string representation including the coached team or commissioned league.
        """

        full_name = f"{self.first_name} {self.last_name}"

        # Why is it necessary to exclude the null values?
        if Team.objects.exclude(coach__isnull=True).filter(coach_id=self.id).exists():
            full_name += _(f" (Coach of {self.coached_team.name})")
        elif League.objects.exclude(commissioner__isnull=True).filter(commissioner_id=self.id).exists():
            full_name += _(f" (Commissioner of {self.commissioned_leagues.first().name})")

        return full_name

    def compute_str(self) -> str:
        self.slugify_computed_str = slugify(self.str_full(), separator=" ")
        return self.str_full()

    def get_player(self) -> Player | None:
        """Tries to cast a sport person into its child player class."""

        try:
            return Player.objects.get(id=self.pk)
        except Player.DoesNotExist:
            return None

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:person"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:personrepresentation-list"

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    slugify_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    rules = models.TextField(max_length=100, null=True, blank=True, verbose_name=_("Rules"))
    match_duration = models.PositiveIntegerField(verbose_name=_("Match Duration (min)"))

    matches: models.QuerySet[Match]
    event_types: models.QuerySet[EventType]
    leagues: models.QuerySet[League]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slugify_name = slugify(self.name, separator=" ")
        super().save(*args, **kwargs)

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:sport"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:sportrepresentation-list"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{name}}"

    class Meta:
        verbose_name = _("Sport")
        verbose_name_plural = _("Sports")


@receiver(models.signals.post_save, sender=Sport)
def post_save_sport(sender, instance: Sport, created: bool, raw: bool, **kwargs):
    """Triggers the save signals of the sport's leagues updating their computed_str"""

    if not raw:
        if leagues := instance.leagues.all():
            for league in leagues:
                league.save()


class League(ComplexToStringMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    sport = models.ForeignKey(
        to=Sport,
        on_delete=models.PROTECT,
        related_name="leagues",
        verbose_name=_("Sport"),
    )
    country = models.ForeignKey(
        to=Geography,
        limit_choices_to={"level": 1},
        related_name="leagues",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Country"),
    )
    established_date = models.DateField(null=True, blank=True, verbose_name=_("Established Date"))
    commissioner = models.ForeignKey(
        to=SportPerson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissioned_leagues",
        verbose_name=_("Commissioner"),
    )
    website = models.URLField(max_length=200, null=True, blank=True, verbose_name=_("Website"))
    points_per_win = models.PositiveIntegerField(verbose_name=_("Points Per Win"))
    points_per_draw = models.PositiveIntegerField(verbose_name=_("Points Per Draw"), default=1)
    points_per_loss = models.PositiveIntegerField(verbose_name=_("Points Per Loss"), default=0)
    teams = models.ManyToManyField(
        "Team",
        related_name="leagues",
        blank=True,
        through="TeamResults",
        through_fields=("league", "team"),
        verbose_name=_("Teams"),
    )

    matches: models.QuerySet[Match]
    results: models.QuerySet[TeamResults]
    seasons: models.QuerySet[Season]

    def __str__(self) -> str:
        return f"{self.name} ({self.sport.name})"

    def compute_str(self) -> str:
        return self.__str__()

    class Meta:
        verbose_name = _("League")
        verbose_name_plural = _("Leagues")
        constraints = [
            models.UniqueConstraint(fields=["name", "sport"], name="league_name_sport"),
        ]

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:league"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:leaguerepresentation-list"


@receiver(models.signals.post_save, sender=League)
def post_save_league(sender, instance: League, created: bool, raw: bool, **kwargs):
    """Triggers the save signals of the league's commissioner updating their computed_str"""

    if not raw:
        if instance.commissioner:
            instance.commissioner.save()


class TeamResults(models.Model):
    team = models.ForeignKey(
        on_delete=models.CASCADE,
        to="Team",
        verbose_name=_("Team"),
        related_name="results",
    )
    league = models.ForeignKey(
        on_delete=models.CASCADE,
        to=League,
        verbose_name=_("League"),
        related_name="results",
    )
    points = models.PositiveIntegerField(verbose_name=_("Points"), default=0)
    match_points_for = models.PositiveIntegerField(verbose_name=_("Match Points For"), default=0)
    match_points_against = models.PositiveIntegerField(verbose_name=_("Match Points Against"), default=0)
    match_point_difference = models.IntegerField(verbose_name=_("Match Point Difference"), default=0)
    wins = models.PositiveIntegerField(verbose_name=_("Wins"), default=0)
    draws = models.PositiveIntegerField(verbose_name=_("Draws"), default=0)
    losses = models.PositiveIntegerField(verbose_name=_("Losses"), default=0)
    form = models.CharField(verbose_name=_("Form"), max_length=5, default="-----")

    def __str__(self) -> str:
        return _("{} in {}").format(self.team.name, self.league.name)

    def save(self, *args, **kwargs):
        self.match_point_difference = self.match_points_for - self.match_points_against
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Team Result")
        verbose_name_plural = _("Team Results")
        constraints = [
            models.UniqueConstraint(fields=["team", "league"], name="unique_team_league"),
        ]

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:teamresults"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:teamresultsrepresentation-list"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{team__name}} in {{league__computed_str}}"


class Stadium(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    slugify_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    city = models.ForeignKey(
        to=Geography,
        limit_choices_to={"level": 3},
        related_name="stadiums",
        on_delete=models.PROTECT,
        verbose_name=_("City"),
        null=True,
        blank=True,
    )
    standing_capacity = models.PositiveIntegerField(default=0, verbose_name=_("Standing Capacity"))
    seating_capacity = models.PositiveIntegerField(default=0, verbose_name=_("Seating Capacity"))
    guest_rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        default=3,
        verbose_name=_("Guest Rating"),
    )

    teams_playing: models.QuerySet[Team]
    matches: models.QuerySet[Match]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slugify_name = slugify(self.name, separator=" ")
        super().save(*args, **kwargs)

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:stadium"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:stadiumrepresentation-list"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{name}}"

    @property
    def total_capacity(self):
        return self.standing_capacity + self.seating_capacity

    class Meta:
        verbose_name = _("Stadium")
        verbose_name_plural = _("Stadiums")


class Match(ComplexToStringMixin, CalendarItem):
    class MatchStatus(models.TextChoices):
        SCHEDULED = "SCHEDULED", _("Scheduled")
        ONGOING = "ONGOING", _("Ongoing")
        FINISHED = "FINISHED", _("Finished")

        @classmethod
        def get_color_map(cls) -> list[tuple[Match.MatchStatus, str]]:
            colors = [
                WBColor.YELLOW_LIGHT.value,
                WBColor.BLUE_LIGHT.value,
                WBColor.GREEN_LIGHT.value,
            ]
            return [status for status in zip(cls, colors, strict=False)]

    home = models.ForeignKey(
        to="Team",
        related_name="home_matches",
        on_delete=models.CASCADE,
        verbose_name=_("Home"),
    )
    away = models.ForeignKey(
        to="Team",
        related_name="away_matches",
        on_delete=models.CASCADE,
        verbose_name=_("Away"),
    )
    date_time = models.DateTimeField(verbose_name=_("Date Time"))
    stadium = models.ForeignKey(
        to=Stadium,
        related_name="matches",
        on_delete=models.CASCADE,
        verbose_name=_("Stadium"),
    )
    status = FSMField(
        choices=MatchStatus.choices,
        verbose_name=_("Status"),
        default=MatchStatus.SCHEDULED,
    )
    score_home = models.PositiveIntegerField(verbose_name=_("Home Score"), default=0, editable=False)
    score_away = models.PositiveIntegerField(verbose_name=_("Away Score"), default=0, editable=False)
    referee = models.ForeignKey(
        to=SportPerson,
        null=True,
        blank=True,
        related_name="refereed_matches",
        on_delete=models.SET_NULL,
    )
    league = models.ForeignKey(
        to=League,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches",
        verbose_name=_("League"),
    )
    winner = models.ForeignKey(
        "Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_matches",
    )
    sport = models.ForeignKey(
        to=Sport,
        on_delete=models.PROTECT,
        related_name="matches",
        verbose_name=_("Sport"),
    )
    task_id = models.CharField(blank=True, editable=False, max_length=50)

    events: models.QuerySet[Event]

    def has_permissions(self: Match, user: User) -> bool:
        if user.is_superuser or user.has_perm("wbcore.change_match_status"):
            return True
        return False

    @transition(
        field=status,
        source=[MatchStatus.SCHEDULED],
        target=MatchStatus.ONGOING,
        permission=has_permissions,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("example_app:match",),
                icon=WBIcon.START.icon,
                key="start",
                label=_("Start"),
                action_label=_("Starting"),
                description_fields=_("Are you sure you want to start the match?"),
            )
        },
    )
    def start(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=[MatchStatus.ONGOING],
        target=MatchStatus.FINISHED,
        permission=has_permissions,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("example_app:match",),
                icon=WBIcon.TIME_UP.icon,
                key="end",
                label=_("End"),
                action_label=_("Ending"),
                description_fields=_("Are you sure you want to end the match?"),
            )
        },
    )
    def end(self, by=None, description=None, **kwargs):
        pass

    def __str__(self) -> str:
        return f"{self.home.name} vs. {self.away.name}"

    def recompute_computed_str(self):
        """A separate function to only update the computed_str to not have to call the compute-heavy save method each time"""

        Match.objects.filter(id=self.pk).update(computed_str=self.compute_str())

    def reschedule_task(self):
        """Reschedules the task that automatically starts a match at the given date time"""

        if task_id := self.task_id:
            current_app.control.revoke(task_id, terminate=True)
        new_task = start_match.apply_async(eta=self.date_time, args=[self.pk])
        self.task_id = new_task.id

    def get_color(self) -> str:
        return "#f7be2f"  # dark yellow

    def get_icon(self) -> str:
        return WBIcon.GOAL.icon

    def save(self, *args, **kwargs):
        start_time = self.date_time
        end_time = start_time + datetime.timedelta(minutes=self.sport.match_duration)
        self.period = TimestamptzRange(start_time, end_time)
        self.title = self.__str__()

        if self.status == self.MatchStatus.FINISHED and self.score_home > self.score_away:
            self.winner = self.home
        elif self.status == self.MatchStatus.FINISHED and self.score_away > self.score_home:
            self.winner = self.away
        else:
            self.winner = None

        # if we change the date time we need to reschedule the task that automatically starts the match
        try:
            old_instance = Match.objects.get(pk=self.pk)
            if old_instance.date_time != self.date_time:
                self.reschedule_task()
        except Match.DoesNotExist:
            self.reschedule_task()

        if self.league and self.task_id and self.status == self.MatchStatus.FINISHED:
            home_results, created1 = TeamResults.objects.get_or_create(team=self.home, league=self.league)
            away_results, created2 = TeamResults.objects.get_or_create(team=self.away, league=self.league)

            # Update points, W/L/D & form
            # Home win
            if self.score_home > self.score_away:
                home_results.wins += 1
                home_results.form = home_results.form[1:] + "W"
                home_results.points += self.league.points_per_win
                away_results.losses += 1
                away_results.form = away_results.form[1:] + "L"
                away_results.points += self.league.points_per_loss

            # Away win
            elif self.score_home < self.score_away:
                home_results.losses += 1
                home_results.form = home_results.form[1:] + "L"
                home_results.points += self.league.points_per_loss
                away_results.wins += 1
                away_results.form = away_results.form[1:] + "W"
                away_results.points += self.league.points_per_win

            # Draw
            else:
                home_results.draws += 1
                home_results.form = home_results.form[1:] + "D"
                home_results.points += self.league.points_per_draw
                away_results.draws += 1
                away_results.form = away_results.form[1:] + "D"
                away_results.points += self.league.points_per_draw

            # Update match points
            home_results.match_points_for += self.score_home
            home_results.match_points_against += self.score_away
            away_results.match_points_for += self.score_away
            away_results.match_points_against += self.score_home

            # Update match point difference
            home_results.save()
            away_results.save()

            # Set empty task ID to indicate that this match's result has been synchronized to the league table
            self.task_id = ""

        return super().save(*args, **kwargs)

    def compute_str(self) -> str:
        return self.__str__()

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:match"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:matchrepresentation-list"

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")
        constraints = [
            models.UniqueConstraint(fields=["home", "away", "date_time"], name="match_home_away_date_time"),
            models.CheckConstraint(condition=~models.Q(home=models.F("away")), name="check_match_home_away"),
        ]
        permissions = [("change_match_status", "Change Match Status")]


@shared_task(queue=Queue.DEFAULT.value)
def start_match(match_id: int):
    """Sets the match status from scheduled to ongoing.

    Args:
        match_id (int): ID of the match in question
    """
    with suppress(Match.DoesNotExist):
        match = Match.objects.get(pk=match_id)
        if match.status == Match.MatchStatus.SCHEDULED:
            match.status = Match.MatchStatus.ONGOING
            match.save()


@receiver(models.signals.post_save, sender=Match)
def update_team_duration_since_last_win(sender, instance: Match, **kwargs):
    if instance.winner:
        team = instance.winner

        # Calculate the duration since the current match win
        now = timezone.now()
        match_date = instance.date_time
        new_duration_since_win = now - match_date

        # Update only if this win is more recent (i.e., duration is shorter)
        if team.duration_since_last_win is None or new_duration_since_win < team.duration_since_last_win:
            team.duration_since_last_win = new_duration_since_win
            team.save()


@receiver(models.signals.post_save, sender=Match)
def post_save_match(sender, instance: Match, created: bool, raw: bool, **kwargs):
    """Sets the entities in the parent calendar item"""

    if raw:
        return

    home_sport_persons = SportPerson.objects.filter(
        Q(id__in=instance.home.current_players.all()) | Q(coached_team=instance.home)
    )
    away_sport_persons = SportPerson.objects.filter(
        Q(id__in=instance.away.current_players.all()) | Q(coached_team=instance.away)
    )
    referee = SportPerson.objects.none()
    if instance.referee:
        referee = SportPerson.objects.filter(id=instance.referee.id)
    match_persons_ids = home_sport_persons.union(away_sport_persons, referee).values_list("profile__id", flat=True)

    instance.entities.set(match_persons_ids)
    instance.entities.add(instance.home, instance.away)


class Team(OrderableModel, Company):
    slugify_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    city = models.ForeignKey(
        to=Geography,
        limit_choices_to={"level": 3},
        related_name="teams",
        on_delete=models.PROTECT,
        verbose_name=_("City"),
        null=True,
        blank=True,
    )
    founded_date = models.DateField(null=True, blank=True, verbose_name=_("Founded Date"))
    coach = models.OneToOneField(
        to=SportPerson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coached_team",
        verbose_name=_("Coach"),
    )
    home_stadium = models.ForeignKey(
        to=Stadium,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teams_playing",
        verbose_name=_("Home Stadium"),
    )
    opponents = models.ManyToManyField(
        to="self",
        blank=True,
        through=Match,
        through_fields=("home", "away"),
        verbose_name=_("Opponents"),
    )
    duration_since_last_win = models.DurationField(
        blank=True,
        null=True,
    )
    email = models.EmailField(verbose_name=_("Email Address"), null=True, blank=True)
    phone_number = models.CharField(max_length=255, verbose_name=_("Phone Number"), null=True, blank=True)
    objects = ActiveObjectManager()
    website = models.URLField(default="https://duckduckgo.com/", verbose_name=_("Website"))
    current_players: models.QuerySet[Player]
    former_players: models.QuerySet[Player]
    home_matches: models.QuerySet[Match]
    away_matches: models.QuerySet[Match]
    results: models.QuerySet[TeamResults]
    won_seasons: models.QuerySet[Season]
    won_matches: models.QuerySet[Match]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slugify_name = slugify(self.name, separator=" ")
        super().save(*args, **kwargs)

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:team"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:teamrepresentation-list"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{name}}"

    class Meta(OrderableModel.Meta):
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")


@receiver(models.signals.post_save, sender=Team)
def post_save_team(sender, instance: Team, created: bool, raw: bool, **kwargs):
    """Triggers the save signals of the team's coaches, current players and matches updating their computed_str"""

    if not raw:
        if instance.coach:
            instance.coach.save()
        if players := instance.current_players.all():
            for player in players:
                player.save()
        if home_matches := instance.home_matches.all():
            for home_match in home_matches:
                home_match.recompute_computed_str()
        if away_matches := instance.away_matches.all():
            for away_match in away_matches:
                away_match.recompute_computed_str()


class Player(OrderableModel, SportPerson):  # noqa
    PARTITION_BY = PARENT_FK = "current_team"

    position = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Position"))
    current_team = models.ForeignKey(
        to=Team,
        related_name="current_players",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Current Team"),
    )
    former_teams = models.ManyToManyField(
        to=Team,
        related_name="former_players",
        blank=True,
        verbose_name=_("Former Teams"),
    )
    transfer_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0),
        verbose_name=_("Market Value"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_injured = models.BooleanField(default=False, verbose_name=_("Is Injured"))
    player_strength = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=3,
        verbose_name=_("Player Strength"),
    )
    game_activity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0,
        verbose_name=_("Game Activity"),
    )
    top_scorer_seasons: models.QuerySet[Season]

    def str_full(self) -> str:
        """
        Get the string representation including the position and the current team.
        """

        full_name = f"{self.first_name} {self.last_name}"

        if self.current_team and self.position:
            full_name += _(f" ({self.position} at {self.current_team.name})")
        elif self.current_team:
            full_name += _(f" ({self.current_team.name})")

        return full_name

    def compute_str(self) -> str:
        self.slugify_computed_str = slugify(self.str_full(), separator=" ")
        return self.str_full()

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:player"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:playerrepresentation-list"

    class Meta(OrderableModel.Meta):
        verbose_name = _("Player")
        verbose_name_plural = _("Players")


class Event(models.Model):
    event_description = models.TextField(verbose_name=_("Event Description"), max_length=512, blank=True, null=True)
    person = models.ForeignKey(
        to=SportPerson,
        related_name="events",
        on_delete=models.CASCADE,
        verbose_name=_("Person"),
    )
    match = models.ForeignKey(
        to=Match,
        related_name="events",
        on_delete=models.CASCADE,
        verbose_name=_("Match"),
    )
    minute = models.PositiveIntegerField(verbose_name=_("Minute"))
    event_type = models.ForeignKey(
        to="EventType",
        related_name="events",
        on_delete=models.CASCADE,
        verbose_name=_("Event Type"),
    )

    def __str__(self) -> str:
        return f"{self.event_type.name} ({self.minute}.) - {self.person.computed_str}"

    def save(self, *args, **kwargs):
        match = self.match
        if player := self.person.get_player():
            if player in match.home.current_players.all():
                match.score_home += self.event_type.points
                match.save()
            elif player in match.away.current_players.all():
                match.score_away += self.event_type.points
                match.save()
        super().save(*args, **kwargs)

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:event"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:eventrepresentation-list"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{event_type__name}} ({{minute}}.) - {{person}}"

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        constraints = [
            models.UniqueConstraint(
                fields=["person", "match", "minute", "event_type"],
                name="event_person_match_minute_event_type",
            ),
        ]


class EventType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    points = models.PositiveIntegerField(
        verbose_name=_("Points"),
        help_text=_("Number of points awarded to a player's team per event"),
        default=1,
    )
    sport = models.ForeignKey(
        to=Sport,
        related_name="event_types",
        on_delete=models.CASCADE,
        verbose_name=_("Sport"),
    )
    icon = IconField(
        max_length=128,
        verbose_name=_("Icon"),
        default=WBIcon.GOAL.icon,
    )
    color = ColorField(null=True, blank=True)

    events: models.QuerySet[Event]

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:eventtype"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:eventtyperepresentation-list"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{name}}"

    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")
        constraints = [
            models.UniqueConstraint(fields=["name", "sport"], name="event_type_name_sport"),
        ]


class Season(models.Model):
    league = models.ForeignKey("League", on_delete=models.CASCADE, related_name="seasons")
    date_range = DateRangeField()
    name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="season_files/", blank=True, null=True)
    winner = models.ForeignKey(
        "Team",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="won_seasons",
    )
    top_scorer = models.ForeignKey(
        "Player",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="top_scorer_seasons",
    )

    def __str__(self):
        return f"{self.name} ({self.league})"

    def save(self, *args, **kwargs):
        if self.date_range:
            start_date = self.date_range.lower
            end_date = self.date_range.upper

            if not self.name and (start_date and end_date):
                self.name = f"{self.league.name} / {start_date.year}-{end_date.year} Season"

        super().save(*args, **kwargs)

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "example_app:season"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "example_app:seasonrepresentation-list"

    class Meta:
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")
