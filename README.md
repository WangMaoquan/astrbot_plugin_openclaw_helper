# OpenClaw Helper

AstrBot plugin for maintaining session continuity with OpenClaw.

## Description

This plugin hooks into LLM requests and adds user/group identifiers to maintain independent conversation sessions for each user or group.

## Features

- Automatically adds user ID to LLM requests for private chats
- Automatically adds group ID to LLM requests for group chats
- Maintains separate conversation history per user/group

## How It Works

When AstrBot sends a request to OpenClaw's Chat API, this plugin intercepts the request and adds a `user` parameter:

- Private chat: `user: "<qq_number>"`
- Group chat: `user: "group_<group_number>"`

This allows OpenClaw to maintain separate conversation sessions for each user and group.

## Installation

1. Copy this plugin folder to your AstrBot plugins directory
2. Restart AstrBot
3. Enable the plugin in AstrBot admin panel

## Configuration

| Option | Description | Default |
|--------|-------------|---------|
| user_id_prefix | Prefix for user ID | `group_` |
| enabled | Enable/disable plugin | `true` |

## Requirements

- AstrBot >= 4.16
- OpenClaw with Chat Completions API enabled

## Author

wangmaoquan
