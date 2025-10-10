"""
Sphinx AI Assistant Extension

A Sphinx extension that adds AI assistant features to documentation pages,
including markdown conversion, AI chat integration, and MCP support.
"""

from pathlib import Path
from typing import Any, Dict
from sphinx.application import Sphinx


def setup(app: Sphinx) -> Dict[str, Any]:
    """
    Setup function for the Sphinx extension.
    
    Args:
        app: The Sphinx application instance
        
    Returns:
        Extension metadata
    """
    # Add configuration values
    app.add_config_value('ai_assistant_enabled', True, 'html')
    app.add_config_value('ai_assistant_position', 'sidebar', 'html')  # 'sidebar' or 'title'
    app.add_config_value('ai_assistant_content_selector', 'article', 'html')
    app.add_config_value('ai_assistant_features', {
        'markdown_export': True,
        'ai_chat': False,  # Phase 2
        'mcp_integration': False,  # Phase 3
    }, 'html')
    
    # Get the path to our static files
    static_path = Path(__file__).parent / 'static'
    app.config.html_static_path.append(str(static_path))
    
    # Add our CSS and JS files
    app.add_css_file('ai-assistant.css')
    app.add_js_file('ai-assistant.js')
    
    # Connect to the appropriate event to inject our HTML
    app.connect('html-page-context', add_ai_assistant_context)
    
    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


def add_ai_assistant_context(app: Sphinx, pagename: str, templatename: str, 
                             context: Dict, doctree) -> None:
    """
    Add AI assistant context to the page template context.
    
    This function is called for each page being rendered and adds
    the necessary context variables for the AI assistant dropdown.
    """
    if not app.config.ai_assistant_enabled:
        return
    
    # Add configuration to the page context
    context['ai_assistant_config'] = {
        'position': app.config.ai_assistant_position,
        'content_selector': app.config.ai_assistant_content_selector,
        'features': app.config.ai_assistant_features,
    }
