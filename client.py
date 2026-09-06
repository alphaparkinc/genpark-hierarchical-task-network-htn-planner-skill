"""
Hierarchical Task Network HTN Planner Skill Client
Pure Python Standard Library implementation of Hierarchical Task Network (HTN) Planning (SHOP2 style).
Recursively decomposes compound high-level goals into executable primitive actions
by verifying task preconditions and applying domain methods.
"""

from typing import List, Dict, Any, Tuple, Optional, Set


class HTNPlanner:
    """
    Hierarchical Task Network planning engine.
    State is modeled as a set of ground predicates (e.g. "at(robot, lab)", "has_key(door1)").
    Methods decompose compound tasks into subtasks.
    Operators represent primitive actions with preconditions and add/delete effects.
    """

    def __init__(self):
        self.methods: Dict[str, List[Dict[str, Any]]] = {}
        self.operators: Dict[str, Dict[str, Any]] = {}

    def register_operator(self, name: str, preconditions: List[str], add_effects: List[str], del_effects: List[str]):
        """Register primitive action operator."""
        self.operators[name] = {
            "preconditions": set(preconditions),
            "add_effects": set(add_effects),
            "del_effects": set(del_effects)
        }

    def register_method(self, compound_task: str, preconditions: List[str], subtasks: List[str]):
        """Register method decomposing compound task into subtasks."""
        if compound_task not in self.methods:
            self.methods[compound_task] = []
        self.methods[compound_task].append({
            "preconditions": set(preconditions),
            "subtasks": subtasks
        })

    def plan(self, initial_state: Set[str], task_network: List[str]) -> Optional[List[str]]:
        """
        Decompose task network into ordered list of primitive actions using depth-first search.
        """
        plan_result = []

        def dfs(state: Set[str], tasks: List[str]) -> Optional[Tuple[Set[str], List[str]]]:
            if not tasks:
                return state, []

            curr_task = tasks[0]
            remaining_tasks = tasks[1:]

            # Case 1: Primitive operator
            if curr_task in self.operators:
                op = self.operators[curr_task]
                if op["preconditions"].issubset(state):
                    new_state = (state - op["del_effects"]) | op["add_effects"]
                    res = dfs(new_state, remaining_tasks)
                    if res is not None:
                        final_state, future_actions = res
                        return final_state, [curr_task] + future_actions
                return None

            # Case 2: Compound method decomposition
            if curr_task in self.methods:
                for method in self.methods[curr_task]:
                    if method["preconditions"].issubset(state):
                        expanded_tasks = method["subtasks"] + remaining_tasks
                        res = dfs(state, expanded_tasks)
                        if res is not None:
                            return res
                return None

            # Unknown task
            return None

        result = dfs(set(initial_state), list(task_network))
        if result is not None:
            return result[1]
        return None
