# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsView, QMenuBar, QAction, QToolBar)
from PyQt5.QtGui import (QPen, QColor, QBrush, QPainter)
import sys
#окна
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

window.setWindowTitle("Шахматы")
windowHeight = 600
windowWidth = windowHeight*10/6

window.resize(windowWidth+50, windowHeight+50)
scene = QtWidgets.QGraphicsScene()
view = QtWidgets.QGraphicsView(scene)

#Панели инструментов
toolbar = QToolBar(parent=window)
toolbar.addAction("профиль")

toolbar2 = QToolBar(parent=view)
toolbar2.addAction("цвет")

scene.setSceneRect(0,0,windowWidth,windowHeight)

#Доска
colorPerimeter= QtGui.QColor("#808080")
L = windowHeight/10   # L - величина клетки доски и отступа от верха доски
aboutWest = 5*L # aboutWest - отступ от западной доски
class ChessBoard:
    def __init__(self):
        self.perimeterNorth = scene.addPolygon(QtGui.QPolygonF([
                    QtCore.QPointF(aboutWest,L),
                    QtCore.QPointF(aboutWest+8*L,L),
                    QtCore.QPointF(aboutWest+8*L+L/2,L/2),
                    QtCore.QPointF(aboutWest-L/2,L/2)
                    
                 ]), 
                 pen=QtGui.QPen(QtCore.Qt.black, 1),
                 brush=QtGui.QBrush(colorPerimeter))        
        
        self.perimeterWest = scene.addPolygon(QtGui.QPolygonF([
                    QtCore.QPointF(aboutWest,L),
                    QtCore.QPointF(aboutWest,L*9),
                    QtCore.QPointF(aboutWest-L/2,L*9+L/2),
                    QtCore.QPointF(aboutWest-L/2,L/2)
                    
                 ]), 
                 pen=QtGui.QPen(QtCore.Qt.black, 1),
                 brush=QtGui.QBrush(colorPerimeter))
        self.perimeterEast = scene.addPolygon(QtGui.QPolygonF([
                    QtCore.QPointF(aboutWest+8*L,L),
                    QtCore.QPointF(aboutWest+8*L,L*9),
                    QtCore.QPointF(aboutWest+8*L+L/2,L*9+L/2),
                    QtCore.QPointF(aboutWest+8*L+L/2,L/2)
                    
                 ]), 
                 pen=QtGui.QPen(QtCore.Qt.black, 1),
                 brush=QtGui.QBrush(colorPerimeter))
        self.perimeterSouth = scene.addPolygon(QtGui.QPolygonF([
                    QtCore.QPointF(aboutWest,L*9),
                    QtCore.QPointF(aboutWest+8*L,L*9),
                    QtCore.QPointF(aboutWest+8*L+L/2,L*9+L/2),
                    QtCore.QPointF(aboutWest-L/2,L*9+L/2)
                    
                 ]), 
                 pen=QtGui.QPen(QtCore.Qt.black, 1),
                 brush=QtGui.QBrush(colorPerimeter))       

class Text:
    def __init__(self, value, name, pointSize, posX, posY):
        self.value = value
        self.name = name
        self.pointSize = pointSize
        self.posX = posX
        self.posY = posY
        self.textID =scene.addText(value, QtGui.QFont(name, pointSize=pointSize))
        self.textID.setPos(QtCore.QPointF(posX, posY))        

class Color:
    WHITE = 1
    BLACK = 2
    
    
colorWhiteSquare= QtGui.QColor('#cacaca')
colorBlackSquare= QtGui.QColor('#00ff40')
lastMoveColor = Color.BLACK
move = False
move2 = True
def mateOrStalemateWhite():
    global mateWhite,  stalemateWhite
    if defineCheckWhite(position) == True and any(listWhiteMove) == False:
        mateWhite = True
        print('белым мат')
        # Удаляем символ шаха и конца строки и пишем символ мата и результат
        f = open(r"zapisPGN.pgn",  "a")
        a = f.tell()
        f.truncate(a-2)
        f.write('# 0-1')
        f.close()
        # пишем результат в тег Result
        f = open(r"zapisPGN.pgn",  "r")
        lines = f.readlines()
        lines[6] = '[Result "0-1"]\n'
        f.close()
        f = open(r"zapisPGN.pgn",  "w")
        f.writelines(lines)
        f.close()
        # вывод модального окна об окончании партии 
        mateWhiteView = QtWidgets.QMessageBox(1, 'Мат',  'Черные поставили мат белым', buttons=QtWidgets.QMessageBox.Ok, parent=view)
        mateWhiteView.exec()
    else:
        mateWhite = False
    if defineCheckWhite(position) != True and any(listWhiteMove) == False:
        stalemateWhite = True
        print('белым пат')
        f = open(r"zapisPGN.pgn",  "a")
        f.write('1/2-1/2')
        f.close()
        # пишем результат в тег Result
        f = open(r"zapisPGN.pgn",  "r")
        lines = f.readlines()
        lines[6] = '[Result "1/2-1/2"]\n'
        f.close()
        f = open(r"zapisPGN.pgn",  "w")
        f.writelines(lines)
        f.close()
        # вывод модального окна об окончании партии 
        stalemateWhiteView = QtWidgets.QMessageBox(1, 'Пат',  'Ничья. Черный король в пате', buttons=QtWidgets.QMessageBox.Ok, parent=view)
        stalemateWhiteView.exec()
    else:
        stalemateWhite = False
        
def mateOrStalemateBlack():
    global mateBlack,  stalemateBlack
    if defineCheckBlack(position) == True and any(listBlackMove) == False:
        mateBlack = True
        print('черным мат')
        f = open(r"zapisPGN.pgn",  "a")
        a = f.tell()
        f.truncate(a-2)
        f.write('# 1-0')
        f.close()
        # пишем результат в тег Result
        f = open(r"zapisPGN.pgn",  "r")
        lines = f.readlines()
        lines[6] = '[Result "1-0"]\n'
        f.close()
        f = open(r"zapisPGN.pgn",  "w")
        f.writelines(lines)
        f.close()
        # вывод модального окна об окончании партии 
        mateBlackView = QtWidgets.QMessageBox(1, 'Мат',  'Белые поставили мат черным', buttons=QtWidgets.QMessageBox.Ok, parent=view)
        mateBlackView.exec()
    else:
        mateBlack = False
    if defineCheckBlack(position) != True and any(listBlackMove) == False:
        stalemateBlack = True
        print('черным пат')
        f = open(r"zapisPGN.pgn",  "a")
        f.write('1/2-1/2')
        f.close()
        # пишем результат в тег Result
        f = open(r"zapisPGN.pgn",  "r")
        lines = f.readlines()
        lines[6] = '[Result "1/2-1/2"]\n'
        f.close()
        f = open(r"zapisPGN.pgn",  "w")
        f.writelines(lines)
        f.close()
        # вывод модального окна об окончании партии 
        stalemateBlackView = QtWidgets.QMessageBox(1, 'Пат',  'Ничья. Белый король в пате', buttons=QtWidgets.QMessageBox.Ok, parent=view)
        stalemateBlackView.exec()
    else:
        stalemateBlack = False
        
def drawFailureMaterial():
    global failureMaterial, draw
    if (len(listWhitePieces) == 1 and len(listBlackPieces) == 1) or (len(listWhitePieces) == 1 and len(listBlackPieces) == 2 and listBlackPieces[1].pieceType == pieceType[4]) or \
    (len(listWhitePieces) == 1 and len(listBlackPieces) == 2 and listBlackPieces[1].pieceType == pieceType[5])  or (len(listBlackPieces) == 1 and len(listWhitePieces) == 2 and listWhitePieces[1].pieceType == pieceType[4]) or \
    (len(listBlackPieces) == 1 and len(listWhitePieces) == 2 and listWhitePieces[1].pieceType == pieceType[5]):
        failureMaterial = True
        draw = True
        print('ничья. недостаточно материала')
        f = open(r"zapisPGN.pgn",  "a")
        f.write('1/2-1/2')
        f.close()
        # пишем результат в тег Result
        f = open(r"zapisPGN.pgn",  "r")
        lines = f.readlines()
        lines[6] = '[Result "1/2-1/2"]\n'
        f.close()
        f = open(r"zapisPGN.pgn",  "w")
        f.writelines(lines)
        f.close()
        # вывод модального окна об окончании партии 
        failureMaterialView = QtWidgets.QMessageBox(1, 'Ньчья',  'Ничья. Недостаточно материала для постановки мата', buttons=QtWidgets.QMessageBox.Ok, parent=view)
        failureMaterialView.exec()
    else:
        failureMaterial = False
        
ruleOfFifty = 0
def drawRuleOfFifty():
    global ruleOfFifty,  draw
    if ruleOfFifty == 100:
        draw = True
        print('ничья.правило пятидесяти')
        f = open(r"zapisPGN.pgn",  "a")
        f.write('1/2-1/2')
        f.close()
        # пишем результат в тег Result
        f = open(r"zapisPGN.pgn",  "r")
        lines = f.readlines()
        lines[6] = '[Result "1/2-1/2"]\n'
        f.close()
        f = open(r"zapisPGN.pgn",  "w")
        f.writelines(lines)
        f.close()
        # вывод модального окна об окончании партии 
        ruleOfFiftyView = QtWidgets.QMessageBox(1, 'Ничья',  'Ничья. Обе стороны сделали 50 последних ходов без взятия и без хода пешкой', buttons=QtWidgets.QMessageBox.Ok, parent=view)
        ruleOfFiftyView.exec()
    else:
        draw = False
        
def iteratesThroughList(list):
    global draw        
    for i in range(len(list) -1):
        repetition =0        
        for j in range(i+1, len(list)):
            if list[i] == list[j]:
                repetition = repetition +1
                print('repetition=',  repetition)
                if repetition == 2:
                    draw = True
                    print('ничья.три повтора позиции')
                    f = open(r"zapisPGN.pgn",  "a")
                    f.write('1/2-1/2')
                    f.close()
                    # пишем результат в тег Result
                    f = open(r"zapisPGN.pgn",  "r")
                    lines = f.readlines()
                    lines[6] = '[Result "1/2-1/2"]\n'
                    f.close()
                    f = open(r"zapisPGN.pgn",  "w")
                    f.writelines(lines)
                    f.close()
                    # вывод модального окна об окончании партии                    
                    repetitionView = QtWidgets.QMessageBox(1, 'Ничья',  'Ничья. Троекратное повторение одной и той же позиции', buttons=QtWidgets.QMessageBox.Ok, parent=view)
                    repetitionView.exec()
                    break    
        
def promotion2(ww):
    global promotionSymbol
    
    promotionPiece = QtWidgets.QMessageBox(4, 'Превращение пешки',  'Выберите фигуру в которую превратится ваша пешка', parent=view)
    
    promotionPieceQueeen = promotionPiece.addButton('QUEEN---Ферзь', QtWidgets.QMessageBox.AcceptRole )
    promotionPieceRook = promotionPiece.addButton('ROOK---Ладья', QtWidgets.QMessageBox.AcceptRole )
    promotionPieceBishop = promotionPiece.addButton('BISHOP---Слон', QtWidgets.QMessageBox.AcceptRole )
    promotionPieceKnight = promotionPiece.addButton('KNIGHT---Конь', QtWidgets.QMessageBox.AcceptRole )
    promotionPiece.exec()
    whichButton = promotionPiece.clickedButton()
    if whichButton == promotionPieceQueeen:            
        ww.piece.pieceType = 'QUEEN'
        if ww.piece.color == Color.WHITE:
            ww.piece.image = imageWhiteQueen
        if ww.piece.color == Color.BLACK:
            ww.piece.image = imageBlackQueen
        promotionSymbol = '=Q'
        ww.piece.symbol = 'Q'
    
            
    if whichButton == promotionPieceRook:            
        ww.piece.pieceType = 'ROOK'
        if ww.piece.color == Color.WHITE:
            ww.piece.image = imageWhiteRook
        if ww.piece.color == Color.BLACK:
            ww.piece.image = imageBlackRook
        promotionSymbol = '=R'
        ww.piece.symbol = 'R'
            
    if whichButton == promotionPieceBishop:            
        ww.piece.pieceType = 'BISHOP'
        if ww.piece.color == Color.WHITE:
            ww.piece.image = imageWhiteBishop
        if ww.piece.color == Color.BLACK:
            ww.piece.image = imageBlackBishop
        promotionSymbol = '=B'
        ww.piece.symbol = 'B'
            
    if whichButton == promotionPieceKnight:            
        ww.piece.pieceType = 'KNIGHT'
        if ww.piece.color == Color.WHITE:
            ww.piece.image = imageWhiteKnight
        if ww.piece.color == Color.BLACK:
            ww.piece.image = imageBlackKnight
        promotionSymbol = '=N'
        ww.piece.symbol = 'N'



