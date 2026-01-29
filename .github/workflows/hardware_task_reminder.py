import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import datetime
import os

# 从 GitHub Secrets 获取
WEBHOOK = os.environ["WEBHOOK"]
SECRET = os.environ["SECRET"]

# 钉钉加签
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

# 发送消息
def send_msg():
    url = sign_url()
    content = (
        "【更新提醒】\n"
        "请大家及时更新《硬件待测任务》信息\n"
        "并将近期的原始记录和报告解密版以文件夹整理好上传SVN"
    )

    data = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {
            "isAtAll": True  # @所有人
        }
    }

    resp = requests.post(url, json=data)
    print("发送状态:", resp.status_code, resp.text)

def main():
    today = datetime.date.today()
    if today.year != 2026:
        # print("不是 2026 年，不发送提醒")
        return
    if today.day != 22:
        # print("今天不是 22 号，不发送提醒")
        return

    send_msg()
    print("提醒已发送")


if __name__ == "__main__":
    main()
