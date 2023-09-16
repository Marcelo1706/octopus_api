from datetime import datetime

import requests

from app import schemas
from app.config.cfg import RECEPTION_URL
from app.models.dte import RespuestaHacienda
from app.models.orm import DTE
from app.utils.auth import get_token
from app.utils.dte_date_parser import parse_dte_date


async def recepcion_dte(
    codGeneracion: str,
    ambiente: str,
    idEnvio: int,
    version: int,
    tipoDte: str,
    documento_firmado: str,
    documento_sin_firma: str = None
) -> schemas.DTESchema:
    """Request to the Recepción DTE API to send a DTE."""
    try:
        token = get_token()
        headers = {"Authorization": f"{token}"}
        data = {
            "ambiente": ambiente,
            "idEnvio": idEnvio,
            "version": version,
            "tipoDte": tipoDte,
            "documento": documento_firmado
        }
        response = requests.post(RECEPTION_URL, json=data, headers=headers)

        if response.status_code == 200:
            respuesta_hacienda = RespuestaHacienda(**response.json())

            dte = DTE(
                codGeneracion=codGeneracion,
                selloRecibido=respuesta_hacienda.selloRecibido,
                estado=respuesta_hacienda.estado,
                documento=documento_sin_firma,
                fhProcesamiento=parse_dte_date(
                    respuesta_hacienda.fhProcesamiento
                ),
                observaciones=respuesta_hacienda.observaciones,
                tipo_dte=tipoDte
            )
            await dte.save()

        else:
            raise Exception(
                f"Received non-200 status code: {response.status_code}"
                f" with message: {response.text}"
            )

    except Exception as e:
        # Handle other exceptions here
        print(f"Exception: {e}")
        # Handle the error case by creating a DTE with CONTINGENCIA status.
        dte = DTE(
            codGeneracion=codGeneracion,
            selloRecibido=None,
            estado="CONTINGENCIA",
            documento=documento_sin_firma,
            fhProcesamiento=datetime.now(),
            observaciones="No se pudo conectar con MH",
            tipo_dte=tipoDte
        )
        await dte.save()

    return schemas.DTESchema(
        codGeneracion=dte.codGeneracion,
        selloRecibido=dte.selloRecibido,
        estado=dte.estado,
        documento=dte.documento,
        fhProcesamiento=dte.fhProcesamiento,
        observaciones=dte.observaciones,
        tipo_dte=tipoDte
    )
