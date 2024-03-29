"""Standalone application class"""
from __future__ import annotations
import asyncio
from asyncio import AbstractEventLoop, CancelledError, Task
from logging import Logger
from typing import Any, Callable, Coroutine, Optional

from .aiosignal import Signal
from .log import fake_logger

AppTask = Callable[["StandaloneApplication"], Coroutine[None, None, None]]


class StandaloneApplication:
    """A standalone async application to run"""

    def __init__(self, *, logger: Logger = fake_logger,
                 loop: Optional[AbstractEventLoop] = None) -> None:
        """Initialize the application to run

        :param logger: The logger class to use
        """
        self.logger = logger

        self._on_startup = Signal(self)
        self._on_shutdown = Signal(self)
        self._on_cleanup = Signal(self)

        self._state: dict[str, Any] = {}
        self._loop = loop
        self._started_tasks: list[Task] = []
        self.tasks: list[AppTask] = []
        self.main_task: Optional[AppTask] = None

    def __getitem__(self, key) -> Any:
        return self._state[key]

    def __setitem__(self, key, value) -> None:
        self._state[key] = value

    @property
    def on_startup(self) -> Signal:
        return self._on_startup

    @property
    def on_shutdown(self) -> Signal:
        return self._on_shutdown

    @property
    def on_cleanup(self) -> Signal:
        return self._on_cleanup

    async def startup(self) -> None:
        """Trigger the startup callbacks"""
        await self.on_startup.send(self)

    async def shutdown(self) -> None:
        """Trigger the shutdown callbacks

        Call this before calling cleanup()
        """
        await self.on_shutdown.send(self)

    async def cleanup(self) -> None:
        """Trigger the cleanup callbacks

        Calls this after calling shutdown()
        """
        await self.on_cleanup.send(self)

    @property
    def loop(self) -> AbstractEventLoop:
        if not self._loop:
            self._loop = asyncio.new_event_loop()
        return self._loop

    def start_task(self, func: AppTask) -> Task:
        """Start up a task"""
        task = self.loop.create_task(func(self))
        self._started_tasks.append(task)

        def done_callback(done_task) -> None:
            self._started_tasks.remove(done_task)

        task.add_done_callback(done_callback)
        return task

    def run(self) -> None:
        """ Actually run the application """
        loop = self.loop
        loop.run_until_complete(self.startup())

        for func in self.tasks:
            self.start_task(func)

        def shutdown_exception_handler(_loop: AbstractEventLoop, context: dict[str, Any]) -> None:
            if "exception" not in context or not isinstance(context["exception"], CancelledError):
                _loop.default_exception_handler(context)
        loop.set_exception_handler(shutdown_exception_handler)

        try:
            assert self.main_task
            task = self.start_task(self.main_task)
            loop.run_until_complete(task)
        except (KeyboardInterrupt, SystemError):
            print("Attempting graceful shutdown, press Ctrl-C again to exit", flush=True)

            tasks = asyncio.gather(*self._started_tasks, return_exceptions=True)
            tasks.add_done_callback(lambda _: loop.stop())
            tasks.cancel()

            while not tasks.done() and not loop.is_closed():
                loop.run_forever()
        finally:
            loop.run_until_complete(self.shutdown())
            loop.run_until_complete(self.cleanup())
            loop.close()
