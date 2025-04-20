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
    config=Config,
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

    url = 'https://fz.qimeng.fun/OpenAPI/all_f.php?id=123456789&key=my_key'
    key = api_key.yunhei_api_key  # 使用从配置中读取的API密钥
    params = {'id': location, 'key': key}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data2 = response.json()

            if 'info' in data2 and isinstance(data2['info'], list) and len(data2['info']) > 0:
                # 拆分三个信息块（原结构为包含三个对象的数组）
                basic_info, activity_info, black_info = data2['info']
                
                # 提取各部分字段
                user = basic_info.get('user', '')
                tel = basic_info.get('tel', '')
                wx = basic_info.get('wx', '')
                zfb = basic_info.get('zfb', '')
                shiming = basic_info.get('shiming', '')
                
                group_num = activity_info.get('group_num', '')
                m_send_num = activity_info.get('m_send_num', '')
                send_num = activity_info.get('send_num', '')
                first_send = activity_info.get('first_send', '')
                last_send = activity_info.get('last_send', '')
                
                yh = black_info.get('yh', '')
                type_ = black_info.get('type', '')
                note = black_info.get('note', '')
                admin = black_info.get('admin', '')
                level = black_info.get('level', '')
                date = black_info.get('date', '')

                # 处理数据（wx zfb tel shiming）
                if wx == 'false':
                    wxzt = '未绑定'
                elif wx == 'true':
                    wxzt = '已绑定'
                if tel == 'false':
                    telzt = '未绑定'
                elif tel == 'true':
                    telzt = '已绑定'
                if shiming == 'false':
                    shimingzt = '未实名'  # 修改变量名避免覆盖
                elif shiming == 'true':
                    shimingzt = '已实名'
                if zfb == 'false':
                    zfbzt = '未绑定'
                elif zfb == 'true':
                    zfbzt = '已绑定'

                if yh == 'false':
                    if type_ == 'none':
                        return_ = f'账号:{user}暂无云黑，请谨慎甄别！\n\n云存储认证信息及活跃度信息：\n电话：{telzt}\n微信认证：{wxzt}\n支付宝认证：{zfbzt}\n实名：{shimingzt}\n累计加群(含有梦梦的群)：{group_num}\n月活数量/累计发送：{m_send_num}/{send_num}\n首次消息发送时间：{first_send}\n最后消息发送时间：{last_send}\n'
                    elif type_ == 'bilei':
                        return_ = f'账号:{user}暂无云黑，请谨慎甄别！\n此账号有避雷/前科记录。\n备注：{note}\n上黑等级：{level}\n上黑时间：{date}\n登记管理员：{admin}\n\n云存储认证信息及活跃度信息：电话：{telzt}，微信认证：{wxzt}，支付宝认证：{zfbzt}\n实名：{shimingzt}\n累计加群(含有梦梦的群)：{group_num}\n月活数量/累计发送：{m_send_num}/{send_num}\n首次消息发送时间：{first_send}\n最后消息发送时间：{last_send}\n'
                    else:
                        return_ = '未知类型，请检查数据源或自行登录fz.qimeng.fun查询。'
                elif yh == 'true':
                    return_ = f'{user}为云黑账号，请停止一切交易！\n备注：{note}\n上黑等级：{level}\n上黑时间：{date}\n登记管理员：{admin}\n\n云存储认证信息及活跃度信息：电话：{telzt}，微信认证：{wxzt}，支付宝认证：{zfbzt}\n实名：{shimingzt}\n累计加群(含有梦梦的群)：{group_num}\n月活数量/累计发送：{m_send_num}/{send_num}\n首次消息发送时间：{first_send}\n最后消息发送时间：{last_send}\n'
                else:
                    return_ = f'未知状态，请检查数据源及控制台报错和日志。返回值{data2}'
                await furryyunhei.finish(return_)
            else:
                await furryyunhei.finish("未找到有效的信息条目，请检查数据源及控制台报错和日志。")
        except httpx.HTTPError as e:
            await furryyunhei.finish(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError:
            await furryyunhei.finish("API响应无法解析为JSON，请检查服务器返回内容。")
