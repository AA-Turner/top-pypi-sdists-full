from datetime import datetime, timedelta
from enum import StrEnum
from zoneinfo import ZoneInfo

from pydantic import (
    AfterValidator, AwareDatetime, BaseModel, ConfigDict, Field, NonNegativeFloat, PositiveInt,
    TypeAdapter, ValidationError, ValidationInfo, field_validator, model_validator,
)
import logging
from typing import Annotated, Any, Optional, ClassVar
from ...base_models.chatty_asset_model import CompanyAssetModel
from ...base_models.helpers import _normalize_precision
from ...utils.types.identifier import StrObjectId
from .sin_producto import SIN_PRODUCTO


class SaleStatus(StrEnum):
    DRAFT = "DRAFT"
    OFFERED = "OFFERED"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PaymentStatus(StrEnum):
    UNPAID = "UNPAID"
    PARTIAL = "PARTIAL"
    PAID = "PAID"
    OVERPAID = "OVERPAID"
    REFUNDED = "REFUNDED"


#: Cuánto puede quedar `sold_at` por delante del reloj del servidor. No es para aceptar
#: ventas futuras: es para que una venta cargada "ahora" desde una PC con el reloj un par
#: de minutos adelantado no rebote.
TOLERANCIA_RELOJ_FECHA_DE_VENTA = timedelta(minutes=5)

#: Piso de cordura, no de negocio: ataja un año mal tipeado ("0202") antes de guardarlo.
FECHA_DE_VENTA_MINIMA = datetime(2000, 1, 1, tzinfo=ZoneInfo("UTC"))


def _a_utc(fecha: datetime) -> datetime:
    """UTC y al milisegundo, que es lo que guarda Mongo.

    Una fecha sin zona se toma como UTC porque así vuelven de Mongo. Sin recortar al
    milisegundo, la fecha que se escribe y la que se relee no serían iguales.
    """
    utc = fecha.replace(tzinfo=ZoneInfo("UTC")) if fecha.tzinfo is None else fecha.astimezone(ZoneInfo("UTC"))
    return _normalize_precision(utc)


def _no_futura(fecha: datetime) -> datetime:
    if fecha > datetime.now(ZoneInfo("UTC")) + TOLERANCIA_RELOJ_FECHA_DE_VENTA:
        raise ValueError("La fecha de venta no puede ser futura")
    return fecha


def _no_anterior_a_la_minima(fecha: datetime) -> datetime:
    if fecha < FECHA_DE_VENTA_MINIMA:
        raise ValueError("La fecha de venta no puede ser anterior al 2000")
    return fecha


#: La fecha de venta tal como la acepta quien REGISTRA o EDITA una venta (la frontera):
#:
#: - Con zona horaria explícita. "2026-09-15T22:00" sin zona es ambiguo: el servidor lo
#:   leería como UTC y una venta de las 22 h de Buenos Aires pasaría al día siguiente.
#: - No futura: una venta que todavía no pasó no se registra.
#: - No anterior al 2000: un año mal tipeado se ataja acá y no queda guardado.
#:
#: `Sale` no repite estas reglas a propósito. Lo que ya está guardado se tiene que poder
#: leer siempre: si una fecha rara llegara a la base por otro camino, no puede tumbar la
#: carga del chat, que es donde se leen las ventas.
FechaDeVenta = Annotated[
    AwareDatetime,
    AfterValidator(_a_utc),
    AfterValidator(_no_futura),
    AfterValidator(_no_anterior_a_la_minima),
]


logger = logging.getLogger("sale")

#: Coerción de enteros como la de pydantic en modo lax (2.0 y "2" → 2), la misma que
#: aplicaba el modelo de antes a `quantity`.
_ENTERO = TypeAdapter(int)

#: Tope de líneas por venta: acota el documento y el texto de la notificación del chat.
MAXIMO_DE_LINEAS_POR_VENTA = 50

#: Cuántos productos se nombran en el texto de una venta antes de resumir con "y N más".
_PRODUCTOS_NOMBRADOS_EN_EL_TITULO = 2


