# Example Sphinx configuration showing how to use sphinx-ai-assistant

# Add extension
extensions = [
    'sphinx_ai_assistant',
]

# HTML theme configuration (using Furo as example)
html_theme = 'furo'

# AI Assistant Configuration
# These are the default values.

# Enable or disable the assistant
ai_assistant_enabled = True

# Where to place the button: 'sidebar' or 'title'
ai_assistant_position = 'sidebar'

# CSS selector for the main content area to convert
# For Furo: 'article'
# Check for other themes
ai_assistant_content_selector = 'article'

# Feature flags
ai_assistant_features = {
    'markdown_export': True,    # Copy to clipboard
    'view_markdown': True,      # View as Markdown in new tab
    'ai_chat': False,           # AI chat integration
    'mcp_integration': False,   # MCP tool installation
}

# Build-time markdown generation from topics
ai_assistant_generate_markdown = True

# Patterns to exclude from markdown generation
ai_assistant_markdown_exclude_patterns = [
    'genindex',
    'search',
    'py-modindex',
    '_sources',  # Exclude source files
]

# llms.txt generation
ai_assistant_generate_llms_txt = True
ai_assistant_base_url = 'https://docs.example.com'  # Or use html_baseurl

# AI provider configuration
ai_assistant_providers = {
    'claude': {
        'enabled': True,
        'label': 'Ask Claude',
        'description': 'Ask Claude about this topic.',
        'icon': 'claude.svg',
        'url_template': 'https://claude.ai/new?q={prompt}',
        'prompt_template': 'Get familiar with the documentation content at {url} so that I can ask questions about it.',
    },
    'chatgpt': {
        'enabled': True,
        'label': 'Ask ChatGPT',
        'description': 'Ask ChatGPT about this topic.',
        'icon': 'chatgpt.svg',
        'url_template': 'https://chatgpt.com/?q={prompt}',
        'prompt_template': 'Get familiar with the documentation content at {url} so that I can ask questions about it.',
    },
    # Example: Custom AI provider
    'custom': {
        'enabled': True,
        'label': 'Ask Perplexity',
        'url_template': 'https://www.perplexity.ai/?q={prompt}',
        'prompt_template': 'Analyze this documentation: {url}',
    },
}

# AI provider fallback configuration in case of content too long for URL embedding
ai_assistant_use_pregenerated_markdown = True
# Number of characters when content is too long for embedding in URL
ai_assistant_max_content_length = 4000

# MCP tools configuration
ai_assistant_mcp_tools = {
    'vscode': {
        'enabled': True,
        'type': 'vscode',
        'label': 'Connect to VS Code',
        'description': 'Install MCP server to VS Code.',
        'icon': 'vscode.svg',
        'server_name': 'your-docs-mcp-server',
        'server_url': 'https://your-docs-mcp-server/sse',
        'transport': 'sse',  # 'sse' or 'stdio'
    },
    'claude_desktop': {
        'enabled': True,
        'type': 'claude_desktop',
        'label': 'Connect to Claude',
        'description': 'Download and run the Claude mcpb.',
        'icon': 'claude.svg',
        'mcpb_url': 'https://docs.example.com/_static/your-mcpb-config.zip',
    },
}