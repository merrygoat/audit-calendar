from pathlib import Path
from typing import Any, Optional, Callable

from nicegui.element import Element
from nicegui.events import handle_event


class FullCalendar(Element, component='fullcalendar.js'):

    def __init__(self, options: dict[str, Any], on_click: Optional[Callable] = None) -> None:
        """FullCalendar

        An element that integrates the FullCalendar library (https://fullcalendar.io/) to create an interactive calendar
         display.

        :param options: dictionary of FullCalendar properties for customization, such as "initialView",
            "slotMinTime", "slotMaxTime", "allDaySlot", "timeZone", "height", and "events".
        :param on_click: callback that is called when a calendar event is clicked.
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib')
        self._props['options'] = options

        if on_click:
            self.on('click', lambda e: handle_event(on_click, e))

    def add_event(self, event: dict) -> None:
        """Add an event to the calendar.

        :param event: A dictionary of event parameters.
        """
        self._props['options']['events'].append(event)
        self.update()
        self.run_method('update_calendar')

    def remove_event(self, event_id: str, update: bool = True) -> None:
        """Remove an event from the calendar.

        :param event_id: id of the event
        :param update: Whether to run an update of the calendar element.
        """
        for event in self._props['options']['events']:
            if event['id'] == event_id:
                self._props['options']['events'].remove(event)
                break

        if update:
            self.update()
            self.run_method('update_calendar')

    def set_event_start(self, event_id: int, date: str) -> None:
        self.run_method("set_event_start", event_id, date)

    def set_event_props(self, event_id: int, props: dict[str, str]) -> None:
        for name, value in props.items():
            self.run_method("set_event_prop", event_id, name, value)

    def update_event(self, event_id, new_date, new_title):
        self.run_method("update_event", id, new_date, new_title)

    async def get_events(self) -> None:
        """Get a list of all events in the calendar."""
        result = await self.run_method('get_events', timeout=20)
        print(result)

    @property
    def events(self) -> list[dict]:
        """List of events currently displayed in the calendar."""
        return self._props['options']['events']
