from chronocli.database.db import get_session, init_db
from chronocli.models.models import Session as TrackingSession
from datetime import datetime, timedelta
import random

def seed_data():
    init_db()
    tasks = ["Coding Frontend", "Bug Squashing", "Writing Documentation", "Client Meeting", "UI Design", "Database Optimization"]
    categories = ["Development", "Meetings", "Design", "Research"]
    
    with get_session() as session:
        for i in range(15):
            task = random.choice(tasks)
            cat = random.choice(categories)
            start = datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
            duration = random.randint(1800, 7200) # 30m to 2h
            end = start + timedelta(seconds=duration)
            
            new_session = TrackingSession(
                task_name=task,
                category=cat,
                start_time=start,
                end_time=end,
                duration=float(duration)
            )
            session.add(new_session)
        session.commit()
    print("Sample data seeded successfully!")

if __name__ == "__main__":
    seed_data()
