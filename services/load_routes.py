import importlib.util
from pathlib import Path

from fastapi import FastAPI

import os
import time

def load_dynamic_routes(app: FastAPI, routes_dir="entities"):
    routes_path = Path(routes_dir)
    for route_file in routes_path.rglob("*.py"):
        if route_file.name == "__init__.py":
            continue

        module_name = f"{routes_dir.replace('/', '.')}.{route_file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, route_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            router = getattr(module, "router", None)
            if router:
                prefix = f"/{route_file.stem}"
                print(prefix)
                app.include_router(router)


def trigger_reload(file="main.py"):
    os.utime(file, (time.time(), time.time()))
