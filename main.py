import aiohttp
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

# services/oss.py
import oss2
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import requests
from alibabacloud_openapi_util.client import Client as util
from Tea.request import TeaRequest

import os

accessKeyId = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
accessKeySecret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
securityToken = None

bucket_name = 'winjava21'
region = 'oss-cn-hangzhou'  # Bucket 所在区域

class OSSClient:
    def __init__(self):
        endpoint = f"https://{region}.aliyuncs.com"
        auth = oss2.Auth(accessKeyId, accessKeySecret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)


    def get_signed_url(self, local_path, remote_name, expire=3600):
        remote_name = str(remote_name)
        self.bucket.put_object_from_file(remote_name, local_path)
        return self.bucket.sign_url("GET", remote_name, expire)


    def download(self, local_path, remote_name):
        self.bucket.get_object_to_file(remote_name, local_path)


class FcClient:
    def __init__(self):
        method = 'POST'
        url = 'https://enkacard-qsspclkjbz.ap-southeast-1.fcapp.run'  # 你的HTTP触发器地址
        date = datetime.utcnow().isoformat('T')[:19] + 'Z'
        headers = {
            'x-acs-date': date,
            'x-acs-security-token': securityToken
        }
        self.headers = headers
        self.url = url
        parsedUrl = urlparse(url)
        authRequest = TeaRequest()
        authRequest.method = method
        authRequest.pathname = parsedUrl.path.replace('$', '%24')
        authRequest.headers = headers
        authRequest.query = {k: v[0] for k, v in parse_qs(parsedUrl.query).items()}
        auth = util.get_authorization(authRequest, 'ACS3-HMAC-SHA256', '', accessKeyId, accessKeySecret)
        headers['authorization'] = auth


    def card(self, uid: str, character_id: str):
        body = {
            "uid": uid,
            "character_id": character_id
        }
        resp = requests.post(self.url, json=body, headers=self.headers)
        return resp.json()

idAvatarMap = {
    10000001: '凯特',
    10000002: '神里绫华',
    10000003: '琴',
    10000005: '主角',
    10000006: '丽莎',
    10000007: '主角',
    10000014: '芭芭拉',
    10000015: '凯亚',
    10000016: '迪卢克',
    10000020: '雷泽',
    10000021: '安柏',
    10000022: '温迪',
    10000023: '香菱',
    10000024: '北斗',
    10000025: '行秋',
    10000026: '魈',
    10000027: '凝光',
    10000029: '可莉',
    10000030: '钟离',
    10000031: '菲谢尔',
    10000032: '班尼特',
    10000033: '达达利亚',
    10000034: '诺艾尔',
    10000035: '七七',
    10000036: '重云',
    10000037: '甘雨',
    10000038: '阿贝多',
    10000039: '迪奥娜',
    10000041: '莫娜',
    10000042: '刻晴',
    10000043: '砂糖',
    10000044: '辛焱',
    10000045: '罗莎莉亚',
    10000046: '胡桃',
    10000047: '枫原万叶',
    10000048: '烟绯',
    10000049: '宵宫',
    10000050: '托马',
    10000051: '优菈',
    10000052: '雷电将军',
    10000053: '早柚',
    10000054: '珊瑚宫心海',
    10000055: '五郎',
    10000056: '九条裟罗',
    10000057: '荒泷一斗',
    10000058: '八重神子',
    10000059: '鹿野院平藏',
    10000060: '夜兰',
    10000062: '埃洛伊',
    10000063: '申鹤',
    10000064: '云堇',
    10000065: '久岐忍',
    10000066: '神里绫人',
    10000067: '柯莱',
    10000068: '多莉',
    10000069: '提纳里',
    10000070: '妮露',
    10000071: '赛诺',
    10000072: '坎蒂丝',
    10000073: '纳西妲',
    10000075: '流浪者',
    10000078: '艾尔海森',
    10000079: '迪希雅',
    10000082: '白术',
    10000084: '林尼',
    10000086: '莱欧斯利',
    10000087: '那维莱特',
    10000089: '芙宁娜',
    10000091: '娜维娅',
    10000093: '闲云',
    10000094: '千织',
    10000095: '希格雯',
    10000096: '阿蕾奇诺',
    10000098: '克洛琳德',
    10000099: '艾梅莉埃',
    10000101: '基尼奇',
    10000102: '玛拉妮',
    10000103: '希诺宁',
    10000104: '恰斯卡',
    10000106: '玛薇卡',
    10000107: '茜特菈莉',
    10000109: '梦见月瑞希',
    10000111: '瓦蕾莎',
    10000112: '爱可菲',
    10000114: '丝柯克',
    10000116: '伊涅芙',
    10000119: '菈乌玛',
    10000120: '菲林斯',
    10000123: '杜林'
}

