# Sphinx AI Assistant

A Sphinx extension that adds AI-powered features to documentation pages, making it easier to use your documentation with AI tools.

## Features

### Phase 1: Markdown Export ✅
- **Copy as Markdown**: Convert any documentation page to Markdown format with a single click
- Perfect for pasting into ChatGPT, Claude, or other AI tools
- Preserves code blocks, headings, links, and formatting
- Clean conversion that removes navigation, headers, and other non-content elements

### Coming Soon
- **Phase 2**: Direct AI chat integration (open ChatGPT/Claude with pre-filled context)
- **Phase 3**: MCP (Model Context Protocol) integration for seamless AI tool connections

## Installation

### Using pip

```bash
pip install sphinx-ai-assistant
```

### Development Installation

```bash
git clone https://github.com/yourusername/sphinx-ai-assistant.git
cd sphinx-ai-assistant
pip install -e .
```

## Usage

### Basic Setup

1. Add the extension to your `conf.py`:

```python
extensions = [
    # ... your other extensions
    'sphinx_ai_assistant',
]
```

2. Build your documentation:

```bash
sphinx-build -b html docs/ docs/_build/html
```

That's it! The AI Assistant button will now appear on every page.

### Configuration

You can customize the extension in your `conf.py`:

```python
# Enable or disable the extension (default: True)
ai_assistant_enabled = True

# Button position: 'sidebar' or 'title' (default: 'sidebar')
# 'sidebar': Places button in the right sidebar (above TOC in Furo)
# 'title': Places button near the page title
ai_assistant_position = 'sidebar'

# CSS selector for content to convert (default: 'article')
# For Furo theme, you might want: 'article'
# For other themes, adjust as needed
ai_assistant_content_selector = 'article'

# Enable/disable specific features (default: as shown)
ai_assistant_features = {
    'markdown_export': True,
    'ai_chat': False,        # Coming in Phase 2
    'mcp_integration': False, # Coming in Phase 3
}
```

### Theme Compatibility

Currently optimized for:
- ✅ **Furo** - Full support with sidebar integration

The extension should work with other themes but may require CSS adjustments. Support for more themes will be added in future releases.

## How It Works

### Markdown Conversion

When you click "Copy as Markdown":

1. The extension identifies the main content area of the page
2. Removes non-content elements (navigation, headers, footers, etc.)
3. Converts the HTML to clean Markdown using [Turndown.js](https://github.com/mixmark-io/turndown)
4. Copies the result to your clipboard
5. Shows a confirmation notification

The converted Markdown includes:
- All text content
- Headings (with proper ATX-style formatting)
- Code blocks (with language syntax highlighting preserved)
- Links and images
- Lists and tables
- Block quotes

## Examples

### Using with AI Tools

After copying a page as Markdown, you can paste it into:

**ChatGPT/Claude:**
```
Here's the documentation for [feature]:

[paste markdown here]

Can you help me understand how to use this?
```

**Cursor/VS Code:**
```
# Context from docs

[paste markdown here]

# Question
How do I implement this in my project?
```

## Development

### Project Structure

```
sphinx-ai-assistant/
├── sphinx_ai_assistant/
│   ├── __init__.py          # Main extension module
│   └── static/
│       ├── ai-assistant.js   # JavaScript functionality
│       └── ai-assistant.css  # Styling
├── pyproject.toml            # Package configuration
└── README.md                 # This file
```

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests (when added)
pytest
```

### Building Documentation

```bash
cd docs/
sphinx-build -b html . _build/html
```

## Contributing

Contributions are welcome! This is a young project and there are many ways to help:

- Report bugs or suggest features via [GitHub Issues](https://github.com/yourusername/sphinx-ai-assistant/issues)
- Improve documentation
- Add support for more Sphinx themes
- Help with Phase 2 and 3 features

## Roadmap

- [x] **Phase 1**: Markdown export functionality
- [ ] **Phase 2**: AI chat integration
  - Direct links to ChatGPT/Claude with pre-filled context
  - Custom AI chat URL configuration
  - Context optimization for token limits
- [ ] **Phase 3**: MCP integration
  - Auto-generate MCP server configurations
  - Deep links for Cursor, VS Code, Claude Desktop
  - Documentation context injection

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Turndown.js](https://github.com/mixmark-io/turndown) for HTML to Markdown conversion
- Designed to work seamlessly with the [Furo](https://github.com/pradyunsg/furo) Sphinx theme
- Inspired by the need to make documentation more AI-friendly

## Questions or Issues?

- Check the [documentation](https://github.com/yourusername/sphinx-ai-assistant)
- Open an [issue](https://github.com/yourusername/sphinx-ai-assistant/issues)
- Start a [discussion](https://github.com/yourusername/sphinx-ai-assistant/discussions)