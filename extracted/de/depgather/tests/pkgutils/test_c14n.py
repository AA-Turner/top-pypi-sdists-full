from packaging.requirements import Requirement

from depgather.utils import c14n_reqs


def test_c14n_reqs_mutates_names() -> None:
	reqs = [
		Requirement("Requests>=2.0"),
		Requirement("PyTest>=8"),
	]

	out = c14n_reqs(reqs)

	assert all(r.name.islower() for r in out)
	assert len(out) == 2


def test_c14n_reqs_name_deduplication() -> None:
	reqs = [
		Requirement("Requests>=3.0"),
		Requirement("requests>=3.0"),
	]

	out = c14n_reqs(reqs)

	assert len(out) == 1


def test_c14n_reqs_mutates_in_place() -> None:
	r = Requirement("Requests>=2.0")

	c14n_reqs([r])

	assert r.name == "requests"
