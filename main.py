"""Dokobot MCP 自动配置插件 - 一键启用 dokobot 网页搜索"""

import asyncio
import json
import os
import subprocess
from pathlib import Path

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star


class DokobotMCPPlugin(Star):
    def __init__(self, context: Context, config: dict | None = None):
        super().__init__(context)

    async def _run_command(self, cmd: list[str], timeout: int = 300) -> tuple[bool, str]:
        """运行命令"""
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            output = stdout.decode("utf-8", errors="ignore") + stderr.decode("utf-8", errors="ignore")
            return proc.returncode == 0, output
        except Exception as e:
            return False, str(e)

    async def _install_npm_package(self) -> bool:
        """安装 npm 包"""
        logger.info("[dokobot-mcp] 检查 dokobot-mcp-server...")

        # 检查是否已安装
        success, _ = await self._run_command(["npm", "list", "-g", "dokobot-mcp-server"], timeout=10)
        if success:
            logger.info("[dokobot-mcp] dokobot-mcp-server 已安装")
            return True

        logger.info("[dokobot-mcp] 正在安装 dokobot-mcp-server（可能需要几分钟）...")
        success, output = await self._run_command(["npm", "install", "-g", "dokobot-mcp-server"])

        if success:
            logger.info("[dokobot-mcp] dokobot-mcp-server 安装成功")
            return True
        else:
            logger.error(f"[dokobot-mcp] npm 包安装失败: {output}")
            return False

    def _find_dokobot_mcp_js(self) -> str | None:
        """查找 dokobot-mcp.js 文件"""
        possible_paths = [
            str(Path.home() / "dokobot-mcp.js"),
            str(Path.home() / "AppData/Roaming/npm/node_modules/dokobot-mcp-server/dokobot-mcp.js"),
        ]

        # Windows npm 全局路径
        try:
            result = subprocess.run(
                ["npm", "root", "-g"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                npm_global = result.stdout.strip()
                possible_paths.insert(0, str(Path(npm_global) / "dokobot-mcp-server" / "dokobot-mcp.js"))
        except Exception:
            pass

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    async def initialize(self):
        """插件加载时自动安装并配置"""
        try:
            # 1. 安装 npm 包
            if not await self._install_npm_package():
                logger.warning("[dokobot-mcp] npm 包安装失败，请手动运行: npm install -g dokobot-mcp-server")
                return

            # 2. 查找 MCP 文件
            dokobot_path = self._find_dokobot_mcp_js()
            if not dokobot_path:
                logger.warning(
                    "[dokobot-mcp] 未找到 dokobot-mcp.js，请检查 npm 全局安装目录"
                )
                return

            # 3. 配置 MCP
            mcp_config_path = Path.home() / ".astrbot" / "data" / "mcp_server.json"

            if mcp_config_path.exists():
                with open(mcp_config_path, "r", encoding="utf-8") as f:
                    mcp_config = json.load(f)
            else:
                mcp_config = {"mcpServers": {}}

            if "dokobot" not in mcp_config.get("mcpServers", {}):
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
            logger.error(f"[dokobot-mcp] 初始化失败: {e}")

    @filter.command("dokobot状态")
    async def check_status(self, event: AstrMessageEvent):
        """检查 dokobot MCP 配置状态"""
        mcp_config_path = Path.home() / ".astrbot" / "data" / "mcp_server.json"

        lines = ["Dokobot MCP 状态:\n"]

        # 检查 npm 包
        success, output = await self._run_command(["npm", "list", "-g", "dokobot-mcp-server"], timeout=10)
        if success:
            lines.append("✓ npm 包: 已安装")
        else:
            lines.append("✗ npm 包: 未安装")

        # 检查 MCP 配置
        if not mcp_config_path.exists():
            lines.append("✗ MCP 配置: 不存在")
            yield event.plain_result("\n".join(lines))
            return

        with open(mcp_config_path, "r", encoding="utf-8") as f:
            mcp_config = json.load(f)

        dokobot_config = mcp_config.get("mcpServers", {}).get("dokobot")

        if dokobot_config:
            path = dokobot_config.get("args", [""])[0]
            exists = os.path.exists(path)
            lines.append(f"✓ MCP 配置: 已配置")
            lines.append(f"文件路径: {path}")
            lines.append(f"文件状态: {'✓ 存在' if exists else '✗ 不存在'}")
        else:
            lines.append("✗ MCP 配置: 未配置")

        yield event.plain_result("\n".join(lines))

