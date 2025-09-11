#!/usr/bin/env python3
"""
Artifact generation CLI for the Role Atlas system.

Usage:
    python generate_artifacts.py onboarding --role=data-engineer [--seniority=mid]
    python generate_artifacts.py career --role=data-engineer --from=mid --to=senior
    python generate_artifacts.py all-onboarding
    python generate_artifacts.py all-career
    python generate_artifacts.py all
"""

import sys
import argparse
from pathlib import Path

# Add generators to path
sys.path.insert(0, str(Path(__file__).parent / 'generators'))

from generators.core import ProfileParser
from generators.onboarding.checklist_generator import OnboardingGenerator
from generators.career.ladder_generator import CareerLadderGenerator
from generators.agent.profile_generator import AgentProfileGenerator

def main():
    parser = argparse.ArgumentParser(description='Generate artifacts from role profiles')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Onboarding command
    onboarding_parser = subparsers.add_parser('onboarding', help='Generate onboarding checklist')
    onboarding_parser.add_argument('--role', required=True, help='Role slug (e.g., data-engineer)')
    onboarding_parser.add_argument('--seniority', help='Target seniority level')
    
    # Agent command
    agent_parser = subparsers.add_parser('agent', help='Generate agent professional profile')
    agent_parser.add_argument('--role', required=True, help='Role slug (e.g., data-engineer)')
    agent_parser.add_argument('--agent-name', help='Custom name for the agent')
    agent_parser.add_argument('--specialization', help='Specialization within the role')
    
    # Career command
    career_parser = subparsers.add_parser('career', help='Generate career ladder')
    career_parser.add_argument('--role', required=True, help='Role slug')
    career_parser.add_argument('--from', dest='from_seniority', required=True, help='Current seniority')
    career_parser.add_argument('--to', dest='to_seniority', help='Target seniority')
    
    # Bulk generation commands
    subparsers.add_parser('all-onboarding', help='Generate all onboarding checklists')
    subparsers.add_parser('all-career', help='Generate all career ladders')
    subparsers.add_parser('all-agents', help='Generate all agent profiles')
    subparsers.add_parser('all', help='Generate all artifacts')
    
    # List command
    subparsers.add_parser('list-roles', help='List available roles')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'onboarding':
            generate_onboarding(args.role, args.seniority)
        elif args.command == 'career':
            generate_career(args.role, args.from_seniority, args.to_seniority)
        elif args.command == 'agent':
            generate_agent_profile(args.role, args.agent_name, args.specialization)
        elif args.command == 'all-onboarding':
            generate_all_onboarding()
        elif args.command == 'all-career':
            generate_all_career()
        elif args.command == 'all-agents':
            generate_all_agents()
        elif args.command == 'all':
            generate_all_artifacts()
        elif args.command == 'list-roles':
            list_roles()
        else:
            print(f"Unknown command: {args.command}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def generate_onboarding(role_slug: str, seniority: str = None):
    """Generate onboarding checklist for a role."""
    print(f"Generating onboarding checklist for {role_slug}...")
    
    generator = OnboardingGenerator()
    output_path = generator.save_checklist(role_slug, seniority)
    
    print(f"✅ Generated: {output_path}")

def generate_career(role_slug, from_seniority, to_seniority=None):
    """Generate career ladder for a specific role and progression."""
    generator = CareerLadderGenerator(
        roles_dir='./roles',
        templates_dir='./generators/templates',
        output_dir='./generated'
    )
    
    output_path = generator.generate_career_ladder(role_slug, from_seniority, to_seniority)
    print(f"✅ Career ladder generated: {output_path}")

def generate_agent_profile(role_slug, agent_name=None, specialization=None):
    """Generate agent professional profile for a specific role."""
    generator = AgentProfileGenerator(
        roles_dir='./roles',
        templates_dir='./generators/templates',
        output_dir='./generated'
    )
    
    output_path = generator.generate_agent_profile(role_slug, agent_name, specialization)
    print(f"✅ Agent profile generated: {output_path}")

def generate_all_onboarding():
    """Generate onboarding checklists for all roles."""
    print("Generating all onboarding checklists...")
    
    generator = OnboardingGenerator()
    generated_files = generator.generate_all_checklists(include_seniority_variants=True)
    
    print(f"✅ Generated {len(generated_files)} onboarding checklists:")
    for name, path in generated_files.items():
        print(f"   - {name}: {path.name}")

def generate_all_agents():
    """Generate agent profiles for all roles."""
    print("Generating all agent profiles...")
    
    generator = AgentProfileGenerator(
        roles_dir='./roles',
        templates_dir='./generators/templates',
        output_dir='./generated'
    )
    
    parser = ProfileParser(Path('./roles'))
    roles = parser.get_all_roles()
    
    generated_count = 0
    for role_slug in roles:
        try:
            output_path = generator.generate_agent_profile(role_slug)
            print(f"   ✅ {role_slug}: {Path(output_path).name}")
            generated_count += 1
        except Exception as e:
            print(f"   ❌ {role_slug}: {e}")
    
    print(f"✅ Generated {generated_count} agent profiles")

def generate_all_career():
    """Generate career ladders for all roles."""
    print("Generating all career ladders...")
    
    generator = CareerLadderGenerator()
    generated_files = generator.generate_all_ladders(include_all_transitions=False)
    
    print(f"✅ Generated {len(generated_files)} career ladders:")
    for name, path in generated_files.items():
        print(f"   - {name}: {path.name}")

def generate_all_artifacts():
    """Generate all artifacts."""
    print("Generating all artifacts...")
    
    # Generate onboarding checklists
    print("\n1. Generating onboarding checklists...")
    onboarding_generator = OnboardingGenerator()
    onboarding_files = onboarding_generator.generate_all_checklists()
    print(f"   ✅ {len(onboarding_files)} onboarding checklists generated")
    
    # Generate career ladders
    print("\n2. Generating career ladders...")
    career_generator = CareerLadderGenerator()
    career_files = career_generator.generate_all_ladders()
    print(f"   ✅ {len(career_files)} career ladders generated")
    
    # Generate agent profiles
    print("\n3. Generating agent profiles...")
    generate_all_agents()
    
    total_files = len(onboarding_files) + len(career_files)
    print(f"\n🎉 Generated {total_files}+ total artifacts!")
    
    # Generate index
    generate_index()

def generate_index():
    """Generate an index of all artifacts."""
    from generators.core import OutputFormatter
    
    print("\n3. Generating artifacts index...")
    formatter = OutputFormatter()
    
    # Discover all generated files
    generated_dir = Path(__file__).parent / 'generated'
    artifacts = {}
    
    for subdir in generated_dir.iterdir():
        if subdir.is_dir():
            artifact_list = [f.name for f in subdir.iterdir() if f.suffix == '.md']
            if artifact_list:
                artifacts[subdir.name] = artifact_list
    
    index_path = formatter.create_index_file(artifacts)
    print(f"   ✅ Index generated: {index_path}")

def list_roles():
    """List all available roles."""
    parser = ProfileParser()
    roles = parser.get_all_roles()
    
    print(f"Available roles ({len(roles)}):")
    for role_slug in roles:
        profile = parser.parse_profile(role_slug)
        if profile:
            print(f"  - {role_slug}: {profile.name} ({profile.default_seniority})")
        else:
            print(f"  - {role_slug}: (failed to parse)")

if __name__ == '__main__':
    main()
