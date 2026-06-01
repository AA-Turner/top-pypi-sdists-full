use geographiclib::Geodesic;
use pyo3::prelude::*;
use rayon::prelude::*;

#[pyfunction]
pub fn geodesic(
    latitude_a: f64,
    longitude_a: f64,
    latitude_b: f64,
    longitude_b: f64,
) -> PyResult<f64> {
    let g = Geodesic::wgs84();
    let (_d_deg, d_m, _az1, _az2) = g.inverse(latitude_a, longitude_a, latitude_b, longitude_b);

    Ok(d_m)
}

#[pyfunction]
pub fn batch_geodesic(
    latitude: f64,
    longitude: f64,
    points_of_interest: Vec<(f64, f64)>,
) -> PyResult<Vec<f64>> {
    let g = Geodesic::wgs84();

    let distances: Vec<f64> = points_of_interest
        .into_par_iter()
        .map(|point| {
            let (_d_deg, d_m, _az1, _az2) =g.inverse(latitude, longitude, point.0, point.1);

            return d_m;
        })
        .collect();

    Ok(distances)
}

/// A Python module implemented in Rust.
#[pymodule]
fn fast_geo_distance(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(geodesic, m)?)?;
    m.add_function(wrap_pyfunction!(batch_geodesic, m)?)?;
    Ok(())
}
