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

