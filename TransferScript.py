import pymel.core as pm
import pymel.core.datatypes as dt

def printHierarchy(node, childList, rot, ori, thisVar):
    #pm.currentTime(0, edit = True)
    if thisVar is True:
        childList.insert(0, node)
        rot.insert(0, node.getRotation().asMatrix())
        ori.insert(0, node.getOrientation().asMatrix())
        thisVar = False
    
    for child in node.getChildren():
        rot.append(child.getRotation().asMatrix())
        ori.append(child.getOrientation().asMatrix()) 
        childList.append(child)
        
        if child.numChildren() > 0:
            printHierarchy(child, childList, rot, ori, thisVar)


#def reorderJoints(jointList, newList):
 #   loopVar = 0
  #  for all in newList:
   #     jointList[loopVar] = all
    #    loopVar += 1

def skeletalSwitch(nodeToSwitch, root2, vari, jointListSource, jointListTarget, rotLst, oriLst, tOriLst):
    parentMat = dt.Matrix()
    tParentMat = dt.Matrix()
    time = 0
    print pm.keyframe(nodeToSwitch, query = True, attribute = 'translateX')
    while time < 23: #631
        if pm.keyframe(query = True, time = time):    #Only set keyframes where there already are
            while vari < len(jointListSource):
                pm.currentTime(0, edit = True)
                for parents in jointListSource[vari].getParent(generations=None):
                    parentMat *= (parents.getOrientation().asMatrix() * parents.getRotation().asMatrix())
                    #print parents + " : " + jointListSource[vari]
                
                for tParents in jointListTarget[vari].getParent(generations=None):
                    tParentMat *= (tParents.getOrientation().asMatrix() * tParents.getRotation().asMatrix()) 
                    #print tParents + " : " + jointListTarget[vari]   
                
                pm.currentTime(time, edit = True)
                isolatedRot = rotLst[vari].inverse() * jointListSource[vari].getRotation().asMatrix()
                worldSpaceRot = oriLst[vari].inverse() * parentMat.inverse() * isolatedRot * parentMat * oriLst[vari]
                tranRot = tOriLst[vari] * tParentMat * worldSpaceRot * tParentMat.inverse() * tOriLst[vari].inverse()
                
                pm.rotate(jointListTarget[vari], 0, 0 , 0)
                jointListTarget[vari].rotateBy(tranRot)
                if vari is 0:
                    pm.move(root2, nodeToSwitch.translate.get())
                pm.setKeyframe(jointListTarget[vari])
                vari += 1
                parentMat.setToIdentity()
                tParentMat.setToIdentity()
        vari = 0
        time += 1
 

def setNewListsSource(inList, newList):
	del inList[:]
	#loopVar = 0
	for all in newList:
		inList.append(all)
		#print jointListSource[loopVar]
		#loopVar += 1    
		
def setNewListsTarget(inList, newList):
	del inList[:]
	#del jointListTarget[:]
	for all in newList:
	    inList.append(all)
	    print all
	    #loopVar += 1
	#loopVar = 0
	#jointListTarget = newList
	#while loopVar < len(newList)
	#	jointListTarget[loopVar] = newList[loopVar]
		#print jointListTarget[loopVar]
	#	loopVar += 1
		
def setRoots(frstRoot, scndRoot):
    root = frstRoot
    root2 = scndRoot		  		        
#################################

#def mainFunc(jointListSource, jointListTarget):
##root = pm.ls(sl=True)[0]
##root2 = pm.ls(sl=True)[1] # [1] is the second selected root joint

##rotLst = []
##oriLst = []

##tRotLst = []
##tOriLst = []

##jointListSource = []
##jointListTarget = []

#pm.currentTime(0, edit = True)

#sRootBindpose = root.getRotation()
#sBindposeMat = sRootBindpose.asMatrix()

#rotLst.append(sBindposeMat)
#oriLst.append(root.getOrientation().asMatrix())

#tRotLst.append(root2.getRotation().asMatrix())
#tOriLst.append(root2.getOrientation().asMatrix())

#jointListSource.append(root)
#jointListTarget.append(root2)

##boolVar = True

##printHierarchy(root, jointListSource, rotLst, oriLst, boolVar)
##printHierarchy(root2, jointListTarget, tRotLst, tOriLst, boolVar)

#for all in jointListTarget:
 #   print all
    
##var = 0
##skeletalSwitch(root, root2, var, jointListSource, jointListTarget, rotLst, oriLst, tOriLst)
 
#for all in jointListSource[0].getParent(generations=None):
    #print all

#mainFunc()