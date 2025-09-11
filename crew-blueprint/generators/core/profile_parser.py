"""
Core utilities for role profile parsing and data extraction.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Responsibility:
    title: str
    description: str
    success_metrics: str
    is_primary: bool = False

@dataclass
class Capability:
    name: str
    proficiency: str
    description: str

@dataclass
class Artifact:
    name: str
    type: str
    description: str = ""

@dataclass
class Interaction:
    type: str
    target_role: str
    frequency: str
    notes: str = ""

@dataclass
class RoleProfile:
    id: str
    slug: str
    name: str
    default_seniority: str
    mission: str
    short_description: str
    properties: Dict
    responsibilities: List[Responsibility]
    capabilities: List[Capability]
    artifacts: List[Artifact]
    interactions: List[Interaction]

class ProfileParser:
    """Parses role profile markdown files into structured data."""
    
    def __init__(self, roles_dir: Path = None):
        if roles_dir is None:
            roles_dir = Path(__file__).parent.parent.parent / 'roles'
        self.roles_dir = roles_dir
    
    def parse_profile(self, role_slug: str) -> Optional[RoleProfile]:
        """Parse a single role profile."""
        profile_path = self.roles_dir / role_slug / 'profile.md'
        
        if not profile_path.exists():
            return None
        
        with open(profile_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        frontmatter = self._extract_frontmatter(content)
        if not frontmatter:
            return None
        
        # Parse sections
        sections = self._parse_sections(content)
        
        return RoleProfile(
            id=frontmatter.get('id', ''),
            slug=frontmatter.get('slug', role_slug),
            name=frontmatter.get('name', ''),
            default_seniority=frontmatter.get('default_seniority', ''),
            mission=sections.get('mission', ''),
            short_description=sections.get('short_description', ''),
            properties=self._parse_properties(sections.get('properties', '')),
            responsibilities=self._parse_responsibilities(sections.get('responsibilities', '')),
            capabilities=self._parse_capabilities(sections.get('capabilities', '')),
            artifacts=self._parse_artifacts(sections.get('artifacts', '')),
            interactions=self._parse_interactions(sections.get('interactions', ''))
        )
    
    def get_all_roles(self) -> List[str]:
        """Get list of all available role slugs."""
        role_dirs = [d.name for d in self.roles_dir.iterdir() 
                    if d.is_dir() and (d / 'profile.md').exists()]
        return sorted(role_dirs)
    
    def get_all_profiles(self) -> Dict[str, RoleProfile]:
        """Parse all role profiles."""
        profiles = {}
        for role_slug in self.get_all_roles():
            profile = self.parse_profile(role_slug)
            if profile:
                profiles[role_slug] = profile
        return profiles
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict]:
        """Extract YAML frontmatter from markdown content."""
        if not content.startswith('---\n'):
            return None
        
        end_marker = content.find('\n---\n', 4)
        if end_marker == -1:
            return None
        
        frontmatter_text = content[4:end_marker]
        return yaml.safe_load(frontmatter_text)
    
    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown sections into a dictionary."""
        sections = {}
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        
        # Skip frontmatter
        in_frontmatter = False
        frontmatter_ended = False
        
        for line in lines:
            if line.strip() == '---' and not frontmatter_ended:
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    in_frontmatter = False
                    frontmatter_ended = True
                continue
            
            if in_frontmatter:
                continue
            
            if line.startswith('# ') and frontmatter_ended:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line[2:].strip().lower().replace(' ', '_')
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _parse_properties(self, properties_text: str) -> Dict:
        """Parse properties section into structured data."""
        properties = {}
        lines = properties_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- **') and '**:' in line:
                key_end = line.find('**:', 4)
                if key_end > 4:
                    key = line[4:key_end].lower().replace(' ', '_')
                    value = line[key_end + 3:].strip()
                    properties[key] = value
        
        return properties
    
    def _parse_responsibilities(self, resp_text: str) -> List[Responsibility]:
        """Parse responsibilities section."""
        responsibilities = []
        lines = resp_text.split('\n')
        
        current_resp = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('- **') and '**' in line:
                # Save previous responsibility
                if current_resp:
                    responsibilities.append(current_resp)
                
                # Parse new responsibility
                title_end = line.find('**', 4)
                if title_end > 4:
                    title = line[4:title_end]
                    is_primary = '(primary)' in line
                    description = line[title_end + 2:].strip()
                    if description.startswith('(primary)'):
                        description = description[9:].strip()
                    
                    current_resp = Responsibility(
                        title=title,
                        description=description,
                        success_metrics="",
                        is_primary=is_primary
                    )
            elif line.startswith('*Success metric*:') and current_resp:
                current_resp.success_metrics = line[17:].strip()
        
        # Save last responsibility
        if current_resp:
            responsibilities.append(current_resp)
        
        return responsibilities
    
    def _parse_capabilities(self, cap_text: str) -> List[Capability]:
        """Parse capabilities section."""
        capabilities = []
        lines = cap_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- **') and '**' in line and '—' in line:
                parts = line[4:].split('**', 1)
                if len(parts) == 2:
                    name = parts[0]
                    remainder = parts[1].strip()
                    if remainder.startswith('—'):
                        proficiency_desc = remainder[1:].strip()
                        # Split proficiency and description
                        prof_parts = proficiency_desc.split('(', 1)
                        proficiency = prof_parts[0].strip()
                        description = prof_parts[1].rstrip(')') if len(prof_parts) > 1 else ""
                        
                        capabilities.append(Capability(
                            name=name,
                            proficiency=proficiency,
                            description=description
                        ))
        
        return capabilities
    
    def _parse_artifacts(self, art_text: str) -> List[Artifact]:
        """Parse artifacts section."""
        artifacts = []
        lines = art_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- **') and '**' in line:
                # Extract name and type
                match = re.match(r'- \*\*(.+?)\*\* \(type: (.+?)\)', line)
                if match:
                    name = match.group(1)
                    artifact_type = match.group(2)
                    artifacts.append(Artifact(
                        name=name,
                        type=artifact_type
                    ))
        
        return artifacts
    
    def _parse_interactions(self, int_text: str) -> List[Interaction]:
        """Parse interactions section."""
        interactions = []
        lines = int_text.split('\n')
        
        current_interaction = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('- **') and '**' in line and '→' in line:
                # Parse interaction line
                # Format: - **interaction_type** → Target Role (frequency)
                match = re.match(r'- \*\*(.+?)\*\* → (.+?) \((.+?)\)', line)
                if match:
                    interaction_type = match.group(1)
                    target_role = match.group(2)
                    frequency = match.group(3)
                    
                    current_interaction = Interaction(
                        type=interaction_type,
                        target_role=target_role,
                        frequency=frequency
                    )
                    interactions.append(current_interaction)
            elif line.startswith('*Notes*:') and current_interaction:
                current_interaction.notes = line[8:].strip()
        
        return interactions