class Square(QtWidgets.QGraphicsRectItem):
    def __init__(self, r, color,  number, name):
        QtWidgets.QGraphicsRectItem.__init__(self)
        self.setPen(QtGui.QPen(color, 1))
        self.setBrush(QtGui.QBrush(color))
        self.setRect(r)
        self.name = name
        self.number = number
        
    def mousePressEvent(self, e):

        global move, lastMoveColor, piece1, note2EnPassant, index2JumpedField, ruleOfFifty, numberMove, note3EnPassant, allPosition
        if move == True and lastMoveColor == Color.BLACK:
            for ww in listWhiteMove:
                if ww.indexGoTo == self.number and piece1 == ww.piece:
                    position[self.number] = ww.piece
                    position[ww.indexGoOut] = 0
                    ww.piece.firstMove = True
                    ww.piece.index_board = self.number
                    promotion = False
                    ruleOfFifty = ruleOfFifty + 1
                    
                    for ii in listWhiteMove:
                            if ww.indexGoTo == ii.indexGoTo and ww.piece.pieceType == ii.piece.pieceType and ww.piece != ii.piece:                       
                                
                                if nameChessboard[ww.indexGoOut][0] == nameChessboard[ii.indexGoOut][0]:
                                    simbolSecondPossibility = nameChessboard[ww.indexGoOut][1]                                    
                                else:
                                    simbolSecondPossibility = nameChessboard[ww.indexGoOut][0]
                                break    
                            else:
                                simbolSecondPossibility = ''
                    if ww.moveType == 'simpleMove' and defineCheckBlack(position) == False and promotion == False and ww.piece.pieceType != pieceType[0]:
                        print(ww.piece.symbol + simbolSecondPossibility + self.name)
                        f = open(r"zapisPGN.pgn",  "a")
                        pgn = str(str(numberMove) +'.'+ ww.piece.symbol + simbolSecondPossibility + self.name + ' ')
                        f.write(pgn)
                        f.close()
                    if ww.moveType == 'simpleMove' and defineCheckBlack(position) == True and promotion == False and ww.piece.pieceType != pieceType[0]:
                        print(ww.piece.symbol + simbolSecondPossibility + self.name + '+')
                        f = open(r"zapisPGN.pgn",  "a")
                        pgn = str(str(numberMove) +'.'+ ww.piece.symbol + simbolSecondPossibility + self.name + '+' + ' ')
                        f.write(pgn)
                        f.close()
                    if ww.moveType == 'simpleMove' and defineCheckBlack(position) == False and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo > 76:
                        print(ww.piece.symbol + simbolSecondPossibility + self.name)
                        f = open(r"zapisPGN.pgn",  "a")
                        pgn = str(str(numberMove) +'.'+ ww.piece.symbol + simbolSecondPossibility + self.name + ' ')
                        f.write(pgn)
                        f.close()
                        ruleOfFifty = 0
                        allPosition = []
                    if ww.moveType == 'simpleMove' and defineCheckBlack(position) == True and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo > 76:
                        print(ww.piece.symbol + simbolSecondPossibility + self.name + '+')
                        f = open(r"zapisPGN.pgn",  "a")
                        pgn = str(str(numberMove) +'.'+ ww.piece.symbol + simbolSecondPossibility + self.name + '+' + ' ')
                        f.write(pgn)
                        f.close()
                        ruleOfFifty = 0
                        allPosition = []
                                
                    if ww.moveType == 'capture':
                        listBlackPieces.remove(ww.pieceCapture)
                        listCaptureWhitePieces.append(ww.pieceCapture)                        
                        PiecesView(QtGui.QPixmap(ww.pieceCapture.image).scaled(L-1,L-1), listCaptureWhitePieces.index(ww.pieceCapture)//4*L, listCaptureWhitePieces.index(ww.pieceCapture)%4*L+L )
                        if defineCheckBlack(position) == False and promotion == False and ww.piece.pieceType != pieceType[0]:
                            print(ww.piece.symbol + simbolSecondPossibility + 'x' + self.name)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ ww.piece.symbol + simbolSecondPossibility +'x' + self.name + ' ')
                            f.write(pgn)
                            f.close()
                            
                        if defineCheckBlack(position) == True and promotion == False and ww.piece.pieceType != pieceType[0]:
                            print(ww.piece.symbol + simbolSecondPossibility + 'x' + self.name + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ ww.piece.symbol + simbolSecondPossibility +'x' + self.name + '+' + ' ')
                            f.write(pgn)
                            f.close()
                        if defineCheckBlack(position) == False and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo > 76:
                            print(ww.piece.symbol + nameChessboard[ww.indexGoOut][0] + 'x' + self.name)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ ww.piece.symbol + nameChessboard[ww.indexGoOut][0] +'x' + self.name + ' ')
                            f.write(pgn)
                            f.close()
                        if defineCheckBlack(position) == True and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo > 76:
                            print(ww.piece.symbol + nameChessboard[ww.indexGoOut][0] + 'x' + self.name + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ ww.piece.symbol + nameChessboard[ww.indexGoOut][0] +'x' + self.name + '+' + ' ')
                            f.write(pgn)
                            f.close()
                        ruleOfFifty = 0
                        allPosition = []
                       
                            
                    if ww.moveType == 'enPassant':
                        position[ww.indexCapture]=0
                        listBlackPieces.remove(ww.pieceCapture)
                        listCaptureWhitePieces.append(ww.pieceCapture)                        
                        PiecesView(QtGui.QPixmap(ww.pieceCapture.image).scaled(L-1,L-1), listCaptureWhitePieces.index(ww.pieceCapture)//4*L, listCaptureWhitePieces.index(ww.pieceCapture)%4*L+L )
                        if defineCheckBlack(position) == False and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo > 76:
                            print(ww.piece.symbol + nameChessboard[ww.indexGoOut][0] + 'x' + self.name)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ ww.piece.symbol + nameChessboard[ww.indexGoOut][0] +'x' + self.name + ' ')
                            f.write(pgn)
                            f.close()
                        if defineCheckBlack(position) == True and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo > 76:
                            print(ww.piece.symbol + nameChessboard[ww.indexGoOut][0] + 'x' + self.name + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ ww.piece.symbol + nameChessboard[ww.indexGoOut][0] +'x' + self.name + '+' + ' ')
                            f.write(pgn)
                            f.close()
                        ruleOfFifty = 0
                        
                    if ww.moveType == 'castling':                            
                        position[ww.indexGoToRook] = ww.castlingRook
                        position[ww. indexGoOutRook] = 0
                        ww.castlingRook.index_board = ww.indexGoToRook                            
                        ww.castlingRook.firstMove = True
                        if defineCheckBlack(position) == False:
                            print(ww.symbol )
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ ww.symbol + ' ')
                            f.write(pgn)
                            f.close()
                        else:
                            print(ww.symbol + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ ww.symbol + '+' + ' ')
                            f.write(pgn)
                            f.close()
                            
                    if ww.piece.pieceType == pieceType[0] and ( ww.indexGoTo >= 68 and ww.indexGoTo <= 75 ):
                        promotion2(ww)
                        promotion = True
                        if ww.moveType == 'simpleMove' and defineCheckBlack(position) == False and promotion == True:
                            print(simbolSecondPossibility + self.name + promotionSymbol)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ simbolSecondPossibility + self.name + promotionSymbol + ' ')
                            f.write(pgn)
                            f.close()
                        if ww.moveType == 'simpleMove' and defineCheckBlack(position) == True and promotion == True:
                            print(simbolSecondPossibility + self.name + promotionSymbol + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ simbolSecondPossibility + self.name + promotionSymbol + '+' + ' ')
                            f.write(pgn)
                            f.close()
                        if ww.moveType == 'capture' and defineCheckBlack(position) == False and promotion == True:
                            print(nameChessboard[ww.indexGoOut][0] + 'x' + self.name + promotionSymbol)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ nameChessboard[ww.indexGoOut][0] + 'x' + self.name + promotionSymbol + ' ')
                            f.write(pgn)
                            f.close()
                        if ww.moveType == 'capture' and defineCheckBlack(position) == True and promotion == True:
                            print(nameChessboard[ww.indexGoOut][0] + 'x' + self.name + promotionSymbol + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(str(numberMove) +'.'+ nameChessboard[ww.indexGoOut][0] + 'x' + self.name + promotionSymbol + '+' + ' ')
                            f.write(pgn)
                            f.close()
                            
                        ruleOfFifty = 0
                        
                    note2EnPassant = ww.noteEnPassant
                    index2JumpedField = ww.indexJumpedField
                        
                    
                    move = False
                    
                    lastMoveColor = Color.WHITE
                    if colorBoard == Color.WHITE:
                        deleteView(listPiecesView)
                        drawPositionWhite(position)
                    else:
                        deleteView(listPiecesViewB)
                        drawPositionBlack(position)
                        
                        
                        
                    
                    
                    listWPieces(position)
                    listBPieces(position)
                    mateOrStalemateBlack()
                    drawFailureMaterial()
                    drawRuleOfFifty()
                    allPosition.append([convertPosition(position), lastMoveColor, longCastlingWhite, shortCastlingWhite, longCastlingBlack, shortCastlingBlack, note3EnPassantWhite1, note3EnPassantWhite2, note3EnPassantBlack1, note3EnPassantBlack2])
                    iteratesThroughList(allPosition)
                    print(note3EnPassantWhite1, note3EnPassantWhite2, note3EnPassantBlack1, note3EnPassantBlack2)
                    if numberMove < 51:
                        Text(pgn, "Verdana", L*0.15, 13.7*L, L*0.2*numberMove - 0.2*L)
                    if numberMove >= 51 and numberMove <= 100:
                        Text(pgn, "Verdana", L*0.15, 15.7*L, L*0.2*(numberMove-50) - 0.2*L)
                    if numberMove >= 101 and numberMove <= 150:
                        Text(pgn, "Verdana", L*0.15, 17.7*L, L*0.2*(numberMove-100) - 0.2*L)
                    
                    
                    
                    
                    
                else:
                    move = False
                    
        if lastMoveColor == Color.BLACK and move == False:
            
            for vv in listWhiteMove:
                if vv.indexGoOut == self.number:
                    move = True
                    piece1 = vv.piece                    
                    break
                else:
                    move = False
                    
        if move == True and lastMoveColor == Color.WHITE:
            
            for ww in listBlackMove:
                
                if ww.indexGoTo == self.number and piece1 == ww.piece:
                    position[self.number] = ww.piece
                    position[ww.indexGoOut] = 0
                    ww.piece.firstMove = True
                    ww.piece.index_board = self.number
                    promotion = False
                    ruleOfFifty = ruleOfFifty + 1
                    
                    for ii in listBlackMove:
                            if ww.indexGoTo == ii.indexGoTo and ww.piece.pieceType == ii.piece.pieceType and ww.piece != ii.piece:
                                
                                
                                if nameChessboard[ww.indexGoOut][0] == nameChessboard[ii.indexGoOut][0]:
                                    simbolSecondPossibility = nameChessboard[ww.indexGoOut][1]                                    
                                else:
                                    simbolSecondPossibility = nameChessboard[ww.indexGoOut][0]
                                break    
                            else:
                                simbolSecondPossibility = ''
                    if ww.moveType == 'simpleMove' and defineCheckWhite(position) == False and promotion == False and ww.piece.pieceType != pieceType[0]:
                        print(ww.piece.symbol + simbolSecondPossibility + self.name)
                        f = open(r"zapisPGN.pgn",  "a")
                        pgn = str(ww.piece.symbol + simbolSecondPossibility + self.name + ' ')
                        f.write(pgn)
                        f.close()
                    if ww.moveType == 'simpleMove' and defineCheckWhite(position) == True and promotion == False and ww.piece.pieceType != pieceType[0]:
                        print(ww.piece.symbol + simbolSecondPossibility + self.name + '+')
                        f = open(r"zapisPGN.pgn",  "a")
                        pgn = str(ww.piece.symbol + simbolSecondPossibility + self.name + '+' + ' ')
                        f.write(pgn)
                        f.close()
                    if ww.moveType == 'simpleMove' and defineCheckWhite(position) == False and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo < 180:
                        print(ww.piece.symbol + simbolSecondPossibility + self.name)
                        f = open(r"zapisPGN.pgn",  "a")
                        pgn = str(ww.piece.symbol + simbolSecondPossibility + self.name + ' ')
                        f.write(pgn)
                        f.close()
                        ruleOfFifty = 0
                        allPosition = []
                    if ww.moveType == 'simpleMove' and defineCheckWhite(position) == True and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo < 180:
                        print(ww.piece.symbol + simbolSecondPossibility + self.name + '+')
                        f = open(r"zapisPGN.pgn",  "a")
                        pgn = str(ww.piece.symbol + simbolSecondPossibility + self.name + '+',  ' ')
                        f.write(pgn)
                        f.close()
                        ruleOfFifty = 0
                        allPosition = []
                                
                    if ww.moveType == 'capture':
                        listWhitePieces.remove(ww.pieceCapture)
                        listCaptureBlackPieces.append(ww.pieceCapture)                        
                        PiecesView(QtGui.QPixmap(ww.pieceCapture.image).scaled(L-1,L-1), listCaptureBlackPieces.index(ww.pieceCapture)//4*L, listCaptureBlackPieces.index(ww.pieceCapture)%4*L+5*L )
                        if defineCheckWhite(position) == False and promotion == False and ww.piece.pieceType != pieceType[0]:
                            print(ww.piece.symbol + simbolSecondPossibility + 'x' + self.name)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(ww.piece.symbol + simbolSecondPossibility +'x' + self.name + ' ')
                            f.write(pgn)
                            f.close()
                        if defineCheckWhite(position) == True and promotion == False and ww.piece.pieceType != pieceType[0]:
                            print(ww.piece.symbol + simbolSecondPossibility + 'x' + self.name + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(ww.piece.symbol + simbolSecondPossibility +'x' + self.name + '+'+' ')
                            f.write(pgn)
                            f.close()
                        if defineCheckWhite(position) == False and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo < 180:
                            print(ww.piece.symbol +  nameChessboard[ww.indexGoOut][0] + 'x' + self.name)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(ww.piece.symbol + nameChessboard[ww.indexGoOut][0] +'x' + self.name + ' ')
                            f.write(pgn)
                            f.close()
                        if defineCheckWhite(position) == True and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo < 180:
                            print(ww.piece.symbol +  nameChessboard[ww.indexGoOut][0] + 'x' + self.name + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(ww.piece.symbol + nameChessboard[ww.indexGoOut][0] +'x' + self.name + '+' + ' ')
                            f.write(pgn)
                            f.close()
                            
                        ruleOfFifty = 0
                        allPosition = []
                       
                    if ww.moveType == 'enPassant':
                        position[ww.indexCapture]=0
                        listWhitePieces.remove(ww.pieceCapture)
                        listCaptureBlackPieces.append(ww.pieceCapture)                        
                        PiecesView(QtGui.QPixmap(ww.pieceCapture.image).scaled(L-1,L-1), listCaptureBlackPieces.index(ww.pieceCapture)//4*L, listCaptureBlackPieces.index(ww.pieceCapture)%4*L+5*L )
                        if defineCheckWhite(position) == False and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo < 180:
                            print(ww.piece.symbol +  nameChessboard[ww.indexGoOut][0] + 'x' + self.name)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(ww.piece.symbol + nameChessboard[ww.indexGoOut][0] +'x' + self.name + ' ')
                            f.write(pgn)
                            f.close()
                        if defineCheckWhite(position) == True and promotion == False and ww.piece.pieceType == pieceType[0] and ww.indexGoTo < 180:
                            print(ww.piece.symbol +  nameChessboard[ww.indexGoOut][0] + 'x' + self.name + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(ww.piece.symbol + nameChessboard[ww.indexGoOut][0] +'x' + self.name + '+' + ' ')
                            f.write(pgn)
                            f.close()
                        ruleOfFifty
                            
                    if ww.moveType == 'castling':                            
                        position[ww.indexGoToRook] = ww.castlingRook
                        position[ww. indexGoOutRook] = 0
                        ww.castlingRook.index_board = ww.indexGoToRook                            
                        ww.castlingRook.firstMove = True
                        if defineCheckWhite(position) == False:
                            print(ww.symbol )
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(ww.symbol + ' ')
                            f.write(pgn)
                            f.close()
                        else:
                            print(ww.symbol + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(ww.symbol + '+' + ' ')
                            f.write(pgn)
                            f.close()
                    
                    if ww.piece.pieceType == pieceType[0] and ( ww.indexGoTo >= 180 and ww.indexGoTo <= 187 ):
                        promotion2(ww)
                        promotion = True
                        if ww.moveType == 'simpleMove' and defineCheckWhite(position) == False and promotion == True:
                            print(simbolSecondPossibility + self.name + promotionSymbol)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(simbolSecondPossibility + self.name + promotionSymbol + ' ')
                            f.write(pgn)
                            f.close()
                        if ww.moveType == 'simpleMove' and defineCheckWhite(position) == True and promotion == True:
                            print(simbolSecondPossibility + self.name + promotionSymbol + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(simbolSecondPossibility + self.name + promotionSymbol + '+' + ' ')
                            f.write(pgn)
                            f.close()
                        if ww.moveType == 'capture' and defineCheckWhite(position) == False and promotion == True:
                            print(nameChessboard[ww.indexGoOut][0] + 'x' + self.name + promotionSymbol)
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(nameChessboard[ww.indexGoOut][0] + 'x' + self.name + promotionSymbol + ' ')
                            f.write(pgn)
                            f.close()
                        if ww.moveType == 'capture' and defineCheckWhite(position) == True and promotion == True:
                            print(nameChessboard[ww.indexGoOut][0] + 'x' + self.name + promotionSymbol + '+')
                            f = open(r"zapisPGN.pgn",  "a")
                            pgn = str(nameChessboard[ww.indexGoOut][0] + 'x' + self.name + promotionSymbol + '+' + ' ')
                            f.write(pgn)
                            f.close()
                        ruleOfFifty = 0
                        
                    note2EnPassant = ww.noteEnPassant
                    index2JumpedField = ww.indexJumpedField
                    
                   
                    
                    move = False
                    
                    lastMoveColor = Color.BLACK
                    if colorBoard == Color.WHITE:
                        deleteView(listPiecesView)
                        drawPositionWhite(position)
                    else:
                        deleteView(listPiecesViewB)
                        drawPositionBlack(position)
                    
                    
                    listWPieces(position)
                    listBPieces(position)
                    mateOrStalemateWhite()
                    drawFailureMaterial()
                    drawRuleOfFifty()
                    allPosition.append([convertPosition(position), lastMoveColor, longCastlingWhite, shortCastlingWhite, longCastlingBlack, shortCastlingBlack, note3EnPassantWhite1, note3EnPassantWhite2, note3EnPassantBlack1, note3EnPassantBlack2])
                    iteratesThroughList(allPosition)
                    print(note3EnPassantWhite1, note3EnPassantWhite2, note3EnPassantBlack1, note3EnPassantBlack2)
                    if numberMove < 51:
                        Text(pgn, "Verdana", L*0.15, 14.7*L, L*0.2*numberMove - 0.2*L)
                    if numberMove >= 51 and numberMove <= 100:
                        Text(pgn, "Verdana", L*0.15, 16.7*L, L*0.2*(numberMove-50) - 0.2*L)
                    if numberMove >= 101 and numberMove <= 150:
                        Text(pgn, "Verdana", L*0.15, 18.7*L, L*0.2*(numberMove-100) - 0.2*L)
                        
                    
                    
                    
                    numberMove = numberMove +1
                else:
                    move = False
                    
                    
        if lastMoveColor == Color.WHITE and move == False:
            
            for vv in listBlackMove:
                if vv.indexGoOut == self.number:
                    move = True
                    piece1 = vv.piece                    
                    break
                else:
                    move = False           
     
        e.accept()

# кнопка переварачивания доски     
class Button(QtWidgets.QGraphicsRectItem):
    
    def __init__(self, r, color):
        QtWidgets.QGraphicsRectItem.__init__(self)
        self.setPen(QtGui.QPen())
        self.setBrush(QtGui.QBrush(color))
        self.setRect(r)        
    def mousePressEvent(self, e):        
        rotate()       
        e.accept()
        
buttonRotate = Button(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare)
buttonRotate.setPos(QtCore.QPointF(aboutWest,     9.6*L))
scene.addItem(buttonRotate)
text_1 = 'Перевернуть доску'
buttonRotate.setToolTip(text_1)
scene.addLine(aboutWest+L/3, 9.7*L, aboutWest+L/3, 10.5*L )
scene.addLine(aboutWest+L*2/3, 9.7*L, aboutWest+L*2/3, 10.5*L )
scene.addLine(aboutWest+L/3, 9.7*L, aboutWest+L/3-0.1*L, 9.8*L )
scene.addLine(aboutWest+L/3, 9.7*L, aboutWest+L/3+0.1*L, 9.8*L )
scene.addLine(aboutWest+L*2/3+0.1*L, 10.4*L, aboutWest+L*2/3, 10.5*L )
scene.addLine(aboutWest+L*2/3-0.1*L, 10.4*L, aboutWest+L*2/3, 10.5*L )



#Фигуры

pieceType = ['PAWN','KING','QUEEN','ROOK', 'KNIGHT', 'BISHOP']
firstMove = [True, False] # True - фигура ходила, False - фигура не ходила

incrementQueen = [1, 15, 16, 17, -15, -16, -17, -1]
incrementBishop = [15, 17, -15, -17]
incrementRook = [1, 16, -1, -16, 0]
incrementKnight = [14, 18, 33, 31, -14, -18, -33, -31]
incrementWhitePawn = [-16, -15, -17, -32]
incrementBlackPawn = [16, 15, 17, 32]

nameChessboard = {68 : 'a8',  69 : 'b8', 70 : 'c8',  71 : 'd8', 72 : 'e8',  73 : 'f8', 74 : 'g8',  75 : 'h8', \
                    84 : 'a7',  85 : 'b7', 86 : 'c7',  87 : 'd7', 88 : 'e7',  89 : 'f7', 90 : 'g7',  91 : 'h7', \
                    100 : 'a6',  101 : 'b6', 102 : 'c6',  103 : 'd6', 104 : 'e6',  105 : 'f6', 106 : 'g6',  107 : 'h6', \
                    116 : 'a5',  117 : 'b5', 118 : 'c5',  119 : 'd5', 120 : 'e5',  121 : 'f5', 122 : 'g5',  123 : 'h5', \
                    132 : 'a4',  133 : 'b4', 134 : 'c4',  135 : 'd4', 136 : 'e4',  137 : 'f4', 138 : 'g4',  139 : 'h4', \
                    148 : 'a3',  149 : 'b3', 150 : 'c3',  151 : 'd3', 152 : 'e3',  153 : 'f3', 154 : 'g3',  155 : 'h3', \
                    164 : 'a2',  165 : 'b2', 166 : 'c2',  167 : 'd2', 168 : 'e2',  169 : 'f2', 170 : 'g2',  171 : 'h2', \
                    180 : 'a1',  181 : 'b1', 182 : 'c1',  183 : 'd1', 184 : 'e1',  185 : 'f1', 186 : 'g1',  187 : 'h1'}

imageWhiteRook = "WhiteRook.gif"
imageWhiteKnight = "WhiteKnight.gif"
imageWhiteBishop = "WhiteBishop.gif"
imageWhiteQueen = "WhiteQueen.gif"
imageWhiteKing = "WhiteKing.gif"
imageWhitePawn = "WhitePawn.gif"

imageBlackRook = "BlackRook.gif"
imageBlackKnight = "BlackKnight.gif"
imageBlackBishop = "BlackBishop.gif"
imageBlackQueen = "BlackQueen.gif"
imageBlackKing = "BlackKing.gif"
imageBlackPawn = "BlackPawn.gif"

position = ['OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 0, 0, 0, 0, 0, 0, 0, 0, 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 0, 0, 0, 0, 0, 0, 0, 0, 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 0, 0, 0, 0, 0, 0, 0, 0, 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 0, 0, 0, 0, 0, 0, 0, 0, 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 0, 0, 0, 0, 0, 0, 0, 0, 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 0, 0, 0, 0, 0, 0, 0, 0, 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 0, 0, 0, 0, 0, 0, 0, 0, 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 0, 0, 0, 0, 0, 0, 0, 0, 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT',\
            'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT', 'OUT']
            
            

def convertPieces(cp):
    if cp.color == Color.WHITE and cp.pieceType == pieceType[1]:
        return 1
    if cp.color == Color.WHITE and cp.pieceType == pieceType[2]:
        return 2
    if cp.color == Color.WHITE and cp.pieceType == pieceType[3]:
        return 3
    if cp.color == Color.WHITE and cp.pieceType == pieceType[4]:
        return 4
    if cp.color == Color.WHITE and cp.pieceType == pieceType[5]:
        return 5
    if cp.color == Color.WHITE and cp.pieceType == pieceType[0]:
        return 6
    if cp.color == Color.BLACK and cp.pieceType == pieceType[1]:
        return 7
    if cp.color == Color.BLACK and cp.pieceType == pieceType[2]:
        return 8
    if cp.color == Color.BLACK and cp.pieceType == pieceType[3]:
        return 9
    if cp.color == Color.BLACK and cp.pieceType == pieceType[4]:
        return 10
    if cp.color == Color.BLACK and cp.pieceType == pieceType[5]:
        return 11
    if cp.color == Color.BLACK and cp.pieceType == pieceType[0]:
        return 12
    
    
def convertPosition(position):
    global positionNew
    positionNew = []
    for t1 in range(68, 76):
        if position[t1] == 0 and position[t1] != 'OUT':
            positionNew.append(0)
        else:
            positionNew.append(convertPieces(position[t1]))
    for t2 in range(84, 92):
        if position[t2] == 0 and position[t2] != 'OUT':
            positionNew.append(0)
        else:
            positionNew.append(convertPieces(position[t2]))
    for t3 in range(100, 108):
        if position[t3] == 0 and position[t3] != 'OUT':
            positionNew.append(0)
        else:
            positionNew.append(convertPieces(position[t3]))
    for t4 in range(116, 124):
        if position[t4] == 0 and position[t4] != 'OUT':
            positionNew.append(0)
        else:
            positionNew.append(convertPieces(position[t4]))
    for t5 in range(132, 140):
        if position[t5] == 0 and position[t5] != 'OUT':
            positionNew.append(0)
        else:
            positionNew.append(convertPieces(position[t5]))
    for t6 in range(148, 156):
        if position[t6] == 0 and position[t6] != 'OUT':
            positionNew.append(0)
        else:
            positionNew.append(convertPieces(position[t6]))
    for t7 in range(164, 172):
        if position[t7] == 0 and position[t7] != 'OUT':
            positionNew.append(0)
        else:
            positionNew.append(convertPieces(position[t7]))
    for t8 in range(180, 188):
        if position[t8] == 0 and position[t8] != 'OUT':
            positionNew.append(0)
        else:
            positionNew.append(convertPieces(position[t8]))
    return positionNew
            

board = ChessBoard()

square_a8 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 68,  'a8')
square_a8.setPos(QtCore.QPointF(aboutWest,     L))
scene.addItem(square_a8)

square_b8 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 69,  'b8')
square_b8.setPos(QtCore.QPointF(aboutWest+L,     L))
scene.addItem(square_b8)

square_c8 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 70,  'с8')
square_c8.setPos(QtCore.QPointF(aboutWest+2*L,     L))
scene.addItem(square_c8)

square_d8 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 71,  'd8')
square_d8.setPos(QtCore.QPointF(aboutWest+3*L,     L))
scene.addItem(square_d8)

square_e8 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 72,  'e8')
square_e8.setPos(QtCore.QPointF(aboutWest+4*L,     L))
scene.addItem(square_e8)

square_f8 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 73,  'f8')
square_f8.setPos(QtCore.QPointF(aboutWest+5*L,     L))
scene.addItem(square_f8)

square_g8 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 74,  'g8')
square_g8.setPos(QtCore.QPointF(aboutWest+6*L,     L))
scene.addItem(square_g8)

square_h8 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 75,  'h8')
square_h8.setPos(QtCore.QPointF(aboutWest+7*L,     L))
scene.addItem(square_h8)

