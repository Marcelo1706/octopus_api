import requests



def generar_pdf(
        documento_sin_firma: str,
        selloRecibido: str,
        tipo_dte: str
        ) -> dict:
    """Genera un PDF a partir de un documento sin firmar."""
    response = requests.post(
        f"http://php.konverza.digital?documento={tipo_dte}",
        json={"documento": documento_sin_firma, "selloRecibido": selloRecibido}
    )

    print(response.text)
    return response.json()
