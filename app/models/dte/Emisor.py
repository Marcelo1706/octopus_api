from pydantic import BaseModel, EmailStr

from app.models.dte.Direccion import Direccion


class Emisor(BaseModel):
    nit: str
    nrc: str
    nombre: str
    codActividad: str
    descActividad: str
    nombreComercial: str
    tipoEstablecimiento: str
    direccion: Direccion
    telefono: str
    correo: EmailStr
    codEstableMH: str | None = None
    codEstable: str | None = None
    codPuntoVentaMH: str | None = None
    codPuntoVenta: str | None = None


class EmisorFEX(Emisor):
    regimen: str
    recintoFiscal: str
    tipoItemExpor: int
