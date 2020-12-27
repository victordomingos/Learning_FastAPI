from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse

api = FastAPI()

@api.get('/')
def index():
    body = """
    <html>
      <body>
        <h1>Welcome to this API</h1>
        <div>
          Try it now: <a href="/api/calculate?x=230&y=327&z=1327">/api/calculate?x=230&y=327&z=1327</a>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=body)


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


uvicorn.run(api, port=8001, host='127.0.0.1')
