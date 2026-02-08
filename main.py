from tkinter import *
from tkinter import ttk

from watermark_engine import WatermarkEngine as WME

# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()

# print(im.format, im.size, im.mode)

engine = WME("images/background_red.png")

img = engine.add_watermark(
    text="CONFIDENTIAL",
    position="center",
    font_size=106,
    opacity=128,
    padding=20
)

img.show()
