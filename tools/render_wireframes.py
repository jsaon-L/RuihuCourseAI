from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "visual_wireframes"
W, H = 1280, 720


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = font(44, True)
F_H1 = font(34, True)
F_H2 = font(28, True)
F_BODY = font(24)
F_SMALL = font(18)
F_TINY = font(15)


INK = "#263238"
MUTED = "#667085"
LINE = "#B7C0CE"
BG = "#F6F8FB"
PANEL = "#FFFFFF"
SOFT = "#EAF1F8"
BLUE = "#2D6CDF"
GREEN = "#2B9B72"
ORANGE = "#E9922E"
RED = "#C84646"


@dataclass
class Screen:
    filename: str
    title: str
    draw: Callable[[ImageDraw.ImageDraw], None]


def rect(draw: ImageDraw.ImageDraw, xy, fill=PANEL, outline=LINE, width=2, radius=14):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def line(draw: ImageDraw.ImageDraw, xy, fill=LINE, width=2):
    draw.line(xy, fill=fill, width=width)


def text(draw: ImageDraw.ImageDraw, xy, value: str, fnt=F_BODY, fill=INK, anchor=None):
    draw.text(xy, value, font=fnt, fill=fill, anchor=anchor)


def button(draw: ImageDraw.ImageDraw, xy, label: str, fill=SOFT, outline=LINE, fg=INK, radius=12):
    rect(draw, xy, fill=fill, outline=outline, width=2, radius=radius)
    x1, y1, x2, y2 = xy
    text(draw, ((x1 + x2) / 2, (y1 + y2) / 2), label, F_BODY, fg, "mm")


def title_bar(draw: ImageDraw.ImageDraw, title: str, right: str = ""):
    rect(draw, (24, 22, 1256, 86), fill="#FFFFFF", radius=12)
    text(draw, (50, 54), title, F_H1, anchor="lm")
    if right:
        text(draw, (1230, 54), right, F_BODY, MUTED, "rm")


def base(draw: ImageDraw.ImageDraw, title: str):
    draw.rectangle((0, 0, W, H), fill=BG)
    title_bar(draw, title)


def content_box(draw: ImageDraw.ImageDraw, xy=(80, 140, 1200, 560), label="主内容展示区", sub="视频 / 图片 / 图文 / 互动题面"):
    rect(draw, xy, fill="#FFFFFF", outline="#9AA8BA", width=3, radius=18)
    x1, y1, x2, y2 = xy
    text(draw, ((x1 + x2) / 2, (y1 + y2) / 2 - 18), label, F_H1, MUTED, "mm")
    if sub:
        text(draw, ((x1 + x2) / 2, (y1 + y2) / 2 + 28), sub, F_BODY, MUTED, "mm")


def card(draw: ImageDraw.ImageDraw, x, y, w, h, title_value, subtitle):
    rect(draw, (x, y, x + w, y + h), radius=16)
    rect(draw, (x + 14, y + 14, x + w - 14, y + 104), fill="#DDE7F3", outline="#A9B7C8", radius=12)
    text(draw, (x + w / 2, y + 62), "封面图", F_BODY, MUTED, "mm")
    text(draw, (x + 18, y + 136), title_value, F_BODY)
    text(draw, (x + 18, y + 170), subtitle, F_SMALL, MUTED)


def draw_player_loading(draw):
    base(draw, "播放端 - 启动加载页")
    text(draw, (640, 250), "幼儿课程课件系统", F_TITLE, BLUE, "mm")
    text(draw, (640, 320), "正在加载本地课程...", F_H2, INK, "mm")
    rect(draw, (410, 370, 870, 408), fill="#FFFFFF", radius=20)
    draw.rounded_rectangle((420, 380, 710, 398), radius=9, fill=BLUE)
    text(draw, (640, 470), "正在扫描 Courses 目录", F_BODY, MUTED, "mm")
    text(draw, (1180, 660), "版本号 v1.0", F_SMALL, MUTED, "rm")


