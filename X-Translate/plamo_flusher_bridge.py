"""Two-endpoint PLaMo 3 Translate bridge using one local llama.cpp server.

Edit LLAMA_SERVER_EXE and GGUF_MODEL_FILE below, then run:
  python plamo_flusher_bridge.py

GET http://127.0.0.1:8001/translate-X?q=$q  Auto source -> Traditional Chinese (X posts; X-Translate)
GET http://127.0.0.1:8001/translate?q=$q    Auto source -> Traditional Chinese (Live chat; YT Flusher; disabled by default)
Set ENABLE_FLUSHER = True to enable the live chat endpoint before launch.
Both endpoints use the Google Translate-style JSON response used by YT Flusher.
Incoming sl/tl query parameters are ignored by both endpoints.

Optional environment variables:
  PLAMO_CONTEXT       context for the live chat endpoint
  PLAMO_AUTO_CONTEXT  context for the X posts endpoint
Sampling controls and maximum prediction tokens remain in llama-server CLI.
"""

import json
import os
import socket
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# ===== Edit these two Windows paths before the first launch =====
LLAMA_SERVER_EXE = Path(r"I:\llama.cpp\llama-server.exe")
GGUF_MODEL_FILE = Path(r"I:\_models\plamo-3-translate-0.8b-Q4_K_M.gguf")
# ================================================================

ENABLE_FLUSHER = False    # Enable the live chat /translate endpoint
TARGET_LANG = "zh-hant"      # Fixed target for both endpoints

AUTO_CONTEXT = os.getenv("PLAMO_AUTO_CONTEXT", "X（旧Twitter）に投稿されたポストです。")
CONTEXT = os.getenv(
    "PLAMO_CONTEXT",
    "日本の配信者のライブ配信に寄せられた視聴者コメントです。ゲーム、配信、視聴者の俗語が使われています。",
)

HOST = "127.0.0.1"
PORT = 8001                 # Translation API port
LLAMA_HOST = "127.0.0.1"
LLAMA_PORT = 8000           # llama-server OpenAI-compatible API
LLAMA_STARTUP_TIMEOUT = 120  # seconds; startup only, not a translation timeout
MODEL = "plamo-3-translate"
BACKEND_URL = f"http://{LLAMA_HOST}:{LLAMA_PORT}/v1/completions"

# This adapter talks exclusively to a localhost llama-server. Bypass ALL system
# / environment proxies (Windows proxy settings, HTTP_PROXY, etc.) for both
# the readiness check and inference calls. urllib.request.urlopen() may inherit
# those proxies and fail even when the model is already listening on 127.0.0.1.
LOCAL_HTTP = urllib.request.build_opener(urllib.request.ProxyHandler({}))

# All sampling defaults live here, in the llama-server command line.
# The /v1/completions request intentionally does NOT set sampling fields.
LLAMA_SERVER_ARGS = [
    "--alias", MODEL,
    "--host", LLAMA_HOST,
    "--port", str(LLAMA_PORT),
    "--n-gpu-layers", "99",
    "--ctx-size", "2048",
    "--n-predict", "256",
    "--parallel", "4",
    "--jinja",
    "--no-prefill-assistant",
    "--temp", "0"
]

GLOSSARY_PATH = Path(__file__).with_name("glossary.json")

TOKENS = ("<|plamo:tag|>", "<|plamo:msg|>", "<|plamo:key|>",
          "<|plamo:val|>", "<|plamo:index|>", "<|plamo:item|>", "<|plamo:bos|>")

