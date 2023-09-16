import time

from fastapi import APIRouter, status, HTTPException

from app import schemas
from app.models.enums import Ambientes, Dte
from app.models.dte import DocumentoFirmado
from app.services.generar_dte import generate_credito_fiscal
from app.services.recepcion_dte import recepcion_dte
from app.utils.signing import firmar_documento


router = APIRouter()


@router.post(
    "/",
    response_model=schemas.DTESchema,
    status_code=status.HTTP_201_CREATED)
async def create(credito_fiscal: schemas.CreditoFiscalAPI):
    """
    Genera un Crédito Fiscal con el formato establecido por MH,
    lo firma y la envía a Recepción DTE para su posterior aprobación.
    """
    documento = await generate_credito_fiscal(
        credito_fiscal,
        int(time.time())
    )
    documento_firmado: DocumentoFirmado = firmar_documento(documento)

    if not documento_firmado.status == "OK":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=documento_firmado.body
        )

    respuesta_hacienda = await recepcion_dte(
        codGeneracion=documento.identificacion.codigoGeneracion,
        ambiente=Ambientes.PRUEBA,
        idEnvio=1,
        version=3,
        tipoDte=Dte.CREDITO_FISCAL,
        documento_firmado=documento_firmado.body,
        documento_sin_firma=documento.model_dump_json()
    )

    return respuesta_hacienda
