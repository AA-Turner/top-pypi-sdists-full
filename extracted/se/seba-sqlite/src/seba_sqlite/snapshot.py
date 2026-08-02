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

from collections import namedtuple

from .database import Database
from .function import Function

OptimizationInfo = namedtuple(
    "OptimizationInfo", "controls objective_value merit_flag batch_id gradient_info"
)
# Contains information about the optimization steps:
#   controls        ->  {control_name : control_value}
#   objective_value -> value # objective value of the optimization step
#   merit_flag      -> 0 or 1 # 1 if the optimization step increases the merit
#                      of the optimization process
#   batch_id        -> the id of the batch generating the optimization step
#   gradient_info   -> gradient information per function for each of the controls.
#   Ex: {
#   'function_name_1': {'control_name_1': control_value,
#                       'control_name_2': control_value,},
#   'function_name_2': {'control_name_1': control_value,
#                       'control_name_2': control_value,}
#   }

Metadata = namedtuple(
    "Metadata", "realizations functions objectives constraints controls"
)
# Contains information about the Seba DB definitions:
#   realization -> dictionary mapping realization ids to seba Realization
#                  objects
#   functions   -> dictionary mapping function ids to Seba Function objects
#   controls    -> dictionary mapping control ids to Seba ControlDefinition
#                  objects


SimulationInfo = namedtuple(
    "SimulationInfo",
    "batch objectives constraints controls sim_avg_obj"
    " is_gradient realization start_time end_time success"
    " realization_weight simulation",
)
# Contains information about the simulations:
#     batch -> the batch id
#     objectives  -> Dictionary mapping the objective function names to the
#                    objective values per simulation also contains mapping
#                    of the normalized and weighted normalized objective values
#     constraints -> Dictionary mapping the constraint function names to the
#                    constraint values per simulation also contains mapping of
#                    the normalized and weighted normalized constraint values
#     controls    -> Dictionary mapping the control names to their values.
#                    Controls generating the simulation results
#     sim_avg_obj -> The value of the objective function for the simulation
#     is_gradient -> Flag describing if the simulation is a gradient or non
#                    gradient simulation
#     realization -> The name of the realization the simulation is part of
#     start_time  -> The starting timpestamp for the simulation
#     end_time    -> The end timpstamp for the simulation
#     success     -> Flag describing if the simulation was successful or not (1 or 0)
#     realization_weight -> The weight of the realization the simulation was part of.
#     simulation  -> The simulation number used in libres