def draw_player_course_list(draw):
    base(draw, "播放端 - 课程列表页")
    for i, label in enumerate(["全部", "最近播放", "魔方", "思维训练", "启蒙认知", "动手操作"]):
        button(draw, (50 + i * 132, 110, 160 + i * 132, 158), label, fill="#FFFFFF")
    button(draw, (930, 34, 1005, 74), "刷新")
    button(draw, (1020, 34, 1095, 74), "设置")
    button(draw, (1110, 34, 1185, 74), "退出")
    items = [
        ("魔方启蒙第一课", "Level 1 / 认识魔方"),
        ("颜色观察课", "Level 1 / 启蒙认知"),
        ("空间思维课", "Level 2 / 思维训练"),
        ("动手拼搭课", "Level 1 / 动手操作"),
        ("魔方第二课", "Level 1 / 基础手法"),
        ("图形分类课", "Level 2 / 分类"),
        ("观察挑战课", "Level 1 / 找一找"),
        ("课堂复习课", "Level 1 / 巩固"),
    ]
    for idx, item in enumerate(items):
        row, col = divmod(idx, 4)
        card(draw, 55 + col * 305, 190 + row * 230, 260, 190, item[0], item[1])


def draw_player_play(draw):
    base(draw, "播放端 - 课程播放页")
    text(draw, (1170, 54), "3 / 8", F_H2, BLUE, "rm")
    content_box(draw)
    y = 610
    labels = ["上一环节", "暂停/继续", "重播", "下一环节", "环节列表", "隐藏"]
    for i, label in enumerate(labels):
        button(draw, (70 + i * 195, y, 235 + i * 195, y + 68), label, fill="#FFFFFF")


