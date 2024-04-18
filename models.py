import peewee

db = peewee.SqliteDatabase('data.db')


class Event(peewee.Model):
    name = peewee.CharField()
    description = peewee.CharField()
    date = peewee.DateField()

    class Meta:
        database = db
