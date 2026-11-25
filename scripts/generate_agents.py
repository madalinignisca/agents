"""Render native Claude Code and Codex agent profiles from the engineering catalog."""

import argparse
import json
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAUDE_DIR = ROOT / ".claude" / "agents"
CODEX_DIR = ROOT / ".codex" / "agents"
READ_TOOLS = "Read, Grep, Glob"
CLAUDE_TOOLS = {
    "inspect": READ_TOOLS,
    "research": READ_TOOLS + ", WebSearch, WebFetch",
    "build": READ_TOOLS + ", Edit, Write, Bash",
    "docs": READ_TOOLS + ", Edit, Write",
}


def profiles():
    source = ROOT / "engineering"
    mappings = tomllib.loads((source / "model-mappings.toml").read_text(encoding="utf-8"))
    roles = {path.stem: path for path in (source / "agents").glob("*.md")}
    if roles.keys() != mappings.keys():
        raise ValueError(f"Unpaired roles or mappings: {sorted(roles.keys() ^ mappings.keys())}")

    outputs = {}
    for name, path in sorted(roles.items()):
        heading, description, instructions = path.read_text(encoding="utf-8").strip().split("\n\n", 2)
        if heading != f"# {name}" or "\n" in description or not instructions.strip():
            raise ValueError(f"Expected a role heading, a one-line description and instructions in {path}")
        mapping = mappings[name]
        claude_model, claude_effort = mapping["claude"]
        codex_model, codex_effort = mapping["codex"]
        tools = CLAUDE_TOOLS[mapping["tools"]]
        body = f"{description}\n\n{instructions}"
        outputs[CLAUDE_DIR / f"{name}.md"] = (
            f"---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n"
            f"model: {claude_model}\neffort: {claude_effort}\ntools: {tools}\n---\n\n{body}\n"
        )
        # Keep the TOML prompt readable while escaping quotes and literal backslashes.
        escaped_body = "\n".join(
            json.dumps(line, ensure_ascii=False)[1:-1] for line in body.split("\n")
        )
        outputs[CODEX_DIR / f"{name}.toml"] = (
            f'name = "{name}"\ndescription = {json.dumps(description, ensure_ascii=False)}\n'
            f'model = "{codex_model}"\nmodel_reasoning_effort = "{codex_effort}"\n\n'
            f'developer_instructions = """\n{escaped_body}"""\n'
        )
        parsed = tomllib.loads(outputs[CODEX_DIR / f"{name}.toml"])
        if parsed["developer_instructions"] != body:
            raise ValueError(f"Instructions failed to round-trip for {name}")
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale or missing profiles")
    args = parser.parse_args()
    outputs = profiles()
    stale = []
    for path, content in outputs.items():
        if path.exists() and path.read_text(encoding="utf-8") == content:
            continue
        if args.check:
            stale.append(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        for path in stale:
            print(f"Needs regeneration: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    print(f"{len(outputs)} native profiles are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
