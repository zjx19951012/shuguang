import argparse
parser = argparse.ArgumentParser(description='para transfer')
parser.add_argument('--function', default=1, help='1:NodeList.txt标准化;2:LIDlog标准化')
args = parser.parse_args()

def Normalized_Lidlog():
    with open('LIDlog.txt',"r") as f:
        str1 = f.read()
        strings = str1.split('\n')
    if strings[-1] == '':del strings[-1]

    single_lid=[]
    multi_lid=[]
    tmp=0
    for i in strings:
        if 'ssh' in i:
            nodetmp = i.split(' ')[1]
            tmp=0
            continue
        if int(i) == tmp and nodetmp not in single_lid:
            single_lid.append(nodetmp)
        elif tmp != 0 and int(i) != tmp and nodetmp not in multi_lid:
            multi_lid.append(nodetmp)
        tmp = int(i)
    tmp=''
    Newstrings=[]
    for i in strings:
        if 'ssh' in i:
            Newstrings.append(i)
            tmp = i
            continue
        elif i == tmp:continue
        else:
            tmp = i
            Newstrings.append(i)
    file = open("LIDlog.txt", 'w').close()
    f = open('LIDlog.txt','a', encoding='utf-8')
    for i in Newstrings:
        f.write(i+'\n')
    f.close()
    if len(single_lid)==0:
        print('所有节点都为多lid')
    elif len(multi_lid)==0:
        print('所有节点都为单lid')
    else:
        print('多lid节点如下：')
        print(multi_lid)
        print('单lid节点如下：')
        print(single_lid)
    print('相关信息保存于LIDlog.txt')

def Normalized_NodeList():
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


def Got_Cards_Info():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
    deviceList = listDevices()
    if deviceList is None:
        print('获取设备列表失败')
        sys.exit(1)
    for device in deviceList:
        memInfo = getMemInfo(device, 'vram')
        if memInfo[0] == None or memInfo[1] == None:
            print('显存读取失败')
            sys.exit(1)
        if getGpuUse(device) != -1:
            gpu_busy = str(getGpuUse(device)) + '%'
        mem_use_pct = '% 3.0f%%' % (100 * (float(memInfo[0]) / float(memInfo[1])))
        print(mem_use_pct,gpu_busy)


if args.function == '1':
    Normalized_NodeList()
elif args.function == '2':
    Normalized_Lidlog() 
elif args.function == '3':
    import sys
    import json
    sys.path.append('/public/software/compiler/rocm/rocm-4.0.1/bin')
    from rocm_smi import *
    Got_Cards_Info()
