"""
Agent Professional Profile Generator

Generates comprehensive professional profiles for AI agents based on role definitions.
These profiles provide agents with detailed context about their role, capabilities,
responsibilities, and operational guidelines.
"""

from pathlib import Path
from typing import Dict, List
import sys

# Add the parent directory to sys.path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core.profile_parser import ProfileParser, RoleProfile
from core.template_engine import TemplateEngine
from core.output_formatter import OutputFormatter

class AgentProfileGenerator:
    """Generates professional profiles for AI agents."""
    
    def __init__(self, roles_dir: str, templates_dir: str, output_dir: str):
        self.parser = ProfileParser(Path(roles_dir))
        self.template_engine = TemplateEngine(templates_dir)
        self.output_formatter = OutputFormatter(Path(output_dir))
    
    def generate_agent_profile(self, role_slug: str, agent_name: str = None, 
                              specialization: str = None) -> str:
        """
        Generate a professional profile for an AI agent.
        
        Args:
            role_slug: The slug of the role to generate profile for
            agent_name: Optional custom name for the agent
            specialization: Optional specialization within the role
            
        Returns:
            Path to the generated agent profile file
        """
        # Parse the role profile
        role = self.parser.parse_profile(role_slug)
        if not role:
            raise ValueError(f"Role '{role_slug}' not found")
        
        # Generate agent-specific context
        agent_context = self._build_agent_context(role, agent_name, specialization)
        
        # Render the agent profile template
        content = self.template_engine.render_template(
            'agent/professional_profile.md',
            agent_context
        )
        
        # Generate output filename
        filename = f"agent_profile_{role_slug}"
        if specialization:
            filename += f"_{specialization.lower().replace(' ', '-')}"
        filename += ".md"
        
        # Write the file
        output_path = self.output_formatter.save_artifact(
            content, 
            filename, 
            subfolder="agent"
        )
        
        return output_path
    
    def _build_agent_context(self, role: RoleProfile, agent_name: str = None, 
                           specialization: str = None) -> Dict:
        """Build context dictionary for agent profile template."""
        
        # Default agent name if not provided
        if not agent_name:
            agent_name = f"{role.name} Agent"
        
        # Extract key capabilities by proficiency level
        advanced_capabilities = [
            cap for cap in role.capabilities 
            if cap.proficiency.lower() in ['advanced', 'expert']
        ]
        
        intermediate_capabilities = [
            cap for cap in role.capabilities 
            if cap.proficiency.lower() in ['intermediate', 'proficient']
        ]
        
        # Primary responsibilities (marked as primary or first 3)
        primary_responsibilities = [
            resp for resp in role.responsibilities 
            if resp.is_primary
        ]
        if not primary_responsibilities:
            primary_responsibilities = role.responsibilities[:3]
        
        # Key artifacts the agent would work with
        key_artifacts = role.artifacts[:5]  # Top 5 artifacts
        
        # Interaction patterns for collaboration
        collaboration_patterns = [
            inter for inter in role.interactions 
            if inter.type.lower() in ['collaborates with', 'provides', 'receives']
        ]
        
        # Build decision-making guidelines from responsibilities
        decision_guidelines = self._extract_decision_guidelines(role)
        
        # Build operational context
        operational_context = self._build_operational_context(role)
        
        return {
            'agent_name': agent_name,
            'role': role,
            'specialization': specialization,
            'advanced_capabilities': advanced_capabilities,
            'intermediate_capabilities': intermediate_capabilities,
            'primary_responsibilities': primary_responsibilities,
            'key_artifacts': key_artifacts,
            'collaboration_patterns': collaboration_patterns,
            'decision_guidelines': decision_guidelines,
            'operational_context': operational_context,
            'success_metrics': self._extract_success_metrics(role),
            'escalation_triggers': self._build_escalation_triggers(role),
            'quality_standards': self._extract_quality_standards(role)
        }
    
    def _extract_decision_guidelines(self, role: RoleProfile) -> List[Dict]:
        """Extract decision-making guidelines from role responsibilities."""
        guidelines = []
        
        for resp in role.responsibilities:
            if any(keyword in resp.title.lower() for keyword in 
                   ['design', 'architecture', 'strategy', 'planning']):
                guidelines.append({
                    'domain': resp.title,
                    'approach': resp.description,
                    'success_criteria': resp.success_metrics
                })
        
        return guidelines
    
    def _build_operational_context(self, role: RoleProfile) -> Dict:
        """Build operational context from role properties."""
        context = {
            'tech_stack': [],
            'methodology': [],
            'working_style': []
        }
        
        properties = role.properties
        if 'Preferred Tech' in properties:
            context['tech_stack'] = [
                tech.strip() for tech in properties['Preferred Tech'].split(',')
            ]
        
        if 'Workstyle' in properties:
            context['working_style'] = [properties['Workstyle']]
        
        if 'Working Model' in properties:
            context['methodology'] = [properties['Working Model']]
        
        return context
    
    def _extract_success_metrics(self, role: RoleProfile) -> List[str]:
        """Extract success metrics from responsibilities."""
        metrics = []
        for resp in role.responsibilities:
            if resp.success_metrics:
                metrics.append(resp.success_metrics)
        return metrics
    
    def _build_escalation_triggers(self, role: RoleProfile) -> List[str]:
        """Build escalation triggers based on role responsibilities."""
        triggers = [
            "When technical decisions exceed defined authority levels",
            "When cross-team coordination is required for implementation",
            "When timeline or resource constraints impact deliverables",
            "When security or compliance requirements are unclear"
        ]
        
        # Add role-specific triggers based on responsibilities
        for resp in role.responsibilities:
            if 'security' in resp.title.lower():
                triggers.append("When security vulnerabilities are discovered")
            if 'performance' in resp.title.lower():
                triggers.append("When performance metrics exceed acceptable thresholds")
            if 'integration' in resp.title.lower():
                triggers.append("When third-party service integrations fail")
        
        return list(set(triggers))  # Remove duplicates
    
    def _extract_quality_standards(self, role: RoleProfile) -> List[str]:
        """Extract quality standards from role context."""
        standards = [
            "Follow established coding standards and best practices",
            "Ensure comprehensive testing before implementation",
            "Document all technical decisions and trade-offs",
            "Maintain backward compatibility unless explicitly breaking"
        ]
        
        # Add role-specific standards
        if any('api' in resp.title.lower() for resp in role.responsibilities):
            standards.append("Ensure API responses include proper error handling and status codes")
        
        if any('database' in resp.title.lower() for resp in role.responsibilities):
            standards.append("Optimize database queries for performance and scalability")
        
        if any('security' in resp.title.lower() for resp in role.responsibilities):
            standards.append("Apply security-first principles to all implementations")
        
        return standards

def main():
    """CLI entry point for agent profile generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate AI agent professional profiles')
    parser.add_argument('role_slug', help='Role slug to generate profile for')
    parser.add_argument('--agent-name', help='Custom name for the agent')
    parser.add_argument('--specialization', help='Specialization within the role')
    parser.add_argument('--roles-dir', default='./roles', help='Directory containing role profiles')
    parser.add_argument('--templates-dir', default='./generators/templates', help='Templates directory')
    parser.add_argument('--output-dir', default='./generated', help='Output directory')
    
    args = parser.parse_args()
    
    generator = AgentProfileGenerator(
        roles_dir=args.roles_dir,
        templates_dir=args.templates_dir,
        output_dir=args.output_dir
    )
    
    try:
        output_path = generator.generate_agent_profile(
            role_slug=args.role_slug,
            agent_name=args.agent_name,
            specialization=args.specialization
        )
        print(f"Agent profile generated: {output_path}")
    except Exception as e:
        print(f"Error generating agent profile: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
