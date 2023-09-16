from typing import List

from pydantic import BaseModel


class ItemBase(BaseModel):
    numItem: int
    tipoItem: int
    numeroDocumento: str | None = None
    cantidad: float
    codigo: str | None = None
    codTributo: str | None = None
    uniMedida: int
    descripcion: str
    precioUni: float
    montoDescu: float
    ventaNoSuj: float
    ventaExenta: float
    ventaGravada: float
    tributos: List[str] | None = None
    psv: float
    noGravado: float


class ItemFE(ItemBase):
    ivaItem: float


class ItemCCF(ItemBase):
    pass


class ItemFEX(BaseModel):
    numItem: int
    cantidad: float
    codigo: str | None = None
    uniMedida: int
    descripcion: str
    precioUni: float
    montoDescu: float
    ventaGravada: float
    tributos: List[str] | None = None
    noGravado: float
