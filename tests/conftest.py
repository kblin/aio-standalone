import asyncio
import pytest


@pytest.fixture
def loop():
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    return _loop
