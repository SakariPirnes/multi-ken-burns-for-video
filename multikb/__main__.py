import get_cropped_frames
import connect_cropped_frames
import make_video_from_connected_cropped_frames

__all__ = ["main"]

def main(file_in, directory, file_out, aratio, smoothness, freq):
    """TODO: Docstring for main.
    :returns: TODO

    """
    file_c = directory+"/cropped_frames.npy"
    a = aratio.split(":")
    aratio = int(a[0])/int(a[1])
    freq = float(freq)

    print("Collecting manually cropped frames...")
    get_cropped_frames.main(file_in, file_c, aratio, freq)

    print("Cropped frames collected!")
    print("Connecting cropped frames...")


    file_cc = directory+"/connected_cropped_frames.npy"
    connect_cropped_frames.main(file_c, file_cc, int(smoothness))

    print("Cropped frames connected!")
    print("Writing output video...")

    make_video_from_connected_cropped_frames.main(file_in, directory+"/"+file_out,
            file_cc, aratio)

    print("DONE!")

if __name__ == "__main__":
    from sys import argv

    file_in, directory, file_out, aratio, smoothness, freq = argv[1:]
    main(file_in, directory, file_out, aratio, smoothness, freq)    
