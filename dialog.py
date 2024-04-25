from nicegui import events

import models
from models import Event


def open_edit_event_dialog(event: events.GenericEventArguments, ui_elements: dict):
    ui_elements["dialog_confirm_button"].text = "Update Event"

    if 'info' in event.args:
        clicked_event = event.args["info"]["event"]
        for prop in models.props:
            ui_elements[prop].set_value(clicked_event[prop])
        for prop in models.extended_props:
            ui_elements[prop].set_value(clicked_event["extendedProps"][prop])

        ui_elements["dialog"].open()


def update_event(ui_elements: dict):
    event_id = ui_elements["id"].value

    # Get the event and update it from the values in the dialog
    event = Event.select().where(Event.id == event_id).get()
    for prop in models.all_props:
        event.__setattr__(prop, ui_elements[prop].value)
    event.save()

    ui_elements["month_calendar"].remove_event(event_id, update=False)
    ui_elements["month_calendar"].add_event(event.to_dict())

    ui_elements["dialog"].close()
