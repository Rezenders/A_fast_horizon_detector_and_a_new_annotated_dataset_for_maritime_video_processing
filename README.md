Install the requirements: numpy, opencv-python, opencv-contrib-python
Convert the input video to .avi format
-------
Run the main.py script:
  * Imports the algorithm's API using "from FastHorizonAlg import FastHorizon"
  * Instantiates a class instance
  * Invoke the horiozn detection method on the .avi video

## Docker

Build:

```Bash
docker build -t fast_detector -f docker/Dockerfile .
```

Run:
```Bash
docker run -it --rm --name vsnt_opencv  -e DISPLAY=$DISPLAY  -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v ${HOME}/Documents/git/A_fast_horizon_detector_and_a_new_annotated_dataset_for_maritime_video_processing:/fast_detector -v ${HOME}/Documents/datasets/TMD:/datasets/TMD fast_detector
```

```Bash
docker run -it --rm --name vsnt_opencv  -e DISPLAY=$DISPLAY  -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v ${HOME}/git/A_fast_horizon_detector_and_a_new_annotated_dataset_for_maritime_video_processing:/fast_detector -v ${HOME}/Documents/datasets/TMD:/datasets/TMD fast_detector
```