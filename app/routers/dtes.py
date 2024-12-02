from typing import List
from fastapi import APIRouter

from app.models.orm import DTE
from app import schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.DTE])
async def read_all():
    return await DTE.all()
