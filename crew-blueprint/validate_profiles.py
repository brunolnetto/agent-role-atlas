#!/usr/bin/env python3
"""
Role Profile Validator

Validates YAML frontmatter in role profile.md files against the JSON Schema.
Usage: python validate_profiles.py [role_path]
"""

import json
import yaml
import jsonschema
import sys
import os
from pathlib import Path

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from a Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---\n'):
        raise ValueError(f"File {file_path} does not start with YAML frontmatter")
    
    # Find the end of frontmatter
    end_marker = content.find('\n---\n', 4)
    if end_marker == -1:
        raise ValueError(f"File {file_path} does not have properly closed YAML frontmatter")
    
    frontmatter = content[4:end_marker]
    return yaml.safe_load(frontmatter)

def load_schema():
    """Load the JSON Schema for role profiles."""
    schema_path = Path(__file__).parent / 'schema.json'
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_profile(profile_path):
    """Validate a single profile against the schema."""
    try:
        frontmatter = extract_frontmatter(profile_path)
        schema = load_schema()
        
        jsonschema.validate(frontmatter, schema)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) > 1:
        profile_path = sys.argv[1]
        if os.path.isfile(profile_path):
            profiles = [profile_path]
        else:
            # Assume it's a role directory
            profiles = [os.path.join(profile_path, 'profile.md')]
    else:
        # Find all profile.md files in roles directory
        roles_dir = Path(__file__).parent / 'roles'
        profiles = list(roles_dir.glob('*/profile.md'))
    
    print("🔍 Validating role profiles...")
    print("=" * 50)
    
    valid_count = 0
    total_count = 0
    
    for profile_path in profiles:
        total_count += 1
        is_valid, error = validate_profile(profile_path)
        
        role_name = Path(profile_path).parent.name
        if is_valid:
            print(f"✅ {role_name}: VALID")
            valid_count += 1
        else:
            print(f"❌ {role_name}: INVALID")
            print(f"   Error: {error}")
    
    print("=" * 50)
    print(f"📊 Summary: {valid_count}/{total_count} profiles valid")
    
    if valid_count == total_count:
        print("🎉 All profiles are valid!")
        sys.exit(0)
    else:
        print("⚠️  Some profiles need attention")
        sys.exit(1)

if __name__ == '__main__':
    main()
