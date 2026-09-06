"""
MCP Server for Hierarchical Task Network HTN Planner Skill.
"""

import json
import sys
from client import HTNPlanner

PLANNER = HTNPlanner()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "register_operator",
                    "description": "Register primitive action operator with preconditions and effects",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "preconditions": {"type": "array", "items": {"type": "string"}},
                            "add_effects": {"type": "array", "items": {"type": "string"}},
                            "del_effects": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["name", "preconditions", "add_effects", "del_effects"]
                    }
                },
                {
                    "name": "plan_task_network",
                    "description": "Decompose compound tasks into primitive plan sequence",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "initial_state": {"type": "array", "items": {"type": "string"}},
                            "task_network": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["initial_state", "task_network"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "register_operator":
            PLANNER.register_operator(
                args["name"],
                args["preconditions"],
                args["add_effects"],
                args["del_effects"]
            )
            return {"content": [{"type": "text", "text": json.dumps({"status": "operator_registered"})}]}

        elif tool_name == "plan_task_network":
            res = PLANNER.plan(set(args["initial_state"]), args["task_network"])
            return {"content": [{"type": "text", "text": json.dumps({"plan": res})}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
