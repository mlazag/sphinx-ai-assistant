"""
Sphinx AI Assistant Extension

A Sphinx extension that adds AI assistant features to documentation pages,
including markdown conversion, AI chat integration, and MCP support.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
    from markdownify import MarkdownConverter
    HAS_MARKDOWN_DEPS = True
except ImportError:
    HAS_MARKDOWN_DEPS = False


class SphinxMarkdownConverter(MarkdownConverter):
    """
    Custom converter that handles Sphinx-specific elements better
    """
    def convert_code(self, el, text=None, convert_as_inline=False, **options):
        """Handle code blocks with language info"""
        if text is None:
            text = el.get_text()

        classes = el.get('class', [])
        language = ''
        for cls in classes:
            if cls.startswith('highlight-'):
                language = cls.replace('highlight-', '')
                break

        if not convert_as_inline and language:
            return f'\n```{language}\n{text}```\n'
        return f'`{text}`' if text else ''

    def convert_div(self, el, text=None, convert_as_inline=False, **options):
        """Handle Sphinx admonitions"""
        if text is None:
            text = el.get_text()

        classes = el.get('class', [])
        if 'admonition' in classes:
            title = el.find('p', class_='admonition-title')
            if title:
                title_text = title.get_text()
                # Remove title from content
                title.decompose()
                content = el.get_text().strip()
                return f'\n> **{title_text}**\n> {content}\n'
        return text if text else ''

    def convert_pre(self, el, text=None, convert_as_inline=False, **options):
        """Handle pre blocks"""
        if text is None:
            text = el.get_text()

        # Check if this is a code block
        code = el.find('code')
        if code:
            return self.convert_code(code, code.get_text(), False)
        return f'\n```\n{text}```\n' if text else ''


def html_to_markdown_converter(html_content):
    """Convert HTML content to markdown using custom converter"""
    return SphinxMarkdownConverter(
        heading_style='ATX',
        bullets='*',
        strong_em_symbol='**',
        strip=['script', 'style']
    ).convert(html_content)


def generate_markdown_files(app: Sphinx, exception):
    """
    Post-build hook to generate .md files for each .html file
    """
    if exception is not None:
        return

    builder = app.builder
    if not isinstance(builder, StandaloneHTMLBuilder):
        return

    # Check if markdown generation is enabled
    if not app.config.ai_assistant_generate_markdown:
        logger.info('AI Assistant: Markdown generation disabled')
        return

    if not HAS_MARKDOWN_DEPS:
        logger.warning('AI Assistant: Cannot generate markdown files. Install dependencies: pip install beautifulsoup4 markdownify')
        return

    outdir = Path(builder.outdir)
    exclude_patterns = app.config.ai_assistant_markdown_exclude_patterns

    # Get list of HTML files
    html_files = list(outdir.rglob('*.html'))
    generated_count = 0
    skipped_count = 0

    logger.info(f'AI Assistant: Generating markdown files for {len(html_files)} HTML files...')

    for html_file in html_files:
        # Check if file should be excluded
        rel_path = html_file.relative_to(outdir)
        if any(pattern in str(rel_path) for pattern in exclude_patterns):
            skipped_count += 1
            continue

        try:
            # Read HTML
            html_content = html_file.read_text(encoding='utf-8')

            # Extract main content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Try different selectors based on common Sphinx themes
            selectors = [
                'article[role="main"]',   # Furo theme
                'div[role="main"]',       # Many themes
                'div.document',           # Classic theme
                'main',                   # Generic HTML5
                'div.body',               # Older themes
            ]

            main_content = None
            for selector in selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            if not main_content:
                logger.warning(f'AI Assistant: Could not find main content in {rel_path}')
                skipped_count += 1
                continue

            # Convert to markdown
            markdown_content = html_to_markdown_converter(str(main_content))

            # Write .md file alongside .html
            md_file = html_file.with_suffix('.md')
            md_file.write_text(markdown_content, encoding='utf-8')

            generated_count += 1

        except Exception as e:
            logger.warning(f'AI Assistant: Failed to generate markdown for {rel_path}: {e}')
            skipped_count += 1

    logger.info(f'AI Assistant: Generated {generated_count} markdown files, skipped {skipped_count}')


def generate_llms_txt(app: Sphinx, exception):
    """Generate llms.txt with all markdown URLs"""
    if exception is not None:
        return

    if not app.config.ai_assistant_generate_markdown:
        return

    if not app.config.ai_assistant_generate_llms_txt:
        return

    builder = app.builder
    if not isinstance(builder, StandaloneHTMLBuilder):
        return

    outdir = Path(builder.outdir)
    base_url = app.config.html_baseurl or app.config.ai_assistant_base_url or ''

    # Get all markdown files
    md_files = sorted(outdir.rglob('*.md'))

    if not md_files:
        return

    llms_txt = outdir / 'llms.txt'
    with llms_txt.open('w', encoding='utf-8') as f:
        f.write(f"# {app.config.project} Documentation\n\n")
        f.write(f"This file lists all available documentation pages in markdown format.\n")
        f.write(f"Generated by sphinx-ai-assistant extension.\n\n")

        for md_file in md_files:
            rel_path = md_file.relative_to(outdir)
            if base_url:
                url = f"{base_url.rstrip('/')}/{str(rel_path).replace(os.sep, '/')}"
            else:
                url = str(rel_path).replace(os.sep, '/')
            f.write(f"{url}\n")

    logger.info(f'AI Assistant: Generated llms.txt with {len(md_files)} pages')


def setup(app: Sphinx) -> Dict[str, Any]:
    """
    Setup function for the Sphinx extension.

    Args:
        app: The Sphinx application instance

    Returns:
        Extension metadata
    """
    # Enabling extension
    app.add_config_value('ai_assistant_enabled', True, 'html')
    app.add_config_value('ai_assistant_position', 'sidebar', 'html')
    app.add_config_value('ai_assistant_content_selector', 'article', 'html')

    # Markdown generation
    app.add_config_value('ai_assistant_generate_markdown', True, 'html')
    app.add_config_value('ai_assistant_markdown_exclude_patterns',
                         ['genindex', 'search', 'py-modindex'], 'html')
    app.add_config_value('ai_assistant_generate_llms_txt', True, 'html')
    app.add_config_value('ai_assistant_base_url', '', 'html')

    # Enabling extension options
    app.add_config_value('ai_assistant_features', {
        'markdown_export': True,
        'view_markdown': True,
        'ai_chat': True,
        'mcp_integration': True,
    }, 'html')

    # AI provider configuration
    app.add_config_value('ai_assistant_providers', {
        'claude': {
            'enabled': True,
            'label': 'Ask Claude',
            'description': 'Open AI chat with this page context',
            'icon': 'claude.svg',
            'url_template': 'https://claude.ai/new?q={prompt}',
            'prompt_template': 'Hi! Please read this documentation page: {url}\n\nI have questions about it.',
        },
        'chatgpt': {
            'enabled': True,
            'label': 'Ask ChatGPT',
            'description': 'Open AI chat with this page context',
            'icon': 'chatgpt.svg',
            'url_template': 'https://chatgpt.com/?q={prompt}',
            'prompt_template': 'Read {url} so I can ask questions about it.',
        },
        'custom': {
            'enabled': False,
            'label': 'Custom AI',
            'description': 'Open AI chat with this page context',
            'icon': 'comment-discussion.svg',
            'url_template': 'https://your-ai.com/chat?q={prompt}',
            'prompt_template': 'Read {url} and answer my questions about it.',
        }
    }, 'html')

    # Fallback configuration
    app.add_config_value('ai_assistant_use_pregenerated_markdown', True, 'html')
    app.add_config_value('ai_assistant_max_content_length', 4000, 'html')

    # MCP tools configuration
    app.add_config_value('ai_assistant_mcp_tools', {
        'vscode': {
            'enabled': False,
            'type': 'vscode',
            'label': 'Connect to VS Code',
            'description': 'Install MCP server in VS Code',
            'icon': 'vscode.svg',
            'server_name': '',
            'server_url': '',
            'transport': 'sse',
        },
        'claude_desktop': {
            'enabled': False,
            'type': 'claude_desktop',
            'label': 'Connect to Claude',
            'description': 'Download and install MCP extension',
            'icon': 'claude.svg',
            'mcpb_url': '',
        },
    }, 'html')

    # Get the path to our static files
    static_path = Path(__file__).parent / 'static'
    app.config.html_static_path.append(str(static_path))

    # Add our CSS and JS files
    app.add_css_file('ai-assistant.css')
    app.add_js_file('ai-assistant.js')

    # Connect to events
    app.connect('html-page-context', add_ai_assistant_context)
    app.connect('build-finished', generate_markdown_files)
    app.connect('build-finished', generate_llms_txt)

    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': False,
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
    config = {
        'position': app.config.ai_assistant_position,
        'content_selector': app.config.ai_assistant_content_selector,
        'features': app.config.ai_assistant_features,
        'providers': app.config.ai_assistant_providers,
        'mcp_tools': app.config.ai_assistant_mcp_tools,
        'usePreGeneratedMarkdown': app.config.ai_assistant_use_pregenerated_markdown,
        'maxContentLength': app.config.ai_assistant_max_content_length,
        'baseUrl': app.config.html_baseurl or app.config.ai_assistant_base_url or '',
    }

    context['ai_assistant_config'] = config

    # Inject configuration as inline script for JavaScript access
    if 'metatags' not in context:
        context['metatags'] = ''

    config_script = f'''
<script>
window.AI_ASSISTANT_CONFIG = {json.dumps(config)};
</script>
'''

    context['metatags'] += config_script