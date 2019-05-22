from maya import OpenMayaUI as omui
import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import sys
sys.path.insert(0, 'D:\Animation\Skripting PyMel')
import TransferScript
reload(TransferScript)

childLstSource = []
childLstTarget = []

sRotLst = []
sOriLst = []

tRotLst = []
tOriLst = []

myBool = True
myBool2 = True

def getMayaWin():
	mayaWinPtr = omui.MQtUtil.mainWindow( )
	mayaWin = wrapInstance( long( mayaWinPtr ), QWidget )


def loadUI( path ):
	loader = QUiLoader()
	uiFile = QFile( path )

	dirIconShapes = ""
	buff = None

	if uiFile.exists():
		dirIconShapes = path
		uiFile.open( QFile.ReadOnly )

		buff = QByteArray( uiFile.readAll() )
		uiFile.close()
	else:
		print "UI file missing! Exiting..."
		exit(-1)

	fixXML( path, buff )
	qbuff = QBuffer()
	qbuff.open( QBuffer.ReadOnly | QBuffer.WriteOnly )
	qbuff.write( buff )
	qbuff.seek( 0 )
	ui = loader.load( qbuff, parentWidget = getMayaWin() )
	ui.path = path

	return ui


def fixXML( path, qbyteArray ):
	# first replace forward slashes for backslashes
	if path[-1] != '/':
		path += '/'
	path = path.replace( "/", "\\" )

	# construct whole new path with <pixmap> at the begining
	tempArr = QByteArray( "<pixmap>" + path + "\\" )

	# search for the word <pixmap>
	lastPos = qbyteArray.indexOf( "<pixmap>", 0 )
	while lastPos != -1:
		qbyteArray.replace( lastPos, len( "<pixmap>" ), tempArr )
		lastPos = qbyteArray.indexOf( "<pixmap>", lastPos + 1 )
	return


