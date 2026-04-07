# BombSquad Pure Mod (v10.9.3 coop2027)

基于：`scripts-patched-v10.9.3-coop2027-wingsfix-utf8-from-v10.9.0.zip`

## 分支说明

- `legacy`：原始导入版本（完整历史魔改内容）
- `main`：纯净魔改版（面向公开仓库）

## main 分支改动目标

- 去掉拳套（`punch`）道具效果
- 去掉拳套随机掉落
- 保留现有特效逻辑
- 保留魔改 coop 关卡播放器

## 当前已做

1. `scripts/bsPowerup.py`
   - 从默认随机道具分布中移除 `punch`
2. `scripts/bsSpaz.py`
   - 屏蔽 `punch` 道具应用逻辑（即使意外拿到，也不会生效）

> 注：该仓库用于“纯净发布向”整理；若后续你要进一步剥离更多自定义道具入口（UI/指令/隐藏触发），可继续在 `main` 分支追加清理。
