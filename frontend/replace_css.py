import re

with open('styles/main.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update variables
css = re.sub(
    r':root \{.*?\n\}',
    ''':root {
    color-scheme: dark;
    --bg-main: #06080d;
    --bg-surface: #0c1017;
    --bg-surface-strong: #161b22;
    --bg-panel: #0d1117;
    --border-color: rgba(255, 255, 255, 0.1);
    --border-strong: rgba(255, 255, 255, 0.2);
    --border-soft: rgba(255, 255, 255, 0.05);
    --text-primary: #e6edf3;
    --text-secondary: #848d97;
    --text-muted: #6b7280;
    --accent: #2f81f7;
    --cyan: #2f81f7;
    --blue: #2f81f7;
    --pink: #e6edf3;
    --green: #2ea043;
    --amber: #d29922;
    --red: #f85149;
    --shadow-soft: 0 4px 12px rgba(0, 0, 0, 0.15);
    --shadow-panel: 0 8px 24px rgba(0, 0, 0, 0.2);
    --shadow-focus: 0 0 0 2px rgba(47, 129, 247, 0.4);
    --shadow-elevated: 0 16px 32px rgba(0, 0, 0, 0.4);
}''',
    css,
    flags=re.DOTALL
)

# 2. Update body background
css = re.sub(
    r'html,\s*body \{.*?\n\}',
    '''html,
body {
    min-height: 100dvh;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg-main);
    color: var(--text-primary);
    overflow-x: hidden;
    overflow-y: auto;
}''',
    css,
    flags=re.DOTALL
)

# 3. Remove .bg-orb and .bg-grid
css = re.sub(r'\.bg-orb \{.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'\.orb-one \{.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'\.orb-two \{.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'\.bg-grid \{.*?\n\}', '', css, flags=re.DOTALL)

# 4. Remove .app-container::before
css = re.sub(r'\.app-container::before \{.*?\n\}', '', css, flags=re.DOTALL)

# 5. Remove backdrop-filter
css = re.sub(r'\.sidebar,\s*\.workspace-header,\s*\.chat-stage,\s*\.composer-box \{\s*backdrop-filter:[^}]+\}\s*', '', css)

# 6. Update sidebar background
css = re.sub(
    r'\.sidebar \{([^}]+)\}',
    r'.sidebar {\1}',
    css
)
css = re.sub(
    r'background:\s*linear-gradient[^;]+;',
    'background: var(--bg-surface);',
    css
)

# Fix .btn-new-chat
css = re.sub(
    r'\.btn-new-chat \{([^}]+)\}',
    '''.btn-new-chat {
    width: 100%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 12px 16px;
    color: var(--bg-main);
    background: var(--text-primary);
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: var(--shadow-soft);
}''',
    css
)
# Fix .send-btn
css = re.sub(
    r'\.send-btn \{([^}]+)\}',
    '''.send-btn {
    color: var(--bg-main);
    background: var(--text-primary);
    box-shadow: var(--shadow-soft);
}''',
    css
)

# Remove @keyframes gradient-shift
css = re.sub(r'@keyframes gradient-shift \{.*?\}\s*', '', css, flags=re.DOTALL)

# Fix .workspace-header
css = re.sub(
    r'\.workspace-header \{.*?\n\}',
    '''.workspace-header {
    position: relative;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    box-shadow: var(--shadow-soft);
}''',
    css,
    flags=re.DOTALL
)
# Remove workspace-header::after
css = re.sub(r'\.workspace-header::after \{.*?\n\}', '', css, flags=re.DOTALL)

# Fix .chat-stage
css = re.sub(
    r'\.chat-stage \{.*?\n\}',
    '''.chat-stage {
    position: relative;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    border-radius: 12px;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-soft);
    overflow: hidden;
}''',
    css,
    flags=re.DOTALL
)
css = re.sub(r'\.chat-stage::before,\s*\.chat-stage::after \{.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'\.chat-stage::before \{.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'\.chat-stage::after \{.*?\n\}', '', css, flags=re.DOTALL)

# Remove @keyframes float-gradient and drift-orb
css = re.sub(r'@keyframes float-gradient \{.*?\}\s*', '', css, flags=re.DOTALL)
css = re.sub(r'@keyframes drift-orb \{.*?\}\s*', '', css, flags=re.DOTALL)

# Fix panel-block, panel-card background
css = re.sub(
    r'\.panel-block,\s*\.panel-card,\s*\.hero-stat-card,\s*\.status-card,\s*\.trust-item,\s*\.executive-card \{.*?\n\}',
    '''.panel-block,
.panel-card,
.hero-stat-card,
.status-card,
.trust-item,
.executive-card {
    position: relative;
    background: var(--bg-surface-strong);
    border-radius: 12px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-soft);
    overflow: hidden;
}''',
    css,
    flags=re.DOTALL
)
css = re.sub(r'\.panel-block::before,[^{]+\{.*?\}\s*', '', css, flags=re.DOTALL)

# Fix msg-content background
css = re.sub(
    r'\.msg-content \{.*?\n\}',
    '''.msg-content {
    flex: 1;
    min-width: 0;
    border-radius: 12px;
    padding: 16px 18px;
    line-height: 1.72;
    background: var(--bg-surface-strong);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-soft);
}''',
    css,
    flags=re.DOTALL
)

css = re.sub(
    r'\.bot-msg \.msg-content \{.*?\n\}',
    '''.bot-msg .msg-content {
    background: var(--bg-surface);
}''',
    css,
    flags=re.DOTALL
)

css = re.sub(
    r'\.user-msg \.msg-content \{.*?\n\}',
    '''.user-msg .msg-content {
    background: var(--bg-surface-strong);
    border-color: var(--border-strong);
}''',
    css,
    flags=re.DOTALL
)

css = re.sub(
    r'\.intro-card \{.*?\n\}',
    '''.intro-card {
    background: var(--bg-surface);
}''',
    css,
    flags=re.DOTALL
)

css = re.sub(
    r'\.nura-avatar \{.*?\n\}',
    '''.nura-avatar {
    background: var(--bg-surface-strong);
    border: 1px solid var(--border-color);
}''',
    css,
    flags=re.DOTALL
)

# Fix ghost-action
css = re.sub(
    r'\.ghost-action \{.*?\n\}',
    '''.ghost-action {
    min-height: 40px;
    padding: 0 16px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--bg-surface-strong);
    color: var(--text-primary);
    cursor: pointer;
    font-size: 0.9rem;
}''',
    css,
    flags=re.DOTALL
)
css = re.sub(
    r'\.ghost-action\.primary \{.*?\n\}',
    '''.ghost-action.primary {
    color: var(--bg-main);
    background: var(--text-primary);
    border-color: transparent;
}''',
    css,
    flags=re.DOTALL
)

# Fix composer-box
css = re.sub(
    r'\.composer-box \{.*?\n\}',
    '''.composer-box {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    border-radius: 12px;
    padding: 10px;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-panel);
}''',
    css,
    flags=re.DOTALL
)

with open('styles/main.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS updated successfully")
