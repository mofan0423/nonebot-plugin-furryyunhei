from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import requests
import json
import os
from nonebot.plugin import PluginMetadata
from dotenv import load_dotenv, find_dotenv


__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-furryyunhei",
    description="接入 梦梦 的furry云黑api，群内查询云黑",
    usage="/查云黑 [QQ号]或/yunhei [QQ号]",
    type="application",
    homepage="{项目主页}",
    supported_adapters={"~onebot.v11"},
)



furryyunhei = on_command("查云黑", aliases={"yunhei"}, priority=10, block=True)
load_dotenv(verbose=True)
@furryyunhei.handle()
async def handle_function(args: Message = CommandArg()):
    location = args.extract_plain_text().strip()

    if not location:
        await furryyunhei.finish("请输入要查询的QQ号。")
        return

    url = 'http://yunhei.qimeng.fun:12301/OpenAPI.php'
    KEY = os.getenv("YUNHEIAPIKEY")
    parms = {'id': location, 'key': KEY}

    try:
        back = requests.get(url, params=parms)
        back.raise_for_status() 
        data2 = back.json() 
        
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
                    return_ = f'账号暂无云黑，请谨慎甄别！此账号有避雷/前科记录。备注：{note}，上黑等级：{level}，上黑时间：{date}，登记管理员：{admin}'
                else:
                    return_ = '未知类型，请检查数据源。'
            elif yh == 'true':
                return_ = f'备注：{note}，上黑等级：{level}，上黑时间：{date}，登记管理员：{admin}'
            else:
                return_ = '未知状态，请检查数据源。'
            
            await furryyunhei.finish(return_)
        else:
            await furryyunhei.finish("未找到有效的信息条目，请检查数据源。")
    except requests.exceptions.RequestException as e:
        await furryyunhei.finish(f"请求失败: {e}")
    except json.JSONDecodeError as e:
        await furryyunhei.finish(f"JSON解析失败: {e}")
