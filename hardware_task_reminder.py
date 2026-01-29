import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import datetime
import os

WEBHOOK = os.environ["WEBHOOK"]
SECRET = os.environ["SECRET"]

def sign_url():
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{SECRET}"
    sign = base64.b64encode(
        hmac.new(
            SECRET.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()
    )
    return f"{WEBHOOK}&timestamp={timestamp}&sign={urllib.parse.quote_plus(sign)}"

def send_msg():
    url = sign_url()
    content = (
        "【硬件任务提醒】\n"
        "请大家更新《硬件待测任务》信息，\n"
        "并将近期的原始记录和报告解密版以文件夹整理好上传 SVN。\n"
        "谢谢配合！"
    )

    data = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {
            "isAtAll": True  # @全员
        }
    }

    resp = requests.post(url, json=data)
    print("发送状态:", resp.status_code, resp.text)

def main():
    today = datetime.date.today()

    # 只在 2026 年每月 22 号
    if today.year != 2026:
        print("不是 2026 年，不发送提醒")
        return
    if today.day != 22:
        print("今天不是 22 号，不发送提醒")
        return

    # 防重复发送（可选）
    sent_file = f".sent_{today}.txt"
    if os.path.exists(sent_file):
        print("今日已发送提醒，退出")
        return
    open(sent_file, "w").close()

    send_msg()
    print("提醒已发送")

if __name__ == "__main__":
    main()
