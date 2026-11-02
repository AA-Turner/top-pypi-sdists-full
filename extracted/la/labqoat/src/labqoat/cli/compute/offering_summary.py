"""The hardware catalog as an agent picks from it: one line per GPU model it may buy."""

from decimal import Decimal

from labqoat.json_document import JsonDocument, JsonValue


class OfferingSummary:
    """Summarize purchasable shapes; the raw catalog of every shape in every location stays behind --all."""

    @staticmethod
    def summarize(items: list[JsonDocument], gpu: str | None) -> JsonDocument:
        """GPU models with their cheapest shape, or the shapes of one model when ``gpu`` names it."""
        usable = [item for item in items if item.get("selected")]
        if gpu is not None:
            shapes = [OfferingSummary.shape(item) for item in usable if OfferingSummary.model(item) == gpu]
            ordered: list[JsonValue] = sorted(shapes, key=OfferingSummary.price)
            return JsonDocument(gpu=gpu, shapes=ordered)
        models = OfferingSummary.models(usable)
        unused: list[JsonValue] = [model for model in OfferingSummary.models(items) if model not in models]
        cpu = [OfferingSummary.shape(item) for item in usable if OfferingSummary.model(item) is None]
        cheapest_cpu: JsonValue = min(cpu, key=OfferingSummary.price) if cpu else None
        lines: list[JsonValue] = [OfferingSummary.gpu_line(model, usable) for model in models]
        return JsonDocument(
            gpus=lines,
            cpu={"shapes": len(cpu), "cheapest": cheapest_cpu},
            not_enabled=unused,
            next="lab compute offerings --gpu MODEL lists a model's shapes; --all prints the whole catalog",
        )

    @staticmethod
    def models(items: list[JsonDocument]) -> list[str]:
        """The distinct GPU models among the items, sorted."""
        return sorted({model for model in map(OfferingSummary.model, items) if model is not None})

    @staticmethod
    def gpu_line(model: str, items: list[JsonDocument]) -> dict[str, JsonValue]:
        """One GPU model: memory, GPUs per machine, cheapest shape and where it is sold."""
        shapes = sorted(
            (OfferingSummary.shape(i) for i in items if OfferingSummary.model(i) == model), key=OfferingSummary.price
        )
        cheapest = shapes[0]
        counts: list[JsonValue] = [*sorted({int(str(shape["gpus"])) for shape in shapes})]
        locations: list[JsonValue] = [*sorted({str(shape["location"]) for shape in shapes})]
        return {
            "gpu": model,
            "gpu_memory_gb": cheapest["gpu_memory_gb"],
            "gpus_per_machine": counts,
            "cheapest": {key: cheapest[key] for key in ("shape", "hourly_rate", "location")},
            "locations": locations,
        }

    @staticmethod
    def shape(item: JsonDocument) -> dict[str, JsonValue]:
        """One purchasable machine in human units."""
        resources = JsonDocument.expect_dict(item.get("resources", {}))
        price = JsonDocument.expect_dict(item.get("price", {}))
        shape: dict[str, JsonValue] = {"shape": item.get("shape"), "location": item.get("location_id")}
        if resources.get("gpu_count"):
            shape["gpus"] = resources["gpu_count"]
            shape["gpu_memory_gb"] = round(int(str(resources.get("gpu_memory_mb", 0))) / 1024)
        shape["vcpus"] = resources.get("physical_vcpus")
        shape["memory_gb"] = round(int(str(resources.get("memory_mb", 0))) / 1024)
        shape["hourly_rate"] = str(Decimal(str(price.get("hourly_rate", "0"))).quantize(Decimal("0.01")))
        return shape

    @staticmethod
    def model(item: JsonDocument) -> str | None:
        """The GPU model of a shape, or None for a CPU shape."""
        resources = JsonDocument.expect_dict(item.get("resources", {}))
        model = resources.get("gpu_model")
        return str(model) if model and resources.get("gpu_count") else None

    @staticmethod
    def price(shape: JsonValue) -> Decimal:
        """Sort key: the hourly price of a shape built by ``shape``."""
        return Decimal(str(JsonDocument.expect_dict(shape)["hourly_rate"]))
