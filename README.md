# Engineering agents for Claude Code and Codex CLI

Both CLIs have the same 13 project-scoped specialists. Start a new session from this directory and trust the project when prompted. For example, ask “Use the database-engineer to review the proposed migration for compatibility with the previous application version.” For an independent review, give the code-reviewer the diff and the behavior the change must preserve.

## Model assignments

| Role | Claude Code model · effort | Codex CLI model · effort |
| --- | --- | --- |
| `architect` | `opus` · high | `gpt-6.2-astra` · high |
| `planner` | `sonnet` · medium | `gpt-6.2-sol` · medium |
| `backend-engineer` | `sonnet` · medium | `gpt-6.2-sol` · medium |
| `frontend-engineer` | `sonnet` · medium | `gpt-6.2-sol` · medium |
| `database-engineer` | `sonnet` · high | `gpt-6.2-sol` · high |
| `security-auditor` | `opus` · high | `gpt-6.2-astra` · high |
| `code-reviewer` | `sonnet` · high | `gpt-6.2-sol` · high |
| `qa-engineer` | `sonnet` · medium | `gpt-6.2-sol` · medium |
| `devops-engineer` | `sonnet` · medium | `gpt-6.2-sol` · medium |
| `performance-engineer` | `sonnet` · high | `gpt-6.2-sol` · high |
| `researcher` | `sonnet` · medium | `gpt-6.2-sol` · medium |
| `technical-writer` | `sonnet` · medium | `gpt-6.1-terra` · medium |
| `wiki-curator` | `haiku` · low | `gpt-6-luna` · high |

These defaults suit a contractor supporting several small and medium-sized clients. Sonnet and Sol at medium effort cover routine delivery. Independent code review, database changes and performance diagnosis get high effort on those same models. Reserve Opus and Astra at high effort for consequential design decisions and security reviews, such as changing tenant isolation. The technical writer uses Terra on Codex. Wiki maintenance uses Haiku at low effort or Luna at its recommended high starting effort. [Claude Code model configuration](https://code.claude.com/docs/en/model-config) · [Codex models](https://learn.chatgpt.com/docs/models)

The model families were checked on 2026-11-25. Claude resolves family aliases according to the provider and account settings. Codex uses model identifiers from the signed-in CLI catalog. The earlier live delegation checks covered GPT-6.2 Sol at medium and high, GPT-6.2 Astra at high, and GPT-6 Luna at high. Those checks preceded this role reassignment.

## Source and generated profiles

- `engineering/agents/*.md` defines when each role is useful, its work and its expected handoff. The first paragraph becomes the native routing description.
- `engineering/model-mappings.toml` assigns models, effort and Claude tool groups. The generator uses Python 3.11+ and its standard library.
- `.claude/agents/*.md` and `.codex/agents/*.toml` are the generated native profiles. Each file contains the complete prompt and can be deployed independently.
- `AGENTS.md` defines routing and delegation for the lead. Claude loads the same guidance through `CLAUDE.md`.

After changing a role or its mapping, regenerate the profiles and check for drift.

```sh
python3 scripts/generate_agents.py
python3 scripts/generate_agents.py --check
```

## Use on separate VMs

For a project installation, copy the chosen provider’s dot-directory to the target repository root. Include `AGENTS.md` for Codex. Include both `CLAUDE.md` and `AGENTS.md` for Claude, preserving their relative locations. Merge guidance and settings with existing files when installing into an established repository.

For a user-wide installation, copy the individual generated profiles into `~/.claude/agents/` on the Claude VM and `~/.codex/agents/` on the Codex VM. Merge the delegation guidance into the corresponding user-level `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`. To apply the project's concurrency limit globally, merge its `[agents]` settings into the VM's Codex configuration. Start a fresh session after installation. [Claude Code subagent scopes](https://code.claude.com/docs/en/sub-agents) · [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Claude's inspection profiles have read/search tools, the researcher adds web access, and only implementation roles have shell access. Codex agents inherit the parent session's permissions. For enforced read-only Codex reviews, start the review in a read-only parent session. [Claude Code subagent tools](https://code.claude.com/docs/en/sub-agents) · [Codex custom agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents)
