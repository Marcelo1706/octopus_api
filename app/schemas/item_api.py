from pydantic import BaseModel

from app.models.enums import TipoItem, UnidadesMedida


class ItemAPIBase(BaseModel):
    cantidad: float
    codigo: str | None = None
    uniMedida: UnidadesMedida = UnidadesMedida.UNIDAD
    descripcion: str
    precioUni: float
    montoDescu: float = 0.0
    ventaGravada: float = 0.0
    noGravado: float = 0.0


class ItemAPIFE(ItemAPIBase):
    tipoItem: TipoItem = TipoItem.BIENES
    ventaNoSuj: float = 0.0
    ventaExenta: float = 0.0
    ivaItem: float = 0.0


class ItemAPICCF(ItemAPIBase):
    tipoItem: TipoItem = TipoItem.BIENES
    ventaNoSuj: float = 0.0
    ventaExenta: float = 0.0


class ItemAPIFEX(ItemAPIBase):
    pass
