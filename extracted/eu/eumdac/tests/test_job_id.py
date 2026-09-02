import pytest
from eumdac.job_id import JobIdentifier, JobIdError


def test_register():
    uut = JobIdentifier(3)

    uut.register("a")
    assert 1 == len(uut.registered_objects)
    uut.register("b")
    assert 2 == len(uut.registered_objects)
    uut.register("c")
    assert 3 == len(uut.registered_objects)


def test_register_raise_register_same_object_twice():
    uut = JobIdentifier(3)
    uut.register("a")
    with pytest.raises(JobIdError) as exc_info:
        uut.register("a")
    assert str(exc_info.value) == "Object 'a' already registered."


def test_total_jobs_exceed():
    uut = JobIdentifier(1)
    uut.register("a")
    with pytest.raises(JobIdError) as exc_info:
        uut.register("b")
    assert (
        str(exc_info.value) == "Too many Job IDs requested. Expected a maximum of 1 Job ID requests"
    )


def test_job_id_tuple():
    uut = JobIdentifier(1)
    uut.register("a")
    out = uut.job_id_tuple("a")
    assert out[0] == 1


def test_request_non_existent_object():
    uut = JobIdentifier(1)
    uut.register("a")
    with pytest.raises(JobIdError) as exc_info:
        uut.job_id_tuple("b")
    assert str(exc_info.value) == "No Job ID for 'b'. Available ones: ['a']"
