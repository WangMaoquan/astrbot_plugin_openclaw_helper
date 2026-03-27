# OpenClaw Helper

AstrBot 插件，用于保持与 OpenClaw 的会话连续性。

## 简介

该插件通过拦截 LLM 请求，添加用户/群组标识符来维护独立的对话会话。

## 功能

- 私聊时自动将用户 QQ 号添加到 LLM 请求
- 群聊时自动将群号添加到 LLM 请求
- 为每个用户/群聊维护独立的对话历史

## 工作原理

当 AstrBot 向 OpenClaw 的 Chat API 发送请求时，本插件会拦截请求并添加 `user` 参数：

- 私聊：`user: "<QQ号>"`
- 群聊：`user: "group_<群号>"`

这样 OpenClaw 就可以为每个用户和群聊维护独立的对话会话。

## 安装

1. 将插件文件夹复制到 AstrBot 插件目录
2. 重启 AstrBot
3. 在 AstrBot 管理面板中启用插件

## 配置

| 选项 | 说明 | 默认值 |
|------|------|--------|
| user_id_prefix | 用户 ID 前缀 | `group_` |
| enabled | 启用/禁用插件 | `true` |

## 依赖

- AstrBot >= 4.16
- 已启用 Chat Completions API 的 OpenClaw

## 作者

wangmaoquan
