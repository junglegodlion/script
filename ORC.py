import keyboard
import time
from PIL import ImageGrab
import pytesseract
from aip import AipOcr
from PIL import ImageGrab


# 利用截图软件（Snipaste）截图到剪贴板
# 输入键盘的触发事件
while True:
    keyboard.wait(hotkey="f1")
    keyboard.wait(hotkey="ctrl+c")
    time.sleep(0.1)

    # 把图片从剪切板保存到当前路径
    image = ImageGrab.grabclipboard()
    image.save("screen.png")

    # 法二：利用百度API
    APP_ID = '你的 App ID'
    API_KEY = '你的 Api Key'
    SECRET_KEY = '你的 Secret Key'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    with open("screen.png", 'rb') as f:
        image = f.read()

        # 调用百度API通用文字识别（高精度版），提取图片中的内容
        text = client.basicAccurate(image)
        result = text["words_result"]
        for i in result:
            print(i["words"])