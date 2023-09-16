from datetime import datetime

from app.models.dte import (
    FacturaElectronica,
    CreditoFiscal,
    FacturaExportacion,
    Identificacion,
    IdentificacionFEX
)
from app.models import enums
from app.schemas import (
    FacturaElectronicaAPI,
    CreditoFiscalAPI
)
from app.schemas.factura_exportacion import FacturaExportacionAPI
from app.services.converters import (
    convert_itemapi_to_itemfe,
    convert_itemapi_to_itemccf,
    convert_itemapi_to_itemfex
)
from app.services.datos_emisor import get_datos_emisor
from app.services.generar_resumen import (
    generar_resumen_fe,
    generar_resumen_ccf,
    generar_resumen_fex
)
from app.utils.codes import generate_uuid, generate_numero_control


async def generate_factura_electronica(
        factura: FacturaElectronicaAPI,
        correlativo: int) -> FacturaElectronica:
    """Convierte una FacturaElectronicaAPI a FacturaElectronica."""

    items = [
        convert_itemapi_to_itemfe(item, numero)
        for numero, item in enumerate(factura.cuerpoDocumento, start=1)
    ]

    return FacturaElectronica(
        identificacion=Identificacion(
            version=1,
            ambiente=enums.Ambientes.PRUEBA,
            tipoDte=enums.Dte.FACTURA,
            numeroControl=generate_numero_control(
                enums.Dte.FACTURA, correlativo
            ),
            codigoGeneracion=generate_uuid(),
            tipoModelo=enums.ModeloFacturacion.PREVIO,
            tipoOperacion=enums.TipoTransmision.NORMAL,
            tipoContingencia=None,
            motivoContin=None,
            fecEmi=datetime.now().strftime("%Y-%m-%d"),
            horEmi=datetime.now().strftime("%H:%M:%S"),
            tipoMoneda="USD",
        ),
        documentoRelacionado=factura.documentoRelacionado,
        emisor=await get_datos_emisor(),
        receptor=factura.receptor,
        otrosDocumentos=factura.otrosDocumentos,
        ventaTercero=factura.ventaTercero,
        cuerpoDocumento=items,
        resumen=generar_resumen_fe(items, factura.resumen),
        extension=factura.extension,
        apendice=factura.apendice
    )


async def generate_credito_fiscal(
        credito_fiscal: CreditoFiscalAPI,
        correlativo: int) -> CreditoFiscal:
    """Convierte un CreditoFiscalAPI a CreditoFiscal."""
    items = [
        convert_itemapi_to_itemccf(item, numero)
        for numero, item in enumerate(credito_fiscal.cuerpoDocumento, start=1)
    ]

    return CreditoFiscal(
        identificacion=Identificacion(
            version=3,
            ambiente=enums.Ambientes.PRUEBA,
            tipoDte=enums.Dte.CREDITO_FISCAL,
            numeroControl=generate_numero_control(
                enums.Dte.CREDITO_FISCAL, correlativo
            ),
            codigoGeneracion=generate_uuid(),
            tipoModelo=enums.ModeloFacturacion.PREVIO,
            tipoOperacion=enums.TipoTransmision.NORMAL,
            tipoContingencia=None,
            motivoContin=None,
            fecEmi=datetime.now().strftime("%Y-%m-%d"),
            horEmi=datetime.now().strftime("%H:%M:%S"),
            tipoMoneda="USD",
        ),
        documentoRelacionado=credito_fiscal.documentoRelacionado,
        emisor=await get_datos_emisor(),
        receptor=credito_fiscal.receptor,
        otrosDocumentos=credito_fiscal.otrosDocumentos,
        ventaTercero=credito_fiscal.ventaTercero,
        cuerpoDocumento=items,
        resumen=generar_resumen_ccf(items, credito_fiscal.resumen),
        extension=credito_fiscal.extension,
        apendice=credito_fiscal.apendice
    )


async def generate_factura_exportacion(
        factura: FacturaExportacionAPI,
        correlativo: int) -> FacturaExportacion:
    """Convierte una FacturaExportacionAPI a FacturaExportacion."""

    items = [
        convert_itemapi_to_itemfex(item, numero)
        for numero, item in enumerate(factura.cuerpoDocumento, start=1)
    ]

    return FacturaExportacion(
        identificacion=IdentificacionFEX(
            version=1,
            ambiente=enums.Ambientes.PRUEBA,
            tipoDte=enums.Dte.EXPORTACION,
            numeroControl=generate_numero_control(
                enums.Dte.EXPORTACION, correlativo
            ),
            codigoGeneracion=generate_uuid(),
            tipoModelo=enums.ModeloFacturacion.PREVIO,
            tipoOperacion=enums.TipoTransmision.NORMAL,
            tipoContingencia=None,
            motivoContigencia=None,
            fecEmi=datetime.now().strftime("%Y-%m-%d"),
            horEmi=datetime.now().strftime("%H:%M:%S"),
            tipoMoneda="USD",
        ),
        emisor=await get_datos_emisor(factura.emisor),
        receptor=factura.receptor,
        otrosDocumentos=factura.otrosDocumentos,
        ventaTercero=factura.ventaTercero,
        cuerpoDocumento=items,
        resumen=generar_resumen_fex(items, factura.resumen),
        apendice=factura.apendice
    )
