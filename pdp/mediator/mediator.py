""" Mediator pattern implementation. """

from pdp.mediator.base_component import BaseComponent


class Mediator:
    """Mediator class."""

    def __init__(self):
        self._components = []

    def add_component(self, component: BaseComponent):
        """Add a component to the mediator.

        :param component: The component to add.
        :type component: BaseComponent
        """
        if not isinstance(component, BaseComponent):
            raise ValueError("Component must be an instance of BaseComponent.")
        self._components.append(component)

    def add_components(self, *components: BaseComponent):
        """Add multiple components to the mediator.

        :param components: The components to add.
        :type components: BaseComponent

        Example:

        mediator = Mediator()
        component_a = ConcreteComponent(name="A", mediator=mediator)
        component_b = ConcreteComponent(name="B", mediator=mediator)
        mediator.add_components(component_a, component_b)
        """
        for component in components:
            self.add_component(component)

    def remove_component(self, component: BaseComponent):
        """Remove a component from the mediator.

        :param component: The component to remove.
        :type component: BaseComponent
        """
        self._components.remove(component)

    def notify(self, sender: BaseComponent, event: dict, **kwargs):
        """Notify all components of an event.

        :param sender: The component sending the notification.
        :type sender: BaseComponent
        :param event: The event to send.
        :type event: dict
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict

        notify_sender (bool): Whether to notify the sender of the event. Default is False. in kwargs
        """
        if sender not in self._components:
            raise ValueError("Component is not registered with the mediator.")
        for component in self._components:
            if component != sender or kwargs.get("notify_sender", False):
                component.on_notify(sender, event, **kwargs)
