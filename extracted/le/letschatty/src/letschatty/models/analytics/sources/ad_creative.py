from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


class AdCreative(BaseModel):
    """El creativo que Meta sirvió en UN referral puntual.

    Vive en el touchpoint, no en la fuente, porque un mismo `ad_id` puede servir varios
    creativos: anuncios dinámicos, catálogo, carrusel, o simplemente editar el anuncio —
    el `ad_id` sobrevive a la edición. Medido en producción sobre el anuncio
    `120252665872680019`: 15 chats entraron con el titular «Consultanos ✨» sobre una mesa
    de comedor y uno con «Chatea con nosotros» sobre un sillón, todos bajo la MISMA
    fuente. Guardarlo en la fuente hace que gane el creativo del primer lead y que todos
    los demás hereden una imagen —y un texto— que no es la suya.

    Se copia al ingresar el referral y no después: las URLs del CDN de Meta van firmadas
    con vencimiento en `oe=` (del orden de una semana), así que la imagen que no se copia
    en el momento se perdió. `image_url`/`thumbnail_url` conservan la original de Meta
    para trazabilidad aunque ya no resuelva; `mirror_url` es nuestra copia, que no caduca.
    """
    headline: Optional[str] = Field(default=None, description="El titular tal como vino en ESTE referral")
    body: Optional[str] = Field(default=None, description="El cuerpo tal como vino en ESTE referral")
    media_type: Optional[str] = Field(default=None, description='"image" | "video" | "" según lo que haya mandado Meta')
    image_url: Optional[str] = Field(default=None, description="La URL original de Meta, firmada y con vencimiento. Se guarda para trazabilidad: deja de resolver a los ~7 días, así que para mostrar la imagen va `mirror_url`.")
    video_url: Optional[str] = Field(default=None, description="El video original de Meta, si el anuncio era de video. No se espeja: sólo copiamos la imagen/thumbnail.")
    thumbnail_url: Optional[str] = Field(default=None, description="El thumbnail original de Meta, firmado y con vencimiento. Meta manda `image_url` o `thumbnail_url` según el formato del anuncio, casi nunca las dos.")
    permalink: Optional[str] = Field(default=None, description="`referral.source_url`: el link al anuncio o al posteo original")
    mirror_url: Optional[str] = Field(default=None, description="Nuestra copia de la imagen en S3, la única que no caduca. Puede quedar vacía si el CDN falló al ingresar el referral, y en ese caso el touchpoint conserva igual el texto y la URL original.")
