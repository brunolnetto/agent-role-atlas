# Agent Role Atlas

> **A Markdown-first framework for modeling professional roles and generating practical organizational artifacts**

[![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-brightgreen)](#status)
[![Roles](https://img.shields.io/badge/Roles-8%20Documented-blue)](#roles)
[![Artifacts](https://img.shields.io/badge/Artifacts-24%20Generated-orange)](#artifacts)
[![Validation](https://img.shields.io/badge/Validation-100%25%20Success-success)](#validation)

## 🎯 What is Agent Role Atlas?

The Agent Role Atlas transforms structured role profiles into actionable organizational deliverables. Instead of maintaining static job descriptions, this system creates living documentation that generates practical artifacts like onboarding checklists, career development ladders, and team formation guides.

### Key Benefits
- **🚀 Automated Artifact Generation** - Transform role profiles into practical deliverables
- **📋 Standardized Onboarding** - Consistent new hire experience across all roles  
- **📈 Clear Career Paths** - Transparent progression expectations and milestones
- **🔗 Role Interaction Mapping** - Visualize team dependencies and collaboration patterns
- **✅ Schema Validation** - Prevent documentation drift and ensure consistency

## 🏃‍♂️ Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/agent-role-atlas.git
cd agent-role-atlas

# Generate all artifacts
cd crew-blueprint
python3 generate_artifacts.py all

# Validate role profiles
python3 validate_profiles.py

# View generated artifacts
ls generated/
```

## 📊 Current Status

### ✅ Phase 1 Complete (Production Ready)

| Component | Status | Count | Success Rate |
|-----------|--------|-------|--------------|
| **Role Profiles** | ✅ Complete | 8 roles | 100% valid |
| **Generated Artifacts** | ✅ Complete | 24 artifacts | 100% success |
| **Schema Validation** | ✅ Complete | All profiles | 0 errors |
| **CLI Tools** | ✅ Complete | 4 utilities | 100% functional |

### 🎯 Documented Roles

- **Backend Engineer** (Senior) - API development and system reliability
- **Data Analyst** (Mid) - Business intelligence and reporting
- **Data Engineer** (Senior) - Data pipeline design and implementation  
- **Frontend Engineer** (Senior) - User interface development
- **Platform Engineer** (Senior) - Infrastructure and developer experience
- **Product Manager** (Senior) - Product strategy and execution
- **QA Engineer** (Mid) - Quality assurance and testing
- **UX Designer** (Mid) - User experience and design systems

## 🏗 Architecture

```
agent-role-atlas/
├── crew-blueprint/             # Core system
│   ├── roles/                 # Role profiles (8 profiles)
│   ├── generators/            # Python generation framework
│   ├── templates/             # Jinja2 templates
│   ├── generated/             # Output artifacts (24 files)
│   └── schemas/               # JSON Schema validation
├── docs/                      # Technical documentation
└── .github/                   # GitHub configuration
```

### Generated Artifacts

The system automatically produces:
- **Onboarding Checklists** (8) - Role-specific new hire guidance
- **Career Development Ladders** (16) - Progression paths with milestones
- **Agent Professional Profiles** (8+) - Comprehensive AI agent context
- **Team Interaction Maps** - Visual collaboration patterns
- **Artifact Index** - Organized catalog with metadata

## 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **[docs/README.md](docs/README.md)** | Detailed technical overview | Developers & System Admins |
| **[docs/ontology.md](docs/ontology.md)** | Data model and database schema | Data Architects |
| **[docs/structure.md](docs/structure.md)** | File format specifications | Content Authors |
| **[docs/CREW_MAP.md](docs/CREW_MAP.md)** | Visual role interaction diagram | Team Leads |

## 🛠 Usage Examples

### Generate Onboarding Checklist
```bash
python3 generate_artifacts.py onboarding backend-engineer
```

### Create Career Development Plan
```bash
python3 generate_artifacts.py career data-engineer senior
```

### Generate AI Agent Profile
```bash
python3 generate_artifacts.py agent --role=backend-engineer
python3 generate_artifacts.py agent --role=data-engineer --agent-name="DataFlow Agent" --specialization="Real-time Processing"
```

### Generate All Agent Profiles
```bash
python3 generate_artifacts.py all-agents
```

### Validate All Profiles
```bash
python3 validate_profiles.py
```

### Generate Team Interaction Map
```bash
python3 generate_crew_map.py
```

## 🚀 Phase 2 Roadmap

### Immediate Priorities
- **Team Formation Advisor** - Generate optimal team compositions
- **Runbook Generator** - Incident response procedures by role
- **Interview Guide Generator** - Role-specific assessment materials

### Expansion Plans
- **Additional Roles** - DevOps, Security, ML Engineer, Engineering Manager
- **Web Interface** - Browser-based artifact generation and exploration
- **API Layer** - Programmatic access for HRIS and workflow integration
- **AI Features** - Smart role recommendations and career path optimization

## 🤝 Contributing

1. **Add New Roles** - Follow the format in `docs/structure.md`
2. **Create Generators** - Extend the framework in `crew-blueprint/generators/`
3. **Improve Templates** - Enhance output quality in `crew-blueprint/templates/`
4. **Validate Changes** - Always run `validate_profiles.py` before committing

## 🎯 Use Cases

### For Engineering Teams
- **Hiring** - Clear role definitions and interview guides
- **Onboarding** - Structured new hire checklists and milestones
- **Career Development** - Transparent progression paths and expectations
- **Team Formation** - Optimal role combinations for projects

### For AI Agent Development
- **Agent Context** - Comprehensive professional profiles for AI agents
- **Role Boundaries** - Clear scope definition and operational guidelines
- **Decision Frameworks** - Structured approaches to role-specific decisions
- **Collaboration Protocols** - How agents should interact with teams

### For Organizations
- **Role Standardization** - Consistent definitions across departments
- **Process Automation** - Generate documentation instead of writing manually
- **Talent Planning** - Understand skill gaps and development needs
- **Knowledge Management** - Centralized, version-controlled role documentation

## 📈 Success Metrics

The system demonstrates value through:
- **Consistency** - All artifacts follow established quality standards
- **Scalability** - Adding roles/artifacts requires minimal effort
- **Automation** - Bulk generation replaces manual documentation processes
- **Quality** - Schema validation prevents errors and documentation drift

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙋‍♀️ Support

- **Issues** - Report bugs and request features via GitHub Issues
- **Discussions** - Ask questions and share ideas via GitHub Discussions  
- **Documentation** - Comprehensive guides in the `/docs` folder

---

*Transform your role documentation from static descriptions into dynamic organizational intelligence.*
