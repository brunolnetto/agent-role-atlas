# {{ role.name }} Onboarding Checklist
{{ "- " + seniority + " Level -" if seniority else "" }}

*Generated for: {{ role.name }} ({{ role.default_seniority }})*  
*Generated on: {{ generation_date }}*

## Overview

Welcome to your role as a **{{ role.name }}**! This checklist will guide you through your first 90 days and help you become effective in your new position.

**Mission**: {{ role.mission }}

**What you'll be doing**: {{ role.short_description }}

## 30-Day Goals (Foundation)

### Week 1: Orientation & Setup
{% for item in week_1_tasks %}
- [ ] {{ item }}
{% endfor %}

### Week 2-4: Core Understanding
{% for item in foundation_tasks %}
- [ ] {{ item }}
{% endfor %}

## 60-Day Goals (Integration)

### Learning & Development
{% for capability in learning_priorities %}
- [ ] **{{ capability.name }}**: {{ capability.development_plan }}
{% endfor %}

### Relationship Building
{% for interaction in key_relationships %}
- [ ] **{{ interaction.type }}** with {{ interaction.target_role }}
  - Meet within: {{ interaction.timeline }}
  - Focus: {{ interaction.focus_areas }}
  - Frequency going forward: {{ interaction.frequency }}
{% endfor %}

### Initial Responsibilities
{% for resp in starter_responsibilities %}
- [ ] **{{ resp.title }}**
  - Shadow current owner for {{ resp.shadow_period }}
  - Take on {{ resp.initial_scope }}
  - Success metrics: {{ resp.success_metrics }}
{% endfor %}

## 90-Day Goals (Ownership)

### Full Responsibility Ownership
{% for resp in role.responsibilities %}
- [ ] **{{ resp.title }}** {% if resp.is_primary %}*(Primary)*{% endif %}
  - Expected proficiency: {{ get_expected_proficiency(resp, seniority) }}
  - Success criteria: {{ resp.success_metrics }}
  - Review with manager: Week {{ get_review_week(resp) }}
{% endfor %}

### Capability Development
{% for capability in role.capabilities %}
- [ ] **{{ capability.name }}** - Target: {{ get_target_proficiency(capability, seniority) }}
  - Current assessment: ___________
  - Development plan: {{ get_development_plan(capability, seniority) }}
  - Resources: {{ get_capability_resources(capability) }}
{% endfor %}

### Artifact Ownership
{% for artifact in role.artifacts %}
- [ ] **{{ artifact.name }}** ({{ artifact.type }})
  - Understand current state and ownership
  - Identify improvement opportunities
  - Document any issues or gaps
{% endfor %}

## Success Metrics & Check-ins

### 30-Day Review
- [ ] Complete technical setup and access provisioning
- [ ] Understand team structure and key relationships
- [ ] Familiar with all primary responsibilities
- [ ] Initial capability assessment completed

### 60-Day Review  
- [ ] Contributing to {{ get_contribution_areas(role, seniority) }}
- [ ] Established working relationships with key collaborators
- [ ] Demonstrated learning in core capabilities
- [ ] Identified areas for continued development

### 90-Day Review
- [ ] Full ownership of appropriate responsibilities
- [ ] Meeting success metrics for primary responsibilities
- [ ] Effective collaboration patterns established
- [ ] Clear development plan for next 6 months

## Resources & References

### Technical Resources
{% for tech in role.properties.get('preferred_tech', '').split(', ') if role.properties.get('preferred_tech') %}
- **{{ tech }}**: [Add resource links during onboarding]
{% endfor %}

### Internal Contacts
{% for interaction in role.interactions %}
- **{{ interaction.target_role }}**: {{ interaction.notes }}
{% endfor %}

### Documentation
- Role profile: [Link to profile.md]
- Team documentation: [Add during onboarding]
- Process documentation: [Add during onboarding]

## Notes & Feedback

*Use this space to track progress, questions, and feedback throughout your onboarding process.*

### Week 1 Notes
_Date: _______ Reviewer: _________________

### Week 4 Review
_Date: _______ Reviewer: _________________

### Week 8 Review  
_Date: _______ Reviewer: _________________

### Week 12 Review
_Date: _______ Reviewer: _________________

---
*This checklist was generated from the {{ role.name }} role profile. Customize as needed for your specific context and team.*
