# BombSquad 1.4 魔改服务端

这是一个基于 BombSquad 1.4 脚本体系整理的魔改服务端仓库。

## 仓库定位

- `main`：当前公开维护分支（偏纯净、可发布）
- `legacy`：历史完整魔改分支（保留原始改动）

## 主要特点

- **Coop 关卡播放器**
  - 支持更灵活地加载/游玩 coop 关卡内容。
- **指令系统扩展**
  - 保留了常用管理与玩法指令能力，方便服主管理与调试。
- **特效体系增强**
  - 在不破坏基础玩法的前提下，保留已有视觉特效增强能力。
- **1.4 生态兼容改造**
  - 面向 BombSquad 1.4 服务端脚本环境进行整理与适配。

## 当前 main 分支说明

当前分支已按“更接近原版体验”的方向做了整理：

- 不再默认给玩家戴拳套。
- 不再强制全局感应炸弹（impact）玩法。
- 回归正常“拾取道具”模式。
- 保留 `spazPC` 相关能力；停用 `pcpowerup` 注入式新增道具逻辑。

## CheatCmd 指令总览

> 指令入口：`scripts/cheatCmd.py`（已拆分到多个 `cmd_handlers_*` 模块）

### 1) 社交 / 信息

- `/help`：显示帮助
- `/list`：显示玩家列表（kick 用）
- `/me [clientID]`：查询战绩
- `/top`：积分前十
- `/ego`：个人分数/KD/与上一名差距
- `/contact`：联系信息
- `/tag <text>`：设置个人标签
- `/lm444`：回放最近聊天

### 2) 管理

- `/kick <name|clientID>`：踢人
- `/getlost <name|clientID>`：踢人（别名）
- `/admin <clientID> add|remove`：管理 admin
- `/vip <clientID> add|remove`：管理 vip
- `/member <clientID> add|remove`：管理 member
- `/maxPlayers <count>`：设置人数上限
- `/quit`：退出/关服

### 3) 基础玩法控制

- `/freeze <all|index>`：冻结
- `/thaw <all|index>`：解冻
- `/kill <all|index>`：击杀
- `/heal <all|index|name>`：回血
- `/fly <all|index>`：飞行开关

### 4) 角色 / 战斗效果

- `/curse <all|index|name>`：诅咒
- `/box <all|index|name>`：箱子外观
- `/mine <all|index|name>`：地雷外观
- `/headless <all|index|name>`：无头
- `/shield <all|index|name>`：护盾
- `/celebrate <all|index|name>`：庆祝动作
- `/remove <all|index|name>`：移出游戏
- `/hug <all|indexA indexB>`：抱人
- `/gm [index]`：GM状态切换（invincible/hockey/拳力）
- `/spaz <all|index|name> <character>`：换角色模型
- `/inv <all|index|name>`：隐身（清空模型）
- `/punch [all|index|name]`：给拳套
- `/gift`：随机给道具（shield/punch/curse/health）
- `/shatter <all|index> <value>`：设置碎裂值
- `/sleep <all|index|name>`：击晕
- `/cmr [ms]`：临时地图淡化/镜头特效

### 5) 环境 / 画面 / 音效

- `/ooh [count] [delayMs]`：播放 ooh 音效
- `/playSound <name> [count] [delayMs]`：播放指定音效
- `/nv [off]`：夜视开关
- `/end`：结束对局
- `/tint <r g b>` 或 `/tint r <bright> <speed>`：色调
- `/sm`：慢动作开关
- `/cameraMode`：镜头模式切换
- `/floorReflection`：地面反射开关
- `/ac <r g b>` 或 `/ac r <bright> <speed>`：环境光
- `/iceOff`：关闭冰面效果
- `/reflections <type(1/0)> <scale>`：反射类型/强度
- `/reset`：重置环境参数
- `/disco`：迪斯科灯效
- `/id <index>`：查看目标玩家 profile 列表

## 使用建议

- 想要稳定公开服：使用 `main`
- 想查看或回溯历史魔改：切换到 `legacy`

---
如需二次魔改，建议在 `main` 新建功能分支，便于后续合并与回滚。
