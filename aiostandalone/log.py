"""Fake logger configuration"""
from logging import Logger


class FakeLogger(Logger):
    """Fake logger that simply discards all logs"""

    def debug(self, msg, *args, **kwargs):
        """Discard debug messages"""
        pass

    def info(self, msg, *args, **kwargs):
        """Discard info messages"""
        pass

    def warning(self, msg, *args, **kwargs):
        """Discard warning messages"""
        pass

    def error(self, msg, *args, **kwargs):
        """Discard error messages"""
        pass

    def critical(self, msg, *args, **kwargs):
        """Discard critical messages"""
        pass


fake_logger = FakeLogger("FakeLogger")
