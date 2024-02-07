from abc import ABC, abstractmethod
from typing import Any

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.logger import Logger


class SimpleTask(ABC):
    """Simple Twisted Looping Call abstract base class."""

    INTERVAL = NotImplemented
    CLOCK = reactor

    def __init__(self, interval: float = INTERVAL):
        self.interval = interval
        self.log = Logger(self.__class__.__name__)
        self._task = LoopingCall(self.run)
        self._task.clock = self.CLOCK
        self._task.interval = self.interval

    @property
    def running(self) -> bool:
        """Determine whether the task is already running."""
        return self._task.running

    def start(self, now: bool = False):
        """Start task."""
        if not self.running:
            d = self._task.start(interval=self.interval, now=now)
            d.addErrback(self.handle_errors)
            return d

    def stop(self):
        """Stop task."""
        if self.running:
            self._task.stop()

    @abstractmethod
    def run(self):
        """Task method that should be periodically run."""
        raise NotImplementedError

    @abstractmethod
    def handle_errors(self, *args, **kwargs) -> Any:
        """Error callback for error handling during execution."""
        raise NotImplementedError