"""Test the standalone application"""
import asyncio
import pytest
from aiostandalone.app import StandaloneApplication


def test_init():
    app = StandaloneApplication()
    app['fake'] = 'totally'
    assert app['fake'] == 'totally'


def fake_startup(app):
    app['ran_startup'] = True


def fake_cleanup(app):
    app['ran_cleanup'] = True


def fake_shutdown(app):
    app['ran_shutdown'] = True


async def fake_side_task(app):
    await asyncio.sleep(0.01)
    app['ran_side_task'] = True


async def fake_main_task(app):
    await asyncio.sleep(0.01)
    app['ran_main_task'] = True


def test_run(loop):
    app = StandaloneApplication()

    app.on_startup.append(fake_startup)
    app.on_shutdown.append(fake_shutdown)
    app.on_cleanup.append(fake_cleanup)
    app.tasks.append(fake_side_task)
    app.main_task = fake_main_task

    app.run()

    assert app['ran_startup']
    assert app['ran_shutdown']
    assert app['ran_cleanup']
    assert app['ran_side_task']
    assert app['ran_main_task']


def test_loop():
    loop = asyncio.get_event_loop()
    app = StandaloneApplication()
    app.loop = loop

    assert app._loop == loop

    app.loop = None

    with pytest.raises(RuntimeError):
        app.loop = 23


async def fake_failing_task(_):
    await asyncio.sleep(0.01)
    raise SystemError


async def long_running_side_task(_):
    await asyncio.sleep(1)


def test_abort(loop):
    app = StandaloneApplication()
    app.on_startup.append(fake_startup)
    app.on_shutdown.append(fake_shutdown)
    app.on_cleanup.append(fake_cleanup)

    app.main_task = fake_failing_task
    app.tasks.append(long_running_side_task)

    app.run(loop)
    assert app['ran_shutdown']
    assert app['ran_cleanup']
