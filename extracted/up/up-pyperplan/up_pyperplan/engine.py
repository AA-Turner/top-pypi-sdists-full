# Copyright 2021 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from functools import partial
from ConfigSpace import ConfigurationSpace
from typing import IO, Callable, List, Dict, Optional, Set, Tuple, Union, cast
import time
import warnings
import unified_planning as up
import unified_planning.engines
import unified_planning.engines.mixins
import unified_planning.engines.compilers
from unified_planning.exceptions import UPUnsupportedProblemTypeError, UPUsageError
from unified_planning.engines import PlanGenerationResultStatus, CompilerResult, Credits
from unified_planning.engines.mixins.compiler import CompilationKind
from unified_planning.model import FNode, ProblemKind, Type as UPType
from up_pyperplan.grounder import rewrite_back_task

from pyperplan.pddl.pddl import Action as PyperplanAction # type: ignore
from pyperplan.pddl.pddl import Type as PyperplanType # type: ignore
from pyperplan.pddl.pddl import Problem as PyperplanProblem # type: ignore
from pyperplan.pddl.pddl import Predicate, Effect, Domain # type: ignore


from pyperplan.planner import _ground, _search, SEARCHES, HEURISTICS # type: ignore

credits = Credits('pyperplan',
                  'Albert-Ludwigs-Universität Freiburg (Yusra Alkhazraji, Matthias Frorath, Markus Grützner, Malte Helmert, Thomas Liebetraut, Robert Mattmüller, Manuela Ortlieb, Jendrik Seipp, Tobias Springenberg, Philip Stahl, Jan Wülfing)',
                  'Jendrik Seipp, Malte Helmert (Pyperplan is now maintained by the AI group at the University of Basel)',
                  'https://github.com/aibasel/pyperplan',
                  'GNU GENERAL PUBLIC LICENSE, Version 3',
                  'Pyperplan is a lightweight STRIPS planner written in Python.',
                  'Pyperplan is a lightweight STRIPS planner written in Python.\nPlease note that Pyperplan deliberately prefers clean code over fast code. It is designed to be used as a teaching or prototyping tool. If you use it for paper experiments, please state clearly that Pyperplan does not offer state-of-the-art performance.\nIt was developed during the planning practical course at Albert-Ludwigs-Universität Freiburg during the winter term 2010/2011 and is published under the terms of the GNU General Public License 3 (GPLv3).\nPyperplan supports the following PDDL fragment: STRIPS without action costs.'
                )

