import peewee

db = peewee.SqliteDatabase('data.db')

# FullCalendar Event properties
props = ["id", "title", "start"]

# FullCalendar Event extendedProperties
extended_props = ["status", "completed", "project"]

# Unused properties
unused_props = ["description", "repeating"]

# FullCalendar Event properties that are presented in the edit event dialog
all_props = props + extended_props


class Event(peewee.Model):
    id = peewee.AutoField()
    title = peewee.CharField()
    start = peewee.CharField()  # Date of event in YYYY-MM-DD format
    status = peewee.CharField(choices=["Scheduled", "Logged"])
    completed = peewee.BooleanField()
    project = peewee.CharField(null=True)
    description = peewee.CharField(null=True)
    repeating = peewee.BooleanField(default=False)

    class Meta:
        database = db

    def to_dict(self):
        if self.completed:
            completed = "Yes"
        else:
            completed = "No"
        return {"id": self.id,
                "title": self.title,
                "start": self.start,
                "status": self.status,
                "completed": completed,
                "project": self.project,
                "description": self.description,
                "repeating": self.repeating,
                "allDay": "true"}

