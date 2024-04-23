from nicegui import events, ui

from fullcalendar import FullCalendar
from models import db, Event

CURRENT_EVENT_ID = None


def month_view_calendar(events_list: list[Event], ui_elements: dict, classes="") -> FullCalendar:

    events_list = [event.to_dict() for event in events_list]

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
        clicked_event = event.args["info"]["event"]
        ui_elements["title"].set_value(clicked_event["title"])
        ui_elements["date"].set_value(clicked_event["start"])
        ui_elements["status"].set_value(clicked_event["extendedProps"]["status"])
        ui_elements["completed"].set_value(clicked_event["extendedProps"]["completed"])
        if "project" in clicked_event["extendedProps"]:
            ui_elements["project"].set_value(clicked_event["extendedProps"]["project"])
        else:
            ui_elements["project"].set_value("")

        ui_elements["dialog"].open()
        global CURRENT_EVENT_ID
        CURRENT_EVENT_ID = clicked_event["id"]


def handle_update_event(ui_elements: dict):
    if CURRENT_EVENT_ID is None:
        return None
    else:
        new_date = ui_elements["date"].value
        new_title = ui_elements["title"].value
        new_project = ui_elements["project"].value
        new_status = ui_elements["status"].value
        new_completed = ui_elements["completed"].value
        ui_elements["month_calendar"].set_event_start(CURRENT_EVENT_ID, new_date)
        ui_elements["month_calendar"].set_event_props(CURRENT_EVENT_ID, {"title": new_title, "project": new_project,
                                                                         "status": new_status, "completed": new_completed})
        ui_elements["dialog"].close()


def list_view_calendar(events_list: list[Event]):
    events_list = [event.to_dict() for event in events_list]

    options = {
        "initialView": 'listYear',
        "events": events_list,
        'height': 'auto',
    }

    FullCalendar(options)


@ui.page('/')
def main():
    events_query = Event.select()
    events_list = [event for event in events_query]
    projects_list = ["REMORA", "CFHH"]

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

    with ui.dialog() as ui_elements["dialog"], ui.card():
        ui.label("Selected Event Details")
        with ui.grid(columns=2):
            ui.label("Title")
            ui_elements["title"] = ui.input()

            ui.label("Date")
            with ui.input('Date') as ui_elements["date"]:
                with ui_elements["date"].add_slot('append'):
                    ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
                with ui.menu() as menu:
                    ui.date().bind_value(ui_elements["date"])
            ui.label("Project")
            ui_elements["project"] = ui.select(projects_list, value=1, clearable=True, with_input=True)
            ui.label("Status")
            ui_elements["status"] = ui.select(["Scheduled", "Logged"], value="")
            ui.label("Completed")
            ui_elements["completed"] = ui.radio(["Yes", "No"], value="No").props('inline')
            ui.button('Update Event', on_click=lambda: handle_update_event(ui_elements))
            ui.button('Cancel', on_click=lambda: ui_elements["dialog"].close())

    ui.run()

def initialise_db(events_list: list[dict]):
    db.create_tables([Event])

    for event in events_list:
        new_event = Event.create(name=event["name"], description=event["description"], date=event["date"])


main()