square_a7 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 84,  'a7')
square_a7.setPos(QtCore.QPointF(aboutWest,     2*L))
scene.addItem(square_a7)

square_b7 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 85,  'b7')
square_b7.setPos(QtCore.QPointF(aboutWest+L,     2*L))
scene.addItem(square_b7)

square_c7 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 86,  'с7')
square_c7.setPos(QtCore.QPointF(aboutWest+2*L,     2*L))
scene.addItem(square_c7)

square_d7 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 87,  'd7')
square_d7.setPos(QtCore.QPointF(aboutWest+3*L,     2*L))
scene.addItem(square_d7)

square_e7 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 88,  'e7')
square_e7.setPos(QtCore.QPointF(aboutWest+4*L,     2*L))
scene.addItem(square_e7)

square_f7 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 89,  'f7')
square_f7.setPos(QtCore.QPointF(aboutWest+5*L,     2*L))
scene.addItem(square_f7)

square_g7 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 90,  'g7')
square_g7.setPos(QtCore.QPointF(aboutWest+6*L,     2*L))
scene.addItem(square_g7)

square_h7 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 91,  'h7')
square_h7.setPos(QtCore.QPointF(aboutWest+7*L,     2*L))
scene.addItem(square_h7)

square_a6 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 100,  'a6')
square_a6.setPos(QtCore.QPointF(aboutWest,     3*L))
scene.addItem(square_a6)

square_b6 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 101,  'b6')
square_b6.setPos(QtCore.QPointF(aboutWest+L,     3*L))
scene.addItem(square_b6)

square_c6 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 102,  'с6')
square_c6.setPos(QtCore.QPointF(aboutWest+2*L,     3*L))
scene.addItem(square_c6)

square_d6 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 103,  'd6')
square_d6.setPos(QtCore.QPointF(aboutWest+3*L,     3*L))
scene.addItem(square_d6)

square_e6 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 104,  'e6')
square_e6.setPos(QtCore.QPointF(aboutWest+4*L,     3*L))
scene.addItem(square_e6)

square_f6 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 105,  'f6')
square_f6.setPos(QtCore.QPointF(aboutWest+5*L,     3*L))
scene.addItem(square_f6)

square_g6 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 106,  'g6')
square_g6.setPos(QtCore.QPointF(aboutWest+6*L,     3*L))
scene.addItem(square_g6)

square_h6 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 107,  'h6')
square_h6.setPos(QtCore.QPointF(aboutWest+7*L,     3*L))
scene.addItem(square_h6)

square_a5 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 116,  'a5')
square_a5.setPos(QtCore.QPointF(aboutWest,     4*L))
scene.addItem(square_a5)

square_b5 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 117,  'b5')
square_b5.setPos(QtCore.QPointF(aboutWest+L,     4*L))
scene.addItem(square_b5)

square_c5 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 118,  'с5')
square_c5.setPos(QtCore.QPointF(aboutWest+2*L,     4*L))
scene.addItem(square_c5)

square_d5 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 119,  'd5')
square_d5.setPos(QtCore.QPointF(aboutWest+3*L,     4*L))
scene.addItem(square_d5)

