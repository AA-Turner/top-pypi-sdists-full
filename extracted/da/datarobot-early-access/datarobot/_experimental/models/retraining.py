#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot._compat import String
from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate

use_case_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String,
    }
).ignore_extra("*")


class RetrainingUseCase(APIObject):
    """
    Retraining use case.

    Attributes
    ----------
    id : str
        The ID of the use case.
    name : str
        The name of the use case.
    """

    _converter = use_case_trafaret

    def __init__(
        self,
        id: str,
        name: str,
    ):
        self.id = id
        self.name = name


class RetrainingPolicy(APIObject):
    """Retraining Policy.

    Attributes
    ----------
    policy_id : str
        ID of the retraining policy
    name : str
        Name of the retraining policy
    description : str
        Description of the retraining policy
    use_case : Optional[dict]
        Use case the retraining policy is associated with
    """

    _path = "deployments/{}/retrainingPolicies/"

    _converter = t.Dict(
        {
            t.Key("deployment_id"): String(),
            t.Key("id"): String(),
            t.Key("name"): String(),
            t.Key("description", optional=True): String(allow_blank=True),
            t.Key("use_case", optional=True): use_case_trafaret,
        }
    ).allow_extra("*")

    def __init__(
        self,
        deployment_id: str,
        id: str,
        name: str,
        description: Optional[str] = None,
        use_case: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.deployment_id = deployment_id
        self.id = id
        self.name = name
        self.description = description
        self.use_case = RetrainingUseCase.from_server_data(use_case) if use_case else None

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.id or self.name)

    @classmethod
    def list(cls, deployment_id: str) -> List[RetrainingPolicy]:
        """Lists all retraining policies associated with a deployment

        Parameters
        ----------
        deployment_id : str
            Id of the deployment

        Returns
        -------
        policies : list
            List of retraining policies associated with a deployment

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            from datarobot._experimental.models.retraining import RetrainingPolicy
            deployment = Deployment.get(deployment_id='620ed0e37b6ce03244f19631')
            RetrainingPolicy.list(deployment.id)
            >>> [RetrainingPolicy('620ed248bb0a1f5889eb6aa7'), RetrainingPolicy('624f68be8828ed81bf487d8d')]
        """

        path = cls._path.format(deployment_id)
        data = unpaginate(path, None, cls._client)

        # TODO: Move RetrainingPolicy to the datarobot package, refactor it to be
        # a sub-entity of Deployment, and eliminate deployment_id injections (MMM-18508)
        return [cls.from_server_data({**item, "deployment_id": deployment_id}) for item in data]

    @classmethod
    def get(cls, deployment_id: str, retraining_policy_id: str) -> RetrainingPolicy:
        """Retrieves a retraining policy associated with a deployment

        Parameters
        ----------
        deployment_id : str
            Id of the deployment
        retraining_policy_id : str
            Id of the policy

        Returns
        -------
        retraining_policy : Retraining Policy
            Retraining policy

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.retraining import RetrainingPolicy
            policy = RetrainingPolicy.get(
                deployment_id='620ed0e37b6ce03244f19631',
                retraining_policy_id='624f68be8828ed81bf487d8d'
            )
            policy.id
            >>>'624f68be8828ed81bf487d8d'
            policy.name
            >>>'PolicyA'
        """

        path = "{}{}/".format(cls._path.format(deployment_id), retraining_policy_id)

        data = cls._client.get(path).json()
        data["deployment_id"] = deployment_id

        return cls.from_server_data(data)

    @classmethod
    def create(
        cls,
        deployment_id: str,
        name: str,
        description: Optional[str] = None,
        use_case_id: Optional[str] = None,
    ) -> RetrainingPolicy:
        """Create a retraining policy associated with a deployment

        Parameters
        ----------
        deployment_id : str
            The ID of the deployment.
        name : str
            The retraining policy name.
        description : str
            The retraining policy description.
        use_case_id : Optional[str]
            The ID of the Use Case that the retraining policy is associated with.

        Returns
        -------
        retraining_policy : Retraining Policy
            Retraining policy

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.retraining import RetrainingPolicy
            policy = RetrainingPolicy.create(
                deployment_id='620ed0e37b6ce03244f19631',
                name='Retraining Policy A',
                use_case_id='678114c41e9114cabca27044',
            )
            policy.id
            >>>'624f68be8828ed81bf487d8d'

        """

        path = cls._path.format(deployment_id)
        payload = {
            "name": name,
            "use_case_id": use_case_id,
            "description": description,
        }

        data = cls._client.post(path, payload).json()
        data["deployment_id"] = deployment_id

        return cls.from_server_data(data)

    @classmethod
    def delete(cls, deployment_id: str, retraining_policy_id: str) -> None:
        """Deletes a retraining policy associated with a deployment

        Parameters
        ----------
        deployment_id : str
            Id of the deployment
        retraining_policy_id : str
            Id of the policy

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.retraining import RetrainingPolicy
            RetrainingPolicy.delete(
                deployment_id='620ed0e37b6ce03244f19631',
                retraining_policy_id='624f68be8828ed81bf487d8d'
            )
        """

        path = "{}{}/".format(cls._path.format(deployment_id), retraining_policy_id)
        cls._client.delete(path)

    def update_use_case(self, use_case_id: str | None) -> RetrainingPolicy:
        """Update the use case associated with this retraining policy

        Parameters
        ----------
        use_case_id : str
            Id of the use case the retraining policy is associated with

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.retraining import RetrainingPolicy
            policy = RetrainingPolicy.get(
                deployment_id='620ed0e37b6ce03244f19631',
                retraining_policy_id='624f68be8828ed81bf487d8d'
            )
            updated = RetrainingPolicy.update_use_case(use_case_id='620ed0e37b6ce03244f19633')
            updated.use_case.id
            >>>'620ed0e37b6ce03244f19633'
        """

        path = "{}{}".format(self._path.format(self.deployment_id), self.id)
        payload = {"use_case_id": use_case_id}

        data = self._client.patch(path, payload).json()
        data["deployment_id"] = self.deployment_id

        return self.from_server_data(data)


