from datetime import datetime

from pydantic import BaseModel


class DTESchema(BaseModel):
    codGeneracion: str
    selloRecibido: str | None
    estado: str
    documento: str
    fhProcesamiento: datetime | None
    observaciones: str | None
    tipo_dte: str
