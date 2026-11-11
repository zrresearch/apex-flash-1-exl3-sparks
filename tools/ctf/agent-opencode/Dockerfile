# The Cybench agent image (with Node 22 from the Pi image) plus OpenCode, pinned.
FROM ctf-agent-pi:local
RUN npm install -g opencode-ai@1.19.4 && opencode --version
# No update checks, model catalogue downloads, language-server downloads or sharing: attempts run offline.
ENV OPENCODE_DISABLE_AUTOUPDATE=1 \
    OPENCODE_DISABLE_MODELS_FETCH=1 \
    OPENCODE_DISABLE_LSP_DOWNLOAD=1 \
    OPENCODE_DISABLE_SHARE=1
