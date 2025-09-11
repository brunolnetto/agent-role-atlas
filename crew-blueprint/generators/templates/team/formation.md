# Team Formation Guide: {{ project_name }}
{{ project_type + " Project" if project_type else "Project" }}

*Generated on: {{ generation_date }}*

## Project Overview

**Project Name**: {{ project_name }}  
**Project Type**: {{ project_type }}  
**Duration**: {{ estimated_duration }}  
**Scope**: {{ project_scope }}

{% if project_requirements %}
**Requirements**:
{% for req in project_requirements %}
- {{ req }}
{% endfor %}
{% endif %}

## Recommended Team Composition

### Core Team Members
{% for role in core_team %}
#### {{ role.name }} ({{ role.seniority }})

**Why This Role**: {{ role.justification }}

**Key Responsibilities**:
{% for resp in role.key_responsibilities %}
- {{ resp }}
{% endfor %}

**Success Metrics**: {{ role.success_metrics }}

**Time Commitment**: {{ role.time_commitment }}

---
{% endfor %}

### Supporting Team Members
{% if supporting_team %}
{% for role in supporting_team %}
#### {{ role.name }} ({{ role.seniority }})

**Contribution**: {{ role.contribution }}  
**Time Commitment**: {{ role.time_commitment }}  
**Engagement Model**: {{ role.engagement_model }}

---
{% endfor %}
{% else %}
*No supporting roles identified for this project scope.*
{% endif %}

## Team Size Analysis

**Total Team Size**: {{ team_size.total }}  
**Core Team**: {{ team_size.core }} members  
**Supporting**: {{ team_size.supporting }} members

**Size Rationale**: {{ size_rationale }}

### Team Size Considerations
{% for consideration in team_size_considerations %}
- **{{ consideration.factor }}**: {{ consideration.description }}
{% endfor %}

## Communication Patterns

### Daily Interactions
{% for interaction in daily_interactions %}
- **{{ interaction.from_role }}** ↔ **{{ interaction.to_role }}**: {{ interaction.purpose }}
  - Frequency: {{ interaction.frequency }}
  - Method: {{ interaction.method }}
{% endfor %}

### Weekly Coordination
{% for interaction in weekly_interactions %}
- **{{ interaction.pattern }}**: {{ interaction.description }}
  - Participants: {{ interaction.participants | join(', ') }}
  - Purpose: {{ interaction.purpose }}
{% endfor %}

### Escalation Paths
{% for escalation in escalation_paths %}
- **{{ escalation.issue_type }}**: {{ escalation.from_role }} → {{ escalation.to_role }}
  - Trigger: {{ escalation.trigger }}
  - Timeline: {{ escalation.timeline }}
{% endfor %}

## Skill Coverage Analysis

### Technical Skills
{% for skill in technical_skills %}
#### {{ skill.name }}
- **Coverage**: {{ skill.coverage }}
- **Primary Owner**: {{ skill.primary_owner }}
- **Backup Coverage**: {{ skill.backup_coverage }}
- **Risk Level**: {{ skill.risk_level }}
{% endfor %}

### Capability Gaps
{% if capability_gaps %}
{% for gap in capability_gaps %}
#### {{ gap.capability }}
- **Gap Description**: {{ gap.description }}
- **Impact**: {{ gap.impact }}
- **Mitigation Strategy**: {{ gap.mitigation }}
- **Timeline**: {{ gap.timeline }}
{% endfor %}
{% else %}
*No significant capability gaps identified.*
{% endif %}

## Collaboration Efficiency

### High-Efficiency Partnerships
{% for partnership in high_efficiency_partnerships %}
- **{{ partnership.role_a }}** ↔ **{{ partnership.role_b }}**
  - Synergy: {{ partnership.synergy }}
  - Collaboration Benefits: {{ partnership.benefits }}
  - Optimization Tips: {{ partnership.optimization }}
{% endfor %}

### Potential Friction Points
{% for friction in potential_friction %}
- **{{ friction.between }}**: {{ friction.description }}
  - Root Cause: {{ friction.root_cause }}
  - Mitigation: {{ friction.mitigation }}
  - Monitoring: {{ friction.monitoring }}
{% endfor %}

## Project Phases & Team Evolution

{% for phase in project_phases %}
### Phase {{ loop.index }}: {{ phase.name }}
**Duration**: {{ phase.duration }}  
**Objectives**: {{ phase.objectives }}