class SaleItem(BaseModel):
    """Una línea de la venta: qué producto, cuántos y a qué precio unitario.

    Sin reglas de negocio a propósito, igual que `Sale`: lo guardado se tiene que poder
    leer siempre. Las reglas (cantidad ≥ 1, precio ≥ 0, producto real) viven en la
    frontera, `SaleItemRequest`.
    """
    product_id: StrObjectId
    product_name: Optional[str] = Field(
        default=None,
        description=(
            "El nombre del producto al momento de la venta. Es una foto: si el producto se "
            "renombra o se borra, la venta se sigue viendo como se vendió. Lo completa el "
            "servidor desde el catálogo; las ventas guardadas antes de las líneas no lo tienen."
        ),
    )
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


def _linea_de_una_venta_de_un_producto(product_id: StrObjectId, quantity: Any, total_amount: Any) -> dict:
    """La línea de una venta guardada antes de que existieran las líneas.

    Hasta ahora una venta era un producto: `product_id`, `quantity` y `total_amount`. El
    precio unitario sale de dividir, que es exactamente como el frontend armaba
    `details.items` desde marzo de 2026.
    """
    try:
        cantidad = _ENTERO.validate_python(quantity)
    except ValidationError:
        cantidad = 1  # sin cantidad legible, una unidad (el precio queda = total)
    total = float(total_amount or 0)
    return {"product_id": product_id, "quantity": cantidad, "unit_price": total / cantidad if cantidad else total}


def _lineas_validas(crudo: Any) -> Optional[list[SaleItem]]:
    """Las líneas, si todas validan; si no, `None`. Nunca levanta: esto corre al leer."""
    if not isinstance(crudo, list):
        return None
    try:
        return [SaleItem.model_validate(linea) for linea in crudo]
    except ValidationError:
        return None


def _lineas_guardadas_en_details(crudo: Any, product_id: Any, quantity: Any) -> Optional[list[SaleItem]]:
    """Las líneas que el frontend guarda en `details.items` desde el 17-mar-2026.

    Son 15.313 ventas, todas con una sola línea y consistentes con `product_id` y
    `quantity` (verificado en prod). Se usan sólo si coinciden con esos dos, que en estas
    ventas son los que mandan: `details` es un dict libre, y una integración puede traer
    ahí cualquier cosa. Siete tienen `unit_price: null`: si una línea no valida no se usa
    ninguna, y la venta se lee como una venta de un producto, que da lo mismo.
    """
    lineas = _lineas_validas(crudo)
    if not lineas:
        return None
    if lineas[0].product_id != product_id or sum(linea.quantity for linea in lineas) != quantity:
        return None
    return lineas


