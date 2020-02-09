import numpy as np

# 将输入的string转换为list
def changeStr2List(theStr):
    locationStr = theStr
    locationStr = locationStr[1:len(locationStr) - 1]
    theListStr = locationStr.split(';')
    locationList = []
    for item in theListStr:
        item = item[1:len(item) - 1]
        # print(item)
        item = item.split(',')
        tmpList = []
        tmpList.append(int(item[0]))
        tmpList.append(int(item[1]))
        locationList.append(tmpList)
    return locationList

# 用于生成初始矩阵
def initMatrix():
    print('请输入矩阵维度：(example:2*3)')
    dimensionStr=input()
    row=int(dimensionStr.split('*')[0])
    line=int(dimensionStr.split('*')[-1])
    # print(row,line)
    theMatrix=np.zeros([row,line],int)-np.ones([row,line],int)
    print('请输入哪些位置为亮灯:(example:[[0,1];[1,2]])')
    locationStr=input()
    if locationStr!='无':
        locationList=changeStr2List(locationStr)
        for location in locationList:
            rowIndex=location[0];lineIndex=location[1]
            theMatrix[rowIndex,lineIndex]=1
    # print(theMatrix)
    print('请输入哪些位置为灭灯:(example:[[0,1];[1,2]])')
    locationStr = input()
    if locationStr!='无':
        locationList = changeStr2List(locationStr)
        for location in locationList:
            rowIndex=location[0];lineIndex=location[1]
            theMatrix[rowIndex,lineIndex]=0
    return theMatrix

# 判断当前状态是否为成功状态
def checkSuccess(theMatrix):
    row,line=theMatrix.shape
    for i in range(row):
        for j in range(line):
            if theMatrix[i][j]==0:
                return 0
    return 1

# 点亮某个灯后，更改状态函数
def changeState(location,theMatrix):
    theMatrix[location[0]][location[1]]=1-theMatrix[location[0]][location[1]]
    shape=theMatrix.shape
    row=location[0];line=location[1]
    neighborList=[[row-1,line],[row,line-1],[row,line+1],[row+1,line]]
    rightNeighborList=[]
    for neighbor in neighborList:
        if neighbor[0]>=0 and neighbor[0]<shape[0] and neighbor[1]>=0 and neighbor[1]<shape[1]:
            if theMatrix[neighbor[0]][neighbor[1]]!=-1:
                rightNeighborList.append(neighbor)
    for location in rightNeighborList:
        row=location[0];line=location[1]
        if theMatrix[row][line]==-1:
            raise ValueError('Error!该坐标下元素为-1')
        else:
            theMatrix[row][line]=1-theMatrix[row][line]
    # print(theMatrix)
    return theMatrix

def getAllPossibleLocation(theMatrix):
    locationList=[]
    for row in range(theMatrix.shape[0]):
        for line in range(theMatrix.shape[1]):
            if theMatrix[row][line]==0:
                locationList.append([row,line])
    return locationList

# 判断一个矩阵是否已经存在当前的List当中
def judgeIn(tmpMatrix,theList):
    for item in theList:
        if (tmpMatrix==item).all():
            return True
    return False

# 主函数
def theMain(theStateHistory,rightPath):
    row,line=theStateHistory[-1].shape
    theMatrix = theStateHistory[-1]

    # 获取当前矩阵下所有灭灯的位置
    possibleLocation=getAllPossibleLocation(theMatrix)

    #开始进行遍历
    for location in possibleLocation:
        # tmp = theStateHistory[-1] - np.zeros([theMatrix.shape[0], theMatrix.shape[1]], int)
        tmp = theStateHistory[-1].copy()
        tmpMatrix=changeState(location,tmp)
        if not judgeIn(tmpMatrix,theStateHistory):
            if len(rightPath)<=10:
                if checkSuccess(tmpMatrix)==1:
                    rightPath.append([location[0],location[1]])
                    if len(rightPath)<=50:

                        # 为了使输出时下标从1开始
                        thePath=[]
                        for item in rightPath:
                            thePath.append(item.copy())
                        for i in range(len(thePath)):
                            for j in range(len(thePath[i])):
                                thePath[i][j]+=1
                        print("成功！","路径是：",thePath)
                    rightPath.pop()
                else:
                    # theMatrix = tmpMatrix - np.zeros([theMatrix.shape[0], theMatrix.shape[1]], int)
                    theMatrix=tmpMatrix.copy()
                    theStateHistory.append(theMatrix)
                    rightPath.append(location)
                    theMain(theStateHistory,rightPath)
    if len(rightPath)!=0:
        rightPath.pop()
    theStateHistory.pop()



if __name__=='__main__':
    theStateHistory=[]
    theMatrix = initMatrix()
    print('初始矩阵状态')
    print(theMatrix)
    theStateHistory.append(theMatrix)
    rightPath=[]
    theMain(theStateHistory,rightPath)
