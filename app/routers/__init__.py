from app.routers.datos_empresa import router as datos_empresa_router
from app.routers.credito_fiscal import router as credito_fiscal_router
from app.routers.factura_electronica import router as factura_electronica_router  # noqa: E501
from app.routers.factura_exportacion import router as factura_exportacion_router  # noqa: E501
from app.routers.dtes import router as dtes_router
from app.utils.api.router import TypedAPIRouter

datos_empresa_router = TypedAPIRouter(
    router=datos_empresa_router,
    prefix="/datos_empresa",
    tags=["Datos de la Empresa"])
factura_electronica_router = TypedAPIRouter(
    router=factura_electronica_router,
    prefix="/factura",
    tags=["Documentos Tributarios Electrónicos"])
credito_fiscal_router = TypedAPIRouter(
    router=credito_fiscal_router,
    prefix="/credito_fiscal",
    tags=["Documentos Tributarios Electrónicos"])
factura_exportacion_router = TypedAPIRouter(
    router=factura_exportacion_router,
    prefix="/factura_exportacion",
    tags=["Documentos Tributarios Electrónicos"])
dtes_router = TypedAPIRouter(
    router=dtes_router,
    prefix="/dtes",
    tags=["Documentos Tributarios Electrónicos"])