square_e5 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 120,  'e5')
square_e5.setPos(QtCore.QPointF(aboutWest+4*L,     4*L))
scene.addItem(square_e5)

square_f5 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 121,  'f5')
square_f5.setPos(QtCore.QPointF(aboutWest+5*L,     4*L))
scene.addItem(square_f5)

square_g5 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 122,  'g5')
square_g5.setPos(QtCore.QPointF(aboutWest+6*L,     4*L))
scene.addItem(square_g5)

square_h5 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 123,  'h5')
square_h5.setPos(QtCore.QPointF(aboutWest+7*L,     4*L))
scene.addItem(square_h5)

square_a4 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 132,  'a4')
square_a4.setPos(QtCore.QPointF(aboutWest,     5*L))
scene.addItem(square_a4)

square_b4 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 133,  'b4')
square_b4.setPos(QtCore.QPointF(aboutWest+L,     5*L))
scene.addItem(square_b4)

square_c4 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 134,  'с4')
square_c4.setPos(QtCore.QPointF(aboutWest+2*L,     5*L))
scene.addItem(square_c4)

square_d4 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 135,  'd4')
square_d4.setPos(QtCore.QPointF(aboutWest+3*L,     5*L))
scene.addItem(square_d4)

square_e4 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 136,  'e4')
square_e4.setPos(QtCore.QPointF(aboutWest+4*L,     5*L))
scene.addItem(square_e4)

square_f4 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 137,  'f4')
square_f4.setPos(QtCore.QPointF(aboutWest+5*L,     5*L))
scene.addItem(square_f4)

square_g4 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 138,  'g4')
square_g4.setPos(QtCore.QPointF(aboutWest+6*L,     5*L))
scene.addItem(square_g4)

square_h4 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 139,  'h4')
square_h4.setPos(QtCore.QPointF(aboutWest+7*L,     5*L))
scene.addItem(square_h4)

square_a3 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 148,  'a3')
square_a3.setPos(QtCore.QPointF(aboutWest,     6*L))
scene.addItem(square_a3)

square_b3 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 149,  'b3')
square_b3.setPos(QtCore.QPointF(aboutWest+L,     6*L))
scene.addItem(square_b3)

square_c3 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 150,  'с3')
square_c3.setPos(QtCore.QPointF(aboutWest+2*L,     6*L))
scene.addItem(square_c3)

square_d3 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 151,  'd3')
square_d3.setPos(QtCore.QPointF(aboutWest+3*L,     6*L))
scene.addItem(square_d3)

square_e3 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 152,  'e3')
square_e3.setPos(QtCore.QPointF(aboutWest+4*L,     6*L))
scene.addItem(square_e3)

square_f3 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 153,  'f3')
square_f3.setPos(QtCore.QPointF(aboutWest+5*L,     6*L))
scene.addItem(square_f3)

square_g3 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 154,  'g3')
square_g3.setPos(QtCore.QPointF(aboutWest+6*L,     6*L))
scene.addItem(square_g3)

square_h3 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 155,  'h3')
square_h3.setPos(QtCore.QPointF(aboutWest+7*L,     6*L))
scene.addItem(square_h3)

square_a2 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 164,  'a2')
square_a2.setPos(QtCore.QPointF(aboutWest,     7*L))
scene.addItem(square_a2)

square_b2 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 165,  'b2')
square_b2.setPos(QtCore.QPointF(aboutWest+L,     7*L))
scene.addItem(square_b2)

square_c2 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 166,  'с2')
square_c2.setPos(QtCore.QPointF(aboutWest+2*L,     7*L))
scene.addItem(square_c2)

square_d2 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 167,  'd2')
square_d2.setPos(QtCore.QPointF(aboutWest+3*L,     7*L))
scene.addItem(square_d2)

square_e2 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 168,  'e2')
square_e2.setPos(QtCore.QPointF(aboutWest+4*L,     7*L))
scene.addItem(square_e2)

square_f2 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 169,  'f2')
square_f2.setPos(QtCore.QPointF(aboutWest+5*L,     7*L))
scene.addItem(square_f2)

square_g2 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 170,  'g2')
square_g2.setPos(QtCore.QPointF(aboutWest+6*L,     7*L))
scene.addItem(square_g2)

square_h2 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 171,  'h2')
square_h2.setPos(QtCore.QPointF(aboutWest+7*L,     7*L))
scene.addItem(square_h2)

square_a1 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 180,  'a1')
square_a1.setPos(QtCore.QPointF(aboutWest,     8*L))
scene.addItem(square_a1)

square_b1 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 181,  'b1')
square_b1.setPos(QtCore.QPointF(aboutWest+L,     8*L))
scene.addItem(square_b1)

square_c1 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 182,  'с1')
square_c1.setPos(QtCore.QPointF(aboutWest+2*L,     8*L))
scene.addItem(square_c1)

square_d1 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 183,  'd1')
square_d1.setPos(QtCore.QPointF(aboutWest+3*L,     8*L))
scene.addItem(square_d1)

square_e1 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 184,  'e1')
square_e1.setPos(QtCore.QPointF(aboutWest+4*L,     8*L))
scene.addItem(square_e1)

square_f1 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 185,  'f1')
square_f1.setPos(QtCore.QPointF(aboutWest+5*L,     8*L))
scene.addItem(square_f1)

square_g1 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorBlackSquare, 186,  'g1')
square_g1.setPos(QtCore.QPointF(aboutWest+6*L,     8*L))
scene.addItem(square_g1)

square_h1 = Square(QtCore.QRectF(0.0, 0.0, L, L), colorWhiteSquare, 187,  'h1')
square_h1.setPos(QtCore.QPointF(aboutWest+7*L,     8*L))
scene.addItem(square_h1)

def squareRotateBlack():    
    square_h1.setPos(QtCore.QPointF(aboutWest,     L))
    square_g1.setPos(QtCore.QPointF(aboutWest+L,     L))
    square_f1.setPos(QtCore.QPointF(aboutWest+2*L,     L))
    square_e1.setPos(QtCore.QPointF(aboutWest+3*L,     L))
    square_d1.setPos(QtCore.QPointF(aboutWest+4*L,     L))
    square_c1.setPos(QtCore.QPointF(aboutWest+5*L,     L))
    square_b1.setPos(QtCore.QPointF(aboutWest+6*L,     L))
    square_a1.setPos(QtCore.QPointF(aboutWest+7*L,     L))
    square_h2.setPos(QtCore.QPointF(aboutWest,     2*L))
    square_g2.setPos(QtCore.QPointF(aboutWest+L,     2*L))
    square_f2.setPos(QtCore.QPointF(aboutWest+2*L,     2*L))
    square_e2.setPos(QtCore.QPointF(aboutWest+3*L,     2*L))
    square_d2.setPos(QtCore.QPointF(aboutWest+4*L,     2*L))
    square_c2.setPos(QtCore.QPointF(aboutWest+5*L,     2*L))
    square_b2.setPos(QtCore.QPointF(aboutWest+6*L,     2*L))
    square_a2.setPos(QtCore.QPointF(aboutWest+7*L,     2*L))
    square_h3.setPos(QtCore.QPointF(aboutWest,     3*L))
    square_g3.setPos(QtCore.QPointF(aboutWest+L,     3*L))
    square_f3.setPos(QtCore.QPointF(aboutWest+2*L,     3*L))
    square_e3.setPos(QtCore.QPointF(aboutWest+3*L,     3*L))
    square_d3.setPos(QtCore.QPointF(aboutWest+4*L,     3*L))
    square_c3.setPos(QtCore.QPointF(aboutWest+5*L,     3*L))
    square_b3.setPos(QtCore.QPointF(aboutWest+6*L,     3*L))
    square_a3.setPos(QtCore.QPointF(aboutWest+7*L,     3*L))
    square_h4.setPos(QtCore.QPointF(aboutWest,     4*L))
    square_g4.setPos(QtCore.QPointF(aboutWest+L,     4*L))
    square_f4.setPos(QtCore.QPointF(aboutWest+2*L,     4*L))
    square_e4.setPos(QtCore.QPointF(aboutWest+3*L,     4*L))
    square_d4.setPos(QtCore.QPointF(aboutWest+4*L,     4*L))
    square_c4.setPos(QtCore.QPointF(aboutWest+5*L,     4*L))
    square_b4.setPos(QtCore.QPointF(aboutWest+6*L,     4*L))
    square_a4.setPos(QtCore.QPointF(aboutWest+7*L,     4*L))
    square_h5.setPos(QtCore.QPointF(aboutWest,     5*L))
    square_g5.setPos(QtCore.QPointF(aboutWest+L,     5*L))
    square_f5.setPos(QtCore.QPointF(aboutWest+2*L,     5*L))
    square_e5.setPos(QtCore.QPointF(aboutWest+3*L,     5*L))
    square_d5.setPos(QtCore.QPointF(aboutWest+4*L,     5*L))
    square_c5.setPos(QtCore.QPointF(aboutWest+5*L,     5*L))
    square_b5.setPos(QtCore.QPointF(aboutWest+6*L,     5*L))
    square_a5.setPos(QtCore.QPointF(aboutWest+7*L,     5*L))
    square_h6.setPos(QtCore.QPointF(aboutWest,     6*L))
    square_g6.setPos(QtCore.QPointF(aboutWest+L,     6*L))
    square_f6.setPos(QtCore.QPointF(aboutWest+2*L,     6*L))
    square_e6.setPos(QtCore.QPointF(aboutWest+3*L,     6*L))
    square_d6.setPos(QtCore.QPointF(aboutWest+4*L,     6*L))
    square_c6.setPos(QtCore.QPointF(aboutWest+5*L,     6*L))
    square_b6.setPos(QtCore.QPointF(aboutWest+6*L,     6*L))
    square_a6.setPos(QtCore.QPointF(aboutWest+7*L,     6*L))
    square_h7.setPos(QtCore.QPointF(aboutWest,     7*L))
    square_g7.setPos(QtCore.QPointF(aboutWest+L,     7*L))
    square_f7.setPos(QtCore.QPointF(aboutWest+2*L,     7*L))
    square_e7.setPos(QtCore.QPointF(aboutWest+3*L,     7*L))
    square_d7.setPos(QtCore.QPointF(aboutWest+4*L,     7*L))
    square_c7.setPos(QtCore.QPointF(aboutWest+5*L,     7*L))
    square_b7.setPos(QtCore.QPointF(aboutWest+6*L,     7*L))
    square_a7.setPos(QtCore.QPointF(aboutWest+7*L,     7*L))
    square_h8.setPos(QtCore.QPointF(aboutWest,     8*L))
    square_g8.setPos(QtCore.QPointF(aboutWest+L,     8*L))
    square_f8.setPos(QtCore.QPointF(aboutWest+2*L,     8*L))
    square_e8.setPos(QtCore.QPointF(aboutWest+3*L,     8*L))
    square_d8.setPos(QtCore.QPointF(aboutWest+4*L,     8*L))
    square_c8.setPos(QtCore.QPointF(aboutWest+5*L,     8*L))
    square_b8.setPos(QtCore.QPointF(aboutWest+6*L,     8*L))
    square_a8.setPos(QtCore.QPointF(aboutWest+7*L,     8*L))


def squareRotateWhite():    
    square_a8.setPos(QtCore.QPointF(aboutWest,     L))    
    square_b8.setPos(QtCore.QPointF(aboutWest+L,     L))    
    square_c8.setPos(QtCore.QPointF(aboutWest+2*L,     L))   
    square_d8.setPos(QtCore.QPointF(aboutWest+3*L,     L))    
    square_e8.setPos(QtCore.QPointF(aboutWest+4*L,     L))    
    square_f8.setPos(QtCore.QPointF(aboutWest+5*L,     L))    
    square_g8.setPos(QtCore.QPointF(aboutWest+6*L,     L))    
    square_h8.setPos(QtCore.QPointF(aboutWest+7*L,     L))    
    square_a7.setPos(QtCore.QPointF(aboutWest,     2*L))    
    square_b7.setPos(QtCore.QPointF(aboutWest+L,     2*L))    
    square_c7.setPos(QtCore.QPointF(aboutWest+2*L,     2*L))    
    square_d7.setPos(QtCore.QPointF(aboutWest+3*L,     2*L))    
    square_e7.setPos(QtCore.QPointF(aboutWest+4*L,     2*L))    
    square_f7.setPos(QtCore.QPointF(aboutWest+5*L,     2*L))    
    square_g7.setPos(QtCore.QPointF(aboutWest+6*L,     2*L))    
    square_h7.setPos(QtCore.QPointF(aboutWest+7*L,     2*L))    
    square_a6.setPos(QtCore.QPointF(aboutWest,     3*L))   
    square_b6.setPos(QtCore.QPointF(aboutWest+L,     3*L))    
    square_c6.setPos(QtCore.QPointF(aboutWest+2*L,     3*L))   
    square_d6.setPos(QtCore.QPointF(aboutWest+3*L,     3*L))    
    square_e6.setPos(QtCore.QPointF(aboutWest+4*L,     3*L))    
    square_f6.setPos(QtCore.QPointF(aboutWest+5*L,     3*L))    
    square_g6.setPos(QtCore.QPointF(aboutWest+6*L,     3*L))    
    square_h6.setPos(QtCore.QPointF(aboutWest+7*L,     3*L))    
    square_a5.setPos(QtCore.QPointF(aboutWest,     4*L))    
    square_b5.setPos(QtCore.QPointF(aboutWest+L,     4*L))    
    square_c5.setPos(QtCore.QPointF(aboutWest+2*L,     4*L))    
    square_d5.setPos(QtCore.QPointF(aboutWest+3*L,     4*L))    
    square_e5.setPos(QtCore.QPointF(aboutWest+4*L,     4*L))   
    square_f5.setPos(QtCore.QPointF(aboutWest+5*L,     4*L))    
    square_g5.setPos(QtCore.QPointF(aboutWest+6*L,     4*L))    
    square_h5.setPos(QtCore.QPointF(aboutWest+7*L,     4*L))    
    square_a4.setPos(QtCore.QPointF(aboutWest,     5*L))    
    square_b4.setPos(QtCore.QPointF(aboutWest+L,     5*L))    
    square_c4.setPos(QtCore.QPointF(aboutWest+2*L,     5*L))    
    square_d4.setPos(QtCore.QPointF(aboutWest+3*L,     5*L))    
    square_e4.setPos(QtCore.QPointF(aboutWest+4*L,     5*L))    
    square_f4.setPos(QtCore.QPointF(aboutWest+5*L,     5*L))    
    square_g4.setPos(QtCore.QPointF(aboutWest+6*L,     5*L))    
    square_h4.setPos(QtCore.QPointF(aboutWest+7*L,     5*L))   
    square_a3.setPos(QtCore.QPointF(aboutWest,     6*L))    
    square_b3.setPos(QtCore.QPointF(aboutWest+L,     6*L))    
    square_c3.setPos(QtCore.QPointF(aboutWest+2*L,     6*L))    
    square_d3.setPos(QtCore.QPointF(aboutWest+3*L,     6*L))    
    square_e3.setPos(QtCore.QPointF(aboutWest+4*L,     6*L))    
    square_f3.setPos(QtCore.QPointF(aboutWest+5*L,     6*L))    
    square_g3.setPos(QtCore.QPointF(aboutWest+6*L,     6*L))   
    square_h3.setPos(QtCore.QPointF(aboutWest+7*L,     6*L))   
    square_a2.setPos(QtCore.QPointF(aboutWest,     7*L))    
    square_b2.setPos(QtCore.QPointF(aboutWest+L,     7*L))    
    square_c2.setPos(QtCore.QPointF(aboutWest+2*L,     7*L))    
    square_d2.setPos(QtCore.QPointF(aboutWest+3*L,     7*L))    
    square_e2.setPos(QtCore.QPointF(aboutWest+4*L,     7*L))    
    square_f2.setPos(QtCore.QPointF(aboutWest+5*L,     7*L))    
    square_g2.setPos(QtCore.QPointF(aboutWest+6*L,     7*L))    
    square_h2.setPos(QtCore.QPointF(aboutWest+7*L,     7*L))    
    square_a1.setPos(QtCore.QPointF(aboutWest,     8*L))    
    square_b1.setPos(QtCore.QPointF(aboutWest+L,     8*L))    
    square_c1.setPos(QtCore.QPointF(aboutWest+2*L,     8*L))    
    square_d1.setPos(QtCore.QPointF(aboutWest+3*L,     8*L))    
    square_e1.setPos(QtCore.QPointF(aboutWest+4*L,     8*L))    
    square_f1.setPos(QtCore.QPointF(aboutWest+5*L,     8*L))    
    square_g1.setPos(QtCore.QPointF(aboutWest+6*L,     8*L))  
    square_h1.setPos(QtCore.QPointF(aboutWest+7*L,     8*L))    


    
