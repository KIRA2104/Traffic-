import cv2
import os
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

# Replace with the direct URL obtained from yt-dlp
url = "https://rr8---sn-b51vo-2o9z.googlevideo.com/videoplayback?expire=1743201450&ei=StDmZ8qcCduJ9fwP9NrnsAw&ip=43.228.74.50&id=o-AM84SKjsBm8_M2_rR93fQYOdt0isSvJmGc8ovk5YZVwh&itag=313&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C271%2C278%2C313&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1743179850%2C&mh=_Q&mm=31%2C29&mn=sn-b51vo-2o9z%2Csn-cvh7knzl&ms=au%2Crdu&mv=m&mvi=8&pcm2cms=yes&pl=24&rms=au%2Cau&initcwndbps=1635000&bui=AccgBcNNKLPnrE_1sjo0mYdyjaYrxWf4Qyw-FjDgeDVYTOA15qMkvOuwL9MC0cE3dOyXdMhiosZ24src&vprv=1&svpuc=1&mime=video%2Fwebm&ns=ks5_Yw37Ue9lW4xnPnzJBRcQ&rqh=1&gir=yes&clen=505276332&dur=306.133&lmt=1726216654265241&mt=1743179139&fvip=4&keepalive=yes&lmw=1&c=TVHTML5&sefc=1&txp=531F224&n=r-ARrIlfjRajMA&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRQIhAMMdyCbsixJsLbVQUoq-lPCxurielhL3PgRpSqdZNdpuAiBg6tR7eW9evgZSZJMmvxyJML1x8wzUjNAr82VquMGjfA%3D%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Crms%2Cinitcwndbps&lsig=AFVRHeAwRgIhAKTBalI7mHeBamGrHB0QmgbPhEsVc-XuU8skGrPZ_VwkAiEAzlc1Rtoe_FflSvT1N0k8VRjYzHIDjC6sLx-sxX3umC0%3D"

cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from stream.")
        break

    cv2.imshow("Live Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
