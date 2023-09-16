from app.config.cfg import NIT

from app.models.orm import DatosEmpresa
from app.models.dte import Emisor, EmisorFEX


async def get_datos_emisor(emisor_fex=None):
    """Get DatosEmpresa from database."""
    datos_emisor = await DatosEmpresa.get(nit=NIT).first()
    emisor = {
        "nombre": datos_emisor.nombre,
        "nit": datos_emisor.nit,
        "nrc": datos_emisor.nrc,
        "codActividad": datos_emisor.codActividad,
        "descActividad": datos_emisor.descActividad,
        "nombreComercial": datos_emisor.nombreComercial,
        "tipoEstablecimiento": datos_emisor.tipoEstablecimiento,
        "direccion": {
            "departamento": datos_emisor.departamento,
            "municipio": datos_emisor.municipio,
            "complemento": datos_emisor.complemento
        },
        "telefono": datos_emisor.telefono,
        "correo": datos_emisor.correo,
        "codEstableMH": datos_emisor.codEstableMH,
        "codEstable": datos_emisor.codEstable,
        "codPuntoVentaMH": datos_emisor.codPuntoVentaMH,
        "codPuntoVenta": datos_emisor.codPuntoVenta
    }
    if emisor_fex:
        emisor["regimen"] = emisor_fex.regimen
        emisor["recintoFiscal"] = emisor_fex.recintoFiscal
        emisor["tipoItemExpor"] = emisor_fex.tipoItemExpor
        return EmisorFEX(**emisor)

    return Emisor(**emisor)
