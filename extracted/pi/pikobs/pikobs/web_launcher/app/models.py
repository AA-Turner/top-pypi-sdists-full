from __future__ import annotations

from typing import List
import re

from pydantic import BaseModel, Field, field_validator, model_validator

_DATE_RE = re.compile(r'^\d{10}$')


def _clean_scalar(v: str, *, allow_empty: bool = False) -> str:
    value = str(v).strip()
    if not value and not allow_empty:
        raise ValueError('must not be empty')
    if '\n' in value or '\r' in value:
        raise ValueError('newlines are not allowed')
    return value


def _clean_list(values: List[str], *, allow_empty: bool = False) -> List[str]:
    if not values and not allow_empty:
        raise ValueError('at least one selection is required')
    out: list[str] = []
    for value in values:
        value = _clean_scalar(value)
        if value not in out:
            out.append(value)
    return out


class _PeriodMixin(BaseModel):
    datestart: str
    dateend: str
    project_label: str = ''

    @field_validator('project_label')
    @classmethod
    def clean_project_label(cls, v: str) -> str:
        return _clean_scalar(v, allow_empty=True)

    @field_validator('datestart', 'dateend')
    @classmethod
    def valid_date(cls, v: str) -> str:
        value = _clean_scalar(v)
        if not _DATE_RE.match(value):
            raise ValueError('must be YYYYMMDDHH')
        return value


class _ExperienceMixin(_PeriodMixin):
    path_experience_files: List[str] = Field(min_length=1)
    experience_name: List[str] = Field(min_length=1)
    pathwork: str
    region: List[str] = Field(min_length=1)
    family: List[str] = Field(min_length=1)
    flags_criteria: List[str] = Field(min_length=1)
    n_cpus: int = Field(default=80, ge=1, le=256)
    publish: bool = False

    @field_validator('pathwork')
    @classmethod
    def pathwork_required(cls, v: str) -> str:
        return _clean_scalar(v)

    @field_validator(
        'path_experience_files', 'experience_name', 'region', 'family',
        'flags_criteria'
    )
    @classmethod
    def clean_required_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @model_validator(mode='after')
    def matching_experiences(self):
        if len(self.path_experience_files) != len(self.experience_name):
            raise ValueError(
                'path_experience_files and experience_name must have the same number of entries'
            )
        return self


class _OptionalControlMixin(_ExperienceMixin):
    path_control_files: str = ''
    control_name: str = 'control'

    @field_validator('path_control_files')
    @classmethod
    def clean_optional_control(cls, v: str) -> str:
        return _clean_scalar(v, allow_empty=True)

    @field_validator('control_name')
    @classmethod
    def clean_control_name(cls, v: str) -> str:
        return _clean_scalar(v)


class _RequiredControlMixin(_ExperienceMixin):
    path_control_files: str
    control_name: str = 'control'

    @field_validator('path_control_files', 'control_name')
    @classmethod
    def clean_control(cls, v: str) -> str:
        return _clean_scalar(v)


class VdedrRequest(_RequiredControlMixin):
    land_ocean: List[str] = Field(min_length=1)
    special_column: str = 'off'
    id_stn: str = 'all'
    varnos: List[int] = Field(default_factory=list)
    match: str = 'on'
    svg: str = 'off'

    @field_validator('land_ocean')
    @classmethod
    def clean_land(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('special_column', 'id_stn', 'match', 'svg')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)


class CardioRequest(_OptionalControlMixin):
    land_ocean: List[str] = Field(min_length=1)
    special_column: str = 'off'
    id_stn: List[str] = Field(min_length=1)
    channel: List[str] = Field(min_length=1)
    varnos: List[int] = Field(default_factory=list)
    match: str = 'on'
    svg: str = 'off'

    @field_validator('land_ocean', 'id_stn', 'channel')
    @classmethod
    def clean_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('special_column', 'match', 'svg')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)


class ScatterRequest(_OptionalControlMixin):
    land_ocean: List[str] = Field(min_length=1)
    fonction: List[str] = Field(min_length=1)
    boxsizex: float = Field(default=2.0, gt=0)
    boxsizey: float = Field(default=2.0, gt=0)
    projection: List[str] = Field(min_length=1)
    pressure_layers: List[float] = Field(default_factory=list)
    height_layers: List[float] = Field(default_factory=list)
    id_stn: List[str] = Field(min_length=1)
    channel: List[str] = Field(min_length=1)
    points: str = 'OFF'
    special_column: str = 'off'
    varnos: List[int] = Field(default_factory=list)
    match: str = 'on'
    svg: str = 'off'

    @field_validator('land_ocean', 'fonction', 'projection', 'id_stn', 'channel')
    @classmethod
    def clean_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('points', 'special_column', 'match', 'svg')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)


class ZoneRequest(_OptionalControlMixin):
    fonction: List[str] = Field(min_length=1)
    boxsizey: float = Field(default=2.0, gt=0)
    land_ocean: List[str] = Field(min_length=1)
    min_obs: int = Field(default=5, ge=1)
    special_column: str = 'off'
    white_band: float = Field(default=0.1, ge=0)
    id_stn: List[str] = Field(min_length=1)
    channel: List[str] = Field(min_length=1)
    varnos: List[int] = Field(default_factory=list)
    match: str = 'on'
    svg: str = 'off'

    @field_validator('fonction', 'land_ocean', 'id_stn', 'channel')
    @classmethod
    def clean_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('special_column', 'match', 'svg')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)


