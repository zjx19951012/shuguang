#!/bin/sh
#注意！！！！！！需要python3!!!
#本脚本用来检测节点报错情况
#使用方法：./CheckNode.sh JOBID TIME   

#检查/opt/gridview/slurm/log/nhc_script.log，例子如下：
#./CheckNode.sh 14326937 '2021-11-19 14'

#检查cat /var/log/messages，例子如下：
#./Check 14326937 'Dec  3 16:17'

sacct -j $1 --format=NodeList -p | grep -v NodeList | cut -d "|" -f 1 | sed -n '1p' > NodeList.txt
echo "寻找 $2 这一段时间的报错"
python zjx_Normalized_NodeList.py

rm Nodelog.txt

if [[ $2 == 2* ]];then
  for i in `cat NodeList.txt`;do
    echo ssh $i
    ssh $i cat /opt/gridview/slurm/log/nhc_script.log | grep "$2"
    #ssh $i tail -n 1 /opt/gridview/slurm/log/nhc_script.log | grep "$2"
  done >> Nodelog.txt
else
  for i in `cat NodeList.txt`;do
    echo ssh $i
    ssh $i cat /var/log/messages | grep "$2"
  done >> Nodelog.txt 
fi
echo "记录保存至Nodelog.txt中"
