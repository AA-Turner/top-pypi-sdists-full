import pytest

pd = pytest.importorskip("pandas")

from flowtask.components.MarketClustering import MarketClustering


def test_rebalance_removes_store_when_constraints_violated(monkeypatch):
    component = MarketClustering(use_fte_constraints=True, day_hours=8, max_stores_per_day=3)

    data = pd.DataFrame(
        {
            'store_id': [1, 2, 3],
            'latitude': [0.0, 0.05, 1.0],
            'longitude': [0.0, 0.05, 0.0],
            component._cluster_id: [0, 0, 0],
        }
    )

    component._data = data.copy()
    component._rejected = pd.DataFrame()
    component._cluster_centroids = {
        0: {
            'centroid_lat': float(data['latitude'].mean()),
            'centroid_lon': float(data['longitude'].mean()),
        }
    }

    def fake_recompute():
        cluster_df = component._data[component._data[component._cluster_id] == 0]
        if len(cluster_df) > 2:
            component._cluster_fte_info = {
                0: {
                    'constraint_warning': 'monthly_hours_outside_tolerance',
                    'daily_hours_per_employee': 10.0,
                    'stores_per_employee': 5.0,
                }
            }
        else:
            component._cluster_fte_info = {
                0: {
                    'constraint_warning': None,
                    'daily_hours_per_employee': 6.0,
                    'stores_per_employee': 2.0,
                }
            }

    monkeypatch.setattr(component, "_recompute_cluster_fte_info", fake_recompute)

    component._rebalance_clusters_for_fte_constraints()

    assert len(component._data) == 2
    assert component._rejected['store_id'].tolist() == [3]
    assert component._rejected['constraint_reason'].iloc[0] == 'fte_constraint_violation'
    assert component._cluster_satisfies_constraints(component._cluster_fte_info[0])
