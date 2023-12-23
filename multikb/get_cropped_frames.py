import numpy as np
import cv2

__all__ = ["main"]

def aspect_ratio(aratio, width, height):
    """TODO: Docstring for aspect_ratio.

    :aratio: TODO
    :width: TODO
    :height: TODO
    :returns: TODO

    """

    a = width/height

    if width/height >= aratio:
        return int(height*aratio), height 
    else:
        return width, int(width/aratio)

def frame_filter(frame, crop_filter, crop, aratio, fcount):
    """TODO: Docstring for frame_filter.

    :frame: TODO
    :crop_filter: TODO
    :crop: TODO
    :aratio: TODO
    :returns: TODO

    """
    # top left corner (y,x) coordinates
    tl = (crop[1], crop[0])

    # bottom right corner (y,x) coordinates
    br = (crop[1]+crop[2], crop[0]+int(aratio*crop[2]))

    output = crop_filter.copy()
    output[tl[0]:br[0], tl[1]:br[1]] = frame[tl[0]:br[0], tl[1]:br[1]]
    return output

def xy_mouse(event, x, y, flags, param):
    """TODO: Docstring for xy_mouse.

    :event: TODO
    :x: TODO
    :y: TODO
    :flags: TODO
    :param: TODO
    :returns: TODO

    """
    global crop
    if event == cv2.EVENT_LBUTTONDOWN: #EVENT_LBUTTONDBLCLK:
        crop[0] = x
        crop[1] = y
        print("Changes: x={}, y={}".format(*crop))
    elif event == cv2.EVENT_LBUTTONUP:
        h = y-crop[1]
        if h>0:
            crop[2] = h 
            print("Changes: h={}".format(crop[2]))
def main(file_in, file_out,aratio, freq=1, fill_color=[255,255,255]):
    """TODO: Docstring for main.

    :file_in: TODO
    :returns: TODO

    """
    global crop
    cap = cv2.VideoCapture(file_in)

    if (cap.isOpened()==False):
        raise("Unable to read the given video")

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    nf = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)+0.5)

    Ffreq = int(fps/freq)


    w_out, h_out = aspect_ratio(aratio,width,height)

    
    data_out = []

    crop = np.array([0,0,h_out])
    fcount = 0
    crop_filter = np.full((height, width,3), fill_color, dtype=np.uint8) 

    print("Click left mouse button and drag inorder to select area\n or press  x,y or h to change xy-coordinates of top left coorner and height of the crop")

    while (True):
        ret, frame = cap.read()
        if (ret == True) and (fcount%Ffreq==0 or fcount==nf-1):
            

            msg = "Frame {}".format(fcount)
            cv2.namedWindow(msg)
            cv2.setMouseCallback(msg, xy_mouse)

            stop = False
            while(True):
                output = frame_filter(frame, crop_filter, crop, aratio, fcount)       
                #print(crop)
                cv2.addWeighted(frame, 0.2, output, 1-0.2, 0, output)
                cv2.imshow(msg, output)

                key = cv2.waitKey(25) & 0xFF

                if key == ord("x"):
                    x = int(input("Give new x coord: "))
                    print("Changes: x={}".format(x))
                    crop[0]= x 

                elif key == ord("y"):
                    y = int(input("Give new y coord: "))
                    print("Changes: y={}".format(y))
                    crop[1] = y

                elif key == ord("h"):
                    h = int(input("Give new height: "))
                    print("Changes: h={}".format(h))
                    crop[2] = h

                elif key == ord("d"):
                    if (0<= crop[0]) and (0<=crop[1]) and (crop[0]+int(aratio*crop[2])<=width) and (crop[1]+crop[2]<=height):
                        cv2.destroyWindow(msg)
                        data_out.append([fcount]+list(crop.copy()) )
                        break
                    else:
                        print("CHOSEN AREA IS NOT INSIDE THE ORIGINAL FRAME:")
                        print("RECHOOSE THE AREA!")

                elif key == ord("q"):
                    stop = True
                    break

            if stop:
                break

        if ret==False:
            # all frames read
            break
        fcount+=1

    cap.release()
    cv2.destroyAllWindows()
    np.save(file_out, data_out)


if __name__ == "__main__":
    from sys import argv

    file_in, file_out, aratio, freq = argv[1:]

    a = aratio.split(":")
    aratio = int(a[0])/int(a[1])
    freq = float(freq)
    main(file_in, file_out, aratio, freq)
