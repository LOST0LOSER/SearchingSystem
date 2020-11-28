
def mergeTwoList(list1,list2):
    resultlist = []
    len1 = len(list1)
    len2 = len(list2)
    n1 = 0
    n2 = 0
    while n1 < len1 and n2 < len2 :
        if list1[n1] < list2[n2]:
            resultlist.append(list1[n1])
            n1 += 1
        elif list1[n1] > list2[n2]:
            resultlist.append(list2[n2])
            n2 += 1
        else:
            resultlist.append(list1[n1])
            n1 += 1
            n2 += 1

    if n1 < len1:
        resultlist.extend(list1[n1 : len1])
    if n2 < len2:
        resultlist.extend(list2[n2 : len2])
    return resultlist



def andTwoList(list1,list2):
    resultlist = []
    len1 = len(list1)
    len2 = len(list2)
    n1 = 0
    n2 = 0
    while n1 < len1 and n2 < len2:
        if list1[n1] < list2[n2]:
            n1 += 1
        elif list1[n1] > list2[n2]:
            n2 += 1
        else:
            resultlist.append(list1[n1])
            n1 += 1
            n2 += 1
    return resultlist

#list1中不包含list2的
def listNotcontain(list1,list2):
    resultlist = []
    len1 = len(list1)
    len2 = len(list2)
    n1 = 0
    n2 = 0
    while n1 < len1 and n2 < len2:
        if list1[n1] < list2[n2]:
            resultlist.append(list1[n1])
            n1 += 1
        elif list1[n1] > list2[n2]:
            n2 += 1
        else:
            n1 += 1
            n2 += 1
    return resultlist


# list1 = [1,3,4,5,6,7,9,10]
# list2 = [2,4,6,8,10,12]