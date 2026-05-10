#!/usr/bin/env python3
"""Build the static CV site from content/cv.json."""
from __future__ import annotations

import http.server
import json
import shutil
import socketserver
import sys
from functools import partial
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT = ROOT / "content" / "cv.json"
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"


def build() -> None:
    data = json.loads(CONTENT.read_text(encoding="utf-8"))

    # Reverse-chronological sort
    for key in ("publications", "talks"):
        if key in data and isinstance(data[key], list):
            data[key].sort(key=lambda x: x.get("year", 0), reverse=True)

    profile = data.get("profile", {})
    me_names = {profile.get("name", "")} | set(profile.get("name_variants", []))
    me_names.discard("")

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    env.globals["is_me"] = lambda author: author in me_names

    html = env.get_template("index.html").render(**data)

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    (DIST / "index.html").write_text(html, encoding="utf-8")
    shutil.copytree(ASSETS, DIST / "assets")

    print(f"Built: {DIST}/index.html")


def serve(port: int = 8000) -> None:
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving http://localhost:{port}  (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
