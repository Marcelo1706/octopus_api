from datetime import datetime
import pandas as pd
from app.models import enums
from app.models.dte import CreditoFiscal, Direccion, FacturaElectronica, Identificacion, Tributo
from app.models.dte.Item import ItemCCF, ItemFE
from app.models.dte.Receptor import ReceptorCCF, ReceptorFE
from app.models.dte.Resumen import ResumenCCF, ResumenFE
from app.services.datos_emisor import get_datos_emisor
from app.utils.codes import generate_numero_control, generate_uuid

from app.utils.currency import total_en_letras

async def convert_df_to_fe(df: pd.DataFrame) -> FacturaElectronica:
    cuerpoDocumento = []
    correlativo = 1
    current_row = df.iloc[0]

    for index, row in df.iterrows():
        correlativo = row[0]
        tributos = []
        tributo1 = row[14].strip() or None
        tributo2 = row[15].strip() or None

        if tributo1 is not None:
            tributos.append(tributo1)
        if tributo2 is not None:
            tributos.append(tributo2)

        if tributos == []:
            tributos = None

        item_cuerpo = ItemFE(
            numItem=row[4],
            tipoItem=row[5],
            cantidad=row[6],
            codigo=str(row[6]),
            uniMedida=row[7],
            descripcion=row[8].strip(),
            precioUni=row[9],
            montoDescu=row[10],
            ventaNoSuj=row[11],
            ventaExenta=row[12],
            ventaGravada=row[13],
            tributos = tributos,
            psv=row[16],
            noGravado=row[17],
            ivaItem=row[18],
        )
        cuerpoDocumento.append(item_cuerpo)
        current_row = row

    return FacturaElectronica(
        identificacion=Identificacion(
            version=1,
            ambiente=enums.Ambientes.PRUEBA,
            tipoDte=enums.Dte.FACTURA,
            numeroControl=generate_numero_control(
                "01", correlativo
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
        documentoRelacionado=None,
        emisor= await get_datos_emisor(),
        receptor=ReceptorFE(
            tipoDocumento=None,
            numDocumento=None,
            nombre=None,
            telefono=None,
            correo=None,
        ),
        otrosDocumentos=None,
        ventaTercero=None,
        cuerpoDocumento=cuerpoDocumento,
        resumen=ResumenFE(
            totalNoSuj=current_row[19],
            totalExenta=current_row[20],
            totalGravada=current_row[21],
            subTotalVentas=current_row[22],
            descuNoSuj=current_row[23],
            descuExenta=current_row[24],
            descuGravada=current_row[25],
            porcentajeDescuento=current_row[26],
            totalDescu=current_row[27],
            tributos = [
                Tributo(
                    codigo=current_row[28],
                    descripcion=current_row[29],
                    valor=current_row[30],
                ),
                Tributo(
                    codigo=current_row[31],
                    descripcion=current_row[32],
                    valor=current_row[33],
                )
            ],
            subTotal=current_row[34],
            ivaRete1=current_row[35],
            reteRenta=current_row[36],
            montoTotalOperacion=current_row[37],
            totalNoGravado=0.0,
            totalPagar=current_row[38],
            totalLetras=total_en_letras(current_row[38]),
            totalIva=current_row[40],
            saldoFavor=current_row[41],
            condicionOperacion=current_row[42],
        ),
        extension=None,
        apendice=None
    )


async def convert_df_to_ccf(df: pd.DataFrame) -> CreditoFiscal:
    cuerpoDocumento = []
    correlativo = 1
    current_row = df.iloc[0]

    for index, row in df.iterrows():
        correlativo = row[0]
        tributos = []
        tributo1 = str(row[25]).strip() or None
        tributo2 = row[26].strip() or None
        tributo3 = row[27].strip() or None

        if tributo1 is not None:
            tributos.append(tributo1)
        if tributo2 is not None:
            tributos.append(tributo2)
        if tributo3 is not None:
            tributos.append(tributo3)

        if tributos == []:
            tributos = None

        item_cuerpo = ItemCCF(
            numItem=row[15],
            tipoItem=row[16],
            descripcion=row[17].strip(),
            cantidad=row[18],
            uniMedida=row[19],
            precioUni=row[20],
            montoDescu=row[21],
            ventaNoSuj=row[22],
            ventaExenta=row[23],
            ventaGravada=row[24],
            tributos=tributos,
            psv=row[28],
            noGravado=row[29],
        )
        cuerpoDocumento.append(item_cuerpo)
        current_row = row
        
    return CreditoFiscal(
        identificacion=Identificacion(
            version=3,
            ambiente=enums.Ambientes.PRUEBA,
            tipoDte=enums.Dte.CREDITO_FISCAL,
            numeroControl=generate_numero_control(
                "03", correlativo
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
        documentoRelacionado=None,
        emisor= await get_datos_emisor(),
        receptor=ReceptorCCF(
            nit=str(current_row[4]).zfill(14),
            nrc=str(current_row[5]),
            nombre=current_row[6].strip(),
            codActividad=str(current_row[7]),
            descActividad=current_row[8].strip(),
            nombreComercial=current_row[9].strip(),
            direccion=Direccion(
                departamento=str(current_row[10]).zfill(2),
                municipio=str(current_row[11]) if current_row[11] < 99 else "14",
                complemento=current_row[12].strip()
            ),
            telefono=str(current_row[13]),
            correo=current_row[14].strip(),
        ),
        otrosDocumentos=None,
        ventaTercero=None,
        cuerpoDocumento=cuerpoDocumento,
        resumen=ResumenCCF(
            totalNoSuj=current_row[30],
            totalExenta=current_row[31],
            totalGravada=current_row[32],
            subTotalVentas=current_row[33],
            descuNoSuj=current_row[34],
            descuExenta=current_row[35],
            descuGravada=current_row[36],
            porcentajeDescuento=current_row[37],
            totalDescu=current_row[38],
            tributos = [
                Tributo(
                    codigo=str(current_row[39]),
                    descripcion=current_row[40],
                    valor=current_row[41],
                ),
                Tributo(
                    codigo=current_row[42],
                    descripcion=current_row[43],
                    valor=current_row[44],
                ),
                Tributo(
                    codigo=current_row[45],
                    descripcion=current_row[46],
                    valor=current_row[47],
                )
            ],
            subTotal=current_row[48],
            ivaPerci1=current_row[49],
            ivaRete1=current_row[50],
            reteRenta=current_row[51],
            montoTotalOperacion=current_row[52],
            totalNoGravado=current_row[53],
            saldoFavor=current_row[54],
            totalPagar=current_row[55],
            totalLetras=total_en_letras(current_row[55]),
            condicionOperacion=current_row[57],
        )
    )
