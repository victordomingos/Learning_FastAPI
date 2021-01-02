import bleach
import fastapi
import requests
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
from fastapi.responses import JSONResponse

router = fastapi.APIRouter()


@router.get('/api/ctt-track')
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