#    global textH, textG, textF, textE, textD, textC, textB, textA,  textAb, textHb, textGb, textFb, textEb, textDb, textCb, textBb, textAb, \
#    text1, text2, text3, text4, text5, text6, text7, text8, text1b, text2b, text3b, text4b, text5b, text6b, text7b, text8b    
textH = Text("H", "Verdana", L*0.4, aboutWest+0.2*L+7*L, L*8.85)    
textG = Text("G", "Verdana", L*0.4, aboutWest+0.2*L+6*L, L*8.85)    
textF = Text("F", "Verdana", L*0.4, aboutWest+0.2*L+5*L, L*8.85)   
textE = Text("E", "Verdana", L*0.4, aboutWest+0.2*L+4*L, L*8.85)    
textD = Text("D", "Verdana", L*0.4, aboutWest+0.2*L+3*L, L*8.85)   
textC = Text("C", "Verdana", L*0.4, aboutWest+0.2*L+2*L, L*8.85)   
textB = Text("B", "Verdana", L*0.4, aboutWest+0.2*L+L,   L*8.85)   
textA = Text("A", "Verdana", L*0.4, aboutWest+0.2*L,     L*8.85)   

textHb = Text("H", "Verdana", L*0.4, aboutWest+0.7*L+7*L, 1.17*L)  
textGb = Text("G", "Verdana", L*0.4, aboutWest+0.7*L+6*L, 1.17*L)  
textFb = Text("F", "Verdana", L*0.4, aboutWest+0.7*L+5*L, 1.17*L)   
textEb = Text("E", "Verdana", L*0.4, aboutWest+0.7*L+4*L, 1.17*L)   
textDb = Text("D", "Verdana", L*0.4, aboutWest+0.7*L+3*L, 1.17*L)   
textCb = Text("C", "Verdana", L*0.4, aboutWest+0.7*L+2*L, 1.17*L)    
textBb = Text("B", "Verdana", L*0.4, aboutWest+0.7*L+L,   1.17*L)   
textAb = Text("A", "Verdana", L*0.4, aboutWest+0.7*L,     1.17*L)  

textAb.textID.setRotation(180)
textBb.textID.setRotation(180)
textCb.textID.setRotation(180)
textDb.textID.setRotation(180)
textEb.textID.setRotation(180)
textFb.textID.setRotation(180)
textGb.textID.setRotation(180)
textHb.textID.setRotation(180)

text1 = Text("1", "Verdana", L*0.4, aboutWest-0.46*L, L*8.12) 
text2 = Text("2", "Verdana", L*0.4, aboutWest-0.46*L, L*7.12)   
text3 = Text("3", "Verdana", L*0.4, aboutWest-0.46*L, L*6.12)  
text4 = Text("4", "Verdana", L*0.4, aboutWest-0.46*L, L*5.12)    
text5 = Text("5", "Verdana", L*0.4, aboutWest-0.46*L, L*4.12)   
text6 = Text("6", "Verdana", L*0.4, aboutWest-0.46*L, L*3.12) 
text7 = Text("7", "Verdana", L*0.4, aboutWest-0.46*L, L*2.12)   
text8 = Text("8", "Verdana", L*0.4, aboutWest-0.46*L, L*1.12)  

text1b = Text("1", "Verdana", L*0.4, aboutWest+8.5*L, L*8.95)   
text2b = Text("2", "Verdana", L*0.4, aboutWest+8.5*L, L*7.95)  
text3b = Text("3", "Verdana", L*0.4, aboutWest+8.5*L, L*6.95)  
text4b = Text("4", "Verdana", L*0.4, aboutWest+8.5*L, L*5.95)  
text5b = Text("5", "Verdana", L*0.4, aboutWest+8.5*L, L*4.95)  
text6b = Text("6", "Verdana", L*0.4, aboutWest+8.5*L, L*3.95)  
text7b = Text("7", "Verdana", L*0.4, aboutWest+8.5*L, L*2.95)   
text8b = Text("8", "Verdana", L*0.4, aboutWest+8.5*L, L*1.95)  

text1b.textID.setRotation(180)
text2b.textID.setRotation(180)
text3b.textID.setRotation(180)
text4b.textID.setRotation(180)
text5b.textID.setRotation(180)
text6b.textID.setRotation(180)
text7b.textID.setRotation(180)
text8b.textID.setRotation(180)
    
def perimeterRotateBlack():
    textH.textID.setPos(aboutWest+0.2*L,     L*8.85)    
    textG.textID.setPos(aboutWest+0.2*L+L,   L*8.85)    
    textF.textID.setPos(aboutWest+0.2*L+2*L, L*8.85)    
    textE.textID.setPos(aboutWest+0.2*L+3*L, L*8.85)  
    textD.textID.setPos(aboutWest+0.2*L+4*L, L*8.85)     
    textC.textID.setPos(aboutWest+0.2*L+5*L, L*8.85)    
    textB.textID.setPos(aboutWest+0.2*L+6*L, L*8.85)    
    textA.textID.setPos(aboutWest+0.2*L+7*L, L*8.85)
    
    textHb.textID.setPos(aboutWest+0.7*L, 1.17*L)    
    textGb.textID.setPos(aboutWest+0.7*L+L,   1.17*L)    
    textFb.textID.setPos(aboutWest+0.7*L+2*L, 1.17*L)    
    textEb.textID.setPos(aboutWest+0.7*L+3*L, 1.17*L)  
    textDb.textID.setPos(aboutWest+0.7*L+4*L, 1.17*L)     
    textCb.textID.setPos(aboutWest+0.7*L+5*L, 1.17*L)    
    textBb.textID.setPos(aboutWest+0.7*L+6*L, 1.17*L)    
    textAb.textID.setPos(aboutWest+0.7*L+7*L, 1.17*L)
    
    text1.textID.setPos(aboutWest-0.46*L, L*1.12)
    text2.textID.setPos(aboutWest-0.46*L, L*2.12)
    text3.textID.setPos(aboutWest-0.46*L, L*3.12)
    text4.textID.setPos(aboutWest-0.46*L, L*4.12)
    text5.textID.setPos(aboutWest-0.46*L, L*5.12)
    text6.textID.setPos(aboutWest-0.46*L, L*6.12)
    text7.textID.setPos(aboutWest-0.46*L, L*7.12)
    text8.textID.setPos(aboutWest-0.46*L, L*8.12)
    
    text1b.textID.setPos(aboutWest+8.5*L, L*1.95)
    text2b.textID.setPos(aboutWest+8.5*L, L*2.95)
    text3b.textID.setPos(aboutWest+8.5*L, L*3.95)
    text4b.textID.setPos(aboutWest+8.5*L, L*4.95)
    text5b.textID.setPos(aboutWest+8.5*L, L*5.95)
    text6b.textID.setPos(aboutWest+8.5*L, L*6.95)
    text7b.textID.setPos(aboutWest+8.5*L, L*7.95)
    text8b.textID.setPos(aboutWest+8.5*L, L*8.95)
    
def perimeterRotateWhite():
    textA.textID.setPos(aboutWest+0.2*L,     L*8.85)    
    textB.textID.setPos(aboutWest+0.2*L+L,   L*8.85)    
    textC.textID.setPos(aboutWest+0.2*L+2*L, L*8.85)    
    textD.textID.setPos(aboutWest+0.2*L+3*L, L*8.85)  
    textE.textID.setPos(aboutWest+0.2*L+4*L, L*8.85)     
    textF.textID.setPos(aboutWest+0.2*L+5*L, L*8.85)    
    textG.textID.setPos(aboutWest+0.2*L+6*L, L*8.85)    
    textH.textID.setPos(aboutWest+0.2*L+7*L, L*8.85)
    
    textAb.textID.setPos(aboutWest+0.7*L, 1.17*L)    
    textBb.textID.setPos(aboutWest+0.7*L+L,   1.17*L)    
    textCb.textID.setPos(aboutWest+0.7*L+2*L, 1.17*L)    
    textDb.textID.setPos(aboutWest+0.7*L+3*L, 1.17*L)  
    textEb.textID.setPos(aboutWest+0.7*L+4*L, 1.17*L)     
    textFb.textID.setPos(aboutWest+0.7*L+5*L, 1.17*L)    
    textGb.textID.setPos(aboutWest+0.7*L+6*L, 1.17*L)    
    textHb.textID.setPos(aboutWest+0.7*L+7*L, 1.17*L)
    
    text8.textID.setPos(aboutWest-0.46*L, L*1.12)
    text7.textID.setPos(aboutWest-0.46*L, L*2.12)
    text6.textID.setPos(aboutWest-0.46*L, L*3.12)
    text5.textID.setPos(aboutWest-0.46*L, L*4.12)
    text4.textID.setPos(aboutWest-0.46*L, L*5.12)
    text3.textID.setPos(aboutWest-0.46*L, L*6.12)
    text2.textID.setPos(aboutWest-0.46*L, L*7.12)
    text1.textID.setPos(aboutWest-0.46*L, L*8.12)
    
    text8b.textID.setPos(aboutWest+8.5*L, L*1.95)
    text7b.textID.setPos(aboutWest+8.5*L, L*2.95)
    text6b.textID.setPos(aboutWest+8.5*L, L*3.95)
    text5b.textID.setPos(aboutWest+8.5*L, L*4.95)
    text4b.textID.setPos(aboutWest+8.5*L, L*5.95)
    text3b.textID.setPos(aboutWest+8.5*L, L*6.95)
    text2b.textID.setPos(aboutWest+8.5*L, L*7.95)
    text1b.textID.setPos(aboutWest+8.5*L, L*8.95)
#    
    
    
#def drawPerimeterBlack():    
#    global textH, textG, textF, textE, textD, textC, textB, textA,  textAb, textHb, textGb, textFb, textEb, textDb, textCb, textBb, textAb, \
#    text1, text2, text3, text4, text5, text6, text7, text8, text1b, text2b, text3b, text4b, text5b, text6b, text7b, text8b, listPerimeterBlack
#    listPerimeterBlack = []
#    textH = Text("A", "Verdana", L*0.4, aboutWest+0.2*L+7*L, L*8.85)
#    listPerimeterBlack.append(textH)
#    textG = Text("B", "Verdana", L*0.4, aboutWest+0.2*L+6*L, L*8.85)
#    listPerimeterBlack.append(textG)
#    textF = Text("C", "Verdana", L*0.4, aboutWest+0.2*L+5*L, L*8.85)
#    listPerimeterBlack.append(textF)
#    textE = Text("D", "Verdana", L*0.4, aboutWest+0.2*L+4*L, L*8.85)
#    listPerimeterBlack.append(textE)
#    textD = Text("E", "Verdana", L*0.4, aboutWest+0.2*L+3*L, L*8.85)
#    listPerimeterBlack.append(textD)
#    textC = Text("F", "Verdana", L*0.4, aboutWest+0.2*L+2*L, L*8.85)
#    listPerimeterBlack.append(textC)
#    textB = Text("G", "Verdana", L*0.4, aboutWest+0.2*L+L,   L*8.85)
#    listPerimeterBlack.append(textB)
#    textA = Text("H", "Verdana", L*0.4, aboutWest+0.2*L,     L*8.85)
#    listPerimeterBlack.append(textA)
#    
#    textHb = Text("A", "Verdana", L*0.4, aboutWest+0.7*L+7*L, 1.17*L)
#    listPerimeterBlack.append(textHb)
#    textGb = Text("B", "Verdana", L*0.4, aboutWest+0.7*L+6*L, 1.17*L)
#    listPerimeterBlack.append(textGb)
#    textFb = Text("C", "Verdana", L*0.4, aboutWest+0.7*L+5*L, 1.17*L)
#    listPerimeterBlack.append(textFb)
#    textEb = Text("D", "Verdana", L*0.4, aboutWest+0.7*L+4*L, 1.17*L)
#    listPerimeterBlack.append(textEb)
#    textDb = Text("E", "Verdana", L*0.4, aboutWest+0.7*L+3*L, 1.17*L)
#    listPerimeterBlack.append(textDb)
#    textCb = Text("F", "Verdana", L*0.4, aboutWest+0.7*L+2*L, 1.17*L)
#    listPerimeterBlack.append(textCb)
#    textBb = Text("G", "Verdana", L*0.4, aboutWest+0.7*L+L,   1.17*L)
#    listPerimeterBlack.append(textBb)
#    textAb = Text("H", "Verdana", L*0.4, aboutWest+0.7*L,     1.17*L)
#    listPerimeterBlack.append(textAb)
#    
#    textAb.textID.setRotation(180)
#    textBb.textID.setRotation(180)
#    textCb.textID.setRotation(180)
#    textDb.textID.setRotation(180)
#    textEb.textID.setRotation(180)
#    textFb.textID.setRotation(180)
#    textGb.textID.setRotation(180)
#    textHb.textID.setRotation(180)
#    
#    text1 = Text("8", "Verdana", L*0.4, aboutWest-0.46*L, L*8.12)
#    listPerimeterBlack.append(text1)
#    text2 = Text("7", "Verdana", L*0.4, aboutWest-0.46*L, L*7.12)
#    listPerimeterBlack.append(text2)
#    text3 = Text("6", "Verdana", L*0.4, aboutWest-0.46*L, L*6.12)
#    listPerimeterBlack.append(text3)
#    text4 = Text("5", "Verdana", L*0.4, aboutWest-0.46*L, L*5.12)
#    listPerimeterBlack.append(text4)
#    text5 = Text("4", "Verdana", L*0.4, aboutWest-0.46*L, L*4.12)
#    listPerimeterBlack.append(text5)
#    text6 = Text("3", "Verdana", L*0.4, aboutWest-0.46*L, L*3.12)
#    listPerimeterBlack.append(text6)
#    text7 = Text("2", "Verdana", L*0.4, aboutWest-0.46*L, L*2.12)
#    listPerimeterBlack.append(text7)
#    text8 = Text("1", "Verdana", L*0.4, aboutWest-0.46*L, L*1.12)
#    listPerimeterBlack.append(text8)
#    
#    text1b = Text("8", "Verdana", L*0.4, aboutWest+8.5*L, L*8.95)
#    listPerimeterBlack.append(text1b)
#    text2b = Text("7", "Verdana", L*0.4, aboutWest+8.5*L, L*7.95)
#    listPerimeterBlack.append(text2b)
#    text3b = Text("6", "Verdana", L*0.4, aboutWest+8.5*L, L*6.95)
#    listPerimeterBlack.append(text3b)
#    text4b = Text("5", "Verdana", L*0.4, aboutWest+8.5*L, L*5.95)
#    listPerimeterBlack.append(text4b)
#    text5b = Text("4", "Verdana", L*0.4, aboutWest+8.5*L, L*4.95)
#    listPerimeterBlack.append(text5b)
#    text6b = Text("3", "Verdana", L*0.4, aboutWest+8.5*L, L*3.95)
#    listPerimeterBlack.append(text6b)
#    text7b = Text("2", "Verdana", L*0.4, aboutWest+8.5*L, L*2.95)
#    listPerimeterBlack.append(text7b)
#    text8b = Text("1", "Verdana", L*0.4, aboutWest+8.5*L, L*1.95)
#    listPerimeterBlack.append(text8b)
#    
#    text1b.textID.setRotation(180)
#    text2b.textID.setRotation(180)
#    text3b.textID.setRotation(180)
#    text4b.textID.setRotation(180)
#    text5b.textID.setRotation(180)
#    text6b.textID.setRotation(180)
#    text7b.textID.setRotation(180)
#    text8b.textID.setRotation(180)
#    




