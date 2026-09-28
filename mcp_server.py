import sys
import json
from client import NavierStokes2DSolver

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-navier-stokes-2d-fluid-solver-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "simulate_fluid_step",
                        "description": "Apply force impulse and run Chorin's pressure projection for 2D fluid velocity field",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "nx": {"type": "integer", "default": 16},
                                "ny": {"type": "integer", "default": 16},
                                "force_x": {"type": "number", "default": 5.0},
                                "force_y": {"type": "number", "default": 0.0},
                                "pos_x": {"type": "integer", "default": 8},
                                "pos_y": {"type": "integer", "default": 8},
                                "iterations": {"type": "integer", "default": 20}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "simulate_fluid_step":
            nx = args.get("nx", 16)
            ny = args.get("ny", 16)
            ns = NavierStokes2DSolver(nx=nx, ny=ny)
            ns.add_force(args.get("force_x", 5.0), args.get("force_y", 0.0), args.get("pos_x", 8), args.get("pos_y", 8))
            div_before = ns.max_divergence()
            ns.project(iterations=args.get("iterations", 20))
            div_after = ns.max_divergence()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"max_divergence_before": div_before, "max_divergence_after": div_after})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
