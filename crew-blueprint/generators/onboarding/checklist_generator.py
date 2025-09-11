"""
Onboarding checklist generator for role profiles.
"""

from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta

from ..core import ProfileParser, TemplateEngine, OutputFormatter, RoleProfile, Responsibility, Capability, Interaction

class OnboardingGenerator:
    """Generates onboarding checklists for roles at different seniority levels."""
    
    def __init__(self, roles_dir: Path = None, templates_dir: Path = None, output_dir: Path = None):
        self.parser = ProfileParser(roles_dir)
        
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / 'templates'
        self.template_engine = TemplateEngine(templates_dir)
        
        self.formatter = OutputFormatter(output_dir)
        
        # Seniority-specific configurations
        self.seniority_config = {
            'Junior': {
                'shadow_periods': {'primary': '2-3 weeks', 'secondary': '1-2 weeks'},
                'initial_scope': 'well-defined tasks with mentorship',
                'target_proficiency_modifier': -1,
                'review_frequency': 'weekly',
                'learning_focus': 'foundational skills'
            },
            'Mid': {
                'shadow_periods': {'primary': '1-2 weeks', 'secondary': '1 week'},
                'initial_scope': 'independent tasks with guidance',
                'target_proficiency_modifier': 0,
                'review_frequency': 'bi-weekly',
                'learning_focus': 'specialization and depth'
            },
            'Senior': {
                'shadow_periods': {'primary': '1 week', 'secondary': '3-5 days'},
                'initial_scope': 'full ownership with strategic guidance',
                'target_proficiency_modifier': 1,
                'review_frequency': 'monthly',
                'learning_focus': 'leadership and system thinking'
            },
            'Staff': {
                'shadow_periods': {'primary': '3-5 days', 'secondary': '2-3 days'},
                'initial_scope': 'immediate ownership plus improvement initiatives',
                'target_proficiency_modifier': 2,
                'review_frequency': 'monthly',
                'learning_focus': 'architecture and cross-team impact'
            },
            'Principal': {
                'shadow_periods': {'primary': '2-3 days', 'secondary': '1-2 days'},
                'initial_scope': 'strategic ownership and transformation',
                'target_proficiency_modifier': 3,
                'review_frequency': 'quarterly',
                'learning_focus': 'organizational impact and vision'
            }
        }
    
    def generate_checklist(self, role_slug: str, target_seniority: str = None) -> str:
        """Generate an onboarding checklist for a specific role and seniority."""
        
        # Parse role profile
        profile = self.parser.parse_profile(role_slug)
        if not profile:
            raise ValueError(f"Role profile not found: {role_slug}")
        
        # Use target seniority or default
        seniority = target_seniority or profile.default_seniority
        
        # Build template context
        context = self._build_context(profile, seniority)
        
        # Render template
        checklist_content = self.template_engine.render_template(
            'onboarding/checklist.md', 
            context
        )
        
        return checklist_content
    
    def save_checklist(self, role_slug: str, target_seniority: str = None) -> Path:
        """Generate and save an onboarding checklist."""
        
        profile = self.parser.parse_profile(role_slug)
        if not profile:
            raise ValueError(f"Role profile not found: {role_slug}")
        
        seniority = target_seniority or profile.default_seniority
        checklist_content = self.generate_checklist(role_slug, seniority)
        
        # Generate filename and save
        filename = self.formatter.get_output_filename(
            'onboarding', role_slug, seniority, 'checklist'
        )
        
        metadata = {
            'artifact_type': 'onboarding_checklist',
            'role': profile.name,
            'seniority': seniority,
            'source_profile': f'roles/{role_slug}/profile.md'
        }
        
        output_path = self.formatter.save_artifact(
            checklist_content, filename, 'onboarding', metadata
        )
        
        return output_path
    
    def generate_all_checklists(self, include_seniority_variants: bool = False) -> Dict[str, Path]:
        """Generate onboarding checklists for all roles."""
        
        generated_files = {}
        all_roles = self.parser.get_all_roles()
        
        for role_slug in all_roles:
            profile = self.parser.parse_profile(role_slug)
            if not profile:
                continue
            
            # Generate for default seniority
            output_path = self.save_checklist(role_slug)
            generated_files[f"{role_slug}_{profile.default_seniority}"] = output_path
            
            # Generate for other seniority levels if requested
            if include_seniority_variants:
                other_seniorities = [s for s in self.seniority_config.keys() 
                                   if s != profile.default_seniority]
                
                for seniority in other_seniorities:
                    variant_path = self.save_checklist(role_slug, seniority)
                    generated_files[f"{role_slug}_{seniority}"] = variant_path
        
        return generated_files
    
    def _build_context(self, profile: RoleProfile, seniority: str) -> Dict[str, Any]:
        """Build template context for a role and seniority."""
        
        config = self.seniority_config.get(seniority, self.seniority_config['Mid'])
        
        return {
            'role': profile,
            'seniority': seniority,
            'generation_date': datetime.now().strftime('%Y-%m-%d'),
            'week_1_tasks': self._generate_week_1_tasks(profile, seniority),
            'foundation_tasks': self._generate_foundation_tasks(profile, seniority),
            'learning_priorities': self._generate_learning_priorities(profile, seniority),
            'key_relationships': self._generate_key_relationships(profile, seniority),
            'starter_responsibilities': self._generate_starter_responsibilities(profile, seniority),
            'get_expected_proficiency': lambda resp, sen: self._get_expected_proficiency(resp, sen),
            'get_review_week': lambda resp: self._get_review_week(resp, seniority),
            'get_target_proficiency': lambda cap, sen: self._get_target_proficiency(cap, sen),
            'get_development_plan': lambda cap, sen: self._get_development_plan(cap, sen),
            'get_capability_resources': lambda cap: self._get_capability_resources(cap),
            'get_contribution_areas': lambda role, sen: self._get_contribution_areas(role, sen)
        }
    
    def _generate_week_1_tasks(self, profile: RoleProfile, seniority: str) -> List[str]:
        """Generate week 1 orientation tasks."""
        
        base_tasks = [
            "Complete IT setup and access provisioning",
            "Review role profile and expectations",
            f"Meet with direct manager to discuss {profile.name} responsibilities",
            "Join relevant team channels and communication tools",
            "Complete required compliance and security training"
        ]
        
        if seniority in ['Senior', 'Staff', 'Principal']:
            base_tasks.extend([
                "Review team strategy and current initiatives",
                "Understand decision-making processes and escalation paths"
            ])
        
        # Add role-specific tasks
        if 'engineer' in profile.name.lower():
            base_tasks.extend([
                "Set up development environment and tools",
                "Review codebase and technical documentation",
                "Understand deployment and release processes"
            ])
        elif 'manager' in profile.name.lower() or 'product' in profile.name.lower():
            base_tasks.extend([
                "Review current product roadmap and priorities",
                "Understand stakeholder landscape and communication norms"
            ])
        
        return base_tasks
    
    def _generate_foundation_tasks(self, profile: RoleProfile, seniority: str) -> List[str]:
        """Generate foundation-building tasks for weeks 2-4."""
        
        tasks = [
            f"Deep dive into {profile.name} mission and success metrics",
            "Shadow team members in daily workflows",
            "Review all artifacts owned by this role",
            "Understand interaction patterns with other roles"
        ]
        
        # Add responsibility-specific tasks
        for resp in profile.responsibilities[:3]:  # Top 3 responsibilities
            tasks.append(f"Learn current approach to: {resp.title}")
        
        # Add capability-specific tasks
        for cap in profile.capabilities[:2]:  # Top 2 capabilities
            tasks.append(f"Assess current {cap.name} knowledge and identify learning needs")
        
        return tasks
    
    def _generate_learning_priorities(self, profile: RoleProfile, seniority: str) -> List[Dict[str, str]]:
        """Generate learning priorities based on capabilities and seniority."""
        
        priorities = []
        config = self.seniority_config.get(seniority, self.seniority_config['Mid'])
        
        for cap in profile.capabilities:
            priority = {
                'name': cap.name,
                'current_level': cap.proficiency,
                'target_level': self._get_target_proficiency(cap, seniority),
                'development_plan': self._get_development_plan(cap, seniority)
            }
            priorities.append(priority)
        
        return priorities[:4]  # Top 4 priorities
    
    def _generate_key_relationships(self, profile: RoleProfile, seniority: str) -> List[Dict[str, str]]:
        """Generate key relationship building activities."""
        
        relationships = []
        
        for interaction in profile.interactions:
            relationship = {
                'type': interaction.type,
                'target_role': interaction.target_role,
                'frequency': interaction.frequency,
                'timeline': self._get_meeting_timeline(interaction, seniority),
                'focus_areas': self._get_relationship_focus(interaction, seniority)
            }
            relationships.append(relationship)
        
        return relationships
    
    def _generate_starter_responsibilities(self, profile: RoleProfile, seniority: str) -> List[Dict[str, str]]:
        """Generate starter responsibility assignments."""
        
        config = self.seniority_config.get(seniority, self.seniority_config['Mid'])
        starter_resps = []
        
        for resp in profile.responsibilities:
            starter = {
                'title': resp.title,
                'shadow_period': config['shadow_periods']['primary'] if resp.is_primary 
                               else config['shadow_periods']['secondary'],
                'initial_scope': config['initial_scope'],
                'success_metrics': resp.success_metrics
            }
            starter_resps.append(starter)
        
        return starter_resps
    
    def _get_expected_proficiency(self, resp: Responsibility, seniority: str) -> str:
        """Get expected proficiency for a responsibility at given seniority."""
        
        proficiency_map = {
            'Junior': 'Guided execution',
            'Mid': 'Independent execution', 
            'Senior': 'Expert execution + mentoring',
            'Staff': 'Strategic leadership',
            'Principal': 'Organizational impact'
        }
        
        return proficiency_map.get(seniority, 'Independent execution')
    
    def _get_review_week(self, resp: Responsibility, seniority: str) -> int:
        """Get review week for responsibility based on priority and seniority."""
        
        if resp.is_primary:
            return 6 if seniority in ['Junior', 'Mid'] else 4
        else:
            return 10 if seniority in ['Junior', 'Mid'] else 8
    
    def _get_target_proficiency(self, cap: Capability, seniority: str) -> str:
        """Get target proficiency for capability at given seniority."""
        
        proficiency_levels = ['Novice', 'Competent', 'Advanced', 'Expert', 'Master']
        
        try:
            current_index = proficiency_levels.index(cap.proficiency)
        except ValueError:
            current_index = 1  # Default to Competent
        
        config = self.seniority_config.get(seniority, self.seniority_config['Mid'])
        modifier = config['target_proficiency_modifier']
        
        target_index = min(max(current_index + modifier, 0), len(proficiency_levels) - 1)
        return proficiency_levels[target_index]
    
    def _get_development_plan(self, cap: Capability, seniority: str) -> str:
        """Get development plan for capability."""
        
        config = self.seniority_config.get(seniority, self.seniority_config['Mid'])
        focus = config['learning_focus']
        
        plans = {
            'foundational skills': f"Complete basic training and guided practice in {cap.name}",
            'specialization and depth': f"Deepen expertise in {cap.name} through projects and mentorship",
            'leadership and system thinking': f"Apply {cap.name} to complex problems and mentor others",
            'architecture and cross-team impact': f"Lead strategic initiatives using {cap.name}",
            'organizational impact and vision': f"Define organizational standards and vision for {cap.name}"
        }
        
        return plans.get(focus, f"Develop proficiency in {cap.name}")
    
    def _get_capability_resources(self, cap: Capability) -> str:
        """Get learning resources for capability."""
        
        # This would typically pull from a knowledge base
        # For now, return a placeholder
        return f"Internal docs, training materials, and mentorship for {cap.name}"
    
    def _get_contribution_areas(self, profile: RoleProfile, seniority: str) -> str:
        """Get expected contribution areas by seniority."""
        
        primary_resps = [r.title for r in profile.responsibilities if r.is_primary]
        
        if seniority in ['Junior', 'Mid']:
            return f"{primary_resps[0]} with guidance" if primary_resps else "assigned tasks"
        elif seniority == 'Senior':
            return f"{', '.join(primary_resps[:2])}" if len(primary_resps) >= 2 else "primary responsibilities"
        else:
            return "strategic initiatives and team leadership"
    
    def _get_meeting_timeline(self, interaction: Interaction, seniority: str) -> str:
        """Get timeline for initial meetings."""
        
        if interaction.frequency == 'daily':
            return "Week 1"
        elif interaction.frequency in ['weekly', 'per sprint']:
            return "Week 2"
        else:
            return "Week 3-4"
    
    def _get_relationship_focus(self, interaction: Interaction, seniority: str) -> str:
        """Get focus areas for relationship building."""
        
        focus_map = {
            'Collaborates with': 'Working styles, communication preferences, current projects',
            'Depends on': 'Service levels, escalation processes, request procedures',
            'Delivers': 'Quality expectations, delivery schedules, feedback mechanisms',
            'Provides': 'Requirements gathering, stakeholder needs, success metrics',
            'Reports to': 'Goals alignment, feedback cadence, support needs'
        }
        
        return focus_map.get(interaction.type, 'Working relationship and expectations')
