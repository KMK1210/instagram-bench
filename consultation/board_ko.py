"""Build the annotated before/after consultation board (Korean)."""
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

before, after, out = sys.argv[1:4]
S = 1000 / 2576  # source -> panel scale
F = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FB = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
title, h2, body, small = (ImageFont.truetype(FB, 44), ImageFont.truetype(FB, 26),
                          ImageFont.truetype(F, 21), ImageFont.truetype(F, 18))
INK, MUTED, ACCENT, HAIR, BG = (34, 30, 28), (110, 100, 95), (196, 84, 96), (70, 110, 160), (250, 247, 244)

# (number, source xy, colour, heading, explanation)
notes = [
    (1, (1230, 300), HAIR, "헤어: 자연스러운 사이드 가르마 (미적용)",
     "정가운데 가르마를 2-3cm 옆으로 옮기세요. 지금은 정수리 뿌리가 납작한데, 사이드 가르마로 뿌리 볼륨과 부드러움이 생깁니다."),
    (2, (560, 1150), HAIR, "헤어: 얼굴형 커버 레이어드 (미적용)",
     "쇄골 길이는 유지하고, 광대 높이에서 시작해 턱 쪽으로 안쪽으로 감기는 긴 레이어를 넣으세요. 볼 아래쪽 넓이를 가려주고 시선을 광대로 올려줍니다."),
    (3, (540, 1850), HAIR, "헤어: 끝 다듬기 + 글로스 (미적용)",
     "끝이 얇고 가벼워 힘이 없어 보입니다. 2-3cm 정리해 끝선을 도톰하게 만들고, 투명 또는 소프트 브라운 글로스(3-4레벨)로 윤기와 부스스함을 잡으세요. 탈색은 필요 없습니다."),
    (4, (1230, 760), ACCENT, "눈썹: 더 채우고, 부드럽게, 살짝 길게",
     "눈썹이 가늘고 꼬리가 비어 있으며, 앞머리가 코 쪽으로 처져 무표정일 때 살짝 찡그린 인상을 줍니다. 토프 펜슬로 채우고 앞머리는 연하게, 꼬리는 5mm 연장하세요."),
    (5, (1395, 935), ACCENT, "눈: 점막 채우기 + 얇은 브라운 라이너",
     "윗 속눈썹 라인 바깥쪽 2/3를 채우고, 아래 속눈썹 라인 각도를 따라 2-3mm 짧게 빼주세요. 속눈썹이 아래로 곧게 자라 눈에 그늘을 지우니 꼭 컬링하세요. 앞트임 라인은 진하게 하지 마세요."),
    (6, (820, 1035), ACCENT, "눈 밑: 피치 컬러 코렉터",
     "양쪽 눈 밑에 푸른 기 다크서클이 약간 있습니다. 안쪽 절반에만 피치 코렉터를 두드리고 컨실러를 얇게 올리세요. 파우더는 가볍게."),
    (7, (1370, 1110), ACCENT, "블러셔: 높게, 관자놀이 방향으로",
     "로즈 피치 블러셔를 볼 사과존보다 위에 올리고 관자놀이 쪽으로 쓸어 올리세요. 높게 바르면 도톰한 볼 아래쪽이 리프팅돼 보입니다. 볼 정중앙은 피하세요."),
    (8, (1060, 1400), ACCENT, "입술: 로지 코랄 틴트, 선명한 라인",
     "입술 자체는 이미 균형이 좋습니다. 로즈 코랄 틴트에 인중 쪽 입술산과 바깥 꼬리만 살짝 정리하면 살짝 내려간 입꼬리가 보완됩니다."),
    (9, (1030, 1185), ACCENT, "피부: 얇게, 광은 살리기",
     "필요한 곳(코 옆 붉은기)에만 가벼운 틴트나 쿠션을 쓰세요. T존은 유분만 정리하고 광대 윤기는 남기세요. 너무 매트하게 하지 마세요."),
]

panel = 1000
pad = 50
W = pad * 3 + panel * 2
legend_h = 720
H = 150 + panel + 60 + legend_h
board = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(board)
d.text((pad, 40), "뷰티 컨설팅: 비포 / 애프터", font=title, fill=INK)
d.text((pad, 100), "메이크업은 실제 사진에 시뮬레이션했고, 헤어는 추천 사항만 표시했습니다 (파란색).",
       font=small, fill=MUTED)

y0 = 150
for i, (path, label) in enumerate(((before, "BEFORE"), (after, "AFTER (메이크업 시뮬레이션)"))):
    x0 = pad + i * (panel + pad)
    board.paste(Image.open(path).convert("RGB").resize((panel, panel), Image.LANCZOS), (x0, y0))
    d.rectangle((x0, y0, x0 + 330 if i else x0 + 130, y0 + 40), fill=(0, 0, 0))
    d.text((x0 + 12, y0 + 8), label, font=small, fill=(255, 255, 255))

ax = pad * 2 + panel
for n, (sx, sy), col, *_ in notes:
    cx, cy = ax + sx * S, y0 + sy * S
    d.ellipse((cx - 19, cy - 19, cx + 19, cy + 19), fill=col, outline=(255, 255, 255), width=3)
    tw = d.textlength(str(n), font=h2)
    d.text((cx - tw / 2, cy - 16), str(n), font=h2, fill=(255, 255, 255))

ly = y0 + panel + 60
colw = (W - pad * 3) // 2
for idx, (n, _, col, head, text) in enumerate(notes):
    col_i = 0 if idx < 5 else 1
    if idx == 5:
        ly = y0 + panel + 60
    x = pad + col_i * (colw + pad)
    d.ellipse((x, ly, x + 34, ly + 34), fill=col)
    tw = d.textlength(str(n), font=h2)
    d.text((x + 17 - tw / 2, ly + 2), str(n), font=h2, fill=(255, 255, 255))
    d.text((x + 50, ly + 2), head, font=h2, fill=INK)
    ly += 40
    for line in textwrap.wrap(text, 40):
        d.text((x + 50, ly), line, font=body, fill=MUTED)
        ly += 28
    ly += 26

board.save(out, quality=92)
