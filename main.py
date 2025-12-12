from FastHorizonAlg import FastHorizon


def main():
    fast_horizon_algorithm = FastHorizon()  # instantiate the algorithm
    # demo on a video sample
    # fast_horizon_algorithm.video_demo(video_path='./video sample/MMD_annotated_5.avi', display=True)
    fast_horizon_algorithm.evaluate(
        src_video_folder='/datasets/TMD/VideoFilesTMD/',
        src_gt_folder='/datasets/TMD/GroundTruthFilesTMD/GT_Horizon/npy (For Python)/',
        dst_video_folder='/datasets/TMD/results/videos/',
        dst_quantitative_results_folder='/datasets/TMD/results/',
        draw_and_save=True)


if __name__ == '__main__':
    main()