class Snapshot:
    def __init__(self, metadata, simulation_data, optimization_data):
        # Creates Seba database snapshot object
        # :param metadata:
        # :param simulation_data:
        # :param optimization_data:
        self._metadata = metadata
        self._simulation_data = simulation_data
        self._optimization_data = optimization_data

    @property
    def optimization_data(self):
        # :return: List of OptimizationInfo elements
        return self._optimization_data

    @property
    def simulation_data(self):
        # :return: List of SimulationInfo elements
        return self._simulation_data

    @property
    def metadata(self):
        # Seba DB metadata containing information about the realizations function
        # definitions and control definitions
        return self._metadata

    @property
    def expected_single_objective(self):
        # The list of optimization values for each of the optimization steps. In
        # the case of multiple realizations for each optimization step the value
        # is computed as the sum of the optimization value multiplied with the
        # realization weight
        if self._optimization_data:
            return [data_row.objective_value for data_row in self._optimization_data]

        return None

    @property
    def optimization_data_by_batch(self):
        # :return: A dictionary mapping the batch id o the OptimizationInfo element
        if self._optimization_data:
            return {
                optimization.batch_id: optimization
                for optimization in self._optimization_data
            }
        return None

    @property
    def expected_objectives(self):
        # Constructs a dictionary mapping the objective function names to the
        # respective objective value per optimization step. If we are dealing with
        # multiple realization the objective value is calculated as the weighted
        # sum of the individual objective value function per each realization.
        # :return: Expected objective function dictionary.
        # Ex: {
        #      'function_name_1': [obj_val_1, obj_val_1, ..],
        #      'function_name_2': [obj_val_1, obj_val_1, ..]
        #      }
        objective_names = [func.name for func in self._metadata.objectives.values()]
        constraint_names = [func.name for func in self._metadata.constraints.values()]
        function_names = objective_names + constraint_names
        if not self._simulation_data:
            return None

        first_realization = self._simulation_data[0].realization
        expected_objectives = {}
        for sim_info in self._simulation_data:
            for function_name in sim_info.objectives:
                if function_name not in function_names:
                    continue
                if function_name in expected_objectives:
                    if sim_info.realization != first_realization:
                        expected_objectives[function_name][-1] += (
                            sim_info.objectives[function_name]
                            * sim_info.realization_weight
                        )
                    else:
                        expected_objectives[function_name].append(
                            sim_info.objectives[function_name]
                            * sim_info.realization_weight
                        )
                else:
                    expected_objectives[function_name] = [
                        sim_info.objectives[function_name] * sim_info.realization_weight
                    ]
        return expected_objectives

    @property
    def increased_merit_flags(self):
        # :return: A list of merit flags. Ex: [1, 1, 0, 1, 0, 1]
        if self._optimization_data:
            return [data_row.merit_flag for data_row in self._optimization_data]

        return None

    @property
    def increased_merit_indices(self):
        # The index of the single expected objected function that provides an
        # improvement in the optimization process
        # :return: list of indices ex: [0, 1, 3, 5]
        if self.increased_merit_flags:
            return [
                index
                for index, flag in enumerate(self.increased_merit_flags)
                if flag > 0
            ]
        return None

    @property
    def optimization_controls(self):
        # Controls for each of the optimization steps
        # :return: dictionary mapping the control names with a list of control
        # values for each of the optimization steps
        if not self._optimization_data:
            return None

        optimization_controls = {}
        for data in self._optimization_data:
            for name, value in data.controls.items():
                if name in optimization_controls:
                    optimization_controls[name].append(value)
                else:
                    optimization_controls[name] = [value]
        return optimization_controls


