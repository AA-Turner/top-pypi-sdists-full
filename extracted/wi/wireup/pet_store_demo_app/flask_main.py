from __future__ import annotations

import wireup
import wireup.integration.flask as wireup_flask
from flask import Flask
from wireup.integration.flask import GraphEndpointOptions, setup

from pet_store_demo_app import factories
from pet_store_demo_app.services.adoption import AdoptionService
from pet_store_demo_app.services.audit import AuditService
from pet_store_demo_app.services.infra import MetricsClient, RedisConnection, ShelterStore
from pet_store_demo_app.services.owners import OwnerService
from pet_store_demo_app.services.pets import PetCatalogService
from pet_store_demo_app.services.session import SQLAlchemySession

app = Flask(__name__)


@app.get("/")
def index() -> dict[str, str]:
    return {
        "message": "Visit /pets, /pets/adoption-preview, /owners/demo-owner, /db-session, or /_wireup",
    }


@app.get("/pets")
def list_pets(service: wireup.Injected[PetCatalogService]) -> dict[str, object]:
    return service.list_pets()


@app.get("/pets/adoption-preview")
def adoption_preview(service: wireup.Injected[AdoptionService]) -> dict[str, object]:
    return service.preview("pet-123")


@app.get("/owners/demo-owner")
def owner_summary(service: wireup.Injected[OwnerService]) -> dict[str, object]:
    return service.summary("demo-owner")


@app.get("/db-session")
def db_session(service: wireup.Injected[SQLAlchemySession]) -> dict[str, str]:
    return service.describe()


container = wireup.create_sync_container(
    injectables=[
        factories,
        RedisConnection,
        MetricsClient,
        ShelterStore,
        AuditService,
        SQLAlchemySession,
        PetCatalogService,
        AdoptionService,
        OwnerService,
        wireup_flask,
    ],
    config={
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

setup(
    container,
    app,
    add_graph_endpoint=True,
    graph_endpoint_options=GraphEndpointOptions(base_module="pet_store_demo_app"),
)


if __name__ == "__main__":
    app.run(debug=True)
