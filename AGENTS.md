# Engineering delegation

Handle routine client work directly, including the relevant tests and documentation. When a task needs specialist judgment, start with one named profile. Give it the desired outcome, relevant paths or diff, constraints, and an acceptance check. Use the profile's configured model and effort.

Use the architect to resolve design choices and the planner to sequence agreed work. Assign implementation to the backend, frontend, database, DevOps, or performance engineer according to the affected code. Use the researcher for unresolved technical questions.

Add a second specialist when there is a distinct question or an independent review that could change the release decision. Parallelize independent work when it saves time. Give each implementer distinct file ownership and sequence changes that depend on a shared contract.

For a consequential change, choose the review that matches the failure mode. Give the code-reviewer the actual diff for a compatibility change, use QA for a workflow with meaningful regression risk, and include the security-auditor for changes to authorization or tenant isolation. For a migration that could lose client data, have the database-engineer check recovery before rollout. Address material findings and report any unverified checks.

Use the technical-writer when behavior changes affect readers. Ask the wiki-curator to record validated, durable decisions in the project's existing wiki. The lead owns integration and reports the final outcome.