def start_llama_server() -> subprocess.Popen:
    """Start our own llama-server, refusing to attach to an unrelated port listener."""
    if not LLAMA_SERVER_EXE.is_file():
        raise FileNotFoundError(
            f"llama-server not found: {LLAMA_SERVER_EXE}\n"
            "Edit LLAMA_SERVER_EXE near the top of this .py file."
        )
    if not GGUF_MODEL_FILE.is_file():
        raise FileNotFoundError(
            f"GGUF model not found: {GGUF_MODEL_FILE}\n"
            "Edit GGUF_MODEL_FILE near the top of this .py file."
        )

    # Avoid assuming that a preexisting server on 8000 is our model.
    try:
        with socket.create_connection((LLAMA_HOST, LLAMA_PORT), timeout=1):
            raise RuntimeError(
                f"Port {LLAMA_PORT} is already in use. Stop that service, "
                "or change LLAMA_PORT in this script."
            )
    except (ConnectionRefusedError, TimeoutError, OSError):
        pass

    command = [str(LLAMA_SERVER_EXE), "-m", str(GGUF_MODEL_FILE), *LLAMA_SERVER_ARGS]
    print("Starting llama-server:", subprocess.list2cmdline(command), flush=True)
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    # Inherit the current console so all llama.cpp loading/errors remain visible.
    return subprocess.Popen(command, cwd=str(LLAMA_SERVER_EXE.parent), creationflags=flags)


def wait_for_llama_server(process: subprocess.Popen) -> None:
    health_url = f"http://{LLAMA_HOST}:{LLAMA_PORT}/health"
    deadline = time.monotonic() + LLAMA_STARTUP_TIMEOUT
    next_report = time.monotonic() + 5
    last_check = "no health response yet"
    print(f"Waiting for the model to load (direct localhost HTTP; proxy disabled): {health_url}", flush=True)
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"llama-server exited early (exit code {process.returncode}).")
        try:
            # LOCAL_HTTP has ProxyHandler({}); no proxy intercepts local /health.
            with LOCAL_HTTP.open(health_url, timeout=2) as response:
                if response.status == 200:
                    print("PLaMo model ready (HTTP /health 200).", flush=True)
                    return
                last_check = f"HTTP {response.status}"
        except urllib.error.HTTPError as exc:
            # HTTP 503 is normal while llama-server is loading a GGUF file.
            if exc.code != 503:
                raise RuntimeError(f"llama-server /health returned HTTP {exc.code}: {exc.reason}") from exc
            last_check = "HTTP 503: model still loading"
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
            last_check = f"{type(exc).__name__}: {exc}"

        if time.monotonic() >= next_report:
            print(f"  /health not ready: {last_check}", flush=True)
            next_report = time.monotonic() + 10
        time.sleep(0.5)
    raise RuntimeError(
        f"llama-server did not respond ready after {LLAMA_STARTUP_TIMEOUT}s; "
        f"last check: {last_check}. "
        f"Try: curl.exe --noproxy \"*\" {health_url}"
    )

