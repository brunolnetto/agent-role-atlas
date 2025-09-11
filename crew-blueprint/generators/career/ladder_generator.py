"""
Career ladder generator for role progression planning.
"""

from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta

from ..core import ProfileParser, TemplateEngine, OutputFormatter, RoleProfile, Capability

class CareerLadderGenerator:
    """Generates career progression ladders for roles between seniority levels."""
    
    def __init__(self, roles_dir: Path = None, templates_dir: Path = None, output_dir: Path = None):
        self.parser = ProfileParser(roles_dir)
        
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / 'templates'
        self.template_engine = TemplateEngine(templates_dir)
        
        self.formatter = OutputFormatter(output_dir)
        
        # Define seniority progression paths and expectations
        self.seniority_levels = ['Junior', 'Mid', 'Senior', 'Staff', 'Principal']
        self.level_expectations = {
            'Junior': {
                'scope': 'Well-defined tasks',
                'autonomy': 'Guided execution',
                'impact': 'Individual contributor',
                'leadership': 'Learning from others',
                'timeline': 'Following established patterns'
            },
            'Mid': {
                'scope': 'Feature-level ownership',
                'autonomy': 'Independent execution',
                'impact': 'Team efficiency',
                'leadership': 'Peer collaboration',
                'timeline': '3-6 month initiatives'
            },
            'Senior': {
                'scope': 'System-level ownership',
                'autonomy': 'Strategic execution',
                'impact': 'Cross-team influence',
                'leadership': 'Technical mentorship',
                'timeline': '6-12 month initiatives'
            },
            'Staff': {
                'scope': 'Multi-system architecture',
                'autonomy': 'Initiative creation',
                'impact': 'Organizational standards',
                'leadership': 'Team leadership',
                'timeline': '1-2 year strategic goals'
            },
            'Principal': {
                'scope': 'Organizational architecture',
                'autonomy': 'Vision setting',
                'impact': 'Industry influence',
                'leadership': 'Organizational transformation',
                'timeline': '2+ year transformational initiatives'
            }
        }
        
        # Capability progression mapping
        self.capability_progression = {
            'Novice': {'next': 'Competent', 'focus': 'Basic understanding and guided practice'},
            'Competent': {'next': 'Advanced', 'focus': 'Independent application and problem-solving'},
            'Advanced': {'next': 'Expert', 'focus': 'Complex problem-solving and optimization'},
            'Expert': {'next': 'Master', 'focus': 'Innovation and knowledge creation'},
            'Master': {'next': 'Master', 'focus': 'Industry leadership and standard-setting'}
        }
    
    def generate_ladder(self, role_slug: str, from_seniority: str, to_seniority: str = None) -> str:
        """Generate a career ladder for role progression."""
        
        # Parse role profile
        profile = self.parser.parse_profile(role_slug)
        if not profile:
            raise ValueError(f"Role profile not found: {role_slug}")
        
        # Determine target seniority
        if to_seniority is None:
            to_seniority = self._get_next_seniority(from_seniority)
        
        # Build template context
        context = self._build_ladder_context(profile, from_seniority, to_seniority)
        
        # Render template
        ladder_content = self.template_engine.render_template(
            'career/ladder.md',
            context
        )
        
        return ladder_content
    
    def save_ladder(self, role_slug: str, from_seniority: str, to_seniority: str = None) -> Path:
        """Generate and save a career ladder."""
        
        profile = self.parser.parse_profile(role_slug)
        if not profile:
            raise ValueError(f"Role profile not found: {role_slug}")
        
        if to_seniority is None:
            to_seniority = self._get_next_seniority(from_seniority)
        
        ladder_content = self.generate_ladder(role_slug, from_seniority, to_seniority)
        
        # Generate filename
        if from_seniority == to_seniority:
            filename = self.formatter.get_output_filename(
                'career', role_slug, to_seniority, 'development'
            )
        else:
            filename = self.formatter.get_output_filename(
                'career', role_slug, f"{from_seniority.lower()}-to-{to_seniority.lower()}", 'ladder'
            )
        
        metadata = {
            'artifact_type': 'career_ladder',
            'role': profile.name,
            'from_seniority': from_seniority,
            'to_seniority': to_seniority,
            'source_profile': f'roles/{role_slug}/profile.md'
        }
        
        output_path = self.formatter.save_artifact(
            ladder_content, filename, 'career', metadata
        )
        
        return output_path
    
    def generate_all_ladders(self, include_all_transitions: bool = False) -> Dict[str, Path]:
        """Generate career ladders for all roles."""
        
        generated_files = {}
        all_roles = self.parser.get_all_roles()
        
        for role_slug in all_roles:
            profile = self.parser.parse_profile(role_slug)
            if not profile:
                continue
            
            current_seniority = profile.default_seniority
            
            # Generate progression ladder (current → next level)
            next_seniority = self._get_next_seniority(current_seniority)
            if next_seniority != current_seniority:
                output_path = self.save_ladder(role_slug, current_seniority, next_seniority)
                generated_files[f"{role_slug}_{current_seniority}_to_{next_seniority}"] = output_path
            
            # Generate development plan for current level
            dev_path = self.save_ladder(role_slug, current_seniority, current_seniority)
            generated_files[f"{role_slug}_{current_seniority}_development"] = dev_path
            
            # Generate all transitions if requested
            if include_all_transitions:
                for from_level in self.seniority_levels:
                    for to_level in self.seniority_levels:
                        if self._is_valid_progression(from_level, to_level):
                            try:
                                transition_path = self.save_ladder(role_slug, from_level, to_level)
                                generated_files[f"{role_slug}_{from_level}_to_{to_level}"] = transition_path
                            except Exception:
                                continue  # Skip invalid transitions
        
        return generated_files
    
    def _build_ladder_context(self, profile: RoleProfile, from_seniority: str, to_seniority: str) -> Dict[str, Any]:
        """Build template context for career ladder."""
        
        return {
            'role': profile,
            'from_seniority': from_seniority,
            'to_seniority': to_seniority,
            'generation_date': datetime.now().strftime('%Y-%m-%d'),
            'estimated_timeline': self._get_progression_timeline(from_seniority, to_seniority),
            'capability_gaps': self._analyze_capability_gaps(profile, from_seniority, to_seniority),
            'responsibility_evolution': self._analyze_responsibility_evolution(profile, from_seniority, to_seniority),
            'leadership_development': self._get_leadership_development_plan(from_seniority, to_seniority),
            'required_experiences': self._get_required_experiences(profile, from_seniority, to_seniority),
            'recommended_projects': self._get_recommended_projects(profile, from_seniority, to_seniority),
            'mentorship_plan': self._get_mentorship_plan(profile, from_seniority, to_seniority),
            'learning_resources': self._get_learning_resources(profile, from_seniority, to_seniority),
            'key_relationships': self._get_key_relationships(profile, to_seniority),
            'cross_functional_exposure': self._get_cross_functional_exposure(profile, to_seniority),
            'three_month_milestones': self._get_milestones(profile, from_seniority, to_seniority, 3),
            'six_month_milestones': self._get_milestones(profile, from_seniority, to_seniority, 6),
            'annual_goals': self._get_annual_goals(profile, from_seniority, to_seniority),
            'technical_readiness': self._get_technical_readiness(profile, to_seniority),
            'leadership_readiness': self._get_leadership_readiness(to_seniority),
            'business_readiness': self._get_business_readiness(profile, to_seniority)
        }
    
    def _get_next_seniority(self, current_seniority: str) -> str:
        """Get the next seniority level."""
        try:
            current_index = self.seniority_levels.index(current_seniority)
            if current_index < len(self.seniority_levels) - 1:
                return self.seniority_levels[current_index + 1]
            else:
                return current_seniority  # Already at highest level
        except ValueError:
            return 'Mid'  # Default fallback
    
    def _get_progression_timeline(self, from_seniority: str, to_seniority: str) -> str:
        """Estimate timeline for seniority progression."""
        
        if from_seniority == to_seniority:
            return "Ongoing development"
        
        timelines = {
            ('Junior', 'Mid'): '12-18 months',
            ('Mid', 'Senior'): '18-24 months',
            ('Senior', 'Staff'): '2-3 years',
            ('Staff', 'Principal'): '3-5 years'
        }
        
        return timelines.get((from_seniority, to_seniority), '12-24 months')
    
    def _analyze_capability_gaps(self, profile: RoleProfile, from_seniority: str, to_seniority: str) -> List[Dict[str, Any]]:
        """Analyze capability gaps between seniority levels."""
        
        gaps = []
        
        for capability in profile.capabilities:
            current_level = capability.proficiency
            target_level = self._get_target_capability_level(capability, to_seniority)
            
            if current_level != target_level:
                gap = {
                    'name': capability.name,
                    'current_level': current_level,
                    'target_level': target_level,
                    'priority': self._get_capability_priority(capability, to_seniority),
                    'development_actions': self._get_capability_development_actions(capability, current_level, target_level),
                    'success_indicators': self._get_capability_success_indicators(capability, target_level),
                    'timeline': self._get_capability_timeline(current_level, target_level)
                }
                gaps.append(gap)
        
        return sorted(gaps, key=lambda x: {'High': 0, 'Medium': 1, 'Low': 2}[x['priority']])
    
    def _analyze_responsibility_evolution(self, profile: RoleProfile, from_seniority: str, to_seniority: str) -> List[Dict[str, Any]]:
        """Analyze how responsibilities evolve between seniority levels."""
        
        evolution = []
        
        for resp in profile.responsibilities:
            current_expectation = self._get_responsibility_expectation(resp, from_seniority)
            target_expectation = self._get_responsibility_expectation(resp, to_seniority)
            
            if current_expectation != target_expectation:
                resp_evolution = {
                    'title': resp.title,
                    'current_expectation': current_expectation,
                    'target_expectation': target_expectation,
                    'development_areas': self._get_responsibility_development_areas(resp, from_seniority, to_seniority),
                    'target_metrics': self._enhance_success_metrics(resp.success_metrics, to_seniority)
                }
                evolution.append(resp_evolution)
        
        return evolution
    
    def _get_leadership_development_plan(self, from_seniority: str, to_seniority: str) -> List[Dict[str, Any]]:
        """Get leadership development plan based on seniority progression."""
        
        if from_seniority == to_seniority and to_seniority in ['Junior', 'Mid']:
            return []
        
        leadership_areas = {
            'Senior': [
                {
                    'category': 'Technical Leadership',
                    'objective': 'Guide technical decisions and mentor team members',
                    'activities': [
                        'Lead technical design reviews',
                        'Mentor junior team members',
                        'Drive technical standards adoption'
                    ],
                    'measurement': 'Team technical quality improvements, mentee feedback'
                }
            ],
            'Staff': [
                {
                    'category': 'Cross-team Leadership',
                    'objective': 'Influence technical strategy across multiple teams',
                    'activities': [
                        'Lead cross-team technical initiatives',
                        'Define architectural standards',
                        'Facilitate technical decision-making'
                    ],
                    'measurement': 'Cross-team adoption of standards, strategic initiative success'
                },
                {
                    'category': 'Organizational Impact',
                    'objective': 'Drive organizational technical excellence',
                    'activities': [
                        'Establish technical vision and roadmap',
                        'Lead major technical transformations',
                        'Develop technical talent pipeline'
                    ],
                    'measurement': 'Organizational technical metrics, talent development success'
                }
            ],
            'Principal': [
                {
                    'category': 'Strategic Leadership',
                    'objective': 'Shape organizational and industry direction',
                    'activities': [
                        'Define long-term technical strategy',
                        'Represent organization in industry forums',
                        'Drive innovation and emerging technology adoption'
                    ],
                    'measurement': 'Industry recognition, strategic initiative impact'
                }
            ]
        }
        
        return leadership_areas.get(to_seniority, [])
    
    def _get_required_experiences(self, profile: RoleProfile, from_seniority: str, to_seniority: str) -> List[Dict[str, Any]]:
        """Get required experiences for progression."""
        
        base_experiences = [
            {
                'category': 'Technical Execution',
                'description': f'Demonstrate {to_seniority}-level technical execution',
                'examples': ['Complex problem solving', 'System design', 'Performance optimization'],
                'timeline': '6-12 months'
            },
            {
                'category': 'Collaboration',
                'description': 'Effective cross-functional collaboration',
                'examples': ['Cross-team projects', 'Stakeholder management', 'Conflict resolution'],
                'timeline': '3-6 months'
            }
        ]
        
        if to_seniority in ['Senior', 'Staff', 'Principal']:
            base_experiences.append({
                'category': 'Leadership',
                'description': 'Demonstrated leadership impact',
                'examples': ['Mentoring others', 'Leading initiatives', 'Driving change'],
                'timeline': '6-12 months'
            })
        
        return base_experiences
    
    def _get_recommended_projects(self, profile: RoleProfile, from_seniority: str, to_seniority: str) -> List[Dict[str, Any]]:
        """Get recommended projects for skill development."""
        
        projects = []
        
        # Generate projects based on primary responsibilities
        for resp in profile.responsibilities:
            if resp.is_primary:
                project = {
                    'name': f'{resp.title} Enhancement Initiative',
                    'description': f'Lead improvement in {resp.title.lower()} with measurable impact',
                    'skills': [cap.name for cap in profile.capabilities[:3]],
                    'scope': self._get_project_scope_for_seniority(to_seniority),
                    'duration': self._get_project_duration_for_seniority(to_seniority)
                }
                projects.append(project)
        
        return projects[:3]  # Limit to top 3 projects
    
    def _get_mentorship_plan(self, profile: RoleProfile, from_seniority: str, to_seniority: str) -> List[Dict[str, Any]]:
        """Get mentorship plan for development."""
        
        mentorship = [
            {
                'area': 'Technical Excellence',
                'description': f'Technical mentorship for {to_seniority}-level capabilities',
                'mentor_profile': f'{to_seniority} or above in similar technical role',
                'frequency': 'Weekly 1-on-1s',
                'duration': '6-12 months'
            }
        ]
        
        if to_seniority in ['Senior', 'Staff', 'Principal']:
            mentorship.append({
                'area': 'Leadership Development',
                'description': 'Leadership skills and organizational navigation',
                'mentor_profile': f'{to_seniority} or above in leadership role',
                'frequency': 'Bi-weekly sessions',
                'duration': '12 months'
            })
        
        return mentorship
    
    def _get_learning_resources(self, profile: RoleProfile, from_seniority: str, to_seniority: str) -> List[Dict[str, Any]]:
        """Get learning resources for development."""
        
        resources = []
        
        # Add capability-specific resources
        for capability in profile.capabilities[:3]:
            resources.append({
                'category': capability.name,
                'description': f'Advanced {capability.name} training and certification',
                'type': 'Training/Certification',
                'priority': 'High',
                'timeline': '3-6 months'
            })
        
        # Add leadership resources for senior levels
        if to_seniority in ['Senior', 'Staff', 'Principal']:
            resources.append({
                'category': 'Leadership',
                'description': 'Leadership and management training',
                'type': 'Course/Workshop',
                'priority': 'High',
                'timeline': '6 months'
            })
        
        return resources
    
    def _get_key_relationships(self, profile: RoleProfile, to_seniority: str) -> List[Dict[str, Any]]:
        """Get key relationships to develop for target seniority."""
        
        relationships = []
        
        for interaction in profile.interactions:
            relationships.append({
                'role': interaction.target_role,
                'purpose': f'Enhanced {interaction.type.lower()} at {to_seniority} level',
                'interaction_type': interaction.type,
                'development_focus': self._get_relationship_development_focus(interaction, to_seniority)
            })
        
        return relationships
    
    def _get_cross_functional_exposure(self, profile: RoleProfile, to_seniority: str) -> List[Dict[str, Any]]:
        """Get cross-functional exposure recommendations."""
        
        exposure = [
            {
                'area': 'Business Strategy',
                'objective': 'Understand business context and strategic priorities',
                'activities': ['Business review meetings', 'Strategy sessions', 'Customer interactions'],
                'timeline': '6 months'
            }
        ]
        
        if to_seniority in ['Staff', 'Principal']:
            exposure.append({
                'area': 'Organizational Operations',
                'objective': 'Understand organizational dynamics and decision-making',
                'activities': ['Cross-department projects', 'Executive shadowing', 'Board meeting observation'],
                'timeline': '12 months'
            })
        
        return exposure
    
    def _get_milestones(self, profile: RoleProfile, from_seniority: str, to_seniority: str, months: int) -> List[Dict[str, Any]]:
        """Get milestone goals for specified timeframe."""
        
        milestones = []
        
        if months == 3:
            milestones = [
                {
                    'title': 'Capability Development',
                    'description': 'Demonstrate progress in key technical capabilities',
                    'success_criteria': 'Measurable improvement in primary skills',
                    'review_date': 'Month 3'
                },
                {
                    'title': 'Relationship Building',
                    'description': 'Establish key relationships for target role',
                    'success_criteria': 'Regular interaction with key stakeholders',
                    'review_date': 'Month 3'
                }
            ]
        elif months == 6:
            milestones = [
                {
                    'title': 'Leadership Demonstration',
                    'description': 'Lead initiative or project successfully',
                    'success_criteria': 'Positive project outcomes and stakeholder feedback',
                    'review_date': 'Month 6'
                },
                {
                    'title': 'Technical Excellence',
                    'description': 'Demonstrate technical excellence at target level',
                    'success_criteria': 'Recognition from peers and leadership',
                    'review_date': 'Month 6'
                }
            ]
        
        return milestones
    
    def _get_annual_goals(self, profile: RoleProfile, from_seniority: str, to_seniority: str) -> List[Dict[str, Any]]:
        """Get annual development goals."""
        
        goals = [
            {
                'title': 'Role Mastery',
                'description': f'Achieve {to_seniority}-level mastery in core role responsibilities',
                'expected_impact': 'Increased effectiveness and stakeholder confidence',
                'measurement': 'Performance review and 360 feedback'
            },
            {
                'title': 'Organizational Impact',
                'description': 'Drive meaningful improvements in team or organizational outcomes',
                'expected_impact': 'Measurable business or technical improvements',
                'measurement': 'Quantifiable metrics and stakeholder validation'
            }
        ]
        
        return goals
    
    def _get_technical_readiness(self, profile: RoleProfile, to_seniority: str) -> List[Dict[str, Any]]:
        """Get technical readiness criteria."""
        
        readiness = []
        
        for capability in profile.capabilities:
            target_level = self._get_target_capability_level(capability, to_seniority)
            readiness.append({
                'name': capability.name,
                'requirement': f'Demonstrate {target_level} proficiency',
                'evidence_needed': f'Portfolio of work, peer validation, practical demonstration'
            })
        
        return readiness
    
    def _get_leadership_readiness(self, to_seniority: str) -> List[Dict[str, Any]]:
        """Get leadership readiness criteria."""
        
        if to_seniority in ['Junior', 'Mid']:
            return []
        
        readiness = [
            {
                'area': 'Mentorship',
                'requirement': 'Successfully mentor junior team members',
                'examples': 'Mentee development, positive feedback, knowledge transfer'
            },
            {
                'area': 'Initiative Leadership',
                'requirement': 'Lead successful initiatives or projects',
                'examples': 'Project delivery, stakeholder satisfaction, team coordination'
            }
        ]
        
        if to_seniority in ['Staff', 'Principal']:
            readiness.append({
                'area': 'Strategic Thinking',
                'requirement': 'Demonstrate strategic thinking and organizational impact',
                'examples': 'Strategy contributions, cross-team influence, long-term vision'
            })
        
        return readiness
    
    def _get_business_readiness(self, profile: RoleProfile, to_seniority: str) -> List[Dict[str, Any]]:
        """Get business impact readiness criteria."""
        
        readiness = [
            {
                'category': 'Results Delivery',
                'requirement': 'Consistently deliver business results',
                'measurement': 'Success metrics achievement, stakeholder satisfaction'
            },
            {
                'category': 'Quality Excellence',
                'requirement': 'Maintain high quality standards',
                'measurement': 'Quality metrics, error rates, customer satisfaction'
            }
        ]
        
        if to_seniority in ['Senior', 'Staff', 'Principal']:
            readiness.append({
                'category': 'Innovation',
                'requirement': 'Drive innovation and continuous improvement',
                'measurement': 'Process improvements, new capabilities, efficiency gains'
            })
        
        return readiness
    
    # Helper methods for capability and responsibility analysis
    
    def _get_target_capability_level(self, capability: Capability, seniority: str) -> str:
        """Get target capability level for seniority."""
        
        current_level = capability.proficiency
        progression = self.capability_progression.get(current_level, {'next': current_level})
        
        # Senior+ levels typically need Advanced or Expert in key capabilities
        if seniority in ['Senior', 'Staff', 'Principal']:
            if current_level in ['Novice', 'Competent']:
                return 'Advanced'
            elif current_level == 'Advanced' and seniority in ['Staff', 'Principal']:
                return 'Expert'
        
        return progression['next']
    
    def _get_capability_priority(self, capability: Capability, seniority: str) -> str:
        """Determine development priority for capability."""
        
        # Primary capabilities get high priority
        if capability.name.lower() in ['sql', 'python', 'javascript', 'react', 'system', 'design']:
            return 'High'
        
        return 'Medium'
    
    def _get_capability_development_actions(self, capability: Capability, current_level: str, target_level: str) -> List[str]:
        """Get development actions for capability progression."""
        
        actions = [
            f'Complete advanced training in {capability.name}',
            f'Apply {capability.name} to complex real-world problems',
            f'Seek mentorship from {target_level}-level practitioners'
        ]
        
        if target_level in ['Expert', 'Master']:
            actions.extend([
                f'Contribute to {capability.name} best practices and standards',
                f'Present or teach {capability.name} concepts to others'
            ])
        
        return actions
    
    def _get_capability_success_indicators(self, capability: Capability, target_level: str) -> List[str]:
        """Get success indicators for capability development."""
        
        return [
            f'Peer recognition of {target_level} proficiency in {capability.name}',
            f'Successful application of {capability.name} to challenging problems',
            f'Ability to guide others in {capability.name} decisions'
        ]
    
    def _get_capability_timeline(self, current_level: str, target_level: str) -> str:
        """Get timeline for capability development."""
        
        progression_map = {
            ('Novice', 'Competent'): '3-6 months',
            ('Competent', 'Advanced'): '6-12 months',
            ('Advanced', 'Expert'): '12-18 months',
            ('Expert', 'Master'): '18+ months'
        }
        
        return progression_map.get((current_level, target_level), '6-12 months')
    
    def _get_responsibility_expectation(self, responsibility, seniority: str) -> str:
        """Get responsibility expectation for seniority level."""
        
        expectations = self.level_expectations.get(seniority, self.level_expectations['Mid'])
        return f"{expectations['autonomy']} with {expectations['scope'].lower()}"
    
    def _get_responsibility_development_areas(self, responsibility, from_seniority: str, to_seniority: str) -> List[Dict[str, str]]:
        """Get development areas for responsibility evolution."""
        
        return [
            {
                'focus': 'Scope Expansion',
                'description': f'Expand responsibility scope from {from_seniority} to {to_seniority} level',
                'actions': ['Take on larger initiatives', 'Handle more complex scenarios'],
                'timeline': '6 months'
            },
            {
                'focus': 'Quality Enhancement',
                'description': 'Improve quality and efficiency of responsibility execution',
                'actions': ['Optimize processes', 'Reduce errors', 'Increase throughput'],
                'timeline': '3-6 months'
            }
        ]
    
    def _enhance_success_metrics(self, current_metrics: str, seniority: str) -> str:
        """Enhance success metrics for target seniority."""
        
        if not current_metrics:
            return f"Define and achieve {seniority}-appropriate success metrics"
        
        enhancements = {
            'Senior': 'with increased scope and complexity',
            'Staff': 'with cross-team impact and strategic alignment',
            'Principal': 'with organizational transformation and industry leadership'
        }
        
        enhancement = enhancements.get(seniority, '')
        return f"{current_metrics} {enhancement}".strip()
    
    def _get_project_scope_for_seniority(self, seniority: str) -> str:
        """Get appropriate project scope for seniority level."""
        
        scopes = {
            'Mid': 'Single-team feature or component',
            'Senior': 'Cross-team system or major feature',
            'Staff': 'Multi-team platform or architecture initiative',
            'Principal': 'Organization-wide transformation or strategic initiative'
        }
        
        return scopes.get(seniority, 'Team-level project')
    
    def _get_project_duration_for_seniority(self, seniority: str) -> str:
        """Get appropriate project duration for seniority level."""
        
        durations = {
            'Mid': '2-4 months',
            'Senior': '3-6 months',
            'Staff': '6-12 months',
            'Principal': '12+ months'
        }
        
        return durations.get(seniority, '3-6 months')
    
    def _get_relationship_development_focus(self, interaction, seniority: str) -> str:
        """Get relationship development focus for target seniority."""
        
        if seniority in ['Senior', 'Staff', 'Principal']:
            return f'Strategic partnership and leadership influence in {interaction.type.lower()}'
        else:
            return f'Effective collaboration and communication in {interaction.type.lower()}'
    
    def _is_valid_progression(self, from_level: str, to_level: str) -> bool:
        """Check if progression between levels is valid."""
        
        try:
            from_index = self.seniority_levels.index(from_level)
            to_index = self.seniority_levels.index(to_level)
            
            # Allow same level (development plan) or progression up to 2 levels
            return to_index >= from_index and (to_index - from_index) <= 2
        except ValueError:
            return False