class UIController:
	def __init__( self, ui ):
	
		# Connect each signal to it's slot one by one
		ui.transferButton.clicked.connect( self.ButtonClicked )
		
		ui.sRoot.editingFinished.connect(self.getRoots)
		ui.tRoot.editingFinished.connect(self.getRoots)
		
		ui.sRoot.editingFinished.connect(self.printInList)
		ui.tRoot.editingFinished.connect(self.printInList)
		
		ui.upButton.clicked.connect(self.goUp)
		ui.upButton_2.clicked.connect(self.goUp2)
		ui.downButton.clicked.connect(self.goDown)
		ui.downButton_2.clicked.connect(self.goDown2)
		
		ui.delButton.clicked.connect(self.deleteJoint)
		ui.delButton_2.clicked.connect(self.deleteJoint2)
		#TransferScript.setNewListsSource(childLstSource)
		#TransferScript.setNewListsTarget(childLstTarget)

		self.ui = ui
		ui.setWindowFlags( Qt.WindowStaysOnTopHint )
		ui.show()
        
	def ButtonClicked( self ):
	    varia = 0
	    TransferScript.skeletalSwitch(pm.ls(sl=True)[0], pm.ls(sl=True)[1], varia, childLstSource, childLstTarget, sRotLst, sOriLst, tOriLst)

	def getRoots( self ):
		pm.select(pm.ls(self.ui.sRoot.text()))
		pm.select(pm.ls(self.ui.tRoot.text()), add = True)
		#if pm.ls(self.ui.tRoot.text()) and pm.ls(self.ui.tRoot.text()):
			#reload(TransferScript)
		    #TransferScript.setRoots(pm.ls(sl=True)[0], pm.ls(sl=True)[1])
		 #   TransferScript.mainFunc()
		
	def printInList( self ):
		self.ui.listWidget.clear()
		self.ui.listWidget_2.clear()
		
		#del childLstSource[:]
		#del childLstTarget[:]
		
		if pm.ls(self.ui.sRoot.text()):
			del childLstSource[:]
			del sRotLst[:]
			del sOriLst[:]
			TransferScript.printHierarchy(pm.ls(sl=True)[0], childLstSource, sRotLst, sOriLst, myBool)
			for all in childLstSource[1:]:
				print all
				self.ui.listWidget.addItem(str(all))
			#TransferScript.setNewListsSource(jointListSource, childLstSource)	
        
		if pm.ls(self.ui.tRoot.text()):
			del childLstTarget[:]
			del tRotLst[:]
			del tOriLst[:]
			TransferScript.printHierarchy(pm.ls(sl=True)[1], childLstTarget, tRotLst, tOriLst, myBool2)
			for all2 in childLstTarget[1:]:
				self.ui.listWidget_2.addItem(str(all2))
			#TransferScript.setNewListsTarget(jointListTarget, childLstTarget)	

	def getChi(self, jointToUse, lstChildren):
		for child in jointToUse.getChildren():
			lstChildren.append(child)
			if child.numChildren() > 0:
				self.getChi(child, lstChildren)
	
	def changeInList(self, oldList, newList):
		oldList = newList
	
	def goUp(self):
		if uiVar.listWidget.currentRow() != 0:
			indexVar1 = uiVar.listWidget.currentRow() + 1
			indexVar2 = uiVar.listWidget.currentRow()
			
			tempHolder = childLstSource[indexVar1] 
			childLstSource[indexVar1] = childLstSource[indexVar2]
			childLstSource[indexVar2] = tempHolder
			
			tempRot = sRotLst[indexVar1]
			sRotLst[indexVar1] = sRotLst[indexVar2]
			sRotLst[indexVar2] = tempRot
			
			tempOri = sOriLst[indexVar1]
			sOriLst[indexVar1] = sOriLst[indexVar2]
			sOriLst[indexVar2] = tempOri
			#TransferScript.setNewListsSource(jointListSource, childLstSource)
			self.ui.listWidget.clear()
			for all in childLstSource[1:]:
				print all
				self.ui.listWidget.addItem(str(all))
				
	def goUp2(self):
		if uiVar.listWidget_2.currentRow() != 0:
			indexVar3 = uiVar.listWidget_2.currentRow() + 1
			indexVar4 = uiVar.listWidget_2.currentRow()
			
			tempHolder2 = childLstTarget[indexVar3] 
			childLstTarget[indexVar3] = childLstTarget[indexVar4]
			childLstTarget[indexVar4] = tempHolder2
			
			tempRot2 = tRotLst[indexVar3]
			tRotLst[indexVar3] = tRotLst[indexVar4]
			tRotLst[indexVar4] = tempRot2
			
			tempOri2 = tOriLst[indexVar3]
			tOriLst[indexVar3] = tOriLst[indexVar4]
			tOriLst[indexVar4] = tempOri2
			#TransferScript.setNewListsTarget(jointListTarget, childLstTarget)
			self.ui.listWidget_2.clear()
			for all in childLstTarget[1:]:
				self.ui.listWidget_2.addItem(str(all))	

	def goDown(self):
		if uiVar.listWidget.currentRow() < len(childLstSource):
			indexVar1 = uiVar.listWidget.currentRow() + 1
			indexVar2 = uiVar.listWidget.currentRow() + 2
			
			tempHolder = childLstSource[indexVar1] 
			childLstSource[indexVar1] = childLstSource[indexVar2]
			childLstSource[indexVar2] = tempHolder
			
			tempRot = sRotLst[indexVar1]
			sRotLst[indexVar1] = sRotLst[indexVar2]
			sRotLst[indexVar2] = tempRot
			
			tempOri = sOriLst[indexVar1]
			sOriLst[indexVar1] = sOriLst[indexVar2]
			sOriLst[indexVar2] = tempOri			
			
			#TransferScript.setNewListsSource(jointListSource, childLstSource)
			self.ui.listWidget.clear()
			for all in childLstSource[1:]:
				print all
				self.ui.listWidget.addItem(str(all))
				
	def goDown2(self):
		if uiVar.listWidget_2.currentRow() < len(childLstTarget):
			indexVar3 = uiVar.listWidget_2.currentRow()
			indexVar4 = uiVar.listWidget_2.currentRow() + 1
			
			tempHolder2 = childLstTarget[indexVar3] 
			childLstTarget[indexVar3] = childLstTarget[indexVar4]
			childLstTarget[indexVar4] = tempHolder2
			
			tempRot2 = tRotLst[indexVar3]
			tRotLst[indexVar3] = tRotLst[indexVar4]
			tRotLst[indexVar4] = tempRot2
			
			tempOri2 = tOriLst[indexVar3]
			tOriLst[indexVar3] = tOriLst[indexVar4]
			tOriLst[indexVar4] = tempOri2
						
			#TransferScript.setNewListsTarget(jointListTarget, childLstTarget)
			self.ui.listWidget_2.clear()
			for all in childLstTarget[1:]:
				#print all
				self.ui.listWidget_2.addItem(str(all))							
	   
	def deleteJoint(self):
		loopTemp = self.ui.listWidget.currentRow() + 1

		print len(childLstSource)
		self.ui.listWidget.takeItem(loopTemp-1)
		del childLstSource[loopTemp]
		print childLstSource[loopTemp]
		del sRotLst[loopTemp]
		del sOriLst[loopTemp]
		#TransferScript.setNewListsSource(jointListSource, childLstSource)  	    
	    
	def deleteJoint2(self):
		loopTemp = self.ui.listWidget_2.currentRow() + 1
		print loopTemp
		print len(childLstTarget)
		self.ui.listWidget_2.takeItem(loopTemp-1)
		del childLstTarget[loopTemp]
		del tRotLst[loopTemp]
		del tOriLst[loopTemp]   	    
		#TransferScript.setNewListsTarget(jointListTarget, childLstTarget)		    
	    	
uiVar = loadUI("D:\Animation\Skripting PyMel\Redovisning Skript\example.ui")
someVar = UIController(uiVar)
#UIController(uiVar).getChi(pm.ls(sl=True)[0], childLstSource)
#for all in childLstSource:
 #   print all