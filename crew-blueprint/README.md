# Crew Blueprint - Role Atlas

This directory contains structured role profiles for professional roles, responsibilities, capabilities, and interactions.

## Architecture

- **Schema**: [`schema.json`](./schema.json) - JSON Schema for validating role profile frontmatter
- **Validation**: [`validate_profiles.py`](./validate_profiles.py) - Tool for validating role profiles
- **Roles**: [`roles/`](./roles/) - Individual role profile directories

## Current Roles

| Role | Slug | Default Seniority | Status |
|------|------|------------------|---------|
| [Backend Engineer](./roles/backend-engineer/profile.md) | `backend-engineer` | Senior | ✅ Valid |
| [Data Analyst](./roles/data-analyst/profile.md) | `data-analyst` | Mid | ✅ Valid |
| [Data Engineer](./roles/data-engineer/profile.md) | `data-engineer` | Senior | ✅ Valid |
| [Frontend Engineer](./roles/frontend-engineer/profile.md) | `frontend-engineer` | Senior | ✅ Valid |
| [Platform Engineer](./roles/platform-engineer/profile.md) | `platform-engineer` | Senior | ✅ Valid |
| [Product Manager](./roles/product-manager/profile.md) | `product-manager` | Senior | ✅ Valid |
| [QA Engineer](./roles/qa-engineer/profile.md) | `qa-engineer` | Mid | ✅ Valid |
| [UX Designer](./roles/ux-designer/profile.md) | `ux-designer` | Mid | ✅ Valid |

## Role Profile Structure

Each role follows this canonical structure:

```markdown
---
id: role-id
slug: role-slug
name: Role Name
default_seniority: Senior
---

# Mission
[Role's primary purpose and value proposition]

# Short Description
[1-2 sentence summary]

# Properties
[Tech preferences, workstyle, approach]

# Responsibilities
[Key responsibilities with success metrics]

# Capabilities
[Skills and competencies with proficiency levels]

# Artifacts
[Things the role produces or owns]

# Interactions
[How this role interacts with other roles]
```

## Usage

### Validate Profiles
```bash
python3 validate_profiles.py
```

### Validate Specific Role
```bash
python3 validate_profiles.py roles/data-engineer
```

---

*Generated on September 10, 2025*
