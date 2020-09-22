  
from api.models import Task

import uuid

class DBSession:
    tasks = {}

    def __init__(self):
        self.tasks = DBSession.tasks

    def read_tasks(self):
        return self.tasks
    
    def create_task(self, item):
        uuid_ = uuid.uuid4()
        self.tasks[uuid_] = item
        return uuid_

    def read_task(self, uuid_):
        return self.tasks[uuid_]

    def replace_task(self, uuid_, item):
        self.tasks[uuid_] = item

    def alter_task(self, uuid_, item):
        update_data = item.dict(exclude_unset=True)
        self.tasks[uuid_] = self.tasks[uuid_].copy(update=update_data)
    
    def remove_task(self, uuid_):
        del self.tasks[uuid_]

    
def get_db():
    return DBSession()