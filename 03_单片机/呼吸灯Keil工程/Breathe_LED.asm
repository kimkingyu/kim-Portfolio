        ORG	  0000H		  ;程序永远从0地址开始
        LJMP  START		  ;安排远转移指令至主程序入口
        ORG	  000BH		  ;定时器0中断入口地址
        LJMP  I_TIM0	  ;转移至定时器0中断子程序
        ORG	  001BH		  ;定时器1中断入口地址
        LJMP  I_TIM1	  ;转移至定时器1中断子程序
		
        ORG	  0200H		  ;主程序起始地址
START:  SETB  EA		  ;开全局中断
        SETB  ET0		  ;开定时器0中断
        SETB  ET1		  ;开定时器1中断
        MOV	  TMOD, #11H  ;定时器0和1工作模式1（16位）
        MOV	  TH1,  #0FCH ;设置定时器1初值为64536，定时1000周期，也就是1ms，PWM频率1kHz
        MOV	  TL1,  #18H	
        MOV	  R0,	#18H  ;R0和R1用来存储定时器0定时初值，初值设为FC18H
        MOV	  R1,	#0FCH	
        CLR	  20H.0		  ;利用位地址20H.0标记占空比变化方向，0减小，1增大，初始状态0
        SETB  TR1		  ;启动定时器1
		SJMP  $           ;原地循环，等待中断
			
		;定时器0中断程序，用来改变占空比
I_TIM0:	CLR	  TR0		  ;停止定时器0        
		CLR	  P2.7		  ;将P1.0引脚变为低电平，点亮LED
		JB	  00H,DOWN    ;检测标志位，如为1，则初值减1
		INC   R0          ;R1：R0组成的16位寄存器整体加1，用来对定时初值加1
		CJNE  R0, #00H,SWITCH1
		INC   R1		
SWITCH1:CJNE  R1, #0FFH, T0END		  ;如果没有加到最大值，跳到中断结尾
		CJNE  R0, #0FFH, T0END
		SETB  20H.0		  ;如果加到最大，标志置为1，并将R0，R1的16位寄存器恢复到FFFFH
		SJMP  T0END		
DOWN:	DEC   R0	      ;16位寄存器减1程序段
        CJNE  R0, #0FFH,SWITCH2
        DEC   R1		
SWITCH2:CJNE  R1, #0FCH, T0END	  ;如果没有减到最小，转至中断结尾
		CJNE  R0, #18H, T0END
		CLR	  20H.0		  ;否则清除标志位，下次加1
			
T0END:	MOV	  TL0,	R0	  ;将R1，R0赋值给定时器0初值寄存器
		MOV	  TH0,	R1	
		RETI			  ;中断返回
		
		;定时器1中断程序，负责控制PWM频率，并启动定时器0
I_TIM1:	SETB  TR0		  ;启动定时器0
		SETB  P2.7	      ;将P1.0引脚置位为高电平
		MOV	  TH1,	#0FCH  ;设定定时器1初值为64536
		MOV	  TL1,	#18H	
		RETI			  ;中断返回
				
		END			      ;程序结束
