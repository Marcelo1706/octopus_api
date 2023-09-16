from pydantic import BaseModel


class ResumenAPIBase(BaseModel):
    descuNoSuj: float = 0
    descuExtenta: float = 0
    descuGravada: float = 0
    porcentajeDescuento: float = 0
    ivaRete1: float = 0
    reteRenta: float = 0
    saldoFavor: float = 0
    condicionOperacion: int = 1


class ResumenAPIFE(ResumenAPIBase):
    pass


class ResumenAPICCF(ResumenAPIBase):
    ivaPerci1: float = 0


class ResumenAPIFEX(BaseModel):
    porcentajeDescuento: float = 0
    condicionOperacion: int = 1
    codIncoterms: str | None = None
    descIncoterms: str | None = None
    flete: float = 0
    seguro: float = 0
    descuento: float = 0
