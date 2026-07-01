from __future__ import annotations

import wireup
import wireup.integration.fastapi as wireup_fastapi
from fastapi import FastAPI
from wireup._annotations import Injected
from wireup._decorators import inject_from_container
from wireup.renderer.full_page import GraphOptions
from wireup.integration.fastapi import setup

from pet_store_demo_app import factories, fastapi_services, services
from pet_store_demo_app.cbr import DemoClassBasedHandler
from pet_store_demo_app.fastapi_services import AuthService
from pet_store_demo_app.services.adoption import AdoptionService
from pet_store_demo_app.services.owners import OwnerService
from pet_store_demo_app.services.pets import PetCatalogService
from pet_store_demo_app.services.session import SQLAlchemySession

app = FastAPI(title="Wireup Pet Store Demo")


@app.get("/")
async def index() -> dict[str, str]:
    return {
        "message": "Visit /pets, /pets/{pet_id}, /pets/{pet_id}/adopt, /owners/{owner_id}, /db-session, /whoami, or /_wireup",
    }


@app.get("/pets")
async def list_pets(service: wireup.Injected[PetCatalogService]) -> dict[str, object]:
    return service.list_pets()


@app.get("/pets/{pet_id}")
async def pet_detail(pet_id: str, service: wireup.Injected[PetCatalogService]) -> dict[str, object]:
    return service.pet_detail(pet_id)


@app.post("/pets/{pet_id}/adopt")
async def adopt_pet(pet_id: str, service: wireup.Injected[AdoptionService]) -> dict[str, object]:
    return service.preview(pet_id)


@app.get("/owners/{owner_id}")
async def owner_summary(owner_id: str, service: wireup.Injected[OwnerService]) -> dict[str, object]:
    return service.summary(owner_id)


@app.get("/db-session")
async def transaction_snapshot(service: wireup.Injected[SQLAlchemySession]) -> dict[str, str]:
    return service.describe()


@app.get("/whoami")
async def whoami(service: wireup.Injected[AuthService]) -> dict[str, str]:
    return service.describe()


container = wireup.create_async_container(
    injectables=[factories, services, fastapi_services, wireup_fastapi],
    config={
        "auth": {"demo_actor": "shelter-manager"},
        "env": {"name": "demo"},
        "infra": {
            "redis": {"url": "redis://localhost:6379/0"},
            "metrics": {"endpoint": "http://metrics.internal"},
            "database": {
                "url": "postgresql+psycopg://petstore:petstore@localhost:5432/petstore",
                "schema": "adoption",
            },
        },
        "services": {"search": {"base_url": "https://search.petstore.example"}},
        "pets": {"store_name": "Happy Tails Shelter", "default_species": "cat"},
        "messaging": {"events": {"topic_prefix": "petstore-events"}},
    },
)


@inject_from_container(container)
def list_featured_pets(catalog: Injected[PetCatalogService]) -> None:
    catalog.list_pets()


setup(
    container,
    app,
    class_based_handlers=[DemoClassBasedHandler],
    add_graph_endpoint=True,
    graph_endpoint_options=GraphOptions(base_module="pet_store_demo_app"),
)
