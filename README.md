<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-furryyunhei

_✨ NoneBot 插件 furry云黑查询插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/mofan0423/nonebot-plugin-furryyunhei.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-furryyunhei">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-furryyunhei.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>


## 📖 介绍

基于 幻梦 的趣绮梦云黑api开发的相对应的nonebot插件
申请api请联系 幻梦QQ1137889900

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-furryyunhei

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-furryyunhei
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-furryyunhei
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-furryyunhei
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-furryyunhei
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_furryyunhei"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| yunhei_api_key | 是 | 无 | APIKEY,必填 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| /查云黑 [QQ号]或/yunhei [QQ号] | 群员 | 否 | 不限 | 查询云黑 |
