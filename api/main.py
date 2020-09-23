# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
from fastapi import FastAPI
from api.routers import task

tags_metadata = [
    {
        'name': 'task',
        'description': 'Operations related to tasks.',
    },
]

app = FastAPI(
    title='Task list',
    description='Task-list project for the **Megadados** course',
    openapi_tags=tags_metadata,
)

app.include_router(
    task.router,
    prefix="/task",
    tags=["task"],
)