class Sale(CompanyAssetModel):
    """Una venta. Tiene líneas (`items`) o es "sólo monto" (`items` vacía).

    `items` es la fuente de verdad. `product_id` y `quantity` existen porque todo lo que
    lee ventas hoy los lee —el chat, analytics, el export, 35 servicios con su propia
    versión del paquete— y se calculan siempre desde las líneas: nunca se escriben a mano.
    `product_id` nunca es `null`: en una venta sin productos es `SIN_PRODUCTO`.
    """
    chat_id: StrObjectId
    items: list[SaleItem] = Field(
        default_factory=list,
        description="Las líneas de la venta. Vacía = venta sólo monto (un total y un concepto).",
    )
    name: Optional[str] = Field(
        default=None,
        description="Qué se vendió, en palabras del agente. Es el nombre de una venta sin productos.",
    )
    product_id: StrObjectId = Field(description="El producto de la primera línea, o SIN_PRODUCTO. Derivado de `items`.")
    quantity: int = Field(description="La suma de las cantidades de las líneas, o 1 sin líneas. Derivado de `items`.")
    total_amount: float = Field(description="Lo que se COBRÓ. Con líneas puede diferir de la suma de subtotales: la diferencia es un ajuste.")
    currency: str
    paid_amount: float
    installments: int
    details: dict
    crm_id: Optional[str] = Field(default=None)
    creator_id: StrObjectId
    sale_status: Optional[SaleStatus] = Field(default=None)
    payment_status: Optional[PaymentStatus] = Field(default=None)
    sold_at: datetime = Field(
        default=None,
        validate_default=True,
        description=(
            "Cuándo OCURRIÓ la venta. Puede ser anterior a created_at, que es cuándo se "
            "REGISTRÓ en Chatty: una venta cerrada el lunes y cargada el jueves tiene "
            "sold_at=lunes y created_at=jueves. Si no se informa, la venta ocurrió al "
            "registrarse."
        ),
    )

    #: Sin esto `sold_at` llega a Mongo como string y los rangos de fecha no lo encuentran
    #: (ver `ChattyAssetModel.database_datetime_fields`).
    database_datetime_fields: ClassVar[set[str]] = {"sold_at"}

    @model_validator(mode="before")
    @classmethod
    def _lineas_y_sus_derivados(cls, data: Any) -> Any:
        """Las líneas, de donde estén, y `product_id`/`quantity` calculados desde ellas.

        Una venta se lee de tres formas, en este orden:

        1. `items`: lo que se escribe desde que existen las líneas.
        2. `details.items`: lo que el frontend guarda desde marzo, que nadie leía.
        3. `product_id` + `quantity` + `total_amount`: toda venta anterior.

        Así se leen las 29.484 ventas guardadas sin migrar ninguna, y una venta vieja da
        el mismo `product_id` y la misma `quantity` que tenía.
        """
        if not isinstance(data, dict):
            return data
        datos = dict(data)
        lineas = cls._lineas_de(datos)
        datos["items"] = lineas
        datos["product_id"] = lineas[0].product_id if lineas else SIN_PRODUCTO
        datos["quantity"] = sum(linea.quantity for linea in lineas) if lineas else 1
        return datos

    @staticmethod
    def _lineas_de(datos: dict) -> list[SaleItem]:
        if datos.get("items") is not None:
            lineas = _lineas_validas(datos["items"])
            if lineas is not None:
                return lineas
            # Nunca debería pasar (se validan al escribir): se lee por `product_id` antes
            # que dejar la venta —y el chat que la carga— sin poder leerse.
            logger.error(f"Sale {datos.get('_id') or datos.get('id')} has unreadable items, reading it from product_id")
        detalle = datos.get("details")
        if isinstance(detalle, dict):
            guardadas = _lineas_guardadas_en_details(detalle.get("items"), datos.get("product_id"), datos.get("quantity"))
            if guardadas is not None:
                return guardadas
        product_id = datos.get("product_id")
        if product_id and product_id != SIN_PRODUCTO:
            return [SaleItem.model_validate(
                _linea_de_una_venta_de_un_producto(product_id, datos.get("quantity"), datos.get("total_amount"))
            )]
        return []

    @field_validator("sold_at", mode="before")
    @classmethod
    def _por_defecto_ocurrio_al_registrarse(cls, v: Optional[datetime], info: ValidationInfo) -> Optional[datetime]:
        """Sin fecha informada, la venta ocurrió al registrarse.

        Es también cómo se leen las ventas guardadas antes de que existiera el campo, así
        que no hace falta migrarlas: hasta hoy fecha de venta y fecha de registro eran la
        misma cosa.
        """
        return info.data.get("created_at") if v is None else v

    @field_validator("sold_at", mode="after")
    @classmethod
    def _en_utc(cls, v: datetime) -> datetime:
        return _a_utc(v)

    @property
    def tiene_productos(self) -> bool:
        return bool(self.items)

    def ids_de_productos(self) -> list[StrObjectId]:
        """Los productos de la venta, sin repetir, en el orden de las líneas."""
        return list(dict.fromkeys(linea.product_id for linea in self.items))

    def productos_sin_nombre(self) -> set[StrObjectId]:
        """Los productos de líneas que todavía no tienen la foto del nombre."""
        return {linea.product_id for linea in self.items if linea.product_name is None}

    def con_nombres_de_productos(self, nombres: dict[StrObjectId, str]) -> "Sale":
        """La misma venta con el nombre puesto en las líneas que no lo tenían.

        Las que ya lo tienen lo conservan: es la foto del momento de la venta.
        """
        lineas = [
            linea if linea.product_name is not None or linea.product_id not in nombres
            else linea.model_copy(update={"product_name": nombres[linea.product_id]})
            for linea in self.items
        ]
        # `model_copy` no revalida: vale porque sólo cambian nombres, nunca productos ni
        # cantidades (de los que salen `product_id` y `quantity`).
        return self.model_copy(update={"items": lineas})

    def titulo(self, accion: Optional[str] = None) -> str:
        """Cómo se nombra la venta en el chat (highlight y notificación central).

        "Venta de Plan anual", "Venta actualizada de Plan anual y Soporte",
        "Venta de Frutos secos, Yerbas y 11 más", "Venta: Pedido de almacén",
        "Venta sin productos". Con un producto el texto es idéntico al de siempre.
        """
        partes = ["Venta"] + ([accion] if accion else [])
        return " ".join(partes) + self._que_se_vendio()

    def _que_se_vendio(self) -> str:
        if not self.items:
            return f": {self.name}" if self.name else " sin productos"
        por_producto = {linea.product_id: linea.product_name for linea in self.items}
        nombres = [nombre for nombre in por_producto.values() if nombre]
        if len(nombres) != len(por_producto):
            return f" de {len(por_producto)} producto{'s' if len(por_producto) != 1 else ''}"
        if len(nombres) == 1:
            return f" de {nombres[0]}"
        if len(nombres) == 2:
            return f" de {nombres[0]} y {nombres[1]}"
        visibles = ", ".join(nombres[:_PRODUCTOS_NOMBRADOS_EN_EL_TITULO])
        return f" de {visibles} y {len(nombres) - _PRODUCTOS_NOMBRADOS_EN_EL_TITULO} más"

    def con_cambios(self, edicion: "SaleUpdate") -> "Sale":
        """La venta con la edición aplicada. Lo que la edición no trae, se conserva.

        Reemplaza al `update` genérico, que armaba una venta ENTERA con el body antes de
        mezclar: lo que el frontend no mandaba se convertía en un valor por defecto y
        pisaba lo guardado (así se perdieron los `details.items` de 166 ventas editadas).
        Acá se mezcla sólo lo que vino, y recién después se valida la venta completa.
        """
        cambios = edicion.cambios()
        self._verificar_montos(cambios)
        if "details" in cambios:
            cambios["details"] = {**self.details, **cambios["details"]}
        campos_viejos = {campo: cambios.pop(campo) for campo in ("product_id", "quantity") if campo in cambios}
        if "items" in cambios:
            self._verificar_que_los_campos_viejos_son_eco(campos_viejos, cambios["items"])
            cambios["items"] = self._conservando_los_nombres(cambios["items"])
        elif campos_viejos:
            cambios.update(self._lineas_segun_campos_viejos(campos_viejos, cambios.get("total_amount", self.total_amount)))
        return self.update_from_dict(**cambios)

    def _verificar_montos(self, cambios: dict) -> None:
        """Cantidad ≥ 1 y montos ≥ 0, pero sólo si la edición los CAMBIA.

        El frontend de hoy devuelve la venta entera en cada edición: una venta guardada con
        un valor que hoy no se aceptaría tiene que seguir pudiendo editarse en lo demás.
        """
        for campo, minimo in (("quantity", 1), ("total_amount", 0), ("paid_amount", 0)):
            if campo in cambios and cambios[campo] != getattr(self, campo) and cambios[campo] < minimo:
                raise EdicionDeVentaInvalida(f"{campo} no puede ser menor que {minimo}")

    def _verificar_que_los_campos_viejos_son_eco(self, campos: dict, lineas: list[dict]) -> None:
        """Con `items`, `product_id`/`quantity` sueltos tienen que decir lo mismo que las
        líneas nuevas o repetir lo que la venta ya tenía (un cliente que devuelve la venta
        entera con las líneas cambiadas). Otra cosa no se puede interpretar."""
        nuevo_producto = lineas[0]["product_id"] if lineas else SIN_PRODUCTO
        nueva_cantidad = sum(linea["quantity"] for linea in lineas) if lineas else 1
        if campos.get("product_id", nuevo_producto) not in (nuevo_producto, self.product_id):
            raise EdicionDeVentaInvalida("product_id no coincide con el producto de la primera línea de items")
        if campos.get("quantity", nueva_cantidad) not in (nueva_cantidad, self.quantity):
            raise EdicionDeVentaInvalida("quantity no coincide con la suma de las cantidades de items")

    def _conservando_los_nombres(self, lineas: list[dict]) -> list[dict]:
        """Las líneas nuevas, con la foto del nombre de los productos que la venta ya tenía."""
        nombres = {linea.product_id: linea.product_name for linea in self.items if linea.product_name}
        return [{**linea, "product_name": nombres.get(linea["product_id"])} for linea in lineas]

    def _lineas_segun_campos_viejos(self, campos: dict, total_amount: float) -> dict:
        """Una edición con `product_id`/`quantity` sueltos: la que manda el frontend viejo.

        Esos campos son derivados de las líneas, así que se leen como un pedido de cambiar
        la línea. Si repiten lo que la venta ya tiene (el frontend viejo manda la venta
        entera), no tocan nada: es un eco. Si cambian y la venta tiene una línea o ninguna,
        esa línea se rehace como la armaba el frontend viejo (precio = total / cantidad).
        Si cambian y la venta tiene varias, no hay forma de saber a cuál se refieren.
        """
        product_id = campos.get("product_id", self.product_id)
        quantity = campos.get("quantity", self.quantity)
        cambia_la_linea = product_id != self.product_id or quantity != self.quantity
        if product_id == SIN_PRODUCTO:
            if self.items:
                raise EdicionDeVentaInvalida(
                    "Para dejar la venta sin productos, mandá items vacía."
                )
            # Venta sin productos y la edición no nombra ninguno (o repite el id reservado
            # que leyó): `quantity` no significa nada.
            return {}
        if len(self.items) > 1:
            if cambia_la_linea:
                raise EdicionDeVentaInvalida(
                    "Esta venta tiene varios productos: para cambiarlos, mandá las líneas en `items`."
                )
            return {}
        if not cambia_la_linea and (total_amount == self.total_amount or not self._precio_sale_del_total()):
            # Sólo cambió el total de una línea con precio propio: el precio no se toca y
            # la diferencia queda como ajuste (un descuento, por ejemplo).
            return {}
        linea = _linea_de_una_venta_de_un_producto(product_id, quantity, total_amount)
        return {"items": self._conservando_los_nombres([linea])}

    def _precio_sale_del_total(self) -> bool:
        """Si la única línea tiene el precio que resulta de dividir el total por la cantidad:
        la forma de toda venta de antes de las líneas, cuyo precio el frontend viejo sigue
        expresando a través del total."""
        if len(self.items) != 1:
            return False
        return abs(self.items[0].subtotal - self.total_amount) < 0.005

    def mismos_datos_que(self, otra: "Sale") -> bool:
        """Si dos versiones de la venta guardarían lo mismo (sin contar `updated_at`).

        `Sale == Sale` compara sólo el id (`ChattyAssetModel.__eq__`), así que no sirve
        para saber si una edición cambió algo.
        """
        return self.model_dump(exclude={"updated_at"}) == otra.model_dump(exclude={"updated_at"})