**Team Composition**:
{% for role in phase.team_composition %}
- **{{ role.name }}**: {{ role.involvement }}
{% endfor %}

**Key Activities**:
{% for activity in phase.key_activities %}
- {{ activity }}
{% endfor %}

**Success Criteria**: {{ phase.success_criteria }}

---
{% endfor %}

## Resource & Budget Planning

### Personnel Costs
{% for cost in personnel_costs %}
- **{{ cost.role }}** ({{ cost.seniority }}): {{ cost.time_commitment }}
  - Estimated Cost: {{ cost.estimated_cost }}
  - Cost Category: {{ cost.cost_category }}
{% endfor %}

**Total Estimated Personnel Cost**: {{ total_personnel_cost }}

### Additional Resources
{% if additional_resources %}
{% for resource in additional_resources %}
- **{{ resource.type }}**: {{ resource.description }}
  - Cost: {{ resource.cost }}
  - Justification: {{ resource.justification }}
{% endfor %}
{% endif %}

## Success Metrics & KPIs

### Team Performance Metrics
{% for metric in team_metrics %}
- **{{ metric.name }}**: {{ metric.description }}
  - Target: {{ metric.target }}
  - Measurement: {{ metric.measurement }}
  - Review Frequency: {{ metric.review_frequency }}
{% endfor %}

### Project Delivery Metrics
{% for metric in delivery_metrics %}
- **{{ metric.name }}**: {{ metric.description }}
  - Target: {{ metric.target }}
  - Owner: {{ metric.owner }}
{% endfor %}

## Risk Assessment & Mitigation

### Team-Related Risks
{% for risk in team_risks %}
#### {{ risk.risk_type }}: {{ risk.description }}
- **Probability**: {{ risk.probability }}
- **Impact**: {{ risk.impact }}
- **Mitigation Strategy**: {{ risk.mitigation }}
- **Owner**: {{ risk.owner }}
- **Review Date**: {{ risk.review_date }}
{% endfor %}

### Dependency Risks
{% for risk in dependency_risks %}
#### {{ risk.dependency }}: {{ risk.description }}
- **Risk Level**: {{ risk.risk_level }}
- **Mitigation**: {{ risk.mitigation }}
- **Contingency**: {{ risk.contingency }}
{% endfor %}

## Team Formation Recommendations

### Immediate Actions
{% for action in immediate_actions %}
1. **{{ action.title }}**: {{ action.description }}
   - Owner: {{ action.owner }}
   - Deadline: {{ action.deadline }}
   - Success Criteria: {{ action.success_criteria }}
{% endfor %}

### First Week Priorities
{% for priority in first_week_priorities %}
- **{{ priority.category }}**: {{ priority.description }}
  - Activities: {{ priority.activities | join(', ') }}
  - Expected Outcome: {{ priority.expected_outcome }}
{% endfor %}

### 30-Day Team Goals
{% for goal in thirty_day_goals %}
- **{{ goal.title }}**: {{ goal.description }}
  - Success Metrics: {{ goal.success_metrics }}
  - Review Process: {{ goal.review_process }}
{% endfor %}

## Alternative Team Configurations

{% if alternative_configurations %}
{% for config in alternative_configurations %}
### Configuration {{ loop.index }}: {{ config.name }}

**Scenario**: {{ config.scenario }}  
**Trade-offs**: {{ config.tradeoffs }}

**Team Composition**:
{% for role in config.team_composition %}
- {{ role.name }} ({{ role.adjustment }})
{% endfor %}

**Pros**: {{ config.pros | join(', ') }}  
**Cons**: {{ config.cons | join(', ') }}

**Recommendation**: {{ config.recommendation }}

---
{% endfor %}
{% endif %}

## Appendix: Role Interaction Matrix

| From/To | {% for role in core_team %}{{ role.name }} | {% endfor %}
|---------|{% for role in core_team %}:---:|{% endfor %}
{% for from_role in core_team %}| **{{ from_role.name }}** |{% for to_role in core_team %}{% if from_role.name != to_role.name %} {{ get_interaction_frequency(from_role.name, to_role.name) }} |{% else %} - |{% endif %}{% endfor %}
{% endfor %}

**Legend**: 
- D = Daily interaction required
- W = Weekly coordination needed  
- M = Monthly or milestone-based interaction
- R = Rare/as-needed interaction

---

*This team formation guide was generated based on role profiles and project requirements. Customize based on specific organizational context, available personnel, and project constraints.*
