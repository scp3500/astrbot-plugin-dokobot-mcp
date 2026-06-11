#!/bin/bash
# GitHub 初始化脚本

# 1. 初始化 git
git init
git add .
git commit -m "Initial commit: Dokobot MCP auto-config plugin for Astrbot"

# 2. 添加远程仓库（记得先在 GitHub 创建仓库）
git remote add origin https://github.com/scp3500/astrbot-plugin-dokobot-mcp.git

# 3. 推送
git branch -M main
git push -u origin main

echo "✓ 推送完成！"
echo "插件地址: https://github.com/scp3500/astrbot-plugin-dokobot-mcp"