def draw_player_hidden_controls(draw):
    base(draw, "播放端 - 控制面板隐藏状态")
    text(draw, (1170, 54), "3 / 8", F_H2, BLUE, "rm")
    content_box(draw, (80, 130, 1200, 640))
    button(draw, (1080, 590, 1190, 654), "控制", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_player_section_list(draw):
    base(draw, "播放端 - 环节列表面板")
    content_box(draw, (60, 120, 820, 650), "当前课程画面", "")
    rect(draw, (850, 110, 1230, 650), fill="#FFFFFF", radius=20)
    text(draw, (880, 150), "环节列表", F_H2)
    button(draw, (1132, 126, 1210, 174), "关闭")
    items = [
        ("● 1 开场导入", "视频"),
        ("  2 目标呈现", "图文"),
        ("  3 内容讲解", "视频"),
        ("  4 示范观察", "多图"),
        ("  5 课堂练习", "倒计时"),
        ("  6 游戏巩固", "选择题"),
        ("  7 结果反馈", "奖励"),
        ("  8 课堂收束", "文本"),
    ]
    for i, (name, kind) in enumerate(items):
        y = 205 + i * 50
        if i == 0:
            rect(draw, (875, y - 12, 1205, y + 32), fill="#E9F2FF", outline="#D3E4FF", radius=10)
        text(draw, (895, y + 10), name, F_BODY, BLUE if i == 0 else INK, "lm")
        text(draw, (1175, y + 10), kind, F_SMALL, MUTED, "rm")


def draw_player_error(draw):
    base(draw, "播放端 - 异常提示弹窗")
    content_box(draw, (60, 120, 1220, 650), "课程画面背景", "")
    draw.rectangle((0, 0, W, H), fill=(0, 0, 0, 0))
    rect(draw, (390, 210, 890, 520), fill="#FFFFFF", outline="#8794A8", width=3, radius=18)
    text(draw, (430, 260), "资源加载失败", F_H1, RED)
    line(draw, (410, 300, 870, 300))
    text(draw, (430, 350), "当前环节的视频无法播放。", F_BODY)
    text(draw, (430, 392), "可重试，或跳过当前环节继续上课。", F_BODY, MUTED)
    button(draw, (430, 445, 560, 500), "重试", fill="#FFFFFF")
    button(draw, (575, 445, 705, 500), "跳过", fill="#FFFFFF")
    button(draw, (720, 445, 850, 500), "返回列表", fill=SOFT)


def draw_editor_course_manager(draw):
    base(draw, "编辑端 - 课程管理页")
    button(draw, (970, 34, 1095, 74), "新建课程", fill=BLUE, outline=BLUE, fg="#FFFFFF")
    button(draw, (1110, 34, 1240, 74), "导入课程包")
    rect(draw, (45, 110, 940, 166), fill="#FFFFFF", radius=12)
    text(draw, (65, 138), "搜索课程名称/编号", F_BODY, MUTED, "lm")
    rect(draw, (285, 120, 760, 156), fill="#F7FAFC", radius=8)
    button(draw, (785, 116, 900, 160), "搜索")
    for i, (name, code, tag) in enumerate([
        ("魔方启蒙第一课", "CUBE-L1-001", "Level 1 / 认识魔方"),
        ("思维训练第一课", "THINK-L1-001", "Level 1 / 图形观察"),
        ("动手操作课", "HAND-L1-001", "Level 1 / 拼搭"),
    ]):
        y = 205 + i * 150
        rect(draw, (55, y, 1225, y + 122), fill="#FFFFFF", radius=16)
        rect(draw, (80, y + 18, 210, y + 104), fill="#DDE7F3", radius=10)
        text(draw, (145, y + 62), "封面", F_SMALL, MUTED, "mm")
        text(draw, (235, y + 30), f"课程名称：{name}", F_H2)
        text(draw, (235, y + 68), f"编号：{code}", F_BODY, MUTED)
        text(draw, (235, y + 98), f"级别/主题：{tag}", F_SMALL, MUTED)
        button(draw, (980, y + 25, 1060, y + 73), "打开")
        button(draw, (1075, y + 25, 1155, y + 73), "复制")
        button(draw, (1168, y + 25, 1210, y + 73), "删", fill="#FFF2F2", outline="#E7B5B5", fg=RED)


def draw_editor_main(draw):
    base(draw, "编辑端 - 课程编辑主页面")
    button(draw, (970, 34, 1060, 74), "保存", fill="#FFFFFF")
    button(draw, (1080, 34, 1170, 74), "导出", fill=BLUE, outline=BLUE, fg="#FFFFFF")
    rect(draw, (35, 110, 265, 680), fill="#FFFFFF", radius=14)
    text(draw, (60, 145), "环节列表", F_H2)
    sections = ["1 开场导入", "2 目标呈现", "3 内容讲解", "4 示范观察", "5 课堂练习", "6 游戏巩固", "7 结果反馈"]
    for i, s in enumerate(sections):
        y = 185 + i * 48
        if i == 0:
            rect(draw, (55, y - 10, 245, y + 30), fill="#E9F2FF", outline="#D3E4FF", radius=9)
        text(draw, (70, y + 10), s, F_SMALL if i else F_BODY, BLUE if i == 0 else INK, "lm")
    for i, label in enumerate(["添加", "复制", "删除", "上移"]):
        button(draw, (55 + (i % 2) * 95, 590 + (i // 2) * 50, 140 + (i % 2) * 95, 632 + (i // 2) * 50), label)
    rect(draw, (285, 110, 890, 680), fill="#FFFFFF", radius=14)
    text(draw, (315, 145), "当前编辑区", F_H2)
    fields = [("标题", "开场导入"), ("类型", "intro / 开场导入"), ("资源", "intro.mp4"), ("自动切换", "视频结束后进入下一环节"), ("老师提示", "引导孩子观察颜色")]
    for i, (k, v) in enumerate(fields):
        y = 200 + i * 72
        text(draw, (330, y), k, F_BODY, MUTED)
        rect(draw, (460, y - 12, 850, y + 34), fill="#F7FAFC", radius=8)
        text(draw, (478, y + 11), v, F_SMALL, INK, "lm")
    rect(draw, (910, 110, 1245, 680), fill="#FFFFFF", radius=14)
    text(draw, (935, 145), "预览/校验", F_H2)
    rect(draw, (940, 185, 1215, 355), fill="#F1F5F9", radius=12)
    text(draw, (1078, 270), "预览画面", F_BODY, MUTED, "mm")
    text(draw, (940, 410), "校验结果：", F_BODY)
    text(draw, (960, 450), "- 缺少资源 0", F_SMALL, GREEN)
    text(draw, (960, 482), "- 视频警告 0", F_SMALL, GREEN)
    button(draw, (940, 555, 1070, 608), "预览当前")
    button(draw, (1085, 555, 1215, 608), "预览全课")


def draw_editor_basic_info(draw):
    base(draw, "编辑端 - 基础信息编辑页")
    rect(draw, (60, 120, 1220, 660), fill="#FFFFFF", radius=18)
    text(draw, (95, 162), "基础信息", F_H1)
    labels = ["课程名称 *", "课程编号 *", "适用年龄", "课程主题 *", "预计时长", "教学目标"]
    values = ["魔方启蒙第一课", "CUBE-L1-001    课程级别 *  Level 1", "4-6岁          课程分类  魔方", "认识魔方", "30 分钟", "1. 认识魔方的基本结构\n2. 能指出中心块、棱块和角块"]
    for i, (lab, val) in enumerate(zip(labels, values)):
        y = 220 + i * 64
        text(draw, (105, y), lab, F_BODY, MUTED)
        h = 48 if i != 5 else 100
        rect(draw, (260, y - 14, 790, y - 14 + h), fill="#F7FAFC", radius=8)
        text(draw, (280, y + 10), val, F_SMALL, INK, "lm")
    text(draw, (850, 220), "课程封面", F_BODY, MUTED)
    rect(draw, (850, 260, 1150, 430), fill="#DDE7F3", radius=14)
    text(draw, (1000, 345), "封面预览 16:9", F_BODY, MUTED, "mm")
    button(draw, (850, 455, 980, 510), "选择图片")
    button(draw, (1000, 455, 1130, 510), "移除")


def draw_editor_resources(draw):
    base(draw, "编辑端 - 资源管理页")
    button(draw, (970, 34, 1085, 74), "导入图片")
    button(draw, (1100, 34, 1215, 74), "导入视频")
    rect(draw, (55, 115, 1225, 655), fill="#FFFFFF", radius=18)
    text(draw, (85, 155), "类型筛选：全部     使用状态：全部", F_BODY, MUTED)
    headers = ["文件名", "类型", "大小", "状态", "操作"]
    xs = [90, 500, 650, 800, 1010]
    for x, h in zip(xs, headers):
        text(draw, (x, 215), h, F_BODY, MUTED)
    line(draw, (80, 245, 1200, 245))
    rows = [
        ("intro.mp4", "视频", "8.2MB", "已使用", "预览 / 校验"),
        ("goal.jpg", "图片", "650KB", "已使用", "预览"),
        ("old_video.mov", "视频", "20MB", "不兼容", "转码"),
        ("unused.png", "图片", "300KB", "未使用", "删除"),
    ]
    for i, row in enumerate(rows):
        y = 290 + i * 70
        fill = "#FFF7E8" if row[3] == "不兼容" else "#FFFFFF"
        rect(draw, (75, y - 25, 1205, y + 28), fill=fill, outline="#E5EAF2", radius=8)
        for x, val in zip(xs, row):
            color = RED if val == "不兼容" else INK
            text(draw, (x, y), val, F_SMALL, color, "lm")


def draw_editor_video_check(draw):
    base(draw, "编辑端 - 视频校验/转码页")
    rect(draw, (60, 115, 1220, 655), fill="#FFFFFF", radius=18)
    text(draw, (95, 160), "视频校验：old_video.mov", F_H1)
    rect(draw, (95, 205, 595, 465), fill="#FFF8F0", outline="#F1C99C", radius=14)
    rect(draw, (650, 205, 1150, 465), fill="#F0FAF6", outline="#A7D9C5", radius=14)
    text(draw, (125, 245), "原视频信息", F_H2)
    text(draw, (680, 245), "推荐输出", F_H2)
    left = ["容器：MOV", "编码：H.265", "分辨率：1920x1080", "帧率：60fps", "像素格式：yuv420p10", "状态：不兼容"]
    right = ["容器：MP4", "编码：H.264", "分辨率：1280x720", "帧率：25fps", "像素格式：yuv420p", "FFmpeg：StreamingAssets/ffmpeg"]
    for i, value in enumerate(left):
        text(draw, (130, 295 + i * 34), value, F_SMALL, RED if "不兼容" in value else INK)
    for i, value in enumerate(right):
        text(draw, (685, 295 + i * 34), value, F_SMALL, GREEN if i < 5 else MUTED)
    button(draw, (105, 505, 245, 560), "开始转码", fill=BLUE, outline=BLUE, fg="#FFFFFF")
    button(draw, (265, 505, 425, 560), "打开输出目录")
    button(draw, (445, 505, 585, 560), "重新校验")
    rect(draw, (650, 505, 1150, 610), fill="#F7FAFC", radius=10)
    text(draw, (675, 535), "转码日志：", F_SMALL, MUTED)
    text(draw, (675, 570), "> 正在转码...", F_SMALL, INK)


def draw_editor_export(draw):
    base(draw, "编辑端 - 导出课程包页")
    rect(draw, (90, 125, 1190, 650), fill="#FFFFFF", radius=18)
    text(draw, (130, 175), "导出课程包", F_H1)
    text(draw, (130, 235), "导出目录", F_BODY, MUTED)
    rect(draw, (260, 212, 1000, 258), fill="#F7FAFC", radius=8)
    text(draw, (280, 235), r"E:\CourseExports\cube_level1_lesson01", F_SMALL, INK, "lm")
    button(draw, (1020, 210, 1120, 260), "选择")
    text(draw, (130, 315), "导出前校验：", F_H2)
    checks = ["基础信息完整", "环节数量 8", "资源文件完整", "视频格式兼容", "JSON 可解析"]
    for i, check in enumerate(checks):
        text(draw, (160, 370 + i * 44), f"√ {check}", F_BODY, GREEN)
    button(draw, (515, 575, 765, 635), "开始导出", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_prepare(draw):
    base(draw, "课程环节 - 课前准备")
    rect(draw, (120, 135, 1160, 635), fill="#FFFFFF", radius=22)
    text(draw, (640, 190), "课前准备", F_TITLE, BLUE, "mm")
    text(draw, (240, 270), "今天需要准备：", F_H2)
    for i, item in enumerate(["□ 魔方每人一个", "□ 老师演示魔方", "□ 贴纸奖励", "□ 播放设备声音正常"]):
        text(draw, (285, 330 + i * 52), item, F_BODY)
    button(draw, (520, 545, 760, 610), "开始上课", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_intro(draw):
    base(draw, "课程环节 - 开场导入")
    text(draw, (640, 145), "今天我们认识魔方", F_TITLE, BLUE, "mm")
    content_box(draw, (300, 205, 980, 470), "视频 / 主题图", "")
    text(draw, (640, 545), "你看到了哪些颜色？", F_H2, INK, "mm")
    button(draw, (1030, 610, 1170, 665), "下一步", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_goal(draw):
    base(draw, "课程环节 - 目标呈现")
    text(draw, (640, 145), "今天的小目标", F_TITLE, BLUE, "mm")
    rect(draw, (220, 240, 460, 430), fill="#DDE7F3", radius=18)
    text(draw, (340, 335), "图标 / 图", F_BODY, MUTED, "mm")
    for i, item in enumerate(["1. 认识魔方的颜色", "2. 找到中心块", "3. 说出角块和棱块"]):
        text(draw, (540, 270 + i * 62), item, F_H2)
    button(draw, (1030, 610, 1170, 665), "下一步", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_explain(draw):
    base(draw, "课程环节 - 内容讲解")
    text(draw, (1150, 54), "2 / 4", F_H2, BLUE, "rm")
    content_box(draw, (270, 155, 1010, 445), "图片 / 视频", "")
    text(draw, (240, 510), "重点：中心块的位置不会改变。", F_H2, ORANGE)
    button(draw, (430, 600, 590, 660), "上一页")
    button(draw, (690, 600, 850, 660), "下一页", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_demo(draw):
    base(draw, "课程环节 - 示范观察")
    text(draw, (1150, 54), "步骤 1 / 3", F_BODY, BLUE, "rm")
    content_box(draw, (270, 155, 1010, 445), "示范视频 / 分步图", "")
    text(draw, (250, 510), "观察提示：先看白色中心块在哪里。", F_H2)
    button(draw, (430, 600, 610, 660), "再看一次")
    button(draw, (690, 600, 850, 660), "下一步", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_practice(draw):
    base(draw, "课程环节 - 课堂练习")
    text(draw, (640, 155), "请找到你手中魔方的白色中心块。", F_H1, INK, "mm")
    rect(draw, (490, 260, 790, 400), fill="#FFFFFF", outline=BLUE, width=4, radius=24)
    text(draw, (640, 330), "02:00", font(64, True), BLUE, "mm")
    for i, label in enumerate(["开始练习", "暂停", "时间到", "下一步"]):
        button(draw, (250 + i * 205, 560, 415 + i * 205, 625), label, fill=BLUE if i == 0 else "#FFFFFF", outline=BLUE if i == 0 else LINE, fg="#FFFFFF" if i == 0 else INK)


def draw_choice(draw):
    base(draw, "课程环节 - 游戏巩固：选择题")
    text(draw, (640, 145), "哪一个是中心块？", F_TITLE, BLUE, "mm")
    for i, label in enumerate(["A 图片/文字", "B 图片/文字", "C 图片/文字"]):
        x = 205 + i * 315
        rect(draw, (x, 250, x + 245, 420), fill="#FFFFFF", radius=18)
        text(draw, (x + 122, 335), label, F_H2, INK, "mm")
    for i, label in enumerate(["显示答案", "显示反馈", "下一题/下一步"]):
        button(draw, (330 + i * 220, 580, 500 + i * 220, 640), label, fill="#FFFFFF")


def draw_judge(draw):
    base(draw, "课程环节 - 游戏巩固：判断题")
    text(draw, (640, 155), "魔方的中心块会移动到其他位置吗？", F_H1, BLUE, "mm")
    rect(draw, (350, 280, 560, 430), fill="#FFFFFF", radius=18)
    rect(draw, (720, 280, 930, 430), fill="#FFFFFF", radius=18)
    text(draw, (455, 355), "对", font(58, True), GREEN, "mm")
    text(draw, (825, 355), "错", font(58, True), RED, "mm")
    for i, label in enumerate(["显示答案", "显示反馈", "下一步"]):
        button(draw, (360 + i * 220, 580, 530 + i * 220, 640), label)


def draw_find(draw):
    base(draw, "课程环节 - 游戏巩固：找一找")
    text(draw, (640, 135), "请找出图中的红色中心块。", F_H1, BLUE, "mm")
    content_box(draw, (230, 200, 1050, 500), "大图展示区", "")
    button(draw, (430, 590, 610, 650), "显示答案")
    button(draw, (670, 590, 850, 650), "下一步", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_match(draw):
    base(draw, "课程环节 - 游戏巩固：配对")
    text(draw, (360, 145), "左边", F_H2, MUTED, "mm")
    text(draw, (910, 145), "右边", F_H2, MUTED, "mm")
    for i, left_label in enumerate(["中心块", "棱块"]):
        y = 230 + i * 150
        rect(draw, (230, y, 480, y + 90), fill="#FFFFFF", radius=16)
        text(draw, (355, y + 45), left_label, F_H2, INK, "mm")
        rect(draw, (800, y, 1050, y + 90), fill="#FFFFFF", radius=16)
        text(draw, (925, y + 45), f"图片 {chr(65 + i)}", F_H2, INK, "mm")
    for i, label in enumerate(["显示答案", "显示反馈", "下一步"]):
        button(draw, (360 + i * 220, 585, 530 + i * 220, 645), label)


def draw_drag_demo(draw):
    base(draw, "课程环节 - 游戏巩固：拖拽示意")
    text(draw, (640, 135), "请把正确颜色放到目标位置。", F_H1, BLUE, "mm")
    text(draw, (375, 220), "起始状态", F_H2, MUTED, "mm")
    text(draw, (900, 220), "目标状态", F_H2, MUTED, "mm")
    rect(draw, (235, 260, 515, 430), fill="#FFFFFF", radius=18)
    rect(draw, (760, 260, 1040, 430), fill="#FFFFFF", radius=18)
    text(draw, (375, 345), "示意图", F_H2, MUTED, "mm")
    text(draw, (900, 345), "示意图", F_H2, MUTED, "mm")
    text(draw, (640, 345), "→", font(64, True), BLUE, "mm")
    for i, label in enumerate(["显示做法", "显示反馈", "下一步"]):
        button(draw, (360 + i * 220, 585, 530 + i * 220, 645), label)


def draw_feedback(draw):
    base(draw, "课程环节 - 结果反馈")
    text(draw, (640, 205), "太棒了！", font(64, True), BLUE, "mm")
    text(draw, (640, 330), "★   ★   ★", font(62, True), ORANGE, "mm")
    text(draw, (640, 455), "你完成了今天的挑战！", F_H1, INK, "mm")
    button(draw, (410, 585, 590, 645), "再播放一次")
    button(draw, (690, 585, 890, 645), "返回课程列表", fill=BLUE, outline=BLUE, fg="#FFFFFF")


def draw_summary(draw):
    base(draw, "课程环节 - 课堂收束/延伸")
    text(draw, (640, 135), "今天学到了什么？", F_TITLE, BLUE, "mm")
    lines = [
        "1. 我们认识了中心块。",
        "2. 我们找到了棱块和角块。",
        "3. 回家可以和爸爸妈妈一起找一找。",
        "下节课预告：我们来学习魔方第一步。",
    ]
    for i, value in enumerate(lines):
        text(draw, (300, 240 + i * 68), value, F_H2 if i < 3 else F_BODY, INK if i < 3 else MUTED)
    button(draw, (540, 585, 740, 645), "结束课程", fill=BLUE, outline=BLUE, fg="#FFFFFF")


SCREENS: list[Screen] = [
    Screen("01_player_loading.png", "播放端 - 启动加载页", draw_player_loading),
    Screen("02_player_course_list.png", "播放端 - 课程列表页", draw_player_course_list),
    Screen("03_player_play.png", "播放端 - 课程播放页", draw_player_play),
    Screen("04_player_hidden_controls.png", "播放端 - 控制面板隐藏状态", draw_player_hidden_controls),
    Screen("05_player_section_list.png", "播放端 - 环节列表面板", draw_player_section_list),
    Screen("06_player_error.png", "播放端 - 异常提示弹窗", draw_player_error),
    Screen("07_editor_course_manager.png", "编辑端 - 课程管理页", draw_editor_course_manager),
    Screen("08_editor_main.png", "编辑端 - 课程编辑主页面", draw_editor_main),
    Screen("09_editor_basic_info.png", "编辑端 - 基础信息编辑页", draw_editor_basic_info),
    Screen("10_editor_resources.png", "编辑端 - 资源管理页", draw_editor_resources),
    Screen("11_editor_video_check.png", "编辑端 - 视频校验/转码页", draw_editor_video_check),
    Screen("12_editor_export.png", "编辑端 - 导出课程包页", draw_editor_export),
    Screen("13_section_prepare.png", "课程环节 - 课前准备", draw_prepare),
    Screen("14_section_intro.png", "课程环节 - 开场导入", draw_intro),
    Screen("15_section_goal.png", "课程环节 - 目标呈现", draw_goal),
    Screen("16_section_explain.png", "课程环节 - 内容讲解", draw_explain),
    Screen("17_section_demo.png", "课程环节 - 示范观察", draw_demo),
    Screen("18_section_practice.png", "课程环节 - 课堂练习", draw_practice),
    Screen("19_section_choice.png", "课程环节 - 游戏巩固：选择题", draw_choice),
    Screen("20_section_judge.png", "课程环节 - 游戏巩固：判断题", draw_judge),
    Screen("21_section_find.png", "课程环节 - 游戏巩固：找一找", draw_find),
    Screen("22_section_match.png", "课程环节 - 游戏巩固：配对", draw_match),
    Screen("23_section_drag_demo.png", "课程环节 - 游戏巩固：拖拽示意", draw_drag_demo),
    Screen("24_section_feedback.png", "课程环节 - 结果反馈", draw_feedback),
    Screen("25_section_summary.png", "课程环节 - 课堂收束/延伸", draw_summary),
]


def render(screen: Screen) -> Path:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    screen.draw(draw)
    output = OUT_DIR / screen.filename
    img.save(output)
    return output


def make_contact_sheet(paths: Iterable[Path]) -> Path:
    thumbs = []
    for path in paths:
        img = Image.open(path).resize((320, 180))
        thumbs.append((path, img))

    cols = 5
    rows = (len(thumbs) + cols - 1) // cols
    label_h = 34
    sheet = Image.new("RGB", (cols * 340 + 20, rows * (180 + label_h + 20) + 20), "#F3F6FA")
    draw = ImageDraw.Draw(sheet)
    for idx, (path, img) in enumerate(thumbs):
        row, col = divmod(idx, cols)
        x = 20 + col * 340
        y = 20 + row * (180 + label_h + 20)
        sheet.paste(img, (x, y))
        draw.rectangle((x, y, x + 320, y + 180), outline="#AEB8C6", width=1)
        draw.text((x, y + 188), path.stem, font=F_TINY, fill=INK)
    output = OUT_DIR / "00_contact_sheet.png"
    sheet.save(output)
    return output


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    paths = [render(screen) for screen in SCREENS]
    contact = make_contact_sheet(paths)
    print(f"Generated {len(paths)} wireframe images")
    print(contact)


if __name__ == "__main__":
    main()