class TimeserieRequest(_OptionalControlMixin):
    id_stn: List[str] = Field(min_length=1)
    channel: List[str] = Field(min_length=1)
    pressure_layers: List[float] = Field(default_factory=list)
    height_layers: List[float] = Field(default_factory=list)
    land_ocean: List[str] = Field(min_length=1)
    special_column: str = 'off'
    fonction: List[str] = Field(min_length=1)
    match: str = 'on'
    alert_pct: float = Field(default=0.0, ge=0)
    varnos: List[int] = Field(default_factory=list)
    svg: str = 'off'

    @field_validator('id_stn', 'channel', 'land_ocean', 'fonction')
    @classmethod
    def clean_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('special_column', 'match', 'svg')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)


class MapobsRequest(_ExperienceMixin):
    # MAPOBS exposes both the geographic Region and the map Projection in the
    # current Pikobs interface. Keep them independent in the web launcher.
    projection: List[str] = Field(min_length=1)
    land_ocean: List[str] = Field(min_length=1)
    special_column: str = 'off'
    id_stn: List[str] = Field(min_length=1)
    channel: List[str] = Field(min_length=1)
    varnos: List[int] = Field(default_factory=list)
    interval_min: int = Field(default=15, ge=1, le=360)
    panels: List[str] = Field(min_length=1)
    svg: str = 'off'
    dashboard_6h: str = 'auto'

    @field_validator('projection', 'land_ocean', 'id_stn', 'channel', 'panels')
    @classmethod
    def clean_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('special_column', 'svg', 'dashboard_6h')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)


class ObscountdbRequest(_RequiredControlMixin):
    agr: List[str] = Field(default_factory=list)
    svg: str = 'off'

    @field_validator('agr')
    @classmethod
    def clean_optional_agr(cls, values: List[str]) -> List[str]:
        return _clean_list(values, allow_empty=True)

    @field_validator('svg')
    @classmethod
    def clean_svg(cls, v: str) -> str:
        return _clean_scalar(v)

    @model_validator(mode='after')
    def one_experience_only(self):
        if len(self.path_experience_files) != 1:
            raise ValueError('OBSCOUNTDB requires exactly one experience path')
        if len(self.experience_name) != 1:
            raise ValueError('OBSCOUNTDB requires exactly one experience name')
        return self


class FlagsRequest(_PeriodMixin):
    path_experience_files: List[str] = Field(min_length=1)
    experience_name: List[str] = Field(min_length=1)
    pathwork: str
    region: List[str] = Field(min_length=1)
    family: List[str] = Field(min_length=1)
    land_ocean: List[str] = Field(min_length=1)
    special_column: str = 'off'
    id_stn: List[str] = Field(min_length=1)
    channel: List[str] = Field(min_length=1)
    pressure_layers: List[float] = Field(default_factory=list)
    height_layers: List[float] = Field(default_factory=list)
    varnos: List[int] = Field(default_factory=list)
    svg: str = 'off'
    n_cpus: int = Field(default=80, ge=1, le=256)
    publish: bool = False

    @field_validator('pathwork')
    @classmethod
    def pathwork_required(cls, v: str) -> str:
        return _clean_scalar(v)

    @field_validator('path_experience_files', 'experience_name', 'region', 'family', 'land_ocean', 'id_stn', 'channel')
    @classmethod
    def clean_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('special_column', 'svg')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)

    @model_validator(mode='after')
    def matching_experiences(self):
        if len(self.path_experience_files) != len(self.experience_name):
            raise ValueError('path_experience_files and experience_name must have the same number of entries')
        return self


class ProfileRequest(_OptionalControlMixin):
    land_ocean: List[str] = Field(min_length=1)
    special_column: str = 'off'
    fonction: List[str] = Field(min_length=1)
    min_obs: int = Field(default=30, ge=1)
    obs_error_model: str = 'off'
    fit_radar: str = 'off'
    fit_radar_target: str = 'desroziers'
    error_curves: List[str] = Field(default_factory=list)
    id_stn: List[str] = Field(min_length=1)
    varnos: List[int] = Field(default_factory=list)
    match: str = 'on'
    svg: str = 'off'

    @field_validator('land_ocean', 'fonction', 'id_stn')
    @classmethod
    def clean_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('error_curves')
    @classmethod
    def clean_optional_list(cls, values: List[str]) -> List[str]:
        return _clean_list(values, allow_empty=True)

    @field_validator('special_column', 'obs_error_model', 'fit_radar', 'fit_radar_target', 'match', 'svg')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)


class VerifprofileRequest(_OptionalControlMixin):
    fonction: List[str] = Field(min_length=1)
    land_ocean: List[str] = Field(min_length=1)
    min_obs: int = Field(default=30, ge=1)
    ratio_figure: str = 'off'
    special_column: str = 'off'
    id_stn: List[str] = Field(min_length=1)
    varnos: List[int] = Field(default_factory=list)
    match: str = 'on'
    svg: str = 'off'

    @field_validator('fonction', 'land_ocean', 'id_stn')
    @classmethod
    def clean_lists(cls, values: List[str]) -> List[str]:
        return _clean_list(values)

    @field_validator('ratio_figure', 'special_column', 'match', 'svg')
    @classmethod
    def clean_scalars(cls, v: str) -> str:
        return _clean_scalar(v)


REQUEST_MODELS = {
    'vdedr': VdedrRequest,
    'cardio': CardioRequest,
    'scatter': ScatterRequest,
    'zone': ZoneRequest,
    'timeserie': TimeserieRequest,
    'mapobs': MapobsRequest,
    'obscountdb': ObscountdbRequest,
    'flags': FlagsRequest,
    'profile': ProfileRequest,
    'verifprofile': VerifprofileRequest,
}