class Pieces():
    def __init__(self, pieceType, color, index_board,  symbol,  firstMove, image):        
        self.pieceType = pieceType
        self.color = color
        self.firstMove = firstMove
        self.index_board = index_board
        self.symbol = symbol
        self.image = image
        position[index_board] = self
        
class Pawn(Pieces):
    def __init__(self, color, index_board, symbol, firstMove, image):
        Pieces.__init__(self, pieceType[0], color, index_board, symbol,  firstMove,  image)   

class King(Pieces):
    def __init__(self, color, index_board, symbol, firstMove, image):
        Pieces.__init__(self, pieceType[1], color, index_board, symbol, firstMove, image)

class Queen(Pieces):
    def __init__(self, color, index_board, symbol, firstMove, image):
        Pieces.__init__(self, pieceType[2], color, index_board, symbol, firstMove, image)

class Rook(Pieces):
    def __init__(self,color, index_board, symbol, firstMove, image):
        Pieces.__init__(self, pieceType[3], color, index_board, symbol, firstMove,  image)

class Knight(Pieces):
    def __init__(self, color, index_board, symbol, firstMove,  image):
        Pieces.__init__(self, pieceType[4], color, index_board, symbol, firstMove, image)

class Bishop(Pieces):
    def __init__(self, color, index_board, symbol, firstMove, image):
        Pieces.__init__(self, pieceType[5], color, index_board, symbol, firstMove, image)

rook_a1   = Rook(Color.WHITE, 180, 'R', False, imageWhiteRook)
knight_b1 = Knight(Color.WHITE, 181, 'N', False, imageWhiteKnight)   
bishop_c1 = Bishop(Color.WHITE, 182, 'B', False, imageWhiteBishop)  
queen_d1  = Queen(Color.WHITE, 183, 'Q', False, imageWhiteQueen)  
king_e1   = King(Color.WHITE, 184, 'K', False, imageWhiteKing)  
bishop_f1 = Bishop(Color.WHITE, 185, 'B', False, imageWhiteBishop) 
knight_g1 = Knight(Color.WHITE, 186, 'N', False, imageWhiteKnight)  
rook_h1   = Rook(Color.WHITE,   187, 'R', False, imageWhiteRook)

pawn_a2 = Pawn(Color.WHITE, 164, '', False, imageWhitePawn)
pawn_b2 = Pawn(Color.WHITE, 165, '', False, imageWhitePawn)
pawn_c2 = Pawn(Color.WHITE, 166,  '', False, imageWhitePawn)
pawn_d2 = Pawn(Color.WHITE, 167, '', False, imageWhitePawn)
pawn_e2 = Pawn(Color.WHITE, 168, '', False, imageWhitePawn)
pawn_f2 = Pawn(Color.WHITE, 169, '', False, imageWhitePawn)
pawn_g2 = Pawn(Color.WHITE, 170,  '', False, imageWhitePawn)
pawn_h2 = Pawn(Color.WHITE, 171, '', False, imageWhitePawn)

pawn_a7 = Pawn(Color.BLACK, 84, '', False, imageBlackPawn)
pawn_b7 = Pawn(Color.BLACK, 85, '', False, imageBlackPawn)
pawn_c7 = Pawn(Color.BLACK, 86, '', False, imageBlackPawn)
pawn_d7 = Pawn(Color.BLACK, 87, '', False, imageBlackPawn)
pawn_e7 = Pawn(Color.BLACK, 88, '', False, imageBlackPawn)
pawn_f7 = Pawn(Color.BLACK, 89, '', False, imageBlackPawn)
pawn_g7 = Pawn(Color.BLACK, 90, '', False, imageBlackPawn)
pawn_h7 = Pawn(Color.BLACK, 91, '', False, imageBlackPawn)

rook_a8   = Rook(Color.BLACK,   68, 'R', False, imageBlackRook)
knight_b8 = Knight(Color.BLACK, 69, 'N', False, imageBlackKnight)   
bishop_c8 = Bishop(Color.BLACK, 70, 'B', False, imageBlackBishop)  
queen_d8  = Queen(Color.BLACK,  71, 'Q', False, imageBlackQueen)  
king_e8   = King(Color.BLACK,   72, 'K', False, imageBlackKing)  
bishop_f8 = Bishop(Color.BLACK, 73, 'B', False, imageBlackBishop)
knight_g8 = Knight(Color.BLACK, 74, 'N', False, imageBlackKnight)  
rook_h8   = Rook(Color.BLACK,   75, 'R', False, imageBlackRook)    

class PiecesView(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, r, xItem, yItem):        
        QtWidgets.QGraphicsPixmapItem.__init__(self)
        self.setPixmap(r)
        self.setOffset(xItem, yItem)
        scene.addItem(self)        
        
        self.xItem = xItem
        self.yItem = yItem

      

global listPiecesView
def drawPositionWhite(position):  
    global a8, b8, c8, d8, e8, f8, g8, h8, a7, b7, c7, d7, e7, f7, g7, h7, a6, b6, c6, d6, e6, f6, g6, h6, a5, b5, c5, d5, e5, f5, g5, h5, \
    a4, b4, c4, d4, e4, f4, g4, h4, a3, b3, c3, d3, e3, f3, g3, h3, a2, b2, c2, d2, e2, f2, g2, h2, a1, b1, c1, d1, e1, f1, g1, h1, listPiecesView
    listPiecesView = []
    for t in range(68, 188):
        if t == 68 and position[68] != 0:
            a8 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, L+1)
            listPiecesView.append(a8)
        if t == 69 and position[69] != 0:
            b8 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, L+1)
            listPiecesView.append(b8)            
        if t == 70 and position[70] != 0:
            c8 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, L+1)
            listPiecesView.append(c8)
        if t == 71 and position[71] != 0:
            d8 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, L+1)
            listPiecesView.append(d8) 
        if t == 72 and position[72] != 0:
            e8 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, L+1)
            listPiecesView.append(e8)    
        if t == 73 and position[73] != 0:
            f8 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, L+1)
            listPiecesView.append(f8)    
        if t == 74 and position[74] != 0:
            g8 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, L+1)
            listPiecesView.append(g8)    
        if t == 75 and position[75] != 0:
            h8 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, L+1)
            listPiecesView.append(h8)    
            
        if t == 84 and position[84] != 0:
           a7 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 2*L+1)
           listPiecesView.append(a7)
        if t == 85 and position[85] != 0:
            b7 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 2*L+1)
            listPiecesView.append(b7)
        if t == 86 and position[86] != 0:
            c7 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 2*L+1)
            listPiecesView.append(c7)
        if t == 87 and position[87] != 0:
            d7 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 2*L+1)
            listPiecesView.append(d7)
        if t == 88 and position[88] != 0:
            e7 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 2*L+1)
            listPiecesView.append(e7)
        if t == 89 and position[89] != 0:
            f7 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 2*L+1)
            listPiecesView.append(f7)
        if t == 90 and position[90] != 0:
            g7 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 2*L+1)
            listPiecesView.append(g7)
        if t == 91 and position[91] != 0:
            h7 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 2*L+1)
            listPiecesView.append(h7)
            
        if t == 100 and position[100] != 0:
            a6 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 3*L+1)
            listPiecesView.append(a6)
        if t == 101 and position[101] != 0:
            b6 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 3*L+1)
            listPiecesView.append(b6)
        if t == 102 and position[102] != 0:
            c6 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 3*L+1)
            listPiecesView.append(c6)
        if t == 103 and position[103] != 0:
            d6 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 3*L+1)
            listPiecesView.append(d6)
        if t == 104 and position[104] != 0:
            e6 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 3*L+1)
            listPiecesView.append(e6)
        if t == 105 and position[105] != 0:
            f6 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 3*L+1)
            listPiecesView.append(f6)
        if t == 106 and position[106] != 0:
            g6 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 3*L+1)
            listPiecesView.append(g6)
        if t == 107 and position[107] != 0:
            h6 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 3*L+1)
            listPiecesView.append(h6)
            
        if t == 116 and position[116] != 0:
            a5 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 4*L+1)
            listPiecesView.append(a5)
        if t == 117 and position[117] != 0:
            b5 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 4*L+1)
            listPiecesView.append(b5)
        if t == 118 and position[118] != 0:
            c5 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 4*L+1)
            listPiecesView.append(c5)
        if t == 119 and position[119] != 0:
            d5 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 4*L+1)
            listPiecesView.append(d5)
        if t == 120 and position[120] != 0:
            e5 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 4*L+1)
            listPiecesView.append(e5)
        if t == 121 and position[121] != 0:
            f5 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 4*L+1)
            listPiecesView.append(f5)
        if t == 122 and position[122] != 0:
            g5 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 4*L+1)
            listPiecesView.append(g5)
        if t == 123 and position[123] != 0:
            h5 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 4*L+1)
            listPiecesView.append(h5)
            
        if t == 132 and position[132] != 0:
            a4 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 5*L+1)
            listPiecesView.append(a4)
        if t == 133 and position[133] != 0:
            b4 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 5*L+1)
            listPiecesView.append(b4)
        if t == 134 and position[134] != 0:
            c4 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 5*L+1)
            listPiecesView.append(c4)
        if t == 135 and position[135] != 0:
            d4 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 5*L+1)
            listPiecesView.append(d4)
        if t == 136 and position[136] != 0:
            e4 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 5*L+1)
            listPiecesView.append(e4)
        if t == 137 and position[137] != 0:
            f4 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 5*L+1)
            listPiecesView.append(f4)
        if t == 138 and position[138] != 0:
            g4 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 5*L+1)
            listPiecesView.append(g4)
        if t == 139 and position[139] != 0:
            h4 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 5*L+1)
            listPiecesView.append(h4)
            
        if t == 148 and position[148] != 0:
            a3 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 6*L+1)
            listPiecesView.append(a3)
        if t == 149 and position[149] != 0:
            b3 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 6*L+1)
            listPiecesView.append(b3)
        if t == 150 and position[150] != 0:
            c3 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 6*L+1)
            listPiecesView.append(c3)
        if t == 151 and position[151] != 0:
            d3 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 6*L+1)
            listPiecesView.append(d3)
        if t == 152 and position[152] != 0:
            e3 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 6*L+1)
            listPiecesView.append(e3)
        if t == 153 and position[153] != 0:
            f3 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 6*L+1)
            listPiecesView.append(f3)
        if t == 154 and position[154] != 0:
            g3 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 6*L+1)
            listPiecesView.append(g3)
        if t == 155 and position[155] != 0:
            h3 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 6*L+1)
            listPiecesView.append(h3)
            
        if t == 164 and position[164] != 0:
            a2 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 7*L+1)
            listPiecesView.append(a2)
        if t == 165 and position[165] != 0:
            b2 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 7*L+1)
            listPiecesView.append(b2)
        if t == 166 and position[166] != 0:
            c2 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 7*L+1)
            listPiecesView.append(c2)
        if t == 167 and position[167] != 0:
            d2 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 7*L+1)
            listPiecesView.append(d2)
        if t == 168 and position[168] != 0:
            e2 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 7*L+1)
            listPiecesView.append(e2)
        if t == 169 and position[169] != 0:
            f2 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 7*L+1)
            listPiecesView.append(f2)
        if t == 170 and position[170] != 0:
            g2 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 7*L+1)
            listPiecesView.append(g2)
        if t == 171 and position[171] != 0:
            h2 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 7*L+1)
            listPiecesView.append(h2)
            
        if t == 180 and position[180] != 0:
            a1 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 8*L+1)
            listPiecesView.append(a1)
        if t == 181 and position[181] != 0:
            b1 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 8*L+1)
            listPiecesView.append(b1)
        if t == 182 and position[182] != 0:
            c1 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 8*L+1)
            listPiecesView.append(c1)
        if t == 183 and position[183] != 0:
            d1 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 8*L+1)
            listPiecesView.append(d1)
        if t == 184 and position[184] != 0:
            e1 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 8*L+1)
            listPiecesView.append(e1)
        if t == 185 and position[185] != 0:
            f1 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 8*L+1)
            listPiecesView.append(f1)
        if t == 186 and position[186] != 0:
            g1 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 8*L+1)
            listPiecesView.append(g1)
        if t == 187 and position[187] != 0:
            h1 = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 8*L+1)
            listPiecesView.append(h1)
            
