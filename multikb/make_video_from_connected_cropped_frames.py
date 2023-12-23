import numpy as np
import cv2 
from get_cropped_frames import aspect_ratio
import ffmpeg

__all__ = ["main"]

def main(video_in, video_out, data_file, aratio):
    """TODO: Docstring for main.

    :video_in: TODO
    :video_out: TODO
    :data_file: TODO
    :returns: TODO

    """
    data = np.load(data_file)
    
    cap = cv2.VideoCapture(video_in)
    if (cap.isOpened()==False):
        raise("Unable to read the given video")

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    nf = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)+0.5)

    w_out, h_out = aspect_ratio(aratio,width,height)
    
    s = video_out.split(".")
    video_out_soundless = video_out[:-len(s[-1])-1]+"_no-sound."+s[-1]
    output = cv2.VideoWriter(video_out_soundless, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w_out,h_out))
    fcount = 0
    while (True):

        ret, frame = cap.read()

        if ret==True and fcount<data.shape[0]:
            x, y, h = data[fcount]
            
            # left and right x coordinates
            lx = int( x )
            rx = int( x+h*aratio + 0.5)

            # up and bottom y coordinates
            yu = int( y )
            yb = int( y+h +0.5)

            frame_out = frame[yu:yb, lx:rx]

            frame_out_scale = cv2.resize(frame_out, (w_out, h_out))

            output.write(frame_out_scale)
        else:
            break 
        fcount+=1
    
    cap.release()
    output.release()

    cv2.destroyAllWindows()

    # add sound
    video = ffmpeg.input(video_out_soundless)
    audio = ffmpeg.input(video_in)

    ffmpeg.concat(video, audio, v=1, a=1).output(video_out).run()




if __name__ =="__main__":
    from sys import argv

    video_in, video_out, data_file, aratio = argv[1:]
    a = aratio.split(":")
    aratio = int(a[0])/int(a[1])

    main(video_in,video_out, data_file, aratio)
