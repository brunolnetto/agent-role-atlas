# {{ role.name }} Career Progression Ladder
{{ from_seniority + " → " + to_seniority if from_seniority != to_seniority else "Development Plan for " + to_seniority }}

*Generated for: {{ role.name }}*  
*Generated on: {{ generation_date }}*

## Current State Analysis
{% if from_seniority != to_seniority %}
**Current Level**: {{ from_seniority }}  
**Target Level**: {{ to_seniority }}  
**Estimated Timeline**: {{ estimated_timeline }}
{% else %}
**Current Level**: {{ to_seniority }}  
**Focus**: Continuous development and excellence
{% endif %}

**Role Mission**: {{ role.mission }}

## Capability Gap Analysis

{% for capability in capability_gaps %}
### {{ capability.name }}

**Current Level**: {{ capability.current_level }}  
**Target Level**: {{ capability.target_level }}  
**Priority**: {{ capability.priority }}

**Development Plan**:
{% for action in capability.development_actions %}
- {{ action }}
{% endfor %}

**Success Indicators**:
{% for indicator in capability.success_indicators %}
- {{ indicator }}
{% endfor %}

**Timeline**: {{ capability.timeline }}

---
{% endfor %}

## Responsibility Evolution

{% for resp_evolution in responsibility_evolution %}
### {{ resp_evolution.title }}

**Current Expectation**: {{ resp_evolution.current_expectation }}  
**Target Expectation**: {{ resp_evolution.target_expectation }}

**Development Areas**:
{% for area in resp_evolution.development_areas %}
- **{{ area.focus }}**: {{ area.description }}
  - Actions: {{ area.actions | join(', ') }}
  - Timeline: {{ area.timeline }}
{% endfor %}

**Success Metrics**: {{ resp_evolution.target_metrics }}

---
{% endfor %}

## Leadership & Impact Development
{% if leadership_development %}

{% for area in leadership_development %}
### {{ area.category }}

**Objective**: {{ area.objective }}

**Key Activities**:
{% for activity in area.activities %}
- {{ activity }}
{% endfor %}

**Measurement**: {{ area.measurement }}

---
{% endfor %}
{% endif %}

## Experience & Project Requirements

### Required Experiences
{% for experience in required_experiences %}
- **{{ experience.category }}**: {{ experience.description }}
  - Specific examples: {{ experience.examples | join(', ') }}
  - Timeline: {{ experience.timeline }}
{% endfor %}

### Recommended Projects
{% for project in recommended_projects %}
- **{{ project.name }}**: {{ project.description }}
  - Skills developed: {{ project.skills | join(', ') }}
  - Scope: {{ project.scope }}
  - Duration: {{ project.duration }}
{% endfor %}

## Mentorship & Learning Plan

### Mentorship Needs
{% for mentorship in mentorship_plan %}
- **{{ mentorship.area }}**: {{ mentorship.description }}
  - Mentor profile: {{ mentorship.mentor_profile }}
  - Frequency: {{ mentorship.frequency }}
  - Duration: {{ mentorship.duration }}
{% endfor %}

### Learning Resources
{% for resource in learning_resources %}
- **{{ resource.category }}**: {{ resource.description }}
  - Type: {{ resource.type }}
  - Priority: {{ resource.priority }}
  - Timeline: {{ resource.timeline }}
{% endfor %}

## Stakeholder & Network Development

### Key Relationships to Build
{% for relationship in key_relationships %}
- **{{ relationship.role }}**: {{ relationship.purpose }}
  - Interaction type: {{ relationship.interaction_type }}
  - Development focus: {{ relationship.development_focus }}
{% endfor %}

### Cross-functional Exposure
{% for exposure in cross_functional_exposure %}
- **{{ exposure.area }}**: {{ exposure.objective }}
  - Activities: {{ exposure.activities | join(', ') }}
  - Timeline: {{ exposure.timeline }}
{% endfor %}

## Milestone & Review Schedule

### 3-Month Milestones
{% for milestone in three_month_milestones %}
- **{{ milestone.title }}**: {{ milestone.description }}
  - Success criteria: {{ milestone.success_criteria }}
  - Review date: {{ milestone.review_date }}
{% endfor %}

### 6-Month Milestones  
{% for milestone in six_month_milestones %}
- **{{ milestone.title }}**: {{ milestone.description }}
  - Success criteria: {{ milestone.success_criteria }}
  - Review date: {{ milestone.review_date }}
{% endfor %}

### Annual Goals
{% for goal in annual_goals %}
- **{{ goal.title }}**: {{ goal.description }}
  - Impact: {{ goal.expected_impact }}
  - Measurement: {{ goal.measurement }}
{% endfor %}

## Promotion Readiness Checklist

### Technical Competencies
{% for competency in technical_readiness %}
- [ ] **{{ competency.name }}**: {{ competency.requirement }}
  - Evidence: {{ competency.evidence_needed }}
{% endfor %}

### Leadership & Influence
{% for leadership in leadership_readiness %}
- [ ] **{{ leadership.area }}**: {{ leadership.requirement }}
  - Examples needed: {{ leadership.examples }}
{% endfor %}

### Business Impact
{% for impact in business_readiness %}
- [ ] **{{ impact.category }}**: {{ impact.requirement }}
  - Measurement: {{ impact.measurement }}
{% endfor %}

### Feedback & Validation
- [ ] **360 Review**: Positive feedback from peers, reports, and stakeholders
- [ ] **Manager Assessment**: Confirmation of readiness from direct manager
- [ ] **Peer Recognition**: Acknowledgment from peers at target level
- [ ] **Stakeholder Validation**: External stakeholder confirmation of value delivery

## Development Tracking

### Monthly Check-ins
Use this section to track progress on development goals:

**Month 1 Progress**:
- [ ] Capability development goals on track
- [ ] Required experiences identified and planned
- [ ] Mentorship relationships established
- [ ] Key projects initiated

**Month 2 Progress**:
- [ ] Demonstrable skill improvements
- [ ] Cross-functional relationships developing
- [ ] Leadership opportunities taken
- [ ] Feedback incorporation visible

**Month 3 Progress**:
- [ ] Measurable impact delivery
- [ ] Stakeholder recognition increasing
- [ ] Technical competency demonstrations
- [ ] Promotion discussion initiated

### Notes & Reflections

*Use this space to track insights, challenges, and adjustments to the development plan.*

---

*This career ladder was generated from the {{ role.name }} role profile. Customize based on individual circumstances, organizational needs, and available opportunities.*
