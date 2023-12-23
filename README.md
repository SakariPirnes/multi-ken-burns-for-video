# Multiple Ken Burns Efects for Video Input 

## Example

### Input video in.mp4:

[The following input video is in the example folder](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/example/in.mp4)

https://github.com/SakariPirnes/multi-ken-burns-for-video/assets/64021387/289dd355-bc3e-422f-8c56-a956a87144cf

### Output video out.mp4:

[The following output video is in the example folder](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/example/out.mp4)

https://github.com/SakariPirnes/multi-ken-burns-for-video/assets/64021387/6d89d365-42ea-4c5f-a688-8271a7c1b6a0

### Command to obtain out.mp4 from in.mp4 

    python3 multikb example/in.mp4 example/ out.mp4 4:5 20 3

**Explanation of the arguments for Python:**
1. `multikb`: the program
2. `example/in.mp4`: path to input file
3. `example/`: path to directory for output (use `./` for current directory)
4. `out.mp4`: name of the output file 
5. `4:5`: aspect ratio of the output Video
6. `20`: smootheness of the trajectory, greater number means more smootheness and 
`0` is no smoothing
7. `3`: how many times one has to manually crop a frame in one second

### Running the program
The program has three steps:
1. As shown in the below video, after the above command has been executed frames has to be cropped. In our case we crop 3 frames for every second plus the final frame. The cropping can be done by mouse as shown in the video, or 
by giving exact coordinates, instractions will be printed in the console. This is done by [multikb/get_cropped_frames.py](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/multikb/get_cropped_frames.py) which generates coordinate file [example/cropped_frames.npy](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/example/cropped_frames.npy). This step is equivalent of running reparately:
    python3 multikb/get_cropped_frames.py example/in.mp4 example/cropped_frames.npy 4:5 3
2. After this the coordinate file [example/connected_cropped_frames.npy](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/example/connected_cropped_frames.npy) is generated from [example/cropped_frames.npy](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/example/cropped_frames.npy) by running [multikb/connect_cropped_frames.py](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/multikb/connect_cropped_frames.py). This is done by connecting the cropped frames linearly and then smoothing by taking a convolution with a bumb function which in our case has a support of lenght 20. This step is equivalent of running separately:
    python3 multikb/connect_cropped_frames.py example/cropped_frames.npy example/connected_cropped_frames.npy 20
3. Finaly the program runs [multikb/make_video_from_connected_cropped_frames.py](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/multikb/make_video_from_connected_cropped_frames.py) in order to make the final file. This step is equivalent of running separately:
    python3 multikb/make_video_from_connected_cropped_frames.py example/in.mp4 example/out.mp4 example/connected_cropped_frames.npy 4:5 

In order to avoid the manual labor of cropping the frames (step 1), one can use the obtained coordinate files to run https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/multikb/make_video_from_connected_cropped_frames.py and 
[multikb](https://github.com/SakariPirnes/multi-ken-burns-for-video/blob/main/multikb/make_video_from_connected_cropped_frames.py) again with different parameters.

**Note the below video is sped up. Duration of the original video is 1min 42s which is roughly the time used for manually cropping the frames**

https://github.com/SakariPirnes/multi-ken-burns-for-video/assets/64021387/bd1a3b19-bf11-4cae-9131-ce527a3d5b74


