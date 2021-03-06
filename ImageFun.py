import os
from PIL import Image
import json
import time
import uuid
import base64
import model
from config import DETECTANGLE
from apphelper.image import union_rbox
from application import trainTicket,idcard

def main():
 	billModel = '通用OCR'
 	path = 'test/t3.jpg'
 	img = Image.open(path).convert("RGB")
 	W,H = img.size
 	timeTake = time.time()
 	_,result,angle= model.model(img,
                                    detectAngle=DETECTANGLE,##是否进行文字方向检测
                                    config=dict(MAX_HORIZONTAL_GAP=100,##字符之间的最大间隔，用于文本行的合并
                                    MIN_V_OVERLAPS=0.7,
                                    MIN_SIZE_SIM=0.7,
                                    TEXT_PROPOSALS_MIN_SCORE=0.1,
                                    TEXT_PROPOSALS_NMS_THRESH=0.3,
                                    TEXT_LINE_NMS_THRESH = 0.99,##文本行之间测iou值
                                    MIN_RATIO=1.0,
                                    LINE_MIN_SCORE=0.2,
                                    TEXT_PROPOSALS_WIDTH=0,
                                    MIN_NUM_PROPOSALS=0,                                               
                ),
                                    leftAdjust=True,##对检测的文本行进行向左延伸
                                    rightAdjust=True,##对检测的文本行进行向右延伸
                                    alph=0.2,##对检测的文本行进行向右、左延伸的倍数
                                    ifadjustDegree=False##是否先小角度调整文字倾斜角度
                                   )
    
 	if billModel=='' or billModel=='通用OCR':
            result = union_rbox(result,0.2)
            res = [{'text':x['text'],'name':str(i)} for i,x in enumerate(result)]
 	elif billModel=='火车票':
            res = trainTicket.trainTicket(result)
            res = res.res
            res =[ {'text':res[key],'name':key} for key in res]

 	elif billModel=='身份证':

            res = idcard.idcard(result)
            res = res.res
            res =[ {'text':res[key],'name':key} for key in res]
 	print(result)
main()
