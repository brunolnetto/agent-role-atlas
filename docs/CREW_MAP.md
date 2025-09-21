# Crew Interaction Map

This diagram shows the interactions between roles based on their profile definitions.

```mermaid
flowchart TD
  %% externals first (ids must be used in edges)
  ext_executive_stakeholders["Executive stakeholders"]:::external
  ext_security_engineer["Security Engineer"]:::external

  %% roles
  backend_engineer["Backend Engineer"]
  data_analyst["Data Analyst"]
  data_engineer["Data Engineer"]
  frontend_engineer["Frontend Engineer"]
  platform_engineer["Platform Engineer"]
  product_manager["Product Manager"]
  qa_engineer["QA Engineer"]
  ux_designer["UX Designer"]

  %% solid relationships
  backend_engineer --> frontend_engineer
  backend_engineer --> data_engineer
  backend_engineer --> platform_engineer
  backend_engineer --> qa_engineer

  data_analyst --> data_engineer
  data_analyst --> product_manager
  data_analyst --> backend_engineer
  data_analyst --> ext_executive_stakeholders

  data_engineer --> data_analyst
  data_engineer --> backend_engineer
  data_engineer --> platform_engineer
  data_engineer --> product_manager

  frontend_engineer --> ux_designer
  frontend_engineer --> backend_engineer
  frontend_engineer --> product_manager
  frontend_engineer --> qa_engineer

  platform_engineer --> data_engineer
  platform_engineer --> backend_engineer
  platform_engineer --> frontend_engineer
  platform_engineer --> ext_security_engineer

  product_manager --> data_engineer
  product_manager --> frontend_engineer
  product_manager --> ux_designer
  product_manager --> backend_engineer

  qa_engineer --> frontend_engineer
  qa_engineer --> backend_engineer
  qa_engineer --> ux_designer
  qa_engineer --> product_manager

  ux_designer --> frontend_engineer
  ux_designer --> product_manager
  ux_designer --> backend_engineer
  ux_designer --> qa_engineer

  %% dashed annotated relationships (labels kept punctuation-free)
  backend_engineer -.->|Provides API daily| frontend_engineer
  backend_engineer -.->|Collaborates weekly| data_engineer
  backend_engineer -.->|Depends on demand| platform_engineer
  backend_engineer -.->|Collaborates daily| qa_engineer

  data_analyst -.->|Receives dataset daily| data_engineer
  data_analyst -.->|Provides insights weekly| product_manager
  data_analyst -.->|Collaborates monthly| backend_engineer
  data_analyst -.->|Provides analysis monthly| ext_executive_stakeholders

  data_engineer -.->|Delivers dataset daily| data_analyst
  data_engineer -.->|Collaborates weekly| backend_engineer
  data_engineer -.->|Depends on demand| platform_engineer
  data_engineer -.->|Advises monthly| product_manager

  frontend_engineer -.->|Collaborates daily| ux_designer
  frontend_engineer -.->|Depends daily on backend| backend_engineer
  frontend_engineer -.->|Delivers UI per sprint| product_manager
  frontend_engineer -.->|Collaborates daily| qa_engineer

  platform_engineer -.->|Provides infra on demand| data_engineer
  platform_engineer -.->|Provides infra on demand| backend_engineer
  platform_engineer -.->|Provides infra on demand| frontend_engineer
  platform_engineer -.->|Collaborates weekly| ext_security_engineer

  product_manager -.->|Receives insights monthly| data_engineer
  product_manager -.->|Receives deliverables per sprint| frontend_engineer
  product_manager -.->|Collaborates daily| ux_designer
  product_manager -.->|Provides requirements weekly| backend_engineer

  qa_engineer -.->|Validates daily| frontend_engineer
  qa_engineer -.->|Validates daily| backend_engineer
  qa_engineer -.->|Collaborates weekly| ux_designer
  qa_engineer -.->|Reports weekly| product_manager

  ux_designer -.->|Collaborates daily| frontend_engineer
  ux_designer -.->|Collaborates daily| product_manager
  ux_designer -.->|Provides designs weekly| backend_engineer
  ux_designer -.->|Collaborates weekly| qa_engineer

  classDef external fill:#f9f9f9,stroke:#999,stroke-dasharray:5 5;
```

## Legend

- **Solid arrows**: Direct interactions
- **Dotted arrows**: Interaction details (type and frequency)
- **Dashed boxes**: External roles (not yet defined in this catalog)

---
*Generated automatically from role profiles*
