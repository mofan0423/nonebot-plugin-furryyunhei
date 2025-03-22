import json

from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import httpx
from nonebot.plugin import PluginMetadata
from nonebot import get_plugin_config

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-furryyunhei",
    description="接入 梦梦 的furry云黑api，群内查询云黑",
    usage="/查云黑 [QQ号]或/yunhei [QQ号]",
    type="application",
    homepage="https://github.com/mofan0423/nonebot-plugin-furryyunhei",
    supported_adapters={"~onebot.v11"},
)

furryyunhei = on_command("查云黑", aliases={"yunhei"}, priority=10, block=True)

api_key = get_plugin_config(Config)

@furryyunhei.handle()
async def handle_function(args: Message = CommandArg()):
    location = args.extract_plain_text().strip()
    if not location:
        await furryyunhei.finish("请输入要查询的QQ号。")
        return

    url = 'http://yunhei.qimeng.fun:12301/OpenAPI.php'
    key = api_key.yunhei_api_key  # 使用从配置中读取的API密钥
    params = {'id': location, 'key': key}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data2 = response.json()

            if 'info' in data2 and isinstance(data2['info'], list) and len(data2['info']) > 0:
                info = data2['info'][0]
                yh = info.get('yh')
                type_ = info.get('type')
                note = info.get('note', '')
                admin = info.get('admin', '')
                level = info.get('level', '')
                date = info.get('date', '')

                if yh == 'false':
                    if type_ == 'none':
                        return_ = '账号暂无云黑，请谨慎甄别！'
                    elif type_ == 'bilei':
                        return_ = f'账号暂无云黑，请谨慎甄别！\n此账号有避雷/前科记录。\n备注：{note}\n上黑等级：{level}\n上黑时间：{date}\n登记管理员：{admin}\n'
                    else:
                        return_ = '未知类型，请检查数据源。'
                elif yh == 'true':
                    return_ = f'此为云黑账号，请停止一切交易！\n备注：{note}\n上黑等级：{level}\n上黑时间：{date}\n登记管理员：{admin}'
                else:
                    return_ = '未知状态，请检查数据源。'
                await furryyunhei.finish(return_)
            else:
                await furryyunhei.finish("未找到有效的信息条目，请检查数据源。")

        except httpx.RequestError as e:
            await furryyunhei.finish(f"请求失败: {e}")
        except json.JSONDecodeError as e:
            await furryyunhei.finish(f"JSON解析失败: {e}")