def deleteView(list):    
    for hh in list:
        hh.hide()            

   
drawPositionWhite(position)  

global listPiecesViewB
def drawPositionBlack(position):  
    global a8b, b8b, c8b, d8b, e8b, f8b, g8b, h8b, a7b, b7b, c7b, d7b, e7b, f7b, g7b, h7b, a6b, b6b, c6b, d6b, e6b, f6b, g6b, h6b, a5b, b5b, c5b, d5b, e5b,\
    f5b, g5b, h5b, a4b, b4b, c4b, d4b, e4b, f4b, g4b, h4b, a3b, b3b, c3b, d3b, e3b, f3b, g3b, h3b, a2b, b2b, c2b, d2b, e2b, f2b, g2b, h2b, a1b, b1b, c1b, d1b, \
    e1b, f1b, g1b, h1b, listPiecesViewB
    listPiecesViewB = []
    for t in range(68, 188):
        if t == 187 and position[187] != 0:
            h1b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, L+1)
            listPiecesViewB.append(h1b)
        if t == 186 and position[186] != 0:
            g1b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, L+1)
            listPiecesViewB.append(g1b)            
        if t == 185 and position[185] != 0:
            f1b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, L+1)
            listPiecesViewB.append(f1b)
        if t == 184 and position[184] != 0:
            e1b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, L+1)
            listPiecesViewB.append(e1b) 
        if t == 183 and position[183] != 0:
            d1b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, L+1)
            listPiecesViewB.append(d1b)    
        if t == 182 and position[182] != 0:
            c1b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, L+1)
            listPiecesViewB.append(c1b)    
        if t == 181 and position[181] != 0:
            b1b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, L+1)
            listPiecesViewB.append(b1b)    
        if t == 180 and position[180] != 0:
            a1b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, L+1)
            listPiecesViewB.append(a1b)    
            
        if t == 171 and position[171] != 0:
           h2b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 2*L+1)
           listPiecesViewB.append(h2b)
        if t == 170 and position[170] != 0:
            g2b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 2*L+1)
            listPiecesViewB.append(g2b)
        if t == 169 and position[169] != 0:
            f2b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 2*L+1)
            listPiecesViewB.append(f2b)
        if t == 168 and position[168] != 0:
            e2b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 2*L+1)
            listPiecesViewB.append(e2b)
        if t == 167 and position[167] != 0:
            d2b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 2*L+1)
            listPiecesViewB.append(d2b)
        if t == 166 and position[166] != 0:
            c2b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 2*L+1)
            listPiecesViewB.append(c2b)
        if t == 165 and position[165] != 0:
            b2b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 2*L+1)
            listPiecesViewB.append(b2b)
        if t == 164 and position[164] != 0:
            a2b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 2*L+1)
            listPiecesViewB.append(a2b)
            
        if t == 155 and position[155] != 0:
            h3b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 3*L+1)
            listPiecesViewB.append(h3b)
        if t == 154 and position[154] != 0:
            g3b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 3*L+1)
            listPiecesViewB.append(g3b)
        if t == 153 and position[153] != 0:
            f3b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 3*L+1)
            listPiecesViewB.append(f3b)
        if t == 152 and position[152] != 0:
            e3b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 3*L+1)
            listPiecesViewB.append(e3b)
        if t == 151 and position[151] != 0:
            d3b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 3*L+1)
            listPiecesViewB.append(d3b)
        if t == 150 and position[150] != 0:
            c3b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 3*L+1)
            listPiecesViewB.append(c3b)
        if t == 149 and position[149] != 0:
            b3b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 3*L+1)
            listPiecesViewB.append(b3b)
        if t == 148 and position[148] != 0:
            a3b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 3*L+1)
            listPiecesViewB.append(a3b)
            
        if t == 139 and position[139] != 0:
            h4b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 4*L+1)
            listPiecesViewB.append(h4b)
        if t == 138 and position[138] != 0:
            g4b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 4*L+1)
            listPiecesViewB.append(g4b)
        if t == 137 and position[137] != 0:
            f4b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 4*L+1)
            listPiecesViewB.append(f4b)
        if t == 136 and position[136] != 0:
            e4b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 4*L+1)
            listPiecesViewB.append(e4b)
        if t == 135 and position[135] != 0:
            d4b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 4*L+1)
            listPiecesViewB.append(d4b)
        if t == 134 and position[134] != 0:
            c4b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 4*L+1)
            listPiecesViewB.append(c4b)
        if t == 133 and position[133] != 0:
            b4b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 4*L+1)
            listPiecesViewB.append(b4b)
        if t == 132 and position[132] != 0:
            a4b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 4*L+1)
            listPiecesViewB.append(a4b)
            
        if t == 123 and position[123] != 0:
            h5b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 5*L+1)
            listPiecesViewB.append(h5b)
        if t == 122 and position[122] != 0:
            g5b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 5*L+1)
            listPiecesViewB.append(g5b)
        if t == 121 and position[121] != 0:
            f5b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 5*L+1)
            listPiecesViewB.append(f5b)
        if t == 120 and position[120] != 0:
            e5b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 5*L+1)
            listPiecesViewB.append(e5b)
        if t == 119 and position[119] != 0:
            d5b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 5*L+1)
            listPiecesViewB.append(d5b)
        if t == 118 and position[118] != 0:
            c5b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 5*L+1)
            listPiecesViewB.append(c5b)
        if t == 117 and position[117] != 0:
            b5b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 5*L+1)
            listPiecesViewB.append(b5b)
        if t == 116 and position[116] != 0:
            a5b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 5*L+1)
            listPiecesViewB.append(a5b)
            
        if t == 107 and position[107] != 0:
            h6b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 6*L+1)
            listPiecesViewB.append(h6b)
        if t == 106 and position[106] != 0:
            g6b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 6*L+1)
            listPiecesViewB.append(g6b)
        if t == 105 and position[105] != 0:
            f6b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 6*L+1)
            listPiecesViewB.append(f6b)
        if t == 104 and position[104] != 0:
            e6b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 6*L+1)
            listPiecesViewB.append(e6b)
        if t == 103 and position[103] != 0:
            d6b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 6*L+1)
            listPiecesViewB.append(d6b)
        if t == 102 and position[102] != 0:
            c6b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 6*L+1)
            listPiecesViewB.append(c6b)
        if t == 101 and position[101] != 0:
            b6b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 6*L+1)
            listPiecesViewB.append(b6b)
        if t == 100 and position[100] != 0:
            a6b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 6*L+1)
            listPiecesViewB.append(a6b)
            
        if t == 91 and position[91] != 0:
            h7b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 7*L+1)
            listPiecesViewB.append(h7b)
        if t == 90 and position[90] != 0:
            g7b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 7*L+1)
            listPiecesViewB.append(g7b)
        if t == 89 and position[89] != 0:
            f7b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 7*L+1)
            listPiecesViewB.append(f7b)
        if t == 88 and position[88] != 0:
            e7b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 7*L+1)
            listPiecesViewB.append(e7b)
        if t == 87 and position[87] != 0:
            d7b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 7*L+1)
            listPiecesViewB.append(d7b)
        if t == 86 and position[86] != 0:
            c7b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 7*L+1)
            listPiecesViewB.append(c7b)
        if t == 85 and position[85] != 0:
            b7b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 7*L+1)
            listPiecesViewB.append(b7b)
        if t == 84 and position[84] != 0:
            a7b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 7*L+1)
            listPiecesViewB.append(a7b)
            
        if t == 75 and position[75] != 0:
            h8b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+1, 8*L+1)
            listPiecesViewB.append(h8b)
        if t == 74 and position[74] != 0:
            g8b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+L+1, 8*L+1)
            listPiecesViewB.append(g8b)
        if t == 73 and position[73] != 0:
            f8b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+2*L+1, 8*L+1)
            listPiecesViewB.append(f8b)
        if t == 72 and position[72] != 0:
            e8b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+3*L+1, 8*L+1)
            listPiecesViewB.append(e8b)
        if t == 71 and position[71] != 0:
            d8b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+4*L+1, 8*L+1)
            listPiecesViewB.append(d8b)
        if t == 70 and position[70] != 0:
            c8b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+5*L+1, 8*L+1)
            listPiecesViewB.append(c8b)
        if t == 69 and position[69] != 0:
            b8b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+6*L+1, 8*L+1)
            listPiecesViewB.append(b8b)
        if t == 68 and position[68] != 0:
            a8b = PiecesView(QtGui.QPixmap(position[t].image).scaled(L-1,L-1), aboutWest+7*L+1, 8*L+1)
            listPiecesViewB.append(a8b)
            

        
listWhitePieces = [king_e1, queen_d1, rook_a1, rook_h1, knight_b1, knight_g1, bishop_c1, bishop_f1, \
                   pawn_a2, pawn_b2, pawn_c2, pawn_d2, pawn_e2, pawn_f2, pawn_g2, pawn_h2]

listBlackPieces = [king_e8, queen_d8, rook_a8, rook_h8, knight_b8, knight_g8, bishop_c8, bishop_f8, \
                   pawn_a7, pawn_b7, pawn_c7, pawn_d7, pawn_e7, pawn_f7, pawn_g7, pawn_h7]
                   
                   
def fieldsBrokenWhitePieces(position):
    global listFieldsBrokenWhitePieces   #список полей битых белыми фигурами
    listFieldsBrokenWhitePieces = []
    for i in listWhitePieces:
    
        if i.pieceType == 'QUEEN' and i.color == Color.WHITE:
            for j in incrementQueen:
                n = i.index_board + j
                while position[n] == 0:
                    listFieldsBrokenWhitePieces.append(n)
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    listFieldsBrokenWhitePieces.append(n)

        if i.pieceType == 'BISHOP' and i.color == Color.WHITE:
            for j in incrementBishop:
                n = i.index_board + j
                while position[n] == 0:
                    listFieldsBrokenWhitePieces.append(n)
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    listFieldsBrokenWhitePieces.append(n)

        if i.pieceType == 'ROOK' and i.color == Color.WHITE:
            for j in incrementRook:
                n = i.index_board + j
                while position[n] == 0:
                    listFieldsBrokenWhitePieces.append(n)
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    listFieldsBrokenWhitePieces.append(n)

        if i.pieceType == 'KNIGHT' and i.color == Color.WHITE:
            for j in incrementKnight:
                n = i.index_board + j
                if position[n] == 0:
                    listFieldsBrokenWhitePieces.append(n)
                    
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    listFieldsBrokenWhitePieces.append(n)

        if i.pieceType == 'KING' and i.color == Color.WHITE:
            global checkWhite
            for j in incrementQueen:
                n = i.index_board + j
                if position[n] == 0:
                    listFieldsBrokenWhitePieces.append(n)
                    
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    listFieldsBrokenWhitePieces.append(n)                          

        if i.pieceType == 'PAWN' and i.color == Color.WHITE:
            for j in incrementWhitePawn:
                n = i.index_board + j
                if j == -15 and type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    listFieldsBrokenWhitePieces.append(n)
                if j == -17 and type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    listFieldsBrokenWhitePieces.append(n)

def fieldsBrokenBlackPieces(position):
    global listFieldsBrokenBlackPieces #список список полей битых черными фигурами
    listFieldsBrokenBlackPieces = []
    for i in listBlackPieces:
    
        if i.pieceType == 'QUEEN' and i.color == Color.BLACK:
            for j in incrementQueen:
                n = i.index_board + j
                while position[n] == 0:
                    listFieldsBrokenBlackPieces.append(n)
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    listFieldsBrokenBlackPieces.append(n)

        if i.pieceType == 'BISHOP' and i.color == Color.BLACK:
            for j in incrementBishop:
                n = i.index_board + j
                while position[n] == 0:
                    listFieldsBrokenBlackPieces.append(n)
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    listFieldsBrokenBlackPieces.append(n)

        if i.pieceType == 'ROOK' and i.color == Color.BLACK:
            for j in incrementRook:
                n = i.index_board + j
                while position[n] == 0:
                    listFieldsBrokenBlackPieces.append(n)
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    listFieldsBrokenBlackPieces.append(n)

        if i.pieceType == 'KNIGHT' and i.color == Color.BLACK:
            for j in incrementKnight:
                n = i.index_board + j
                if position[n] == 0:
                    listFieldsBrokenBlackPieces.append(n)
                    
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    listFieldsBrokenBlackPieces.append(n)

        if i.pieceType == 'KING' and i.color == Color.BLACK:
            for j in incrementQueen:
                n = i.index_board + j
                if position[n] == 0:
                    listFieldsBrokenBlackPieces.append(n)
                    
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    listFieldsBrokenBlackPieces.append(n)                   
                

        if i.pieceType == 'PAWN' and i.color == Color.BLACK:
            for j in incrementBlackPawn:
                n = i.index_board + j
                if j == 15 and type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    listFieldsBrokenBlackPieces.append(n)                    
                if j == 17 and type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    listFieldsBrokenBlackPieces.append(n)
                    
def defineCheckWhite(position):
    fieldsBrokenBlackPieces(position)
    global checkWhite, checkWhiteSymbol
    if king_e1.index_board in listFieldsBrokenBlackPieces:
        checkWhite = True
        checkWhiteSymbol = '+'
    else:
        checkWhite = False
        checkWhiteSymbol = ''
    return checkWhite


def defineCheckBlack(position):
    fieldsBrokenWhitePieces(position)
    global checkBlack, checkBlackSymbol
    if king_e8.index_board in listFieldsBrokenWhitePieces:
        checkBlack = True
        checkBlackSymbol = '+'
    else:
        checkBlack = False
        checkBlackSymbol = ''
    return checkBlack

moveType = ['simpleMove', 'capture', 'promotion','enPassant','castling']
class Move:
    def __init__(self, moveType, indexGoOut, indexGoTo, piece):
        self.moveType = moveType       # тип хода
        self.indexGoOut = indexGoOut   # индекс откуда пошла фигура
        self.indexGoTo = indexGoTo     # индекс куда пошла фигура
        self.piece = piece             # какая фигура пошла

class SimpleMove(Move):
    def __init__(self, indexGoOut, indexGoTo, piece, noteEnPassant, indexJumpedField):
        Move.__init__(self, moveType[0], indexGoOut, indexGoTo, piece)
        self.noteEnPassant = noteEnPassant
        self.indexJumpedField = indexJumpedField
     

