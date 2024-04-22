from datetime import datetime

from nicegui import events, ui

from fullcalendar import FullCalendar
from models import db, Event

CURRENT_EVENT_ID = None


def month_view_calendar(events_list: list[dict], ui_elements: dict,
                        classes="") -> FullCalendar:

    options = {
        'initialView': 'dayGridMonth',
        'headerToolbar': {'left': 'title', 'right': ''},
        'footerToolbar': {'right': 'prev,next today'},
        'allDaySlot': True,
        'timeZone': 'local',
        'height': 'auto',
        'events': events_list,
    }

    month_calendar = FullCalendar(options, on_click=lambda e: handle_event_click(e, ui_elements)).classes(classes)
    return month_calendar


def handle_event_click(event: events.GenericEventArguments, ui_elements: dict):
    if 'info' in event.args:
        calendar_instance = event.sender
        clicked_event = event.args["info"]["event"]
        ui_elements["title"].set_value(clicked_event["title"])
        ui_elements["date"].set_value(clicked_event["start"])

        global CURRENT_EVENT_ID
        if CURRENT_EVENT_ID is not None:
            calendar_instance.set_event_props(CURRENT_EVENT_ID, {"backgroundColor": "#3788d8",
                                                                 "borderColor": "#3788d8"})
        CURRENT_EVENT_ID = clicked_event["id"]
        calendar_instance.set_event_props(CURRENT_EVENT_ID, {"backgroundColor": "red",
                                                             "borderColor": "red"})


def handle_update_event(ui_elements: dict):
    if CURRENT_EVENT_ID is None:
        return None
    else:
        new_date = ui_elements["date"].value
        new_title = ui_elements["title"].value
        ui_elements["month_calendar"].set_event_start(CURRENT_EVENT_ID, new_date)
        ui_elements["month_calendar"].set_event_props(CURRENT_EVENT_ID, {"title": new_title})



def list_view_calendar(events_list: list[dict]):
    options = {
        "initialView": 'listYear',
        "events": events_list,
        'height': 'auto',
    }

    FullCalendar(options)


@ui.page('/')
def main():
    events_list = [
        {"id": 1, "title": "Rotate keys", "description": "Rotate keys for REMORA", "date": datetime(2024, 4, 20).isoformat(), 'allDay': 'true'},
        {"id": 2, "title": "Check EC2", "description": "Check the EC2 instances for bugs", "date": datetime(2024, 4, 23).isoformat(), 'allDay': 'true'},
        {"id": 3, "title": "Rebuild instances", "description": "Rebuild and redeploy EC2 instances", "date": datetime(2024, 4, 25).isoformat(), 'allDay': 'true'}
        ]

    ui_elements = {}

    with ui.row().classes('w-full no-wrap'):
        with ui.column().classes('w-1/2'):
            with ui.tabs().classes('w-full') as tabs:
                one = ui.tab('Month View')
                two = ui.tab('List View')
            with ui.tab_panels(tabs, value=one).classes():
                with ui.tab_panel(one):
                    ui_elements["month_calendar"] = month_view_calendar(events_list, ui_elements)
                with ui.tab_panel(two):
                    list_view_calendar(events_list)

        with ui.column().classes('w-1/2'):
            ui.label("Selected Event Details")
            with ui.grid(columns=2).classes('w-1/2'):
                ui.label("Title")
                ui_elements["title"] = ui.input()

                ui.label("Date")
                with ui.input('Date') as ui_elements["date"]:
                    with ui_elements["date"].add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
                    with ui.menu() as menu:
                        ui.date().bind_value(ui_elements["date"])
                ui.button('Update Event', on_click=lambda: handle_update_event(ui_elements))

    ui.run()


def initialise_db(events_list: list[dict]):
    db.create_tables([Event])

    for event in events_list:
        new_event = Event.create(name=event["name"], description=event["description"], date=event["date"])


main()
