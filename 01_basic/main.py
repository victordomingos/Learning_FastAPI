import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api import ctt_api
from api import exercises_api
from api import optimize_images_api
from api import weather_api
from services import openweather_service
from views import home

api = FastAPI()


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(ctt_api.router)
    api.include_router(exercises_api.router)
    api.include_router(optimize_images_api.router)
    api.include_router(weather_api.router)


def configure_apikeys():
    file = Path('settings.json').absolute()
    if not file.exists():
        raise Exception("Please configure settings.json according to the provided template.")

    with open('settings.json') as f:
        settings = json.load(f)
        openweather_service.api_key = settings.get('api_key')


def configure():
    configure_apikeys()
    configure_routing()


if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()
