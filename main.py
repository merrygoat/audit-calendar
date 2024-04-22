from datetime import datetime

import nicegui.elements.input
from nicegui import events, ui

from fullcalendar import FullCalendar
from models import db, Event

CURRENT_EVENT = ""


def month_view_calendar(events_list: list[dict], ui_elements: dict[str, nicegui.elements.input.Input],
                        classes="") -> FullCalendar:
    def handle_click(event: events.GenericEventArguments, ui_elements: dict[str, nicegui.elements.input.Input]):
        ui_elements["title"].set_value(event.args["info"]["event"]["title"])
        ui_elements["date"].set_value(event.args["info"]["event"]["start"])
        global CURRENT_EVENT
        CURRENT_EVENT = event.args["info"]["event"]

    options = {
        'initialView': 'dayGridMonth',
        'headerToolbar': {'left': 'title', 'right': ''},
        'footerToolbar': {'right': 'prev,next today'},
        'allDaySlot': True,
        'timeZone': 'local',
        'height': 'auto',
        'events': events_list,
    }

    month_calendar = FullCalendar(options, on_click=lambda e: handle_click(e, ui_elements)).classes(classes)
    return month_calendar


def list_view_calendar(events_list: list[dict]):
    options = {
        "initialView": 'listYear',
        "events": events_list,
        'height': 'auto',
    }

    FullCalendar(options)


def main():
    events_list = [
        {"title": "Rotate keys", "description": "Rotate keys for REMORA", "date": datetime(2024, 4, 20).isoformat(), 'allDay': 'true'},
        {"title": "Check EC2", "description": "Check the EC2 instances for bugs", "date": datetime(2024, 4, 23).isoformat(), 'allDay': 'true'},
        {"title": "Rebuild instances", "description": "Rebuild and redeploy EC2 instances", "date": datetime(2024, 4, 25).isoformat(), 'allDay': 'true'}
        ]

    ui_elements = {}
    current_event = {}

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
                ui.button('Update Event', on_click=lambda: ui.notify('You clicked me!'))

    ui.run()


def initialise_db(events_list: list[dict]):
    db.create_tables([Event])

    for event in events_list:
        new_event = Event.create(name=event["name"], description=event["description"], date=event["date"])


main()
