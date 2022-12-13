"""Fake tests for the fake logger"""
from aiostandalone.log import FakeLogger, fake_logger


def test_object():
    fake = FakeLogger("Fake")
    fake.debug("Nope")
    fake.info("Nope")
    fake.warning("Nope")
    fake.error("Nope")
    fake.critical("Nope")


def test_instance():
    assert isinstance(fake_logger, FakeLogger)
