from view.winBanner import WinBanner

class BlockController:

    def __init__(self, parent, block):
        self.parent = parent
        self.block = block
        self.blockView = self.block.view
        self.parent.tag_bind(self.blockView, "<Button-1>", self.activate)
        self.parent.tag_bind(self.blockView, "<ButtonRelease-1>", self.de_activate)
        self.parent.tag_bind(self.blockView, "<B1-Motion>", self.move)
        self.currentX = 0
        self.currentY = 0
        self.currentXMovement = 0
        self.currentYMovement = 0
        self.isActivated = False
        self.hasWon = False
    
    def activate(self, event):
        self.currentX = event.x
        self.currentY = event.y
        self.isActivated = True

    def de_activate(self, event):
        self.checkWin()
        if (self.hasWon):
            self.snapPosition(self.blockView,1000,0)
        else:   
            self.snapPosition(self.blockView,self.currentXMovement, self.currentYMovement)
        self.currentXMovement = 0
        self.currentYMovement = 0
        self.isActivated = False

    def move(self, event):
        if self.isActivated and not self.hasWon:
            authorizedMovements = self.checkColision()
            dx = event.x - self.currentX 
            dy = event.y - self.currentY
            if self.block.orientation == "H":
                if "X" in authorizedMovements:
                    if dx > 0 and "R" not in authorizedMovements:
                        pass
                    elif dx < 0 and "L" not in authorizedMovements:
                        pass
                    else:
                        self.parent.move(self.blockView, dx, 0)
                        self.currentXMovement += dx
                        
                else:  
                    if dx < 0 and "R" not in authorizedMovements:
                        pass
                    elif dx > 0 and "L" not in authorizedMovements:
                        pass
                    else:
                        self.parent.move(self.blockView, dx, 0)
                        self.currentXMovement += dx

            else:
                if "X" in authorizedMovements:
                    if dy > 0 and "T" not in authorizedMovements:
                        pass
                    elif dy < 0 and "B" not in authorizedMovements:
                        pass
                    else:
                        self.parent.move(self.blockView, 0, dy)
                        self.currentYMovement += dy
                else:
                    if dy < 0 and "T" not in authorizedMovements:
                        pass
                    elif dy > 0 and "B" not in authorizedMovements:
                        pass
                    else:
                        self.parent.move(self.blockView, 0, dy)
                        self.currentYMovement += dy

            self.currentX = event.x
            self.currentY = event.y

    def checkColision(self):
        padding = 5
        border = self.parent.coords(self.parent.find_withtag("border")[0])
        rightTopBorder = [border[0]-padding,border[1]-padding,border[2]-padding,border[3]+padding]
        topBorder = [border[2]-padding,border[3]+padding,border[4]+padding,border[5]+padding]
        leftBorder = [border[4]+padding,border[5]+padding,border[6]+padding,border[7]-padding]
        bottomBorder = [border[6]+padding,border[7]-padding,border[8]-padding,border[9]-padding]
        rightBottomBorder = [border[8]-padding,border[9]-padding,border[10]-padding,border[11]+padding]

        authorizedMovements = ""
        thisCoords = self.parent.bbox(self.blockView)
        if self.block.orientation == "H":
            thisCoordsA = [int(thisCoords[0]),int(thisCoords[1]+(thisCoords[3]-thisCoords[1])/2)] #milieu gauche
            thisCoordsB = [int(thisCoords[2]),int(thisCoords[1]+(thisCoords[3]-thisCoords[1])/2)] #milieu droite
            authorizedMovements = "LR"

            if thisCoordsA[0] < leftBorder[0]:
                    authorizedMovements = "RX"
            if thisCoordsA[1] in range(int(rightTopBorder[3]),int(rightTopBorder[1])):
                if thisCoordsB[0] > rightTopBorder[0]:
                    authorizedMovements = "LX"
            if thisCoordsA[1] in range(int(rightBottomBorder[3]),int(rightBottomBorder[1])):
                if thisCoordsB[0] > rightBottomBorder[0]:
                    authorizedMovements = "LX"
            
            for b in self.block.getBlocks():
                if self.block!= b:
                    otherCoords = self.parent.bbox(b.view)
                    if thisCoordsA[1] in range(int(otherCoords[1]),int(otherCoords[3])):
                        if thisCoordsA[0] in range(int(otherCoords[0])-padding,int(otherCoords[2])+padding):
                            if authorizedMovements != "R":
                                authorizedMovements = "L"
                        if thisCoordsB[0] in range(int(otherCoords[0])-padding,int(otherCoords[2])+padding):
                            if authorizedMovements != "L":
                                authorizedMovements = "R"

        else:
            thisCoordsA = [int(thisCoords[0] + (thisCoords[2]-thisCoords[0])/2), int(thisCoords[1])] #milieu haut
            thisCoordsB = [int(thisCoords[0] + (thisCoords[2]-thisCoords[0])/2), int(thisCoords[3])] #milieu bas
            authorizedMovements = "TB"

            if thisCoordsA[1] < topBorder[1]:
                authorizedMovements = "TX"
            if thisCoordsB[1] > bottomBorder[1]:
                authorizedMovements = "BX"

            for b in self.block.getBlocks():
                if self.block != b:
                    otherCoords = self.parent.bbox(b.view)
                    if int(thisCoordsA[0]) in range(int(otherCoords[0]),int(otherCoords[2])):
                        if thisCoordsA[1] in range(int(otherCoords[1])-padding,int(otherCoords[3])+padding):
                            authorizedMovements = "B"
                        if thisCoordsB[1] in range(int(otherCoords[1])-padding,int(otherCoords[3])+padding):
                            authorizedMovements = "T"
        
        return authorizedMovements

    def snapPosition(self,blockView,dx,dy):
        if(dx != 0):
            if(dx > 0 and dx > self.block.defaultSize/2):
                factor = abs(int(dx/self.block.defaultSize))
                factor = factor -1 if(factor > 0) else 0 
                self.parent.move(blockView,self.block.defaultSize-dx+factor*self.block.defaultSize,0)
            elif(dx < 0 and dx < -self.block.defaultSize/2):
                factor = abs(int(dx/self.block.defaultSize))
                factor = factor -1 if(factor > 0) else 0 
                self.parent.move(blockView,-self.block.defaultSize-dx-factor*self.block.defaultSize,0)
            else:
                self.parent.move(blockView,-dx,0)
        elif(dy != 0):
            if(dy > 0 and dy > self.block.defaultSize/2):
                factor = abs(int(dy/self.block.defaultSize))
                factor = factor -1 if(factor > 0) else 0 
                self.parent.move(blockView,0,self.block.defaultSize-dy+factor*self.block.defaultSize)
            elif(dy < 0 and dy < -self.block.defaultSize/2):
                factor = abs(int(dy/self.block.defaultSize))
                factor = factor -1 if(factor > 0) else 0 
                self.parent.move(blockView,0,-self.block.defaultSize-dy-factor*self.block.defaultSize)
            else:
                self.parent.move(blockView,0,-dy)

    def checkWin(self):
        if self.block.isMain:
            thisCoords_RX = self.parent.bbox(self.blockView)[2]
            border_RX = self.parent.coords(self.parent.find_withtag("border")[0])[0]
            if thisCoords_RX > border_RX:
                WinBanner(self.parent)
                self.hasWon = True
