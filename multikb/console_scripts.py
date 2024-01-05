import multikb
from sys import argv


def get_cropped_frames_script():
    """TODO: Docstring for get_cropped_frames_script.
    :returns: TODO

    """
    file_in, file_out, aratio, freq, window_height = argv[1:]

    a = aratio.split(":")
    aratio = int(a[0])/int(a[1])
    freq = float(freq)
    window_height = int(window_height)
    multikb.get_cropped_frames(file_in, file_out, aratio, freq, window_height)

def connect_cropped_frames_script():

    file_in, file_out, smoothness = argv[1:]

    multikb.connect_cropped_frames(file_in, file_out, int(smoothness))

def video_from_connected_cropped_frames_script():
    """TODO: Docstring for video_from_connected_cropped_frames_script.
    :returns: TODO

    """
    video_in, video_out, data_file, aratio = argv[1:]
    a = aratio.split(":")
    aratio = int(a[0])/int(a[1])

    multikb.video_from_connected_cropped_frames(video_in,video_out, data_file, aratio)

def main_script():
    """TODO: Docstring for main_script.
    :returns: TODO

    """
    
    if len(argv[1:])==7:
        file_in, directory, file_out, aratio, smoothness, freq, window_height = argv[1:]
    elif len(argv[1:])==6:
        file_in, directory, file_out, aratio, smoothness, freq = argv[1:]
        window_height = None
    multikb.run(file_in, directory, file_out, aratio, smoothness, freq, window_height)    




