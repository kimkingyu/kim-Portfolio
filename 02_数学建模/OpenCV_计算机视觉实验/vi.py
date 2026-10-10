from wlkata_mirobot_Virtual import Virtual_WlkataMirobot
import time

#抓取上方点
p0=[-72,9.4,10.2,0,-19.7,0.2]

# 抓取点
p1=[-72,14.9,15.6,0,-30.4,0.2]


#4放置上方
p41=[-25.5,8.5,10.8,-0.1,-18.3,3.4]
#4放置
p40=[-25.5,13.7,16.2,-0.1,-28.9,3.3]

#3放置上方
p31=[-6.5,-2.5,21.5,0.3,-18,-15.5]
#3放置点
p30=[-6.5,4.3,28,0.3,-31.3,-15.5]
#2放置上方
p21=[13.9,0.2,19.6,0.6,-19,-35.9]
#2放置
p20=[13.9,6.2,25.4,0.7,-30.8,-35.8]
#1放置上方
p11=[31.4,16.2,3.5,0.9,-19.1,-53.3]
#1放置
p10=[31.4,20.6,8,0.9,-27.9,-53.2]


xipan=0
tuigang=1
tg_guangdian=0

count=0
arm = Virtual_WlkataMirobot(server_IP="192.168.10.101", server_port=5478)

# arm.set_Single_modbusValues(301,0)
### 'robot1 6轴复位'
arm.home(com1=True)

arm.set_joint_angle(com1_P=p41)
arm.set_joint_angle(com1_P=p0)