class EngineImpl(
        unified_planning.engines.Engine,
        unified_planning.engines.mixins.OneshotPlannerMixin,
        unified_planning.engines.mixins.CompilerMixin
    ):
    """ Implementation of the up-pyperplan Engine. """


    def __init__(self, search: str = "wastar", heuristic: Optional[str] = "hadd"):
        unified_planning.engines.Engine.__init__(self)
        up.engines.mixins.OneshotPlannerMixin.__init__(self)
        up.engines.mixins.CompilerMixin.__init__(self)
        if search not in SEARCHES:
            raise up.exceptions.UPUsageError(f'{search} not supported!')
        if heuristic not in HEURISTICS:
            raise up.exceptions.UPUsageError(f'{heuristic} not supported!')
        self._search = SEARCHES[search]
        self._heuristic = HEURISTICS[heuristic]
        if search in ["bfs", "ids", "sat"]:
            self._heuristic = None
            self._optimal = True
        elif search == "astar" and heuristic in ["hmax", "blind", "lmcut"]:
            self._optimal = True
        else:
            self._optimal = False

    @property
    def name(self) -> str:
        return "Pyperplan"

    @staticmethod
    def supported_kind() -> ProblemKind:
        supported_kind = ProblemKind(version=2)
        supported_kind.set_problem_class('ACTION_BASED')
        supported_kind.set_typing('FLAT_TYPING')
        supported_kind.set_typing('HIERARCHICAL_TYPING')
        supported_kind.set_quality_metrics("PLAN_LENGTH")
        return supported_kind

    @staticmethod
    def supports(problem_kind: 'up.model.ProblemKind') -> bool:
        return problem_kind <= EngineImpl.supported_kind()

    @staticmethod
    def supports_compilation(compilation_kind: CompilationKind) -> bool:
        return compilation_kind == CompilationKind.GROUNDING

    @staticmethod
    def resulting_problem_kind(
        problem_kind: ProblemKind,
        compilation_kind: Optional[CompilationKind] = None,
    ) -> ProblemKind:
        return problem_kind.clone()

    @staticmethod
    def satisfies(optimality_guarantee: up.engines.OptimalityGuarantee) -> bool:
        return optimality_guarantee == up.engines.OptimalityGuarantee.SATISFICING

    @staticmethod
    def get_credits(**kwargs) -> Optional[unified_planning.engines.Credits]:
        return credits

    @staticmethod
    def get_configuration_space() -> ConfigurationSpace:
        return ConfigurationSpace(space={"search": ["wastar", "astar", "gbf", "bfs", "ehs", "ids", "sat"],
                                         "heuristic": ["hadd", "hmax", "hsa", "hff", "blind", "lmcut", "landmark"]})

    def _compile(self, problem: 'up.model.AbstractProblem',
                 compilation_kind: 'up.engines.CompilationKind') -> CompilerResult:
        assert isinstance(problem, up.model.Problem)
        self.pyp_types: Dict[str, PyperplanType] = {}
        dom = self._convert_domain(problem)
        prob = self._convert_problem(dom, problem)
        task = _ground(prob)
        grounded_problem, rewrite_back_map = rewrite_back_task(task, problem)
        return CompilerResult(grounded_problem, partial(up.engines.compilers.utils.lift_action_instance, map=rewrite_back_map), self.name, [])

    def _solve(self, problem: 'up.model.AbstractProblem',
               heuristic: Optional[Callable[["up.model.state.ROState"], Optional[float]]] = None,
               timeout: Optional[float] = None,
               output_stream: Optional[IO[str]] = None) -> 'up.engines.results.PlanGenerationResult':
        '''This function returns the PlanGenerationResult for the problem given in input.
        The planner used to retrieve the plan is "pyperplan" therefore only flat_typing
        is supported.'''
        assert isinstance(problem, up.model.Problem)
        if heuristic is not None:
            warnings.warn('Pyperplan does not support custom heuristic.', UserWarning)
        if timeout is not None:
            warnings.warn('Pyperplan does not support timeout.', UserWarning)
        if output_stream is not None:
            warnings.warn('Pyperplan does not support output stream.', UserWarning)
        self.pyp_types = {}
        dom = self._convert_domain(problem)
        prob = self._convert_problem(dom, problem)
        start = time.time()
        task = _ground(prob)
        h = None if self._heuristic is None else self._heuristic(task)
        solution = _search(task, self._search, h)
        solving_time = time.time() - start
        actions: List[up.plans.ActionInstance] = []
        if solution is None:
            if self._search in ["bfs", "ids", "astar", "wastar", "gbf"]:
                status = PlanGenerationResultStatus.UNSOLVABLE_PROVEN
            else:
                status = PlanGenerationResultStatus.UNSOLVABLE_INCOMPLETELY
            return up.engines.PlanGenerationResult(status, None, self.name, metrics={"engine_internal_time": str(solving_time)})
        for action_string in solution:
            actions.append(self._convert_string_to_action_instance(action_string.name, problem))
        if self._optimal and len(problem.quality_metrics) > 0:
            status = PlanGenerationResultStatus.SOLVED_OPTIMALLY
        else:
            status = PlanGenerationResultStatus.SOLVED_SATISFICING
        return up.engines.PlanGenerationResult(status, up.plans.SequentialPlan(actions),
                                               self.name, metrics={"engine_internal_time": str(solving_time)})

    def _convert_string_to_action_instance(self, string: str, problem: 'up.model.Problem') -> 'up.plans.ActionInstance':
        assert string[0] == "(" and string[-1] == ")"
        list_str = string[1:-1].split(" ")
        action = problem.action(list_str[0])
        expr_manager = problem.environment.expression_manager
        param = tuple(expr_manager.ObjectExp(problem.object(o_name)) for o_name in list_str[1:])
        return up.plans.ActionInstance(action, param)

    def _convert_problem(self, domain: Domain, problem: 'unified_planning.model.Problem') -> PyperplanProblem:
        objects: Dict[str, PyperplanType] = {o.name: self._convert_type(o.type) for o in problem.all_objects}
        init: List[Predicate] = self._convert_initial_values(problem)
        goal: List[Predicate] = self._convert_goal(problem)
        return PyperplanProblem(problem.name, domain, objects, init, goal)

    def _convert_goal(self, problem: 'up.model.Problem') -> List[Predicate]:
        p_l: List[Predicate] = []
        for f in problem.goals:
            stack: List[FNode] = [f]
            while stack:
                x = stack.pop()
                if x.is_fluent_exp():
                    obj_l: List[Tuple[str, Tuple[PyperplanType]]] = []
                    for o in x.args:
                        obj_l.append((o.object().name, (self._convert_type(o.object().type), )))
                    p_l.append(Predicate(x.fluent().name, obj_l))
                elif x.is_and():
                    stack.extend(x.args)
                else:
                    raise UPUnsupportedProblemTypeError(f'The problem: {problem.name} has expression: {x} into his goals.\nPyperplan does not support that operand.')
        return p_l

    def _convert_initial_values(self, problem: 'up.model.Problem') -> List[Predicate]:
        p_l: List[Predicate] = []
        for f, v in problem.initial_values.items():
            if not v.is_bool_constant():
                raise UPUnsupportedProblemTypeError(f"Initial value: {v} of fluent: {f} is not True or False.")
            if v.bool_constant_value():
                obj_l: List[Tuple[str, PyperplanType]] = []
                for o in f.args:
                    obj_l.append((o.object().name, self._convert_type(o.object().type)))
                p_l.append(Predicate(f.fluent().name, obj_l))
        return p_l

    def _convert_domain(self, problem: 'up.model.Problem') -> Domain:
        self._has_object_type: bool = problem.has_type('object')
        if not self._has_object_type:
            self.pyp_types['object'] = PyperplanType('object', None)
        self.pyp_types.update({cast(up.model.types._UserType, t).name: self._convert_type(t) for t in problem.user_types})
        pyperplan_types = [self.pyp_types.values()]
        predicates: Dict[str, Predicate] = {}
        for f in problem.fluents:
            #predicate_signature
            pred_sign: List[Tuple[str, Tuple[PyperplanType]]] = []
            for param in f.signature:
                pred_sign.append((param.name, (self._convert_type(param.type), )))
            predicates[f.name] = Predicate(f.name, pred_sign)
        actions: Dict[str, PyperplanAction] = {a.name: self._convert_action(a, problem.environment) for a in problem.actions}
        return Domain(f'domain_{problem.name}', pyperplan_types, predicates,  actions)

    def _convert_action(self, action: 'up.model.Action', environment) -> PyperplanAction:
        #action_signature
        assert isinstance(action, up.model.InstantaneousAction)
        act_sign: List[Tuple[str, Tuple[PyperplanType, ...]]] = [(p.name,
            (self._convert_type(p.type), )) for p in action.parameters]
        precond: List[Predicate] = []
        for p in action.preconditions:
            stack: List[FNode] = [p]
            while stack:
                x = stack.pop()
                if x.is_fluent_exp():
                    signature = []
                    for exp in x.args:
                        if exp.is_parameter_exp():
                            signature.append((exp.parameter().name, (self._convert_type(exp.parameter().type), )))
                        elif exp.is_object_exp():
                            signature.append((exp.object().name, (self._convert_type(exp.object().type), )))
                        else:
                            raise NotImplementedError
                    precond.append(Predicate(x.fluent().name, signature))
                elif x.is_and():
                    stack.extend(x.args)
                else:
                    raise UPUnsupportedProblemTypeError(f'In precondition: {x} of action: {action} is not an AND or a FLUENT')
        effect = Effect()
        add_set: Set[Predicate] = set()
        del_set: Set[Predicate] = set()
        for e in action.effects:
            params: List[Tuple[str, Tuple[PyperplanType, ...]]] = []
            for p in e.fluent.args:
                if p.is_parameter_exp():
                    params.append((p.parameter().name,
                                (self._convert_type(p.parameter().type), )))
                elif p.is_object_exp():
                    params.append((p.object().name,
                                (self._convert_type(p.object().type), )))
                else:
                    raise NotImplementedError
            assert not e.is_conditional()
            if e.value.bool_constant_value():
                add_set.add(Predicate(e.fluent.fluent().name, params))
            else:
                del_set.add(Predicate(e.fluent.fluent().name, params))
        effect.addlist = add_set
        effect.dellist = del_set
        return PyperplanAction(action.name, act_sign, precond, effect)

    def _convert_type(self, type: UPType) -> PyperplanType:
        assert type.is_user_type()
        type = cast(up.model.types._UserType, type)
        t = self.pyp_types.get(type.name, None)
        father: Optional[PyperplanType] = None
        if t is not None: # type already defined
            return t
        elif type.father is not None: # type's father is clear
            father = self._convert_type(type.father)
        elif not self._has_object_type: # type father is None and object type is not used, so it's father is pyperplan is 'object'
            father = self.pyp_types['object']
        #else:          # type father is None and object type is used in the problem, so his father also in pyperplan
        #   pass        # must be None; which already is.
        new_t = PyperplanType(type.name, father)
        self.pyp_types[type.name] = new_t
        return new_t


class OptEngineImpl(EngineImpl):
    def __init__(self, search: str = "astar", heuristic: Optional[str] = "lmcut"):
        if search not in ["astar", "bfs", "ids"]:
            raise up.exceptions.UPUsageError(f'{search} not supported!')
        if heuristic not in ["hmax", "blind", "lmcut"]:
            raise up.exceptions.UPUsageError(f'{heuristic} not supported!')
        EngineImpl.__init__(self, search, heuristic)

    @property
    def name(self) -> str:
        return "PyperplanOpt"

    @staticmethod
    def satisfies(optimality_guarantee: up.engines.OptimalityGuarantee) -> bool:
        return True

    @staticmethod
    def get_configuration_space() -> ConfigurationSpace:
        return ConfigurationSpace(space={"search": ["astar", "bfs", "ids"],
                                         "heuristic": ["hmax", "blind", "lmcut"]})
