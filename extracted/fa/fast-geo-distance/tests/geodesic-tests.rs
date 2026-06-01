use pyo3::prelude::*;
use fast_geo_distance::geodesic;
use fast_geo_distance::batch_geodesic;


#[cfg(test)]
mod tests {
    use crate::*;

    const LATITUDE_BERLIN: f64 = 52.518992275104445;
    const LONGITUDE_BERLIN: f64 = 13.404800164623978;
    const LATITUDE_MUNICH: f64 = 48.140313048369265;
    const LONGITUDE_MUNICH: f64 = 11.563939007231188;
    const LATITUDE_NEW_YORK: f64 = 40.657439489432036;
    const LONGITUDE_NEW_YORK: f64 = -73.94123044208536;
    const LATITUDE_TOKIO: f64 = 35.6899224389031;
    const LONGITUDE_TOKIO: f64 = 139.66391017186552;
    const LATITUDE_CAPE_TOWN: f64 = -33.97404971258781;
    const LONGITUDE_CAPE_TOWN: f64 = 18.557786310359266;
    const LATITUDE_SHANGHAI: f64 = 31.091132143208924;
    const LONGITUDE_SHANGHAI: f64 = 121.46984034713057;
    const LATITUDE_MELBOURNE: f64 = -37.79549518995617;
    const LONGITUDE_MELBOURNE: f64 = 144.98909973260731;

    const DISTANCE_BERLIN_MUNICH: f64 = 504347.652400197;
    const DISTANCE_NEW_YORK_TOKIO: f64 = 10881784.370794715;
    const DISTANCE_SHANGHAI_MELBOURN: f64 = 8008368.494128224;
    const DISTANCE_BERLIN_CAPE_TOWN: f64 = 9594984.883884624;

    #[test]
    fn test_berlin_munich() {
        let distance: PyResult<f64> = geodesic(
            LATITUDE_BERLIN,
            LONGITUDE_BERLIN,
            LATITUDE_MUNICH,
            LONGITUDE_MUNICH,
        );

        assert!(distance.is_ok());
        assert_eq!(distance.unwrap(), DISTANCE_BERLIN_MUNICH);
    }

    #[test]
    fn test_new_york_tokio() {
        let distance: PyResult<f64> = geodesic(
            LATITUDE_NEW_YORK,
            LONGITUDE_NEW_YORK,
            LATITUDE_TOKIO,
            LONGITUDE_TOKIO,
        );

        assert!(distance.is_ok());
        assert_eq!(distance.unwrap(), DISTANCE_NEW_YORK_TOKIO);
    }

    #[test]
    fn test_berlin_cape_town() {
        let distance: PyResult<f64> = geodesic(
            LATITUDE_BERLIN,
            LONGITUDE_BERLIN,
            LATITUDE_CAPE_TOWN,
            LONGITUDE_CAPE_TOWN,
        );

        assert!(distance.is_ok());
        assert_eq!(distance.unwrap(), DISTANCE_BERLIN_CAPE_TOWN);
    }

    #[test]
    fn test_shanghai_melbourne() {
        let distance: PyResult<f64> = geodesic(
            LATITUDE_SHANGHAI,
            LONGITUDE_SHANGHAI,
            LATITUDE_MELBOURNE,
            LONGITUDE_MELBOURNE,
        );

        assert!(distance.is_ok());
        assert_eq!(distance.unwrap(), DISTANCE_SHANGHAI_MELBOURN);
    }

    #[test]
    fn test_batch_distance() {
        let points_of_interest: Vec<(f64, f64)> = vec![
            (LATITUDE_MUNICH, LONGITUDE_MUNICH),
            (LATITUDE_NEW_YORK, LONGITUDE_NEW_YORK),
            (LATITUDE_SHANGHAI, LONGITUDE_SHANGHAI),
            (LATITUDE_TOKIO, LONGITUDE_TOKIO),
            (LATITUDE_CAPE_TOWN, LONGITUDE_CAPE_TOWN),
            (LATITUDE_MELBOURNE, LONGITUDE_MELBOURNE),
        ];

        let distances: PyResult<Vec<f64>> =
            batch_geodesic(LATITUDE_BERLIN, LONGITUDE_BERLIN, points_of_interest);

        assert!(distances.is_ok());
        assert_eq!(distances.unwrap()[0], DISTANCE_BERLIN_MUNICH);
    }
}
