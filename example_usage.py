"""
Example usage of Hierarchical Task Network HTN Planner Skill.
"""

from client import HTNPlanner


def main():
    print("=== Hierarchical Task Network HTN Planner Demonstration ===")
    planner = HTNPlanner()

    # Define primitive action operators
    planner.register_operator(
        name="navigate_to_repo",
        preconditions=["online"],
        add_effects=["at_repo"],
        del_effects=[]
    )
    planner.register_operator(
        name="run_git_pull",
        preconditions=["at_repo"],
        add_effects=["code_synced"],
        del_effects=[]
    )
    planner.register_operator(
        name="execute_unit_tests",
        preconditions=["code_synced"],
        add_effects=["tests_passed"],
        del_effects=[]
    )
    planner.register_operator(
        name="deploy_to_production",
        preconditions=["tests_passed"],
        add_effects=["deployed"],
        del_effects=[]
    )

    # Define compound methods
    planner.register_method(
        compound_task="release_service",
        preconditions=["online"],
        subtasks=["prepare_build", "deploy_to_production"]
    )
    planner.register_method(
        compound_task="prepare_build",
        preconditions=["online"],
        subtasks=["navigate_to_repo", "run_git_pull", "execute_unit_tests"]
    )

    initial_state = {"online"}
    compound_goal = ["release_service"]

    print("Initial State:", initial_state)
    print("Compound Goal:", compound_goal)

    executable_plan = planner.plan(initial_state, compound_goal)

    print("\nSynthesized Primitive Action Plan:")
    if executable_plan:
        for idx, step in enumerate(executable_plan, 1):
            print(f"  Step {idx}: {step}")
    else:
        print("  Failed to find valid plan satisfying preconditions.")


if __name__ == "__main__":
    main()
