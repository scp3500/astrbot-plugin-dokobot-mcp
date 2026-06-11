"""Dokobot MCP 自动配置插件 - 一键启用 dokobot 网页搜索"""

import json
import os
from pathlib import Path

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star


class DokobotMCPPlugin(Star):
    def __init__(self, context: Context, config: dict | None = None):
        super().__init__(context)

    async def initialize(self):
        """插件加载时自动配置 MCP"""
        mcp_config_path = Path.home() / ".astrbot" / "data" / "mcp_server.json"

        try:
            if mcp_config_path.exists():
                with open(mcp_config_path, "r", encoding="utf-8") as f:
                    mcp_config = json.load(f)
            else:
                mcp_config = {"mcpServers": {}}

            if "dokobot" not in mcp_config.get("mcpServers", {}):
                # 自动查找 dokobot-mcp.js 位置
                possible_paths = [
                    str(Path.home() / "dokobot-mcp.js"),
                    str(Path.home() / "AppData/Roaming/npm/node_modules/dokobot-mcp-server/dokobot-mcp.js"),
                ]

                dokobot_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        dokobot_path = path
                        break

                if not dokobot_path:
                    logger.warning(
                        "[dokobot-mcp] 未找到 dokobot-mcp.js，请手动创建或安装 dokobot-mcp-server"
                    )
                    return

                mcp_config["mcpServers"]["dokobot"] = {
                    "command": "node",
                    "args": [dokobot_path],
                    "env": {}
                }

                mcp_config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(mcp_config_path, "w", encoding="utf-8") as f:
                    json.dump(mcp_config, f, indent=2, ensure_ascii=False)

                logger.info(f"[dokobot-mcp] 已自动配置 MCP 服务器: {dokobot_path}")
                logger.info("[dokobot-mcp] 请重启 astrbot 使配置生效")
            else:
                logger.info("[dokobot-mcp] MCP 服务器已配置")

        except Exception as e:
            logger.error(f"[dokobot-mcp] 配置失败: {e}")

    @filter.command("dokobot状态")
    async def check_status(self, event: AstrMessageEvent):
        """检查 dokobot MCP 配置状态"""
        mcp_config_path = Path.home() / ".astrbot" / "data" / "mcp_server.json"

        if not mcp_config_path.exists():
            yield event.plain_result("MCP 配置文件不存在")
            return

        with open(mcp_config_path, "r", encoding="utf-8") as f:
            mcp_config = json.load(f)

        dokobot_config = mcp_config.get("mcpServers", {}).get("dokobot")

        if dokobot_config:
            path = dokobot_config.get("args", [""])[0]
            exists = "✓ 存在" if os.path.exists(path) else "✗ 文件不存在"
            yield event.plain_result(
                f"Dokobot MCP 状态:\n"
                f"配置状态: 已配置\n"
                f"文件路径: {path}\n"
                f"文件状态: {exists}"
            )
        else:
            yield event.plain_result("Dokobot MCP 未配置")
