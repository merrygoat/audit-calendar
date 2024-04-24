import nicegui.elements.switch
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
    extended_props = ["status", "completed", "project"]

    if 'info' in event.args:
        clicked_event = event.args["info"]["event"]
        ui_elements["title"].set_value(clicked_event["title"])
        ui_elements["date"].set_value(clicked_event["start"])
        for prop in extended_props:
            ui_elements[prop].set_value(clicked_event["extendedProps"][prop])

        ui_elements["dialog"].open()
        global CURRENT_EVENT_ID
        CURRENT_EVENT_ID = clicked_event["id"]


def handle_update_event(ui_elements: dict):
    props = ["title", "project", "status", "completed"]

    if CURRENT_EVENT_ID is None:
        return None
    else:
        ui_elements["month_calendar"].set_event_start(CURRENT_EVENT_ID, ui_elements["date"].value)
        for prop in props:
            ui_elements["month_calendar"].set_event_props(CURRENT_EVENT_ID, {prop: ui_elements[prop].value})

        ui_elements["dialog"].close()


def list_view_calendar(events_list: list[Event]):
    events_list = [event.to_dict() for event in events_list]

    options = {
        "initialView": 'listYear',
        "events": events_list,
        'height': 'auto',
    }

    FullCalendar(options)


def change_event_visibility(sender: nicegui.elements.switch.Switch, ui_elements: dict):
    if sender.value:
        display_type = 'auto'
    else:
        display_type = 'none'
    if "Scheduled" in sender.text:
        event_type = "Scheduled"
    else:
        event_type = "Logged"
    events_to_show = Event.select().where(Event.status == event_type)
    for event in events_to_show:
        ui_elements["month_calendar"].set_event_props(event.id, {"display": display_type})


@ui.page('/')
def main():
    events_query = Event.select()
    events_list = [event for event in events_query]
    projects_list = ["REMORA", "CFHH"]

    ui_elements = {}

    with ui.row().classes('w-full no-wrap'):
        with ui.column().classes('w-2/3'):
            with ui.tabs().classes('w-full') as tabs:
                one = ui.tab('Month View')
                two = ui.tab('List View')
            with ui.tab_panels(tabs, value=one).classes():
                with ui.tab_panel(one):
                    ui_elements["month_calendar"] = month_view_calendar(events_list, ui_elements)
                with ui.tab_panel(two):
                    list_view_calendar(events_list)
        with ui.column().classes('w-1/3'):
            ui_elements["scheduled_switch"] = ui.switch("Show Scheduled Events", value=True,
                                                        on_change=lambda e: change_event_visibility(e.sender, ui_elements))
            ui_elements["logged_switch"] = ui.switch("Show Logged Events", value=True,
                                                     on_change=lambda e: change_event_visibility(e.sender, ui_elements))

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


main()
