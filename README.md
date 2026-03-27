# OpenClaw Helper

AstrBot 插件，提供危险操作白名单保护功能。

## 简介

该插件用于保护 AstrBot + OpenClaw 组合的 安全，检测危险操作并支持白名单机制。

## 功能

- 危险操作检测：检测消息中的危险关键词
- 白名单管理：通过命令添加/移除白名单用户
- 日志记录：记录危险操作检测日志

## 工作原理

当 AstrBot 向 OpenClaw 发送 LLM 请求时，插件会检测消息内容是否包含危险关键词：

- 危险关键词：删除、rm、exec、sudo、shutdown 等
- 白名单用户不受限制
- 非白名单用户的危险操作会被记录

## 指令

| 指令 | 说明 |
|------|------|
| `/whitelist` | 查看当前白名单 |
| `/whitelist add <user_id>` | 添加用户到白名单 |
| `/whitelist remove <user_id>` | 从白名单移除用户 |
| `/whitelist list` | 查看白名单列表 |

## 安装

1. 将插件文件夹复制到 AstrBot 插件目录
2. 重启 AstrBot
3. 在 AstrBot 管理面板中启用插件

## 配置

| 选项 | 说明 | 默认值 |
|------|------|--------|
| enabled | 启用/禁用插件 | `true` |

## 依赖

- AstrBot >= 4.16

## 作者

wangmaoquan
