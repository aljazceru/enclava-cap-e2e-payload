#!/usr/bin/env python3
import json
import os
import signal
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_NAME = os.environ.get("APP_NAME", "enclava-cap-e2e-payload")
VERSION = os.environ.get("APP_VERSION", "v1")
PORT = int(os.environ.get("PORT", "8080"))
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
STARTED_AT = datetime.now(timezone.utc).isoformat()


def state_file():
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / "owner-lifecycle-state.json"
        if not path.exists():
            path.write_text(json.dumps({"created_at": STARTED_AT, "version": VERSION}) + "\n")
        return {"path": str(path), "content": json.loads(path.read_text())}
    except Exception as exc:
        return {"path": str(DATA_DIR), "error": str(exc)}


class Handler(BaseHTTPRequestHandler):
    server_version = "enclava-cap-e2e-payload/1"

    def _json(self, code, body):
        payload = json.dumps(body, sort_keys=True).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path in ("/", "/health"):
            self._json(200, {
                "ok": True,
                "app": APP_NAME,
                "version": VERSION,
                "started_at": STARTED_AT,
                "data": state_file(),
            })
            return
        if self.path == "/version":
            self._json(200, {"version": VERSION})
            return
        self._json(404, {"error": "not_found", "path": self.path})

    def log_message(self, fmt, *args):
        sys.stdout.write("%s %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()


httpd = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)

def stop(*_):
    httpd.shutdown()

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
print(f"{APP_NAME} {VERSION} listening on :{PORT}", flush=True)
httpd.serve_forever()