class EdicionDeVentaInvalida(ValueError):
    """Una edición que no se puede aplicar a ESTA venta (p. ej. cambiar "el" producto de
    una venta que tiene varios). Es un error del pedido, no del servidor: api-chatty
    contesta 400 con el motivo."""


def _no_es_el_id_reservado(product_id: StrObjectId) -> StrObjectId:
    if product_id == SIN_PRODUCTO:
        raise ValueError("Ese id no es un producto: una venta sin productos se manda con items vacía")
    return product_id


class SaleItemRequest(BaseModel):
    """Una línea tal como llega de quien registra o edita la venta."""
    product_id: Annotated[StrObjectId, AfterValidator(_no_es_el_id_reservado)]
    quantity: PositiveInt
    unit_price: NonNegativeFloat


def _verificar_que_coinciden(
    items: Optional[list[SaleItemRequest]], product_id: Optional[StrObjectId], quantity: Optional[int],
) -> None:
    """`product_id`/`quantity` sueltos junto con `items` tienen que decir lo mismo.

    Se calculan desde las líneas; si un cliente los manda distintos no hay forma de saber
    cuál de los dos quería, y se rechaza en vez de elegir en silencio.
    """
    if items is None:
        return
    esperado_producto = items[0].product_id if items else SIN_PRODUCTO
    esperada_cantidad = sum(linea.quantity for linea in items) if items else 1
    if product_id is not None and product_id != esperado_producto:
        raise ValueError("product_id no coincide con el producto de la primera línea de items")
    if quantity is not None and quantity != esperada_cantidad:
        raise ValueError("quantity no coincide con la suma de las cantidades de items")


