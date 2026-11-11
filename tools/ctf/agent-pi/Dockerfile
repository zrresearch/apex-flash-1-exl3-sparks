# Pi agent for Cybench: the same image as the Codex agent (Kali, task tools, answers removed) plus Node 22 and Pi.
FROM ctf-agent:local
ARG NODE_VERSION=22.20.0
ARG PI_VERSION=1.4.0
RUN curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz" -o /tmp/node.tar.xz && \
    tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1 --exclude CHANGELOG.md --exclude LICENSE --exclude README.md && \
    rm /tmp/node.tar.xz && node --version && \
    npm install -g --ignore-scripts "@earendil-works/pi-coding-agent@${PI_VERSION}" && pi --version
ENV PI_OFFLINE=1
