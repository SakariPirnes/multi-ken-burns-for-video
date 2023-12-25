import multikb
from sys import argv


def get_cropped_frames_script():
    """TODO: Docstring for get_cropped_frames_script.
    :returns: TODO

    """
    file_in, file_out, aratio, freq = argv[1:]

    a = aratio.split(":")
    aratio = int(a[0])/int(a[1])
    freq = float(freq)
    multikb.get_cropped_frames(file_in, file_out, aratio, freq)

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
    
    file_in, directory, file_out, aratio, smoothness, freq = argv[1:]
    multikb.run(file_in, directory, file_out, aratio, smoothness, freq)    




