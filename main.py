from watermark_engine import WatermarkEngine as WME

engine = WME("images/background_red.png")

img = engine.add_watermark(
    text="CONFIDENTIAL",
    position="center",
    font_size=106,
    opacity=128,
    padding=20
)

img.show()
