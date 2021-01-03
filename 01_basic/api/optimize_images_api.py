import shutil
import tempfile
import uuid

import fastapi
import io

from PIL import Image
from starlette.responses import StreamingResponse, FileResponse
from fastapi import File, UploadFile
import magic

router = fastapi.APIRouter()


@router.post('/api/optimize-image')
async def optimize_image(file: UploadFile = File(...)):
    """ Optimize a single image according to the parameters provided
    """
    tmp_filename = uuid.uuid4().hex + file.filename
    with open(tmp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # img = Image.open(file.file)

    mtype = magic.from_file(tmp_filename, mime=True)
    return FileResponse(tmp_filename, media_type=mtype)


    #return StreamingResponse(buffer, media_type=mtype)