listCaptureWhitePieces = []
listCaptureBlackPieces = []
class Capture(Move):
    def __init__(self, indexGoOut, indexGoTo, piece, pieceCapture, noteEnPassant, indexJumpedField):
        Move.__init__(self, moveType[1], indexGoOut, indexGoTo, piece)
        self.pieceCapture = pieceCapture
        self.noteEnPassant = noteEnPassant
        self.indexJumpedField = indexJumpedField
        
class Castling(Move):
    def __init__(self, indexGoOut, indexGoTo, piece, indexGoOutRook, indexGoToRook,  castlingRook, symbol, noteEnPassant, indexJumpedField):
        Move.__init__(self, moveType[4], indexGoOut, indexGoTo, piece)
        self.indexGoOutRook = indexGoOutRook
        self.indexGoToRook = indexGoToRook
        self.castlingRook = castlingRook
        self.symbol = symbol
        self.noteEnPassant = noteEnPassant
        self.indexJumpedField = indexJumpedField
        
class EnPassant(Move):
    def __init__(self, indexGoOut, indexGoTo, piece, pieceCapture, indexCapture, noteEnPassant, indexJumpedField):
        Move.__init__(self, moveType[3], indexGoOut, indexGoTo, piece)
        self.pieceCapture = pieceCapture
        self.indexCapture = indexCapture
        self.noteEnPassant = noteEnPassant
        self.indexJumpedField = indexJumpedField

def defineLongCastlingWhite():
    global longCastlingWhite    
    if king_e1.firstMove == False and defineCheckWhite(position) == False and rook_a1.firstMove == False and position[181]==0 and position[182]==0 \
            and position[183]==0 and  182 not in listFieldsBrokenBlackPieces and 183 not in  listFieldsBrokenBlackPieces:
                listWhiteMove.append(Castling(184,  182,  king_e1,  180,  183,  rook_a1,  'O-O-O', False, None))
                longCastlingWhite = True
    else:
        longCastlingWhite = False
                
                
            
def defineShortCastlingWhite():
    global shortCastlingWhite
    if king_e1.firstMove == False and defineCheckWhite(position) == False and rook_h1.firstMove == False and position[185]==0 and position[186]==0 \
            and  182 not in listFieldsBrokenBlackPieces and 183 not in  listFieldsBrokenBlackPieces:
                listWhiteMove.append(Castling(184,  186,  king_e1,  187,  185,  rook_h1,  'O-O', False, None))
                shortCastlingWhite = True
    else:
        shortCastlingWhite = False
                
            
def defineLongCastlingBlack():
    global longCastlingBlack
    if king_e8.firstMove == False and defineCheckBlack(position) == False and rook_a8.firstMove == False and position[69]==0 and position[70]==0 \
            and position[71]==0 and 70 not in listFieldsBrokenWhitePieces and 71 not in listFieldsBrokenWhitePieces:
                listBlackMove.append(Castling(72,  70,  king_e8,  68,  71,  rook_a8, 'O-O-O', False, None))
                longCastlingBlack = True
    else:
        longCastlingBlack = False
                
                
            
def defineShortCastlingBlack():
    global shortCastlingBlack    
    if king_e8.firstMove == False and defineCheckBlack(position) == False and rook_h8.firstMove == False and position[73]==0 and position[74]==0 \
            and  73 not in listFieldsBrokenWhitePieces and 74 not in listFieldsBrokenWhitePieces:
                listBlackMove.append(Castling(72,  74,  king_e8,  75,  73,  rook_h8,  'O-O', False, None))
                shortCastlingBlack = True
    else:
        shortCastlingBlack = False
                
                
def enPassantWhite(position):
    global note3EnPassantWhite1, note3EnPassantWhite2
    for t in range (116, 124):
        if position[t] != 0 and position[t].pieceType == 'PAWN' and position[t].color == Color.WHITE and note2EnPassant == True:
            if position[t+1] != 0 and position[t+1] != 'OUT' and position[t+1].pieceType == 'PAWN' and position[t+1].color == Color.BLACK and t-15 == index2JumpedField:
                x = position[t].index_board
                y = position[t+1]
                z = position[t]
                xx = position[t].firstMove
                position[t-15] = position[t]
                position[t] = 0
                position[t+1] = 0
                position[t-15].firstMove = True
                position[t-15].index_board = t-15
                listBlackPieces.remove(y)
                if defineCheckWhite(position) == False:
                    position[t+1] = y
                   
                    position[t] = z
                    position[t-15] = 0
                    position[t].index_board = x 
                    position[t].firstMove = xx
                    listBlackPieces.append(y)
                    listWhiteMove.append(EnPassant(t,  t-15, position[t],  position[t+1], t+1, False, None))
                    note3EnPassantWhite1 = True
                    break
                else:
                    note3EnPassantWhite1 = False
            else:
                note3EnPassantWhite1 = False
                    
            if position[t-1] != 0 and position[t-1] != 'OUT' and position[t-1].pieceType == 'PAWN' and position[t-1].color == Color.BLACK and t-17 == index2JumpedField:
                x = position[t].index_board
                y = position[t-1]
                z = position[t]
                xx = position[t].firstMove
                position[t-17] = position[t]
                position[t] = 0
                position[t-1] = 0
                position[t-17].firstMove = True
                position[t-17].index_board = t-17
                listBlackPieces.remove(y)
                if defineCheckWhite(position) == False:
                    position[t-1] = y
                   
                    position[t] = z
                    position[t-17] = 0
                    position[t].index_board = x 
                    position[t].firstMove = xx
                    listBlackPieces.append(y)
                    listWhiteMove.append(EnPassant(t,  t-17, position[t],  position[t-1],  t-1, False, None))
                    note3EnPassantWhite2 = True
                    break
                else:
                    note3EnPassantWhite2 = False
            else:
                note3EnPassantWhite2 = False
        else:
            note3EnPassantWhite1 = False
            note3EnPassantWhite2 = False
            
                    
                
def enPassantBlack(position):
    global note3EnPassantBlack1, note3EnPassantBlack2
    for t in range (132, 140):
        if position[t] != 0 and position[t].pieceType == 'PAWN' and position[t].color == Color.BLACK and note2EnPassant == True:
            if position[t+1] != 0 and position[t+1] != 'OUT' and position[t+1].pieceType == 'PAWN' and position[t+1].color == Color.WHITE and t+17 == index2JumpedField:
                x = position[t].index_board
                y = position[t+1]
                z = position[t]
                xx = position[t].firstMove
                position[t+17] = position[t]
                position[t] = 0
                position[t+1] = 0
                position[t+17].firstMove = True
                position[t+17].index_board = t+17
                listWhitePieces.remove(y)
                if defineCheckBlack(position) == False:
                    position[t+1] = y
                   
                    position[t] = z
                    position[t+17] = 0
                    position[t].index_board = x 
                    position[t].firstMove = xx
                    listWhitePieces.append(y)
                    listBlackMove.append(EnPassant(t,  t+17, position[t],  position[t+1], t+1, False, None))
                    note3EnPassantBlack1 = True
                    break
                else:
                    note3EnPassantBlack1 = False
            else:
                note3EnPassantBlack1 = False
        
                    
            if position[t-1] != 0 and position[t-1] != 'OUT' and position[t-1].pieceType == 'PAWN' and position[t-1].color == Color.WHITE and t+15 == index2JumpedField:
                x = position[t].index_board
                y = position[t-1]
                z = position[t]
                xx = position[t].firstMove
                position[t+15] = position[t]
                position[t] = 0
                position[t-1] = 0
                position[t+15].firstMove = True
                position[t+15].index_board = t+15
                listWhitePieces.remove(y)
                if defineCheckBlack(position) == False:
                    position[t-1] = y
                   
                    position[t] = z
                    position[t+15] = 0
                    position[t].index_board = x 
                    position[t].firstMove = xx
                    listWhitePieces.append(y)
                    listBlackMove.append(EnPassant(t,  t+15, position[t],  position[t-1],  t-1, False, None))
                    note3EnPassantBlack2 = True
                    break
                else:
                    note3EnPassantBlack2 = False
            else:
                note3EnPassantBlack2 = False
        else:
            note3EnPassantBlack1 = False            
            note3EnPassantBlack2 = False
        
                    

                

def listWPieces(position):
    global listWhiteMove   #список ходов белых фигур
    listWhiteMove = []
    for i in listWhitePieces:
    
        if i.pieceType == 'QUEEN' and i.color == Color.WHITE:
            for j in incrementQueen:
                n = i.index_board + j
                while position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                                                  
                        listWhiteMove.append(SimpleMove(i.index_board, n, i, False, None))
                        
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                                                      
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listBlackPieces.remove(y)
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                        listWhiteMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                        

        if i.pieceType == 'BISHOP' and i.color == Color.WHITE:
            for j in incrementBishop:
                n = i.index_board + j
                while position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                                                   
                        listWhiteMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                                        
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listBlackPieces.remove(y)
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                        listWhiteMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                   

        if i.pieceType == 'ROOK' and i.color == Color.WHITE:
            for j in incrementRook:
                n = i.index_board + j
                while position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                                                 
                        listWhiteMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                                            
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listBlackPieces.remove(y)
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                        listWhiteMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                  

        if i.pieceType == 'KNIGHT' and i.color == Color.WHITE:
            for j in incrementKnight:
                n = i.index_board + j
                if position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                                                   
                        listWhiteMove.append(SimpleMove(i.index_board, n, i, False, None))
                       
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                                      
                 
                    
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listBlackPieces.remove(y)
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                        listWhiteMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                   

        if i.pieceType == 'KING' and i.color == Color.WHITE:
            global checkWhite
            for j in incrementQueen:
                n = i.index_board + j
                if position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x  
                        position[i.index_board] = z
                        i.firstMove = xx
                                                
                        listWhiteMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                                      
                 
                    
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listBlackPieces.remove(y)
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                        listWhiteMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                                            

        if i.pieceType == 'PAWN' and i.color == Color.WHITE:
            for j in incrementWhitePawn:
                n = i.index_board + j
               
                if j == -16 and position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                                                  
                        listWhiteMove.append(SimpleMove(i.index_board, n, i, False, None))
                       
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                       
                  
                if j == -32 and position[n] == 0 and position[n+16] == 0 and i.firstMove==False:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                                                 
                        listWhiteMove.append(SimpleMove(i.index_board, n, i, True, n+16))
                        
                    else:
                        position[n] = y
                        i.index_board = x  
                        position[i.index_board] = z
                        i.firstMove = xx
                        
                   
                if j == -15 and type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listBlackPieces.remove(y)
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                        listWhiteMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                  
                if j == -17 and type(position[n]) != str and type(position[n]) != int and position[n].color == Color.BLACK:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listBlackPieces.remove(y)
                    if defineCheckWhite(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y)
                        listWhiteMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackPieces.append(y) 
    defineLongCastlingWhite()
    defineShortCastlingWhite()
    enPassantWhite(position)

def listBPieces(position):
    global listBlackMove #список ходов черных фигур
    listBlackMove = []
    for i in listBlackPieces:
    
        if i.pieceType == 'QUEEN' and i.color == Color.BLACK:
            for j in incrementQueen:
                n = i.index_board + j
                while position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listWhitePieces.remove(y)
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                        listBlackMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                  

        if i.pieceType == 'BISHOP' and i.color == Color.BLACK:
            for j in incrementBishop:
                n = i.index_board + j
                while position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listWhitePieces.remove(y)
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                        listBlackMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                   
        if i.pieceType == 'ROOK' and i.color == Color.BLACK:
            for j in incrementRook:
                n = i.index_board + j
                while position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                    n = n + j
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listWhitePieces.remove(y)
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                        listBlackMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                   

        if i.pieceType == 'KNIGHT' and i.color == Color.BLACK:
            for j in incrementKnight:
                n = i.index_board + j
                if position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                    
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listWhitePieces.remove(y)
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                        listBlackMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                  

        if i.pieceType == 'KING' and i.color == Color.BLACK:
            for j in incrementQueen:
                n = i.index_board + j
                if position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                    
                if type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listWhitePieces.remove(y)
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                        listBlackMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)                                   
                

        if i.pieceType == 'PAWN' and i.color == Color.BLACK:
            for j in incrementBlackPawn:
                n = i.index_board + j
                if j == 16 and position[n] == 0:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackMove.append(SimpleMove(i.index_board, n, i, False, None))
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                if j == 32 and position[n] == 0 and position[n-16] == 0 and i.firstMove==False:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listBlackMove.append(SimpleMove(i.index_board, n, i, True, n-16))
                    else:
                        position[n] = y
                        i.index_board = x
                        position[i.index_board] = z
                        i.firstMove = xx
                if j == 15 and type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listWhitePieces.remove(y)
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                        listBlackMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                 
                if j == 17 and type(position[n]) != str and type(position[n]) != int and position[n].color == Color.WHITE:
                    x = i.index_board
                    y = position[n]
                    z = position[i.index_board]
                    xx = i.firstMove
                    position[n] = i
                    position[i.index_board] = 0
                    i.firstMove = True
                    i.index_board = n
                    listWhitePieces.remove(y)
                    if defineCheckBlack(position) == False:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
                        listBlackMove.append(Capture(i.index_board, n, i, position[n], False, None))
                    else:
                        position[n] = y
                        i.index_board = x 
                        position[i.index_board] = z
                        i.firstMove = xx
                        listWhitePieces.append(y)
    defineLongCastlingBlack()
    defineShortCastlingBlack()
    enPassantBlack(position)
    

                  
                    
listWPieces(position)
listBPieces(position)
allPosition = []
note3EnPassantWhite1 = False
note3EnPassantWhite2 = False
note3EnPassantBlack1 = False
note3EnPassantBlack2 = False

allPosition.append([convertPosition(position), lastMoveColor, longCastlingWhite, shortCastlingWhite, longCastlingBlack, shortCastlingBlack, note3EnPassantWhite1, note3EnPassantWhite2, note3EnPassantBlack1, note3EnPassantBlack2])
iteratesThroughList(allPosition)

f = open(r"zapisPGN.pgn",  "w")
f.write('[Event "?"]\n[Site "Lipetsk"]\n[Date "????.??.??"]\n[Round "1"]\n[White "Puteets66066"]\n[Black "Tolcheev, Iurii"]\n[Result "*"]\n')
f.close()
numberMove = 1
colorBoard = Color.WHITE

def rotate():
    global colorBoard
    
    if colorBoard == Color.WHITE:
        squareRotateBlack()
        deleteView(listPiecesView)
        drawPositionBlack(position)

        colorBoard = Color.BLACK
        perimeterRotateBlack()
        
    else:
        squareRotateWhite()
        deleteView(listPiecesViewB)
        drawPositionWhite(position)

        colorBoard = Color.WHITE
        perimeterRotateWhite()
       
    
    
    
    

#отображение
window.show()
view.show()
sys.exit(app.exec_())
