/**
 * Sphinx AI Assistant
 * 
 * Provides AI-powered features for Sphinx documentation pages.
 * Phase 1: Markdown export functionality
 */

(function() {
    'use strict';
    
    // Load Turndown library from CDN
    function loadTurndown(callback) {
        if (typeof TurndownService !== 'undefined') {
            callback();
            return;
        }
        
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/turndown@7.1.2/dist/turndown.min.js';
        script.onload = callback;
        script.onerror = function() {
            console.error('Failed to load Turndown library');
        };
        document.head.appendChild(script);
    }
    
    // Initialize the AI assistant when DOM is ready
    function initAIAssistant() {
        loadTurndown(function() {
            createAIAssistantUI();
        });
    }
    
    // Create the AI assistant UI
    function createAIAssistantUI() {
        const container = createContainer();
        const button = createButton();
        const dropdown = createDropdown();
        
        container.appendChild(button);
        container.appendChild(dropdown);
        
        // Insert into the appropriate location based on configuration
        const position = window.AI_ASSISTANT_CONFIG?.position || 'sidebar';
        insertContainer(container, position);
        
        // Setup event listeners
        setupEventListeners(button, dropdown);
    }
    
    // Create the main container
    function createContainer() {
        const container = document.createElement('div');
        container.className = 'ai-assistant-container';
        container.id = 'ai-assistant-container';
        return container;
    }
    
    // Create the trigger button
    function createButton() {
        const button = document.createElement('button');
        button.className = 'ai-assistant-button';
        button.id = 'ai-assistant-button';
        button.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 16v-4"></path>
                <path d="M12 8h.01"></path>
            </svg>
            <span>AI Assistant</span>
        `;
        button.setAttribute('aria-label', 'AI Assistant');
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('aria-haspopup', 'true');
        return button;
    }
    
    // Create the dropdown menu
    function createDropdown() {
        const dropdown = document.createElement('div');
        dropdown.className = 'ai-assistant-dropdown';
        dropdown.id = 'ai-assistant-dropdown';
        dropdown.setAttribute('role', 'menu');
        dropdown.style.display = 'none';
        
        const features = window.AI_ASSISTANT_CONFIG?.features || { markdown_export: true };
        
        if (features.markdown_export) {
            const exportItem = createMenuItem(
                'copy-markdown',
                'Copy as Markdown',
                'Copy this page content as Markdown'
            );
            dropdown.appendChild(exportItem);
        }
        
        return dropdown;
    }
    
    // Create a menu item
    function createMenuItem(id, text, title) {
        const item = document.createElement('button');
        item.className = 'ai-assistant-menu-item';
        item.id = `ai-assistant-${id}`;
        item.textContent = text;
        item.title = title;
        item.setAttribute('role', 'menuitem');
        return item;
    }
    
    // Insert container into the appropriate location
    function insertContainer(container, position) {
        if (position === 'sidebar') {
            // For Furo theme, insert at the top of the right sidebar
            const sidebar = document.querySelector('.sidebar-drawer, aside.sidebar-secondary, .toc-drawer');
            if (sidebar) {
                sidebar.insertBefore(container, sidebar.firstChild);
                return;
            }
        }
        
        // Fallback: insert at the top-right of the article container
        const article = document.querySelector('article, .document, .body');
        if (article) {
            article.insertBefore(container, article.firstChild);
        }
    }
    
    // Setup event listeners
    function setupEventListeners(button, dropdown) {
        // Toggle dropdown
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const isOpen = dropdown.style.display !== 'none';
            dropdown.style.display = isOpen ? 'none' : 'block';
            button.setAttribute('aria-expanded', !isOpen);
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!button.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.style.display = 'none';
                button.setAttribute('aria-expanded', 'false');
            }
        });
        
        // Handle menu item clicks
        const copyMarkdownBtn = document.getElementById('ai-assistant-copy-markdown');
        if (copyMarkdownBtn) {
            copyMarkdownBtn.addEventListener('click', handleCopyMarkdown);
        }
    }
    
    // Handle copy as markdown
    function handleCopyMarkdown() {
        const contentSelector = window.AI_ASSISTANT_CONFIG?.content_selector || 'article';
        const content = document.querySelector(contentSelector);
        
        if (!content) {
            alert('Could not find page content to convert');
            return;
        }
        
        // Clone the content to avoid modifying the original
        const clonedContent = content.cloneNode(true);
        
        // Remove elements we don't want in the markdown
        const elementsToRemove = [
            '.headerlink',
            '.ai-assistant-container',
            'script',
            'style',
            '.sidebar',
            'nav'
        ];
        
        elementsToRemove.forEach(selector => {
            clonedContent.querySelectorAll(selector).forEach(el => el.remove());
        });
        
        // Convert to markdown using Turndown
        const turndownService = new TurndownService({
            headingStyle: 'atx',
            codeBlockStyle: 'fenced',
            emDelimiter: '*',
        });
        
        // Add custom rules if needed
        turndownService.addRule('preserveCodeBlocks', {
            filter: ['pre'],
            replacement: function(content, node) {
                const code = node.querySelector('code');
                if (code) {
                    const language = code.className.match(/language-(\w+)/);
                    const lang = language ? language[1] : '';
                    return '\n\n```' + lang + '\n' + code.textContent + '\n```\n\n';
                }
                return '\n\n```\n' + content + '\n```\n\n';
            }
        });
        
        const markdown = turndownService.turndown(clonedContent.innerHTML);
        
        // Copy to clipboard
        copyToClipboard(markdown);
        
        // Close dropdown
        document.getElementById('ai-assistant-dropdown').style.display = 'none';
        document.getElementById('ai-assistant-button').setAttribute('aria-expanded', 'false');
    }
    
    // Copy text to clipboard
    function copyToClipboard(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function() {
                showNotification('Markdown copied to clipboard!');
            }).catch(function(err) {
                console.error('Failed to copy to clipboard:', err);
                fallbackCopy(text);
            });
        } else {
            fallbackCopy(text);
        }
    }
    
    // Fallback copy method for older browsers
    function fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        
        try {
            document.execCommand('copy');
            showNotification('Markdown copied to clipboard!');
        } catch (err) {
            console.error('Fallback copy failed:', err);
            showNotification('Failed to copy to clipboard', true);
        }
        
        document.body.removeChild(textarea);
    }
    
    // Show notification
    function showNotification(message, isError = false) {
        const notification = document.createElement('div');
        notification.className = 'ai-assistant-notification' + (isError ? ' error' : '');
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Trigger animation
        setTimeout(() => notification.classList.add('show'), 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAIAssistant);
    } else {
        initAIAssistant();
    }
    
})();