def stop_llama_server(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    print("Stopping the llama-server started by this script...", flush=True)
    process.terminate()
    try:
        process.wait(timeout=8)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def sanitize(text: str) -> str:
    # Prevent chat messages and glossary terms from spoofing structural PFML3 tokens.
    for token in TOKENS:
        text = text.replace(token, token.replace("<|", "< |"))
    return text


def load_matching_glossary(text: str) -> list[dict]:
    """Return the longest non-overlapping glossary matches, once per source term.

    A shorter term is suppressed only where its occurrence overlaps a selected
    longer term. The same short term can still be included when it appears
    independently elsewhere in the input text.
    """
    if not GLOSSARY_PATH.exists():
        return []
    with GLOSSARY_PATH.open("r", encoding="utf-8-sig") as f:
        items = json.load(f)
    if not isinstance(items, list):
        raise ValueError("glossary.json must be an array of {source, target} objects")

    # Collect positions, not merely matching terms: 'ひなの' within '橘ひなの'
    # must not be sent separately, unless 'ひなの' also occurs on its own.
    # (negative length, start, glossary order, end, source, target)
    matches = []
    for order, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        source, target = item.get("source"), item.get("target")
        if not (isinstance(source, str) and source and isinstance(target, str) and target):
            continue
        start = text.find(source)
        while start != -1:
            matches.append((-len(source), start, order, start + len(source), source, target))
            start = text.find(source, start + 1)

    # Prefer longer matches globally; for equal lengths, prefer the earlier
    # occurrence and then the earlier glossary entry.
    matches.sort()
    occupied = bytearray(len(text))
    selected = {}  # source -> (first accepted position, glossary order, target)
    for _, start, order, end, source, target in matches:
        if any(occupied[start:end]):
            continue
        occupied[start:end] = b"\x01" * (end - start)
        if source not in selected:
            selected[source] = (start, order, target)

    # Send each selected term once, in source-text order.
    return [
        {"source": source, "target": target}
        for source, (start, order, target) in sorted(
            selected.items(), key=lambda pair: (pair[1][0], pair[1][1])
        )
    ]


def make_prompt(text: str, context: str) -> str:
    prompt = "<|plamo:tag|>dataset<|plamo:msg|>translation"
    if context:
        prompt += "<|plamo:tag|>context<|plamo:msg|>" + sanitize(context)
    terms = load_matching_glossary(text)
    if terms:
        prompt += "<|plamo:tag|>glossary"
        for item in terms:
            prompt += "<|plamo:index|>" + sanitize(item["source"])
            prompt += "<|plamo:item|>" + sanitize(item["target"])
    prompt += "<|plamo:tag|>input"
    # Omit the input language for automatic source-language detection.
    prompt += "<|plamo:msg|>" + sanitize(text)
    prompt += "<|plamo:tag|>output<|plamo:key|>lang<|plamo:val|>" + TARGET_LANG
    prompt += "<|plamo:msg|>"
    return prompt


def translate(text: str, context: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": make_prompt(text, context),
        "stop": ["<|plamo:tag|>", "<|plamo:bos|>"],
        "stream": False,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        BACKEND_URL, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with LOCAL_HTTP.open(req, timeout=60) as response:
        result = json.load(response)
        print("Token usage:", result.get("usage"))
    translated = result["choices"][0]["text"].strip()

    if not translated:
        print(f"[EMPTY] {text!r}", flush=True)
    elif translated == text:
        print(f"[UNCHANGED] {text!r}", flush=True)
    else:
        print(f"[TRANSLATED] {text!r} -> {translated!r}", flush=True)

    return translated or text


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self) -> None:
        if urllib.parse.urlsplit(self.path).path == "/translate" and not ENABLE_FLUSHER:
            self.send_json(404, {"error": "Not found"})
            return
        self.send_json(200, {})

    def do_GET(self) -> None:
        parts = urllib.parse.urlsplit(self.path)
        if parts.path not in ("/translate", "/translate-X") or (
            parts.path == "/translate" and not ENABLE_FLUSHER
        ):
            self.send_json(404, {"error": "Not found"})
            return
        context = CONTEXT if parts.path == "/translate" else AUTO_CONTEXT
        query = urllib.parse.parse_qs(parts.query, keep_blank_values=True)
        text = query.get("q", [""])[0]
        if not text or len(text) > 5000:
            self.send_json(400, {"error": "q must contain 1-5000 characters"})
            return
        # Both endpoints use automatic source detection and a fixed target; ignore sl/tl.
        try:
            translated = translate(text, context)
            # "auto" denotes the requested mode, not a detected ISO language code.
            self.send_json(200, {"sentences": [{"trans": translated}], "src": "auto"})
        except Exception as exc:
            print(f"Translation failed: {exc}")
            self.send_json(502, {"error": str(exc)})


if __name__ == "__main__":
    process = None
    server = None
    try:
        # Bind adapter port first: if occupied, do not launch a stray model process.
        server = ThreadingHTTPServer((HOST, PORT), Handler)
        server.daemon_threads = True
        process = start_llama_server()
        wait_for_llama_server(process)
        if ENABLE_FLUSHER:
            print(f"Auto (Flusher) -> {TARGET_LANG}: http://{HOST}:{PORT}/translate?q=$q")
        else:
            print("Flusher endpoint (/translate) is disabled.")
        print(f"Auto (X posts) -> {TARGET_LANG}: http://{HOST}:{PORT}/translate-X?q=$q")
        print(f"Backend: {BACKEND_URL}  model={MODEL}")
        print("Request sl/tl parameters are ignored by both endpoints.")
        print(f"Glossary file: {GLOSSARY_PATH}")
        print("Press Ctrl+C to stop both services.", flush=True)
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except (OSError, RuntimeError) as exc:
        print(f"Startup/runtime error: {exc}", flush=True)
        raise SystemExit(1) from exc
    finally:
        if server is not None:
            server.server_close()
        if process is not None:
            stop_llama_server(process)