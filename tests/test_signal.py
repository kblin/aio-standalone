"""Test the Signal object"""
from collections import defaultdict
import pytest

from aiostandalone.aiosignal import Signal


def test_init():
    signal = Signal(None)
    assert signal._app is None


def fake_sync_callback(counter):
    counter['fake_sync_callback'] += 1


async def fake_async_callback(counter):
    counter['fake_async_callback'] += 1


@pytest.mark.asyncio
async def test_send():
    counter = defaultdict(int)
    signal = Signal(None)
    signal.append(fake_sync_callback)
    signal.append(fake_async_callback)
    await signal.send(counter)
    assert counter['fake_sync_callback'] == 1
    assert counter['fake_async_callback'] == 1
