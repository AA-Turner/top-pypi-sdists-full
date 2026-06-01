import logging
import os
from uuid import UUID

import orjson
import semantic_version
from beartype import beartype
from deprecation import deprecated
from requests import Session

import picsellia
from picsellia import utils
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.exceptions import PicselliaError
from picsellia.sdk.annotation_campaign import AnnotationCampaign
from picsellia.sdk.connection import Connection
from picsellia.sdk.datalake import Datalake
from picsellia.sdk.dataset import Dataset
from picsellia.sdk.dataset_version import DatasetVersion
from picsellia.sdk.datasource import DataSource
from picsellia.sdk.deployment import Deployment
from picsellia.sdk.experiment import Experiment
from picsellia.sdk.job import Job
from picsellia.sdk.model import Model
from picsellia.sdk.model_version import ModelVersion
from picsellia.sdk.processing import Processing
from picsellia.sdk.project import Project
from picsellia.sdk.review_campaign import ReviewCampaign
from picsellia.sdk.tag import Tag
from picsellia.sdk.user import User
from picsellia.services.datasource import DataSourceService
from picsellia.types.enums import InferenceType, ProcessingType, TagTarget
from picsellia.types.schemas import OrganizationSchema
from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


class Client:
    """Picsellia SDK Client can be used to communicate with Picsellia services.
    You need an API Token, available on web platform in Profile Settings > Token.
    From this client object, you will be able to retrieve python objects representing your data in the platform.

    Examples:
        ```python
        client = Client(api_token="a0c9f3bbf7e8bc175494fc44bfc6f89aae3eb9d0")
        ```

    Arguments:
        api_token (str, optional): your api token, that can be found on the web platform.
            Defaults to None, client will try to find it into your environment variable as 'PICSELLIA_TOKEN'
        organization_id: (str or UUID, optional): Specify an organization to connect to by giving its id.
            Defaults to None, you will be connected to your main Organization.
        organization_name: (str, optional): Specify an organization to connect to by giving its name.
            If id is also given, client will use organization_id.
            Defaults to None, you will be connected to your main Organization.
        host (str, optional): Define a custom host used for platform.
            Defaults to our Picsellia environment "https://app.picsellia.com".
        session (requests.Session, optional): Set up your own requests.Session object to add headers or proxies.
    """

    def __init__(
        self,
        api_token: str | None = None,
        organization_id: str | UUID | None = None,
        organization_name: str | None = None,
        host: str = "https://app.picsellia.com",
        session: Session | None = None,
    ):
        if api_token is None:
            if "PICSELLIA_TOKEN" in os.environ:
                token = os.environ["PICSELLIA_TOKEN"]
            else:
                raise PicselliaError(
                    "Please set up the PICSELLIA_TOKEN environment variable or specify your token"
                )
        else:
            token = api_token

        self.connection = Connection(host, token, session=session)

        # Ping platform to get username and version matching api_token
        try:
            ping_response = self.connection.get("/api/home/ping").json()
        except Exception as e:  # pragma: no cover
            raise PicselliaError(
                "Cannot connect to the platform. Please check api_token, organization and host given.\n"
                f"Error is : {e}"
            )

        sdk_version = picsellia.__version__
        platform_version = ping_response["sdk_version"]
        if self.is_sdk_outdated(sdk_version, platform_version):  # pragma: no cover
            logger.warning(
                f"\033[93mYou are using an outdated version of the picsellia package ({sdk_version})\033[0m"
            )
            logger.warning(
                f"\033[93mPlease consider upgrading to {platform_version} with pip install picsellia --upgrade\033[0m"
            )

        if organization_id is not None:
            if isinstance(organization_id, str):
                organization_id = UUID(organization_id)
            self._id = organization_id
            self.sync()
        elif organization_name is not None:
            r = self.connection.get(
                path="/api/organizations/find", params={"name": organization_name}
            ).json()
            self._id = r["id"]
            self.sync()
        elif (
            "default_organization" in ping_response
            and ping_response["default_organization"]
        ):
            self._id = ping_response["default_organization"]
            self.sync()
        else:
            raise PicselliaError(
                "You cannot create a Client with no organization selected when you don't own any organization."
            )

        if self._id == ping_response["default_organization"]:
            message = "your"
        else:  # pragma: no cover
            message = self.name + "'s"

        username = ping_response["username"]
        logger.info(f"Hi {Colors.BLUE}{username}{Colors.ENDC}, welcome back. 🥑")
        logger.info(f"Workspace: {Colors.YELLOW}{message}{Colors.ENDC} organization.")

    def __str__(self) -> str:
        return f"Client initialized for organization `{self.name}`"

    def __enter__(self):
        self.connection = self.connection.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.__exit__(exc_type, exc_val, exc_tb)

    @property
    def id(self) -> UUID:
        """Organization UUID connected with this (Client)"""
        return self._id

    @property
    def name(self) -> str:
        """Organization name connected with this (Client)"""
        return self._name

    @property
    @deprecated(
        deprecated_in="6.29.0",
        details="You should use self.connection instead of this one",
    )
    def connexion(self) -> Connection:
        """deprecated"""
        return self.connection

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/organization/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> OrganizationSchema:
        schema = OrganizationSchema(**data)
        self._name = schema.name
        if schema.default_connector_id is not None:
            self.connection.connector_id = schema.default_connector_id
            self.connection.organization_id = schema.id
        return schema

    @classmethod
    def is_sdk_outdated(cls, sdk: str, platform: str):
        try:
            sdk_version = semantic_version.Version(sdk)
            platform_version = semantic_version.Version(platform)
        except ValueError:
            return False

        return sdk_version < platform_version

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
            print(foo_dataset.get_resource_url_on_platform())
            >>> "https://app.picsellia.com/organization/62cffb84-b92c-450c-bc37-8c4dd4d0f590"
            ```

        Returns:
            Url on Platform for this resource
        """

        return f"{self.connection.host}/organization/{self.id}"

    @exception_handler
    @beartype
    def list_users(self, username: str | None = None) -> list[User]:
        """Retrieve all users of this organization
        Returns:
            a list of (User)
        """
        params = {}
        if username:
            params["username"] = username
        r = self.connection.get(
            f"/api/access/organization/{self.id}/users", params=params
        ).json()
        return [User(self.connection, item) for item in r["users"]]

    @exception_handler
    @beartype
    def get_datalake(
        self, id: str | UUID | None = None, name: str | None = None
    ) -> Datalake:
        """Retrieve a datalake of your organization.
        By default, is nothing is given, this will return your default datalake.

        Examples:
            ```python
            datalake = client.get_datalake()
            datalake = client.get_datalake(name="default")
            datalake = client.get_datalake(id="0188e773-db65-7546-8e3e-b38fe5bed6d2")
            ```

        Arguments:
            id (str or UUID, optional): id of the datalake to retrieve. Defaults to None.
            name (str, optional): name of the datalake to retrieve. Defaults to None.

        Returns:
            The (Datalake) of the client that you are using
        """
        params = {}
        if id:
            params["id"] = UUID(id) if isinstance(id, str) else id
        elif name:
            params["name"] = name

        r = self.connection.get(
            f"/api/organization/{self.id}/datalake", params=params
        ).json()

        return Datalake(self.connection, self.id, r)

    @exception_handler
    @beartype
    def list_datalakes(self) -> list[Datalake]:
        """Retrieve all datalakes linked to this organization

        Examples:
            ```python
            datalakes = client.list_datalakes()
            ```

        Returns:
            List of (Datalake) of the client that you are using
        """
        # Retrieve default datalake
        r = self.connection.get(f"/api/organization/{self.id}/datalakes").json()
        return [Datalake(self.connection, self.id, item) for item in r["items"]]

    @exception_handler
    @beartype
    def create_dataset(
        self,
        name: str,
        description: str = "",
        private: bool = None,
    ) -> Dataset:
        """Create a (Dataset) in this organization.

        This method allows user to create a dataset into the organization currently connected.
        A dataset can then be versioned into (DatasetVersion).
        User can specify name of the dataset, a description and if the dataset is private or not.

        Examples:
            Create a dataset named datatest with data from datalake and version it
            ```python
            foo_dataset = client.create_dataset('foo_dataset')
            foo_dataset_version_1 = foo_dataset.create_version('first')
            some_data = client.get_datalake().list_data(limit=10)
            foo_dataset_version_1.add_data(some_data)
            ```

        Arguments:
            name (str): Name of the dataset. It must be unique in the organization.
            description (str, optional): A description of the dataset. Defaults to ''.
            private (bool, optional): Specify if the dataset is private. Defaults to True.

        Returns:
            A (Dataset) that you can manipulate, connected to Picsellia
        """
        assert name != "", "Dataset name can't be empty"

        if private is not None:
            logging.warning(
                "'private' parameter is deprecated and will be removed in future versions. "
                "You cannot create a public dataset from the SDK anymore."
            )

        payload = {"name": name, "description": description}
        r = self.connection.post(
            f"/api/organization/{self.id}/datasets",
            data=orjson.dumps(payload),
        ).json()
        return Dataset(self.connection, r)

    @exception_handler
    @beartype
    def get_dataset(self, name: str) -> Dataset:
        """Retrieve a dataset by its name

        Examples:
            ```python
            foo_dataset = client.get_dataset('datatest')
            foo_dataset_version = foo_dataset.get_version('first')
            ```

        Arguments:
            name (str): Name of the dataset

        Returns:
            A (Dataset) that you can use and manipulate
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/organization/{self.id}/datasets/find",
            params=params,
        ).json()
        return Dataset(self.connection, r)

    @exception_handler
    @beartype
    def get_dataset_by_id(self, id: UUID | str) -> Dataset:
        """Get a dataset by its id

        Examples:
            ```python
            dataset = client.get_dataset_by_id('918351d2-3e96-4970-bb3b-420f33ded895')
            ```

        Arguments:
            id (str): id of the dataset to retrieve

        Returns:
            A (Dataset) that you can use and manipulate
        """
        if isinstance(id, str):
            id = UUID(id)
        params = {"id": id}
        r = self.connection.get(
            f"/api/organization/{self.id}/datasets/find", params=params
        ).json()
        return Dataset(self.connection, r)

    @exception_handler
    @beartype
    def list_datasets(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Dataset]:
        """Retrieve all dataset of current organization

        Examples:
            ```python
            datasets = client.list_datasets()
            ```

        Arguments:
            limit (int, optional): Limit number of datasets to retrieve. Defaults to None, all datasets will be retrieved.
            offset (int, optional): Offset to begin with when listing datasets. Defaults to None, starting at 0.
            order_by (list[str], optional): Some fields to order datasets against. Defaults to None, datasets will not be sorted

        Returns:
            A list of (Dataset) object that belongs to your organization
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = filter_payload(params)
        r = self.connection.get(
            f"/api/organization/{self.id}/datasets", params=params
        ).json()
        return [Dataset(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def get_dataset_version_by_id(self, id: UUID | str) -> DatasetVersion:
        """Get a dataset version by its id

        Examples:
            ```python
            dataset_version = client.get_dataset_version_by_id('918351d2-3e96-4970-bb3b-420f33ded895')
            ```

        Arguments:
            id (str or UUID): id of the dataset version to retrieve

        Returns:
            A (DatasetVersion)
        """
        if isinstance(id, str):
            id = UUID(id)
        params = {"id": id}
        r = self.connection.get(
            f"/api/organization/{self.id}/datasetversions/find", params=params
        ).json()
        return DatasetVersion(self.connection, r)

    @exception_handler
    @beartype
    def create_model(self, name: str, description: str = None) -> Model:
        """Create a new model.

        Examples:
            ```python
            model = client.create_model(name="foo_model", description="A brand new model!")
            ```

        Arguments:
            name (str): Model name to create.
            description (str, optional): Description of this model. Defaults to None

        Returns:
            A (Model) object that you can manipulate
        """
        if description is None:
            description = "A brand new model!"

        payload = {
            "name": name,
            "description": description,
        }
        r = self.connection.post(
            f"/api/organization/{self.id}/models",
            data=orjson.dumps(payload),
        ).json()
        created_model = Model(self.connection, r)
        logger.info(
            f"📚 Model {created_model.name} created\n📊 🌐 Platform url: {created_model.get_resource_url_on_platform()}"
        )
        return created_model

    @exception_handler
    @beartype
    def get_model_by_id(self, id: UUID | str) -> Model:
        """Retrieve a model by its id

        Examples:
            ```python
            model = client.get_model_by_id(UUID("d8fae655-5c34-4a0a-a59a-e49c89f20998"))
            ```
        Arguments:
            id (str): id of the model that you are looking for

        Returns:
            A (Model) object that you can manipulate
        """
        if isinstance(id, str):
            id = UUID(id)
        params = {"id": id}
        r = self.connection.get(
            f"/api/organization/{self.id}/models/find", params=params
        ).json()
        return Model(self.connection, r)

    def _do_get_model_by_name(self, url: str, name: str):
        params = {"name": name}
        r = self.connection.get(url, params=params).json()
        return Model(self.connection, r)

    @exception_handler
    @beartype
    def get_model(self, name: str) -> Model:
        """Retrieve a model by its name.

        Examples:
            ```python
            model = client.get_model("foo_model")
            ```
        Arguments:
            name (str): name of the model you are looking for

        Returns:
            A (Model) object that you can manipulate
        """
        return self._do_get_model_by_name(
            f"/api/organization/{self.id}/models/find", name
        )

    @exception_handler
    @beartype
    def get_public_model(self, name: str) -> Model:
        """Retrieve a public model by its name.
           It can only retrieve *public* model.

        Examples:
            ```python
            model = client.get_public_model("foo_public_model")
            ```
        Arguments:
            name (str): name of the public model you are looking for

        Returns:
            A (Model) object that you can manipulate
        """
        return self._do_get_model_by_name("/api/models/find", name)

    def _do_list_models(self, url: str, params: dict):
        params = filter_payload(params)
        r = self.connection.get(url, params=params).json()
        return [Model(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def list_models(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Model]:
        """List all models stored in this organization

        This will return all the models stored
        If no project is found, will throw a ResourceNotFoundError

        Examples:
            ```python
            models = client.list_models()
            ```

        Arguments:
            limit (int, optional): Limit number of models to retrieve. Defaults to None, all models will be retrieved.
            offset (int, optional): Offset to begin with when listing models. Defaults to None, starting at 0.
            order_by (list[str], optional): Some fields to order models against. Defaults to None, models will not be sorted

        Returns:
            A list of all (Model) that belong to this organization
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        return self._do_list_models(
            f"/api/organization/{self.id}/models", params=params
        )

    @exception_handler
    @beartype
    def list_public_models(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
        name: str | None = None,
        type: str | InferenceType | None = None,
    ) -> list[Model]:
        """List all public models of Picsellia Hub
        This will return all public models of the hub

        Arguments:
            limit (int, optional): Limit number of public models to retrieve.
                Defaults to None, all public models will be retrieved.
            offset (int, optional): Offset to begin with when listing public models.
                Defaults to None, starting at 0.
            order_by (list[str], optional): Some fields to order models against.
                Defaults to None, models will not be sorted
            name (str, optional): A name to filter public models. It will return models with name *containing*
                this parameter. Defaults to None, models will not be filtered
            type (str or InferenceType, optional): A type to filter public models on.

        Examples:
            ```python
            public_detection_models = client.list_public_models(name="yolo")
            ```

        Returns:
            A list of all public (Model) objects
        """
        if type:
            logging.warning(
                "'type' parameter is deprecated and will be removed in future versions."
            )

        params = {
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "name": name,
        }
        return self._do_list_models("/api/models", params=params)

    @exception_handler
    @beartype
    def get_model_version_by_id(self, id: UUID | str) -> ModelVersion:
        """Get a model version by its id

        Examples:
            ```python
            model_version = client.get_model_version_by_id('918351d2-3e96-4970-bb3b-420f33ded895')
            ```

        Arguments:
            id (str or UUID): id of the model version to retrieve

        Returns:
            A (ModelVersion)
        """
        if isinstance(id, str):
            id = UUID(id)
        params = {"id": id}
        r = self.connection.get(
            f"/api/organization/{self.id}/modelversions/find", params=params
        ).json()
        return ModelVersion(self.connection, r)

    @exception_handler
    @beartype
    def create_project(
        self,
        name: str,
        description: str | None = None,
        private: bool | None = True,
    ) -> Project:
        """Create a project with given name and parameters

        This project will be registered into used organization.

        Examples:
            ```python
            my_project = client.create_project("my_project", description="My first project!")
            ```
        Arguments:
            name (str): name of the project
            description (str): description of the project
            private (bool, deprecated): This parameter is deprecated

        Returns:
            A (Project) that you can manipulate to run experiments, or attach dataset
        """
        payload = {"name": name}

        if private is False:
            logger.warning(
                "You cannot create a public project anymore. This parameter will not be used"
            )

        if description is not None:
            payload["description"] = description

        r = self.connection.post(
            f"/api/organization/{self.id}/projects",
            data=orjson.dumps(payload),
        ).json()
        created_project = Project(self.connection, r)
        logger.info(
            f"📚 Project {name} created\n📊 Description: {description if description is not None else ''}\n🌐 Platform url: {created_project.get_resource_url_on_platform()}"
        )
        return created_project

    @exception_handler
    @beartype
    def get_project(self, project_name: str) -> Project:
        """Get a project from its name

        Retrieve a project from its name.
        Project must belong to used organization.

        Examples:
            ```python
            my_project = client.get_project("my_project")
            ```
        Arguments:
            project_name (str): name of the project to retrieve

        Returns:
            A (Project) of your organization, you can manipulate to run experiments, or attach dataset
        """
        r = self.connection.get(
            f"/api/organization/{self.id}/projects/find",
            params={"name": project_name},
        ).json()
        return Project(self.connection, r)

    @exception_handler
    @beartype
    def get_project_by_id(self, id: UUID | str) -> Project:
        """Get a project from its id

        Retrieve a project from its id.
        Project must belong to used organization.
        If no project is found, will throw a ResourceNotFoundError

        Examples:
            ```python
            my_project = client.get_project_by_id("2214aacc-b884-41e1-b70f-420c0cd7eefb")
            ```
        Arguments:
            id (str): id of the project to retrieve

        Returns:
            A (Project) of your organization, you can manipulate to run experiments, or attach dataset
        """
        if isinstance(id, str):
            id = UUID(id)
        r = self.connection.get(
            f"/api/organization/{self.id}/projects/find?id={id}"
        ).json()
        return Project(self.connection, r)

    @exception_handler
    @beartype
    def list_projects(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Project]:
        """List all projects of your organization.

        Retrieve all projects of your organization

        Examples:
            ```python
            projects = client.list_projects()
            ```

        Arguments:
            limit (int, optional): Limit number of projects to retrieve. Defaults to None, all projects will be retrieved.
            offset (int, optional): Offset to begin with when listing projects. Defaults to None, starting at 0.
            order_by (list[str], optional): Some fields to order projects against. Defaults to None, projects will not be sorted

        Returns:
            A list of Project of your organization
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = filter_payload(params)
        r = self.connection.get(
            f"/api/organization/{self.id}/projects", params=params
        ).json()
        return [Project(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def get_experiment_by_id(self, id: UUID | str) -> Experiment:
        """Get an experiment by its id

        Examples:
            ```python
            experiment = client.get_experiment_by_id('918351d2-3e96-4970-bb3b-420f33ded895')
            ```

        Arguments:
            id (str or UUID): id of the experiment to retrieve

        Returns:
            A (Experiment)
        """
        if isinstance(id, str):
            id = UUID(id)

        params = {"id": id}
        r = self.connection.get(
            f"/api/organization/{self.id}/experiments/find", params=params
        ).json()
        return Experiment(self.connection, r)

    @exception_handler
    @beartype
    def get_deployment(self, name: str) -> Deployment:
        """Get a (Deployment) from its name.

        Examples:
            ```python
            deployment = client.get_deployment(
                name="awesome-deploy"
            )
            ```
        Arguments:
            name (str): auto-generated name of your deployment.

        Returns:
            A (Deployment) object connected and authenticated to all the services.
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/organization/{self.id}/deployments/find", params=params
        ).json()
        return Deployment(self.connection, r)

    @exception_handler
    @beartype
    def get_deployment_by_id(self, id: UUID | str) -> Deployment:
        """Get a (Deployment) from its name.

        Examples:
            ```python
            deployment = client.get_deployment_by_id(
                id="YOUR DEPLOYMENT ID"
            )
            ```
        Arguments:
            id (str): deployment id displayed in your deployment settings.

        Returns:
            A (Deployment) object connected and authenticated to all the services.
        """
        if isinstance(id, str):
            id = UUID(id)
        params = {"id": id}
        r = self.connection.get(
            f"/api/organization/{self.id}/deployments/find", params=params
        ).json()
        return Deployment(self.connection, r)

    @exception_handler
    @beartype
    def list_deployments(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Deployment]:
        """List all (Deployment) of your organization

        Examples:
            ```python
            our_deployments = client.list_deployments()
            ```
        Arguments:
            limit (int, optional): number max of results to return
            offset (int, optional): offset of page for pagination
            order_by (list[str], optional): keys on which deployments shall be sorted

        Returns:
            List of (Deployment): all deployments object connected and authenticated to all the services.
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = filter_payload(params)
        r = self.connection.get(
            f"/api/organization/{self.id}/deployments", params=params
        ).json()
        return [Deployment(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def create_deployment(
        self,
        model_version: ModelVersion,
        shadow_model_version: ModelVersion | None = None,
        name: str | None = None,
        min_threshold: float | None = None,
        target_datalake: Datalake | None = None,
        disable_serving: bool | None = False,
    ):
        """Create a (Deployment) from a model.

        This method allows you to create a (Deployment) on Picsellia. You will then have
        access to the monitoring dashboard and eventually a hosted endpoint.

        Examples:
            Create a serverless deployment
            ```python
            model_version = client.get_model_version_by_id('918351d2-3e96-4970-bb3b-420f33ded895')
            deployment = client.create_deployment(model_version=model_version)
            ```

        Arguments:
            model_version (ModelVersion): ModelVersion to deploy.
            shadow_model_version (ModelVersion, optional): ModelVersion to perform shadow predictions.
            name (str, optional): Name of your deployment. Defaults to a random name.
            min_threshold (float, optional): Threshold of detection scores used by models when predicting. Defaults to 0.
            target_datalake (Datalake, optional): Datalake to use when data are pushed into Picsellia.
                Defaults to organization default Datalake.
            disable_serving (bool, optional): Whether to not use Picsellia Serving. Defaults to False.


        Returns:
            A (Deployment)
        """
        from picsellia.sdk.deployment import Deployment

        payload = {
            "model_version_id": model_version.id,
            "name": name,
            "min_threshold": min_threshold,
        }
        if target_datalake is not None:
            payload["target_datalake_id"] = target_datalake.id
        if shadow_model_version:
            payload["shadow_model_version_id"] = shadow_model_version.id
        if disable_serving:
            payload["disable_serving"] = disable_serving

        filtered_payload = utils.filter_payload(payload)
        r = self.connection.post(
            f"/api/organization/{self.id}/deployments",
            data=orjson.dumps(filtered_payload),
        ).json()
        deployment = Deployment(self.connection, r)
        logger.info(f"{model_version} is deployed on {deployment}")
        return deployment

    @exception_handler
    @beartype
    def create_datasource(self, name: str) -> DataSource:
        """Create a data source into this organization

        Examples:
            ```python
            data_source = client.create_datasource()
            ```

        Arguments:
            name (str): Name of the datasource to create

        Returns:
            A  (DataSource) object that belongs to your organization
        """
        return DataSourceService.create_datasource(self.connection, self._id, name)

    @exception_handler
    @beartype
    def get_datasource(self, name: str) -> DataSource:
        """Retrieve a datasource by its name

        Examples:
            ```python
            data_sources = client.get_datasource("datasource_1")
            ```

        Arguments:
            name (str): Name of the datasource to retrieve

        Returns:
            A (DataSource) object that belongs to your organization
        """
        return DataSourceService.get_datasource(self.connection, self._id, name)

    @exception_handler
    @beartype
    def get_or_create_datasource(self, name: str) -> DataSource:
        """Retrieve a datasource by its name or create it if it does not exist.

        Examples:
            ```python
            datasource = client.get_or_create_datasource("new_source")
            ```

        Arguments:
            name (str): Datasource name to retrieve or create

        Returns:
            A (DataSource) object
        """
        return DataSourceService.get_or_create_datasource(
            self.connection, self._id, name
        )

    @exception_handler
    @beartype
    def list_datasources(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[DataSource]:
        """Retrieve all data source of current organization

        Examples:
            ```python
            data_sources = client.list_datasources()
            ```

        Arguments:
            limit (int, optional): Limit number of data sources to retrieve. Defaults to None, all data sources will be retrieved.
            offset (int, optional): Offset to begin with when listing data sources. Defaults to None, starting at 0.
            order_by (list[str], optional): Some fields to order data sources against. Defaults to None, data sources will not be sorted

        Returns:
            A list of (DataSource) object that belongs to your organization
        """
        return DataSourceService.list_datasources(
            self.connection, self._id, limit, offset, order_by
        )

    @exception_handler
    @beartype
    def _create_tag_organization_scoped(self, name: str, target: TagTarget) -> Tag:
        payload = {"name": name, "target_type": target}
        r = self.connection.post(
            f"/api/organization/{self.id}/tags",
            data=orjson.dumps(payload),
        ).json()
        return Tag(self.connection, r)

    @exception_handler
    @beartype
    def create_dataset_tag(self, name: str) -> Tag:
        """Create a Dataset Tag, usable only on Dataset objects

        Examples:
            ```python
            tag = client.create_dataset_tag("global")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._create_tag_organization_scoped(name, TagTarget.DATASET)

    @exception_handler
    @beartype
    def create_dataset_version_tag(self, name: str) -> Tag:
        """Create a Dataset Version Tag, usable only on Dataset Version objects

        Examples:
            ```python
            tag = client.create_dataset_version_tag("train")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._create_tag_organization_scoped(name, TagTarget.DATASET_VERSION)

    @exception_handler
    @beartype
    def create_model_tag(self, name: str) -> Tag:
        """Create a Model Tag, usable only on Model objects

        Examples:
            ```python
            tag = client.create_model_tag("model")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._create_tag_organization_scoped(name, TagTarget.MODEL)

    @exception_handler
    @beartype
    def create_model_version_tag(self, name: str) -> Tag:
        """Create a Model Version Tag, usable only on Model Version objects

        Examples:
            ```python
            tag = client.create_model_version_tag("initial")
            ```
        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._create_tag_organization_scoped(name, TagTarget.MODEL_VERSION)

    @exception_handler
    @beartype
    def create_deployment_tag(self, name: str) -> Tag:
        """Create a Deployment Tag, usable only on Deployment objects

        Examples:
            ```python
            tag = client.create_deployment_tag("operation")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._create_tag_organization_scoped(name, TagTarget.DEPLOYMENT)

    @exception_handler
    @beartype
    def _list_tags_organization_scoped(self, target: TagTarget) -> list[Tag]:
        params = {"target_type": target.value}
        r = self.connection.get(
            f"/api/organization/{self.id}/tags", params=params
        ).json()
        return [Tag(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def list_dataset_tags(self) -> list[Tag]:
        """List all Dataset tags, usable only on Dataset objects

        Examples:
            ```python
            tags = client.list_dataset_tags()
            ```

        Returns:
            A list of (Tag) objects
        """
        return self._list_tags_organization_scoped(TagTarget.DATASET)

    @exception_handler
    @beartype
    def list_dataset_version_tags(self) -> list[Tag]:
        """List all Dataset Version tags, usable only on Dataset Version objects

        Examples:
            ```python
            tags = client.list_dataset_version_tags()
            ```

        Returns:
            A list of (Tag) objects
        """
        return self._list_tags_organization_scoped(TagTarget.DATASET_VERSION)

    @exception_handler
    @beartype
    def list_model_tags(self) -> list[Tag]:
        """List all Model tags, usable only on Model objects

        Examples:
            ```python
            tags = client.list_model_tags()
            ```

        Returns:
            A list of (Tag) objects
        """
        return self._list_tags_organization_scoped(TagTarget.MODEL)

    @exception_handler
    @beartype
    def list_model_version_tags(self) -> list[Tag]:
        """List all Model Version tags, usable only on Model Version objects

        Examples:
            ```python
            tags = client.list_model_version_tags()
            ```

        Returns:
            A list of (Tag) objects
        """
        return self._list_tags_organization_scoped(TagTarget.MODEL_VERSION)

    @exception_handler
    @beartype
    def list_deployment_tags(self) -> list[Tag]:
        """List all Deployment tags, usable only on Deployment Version objects

        Examples:
            ```python
            tags = client.list_deployment_tags()
            ```

        Returns:
            A list of (Tag) objects
        """
        return self._list_tags_organization_scoped(TagTarget.DEPLOYMENT)

    @exception_handler
    @beartype
    def _find_tag_organization_scoped(self, target: TagTarget, name: str) -> Tag:
        params = {"name": name, "target_type": target.value}
        r = self.connection.get(
            f"/api/organization/{self.id}/tags/find",
            params=params,
        ).json()
        return Tag(self.connection, r)

    @exception_handler
    @beartype
    def find_dataset_tag(self, name: str) -> Tag:
        """Find a Dataset tag, usable only on Dataset objects, from its name

        Examples:
            ```python
            tag = client.find_dataset_tag("global")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._find_tag_organization_scoped(TagTarget.DATASET, name)

    @exception_handler
    @beartype
    def find_dataset_version_tag(self, name: str) -> Tag:
        """Find a Dataset Version tag, usable only on Dataset Version objects, from its name

        Examples:
            ```python
            tag = client.find_dataset_version_tag("train")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._find_tag_organization_scoped(TagTarget.DATASET_VERSION, name)

    @exception_handler
    @beartype
    def find_model_tag(self, name: str) -> Tag:
        """Find a Model tag, usable only on Model objects, from its name

        Examples:
            ```python
            tag = client.find_model_tag("model")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._find_tag_organization_scoped(TagTarget.MODEL, name)

    @exception_handler
    @beartype
    def find_model_version_tag(self, name: str) -> Tag:
        """Find a Model Version tag, usable only on Model version objects, from its name

        Examples:
            ```python
            tag = client.find_model_version_tag("initial")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._find_tag_organization_scoped(TagTarget.MODEL_VERSION, name)

    @exception_handler
    @beartype
    def find_deployment_tag(self, name: str) -> Tag:
        """Find a Deployment tag, usable only on Deployment objects, from its name

        Examples:
            ```python
            tag = client.find_deployment_tag("operation")
            ```

        Arguments:
            name (str): Name of the tag

        Returns:
            A (Tag) object
        """
        return self._find_tag_organization_scoped(TagTarget.DEPLOYMENT, name)

    @exception_handler
    @beartype
    def get_job_by_id(self, id: UUID | str) -> Job:
        """Get a (Job) from its id.

        Examples:
            ```python
            job = client.get_job_by_id(
                id="YOUR JOB ID"
            )
            ```

        Arguments:
            id (str): job id displayed in your job page.

        Returns:
            A (Job) object
        """
        if isinstance(id, str):
            id = UUID(id)
        params = {"id": id}
        r = self.connection.get(
            f"/api/organization/{self.id}/jobv2s/find", params=params
        ).json()
        return Job(self.connection, r, version=2)

    @exception_handler
    @beartype
    def create_processing(
        self,
        name: str,
        type: str | ProcessingType,
        default_cpu: int,
        default_gpu: int,
        default_parameters: dict,
        docker_image: str,
        docker_tag: str,
        docker_flags: list[str] | None = None,
        description: str | None = None,
    ) -> Processing:
        """Create a (Processing) in this organization.

        Examples:
            Create a dataset named datatest with data from datalake and version it
            ```python
            foo_dataset = client.create_processing(
                name="processing-1",
                type="AUTO_TAGGING",
                default_cpu=4,
                default_gpu=0,
                default_parameters={"gamma": 1.2},
                docker_image="training-tf2",
                docker_tag="latest",
                description="A processing to auto-tag images",
            )
            ```

        Arguments:
            name (str): Name of the processing.
            type (str or ProcessingType): Type of the processing.
            default_cpu (int): Default cpu used by this processing.
            default_gpu (int): Default gpu used by this processing.
            default_parameters (dict): Default parameters used by this processing.
            docker_image (str): Docker image of the processing.
            docker_tag (str): Docker tag of the processing.
            docker_flags (list[str], optional): Docker flags of the processing.
            description (str, optional): Description of the processing. Default to None.

        Returns:
            A (Processing)
        """
        type_ = ProcessingType.validate(type)
        payload = {
            "name": name,
            "description": description,
            "type": type_,
            "default_cpu": default_cpu,
            "default_gpu": default_gpu,
            "default_parameters": default_parameters,
            "docker_image": docker_image,
            "docker_tag": docker_tag,
            "docker_flags": docker_flags,
        }
        r = self.connection.post(
            f"/api/organization/{self.id}/processings", data=orjson.dumps(payload)
        ).json()
        return Processing(self.connection, r)

    @exception_handler
    @beartype
    def list_processings(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[Processing]:
        """List all processings stored in this organization

        Examples:
            ```python
            processings = client.list_processings()
            ```

        Arguments:
            limit (int, optional): Limit number of processings to retrieve. Defaults to None, all models will be retrieved.
            offset (int, optional): Offset to begin with when listing processings. Defaults to None, starting at 0.
            order_by (list[str], optional): Some fields to order processings against. Defaults to None, processings will not be sorted

        Returns:
            A list of all (Processing) that belong to this organization
        """
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = filter_payload(params)
        r = self.connection.get(
            f"/api/organization/{self.id}/processings", params=params
        ).json()
        return [Processing(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def get_processing(self, name: str) -> Processing:
        """Find a processing in this organization

        Examples:
            ```python
            processing = client.get_processing(name="auto-tagging-dataset")
            ```

        Arguments:
            name (str): Name of the processing you are looking for

        Returns:
            A (Processing) that belong to this organization
        """
        params = {"name": name}
        r = self.connection.get(
            f"/api/organization/{self.id}/processings/find", params=params
        ).json()
        return Processing(self.connection, r)

    @exception_handler
    @beartype
    def list_annotation_campaigns(
        self, is_closed: bool | None = None
    ) -> list[AnnotationCampaign]:
        """List annotation campaigns of this organization, created on dataset versions.

        Examples:
            ```python
            campaigns = client.list_annotation_campaigns()
            ```
        Returns:
            A list of (AnnotationCampaign) of this organization
        """
        params = {}
        if is_closed is not None:
            params["is_closed"] = is_closed

        r = self.connection.get(
            f"/api/organization/{self.id}/annotationcampaigns", params=params
        ).json()
        return [AnnotationCampaign(self.connection, item) for item in r["items"]]

    @exception_handler
    @beartype
    def list_review_campaigns(
        self, is_closed: bool | None = None
    ) -> list[ReviewCampaign]:
        """List review campaigns of this organization, created on deployments.

        Examples:
            ```python
            campaigns = client.list_review_campaigns()
            ```
        Returns:
            A list of (ReviewCampaign) of this organization
        """
        params = {}
        if is_closed is not None:
            params["is_closed"] = is_closed

        r = self.connection.get(
            f"/api/organization/{self.id}/reviewcampaigns", params=params
        ).json()
        return [ReviewCampaign(self.connection, item) for item in r["items"]]
