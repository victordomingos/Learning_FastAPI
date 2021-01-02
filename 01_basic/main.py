import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api import ctt_api
from api import exercises_api
from views import home

api = FastAPI()


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(ctt_api.router)
    api.include_router(exercises_api.router)


def configure():
    configure_routing()


if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8001, host='127.0.0.1')
else:
    configure()
