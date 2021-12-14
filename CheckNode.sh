#!/bin/sh
#本脚本用来检测节点报错情况
#使用方法：./CheckNode.sh JOBID 参数。 1代表节点log检查；2代表LID检查。  
#############################################
##--------两种模式--------------------#######
#####1、检查节点log##########################
####./CheckNode.sh 14326937 1 '2021-11-19 14'    检查/opt/gridview/slurm/log/nhc_script.log
####./CheckNode.sh 14326937 1 'Dec  3 16:17'#    检查/var/log/messages  需要root
#####2、检查节点LID##########################
####./CheckNode.sh 14326937 2################    检查节点LID的单/多 
#####3、检查节点Card#########################
####./CheckNode.sh 14326937 3################    检查节点显卡使用情况

module rm compiler/rocm/2.9
module load compiler/rocm/4.0.1
module load apps/PyTorch/1.8.0a0/pytroch_1.8-rocm_4.0.1

sacct -j $1 --format=NodeList -p | grep -v NodeList | cut -d "|" -f 1 | sed -n '1p' > NodeList.txt
/public/software/apps/DeepLearning/PyTorch/torch1.7.0a0-rocm4.0.1-build/bin/python3 zjx_Node.py --function 1

if [[ $2 == 1 ]];then
  echo "寻找 $3 这一段时间的报错"
  rm Nodelog.txt
  if [[ $3 == 2* ]];then
  for i in `cat NodeList.txt`;do
    echo ssh $i
    ssh $i cat /opt/gridview/slurm/log/nhc_script.log | grep "$3"
    #ssh $i tail -n 1 /opt/gridview/slurm/log/nhc_script.log | grep "$2"
  done >> Nodelog.txt
  else
    for i in `cat NodeList.txt`;do
      echo ssh $i
      ssh $i cat /var/log/messages | grep "$3"
    done >> Nodelog.txt 
  fi
  echo "记录保存至Nodelog.txt中"
fi

if [[ $2 == 2 ]];then
  rm LIDlog.txt
  echo "开始检查LID单/多"
  for i in `cat NodeList.txt`;do
    echo ssh $i
    ssh $i /usr/sbin/ibstat | grep Base | awk -F": " '{print $2}'
  done >> LIDlog.txt
  /public/software/apps/DeepLearning/PyTorch/torch1.7.0a0-rocm4.0.1-build/bin/python3 zjx_Node.py --function 2
fi

if [[ $2 == 3 ]];then
  rm Cardlog.txt
  echo "开始检查显卡"
  for i in `cat NodeList.txt`;do
    echo ssh $i
    ssh $i /public/software/apps/DeepLearning/PyTorch/torch1.7.0a0-rocm4.0.1-build/bin/python3 zjx_Node.py --function 3
  done >> Cardlog.txt
  echo "所有卡的使用情况保存在Cardlog.txt中"
fi

