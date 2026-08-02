# Copyright (C) The Netherlands Organisation for Applied Scientific Research,
# TNO, 2015-2022. All rights reserved.
#
# This file is part of Seba: a proprietary software library for ensemble based
# optimization developed by TNO. This file, the Seba software or data or
# information contained in the software may not be copied or distributed without
# prior written permission from TNO.
#
# Seba and the information and data contained in this software are confidential.
# Neither the whole or any part of the software and the data and information it
# contains may be disclosed to any third party without the prior written consent
# of The Netherlands Organisation for Applied Scientific Research (TNO).

import os.path
import sqlite3
import time

from .batch import Batch
from .calculation_result import CalculationResult
from .control_definition import ControlDefinition
from .control_value import ControlValue
from .exceptions import ObjectNotFoundError
from .experiment import Experiment
from .function import Function
from .gradient_result import GradientResult
from .realization import Realization
from .simulation import Simulation
from .simulation_result import SimulationResult


# This class is rather large since it is the interface to the database:
class Database:
    FILENAME = "seba.db"

    def __init__(self, outputFolder):
        # :param outputFolder: The folder the database should reside in
        # :type outputFolder: string
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)

        self.experiment = None
        self.location = os.path.join(outputFolder, self.FILENAME)
        self.conn = None
        self._init_db()

    def _init_db(self):
        # Initializes the database instance from the database file.
        # If the file does not exist is will be created with an empty database.

        # If the file exists it will assume one experiment has been already
        # logged and it will be retrieved with all its related data.

        # ===================
        # =====IMPORTANT=====
        # ===================
        # The order of the columns in the tables declared here need to be the same
        # as the corresponding class' arguments.

        if not os.path.isfile(self.location):
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE ControlDefinition ( "
                "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                "`experimentId` INTEGER NOT NULL, "
                "`name` TEXT NOT NULL, "
                "`initialValue` DOUBLE DEFAULT 0, "
                "`minValue` DOUBLE DEFAULT 0, "
                "`maxValue` DOUBLE DEFAULT 0)"
            )
            cursor.execute(
                "CREATE TABLE ControlValue ( "
                "`setId` INTEGER NOT NULL, "
                "`controlDefinitionId` INTEGER NOT NULL, "
                "`value` DOUBLE NOT NULL, PRIMARY KEY(`controlDefinitionId`,`setId`))"
            )
            # to start id from 0, we will handle it ourselves (vis __init__ in batch.py)
            cursor.execute(
                "CREATE TABLE Batch ( "
                "`id` INTEGER NOT NULL DEFAULT 0, "
                "`experimentId` INTEGER NOT NULL, "
                "`startTimeStamp` NUMERIC NOT NULL, "
                "`endTimeStamp` NUMERIC, "
                "`success` INTEGER DEFAULT 1 CHECK(success in (0,1)) )"
            )
            cursor.execute(
                "CREATE TABLE Experiment ( "
                "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                "`name` TEXT NOT NULL UNIQUE, "
                "`startTimeStamp` NUMERIC NOT NULL, "
                "`endTimeStamp` NUMERIC )"
            )
            cursor.execute(
                "CREATE TABLE Realization ( "
                "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                "`name` TEXT NOT NULL, "
                "`experimentId` INTEGER NOT NULL, "
                "`weight` NUMERIC NOT NULL, "
                "`configuration` BLOB )"
            )
            cursor.execute(
                "CREATE TABLE Function ( "
                "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                "`name` TEXT NOT NULL UNIQUE, "
                "`experimentId` INTEGER NOT NULL, "
                "`weight` NUMERIC NOT NULL DEFAULT 0, "
                "`normalization` NUMERIC NOT NULL DEFAULT 0, "
                "`type` TEXT NOT NULL, "
                "`righthandside` NUMERIC NOT NULL DEFAULT 0,"
                " `constraintType` TEXT )"
            )
            cursor.execute(
                "CREATE TABLE Simulation ( "
                "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                "`batchID` INTEGER NOT NULL, "
                "`realizationId` INTEGER NOT NULL, "
                "`setId` INTEGER NOT NULL, "
                "`startTimeStamp` NUMERIC NOT NULL, "
                "`endTimeStamp` NUMERIC, "
                "`name` TEXT NOT NULL, "
                "`success` INTEGER DEFAULT 1 CHECK(success in ( 0 , 1 )), "
                "`isGradient` INTEGER DEFAULT 0 CHECK(isGradient in ( 0 , 1 )) )"
            )
            cursor.execute(
                "CREATE TABLE SimulationResult ( "
                "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                "`simulationId` INTEGER NOT NULL, "
                "`functionId` INTEGER NOT NULL, "
                "`value` DOUBLE, "
                "`timesIndex` INTEGER )"
            )
            cursor.execute(
                "CREATE TABLE GradientResult ( "
                "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                "`batchId` INTEGER NOT NULL, "
                "`functionId` INTEGER NOT NULL, "
                "`value` DOUBLE, "
                "`success` INTEGER NOT NULL DEFAULT 1 CHECK(success in ( 0 , 1 )), "
                "`controlId` INTEGER NOT NULL )"
            )
            cursor.execute(
                "CREATE TABLE CalculationResult ( "
                "`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                "`batchId` INTEGER NOT NULL, "
                "`setId` INTEGER NOT NULL, "
                "`value` DOUBLE, "
                "`meritFnValue` DOUBLE, "
                "`improvedFlag` INTEGER DEFAULT 0 CHECK(improvedFlag in ( 0 , 1 )))"
            )
            conn.commit()
        else:
            # The file exists, assume it has already an experiment added and retrieve it
            self.experiment = self.load_experiment()

    def _get_connection(self):
        # gets the connection to the database.
        # :return a connection to the database
        # :rtype
        if self.conn:
            return self.conn

        self.conn = sqlite3.connect(self.location)
        return self.conn

    def add_experiment(self, name=None, start_time_stamp=None):
        # Creates a new experiment
        # :param name: the name of the new experiment
        # :type name: str
        # :param start_time_stamp: the start timestamp of the new experiment
        # :type start_time_stamp: float

        self.experiment = Experiment.create_or_get_existing(
            self._get_connection(), name=name, starttime=start_time_stamp
        )

    def load_experiment(self, experiment_id=None, retries=5):
        # Loads an existing experiment specified by the experiment_id.
        # If experiment_id is None it will load the first experiment in the database.

        # If there is no experiment in the database it will create one
        # :param experiment_id: the experiment_id of an existing experiment in the
        # database, set to None when creating a new experiment
        # :type experiment_id: int
        # :return experiment
        # :rtype seba.database.Experiment
        error_msg = None
        for _ in range(retries):
            try:
                return Experiment.get(
                    self._get_connection(), experiment_id=experiment_id
                )
            except ObjectNotFoundError as msg:
                error_msg = msg
                time.sleep(1)
        raise ObjectNotFoundError(error_msg)

    def add_batch(self):
        # Adds a new batch to the current experiment.
        # :return batch
        # :rtype seba.database.Batch
        conn = self._get_connection()
        Batch.create_or_get_existing(
            conn,
            experiment_id=self.experiment.experiment_id,
            start_time_stamp=time.time(),
        )

    def load_batch(self, batch_id=None):
        # Load a batch from the database with the given id.
        # If this id is not found an error is raised
        # :param batch_id: The id of the requested batch - in the current experiment
        # :return:
        return Batch.get(
            self._get_connection(),
            experiment=self.experiment.experiment_id,
            batch_id=batch_id,
        )

    def get_number_of_batches(self):
        # Gets the number of batches from the database
        # :return The number of batches if there are any or None otherwise
        conn = self._get_connection()
        all_batches_experiment = Batch.get_for_experiment(
            conn, self.experiment.experiment_id
        )
        return len(all_batches_experiment)

    def load_last_batch(self):
        # Loads the last batch in order of batch_id
        # The last batch added is assumed to be active batch

        # :return:  The last batch in the current experiment
        # :rtype: seba.database.Batch
        conn = self._get_connection()
        all_batches_experiment = Batch.get_for_experiment(
            conn, self.experiment.experiment_id
        )
        if not all_batches_experiment:
            raise AttributeError()
        return max(all_batches_experiment, key=lambda b: b.batch_id)

    def add_control_value(self, set_id, control_name, value):
        # Adds a new control_value to the specified perturbation.
        # :param perturbationName: the perturbation name
        # :type perturbation: str
        # :param control_name: the name of the control definition this value if for
        # :type control_name: str
        # :param value: the value
        # :type value: float

        ControlValue.create_or_get_existing(
            self._get_connection(),
            set_id=set_id,
            control_definition_id=self.load_control_definition(
                name=control_name
            ).control_id,
            value=value,
        )

    def load_control_values(self, set_id=None, batch_id=None):
        if set_id is not None and batch_id is None:
            return [
                (
                    self.load_control_definition(
                        control_id=v.control_definition_id
                    ).name,
                    v.value,
                )
                for v in ControlValue.get_for_set(self._get_connection(), set_id=set_id)
            ]
        if batch_id is not None and set_id is None:
            return [
                self.load_control_values(set_id=sim.set_id)
                for sim in [
                    s for s in self.load_simulations() if s.batch_id == batch_id
                ]
            ]
        return ControlValue.get_all(self._get_connection())

    def add_control_definition(self, name, init_value, min_value, max_value):
        # Adds a new control definition to the current experiment.
        # :param name: the name of the control definition
        # :type name: str
        # :param init_value: the initial value of the control definition
        # :type init_value: float
        # :param min_value: the minimal value of the control definition
        # :type min_value: float
        # :param max_value: the maximum value of the control definition
        # :type max_value: float
        # :return controlDef
        # :rtype seba.database.ControlDefinition

        ControlDefinition.create_or_get_existing(
            self._get_connection(),
            name=name,
            experiment_id=self.experiment.experiment_id,
            initial_value=init_value,
            min_value=min_value,
            max_value=max_value,
        )

    def load_control_definition(self, control_id=None, name=None):
        # Return a control definition with the given name from the database.
        # :param name: the name of the control definition
        # :type name: str
        # :return controlDefinition
        # :rtype seba.database.ControlDefinition
        return ControlDefinition.get(
            self._get_connection(),
            control_id=control_id,
            name=name,
            experiment_id=self.experiment.experiment_id,
        )

    def load_control_definitions(self):
        # resturns a list of ControlDefinitions
        return ControlDefinition.get_all(self._get_connection())

    def add_realization(self, name, weight):
        # Return a new realization with the given name.
        # :param name: the name of the realization
        # :type name: str
        Realization.create_or_get_existing(
            self._get_connection(),
            name=name,
            experiment_id=self.experiment.experiment_id,
            weight=weight,
        )

    def load_realization(self, name=None, realization_id=None):
        # Return a Realization with the given name from the database.
        # :param name: the name of the realization
        # :type name: str
        # :return realization
        # :rtype seba.database.Realization
        if name is not None and realization_id is None:
            return Realization.get(
                self._get_connection(),
                name=name,
                experiment_id=self.experiment.experiment_id,
            )
        if realization_id is not None and name is None:
            return Realization.get(
                self._get_connection(), realization_id=realization_id
            )
        raise ValueError("exactly one of 'name' or 'realization_id' must be provided")

    def load_realizations(self):
        # returns a list of all the realizations.
        # realizations are also known as evaluation in some
        # contexts
        return Realization.get_all(self._get_connection())

    def add_function(
        self,
        name,
        function_type,
        weight=1.0,
        normalization=1.0,
        rhs_value=0.0,
        constraint_type=None,
    ):
        # Return a new function with the given name and description.
        # :param name: the name of the function
        # :type name: str
        # :param function_type: the type of the function
        # :type function_type: str
        # :param weight: the weight of the function
        # :type weight: float
        # :param normalization: the normalization of the function
        # :type normalization: float
        # :param rhs_value: the rhs_value of the constraint function
        # :type rhs_value: float
        # :param constraint_type: the constraint_type the function
        # :type constraint_type: str
        # :return function
        # :rtype seba.database.Function
        Function.create_or_get_existing(
            self._get_connection(),
            name=name,
            experiment_id=self.experiment.experiment_id,
            weight=weight,
            normalization=normalization,
            rhs_value=rhs_value,
            function_type=function_type,
            constraint_type=constraint_type,
        )

    def load_function(self, name=None, function_id=None):
        # Return a Function with the given name from the database.
        # :param name: the name of the function
        # :type name: str
        # :return Function
        # :rtype seba.database.Function
        if name is not None and function_id is None:
            return Function.get(
                self._get_connection(),
                name=name,
                experiment_id=self.experiment.experiment_id,
            )
        if function_id is not None and name is None:
            return Function.get(self._get_connection(), function_id=function_id)
        raise ValueError("exactly one of 'name' or 'function_id' must be provided")

    def load_functions(self, function_type=None):
        objective_functions = Function.get_all_by_type(
            self._get_connection(), Function.FUNCTION_OBJECTIVE_TYPE
        )
        constraint_functions = Function.get_all_by_type(
            self._get_connection(), Function.FUNCTION_CONSTRAINT_TYPE
        )
        if function_type == Function.FUNCTION_OBJECTIVE_TYPE:
            return objective_functions
        if function_type == Function.FUNCTION_CONSTRAINT_TYPE:
            return constraint_functions
        return objective_functions + constraint_functions

    def add_simulation(self, realization_name, set_id, sim_name, is_gradient):
        # Return a new simulation with the given information.

        # :param realization_name: The realization this simulation is using
        # :type realization_name: str
        # :param set_id: the set this simulation is using
        # :type set_id: int
        # :param sim_name: the name of this simulation
        # :type sim_name: str
        # :param is_gradient: True if this simulation result will be used for
        # gradient estimation
        # :type is_gradient: bool
        Simulation.create_or_get_existing(
            self._get_connection(),
            batch_id=self.load_last_batch().batch_id,
            realization_id=self.load_realization(name=realization_name).realization_id,
            set_id=set_id,
            start_time_stamp=time.time(),
            name=sim_name,
            is_gradient=is_gradient,
        )

    def load_simulation(self, name=None, simulation_id=None):
        # Load simulation record by using the simulation name or id
        # :param sim_name: The simulation name, probably formatted as:
        # <batch_number>_<simulation_num>
        # :type sim_name: str
        # :param simulation_id: The simulation id
        # :type simulation_id: str
        # :return: seba.database.Simulation
        conn = self._get_connection()
        if name is not None and simulation_id is None:
            return Simulation.get(conn, name=name)
        if simulation_id is not None and name is None:
            return Simulation.get(conn, simulation_id=simulation_id)
        raise ValueError("exactly one of 'name' or 'simulation_id' must be provided")

    def load_simulations(self, filter_out_gradient=False):
        if filter_out_gradient:
            return Simulation.filter_by_gradient(self._get_connection(), gradient=False)
        return Simulation.get_all(self._get_connection())

    def add_gradient_result(
        self, gradient_value, function_name, success, control_definition_name
    ):
        # Return a new simulation result with the given information.
        # :param gradient_value: result value of the simulation
        # :type gradient_value: float
        # :param function_name: name of the function this value is for
        # :type function_name: str
        # :param success: successful simulation ?
        # :type success: int [0|1]
        # :param control_definition_name: name of the control definition
        # :type control_definition_name: str
        # :return gradientResult
        # :rtype seba.database.GradientResult

        if function_name is not None:
            GradientResult.get_update_or_create(
                self._get_connection(),
                batch_id=self.load_last_batch().batch_id,
                function_id=self.load_function(function_name).function_id,
                control_definition_id=self.load_control_definition(
                    name=control_definition_name
                ).control_id,
                gradient_value=gradient_value,
                success=success,
            )

    def load_gradient_results(self, batch_id=None):
        if batch_id is not None:
            return GradientResult.get_for_batch_id(self._get_connection(), batch_id)
        return GradientResult.get_all(self._get_connection())

    def set_simulation_ended(self, sim_name, success):
        # Set end timestamp for a specific simulation
        # :param sim_name: sim_id
        # :type sim_name: str
        # :param success: successful simulation ?
        # :type success: int [0|1]
        self.load_simulation(name=sim_name).set_ended(
            self._get_connection(), success, time.time()
        )

    def set_batch_ended(self, end_time, success):
        # set end timestamp for a the current batch
        # :param end_time: the end timestamp
        # :type end_time: float
        # :param success: successful simulatie ?
        # :type success: int [0|1]
        self.load_last_batch().set_ended(self._get_connection(), end_time, success)

    def set_experiment_ended(self, end_time):
        # set end timestamp for a the current experiment
        # :param end_time: the end timestamp
        # :type end_time: float
        self.experiment.set_ended(self._get_connection(), end_time)

    def add_calculation_result(
        self,
        set_id,
        object_function_value=None,
        merit_function_value=None,
        improved_flag=False,
    ):
        # :param set_id: the set_id of a control set in the database
        # :type set_id: str or None
        # :param object_function_value: averaged objectives over realizations
        # :type object_function_value: float
        # :param merit_function_value: merit function value of the current
        # simulation state
        # :type merit_function_value: float
        # :param improved_flag: True if the merit function has been only improving
        # recently
        # :type improved_flag: Boolean
        CalculationResult.create_or_get_existing(
            self._get_connection(),
            batch_id=self.load_last_batch().batch_id,
            set_id=set_id,
            object_function_value=float(object_function_value)
            if object_function_value is not None
            else None,
            merit_function_value=float(merit_function_value)
            if merit_function_value is not None
            else None,
            improved_flag=bool(improved_flag) if improved_flag is not None else None,
        )

    def update_calculation_result(self, merit_items):
        # Updates the merit values and improvement flags associated with
        # calculation results.
        # :param merit_items: List of merit items: The "idx" value in a merit item
        # is equal to the function evaluation counter, starting at 0.
        #  example: [
        #     {"iter": 0, "value": merit_value_0}
        #     {"iter": 1, "value": merit_value_1}
        #     {"iter": 2, "value": merit_value_2}
        #     ....
        # ]
        calculation_results = self.load_calculation_results()
        if len(merit_items) > 0:
            merit_values = [item["value"] for item in merit_items]
            # merit improvement means lower value
            improved_merit_indices = [0] + [
                inx
                for inx, val in list(enumerate(merit_values))[1:]
                if merit_values[inx] < min(merit_values[:inx])
            ]
            for inx, merit_item in enumerate(merit_items):
                result = calculation_results[merit_item["iter"]]
                improved_flag = inx in improved_merit_indices
                if result.improved_flag != improved_flag:
                    result.improved_flag = improved_flag
                    result.merit_function_value = merit_item["value"]
                    result.save(self._get_connection())
            if not calculation_results[0].improved_flag:
                calculation_results[0].improved_flag = True
                calculation_results[0].save(self._get_connection())
        else:
            max_fn = None
            for result in calculation_results:
                merit_flag = False
                if max_fn is None or result.object_function_value > max_fn:
                    max_fn = result.object_function_value
                    merit_flag = True
                if result.improved_flag != merit_flag:
                    result.improved_flag = merit_flag
                    result.save(self._get_connection())

    def load_calculation_results(self):
        return CalculationResult.get_all(self._get_connection())

    def add_simulation_result(self, sim_name, result_value, function_name, times_index):
        # Add a simulation result record in the database with the given data
        # :param sim_name: The name of this simulation
        # :type sim_name: str
        # :param result_value: result value of the simulation
        # :type result_value: float
        # :param function_name: function_name this value if for
        # :type function_name: str
        # :param times_index: time index of result
        # :type times_index: int
        if function_name is not None:
            SimulationResult.create_or_get_existing(
                self._get_connection(),
                simulation_id=self.load_simulation(name=sim_name).simulation_id,
                function_id=self.load_function(function_name).function_id,
                value=result_value,
                times_index=times_index,
            )

    def update_simulation_result(
        self, simulation_name, function_name, times_index, value
    ):
        if function_name is not None:
            conn = self._get_connection()
            sim_results = SimulationResult.get_all(conn)

            simulation_id = self.load_simulation(name=simulation_name).simulation_id
            function_id = self.load_function(function_name).function_id

            relevant_sim_result = [
                sim_res
                for sim_res in sim_results
                if (
                    sim_res.simulation_id == simulation_id
                    and sim_res.function_id == function_id
                    and sim_res.times_index == times_index
                )
            ][0]
            relevant_sim_result.value = value
            relevant_sim_result.save(conn)

    def load_simulation_results(
        self, name=None, simulation_id=None, function_name=None, function_type=None
    ):
        if name is not None and simulation_id is None and function_name is None:
            simulation = Simulation.get(self._get_connection(), name=name)
            tmp_results = self.load_simulation_results(
                simulation_id=simulation.simulation_id
            )
            sim_results = []
            for inx in tmp_results:
                function = Function.get(
                    self._get_connection(), function_id=inx.function_id
                )
                if function_type is None or function.function_type == function_type:
                    sim_results_local = {}
                    sim_results_local["name"] = function.name
                    sim_results_local["value"] = inx.value
                    sim_results_local["simulation_id"] = inx.simulation_id
                    sim_results.append(sim_results_local)
            return sim_results
        if simulation_id is not None and name is None and function_name is None:
            return SimulationResult.get_for_simulation(
                self._get_connection(), simulation_id
            )
        if function_name is not None and name is None and simulation_id is None:
            function = self.load_function(function_name)
            if (
                function_type
                in [function.FUNCTION_OBJECTIVE_TYPE, function.FUNCTION_CONSTRAINT_TYPE]
                and function.function_type != function_type
            ):
                return []
            return SimulationResult.get_for_function(
                self._get_connection(), function_id=function.function_id
            )
        return SimulationResult.get_all(self._get_connection())
