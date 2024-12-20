from pydantic import BaseModel

from app.models.enums import (
    Ambientes,
    Dte,
    ModeloFacturacion,
    TipoContingencia,
    TipoTransmision,
)


class IdentificacionBase(BaseModel):
    """Apartado "identificacion" del JSON de un DTE"""
    version: int
    ambiente: Ambientes
    tipoDte: Dte
    numeroControl: str
    codigoGeneracion: str
    tipoModelo: ModeloFacturacion
    tipoOperacion: TipoTransmision
    tipoContingencia: TipoContingencia | None = None
    fecEmi: str
    horEmi: str
    tipoMoneda: str


class Identificacion(IdentificacionBase):
    motivoContin: str | None = None


class IdentificacionFEX(IdentificacionBase):
    motivoContigencia: str | None = None
