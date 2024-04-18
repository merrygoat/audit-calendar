from datetime import datetime

from nicegui import events, ui

from fullcalendar import FullCalendar
from models import db, Event


def month_view_calendar(events_list: list[dict], classes=""):
    def handle_click(event: events.GenericEventArguments):
        if 'info' in event.args:
            ui.notify(event.args['info']['event'])

    options = {
        'initialView': 'dayGridMonth',
        'headerToolbar': {'left': 'title', 'right': ''},
        'footerToolbar': {'right': 'prev,next today'},
        'allDaySlot': True,
        'timeZone': 'local',
        'height': 'auto',
        'events': events_list,
    }

    FullCalendar(options, on_click=handle_click).classes(classes)


def list_view_calendar(events_list: list[dict]):
    options = {
        "initialView": 'listYear',
        "events": events_list,
        'height': 'auto',
    }

    FullCalendar(options)


def main():
    # initialise_db()
    # events_list = [{"title": event.name, "start": event.date.isoformat(), "allDay": "true"} for event in Event.select()]
    events_list = [
        {"title": "Rotate keys", "description": "Rotate keys for REMORA", "date": datetime(2024, 4, 20).isoformat(), 'allDay': 'true'},
        {"title": "Check EC2", "description": "Check the EC2 instances for bugs", "date": datetime(2024, 4, 23).isoformat(), 'allDay': 'true'},
        {"title": "Rebuild instances", "description": "Rebuild and redeploy EC2 instances", "date": datetime(2024, 4, 25).isoformat(), 'allDay': 'true'}
        ]

    with ui.row().classes('w-full no-wrap'):
        month_view_calendar(events_list, 'w-2/3')
            # with ui.tabs().classes('w-full') as tabs:
            #     ui.label("Calendar View")
            #     one = ui.tab('Month View')
            #     two = ui.tab('List View')
            # with ui.tab_panels(tabs, value=one).classes('w-full'):
            #     with ui.tab_panel(one):
            #         month_view_calendar(events_list)
            #     with ui.tab_panel(two):
            #         list_view_calendar(events_list)
        ui.label("Select Event Details").classes('w-1/3')

    ui.run()


def initialise_db():
    db.create_tables([Event])
    events_list = [
        {"title": "Rotate keys", "description": "Rotate keys for REMORA", "date": datetime(2024, 4, 20).isoformat(), 'allDay': 'true'},
        {"title": "Check EC2", "description": "Check the EC2 instances for bugs", "date": datetime(2024, 4, 23).isoformat(), 'allDay': 'true'},
        {"title": "Rebuild instances", "description": "Rebuild and redeploy EC2 instances", "date": datetime(2024, 4, 25).isoformat(), 'allDay': 'true'}
        ]

    for event in events_list:
        new_event = Event.create(name=event["name"], description=event["description"], date=event["date"])


main()
