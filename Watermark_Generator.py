import argparse
from PIL import Image, ImageDraw, ImageFont
import datetime
import os

def main():
    # 设置 argparse 参数解析
    parser = argparse.ArgumentParser(description='生成带有水印的图片。')
    parser.add_argument('text', type=str, help='水印文本')
    parser.add_argument('-d', '--date', action='store_true', help='是否添加日期')
    args = parser.parse_args()

    # 创建一个1920x1080的透明背景图片
    width, height = 1920, 1080
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # 使用 RGBA 模式创建透明背景

    # 获取当前日期并格式化为字符串
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # 设置文本内容（包括日期）、字体和颜色
    watermark_text = f"To {args.text} {current_date}" if args.date else f"To {args.text}"

    try:
        # 使用指定的字体文件
        font = ImageFont.truetype('STHeiti Medium.ttc', size=72)  # 使用 STHeiti Medium 字体
    except IOError:
        print("字体文件未找到，请检查文件路径")
        return

    text_color = 'white'  # 设置文本颜色为白色

    # 计算文本尺寸
    text_width, text_height = font.getmask(watermark_text).size

    # 计算文本的位置以实现居中对齐
    text_x = (width - text_width) / 2
    vertical_offset = 320  # 垂直偏移量
    text_y = (height - text_height) / 2 - vertical_offset

    # 创建一个用于绘图的对象
    draw = ImageDraw.Draw(image)

    # 多次绘制文本以产生加粗效果
    for offset in range(-1, 2):
        draw.text((text_x + offset, text_y), watermark_text, fill=text_color, font=font)
        draw.text((text_x, text_y + offset), watermark_text, fill=text_color, font=font)

    # 生成一个有效的文件名
    valid_filename = "".join(c for c in watermark_text if c.isalnum() or c in (' ', '-', '_')).rstrip()
    file_name = valid_filename.replace(' ', '_') + '.png'

    # 保存图片到用户主目录路径
    save_path = os.path.join(os.path.expanduser('~/Desktop'), file_name)
    image.save(save_path)

    print(f"图片已保存到：{save_path}")

if __name__ == '__main__':
    main()