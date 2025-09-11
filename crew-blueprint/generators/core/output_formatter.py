"""
Output formatting utilities for generated artifacts.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import re

class OutputFormatter:
    """Handles formatting and saving of generated artifacts."""
    
    def __init__(self, output_dir: Path = None):
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / 'generated'
        
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_artifact(self, content: str, filename: str, 
                     subfolder: str = None, metadata: Dict[str, Any] = None) -> Path:
        """Save generated content to a file with optional metadata."""
        
        # Determine output path
        if subfolder:
            output_path = self.output_dir / subfolder
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = self.output_dir
        
        file_path = output_path / filename
        
        # Add metadata header if provided
        if metadata:
            content = self._add_metadata_header(content, metadata)
        
        # Ensure content is properly formatted
        content = self._format_content(content)
        
        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    def get_output_filename(self, artifact_type: str, role_slug: str, 
                           seniority: str = None, suffix: str = None) -> str:
        """Generate a standardized filename for artifacts."""
        parts = [artifact_type, role_slug]
        
        if seniority:
            parts.append(seniority.lower())
        
        if suffix:
            parts.append(suffix)
        
        filename = '_'.join(parts) + '.md'
        return self._sanitize_filename(filename)
    
    def create_index_file(self, artifacts: Dict[str, list], 
                         index_path: Path = None) -> Path:
        """Create an index file listing all generated artifacts."""
        if index_path is None:
            index_path = self.output_dir / 'INDEX.md'
        
        content = self._generate_index_content(artifacts)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return index_path
    
    def _add_metadata_header(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add a metadata header to the content."""
        header_lines = [
            "---",
            "# Generated Artifact Metadata"
        ]
        
        for key, value in metadata.items():
            header_lines.append(f"# {key}: {value}")
        
        header_lines.extend([
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "---",
            ""
        ])
        
        return '\n'.join(header_lines) + content
    
    def _format_content(self, content: str) -> str:
        """Apply consistent formatting to content."""
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove excessive blank lines (more than 2 consecutive)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Ensure file ends with single newline
        content = content.rstrip() + '\n'
        
        return content
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem compatibility."""
        # Replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Replace multiple underscores with single
        filename = re.sub(r'_{2,}', '_', filename)
        
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        
        return filename
    
    def _generate_index_content(self, artifacts: Dict[str, list]) -> str:
        """Generate content for the artifacts index file."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        content = [
            "# Generated Artifacts Index",
            "",
            f"*Generated: {timestamp}*",
            "",
            "This index contains all artifacts generated from role profiles.",
            ""
        ]
        
        total_artifacts = sum(len(artifact_list) for artifact_list in artifacts.values())
        content.extend([
            "## Summary",
            "",
            f"- **Total Artifacts**: {total_artifacts}",
            f"- **Artifact Types**: {len(artifacts)}",
            ""
        ])
        
        for artifact_type, artifact_list in sorted(artifacts.items()):
            content.extend([
                f"## {artifact_type.title()}",
                "",
                f"*{len(artifact_list)} artifacts*",
                ""
            ])
            
            for artifact in sorted(artifact_list):
                # Extract role and seniority from filename
                base_name = Path(artifact).stem
                parts = base_name.split('_')
                
                if len(parts) >= 3:
                    role = parts[1].replace('-', ' ').title()
                    seniority = parts[2].title() if len(parts) > 2 else ""
                    display_name = f"{role} ({seniority})" if seniority else role
                else:
                    display_name = base_name.replace('_', ' ').title()
                
                content.append(f"- [{display_name}](./{artifact})")
            
            content.append("")
        
        content.extend([
            "---",
            "*Generated by the Role Atlas artifact generation system*"
        ])
        
        return '\n'.join(content)


class ValidationError(Exception):
    """Exception raised when output validation fails."""
    pass


class OutputValidator:
    """Validates generated artifacts for quality and consistency."""
    
    def __init__(self):
        self.validation_rules = {
            'min_length': 100,  # Minimum content length
            'required_sections': [],  # Will be set per artifact type
            'max_line_length': 120,  # Maximum line length
        }
    
    def validate_artifact(self, content: str, artifact_type: str) -> Dict[str, Any]:
        """Validate generated artifact content."""
        issues = []
        warnings = []
        
        # Check minimum length
        if len(content.strip()) < self.validation_rules['min_length']:
            issues.append(f"Content too short: {len(content)} chars (min: {self.validation_rules['min_length']})")
        
        # Check for required sections based on artifact type
        required_sections = self._get_required_sections(artifact_type)
        for section in required_sections:
            if f"# {section}" not in content and f"## {section}" not in content:
                issues.append(f"Missing required section: {section}")
        
        # Check line length
        lines = content.split('\n')
        long_lines = [i + 1 for i, line in enumerate(lines) 
                     if len(line) > self.validation_rules['max_line_length']]
        if long_lines:
            warnings.append(f"Lines exceed max length ({self.validation_rules['max_line_length']}): {long_lines[:5]}")
        
        # Check for empty sections
        empty_sections = self._find_empty_sections(content)
        if empty_sections:
            warnings.append(f"Empty sections found: {empty_sections}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'stats': {
                'length': len(content),
                'lines': len(lines),
                'sections': len(re.findall(r'^#{1,3} ', content, re.MULTILINE))
            }
        }
    
    def _get_required_sections(self, artifact_type: str) -> list:
        """Get required sections for each artifact type."""
        section_requirements = {
            'onboarding': ['Overview', 'Timeline', 'Responsibilities', 'Key Relationships'],
            'career': ['Current State', 'Target State', 'Development Plan', 'Success Metrics'],
            'team': ['Team Composition', 'Roles & Responsibilities', 'Communication Patterns'],
            'runbook': ['Procedures', 'Monitoring', 'Escalation', 'Common Issues']
        }
        
        return section_requirements.get(artifact_type, [])
    
    def _find_empty_sections(self, content: str) -> list:
        """Find sections that appear to be empty or have minimal content."""
        empty_sections = []
        lines = content.split('\n')
        
        current_section = None
        section_content = []
        
        for line in lines:
            if re.match(r'^#{1,3} ', line):
                # Check previous section
                if current_section and len(' '.join(section_content).strip()) < 20:
                    empty_sections.append(current_section)
                
                # Start new section
                current_section = line.strip('#').strip()
                section_content = []
            else:
                section_content.append(line.strip())
        
        # Check last section
        if current_section and len(' '.join(section_content).strip()) < 20:
            empty_sections.append(current_section)
        
        return empty_sections
