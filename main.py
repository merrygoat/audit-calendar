from nicegui.elements import switch, select
from nicegui import ui

from dialog import open_edit_event_dialog, update_event
from fullcalendar import FullCalendar
from models import Event


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

    month_calendar = FullCalendar(options, on_click=lambda e: open_edit_event_dialog(e, ui_elements)).classes(classes)
    return month_calendar


def list_view_calendar(events_list: list[Event]):
    events_list = [event.to_dict() for event in events_list]

    options = {
        "initialView": 'listYear',
        "events": events_list,
        'height': 'auto',
    }

    FullCalendar(options)


def change_event_visibility(sender: switch.Switch, ui_elements: dict):
    """When one of the two event visibility buttons is pressed, change which events are visible."""
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


def filter_events_by_project(sender: select.Select, ui_elements: dict):
    """When a project filter is selected, change the visible events by which project they are in."""
    if not sender.value:
        events_to_hide = []
        events_to_show = Event.select()
    else:
        events_to_hide = Event.select().where((Event.project != sender.value) | (Event.project.is_null()))
        events_to_show = Event.select().where(Event.project == sender.value)

    for event in events_to_show:
        ui_elements["month_calendar"].set_event_props(event.id, {"display": 'auto'})

    for event in events_to_hide:
        ui_elements["month_calendar"].set_event_props(event.id, {"display": 'none'})


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
            ui.label("Event Filters")
            ui_elements["scheduled_switch"] = ui.switch("Show Scheduled Events", value=True,
                                                        on_change=lambda e: change_event_visibility(e.sender, ui_elements))
            ui_elements["logged_switch"] = ui.switch("Show Logged Events", value=True,
                                                     on_change=lambda e: change_event_visibility(e.sender, ui_elements))
            ui_elements["project_filter"] = ui.select(projects_list, label="Project", clearable=True, with_input=True,
                                                      on_change=lambda e: filter_events_by_project(e.sender, ui_elements))

    with ui.dialog() as ui_elements["dialog"], ui.card().classes():
        ui.label("Selected Event Details")
        ui_elements["id"] = ui.input()
        ui_elements["id"].set_visibility(False)
        with ui.grid(columns='80px auto').classes('w-full'):
            ui.label("Title").classes('place-content-center')
            ui_elements["title"] = ui.input()
            ui.label("Date").classes('place-content-center')
            with ui.input('Date') as ui_elements["start"]:
                with ui_elements["start"].add_slot('append'):
                    ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
                with ui.menu() as menu:
                    ui.date().bind_value(ui_elements["start"])
            ui.label("Project").classes('place-content-center')
            ui_elements["project"] = ui.select(projects_list, value=1, clearable=True, with_input=True)
            ui.label("Status").classes('place-content-center')
            ui_elements["status"] = ui.radio(["Scheduled", "Logged"]).props('inline')
            ui.label("Completed").classes('place-content-center')
            ui_elements["completed"] = ui.radio(["Yes", "No"], value="No").props('inline')
        with ui.row().classes('w-full q-mt-md'):
            ui.space()
            ui_elements["dialog_confirm_button"] = ui.button('Update Event', on_click=lambda: update_event(ui_elements))
            ui.button('Cancel', on_click=lambda: ui_elements["dialog"].close())

    ui.run()


main()
