"""
Template engine for generating artifacts from role profiles.
"""

from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
from typing import Dict, Any, Optional
import os

class TemplateEngine:
    """Jinja2-based template engine for artifact generation."""
    
    def __init__(self, templates_dir: Path = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / 'templates'
        
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self._register_filters()
        
        # Add global functions
        self._register_globals()
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with the given context."""
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            raise TemplateRenderError(f"Failed to render template {template_name}: {e}")
    
    def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render a template string with the given context."""
        try:
            template = Template(template_string, environment=self.env)
            return template.render(**context)
        except Exception as e:
            raise TemplateRenderError(f"Failed to render template string: {e}")
    
    def template_exists(self, template_name: str) -> bool:
        """Check if a template file exists."""
        template_path = self.templates_dir / template_name
        return template_path.exists()
    
    def list_templates(self, pattern: str = "*.md") -> list:
        """List available templates matching the pattern."""
        import fnmatch
        templates = []
        
        for root, dirs, files in os.walk(self.templates_dir):
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    rel_path = os.path.relpath(os.path.join(root, file), self.templates_dir)
                    templates.append(rel_path.replace(os.sep, '/'))
        
        return sorted(templates)
    
    def _register_filters(self):
        """Register custom Jinja2 filters."""
        
        def title_case(text):
            """Convert text to title case."""
            return ' '.join(word.capitalize() for word in text.replace('-', ' ').replace('_', ' ').split())
        
        def snake_case(text):
            """Convert text to snake_case."""
            return text.lower().replace(' ', '_').replace('-', '_')
        
        def kebab_case(text):
            """Convert text to kebab-case."""
            return text.lower().replace(' ', '-').replace('_', '-')
        
        def bullet_list(items, prefix="- "):
            """Convert list to bullet points."""
            if not items:
                return ""
            return '\n'.join(f"{prefix}{item}" for item in items)
        
        def numbered_list(items, start=1):
            """Convert list to numbered points."""
            if not items:
                return ""
            return '\n'.join(f"{i + start}. {item}" for i, item in enumerate(items))
        
        def checkbox_list(items, checked=False):
            """Convert list to checkbox items."""
            if not items:
                return ""
            marker = "- [x]" if checked else "- [ ]"
            return '\n'.join(f"{marker} {item}" for item in items)
        
        def word_wrap(text, width=80):
            """Wrap text to specified width."""
            import textwrap
            return textwrap.fill(str(text), width=width)
        
        def indent_filter(text, spaces=2):
            """Indent text by specified number of spaces."""
            indent_str = ' ' * spaces
            return '\n'.join(f"{indent_str}{line}" if line.strip() else line 
                           for line in str(text).split('\n'))
        
        def slugify(text):
            """Convert text to URL-safe slug."""
            import re
            text = str(text).lower()
            text = re.sub(r'[^\w\s-]', '', text)
            text = re.sub(r'[-\s]+', '-', text)
            return text.strip('-')

        # Register filters
        self.env.filters['title_case'] = title_case
        self.env.filters['snake_case'] = snake_case
        self.env.filters['kebab_case'] = kebab_case
        self.env.filters['bullet_list'] = bullet_list
        self.env.filters['numbered_list'] = numbered_list
        self.env.filters['checkbox_list'] = checkbox_list
        self.env.filters['word_wrap'] = word_wrap
        self.env.filters['indent'] = indent_filter
        self.env.filters['slugify'] = slugify
    
    def _register_globals(self):
        """Register global template functions."""
        from datetime import datetime
        
        def now(format_str='%Y-%m-%d %H:%M:%S'):
            """Get current timestamp."""
            return datetime.now().strftime(format_str)
        
        # Register globals
        self.env.globals['now'] = now
class TemplateRenderError(Exception):
    """Exception raised when template rendering fails."""
    pass


class TemplateManager:
    """Manages template discovery and organization."""
    
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        
        self.base_dir = base_dir
        self.templates_dir = base_dir / 'templates'
        self.ensure_template_structure()
    
    def ensure_template_structure(self):
        """Ensure the template directory structure exists."""
        template_dirs = [
            'onboarding',
            'career',
            'team',
            'runbooks',
            'common'
        ]
        
        for dir_name in template_dirs:
            dir_path = self.templates_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_template_path(self, generator_type: str, template_name: str) -> Path:
        """Get the full path for a template."""
        return self.templates_dir / generator_type / template_name
    
    def save_template(self, generator_type: str, template_name: str, content: str):
        """Save a template to the appropriate directory."""
        template_path = self.get_template_path(generator_type, template_name)
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def load_template(self, generator_type: str, template_name: str) -> Optional[str]:
        """Load a template from disk."""
        template_path = self.get_template_path(generator_type, template_name)
        
        if not template_path.exists():
            return None
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def list_templates_by_type(self, generator_type: str) -> list:
        """List templates for a specific generator type."""
        type_dir = self.templates_dir / generator_type
        if not type_dir.exists():
            return []
        
        return [f.name for f in type_dir.iterdir() if f.is_file() and f.suffix == '.md']