class RetrainingPolicyRun(APIObject):
    """Retraining policy run.

    Attributes
    ----------
    policy_run_id : str
        ID of the retraining policy run
    status : str
        Status of the retraining policy run
    challenger_id : str
        ID of the challenger model retrieved after running the policy
    error_message: str
        The error message if an error occurs during the policy run
    model_package_id: str
        ID of the model package (version) retrieved after the policy is run
    project_id: str
        ID of the project the deployment is associated with
    start_time: datetime.datetime
        Timestamp of when the policy run starts
    finish_time: datetime.datetime
        Timestamp of when the policy run finishes
    """

    _path = "deployments/{}/retrainingPolicies/{}/runs/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("status"): String(),
            t.Key("start_time"): t.Or(String(), t.Null),
            t.Key("finish_time"): t.Or(String(), t.Null),
            t.Key("challenger_id", optional=True): t.Or(String(), t.Null),
            t.Key("error_message", optional=True): t.Or(String(), t.Null),
            t.Key("model_package_id", optional=True): t.Or(String(), t.Null),
            t.Key("project_id", optional=True): t.Or(String(), t.Null),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        status: str,
        start_time: str,
        finish_time: str,
        challenger_id: Optional[str] = None,
        error_message: Optional[str] = None,
        model_package_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> None:
        self.id = id
        self.status = status
        self.start_time = start_time
        self.finish_time = finish_time
        self.challenger_id = challenger_id
        self.error_message = error_message
        self.model_package_id = model_package_id
        self.project_id = project_id

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.id)

    @classmethod
    def list(cls, deployment_id: str, retraining_policy_id: str) -> List[RetrainingPolicyRun]:
        """Lists all the retraining policy runs of a retraining policy that is associated with a deployment.

        Parameters
        ----------
        deployment_id : str
            ID of the deployment
        retraining_policy_id : str
            ID of the policy

        Returns
        -------
        policy runs : list
            List of retraining policy runs

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.retraining import RetrainingPolicyRun
            RetrainingPolicyRun.list(
                deployment_id='620ed0e37b6ce03244f19631',
                retraining_policy_id='62f4448f0dfd5699feae3e6e'
            )
            >>> [RetrainingPolicyRun('620ed248bb0a1f5889eb6aa7'), RetrainingPolicyRun('624f68be8828ed81bf487d8d')]

        """

        path = cls._path.format(deployment_id, retraining_policy_id)
        data = unpaginate(path, None, cls._client)
        return [cls.from_server_data(item) for item in data]
