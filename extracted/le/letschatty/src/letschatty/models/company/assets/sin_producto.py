"""El `product_id` de una venta que no tiene productos.

Una venta "sólo monto" no tiene producto, pero su `product_id` no puede ser `null`: la
referencia de la venta vive dentro del chat (`client.sales[].product_id`) y a ese chat lo
reconstruyen entero servicios que llevan su propia versión de letschatty —34 de
cintia-lambdas, de 0.4.425 a 0.4.526, y copilot_v2— en todas las cuales el campo es un
`StrObjectId` obligatorio. Con un `null` ahí, esos servicios dejan de poder leer el chat
(la IA no responde, los workflows no disparan) sin ningún error visible.

Por eso el campo lleva este id reservado en los tres lugares donde viaja: el documento de
`sales`, la referencia del chat y el evento. Nunca es un producto: `Product` lo rechaza.
Mismo recurso que `COEXISTENCE_ECHO_SENT_BY_ID` en api-chatty.
"""
from ...utils.types.identifier import StrObjectId

SIN_PRODUCTO: StrObjectId = "5a1e5a1e5a1e5a1e5a1e5a1e"
