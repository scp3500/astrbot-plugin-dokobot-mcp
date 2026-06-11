# Dokobot MCP 插件

一键配置 Dokobot MCP 服务器，让 Astrbot 通过真实浏览器搜索网页。

> **关于 Dokobot**：[Dokobot](https://dokobot.ai) 是一个通过真实浏览器读取网页的工具，由 Dokobot 团队开发。本插件是对其 MCP 集成的自动配置工具。

## 功能

- **全自动安装**：插件加载时自动安装 `dokobot-mcp-server` npm 包（无需手动操作）
- **自动配置**：自动在 `mcp_server.json` 中添加 dokobot 配置
- **智能查找**：自动查找 npm 全局安装目录
- **状态检查**：使用 `/dokobot状态` 命令查看配置状态

## 前置要求

**仅需要用户手动安装的**：

1. [@dokobot/cli](https://www.npmjs.com/package/@dokobot/cli) 全局安装
   ```bash
   npm install -g @dokobot/cli
   ```

2. Chrome 浏览器安装 [Dokobot 扩展](https://dokobot.ai)

3. 本地 bridge 安装
   ```bash
   dokobot install-bridge
   ```

**插件会自动完成的**：
- ✓ 安装 `dokobot-mcp-server` npm 包
- ✓ 查找 `dokobot-mcp.js` 文件路径
- ✓ 配置 `mcp_server.json`

## 使用方法

1. 将插件文件夹放到 `~/.astrbot/data/plugins/`
2. 重启 astrbot
3. 插件会自动下载并配置（首次加载可能需要几分钟）
4. 再次重启 astrbot 使 MCP 生效

## 命令

- `/dokobot状态` - 查看 MCP 配置状态和 npm 包安装情况

## 工作原理

插件在 `initialize()` 时会：
1. 运行 `npm install -g dokobot-mcp-server` 安装 MCP 服务器
2. 查找 npm 全局安装目录中的 `dokobot-mcp.js` 文件
3. 自动写入 `~/.astrbot/data/mcp_server.json` 配置

## 故障排除

如果 MCP 工具不可用：
1. 运行 `/dokobot状态` 检查安装和配置状态
2. 确认 `@dokobot/cli` 已全局安装：`npm list -g @dokobot/cli`
3. 确认 bridge 已安装：`dokobot list`
4. 重启 astrbot

如果 npm 安装失败，可以手动安装：
```bash
npm install -g dokobot-mcp-server
```
然后重启 astrbot，插件会自动检测已安装的包。

## 许可证

MIT

