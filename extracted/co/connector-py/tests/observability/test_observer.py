from connector.observability.observer import DagsterObservations, Observer


class TestObserver:
    def test_observe_total(self):
        dagster: DagsterObservations = {"run_id": "4823904"}
        assert not Observer.observed()

        with Observer.observe({"flows_v2_execution_id": "24", "dagster": dagster}):
            assert Observer.observed() == {
                "flows_v2_execution_id": "24",
                "dagster": dagster,
            }

        assert not Observer.observed()

    def test_observe_partial(self):
        assert not Observer.observed()

        with Observer.observe(
            {
                "flows_v2_execution_id": "24",
            }
        ):
            assert Observer.observed() == {"flows_v2_execution_id": "24"}

        assert not Observer.observed()

    def test_observe_partial_nested(self):
        dagster: DagsterObservations = {"run_id": "4823904"}

        assert not Observer.observed()

        with Observer.observe(
            {
                "flows_v2_execution_id": "24",
            }
        ):
            assert Observer.observed() == {"flows_v2_execution_id": "24"}

            with Observer.observe({"dagster": dagster}):
                assert Observer.observed() == {
                    "flows_v2_execution_id": "24",
                    "dagster": dagster,
                }

            assert Observer.observed() == {"flows_v2_execution_id": "24"}

        assert not Observer.observed()

    def test_observe_total_nested(self):
        dagster: DagsterObservations = {"run_id": "4823904"}

        assert not Observer.observed()

        with Observer.observe({"flows_v2_execution_id": "24", "dagster": dagster}):
            assert Observer.observed() == {
                "flows_v2_execution_id": "24",
                "dagster": dagster,
            }

            with Observer.observe(
                {"flows_v2_execution_id": "override", "dagster": {"run_id": "override"}}
            ):
                assert Observer.observed() == {
                    "flows_v2_execution_id": "override",
                    "dagster": {"run_id": "override"},
                }

            assert Observer.observed() == {
                "flows_v2_execution_id": "24",
                "dagster": dagster,
            }

        assert not Observer.observed()

    def test_observe_resets_with_exception(self):
        assert not Observer.observed()

        try:
            with Observer.observe(
                {
                    "flows_v2_execution_id": "24",
                }
            ):
                assert Observer.observed() == {"flows_v2_execution_id": "24"}
                raise Exception("Howdy")
        except Exception:
            pass

        assert not Observer.observed()
