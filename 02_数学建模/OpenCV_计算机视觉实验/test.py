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
arm = Virtual_WlkataMirobot(server_IP="172.20.10.6", server_port=5478)

# arm.set_Single_modbusValues(301,0)
### 'robot1 6轴复位'
# arm.home(com1=True)

arm.set_joint_angle(com1_P=p41)


arm.set_Output(xipan,0)
arm.set_Output(tuigang,0)
time.sleep(1)
start_time=time.time()
end_time=time.time()

while True:
    time.sleep(1)
    
    guangdian =arm.get_Input(4)

    if guangdian == 1:
        start_time=time.time()
        arm.set_Single_modbusValues(301,1)
        #推缸推出
        arm.set_Output(tuigang,0)
        #机器人到物料抓取上方
        arm.set_joint_angle(com1_P = p0,speed=5000)
        #机器人到物料抓取位置
        arm.set_joint_angle(com1_P = p1,speed=5000)
        #机器人打开吸盘
        arm.set_Output(xipan,1)
        #延时，等待吸盘吸附物料
        time.sleep(1)
        arm.set_joint_angle(com1_P = p0,speed=5000)
        
        #放1位置
        if count==0:
            arm.set_Single_modbusValues(301,2)
            arm.set_joint_angle(com1_P = p11,speed=5000)
            arm.set_joint_angle(com1_P = p10,speed=5000)
            #机器人关闭吸盘
            arm.set_Output(xipan,0)
            time.sleep(1)
            arm.set_joint_angle(com1_P = p11,speed=5000)
            count=count+1
            arm.set_Single_modbusValues(300,count)
            end_time=time.time()
            _time=(int)(end_time-start_time)
            print(_time)
            arm.set_Single_modbusValues(302,_time)
            
        elif count==1:
            arm.set_Single_modbusValues(301,3)
            arm.set_joint_angle(com1_P = p21,speed=5000)
            arm.set_joint_angle(com1_P = p20,speed=5000)
            #机器人关闭吸盘
            arm.set_Output(xipan,0)
            time.sleep(1)
            arm.set_joint_angle(com1_P = p21,speed=5000)
            count=count+1
            arm.set_Single_modbusValues(300,count)
            end_time=time.time()
            _time=(int)(end_time-start_time)
            print(_time)
            arm.set_Single_modbusValues(303,_time)
        
        elif count==2:
            arm.set_Single_modbusValues(301,4)
            arm.set_joint_angle(com1_P = p31,speed=5000)
            arm.set_joint_angle(com1_P = p30,speed=5000)
            #机器人关闭吸盘
            arm.set_Output(xipan,0)
            time.sleep(1)
            arm.set_joint_angle(com1_P = p31,speed=5000)
            count=count+1
            arm.set_Single_modbusValues(300,count)
            end_time=time.time()
            _time=(int)(end_time-start_time)
            print(_time)
            arm.set_Single_modbusValues(304,_time)
        
        elif count==3:
            arm.set_Single_modbusValues(301,5)
            arm.set_joint_angle(com1_P = p41,speed=5000)
            arm.set_joint_angle(com1_P = p40,speed=5000)
            #机器人关闭吸盘
            arm.set_Output(xipan,0)
            time.sleep(1)
            arm.set_joint_angle(com1_P = p41,speed=5000)
            count=count+1
            arm.set_Single_modbusValues(300,count)
            arm.set_Single_modbusValues(301,0)
            end_time=time.time()
            _time=(int)(end_time-start_time)
            print(_time)
            arm.set_Single_modbusValues(305,_time)
            break
    
    else:
        #推物料
        arm.set_Output(tuigang,1)
        time.sleep(2)
        arm.set_Output(tuigang,0)
    

        
        