class SaleRequest(BaseModel):
    """Una venta nueva, tal como llega de quien la registra (frontend, integración, IA).

    Dos formas, las dos válidas:

    - Con `items`: la lista de líneas. Vacía = venta sin productos (conviene un `name`).
    - Con `product_id` + `quantity`: una venta de un producto, como hasta ahora. Es lo que
      manda `POST /phone/{phone}/sale`, el endpoint de integraciones.
    """
    items: Optional[list[SaleItemRequest]] = Field(
        default=None,
        max_length=MAXIMO_DE_LINEAS_POR_VENTA,
        description="Las líneas de la venta. Vacía = venta sin productos.",
    )
    product_id: Optional[Annotated[StrObjectId, AfterValidator(_no_es_el_id_reservado)]] = Field(
        default=None, description="Una venta de un producto, sin items (la forma de siempre).",
    )
    quantity: Optional[PositiveInt] = Field(default=None, description="Con product_id: cuántas unidades.")
    name: Optional[str] = Field(default=None, description="Qué se vendió. Es el nombre de una venta sin productos.")
    creator_id: StrObjectId
    total_amount: NonNegativeFloat
    currency: str
    paid_amount: NonNegativeFloat
    installments: int
    details: dict = Field(default_factory=dict)
    crm_id: Optional[str] = Field(default=None, description="N° de orden o id de la venta en el sistema del cliente.")
    sold_at: Optional[FechaDeVenta] = Field(
        default=None,
        description=(
            "Cuándo ocurrió la venta, ISO 8601 con zona horaria "
            "(p. ej. 2026-09-15T12:00:00-03:00). No puede ser futura ni anterior al 2000. "
            "Al crear, sin fecha la venta ocurrió al registrarse; al editar, sin fecha "
            "(o null) se conserva la que tenía."
        ),
    )

    @model_validator(mode="after")
    def _con_productos_o_sin_ellos_pero_dicho(self) -> "SaleRequest":
        if self.items is None and self.product_id is None:
            raise ValueError(
                "Faltan los productos: mandá items (vacía si la venta no tiene productos) o product_id y quantity"
            )
        if self.items is None and self.quantity is None:
            raise ValueError("Con product_id hace falta quantity")
        _verificar_que_coinciden(self.items, self.product_id, self.quantity)
        return self

    def example_payload(self):
        return {
            "items": [
                {"product_id": "6756ef4959e496069bee54d8", "quantity": 2, "unit_price": 50},
            ],
            "creator_id": "6756ef4959e496069bee54d8",
            "total_amount": 100,
            "currency": "USD",
            "paid_amount": 100,
            "installments": 1,
            "details": {},
            "sold_at": "2026-09-15T12:00:00-03:00"
        }