idEnergyMap = {
    1: "火",
    2: "水",
    3: "草",
    4: "雷",
    5: "冰",
    6: "岩",
    7: "风"
}
status_codes = {
    400: "UID格式错误",
    404: "玩家不存在",
    424: "游戏维护中",
    429: "请求频率限制",
    500: "服务器错误",
    503: "出现了莫名奇妙的错误"
}
pick = {
    "size": True,
    "get_characters": True,
    "add_characters": True,
    "add_generate": True,
    "get_generate": True
}


async def fetch_json(uid):
    url = f"https://enka.network/api/uid/{uid}"  # 替换为你的真实 API 地址
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=20) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                elif resp.status == 400:
                    return "UID似乎不正确"
    except Exception:
        return "莫名奇妙的错误"


async def list_roles(uid):
    data = await fetch_json(uid)
    info_list = data.get("playerInfo", {}).get("showAvatarInfoList", [])
    s = "\n"
    id_list = []
    for i, x in enumerate(info_list):
        name = idAvatarMap.get(x["avatarId"], f"未知{x['avatarId']}")
        lvl = x.get("level")
        elem = idEnergyMap.get(x.get("energyType"), "未知")
        id_list.append(x["avatarId"])
        s += f"{i+1}. {name} 元素：{elem} 等级：{lvl}\n"
    return s


async def generate_card(uid, num):
    data = await fetch_json(uid)
    fc = FcClient()
    try:
        num = int(num)
        avatar_id = str(data.get("playerInfo").get("showAvatarInfoList")[num - 1].get("avatarId"))
    except IndexError:
        return "序号错误"
    # async with encbanner.ENC(uid=uid, character_id=str(avatar_id), lang="chs", pickle = pick) as encard:
    #     c = await encard.creat()
    #     for d in c.card:
    #         filename = f"{uid}_{d.id}.png"
    #         d.card.save(filename)
    #         oss_client = OSSClient()
    #         signed_url = oss_client.get_signed_url(filename, avatar_id)
    #         return signed_url
    return fc.card(uid, avatar_id).get(f"{uid}_{avatar_id}")


async def get_uid_info(uid):
    data = await fetch_json(uid)

    if "playerInfo" not in data:
        return "查询失败，可能是 UID 不存在或未公开。"

    info = data.get("playerInfo")
    name = info.get("nickname", "None")
    level = info.get("level", "None")
    world_level = info.get("worldLevel", "None")
    floor = info.get("towerFloorIndex", None)
    chamber = info.get("towerLevelIndex", None)
    star = info.get("towerStarIndex", None)

    if floor is None:
        abyss_str = "无记录"
    else:
        abyss_str = f"{floor}-{chamber} {star}★"

    act = info.get("theaterActIndex", None)
    star2 = info.get("theaterStarIndex", None)

    if act is None:
        theater_str = "无记录"
    else:
        theater_str = f"{act}|{star2}"

    return (
        f"\n{name}\n"
        f"UID：{uid}\n"
        f"冒险等级：{level}  世界等级：{world_level}\n"
        f"深境螺旋：{abyss_str}\n"
        f"幻想真境剧诗：{theater_str}"
    )


@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    # @filter.command("helloworld")
    # async def helloworld(self, event: AstrMessageEvent):
    #     """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
    #     user_name = event.get_sender_name()
    #     message_str = event.message_str # 用户发的纯文本消息字符串
    #     message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
    #     logger.info(message_chain)
    #     yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息
    @filter("玩家")
    async def player(self, event: AstrMessageEvent):
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        parts = message_str.split(" ")
        yield event.chain_result(await get_uid_info(parts[1]) if len(parts) == 2 else "格式：/uid uid")

    @filter("角色")
    async def character(self, event: AstrMessageEvent):
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        parts = message_str.split(" ")
        if len(parts) == 2:
            yield event.chain_result(await list_roles(parts[1]))
        elif len(parts) == 3:
            yield event.image_result(await generate_card(parts[1], parts[2]))
        else:
            yield event.chain_result("格式：/角色 uid 或 /角色 uid 序号")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""