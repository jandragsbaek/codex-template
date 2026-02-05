#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def parse_iso(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def parse_ts(obj: dict) -> datetime | None:
    ts = obj.get("timestamp")
    dt = parse_iso(ts) if isinstance(ts, str) else None
    if dt:
        return dt
    payload = obj.get("payload") or {}
    if isinstance(payload, dict):
        ts = payload.get("timestamp")
        dt = parse_iso(ts) if isinstance(ts, str) else None
        if dt:
            return dt
    if "ts" in obj:
        try:
            return datetime.fromtimestamp(float(obj["ts"]), tz=timezone.utc)
        except Exception:
            return None
    return None


def extract_text(payload: dict) -> str:
    content = payload.get("content")
    if isinstance(content, list):
        parts = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if "text" in item and isinstance(item["text"], str):
                parts.append(item["text"])
                continue
            if "input_text" in item and isinstance(item["input_text"], str):
                parts.append(item["input_text"])
                continue
            if "output_text" in item and isinstance(item["output_text"], str):
                parts.append(item["output_text"])
        return "\n".join(p for p in parts if p).strip()
    if isinstance(content, str):
        return content.strip()
    return ""


def iter_session_messages(path: Path):
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("type") != "response_item":
                continue
            payload = obj.get("payload") or {}
            if payload.get("type") != "message":
                continue
            role = payload.get("role")
            if role not in {"user", "assistant"}:
                continue
            text = extract_text(payload)
            if not text:
                continue
            ts = parse_ts(obj)
            yield ts, role, text


def iter_history_messages(path: Path):
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            text = obj.get("text")
            if not isinstance(text, str) or not text.strip():
                continue
            ts = parse_ts(obj)
            if not ts:
                continue
            yield ts, "user", text.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", "~/.codex"))
    parser.add_argument("--since-hours", type=float, default=24.0)
    parser.add_argument("--out", default="")
    parser.add_argument("--include-history", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    codex_home = Path(os.path.expanduser(args.codex_home)).resolve()
    sessions_root = codex_home / "sessions"
    history_path = codex_home / "history.jsonl"

    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.since_hours)
    items: list[tuple[datetime, str, str]] = []

    if sessions_root.exists():
        for path in sessions_root.rglob("rollout-*.jsonl"):
            try:
                if datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc) < cutoff:
                    continue
            except Exception:
                pass
            try:
                for ts, role, text in iter_session_messages(path):
                    if ts and ts >= cutoff:
                        items.append((ts, role, text))
            except Exception:
                continue

    if args.include_history and history_path.exists():
        try:
            for ts, role, text in iter_history_messages(history_path):
                if ts and ts >= cutoff:
                    items.append((ts, role, text))
        except Exception:
            pass

    items.sort(key=lambda x: x[0])

    lines = []
    for ts, role, text in items:
        lines.append(f"[{ts.isoformat()}] {role}: {text}")
        if args.limit and len(lines) >= args.limit:
            break

    output = "\n".join(lines) + ("\n" if lines else "")
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
