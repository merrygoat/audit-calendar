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

    def add_event(self, title: str, start: str, end: str, **kwargs) -> None:
        """Add an event to the calendar.

        :param title: title of the event
        :param start: start time of the event
        :param end: end time of the event
        """
        event_dict = {'title': title, 'start': start, 'end': end, **kwargs}
        self._props['options']['events'].append(event_dict)
        self.update()
        self.run_method('update_calendar')

    def remove_event(self, title: str, start: str, end: str) -> None:
        """Remove an event from the calendar.

        :param title: title of the event
        :param start: start time of the event
        :param end: end time of the event
        """
        for event in self._props['options']['events']:
            if event['title'] == title and event['start'] == start and event['end'] == end:
                self._props['options']['events'].remove(event)
                break

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
