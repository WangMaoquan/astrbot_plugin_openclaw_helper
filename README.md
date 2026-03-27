# OpenClaw Helper

AstrBot 插件，提供危险操作白名单保护功能。

## 简介

该插件用于保护 AstrBot + OpenClaw 组合的安全，检测危险操作并支持白名单机制。

## 功能

- 危险操作检测：检测消息中的危险关键词（内置 + 用户自定义）
- 管理员白名单：只有管理员才能执行危险操作
- 日志记录：记录危险操作检测日志

## 危险关键词

### 内置关键词（不可见）

| 类型 | 关键词 |
|------|--------|
| 文件删除 | 删除、rm、del、drop |
| 系统操作 | exec、sudo、shutdown、reboot |
| 获取敏感信息 | 获取密码、获取token、读取密码等 |
| 网络下载执行 | curl、wget |
| 其他 | format、chmod 777 |

### 用户自定义

可在配置中添加额外关键词。

## 指令

> ⚠️ 以下指令仅管理员可用

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
| admin_ids | 管理员ID，逗号分隔 | 空 |
| dangerous_keywords | 额外添加的危险关键词，逗号分隔 | 空 |
| warning_message | 拦截时的警告消息 | 糖浆风格默认消息 |

## 依赖

- AstrBot >= 4.16

## 作者

wangmaoquan
