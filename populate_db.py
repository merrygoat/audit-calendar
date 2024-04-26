from datetime import datetime

from models import Event
from models import db

db.create_tables([Event])

events_list = [
    Event(title="Rotate keys", description="Rotate keys for REMORA", start=datetime(2024, 4, 20), status="Scheduled", completed="No"),
    Event(title="Check EC2", description="Check the EC2 instances for bugs", project="CFHH", start=datetime(2024, 4, 23), status="Scheduled", completed="No"),
    Event(title="Rebuild instances", description="Rebuild and redeploy EC2 instances", start=datetime(2024, 4, 25), status="Scheduled", completed="No")]
for event in events_list:
    event.save()


