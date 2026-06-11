# Dokobot MCP 插件

一键配置 Dokobot MCP 服务器，让 Astrbot 通过真实浏览器搜索网页。

> **关于 Dokobot**：[Dokobot](https://dokobot.ai) 是一个通过真实浏览器读取网页的工具，由 Dokobot 团队开发。本插件是对其 MCP 集成的自动配置工具。

## 功能

- **自动配置**：插件加载时自动在 `mcp_server.json` 中添加 dokobot 配置
- **智能查找**：自动查找 `dokobot-mcp.js` 文件位置
- **状态检查**：使用 `/dokobot状态` 命令查看配置状态

## 前置要求

1. [@dokobot/cli](https://www.npmjs.com/package/@dokobot/cli) 全局安装
   ```bash
   npm install -g @dokobot/cli
   ```

2. Chrome 浏览器 + Dokobot 扩展

3. 本地 bridge 已安装
   ```bash
   dokobot install-bridge
   ```

4. `dokobot-mcp.js` 文件放在以下任一位置：
   - `~/dokobot-mcp.js`
   - `~/AppData/Roaming/npm/node_modules/dokobot-mcp-server/dokobot-mcp.js`

## 使用方法

1. 将插件文件夹放到 `~/.astrbot/data/plugins/`
2. 重启 astrbot
3. 插件会自动配置 MCP 服务器
4. 再次重启 astrbot 使 MCP 生效

## 命令

- `/dokobot状态` - 查看 MCP 配置状态

## 工作原理

插件在 `initialize()` 时会：
1. 检查 `~/.astrbot/data/mcp_server.json`
2. 如果 dokobot 未配置，自动添加配置
3. 自动查找 `dokobot-mcp.js` 文件位置

## 故障排除

如果 MCP 工具不可用：
1. 运行 `/dokobot状态` 检查配置
2. 确认 `dokobot-mcp.js` 文件存在
3. 确认 `@dokobot/cli` 已全局安装
4. 重启 astrbot

## 许可证

MIT
