NodeList = []
LastList = []
with open('NodeList.txt',"r") as f: 
    str1 = f.read()
    str_split = str1.split(',')
    list_len = len(str_split)
    line=1
    for i in str_split:
        if line == list_len: i=i[:-2]
        if len(i) ==  8: LastList.append(i)
        elif len(i) == 12:
            NodeList.append(i[0:6])
            NodeList.append(i[7:])
        elif len(i) == 13:
            NodeList.append(i[0:6])
            NodeList.append(i[7:12])
        else:
            if len(i) == 9:
                NodeList.append(i[0:6])
                NodeList.append(i[7:])
            elif len(i) == 3:
                NodeList.append(i[0:2])
            else:
                NodeList.append(i)
        line=line+1
#print(NodeList)
#print(LastList)
for i in range(len(NodeList)):
    if len(NodeList[i])==6: head=NodeList[i]
    else:
        if len(NodeList[i])==2: LastList.append(head+NodeList[i])
        else:
            index = NodeList[i].split('-')
            start = index[0]
            end = index[1]
            for j in range(int(start),int(end)+1):
                if j >= 10:
                    tmp = str(j) 
                    LastList.append(head+tmp)
                else: 
                    tmp = str(j)
                    LastList.append(head+'0'+tmp)

file = open("NodeList.txt", 'w').close()
f = open('NodeList.txt','a', encoding='utf-8')
for i in LastList:
    f.write(i+'\n')
f.close()