class SebaSnapshot:
    def __init__(self, opt_output_folder=None, database=None):
        self.database = (
            Database(outputFolder=opt_output_folder) if database is None else database
        )

    def _simulations_data(self, simulations):
        # Constructs a list of SimulationInfo elements based on a given list of
        # simulations.
        # :param simulations: List of simulation used to construct the
        # SimulationInfo elements
        # :return: A list of SimulationInfo elements
        functions_info = {
            func.function_id: func for func in self.database.load_functions()
        }
        realization_info = {
            realization.realization_id: realization
            for realization in self.database.load_realizations()
        }

        simulation_data = []

        for sim in simulations:
            sim_results = self.database.load_simulation_results(
                simulation_id=sim.simulation_id
            )
            objectives = {}
            constraints = {}
            sim_avg = 0.0
            realization = realization_info[sim.realization_id]

            for result in sim_results:
                function = functions_info[result.function_id]
                if function.function_type == Function.FUNCTION_OBJECTIVE_TYPE:
                    objectives[function.name] = result.value
                    objectives[function.name + "_norm"] = (
                        result.value * function.normalization
                    )
                    objectives[function.name + "_weighted_norm"] = (
                        result.value * function.normalization * function.weight
                    )
                    sim_avg += objectives[function.name + "_weighted_norm"]
                else:
                    constraints[function.name] = result.value
                    constraints[function.name + "_norm"] = (
                        result.value * function.normalization
                    )
                    constraints[function.name + "_weighted_norm"] = (
                        result.value * function.normalization * function.weight
                    )

            simulation_element = SimulationInfo(
                batch=int(sim.batch_id),
                objectives=objectives,
                constraints=constraints,
                controls=dict(self.database.load_control_values(set_id=sim.set_id)),
                sim_avg_obj=sim_avg,
                is_gradient=sim.is_gradient,
                realization=realization.name,
                start_time=sim.start_time_stamp,
                end_time=sim.end_time_stamp,
                success=sim.success,
                realization_weight=realization.weight,
                simulation=sim.name.split("_")[-1],
            )

            simulation_data.append(simulation_element)
        return simulation_data

    def _gradients_for_batch_id(self, batch_id, func_info, control_info):
        # Retrieves gradient information for a specified bach id.
        # :param batch_id: The required batch id
        # :param func_info: dictionary mapping function ids to the Function
        # objects in the Seba DB
        # :param control_info: dictionary mapping control definition ids to the
        # ControlDefinitions in the Seba DB
        # :return: Gradient information per function for each of the controls.
        # Returned dictionary example structure
        # {
        #  'function_name_1': {'control_name_1': control_value,
        #                      'control_name_2': control_value,},
        #  'function_name_2': {'control_name_1': control_value,
        #                      'control_name_2': control_value,}
        # }
        gradient_info = {}
        for result in self.database.load_gradient_results(batch_id=batch_id):
            function = func_info[result.function_id]
            control = control_info[result.control_definition_id]
            if function.name in gradient_info:
                gradient_info[function.name].update({control.name: result.value})
            else:
                gradient_info[function.name] = {control.name: result.value}
        return gradient_info

    def _optimization_data(self):
        # :return: List of optimizationInfo elements
        func_info = {func.function_id: func for func in self.database.load_functions()}
        control_info = {
            control.control_id: control
            for control in self.database.load_control_definitions()
        }
        calc_results = self.database.load_calculation_results()
        calc_results.sort(key=lambda x: x.batch_id)
        optimization_data = []

        for result in calc_results:
            gradient_info = self._gradients_for_batch_id(
                result.batch_id, func_info, control_info
            )
            optimization_data.append(
                OptimizationInfo(
                    controls=dict(
                        self.database.load_control_values(set_id=result.set_id)
                    ),
                    objective_value=result.object_function_value,
                    merit_flag=result.improved_flag,
                    batch_id=result.batch_id,
                    gradient_info=gradient_info,
                )
            )

        return optimization_data

    def _metadata(self):
        # :return: The metadata data structure
        return Metadata(
            realizations={
                realization.realization_id: realization
                for realization in self.database.load_realizations()
            },
            functions={
                func.function_id: func for func in self.database.load_functions()
            },
            objectives={
                func.function_id: func
                for func in self.database.load_functions(
                    function_type=Function.FUNCTION_OBJECTIVE_TYPE
                )
            },
            constraints={
                func.function_id: func
                for func in self.database.load_functions(
                    function_type=Function.FUNCTION_CONSTRAINT_TYPE
                )
            },
            controls={
                control.control_id: control
                for control in self.database.load_control_definitions()
            },
        )

    def _filtered_simulation_data(self, filter_out_gradient=False, batches=None):
        # Filter simulation by gradient type and by bach ids
        # :param filter_out_gradient: If set to true will only return a list of
        # non gradient simulation
        # :param batches: List of batch ids. If given the return list will contain
        # only simulations associated with the given batch ids
        # :return: List of filtered simulations
        simulations = self.database.load_simulations(
            filter_out_gradient=filter_out_gradient
        )
        if batches:
            simulations = [sim for sim in simulations if sim.batch_id in batches]
        return simulations

    def get_snapshot(self, filter_out_gradient=False, batches=None):
        # Builds and returns a snapshot of the Seba database containing
        # information about the database at the moment the function is called.
        # :param filter_out_gradient: If provided can filter the information in
        # the returned snapshot based on simulation gradient type
        # :param batches: If a list of batch ids is provide it will return seba
        # database information for the given batch ids
        # :return: The seba db Snapshot
        return Snapshot(
            metadata=self._metadata(),
            optimization_data=self._optimization_data(),
            simulation_data=self._simulations_data(
                self._filtered_simulation_data(filter_out_gradient, batches)
            ),
        )

    def get_optimization_data(self):
        # Builds and returns a snapshot of the optimization data in the Seba
        # database at the moment the function is called.
        # :return: The optimization data.
        return self._optimization_data()
