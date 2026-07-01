"""Smoke-test NVIDIA NIM models and save responses to a markdown report."""

import time
import threading
from datetime import datetime, timezone
from pathlib import Path

import tomllib
from openai import OpenAI

REQUEST_TIMEOUT_SECONDS = 60

# Correct NVIDIA NIM IDs (see https://integrate.api.nvidia.com/v1/models):
# - GLM: z-ai/glm-5.1 (not zhipuai/glm-5.1)
# - DeepSeek: deepseek-ai/deepseek-v4-flash (not deepseek/deepseek-v4-flash)
MODELS = [
    "minimaxai/minimax-m3",
    "qwen/qwen3.5-397b-a17b",
    "moonshotai/kimi-k2.6",
    "z-ai/glm-5.1",
    "deepseek-ai/deepseek-v4-flash",
    # Previous models from app.py
    "deepseek-ai/deepseek-v4-pro",
    "meta/llama-3.1-70b-instruct",
    # moonshotai/kimi-k2.5 — removed: returns 404 on NVIDIA NIM (use kimi-k2.6)
]

PROMPT = (
    "You are a witty historian aboard a Mars colony in 2087. "
    "In exactly two sentences, explain why the first lunar coffee shop "
    "failed — and name one surprising item still on its menu today."
)

OUTPUT_FILE = Path(__file__).parent / "model_test_results.md"


def load_api_key() -> str:
    secrets_path = Path(__file__).parent / ".streamlit" / "secrets.toml"
    with secrets_path.open("rb") as f:
        secrets = tomllib.load(f)
    return secrets["NVIDIA_API_KEY"]


def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    remaining = seconds % 60
    return f"{minutes}m {remaining:.1f}s"


def test_model(client: OpenAI, model: str) -> dict:
    started = time.perf_counter()
    result: dict = {}
    error: dict = {}

    def call_api() -> None:
        try:
            result["response"] = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": PROMPT}],
                max_tokens=256,
                stream=False,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except Exception as exc:
            error["exc"] = exc

    thread = threading.Thread(target=call_api, daemon=True)
    thread.start()
    thread.join(timeout=REQUEST_TIMEOUT_SECONDS)

    if thread.is_alive():
        elapsed = time.perf_counter() - started
        return {
            "model": model,
            "ok": False,
            "response": None,
            "error": f"Request exceeded {REQUEST_TIMEOUT_SECONDS}s timeout",
            "elapsed_seconds": elapsed,
            "timed_out": True,
        }

    elapsed = time.perf_counter() - started

    if "response" in result:
        content = result["response"].choices[0].message.content or ""
        return {
            "model": model,
            "ok": True,
            "response": content.strip(),
            "error": None,
            "elapsed_seconds": elapsed,
            "timed_out": False,
        }

    exc = error.get("exc", Exception("Unknown error"))
    error_text = str(exc)
    return {
        "model": model,
        "ok": False,
        "response": None,
        "error": error_text,
        "elapsed_seconds": elapsed,
        "timed_out": "timed out" in error_text.lower(),
    }


def write_markdown_report(results: list[dict], output_path: Path, total_elapsed: float) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    passed = sum(1 for r in results if r["ok"])

    lines = [
        "# NVIDIA NIM Model Test Results",
        "",
        f"- **Endpoint:** `https://integrate.api.nvidia.com/v1`",
        f"- **Run at:** {timestamp}",
        f"- **Timeout:** {REQUEST_TIMEOUT_SECONDS}s per model",
        f"- **Total duration:** {format_duration(total_elapsed)}",
        f"- **Result:** {passed}/{len(results)} models responded successfully",
        "",
        "## Prompt",
        "",
        PROMPT,
        "",
        "## Timing Summary",
        "",
        "| Model | Status | Duration |",
        "| --- | --- | --- |",
    ]

    for result in results:
        status = "OK" if result["ok"] else ("TIMEOUT" if result["timed_out"] else "FAIL")
        lines.append(
            f"| `{result['model']}` | {status} | {format_duration(result['elapsed_seconds'])} |"
        )

    lines.extend(["", "## Responses", ""])

    for result in results:
        status = "OK" if result["ok"] else ("TIMEOUT" if result["timed_out"] else "FAIL")
        lines.extend(
            [
                f"### {result['model']} — {status}",
                "",
                f"**Duration:** {format_duration(result['elapsed_seconds'])}",
                "",
            ]
        )
        if result["ok"]:
            lines.extend([result["response"], ""])
        else:
            lines.extend(
                [
                    "**Error:**",
                    "",
                    "```",
                    result["error"],
                    "```",
                    "",
                ]
            )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def safe_print(text: str) -> None:
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"), flush=True)


def main() -> None:
    api_key = load_api_key()
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    safe_print(f"Prompt: {PROMPT}\n")
    safe_print(f"Timeout: {REQUEST_TIMEOUT_SECONDS}s per model\n")
    safe_print("=" * 72)

    run_started = time.perf_counter()
    results = []
    for model in MODELS:
        result = test_model(client, model)
        results.append(result)
        status = "OK" if result["ok"] else ("TIMEOUT" if result["timed_out"] else "FAIL")
        duration = format_duration(result["elapsed_seconds"])
        safe_print(f"[{status}] {model} ({duration})")
        if result["ok"]:
            preview = result["response"].replace("\n", " ")
            if len(preview) > 120:
                preview = preview[:117] + "..."
            safe_print(f"       {preview}\n")
        else:
            safe_print(f"       {result['error']}\n")

    total_elapsed = time.perf_counter() - run_started
    write_markdown_report(results, OUTPUT_FILE, total_elapsed)

    passed = sum(1 for r in results if r["ok"])
    safe_print("=" * 72)
    safe_print(f"Result: {passed}/{len(MODELS)} models responded successfully")
    safe_print(f"Total duration: {format_duration(total_elapsed)}")
    safe_print(f"Saved responses to: {OUTPUT_FILE}")
    failed = [r["model"] for r in results if not r["ok"]]
    if failed:
        safe_print(f"Failed models: {', '.join(failed)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
