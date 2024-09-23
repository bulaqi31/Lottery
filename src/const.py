# 用于转化十六进制颜色
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

PADY = 20
PADX = 40
FONT_C = "SimHei"
FONT_E = "Arial"

BG_RGB = (255,235,240)
BG = rgb_to_hex(BG_RGB)

ROLL_TIME = 50

WITH = "With replacement"
WITHOUT = "Without replacement"