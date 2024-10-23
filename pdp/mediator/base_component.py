""" Base class for all components in the mediator pattern. """

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pdp.mediator.mediator import Mediator


class BaseComponent(ABC):
    """Base class for all components in the mediator pattern."""

    def __init__(self, name: str, mediator: "Mediator") -> None:
        self.mediator = mediator
        self.name = name

    @abstractmethod
    def on_notify(self, sender: "BaseComponent", event: dict, *args, **kwargs) -> None:
        """Handle notifications from other components.

        :param sender: The component that sent the notification.
        :type sender: BaseComponent
        :param event: The event that was sent.
        :type event: dict
        :param args: Additional arguments.
        :type args: tuple
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        raise NotImplementedError

    def notify(self, event: dict, **kwargs) -> None:
        """Notify all components with the given event.

        :param event: The event to send.
        :type event: dict
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        self.mediator.notify(self, event, **kwargs)
