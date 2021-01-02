from typing import Optional

import fastapi
from fastapi.responses import JSONResponse

router = fastapi.APIRouter()


@router.get('/api/calculate')
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
