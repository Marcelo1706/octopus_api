from typing import List

from pydantic import BaseModel

from app.models.dte.Tributo import Tributo
from app.models.dte.Pago import Pago


class ResumenBase(BaseModel):
    totalNoSuj: float
    totalExenta: float
    totalGravada: float
    subTotalVentas: float
    descuNoSuj: float
    descuExenta: float
    descuGravada: float
    porcentajeDescuento: float
    totalDescu: float
    tributos: List[Tributo] | None = None
    subTotal: float
    ivaRete1: float
    reteRenta: float
    montoTotalOperacion: float
    totalNoGravado: float
    totalPagar: float
    totalLetras: str
    saldoFavor: float
    condicionOperacion: int
    pagos: List[Pago] | None = None
    numPagoElectronico: str | None = None


class ResumenFE(ResumenBase):
    totalIva: float


class ResumenCCF(ResumenBase):
    ivaPerci1: float | None = None


class ResumenFEX(BaseModel):
    totalGravada: float
    descuento: float
    porcentajeDescuento: float
    totalDescu: float
    montoTotalOperacion: float
    totalNoGravado: float
    totalPagar: float
    totalLetras: str
    condicionOperacion: int
    pagos: List[Pago] | None = None
    numPagoElectronico: str | None = None
    codIncoterms: str | None = None
    descIncoterms: str | None = None
    observaciones: str | None = None
    flete: float = 0
    seguro: float = 0
