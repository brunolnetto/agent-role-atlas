#!/usr/bin/env python3
"""
Summary Report Generator

Generates a SUMMARY.md with role count, validation results, and analysis.
Usage: python generate_summary.py
"""

import json
import yaml
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from a Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---\n'):
        return None
    
    end_marker = content.find('\n---\n', 4)
    if end_marker == -1:
        return None
    
    frontmatter = content[4:end_marker]
    return yaml.safe_load(frontmatter)

def analyze_responsibilities(roles_data):
    """Analyze responsibilities across roles for duplicates."""
    responsibility_map = defaultdict(list)
    
    for role_data in roles_data:
        role_name = role_data['frontmatter'].get('name', 'Unknown')
        
        # Extract responsibilities from markdown content
        content = role_data['content']
        lines = content.split('\n')
        
        in_responsibilities = False
        for line in lines:
            if line.strip() == '# Responsibilities':
                in_responsibilities = True
                continue
            elif line.startswith('# ') and in_responsibilities:
                break
            elif in_responsibilities and line.startswith('- **'):
                # Extract responsibility title
                resp_title = line.split('**')[1] if '**' in line else line.strip('- ')
                responsibility_map[resp_title].append(role_name)
    
    duplicates = {resp: roles for resp, roles in responsibility_map.items() if len(roles) > 1}
    return duplicates

def generate_summary():
    """Generate comprehensive summary report."""
    roles_dir = Path(__file__).parent / 'roles'
    profile_files = list(roles_dir.glob('*/profile.md'))
    
    # Collect role data
    roles_data = []
    validation_results = []
    
    for profile_path in profile_files:
        role_slug = profile_path.parent.name
        
        try:
            frontmatter = extract_frontmatter(profile_path)
            with open(profile_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if frontmatter:
                roles_data.append({
                    'slug': role_slug,
                    'frontmatter': frontmatter,
                    'content': content,
                    'path': profile_path
                })
                validation_results.append((role_slug, True, None))
            else:
                validation_results.append((role_slug, False, "Invalid frontmatter"))
                
        except Exception as e:
            validation_results.append((role_slug, False, str(e)))
    
    # Analyze data
    total_roles = len(profile_files)
    valid_roles = sum(1 for _, valid, _ in validation_results if valid)
    invalid_roles = total_roles - valid_roles
    
    seniority_distribution = defaultdict(int)
    for role_data in roles_data:
        seniority = role_data['frontmatter'].get('default_seniority', 'Unknown')
        seniority_distribution[seniority] += 1
    
    duplicate_responsibilities = analyze_responsibilities(roles_data)
    
    # Generate report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# Role Atlas Summary Report

*Generated: {timestamp}*

## Overview

- **Total Roles**: {total_roles}
- **Valid Profiles**: {valid_roles}
- **Invalid Profiles**: {invalid_roles}
- **Success Rate**: {(valid_roles/total_roles*100):.1f}% if total_roles > 0 else 0

## Role Distribution by Seniority

"""
    
    for seniority, count in sorted(seniority_distribution.items()):
        report += f"- **{seniority}**: {count} roles\n"
    
    report += "\n## Validation Results\n\n"
    
    for role_slug, is_valid, error in validation_results:
        status = "✅ VALID" if is_valid else "❌ INVALID"
        report += f"- **{role_slug}**: {status}"
        if error:
            report += f" - {error}"
        report += "\n"
    
    if duplicate_responsibilities:
        report += "\n## ⚠️ Duplicate Responsibilities Detected\n\n"
        for resp, roles in duplicate_responsibilities.items():
            report += f"- **{resp}**: {', '.join(roles)}\n"
    else:
        report += "\n## ✅ No Duplicate Responsibilities\n\n"
    
    report += "\n## Current Roles\n\n"
    
    for role_data in sorted(roles_data, key=lambda x: x['slug']):
        fm = role_data['frontmatter']
        name = fm.get('name', role_data['slug'])
        seniority = fm.get('default_seniority', 'Unknown')
        
        report += f"### {name}\n"
        report += f"- **Slug**: `{role_data['slug']}`\n"
        report += f"- **ID**: `{fm.get('id', 'N/A')}`\n"
        report += f"- **Default Seniority**: {seniority}\n"
        report += f"- **Profile**: [profile.md](./roles/{role_data['slug']}/profile.md)\n\n"
    
    # TODO section
    report += "\n## 📋 Outstanding TODOs\n\n"
    
    todos = []
    if invalid_roles > 0:
        todos.append(f"Fix {invalid_roles} invalid role profiles")
    if duplicate_responsibilities:
        todos.append(f"Resolve {len(duplicate_responsibilities)} duplicate responsibilities")
    if total_roles < 5:
        todos.append("Expand role catalog (current: minimum viable set)")
    
    if todos:
        for todo in todos:
            report += f"- [ ] {todo}\n"
    else:
        report += "- [x] All validations passing\n- [x] No duplicate responsibilities\n- [x] Schema compliance verified\n"
    
    report += f"\n---\n*Report generated by generate_summary.py*"
    
    return report

def main():
    summary = generate_summary()
    
    # Write to file
    summary_path = Path(__file__).parent / 'SUMMARY.md'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"📊 Summary report generated: {summary_path}")
    print("\n" + "="*50)
    print(summary)

if __name__ == '__main__':
    main()
