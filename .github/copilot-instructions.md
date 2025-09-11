# Copilot Instructions for agent-role-atlas

## Project Overview
This repo models professional roles, responsibilities, capabilities, artifacts, and interactions for automation and documentation. The architecture is Markdown-first, with structured YAML frontmatter and JSON Schema validation for role profiles.

## Key Patterns & Conventions
- **Canonical Role Profiles**: Each role is defined in `/crew-blueprint/roles/<slug>/profile.md`.
  - Use YAML frontmatter with required keys: `id`, `slug`, `name`, `default_seniority`.
  - Follow fixed Markdown headers: `# Mission`, `# Short Description`, `# Properties`, `# Responsibilities`, `# Capabilities`, `# Artifacts`, `# Interactions`.
  - Example and schema in `structure.md`.
- **Validation**: Always validate frontmatter against the JSON Schema (see `structure.md`). Do not commit invalid profiles.
- **Enrichment**: If a section is too generic, trigger targeted web search and insert citations inline.
- **Artifacts**: Derived files like crew maps (Mermaid diagrams), index, and runbooks are generated from role profiles.
- **Summary Reporting**: Always produce a `SUMMARY.md` with role count, validation results, and unresolved TODOs.

## Developer Workflows
- **Profile Generation Pipeline**:
  1. Take a list of role slugs.
  2. Generate `profile.md` for each under `/roles/<slug>/`.
  3. Validate frontmatter.
  4. Optionally enrich with web search.
  5. Write to repo.
- **Failure Modes & Mitigations**:
  - Enforce fixed header order to prevent Markdown drift.
  - Use measurable verbs in responsibilities to avoid shallow text.
  - Flag duplicate responsibilities across roles in the summary.
  - Require inline links/citations for web-derived content.

## Integration Points
- **Mermaid diagrams**: Use `interactions` sections to auto-generate crew maps.
- **PostgreSQL schema**: See `ontology.md` for database mapping if needed.

## Examples
- See `structure.md` for canonical profile format and JSON Schema.
- See `ontology.md` for entity relationships and DDL.

## Special Notes
- Repo root slug is `crew-blueprint`.
- All automation should be Markdown-first, human-readable, and agent-friendly.

---
For unclear or incomplete sections, ask for feedback to iterate and improve these instructions.
