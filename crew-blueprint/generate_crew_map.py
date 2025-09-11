#!/usr/bin/env python3
"""
Crew Map Generator

Generates Mermaid diagrams from role interactions.
Usage: python generate_crew_map.py
"""

import yaml
import re
from pathlib import Path

def extract_frontmatter_and_interactions(file_path):
    """Extract frontmatter and interactions section from a profile."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    if not content.startswith('---\n'):
        return None, []
    
    end_marker = content.find('\n---\n', 4)
    if end_marker == -1:
        return None, []
    
    frontmatter = yaml.safe_load(content[4:end_marker])
    
    # Extract interactions
    lines = content.split('\n')
    interactions = []
    in_interactions = False
    
    for line in lines:
        if line.strip() == '# Interactions':
            in_interactions = True
            continue
        elif line.startswith('# ') and in_interactions:
            break
        elif in_interactions and line.strip().startswith('- **'):
            # Parse interaction line
            # Format: - **interaction_type** → Target Role (frequency)
            match = re.match(r'- \*\*(.+?)\*\* → (.+?) \((.+?)\)', line.strip())
            if match:
                interaction_type = match.group(1)
                target_role = match.group(2)
                frequency = match.group(3)
                interactions.append({
                    'type': interaction_type,
                    'target': target_role,
                    'frequency': frequency
                })
    
    return frontmatter, interactions

def generate_mermaid_diagram():
    """Generate a Mermaid flowchart from role interactions."""
    roles_dir = Path(__file__).parent / 'roles'
    profile_files = list(roles_dir.glob('*/profile.md'))
    
    # Collect all roles and interactions
    role_map = {}  # slug -> name
    all_interactions = []
    
    for profile_path in profile_files:
        role_slug = profile_path.parent.name
        frontmatter, interactions = extract_frontmatter_and_interactions(profile_path)
        
        if frontmatter:
            role_name = frontmatter.get('name', role_slug)
            role_map[role_slug] = role_name
            
            for interaction in interactions:
                all_interactions.append({
                    'from_role': role_name,
                    'from_slug': role_slug,
                    'type': interaction['type'],
                    'target': interaction['target'],
                    'frequency': interaction['frequency']
                })
    
    # Generate Mermaid diagram
    mermaid = "```mermaid\nflowchart TD\n"
    
    # Add nodes for each role
    for slug, name in role_map.items():
        safe_id = slug.replace('-', '_')
        mermaid += f"    {safe_id}[\"{name}\"]\n"
    
    # Add interaction edges
    for interaction in all_interactions:
        from_id = interaction['from_slug'].replace('-', '_')
        
        # Try to map target to known role
        target_id = None
        for slug, name in role_map.items():
            if name == interaction['target']:
                target_id = slug.replace('-', '_')
                break
        
        if not target_id:
            # Create external role node
            target_safe = interaction['target'].replace(' ', '_').replace('-', '_').lower()
            target_id = f"ext_{target_safe}"
            mermaid += f"    {target_id}[\"{interaction['target']}\"]:::external\n"
        
        # Add edge with interaction type and frequency
        label = f"{interaction['type']} ({interaction['frequency']})"
        mermaid += f"    {from_id} --> {target_id}\n"
        mermaid += f"    {from_id} -.->|{label}| {target_id}\n"
    
    # Add styling
    mermaid += "\n    classDef external fill:#f9f9f9,stroke:#999,stroke-dasharray: 5 5\n"
    mermaid += "```"
    
    return mermaid

def main():
    """Generate crew interaction map."""
    diagram = generate_mermaid_diagram()
    
    # Create crew map file
    crew_map_content = f"""# Crew Interaction Map

This diagram shows the interactions between roles based on their profile definitions.

{diagram}

## Legend

- **Solid arrows**: Direct interactions
- **Dotted arrows**: Interaction details (type and frequency)
- **Dashed boxes**: External roles (not yet defined in this catalog)

---
*Generated automatically from role profiles*
"""
    
    crew_map_path = Path(__file__).parent / 'CREW_MAP.md'
    with open(crew_map_path, 'w', encoding='utf-8') as f:
        f.write(crew_map_content)
    
    print(f"🗺️  Crew interaction map generated: {crew_map_path}")
    print("\nDiagram preview:")
    print(diagram)

if __name__ == '__main__':
    main()
