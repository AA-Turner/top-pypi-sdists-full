import base64, uuid
from metaflow import (
    Flow,
    current,
    user_step_decorator,
    ob_highlighter,
    StepMutator,
    card,
)


def mimetype(blob):
    if blob[6:10] in (b"JFIF", b"Exif"):
        return "image/jpeg"
    elif blob[:4] == b"\xff\xd8\xff\xdb":
        return "image/jpeg"
    elif blob.startswith(b"\211PNG\r\n\032\n"):
        return "image/png"
    elif blob[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    else:
        return "application/octet-stream"


class HighlightData:
    def __init__(self):
        self.title = ""
        self._labels = []
        self._synopsis = []
        self._columns = []
        self._image = None

    def set_title(self, title):
        self.title = title

    def add_label(self, label):
        self._labels.append(label)

    def add_line(self, line, caption=""):
        self._synopsis.append(f"**{caption}** {line}")

    def add_column(self, big="", small=""):
        self._columns.append({"big": big, "small": small})

    def set_image(self, img):
        mime = mimetype(img)
        encoded = base64.b64encode(img).decode("ascii")
        self._image = f"data:{mime};base64,{encoded}"

    def _modified(self):
        return any(self._serialize().values())

    def _serialize(self):
        if self._image:
            htype = "image"
            hbody = {"src": self._image}
        else:
            htype = "columns"
            hbody = self._columns
        return {
            "type": "highlight",
            "id": f"highlight-{uuid.uuid4()}",
            "title": self.title,
            "labels": self._labels,
            "synopsis": self._synopsis,
            "highlight_type": htype,
            "highlight_body": hbody,
        }


@user_step_decorator
def ob_highlighter_api(step_name, flow, inputs=None, attributes=None):
    flow.highlight = HighlightData()
    try:
        yield
        if flow.highlight._modified():
            Flow(current.flow_name)[current.run_id].add_tag("highlight")
        flow.highlight_data = flow.highlight._serialize()
    finally:
        del flow.highlight


class highlight(StepMutator):
    def mutate(self, mutable_step):
        # ob_highlighter_api manages the self.highlight handle
        mutable_step.add_decorator(ob_highlighter_api)
        # ob_highlighter is required to add a metadata entry
        mutable_step.add_decorator(ob_highlighter)
        # add a highlight card itself
        mutable_step.add_decorator(card, deco_kwargs={"type": "highlight"})
