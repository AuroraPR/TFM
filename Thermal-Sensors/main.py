import cv2
import time 
import os
import numpy as np
from flirpy.camera.lepton import Lepton

path=os.path.join(os.getcwd(),"ImagesGRAYSCALE")
path2=os.path.join(os.getcwd(),"ImagesHEATMAP")
path3=os.path.join(os.getcwd(),"ImagesCAMERA")

os.system("mkdir "+str(path))
os.system("mkdir "+str(path2))
os.system("mkdir "+str(path3))

dsize = (160, 120)
i=0

with Lepton() as thermal:
    camera=cv2.VideoCapture(0)
    while True:
        img = thermal.grab().astype(np.float32)
        ret,imgCam=camera.read()
        # Rescale to 8 bit
        img=255*(img - img.min())/(img.max()-img.min())
        if i>0: cv2.imwrite(os.path.join(path , str(i-1)+".jpg"), img.astype(np.uint8))
        if i>0: cv2.imwrite(os.path.join(path2 , str(i-1)+".jpg"), cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_INFERNO))
        #cv2.imshow('lepton', img.astype(np.uint8))        
        cv2.imwrite(os.path.join(path3 , str(i)+".jpg"), cv2.resize(imgCam, dsize))
        time.sleep(1)
        print(str(i) + "\n")
        i+=1
        
        
#camera.release()
#cv2.destroyAllWindows()