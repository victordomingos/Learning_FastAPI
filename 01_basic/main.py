from typing import Optional

import bleach
import requests
import uvicorn
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

api = FastAPI()
templates = Jinja2Templates('templates')


@api.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@api.get('/api/calculate')
def calculate(x: int, y: int, z: Optional[int] = None):
    if z is not None and z == 0:
        error = {'error': 'Error: z cannot be zero.'}
        return JSONResponse(content=error, status_code=400)

    value = (x + y)
    if z is not None:
        value = value / z

    return {
        'x': x,
        'y': y,
        'z': z,
        'value': value
    }


@api.get('/api/ctt-track')
@cached(cache=TTLCache(maxsize=5, ttl=10))  # 10 segundos, p/reduzir requests
def verificar_estado(tracking_code: str) -> str:
    """ Verificar estado de objeto (Encomenda ou Correio Registado) nos CTT
    Ex: verificar_estado("EA746000000PT")
    """
    ctt_url = "https://www.ctt.pt/feapl_2/app/open/objectSearch/objectSearch.jspx"
    try:
        response = requests.post(ctt_url, data={'objects': tracking_code})
        sopa = BeautifulSoup(response.content, "lxml")
        tabela = sopa.find(id='objectSearchResult').find('table')
        celulas = tabela('td')
        estado = celulas[4].renderContents().strip(b' \r\n\t')
        estado = str(estado, 'utf-8')
        estado = bleach.clean(estado, tags=[], strip=True)
        if estado == "":
            # se valor do ult. estado estiver vazio, usar as celulas da tabela
            # seguinte para ler estado
            estado = celulas[9].renderContents().strip(b' \r\n\t')
            estado = str(estado, 'utf-8')
            estado = bleach.clean(estado, tags=[], strip=True)
    except Exception as e:
        error = "Não foi possível obter estado atualizado a partir da web."
        error += f"\nDetalhes adicionais:\n{e}"
        return JSONResponse(content=error, status_code=400)
    return estado


uvicorn.run(api, port=8001, host='127.0.0.1')
