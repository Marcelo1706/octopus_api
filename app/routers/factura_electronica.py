from io import StringIO
import json
import time

from fastapi import APIRouter, File, UploadFile, status, HTTPException
import pandas as pd

from app import schemas
from app.models.enums import Ambientes, Dte
from app.models.dte import DocumentoFirmado
from app.services.generar_dte import generate_factura_electronica
from app.services.pandas_to_dte import convert_df_to_fe
from app.services.recepcion_dte import recepcion_dte, consultar_dte
from app.utils.signing import firmar_documento, firmar_documento_raw

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.DTESchema,
    status_code=status.HTTP_201_CREATED)
async def create(factura: schemas.FacturaElectronicaAPI):
    """
    Genera una Factura Electrónica con el formato establecido por MH,
    la firma y la envía a Recepción DTE para su posterior aprobación.
    """
    documento = await generate_factura_electronica(
        factura,
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
        version=1,
        tipoDte=Dte.FACTURA,
        documento_firmado=documento_firmado.body,
        documento_sin_firma=documento.model_dump_json()
    )

    return respuesta_hacienda


@router.post("/txt/")
async def create_from_txt(file: UploadFile = File(...)):
    content = await file.read()
    string_io = StringIO(content.decode("utf-8", errors="ignore"))
    df = pd.read_csv(string_io, sep="|", header=None)
    fe = await convert_df_to_fe(df)

    documento_firmado: DocumentoFirmado = firmar_documento(fe)

    if not documento_firmado.status == "OK":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=documento_firmado.body
        )

    respuesta_hacienda = await recepcion_dte(
        codGeneracion=fe.identificacion.codigoGeneracion,
        ambiente=Ambientes.PRUEBA,
        idEnvio=1,
        version=1,
        tipoDte=Dte.FACTURA,
        documento_firmado=documento_firmado.body,
        documento_sin_firma=fe.model_dump_json()
    )

    return respuesta_hacienda


@router.post("/raw/")
async def factura_de_json(factura: dict):
    documento_firmado: DocumentoFirmado = firmar_documento_raw(factura)

    if not documento_firmado.status == "OK":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=documento_firmado.body
        )

    respuesta_hacienda = await recepcion_dte(
        codGeneracion=factura["identificacion"]["codigoGeneracion"],
        ambiente=Ambientes.PRUEBA,
        idEnvio=1,
        version=1,
        tipoDte=Dte.FACTURA,
        documento_firmado=documento_firmado.body,
        documento_sin_firma=json.dumps(factura)
    )

    return respuesta_hacienda


@router.get("/consultar/")
async def consultar_factura(codGeneracion: str, fecEmision: str):
    return await consultar_dte(codGeneracion, fecEmision)
