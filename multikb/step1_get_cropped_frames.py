import numpy as np
import cv2

__all__ = ["get_cropped_frames"]

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

def boundary_check(c):
    """TODO: Docstring for boundary_check.

    :c: TODO
    :returns: TODO

    """
    global crop, w_height, w_width, aratio_copy


    x, y, h = crop
    if ("x" in c) and (int(crop[0]+aratio_copy*crop[2]+0.5)>=w_width):
        crop[0] = int(w_width-aratio_copy*crop[2]-1+0.5)

    if ("y" in c) and ( crop[1]+crop[2]>=w_height ):
        crop[1]=max(0,w_height-crop[2]-1)

    if ("h" in c) and ( int(crop[1]+crop[2])>=w_height ):
        crop[2] = max(0,w_height-crop[1]-1)
    if (x,y,h) != tuple(crop):
        print_list = [x, crop[0], y, crop[1], h, crop[2]]
        print("Automatic changes: "+change_string(*print_list))

def change_string(x_old,x,y_old,y,h_old,h):
    """TODO: Docstring for change_string.

    :x_old: TODO
    :x: TODO
    :y_olde: TODO
    :y: TODO
    :h_old: TODO
    :h: TODO
    :returns: TODO

    """
    l = [x_old, x, y_old, y, h_old, h]
    return "x:{}->{}, y:{}->{}, h:{}->{}".format(*l)

x_temp, y_temp = -1,-1
c_temp=""
def xy_mouse(event, x, y, flags, param):
    """TODO: Docstring for xy_mouse.

    :event: TODO
    :x: TODO
    :y: TODO
    :flags: TODO
    :param: TODO
    :returns: TODO

    """
    
    global crop, aratio_copy, x_temp, y_temp,c_temp
    if event == cv2.EVENT_LBUTTONDOWN: #EVENT_LBUTTONDBLCLK:
        print_list = [crop[0], x, crop[1], y, crop[2], crop[2]]
        print("Changes: "+change_string(*print_list))
        crop[0], crop[1] = x, y
        x_temp, y_temp = x, y
        c_temp = "xy"
    elif (event == cv2.EVENT_LBUTTONUP):
        h = y-crop[1]
        if ((x_temp,y_temp)!=(x,y)) and h>0 and crop[2]!=h:
            print_list = [crop[0], crop[0], crop[1], crop[1], crop[2], h]
            print("Changes: "+change_string(*print_list))
            crop[2] = h 
            c_temp += "h"

        boundary_check(c_temp)
        c_temp = ""


def get_cropped_frames(file_in, file_out,aratio, freq=1, window_height=None, fill_color=[255,255,255]):
    """TODO: Docstring for main.

    :file_in: TODO
    :returns: TODO

    """
    global crop, w_height, w_width, aratio_copy
    aratio_copy = aratio

    cap = cv2.VideoCapture(file_in)

    if (cap.isOpened()==False):
        raise("Unable to read the given video")

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    nf = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)+0.5)

    Ffreq = int(fps/freq)

    vratio = width/height

    window_scaling_needed=False
    wratio = 1
    wratio_inv = 1
    if window_height is not None and window_height!=height:
        window_scaling_needed=True
        wratio = height/window_height
        wratio_inv = 1/wratio
        w_width = int(window_height*vratio+0.5)
    else:
        window_height =height
        w_width =  width
    w_height = window_height


    w_out, h_out = aspect_ratio(aratio,width,height)

    
    data_out = []

    crop = np.array([0,0,int(h_out*wratio_inv+0.5)])
    fcount = 0
    crop_filter = np.full((w_height, w_width,3), fill_color, dtype=np.uint8) 

    print("Click left mouse button and drag inorder to select area\n or press  x,y or h to change xy-coordinates of top left coorner and height of the crop")
    print("Press \"d\" to save the crop and move to next one.")

    while (True):
        ret, frame = cap.read()
        if ret==True and window_scaling_needed:
            frame= cv2.resize(frame, (w_width, w_height), interpolation=cv2.INTER_CUBIC)
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
                    print_list = [crop[0], x, crop[1], crop[1], crop[2], crop[2]]
                    print("Changes: "+change_string(*print_list))
                    crop[0]= x 
                    boundary_check("x")

                elif key == ord("y"):
                    y = int(input("Give new y coord: "))
                    print_list = [crop[0], crop[0], crop[1], y, crop[2], crop[2]]
                    print("Changes: "+change_string(*print_list))
                    crop[1] = y
                    boundary_check("y")

                elif key == ord("h"):
                    h = int(input("Give new height: "))
                    print_list = [crop[0], crop[0], crop[1], crop[1], crop[2], h]
                    print("Changes: "+change_string(*print_list))
                    crop[2] = h
                    boundary_check("h")

                elif key == ord("d"):
                    if (0<= crop[0]) and (0<=crop[1]) and (crop[0]+int(aratio*crop[2])<width) and (crop[1]+crop[2]<height):
                        cv2.destroyWindow(msg)
                        crop_scaled= crop.copy()*wratio
                        data_out.append([fcount]+list(crop_scaled) )
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

    file_in, file_out, aratio, freq, window_height= argv[1:]

    a = aratio.split(":")
    aratio = int(a[0])/int(a[1])

    window_height = int(window_height)

    freq = float(freq)
    get_cropped_frames(file_in, file_out, aratio, freq, window_height)
