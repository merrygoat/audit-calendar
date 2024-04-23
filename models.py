import peewee

db = peewee.SqliteDatabase('data.db')


class Event(peewee.Model):
    id = peewee.AutoField()
    title = peewee.CharField()
    date = peewee.DateField()
    project = peewee.CharField(null=True)
    description = peewee.CharField(null=True)
    status = peewee.CharField()
    completed = peewee.BooleanField()

    class Meta:
        database = db

    def to_dict(self):
        if self.completed:
            completed = "Yes"
        else:
            completed = "No"

        return {"id": self.id,
                "title": self.title,
                "date": self.date.isoformat(),
                "description": self.description,
                "project": self.project,
                "status": self.status,
                "completed": completed,
                "allDay": "true"}