#: Los campos que una edición puede vaciar mandando `null`. En los demás un `null` no
#: significa nada y se ignora: es lo que ya pasaba con `sold_at` (`SaleRequest` vuelca
#: `None` cuando no se informó, y eso no puede convertirse en "borrá la fecha").
_CAMPOS_QUE_SE_PUEDEN_VACIAR = frozenset({"name", "crm_id", "sale_status", "payment_status"})


class SaleUpdate(BaseModel):
    """Una edición de una venta: sólo lo que vino.

    - Ausente → se conserva.
    - `null` → vacía el campo si puede estar vacío (`_CAMPOS_QUE_SE_PUEDEN_VACIAR`); en los
      obligatorios se ignora.
    - `details` se mezcla por clave; `items` se reemplaza entera cuando viene.
    - Cantidad y montos se verifican en `Sale.con_cambios`, sólo si cambian.

    Campos que no se editan (`id`, `chat_id`, `creator_id`, `created_at`…) se ignoran: el
    frontend actual los manda en cada edición.
    """
    model_config = ConfigDict(extra="ignore")

    items: Optional[list[SaleItemRequest]] = Field(default=None, max_length=MAXIMO_DE_LINEAS_POR_VENTA)
    #: Acá sí se acepta `SIN_PRODUCTO`: quien lee una venta sin productos y la devuelve
    #: entera manda el id reservado, y eso es un eco, no un pedido.
    product_id: Optional[StrObjectId] = None
    #: Cantidad y montos sin límites acá: `Sale.con_cambios` los verifica sólo si CAMBIAN,
    #: para que el eco de una venta guardada con un valor de antes no la vuelva ineditable.
    quantity: Optional[int] = None
    name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    paid_amount: Optional[float] = None
    installments: Optional[int] = None
    details: Optional[dict] = None
    crm_id: Optional[str] = None
    sold_at: Optional[FechaDeVenta] = None
    sale_status: Optional[SaleStatus] = None
    payment_status: Optional[PaymentStatus] = None

    def cambios(self) -> dict[str, Any]:
        """Lo que la edición pide cambiar, con la regla de `null` aplicada."""
        enviados = self.model_dump(exclude_unset=True)
        return {
            campo: valor for campo, valor in enviados.items()
            if valor is not None or campo in _CAMPOS_QUE_SE_PUEDEN_VACIAR
        }
