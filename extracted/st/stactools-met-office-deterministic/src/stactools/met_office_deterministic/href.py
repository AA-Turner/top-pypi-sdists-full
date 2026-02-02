"""Parse Met Office deterministic forecast hrefs into structured objects."""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass

from .constants import Model, Theme

PATH_REGEX = re.compile(
    r"^.*/(?P<collection>[^/]+)/(?P<reference_datetime>[^/]+)/(?P<valid_datetime>[^-]+)-(?P<forecast_horizon>[^-]+)-(?P<parameter>.+)\.nc$"
)


@dataclass(frozen=True)
class Href:
    href: str
    model: Model
    theme: Theme
    parameter: str
    reference_datetime: str
    valid_datetime: str
    forecast_horizon: str

    @classmethod
    def parse(
        cls, href: str, model: Model | None = None, theme: Theme | None = None
    ) -> Href:
        matches = PATH_REGEX.match(href)
        if matches is None:
            raise ValueError(f"Invalid file name: {href}")
        if model is None:
            match collection := matches["collection"]:
                case "global-deterministic-10km":
                    model = Model.global_
                case "uk-deterministic-2km":
                    model = Model.uk
                case _:
                    raise ValueError(f"Invalid collection: {collection}")
        parameter = matches["parameter"]
        if theme is None:
            theme = Theme.from_parameter(parameter)
        return Href(
            href=href,
            model=model,
            theme=theme,
            parameter=parameter,
            reference_datetime=matches["reference_datetime"],
            valid_datetime=matches["valid_datetime"],
            forecast_horizon=matches["forecast_horizon"],
        )

    @property
    def collection_id(self) -> str:
        """Gets the STAC collection ID for this href.

        Returns:
            The collection ID string.
        """
        return self.model.get_collection_id(self.theme)

    @property
    def item_id(self) -> str:
        """Gets the STAC item ID for this href."""
        return f"{self.reference_datetime}-{self.valid_datetime}"

    @property
    def datetime(self) -> datetime.datetime:
        """Gets the datetime from the valid time string.

        Returns:
            A datetime object parsed from the valid time.
        """
        return datetime.datetime.strptime(self.valid_datetime, "%Y%m%dT%H%MZ")

    @property
    def duration(self) -> str | None:
        """Extracts the duration from the parameter if present.

        Returns:
            The duration string (ISO 8601 format) if the parameter includes one,
            None otherwise.
        """
        parts = self.parameter.split("-")
        if len(parts) == 2:
            assert parts[1].startswith("PT")
            return parts[1]
        else:
            return None

    @property
    def variable(self) -> str | None:
        """The CF-standard name for this parameter."""
        match self.parameter:
            case "cloud_amount_of_total_cloud":
                return "cloud_area_fraction"
            case "cloud_amount_of_high_cloud":
                return "high_type_cloud_area_fraction"
            case "cloud_amount_of_medium_cloud":
                return "medium_type_cloud_area_fraction"
            case "cloud_amount_of_low_cloud":
                return "low_type_cloud_area_fraction"
            case "cloud_amount_below_1000ft_ASL":
                return "cloud_area_fraction_assuming_only_consider_surface_to_1000_feet_asl"  # noqa: E501
            case "cloud_amount_on_height_levels":
                return "cloud_volume_fraction_in_atmosphere_layer"
            case "height_AGL_at_cloud_base_where_cloud_cover_2p5_oktas":
                return "cloud_base_height_2p5_oktas"
            case "cloud_amount_of_total_convective_cloud":
                return "convective_cloud_area_fraction"
            case "fog_fraction_at_screen_level":
                return "fog_area_fraction"
            case "visibility_at_screen_level":
                return "visibility_in_air"
            case "pressure_at_mean_sea_level":
                return "air_pressure_at_sea_level"
            case "pressure_at_surface":
                return "surface_air_pressure"
            case "height_ASL_on_pressure_levels":
                return "geopotential_height"
            case "pressure_at_tropopause":
                return "tropopause_air_pressure"
            case "precipitation_rate":
                return "lwe_precipitation_rate"
            case (
                "precipitation_accumulation-PT01H"
                | "precipitation_accumulation-PT03H"
                | "precipitation_accumulation-PT06H"
            ):
                return "lwe_thickness_of_precipitation_amount"
            case (
                "rainfall_accumulation-PT01H"
                | "rainfall_accumulation-PT03H"
                | "rainfall_accumulation-PT06H"
            ):
                return "thickness_of_rainfall_amount"
            case "rainfall_rate":
                return "rainfall_rate"
            case (
                "rainfall_rate_from_convection"
                | "rainfall_rate_from_convection_max-PT01H"
                | "rainfall_rate_from_convection_max-PT03H"
                | "rainfall_rate_from_convection_max-PT06H"
            ):
                return "convective_rainfall_rate"
            case "radiation_flux_in_uv_downward_at_surface":
                return "surface_downwelling_ultraviolet_flux_in_air"
            case "radiation_flux_in_longwave_downward_at_surface":
                return "surface_downwelling_longwave_flux_in_air"
            case "radiation_flux_in_shortwave_direct_downward_at_surface":
                return "surface_direct_downwelling_shortwave_flux_in_air"
            case "radiation_flux_in_shortwave_total_downward_at_surface":
                return "surface_downwelling_shortwave_flux_in_air"
            case "radiation_flux_in_shortwave_diffuse_downward_at_surface":
                return "surface_diffusive_downwelling_shortwave_flux_in_air"
            case "snow_depth_water_equivalent":
                return "lwe_thickness_of_surface_snow_amount"
            case "snowfall_rate":
                return "lwe_snowfall_rate"
            case "snowfall_accumulation-PT01H" | "snowfall_accumulation-PT03H":
                return "lwe_thickness_of_snowfall_amount"
            case (
                "snowfall_rate_from_convection"
                | "snowfall_rate_from_convection_mean-PT01H"
                | "snowfall_rate_from_convection_mean-PT03H"
                | "snowfall_rate_from_convection_mean-PT06H"
                | "snowfall_rate_from_convection_max-PT01H"
                | "snowfall_rate_from_convection_max-PT03H"
                | "snowfall_rate_from_convection_max-PT06H"
            ):
                return "lwe_convective_snowfall_rate"
            case "hail_fall_rate":
                return "lwe_graupel_and_hail_fall_rate"
            case "hail_fall_accumulation-PT01H":
                return "lwe_thickness_of_graupel_and_hail_fall_amount"
            case "lightning_flash_accumulation-PT01H":
                return "number_of_lightning_flashes_per_unit_area"
            case (
                "temperature_at_screen_level"
                | "temperature_at_screen_level_max-PT01H"
                | "temperature_at_screen_level_max-PT03H"
                | "temperature_at_screen_level_max-PT06H"
                | "temperature_at_screen_level_min-PT01H"
                | "temperature_at_screen_level_min-PT03H"
                | "temperature_at_screen_level_min-PT06H"
                | "temperature_on_pressure_levels"
                | "temperature_on_height_levels"
            ):
                return "air_temperature"
            case "temperature_at_surface":
                return "surface_temperature"
            case "temperature_at_tropopause":
                return "tropopause_air_temperature"
            case "temperature_of_dew_point_at_screen_level":
                return "dew_point_temperature"
            case "wet_bulb_potential_temperature_on_pressure_levels":
                return "wet_bulb_potential_temperature"
            case (
                "wind_direction_at_10m"
                | "wind_direction_on_pressure_levels"
                | "wind_direction_on_height_levels"
            ):
                return "wind_from_direction"
            case (
                "wind_speed_at_10m"
                | "wind_speed_on_pressure_levels"
                | "wind_speed_on_height_levels"
            ):
                return "wind_speed"
            case (
                "wind_gust_at_10m"
                | "wind_gust_at_10m_max-PT01H"
                | "wind_gust_at_10m_max-PT03H"
                | "wind_gust_at_10m_max-PT06H"
            ):
                return "wind_speed_of_gust"
            case "wind_vertical_velocity_on_pressure_levels":
                return "upward_air_velocity"
            case "CAPE_most_unstable_below_500hPa" | "CAPE_mixed_layer_lowest_500m":
                return "atmosphere_convective_available_potential_energy"
            case "CAPE_surface":
                return "atmosphere_convective_available_potential_energy_wrt_surface"
            case "CIN_surface":
                return "atmosphere_convective_inhibition_wrt_surface"
            case "CIN_mixed_layer_lowest_500m" | "CIN_most_unstable_below_500hPa":
                return "atmosphere_convective_inhibition"
            case "sensible_heat_flux_at_surface":
                return "surface_upward_sensible_heat_flux"
            case (
                "latent_heat_flux_at_surface_mean-PT01H"
                | "latent_heat_flux_at_surface_mean-PT03H"
                | "latent_heat_flux_at_surface_mean-PT06H"
            ):
                return "surface_upward_latent_heat_flux"
            case (
                "relative_humidity_at_screen_level"
                | "relative_humidity_on_pressure_levels"
            ):
                return "relative_humidity"
            case "height_AGL_at_wet_bulb_freezing_level":
                return "wet_bulb_freezing_level_height"
            case "height_AGL_at_freezing_level":
                return "freezing_level_height"
            case "landsea_mask":
                return "land_binary_mask"
            case _:
                return None

    def __str__(self) -> str:
        """Returns the href as a string.

        Returns:
            The href string.
        """
        return self.href
