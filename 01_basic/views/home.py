import fastapi
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates('templates')

router = fastapi.APIRouter()


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/favicon.ico')
def index(request: Request):
    return RedirectResponse(url='/static/images/favicon.ico')
