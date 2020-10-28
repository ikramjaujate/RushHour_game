from tkinter import *

class BlockView:

    def __init__(self, parent, block):
        self.parentCanvas = parent
        self.blockModel = block
        
        self.view = self.parentCanvas.create_rectangle(
            self.blockModel.initialPosition[0] +10,
            self.blockModel.initialPosition[1] +10,
            self.blockModel.width,
            self.blockModel.height,
            fill=self.blockModel.color,
            width=2
        )

    