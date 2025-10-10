# Example Sphinx configuration showing how to use sphinx-ai-assistant

project = 'Example Documentation'
copyright = '2025, Your Name'
author = 'Your Name'

# Add extensions
extensions = [
    'sphinx_ai_assistant',
]

# HTML theme configuration (using Furo as example)
html_theme = 'furo'

# AI Assistant Configuration
# These are the default values - you can customize them

# Enable or disable the assistant
ai_assistant_enabled = True

# Where to place the button: 'sidebar' or 'title'
ai_assistant_position = 'sidebar'

# CSS selector for the main content area to convert
# For Furo: 'article' works well
# For other themes, you may need to adjust
ai_assistant_content_selector = 'article'

# Feature flags
ai_assistant_features = {
    'markdown_export': True,
    'ai_chat': False,        # Phase 2 - not yet implemented
    'mcp_integration': False, # Phase 3 - not yet implemented
}
