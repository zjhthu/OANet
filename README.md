# OANet implementation

Pytorch implementation of OANet for ICCV'19 paper ["Learning Two-View Correspondences and Geometry Using Order-Aware Network"](https://arxiv.org/abs/1908.04964), by Jiahui Zhang, Dawei Sun, Zixin Luo, Anbang Yao, Lei Zhou, Tianwei Shen, Yurong Chen, Long Quan and Hongen Liao.

This paper focuses on establishing correspondences between two images. We introduce the DiffPool and DiffUnpool layers to capture the local context of unordered sparse correspondences in a learnable manner. By the collaborative use of DiffPool operator, we propose Order-Aware Filtering block which exploits the complex global context.

This repo contains the code and data for essential matrix estimation described in our ICCV paper. Besides, we also provide code for fundamental matrix estimation and the usage of side information (ratio test and mutual nearest neighbor check). Documents about this part will also be released soon.

If you find this project useful, please cite:

```
@article{zhang2019oanet,
  title={Learning Two-View Correspondences and Geometry Using Order-Aware Network},
  author={Zhang, Jiahui and Sun, Dawei and Luo, Zixin and Yao, Anbang and Zhou, Lei and Shen, Tianwei and Chen, Yurong and Quan, Long and Liao, Hongen},
  journal={International Conference on Computer Vision (ICCV)},
  year={2019}
}
```

## Requirements

Please use Python 3.6, opencv-contrib-python (3.4.0.12) and Pytorch (>= 1.1.0). Other dependencies should be easily installed through pip or conda.


## Example scripts

### Run the demo

For a quick start, clone the repo and download the pretrained model,
```bash
git clone https://github.com/zjhthu/OANet.git 
cd OANet 
wget https://research.altizure.com/data/oanet_data/model.tar.gz 
tar -xvf model.tar.gz
```

then run the fundamental matrix estimation demo:

```bash
cd ./demo && python demo.py
```

### Test pretrained model

We provide the model trained on YFCC100M described in our ICCV paper. Run the test script to get results in our paper.

Download prepared training and testing data. This might take a while. 
```bash
bash download_data.sh
tar -xvf data_dump.tar.gz
rm -r download_data_oanet_data
cd ./core 
python main.py --run_mode=test --model_path=../model/essential/sift-2000 --res_path=../model/essential/sift-2000/ --use_ransac=False
```
Set `--use_ransac=True` to get results after RANSAC post-processing.

### Train model on YFCC100M

Download prepared data described above. Then run tranining script.
```bash
cd ./core 
python main.py
```

You can train the fundamental estimation model by setting `--use_fundamental=True --geo_loss_margin=0.03` and use side information by setting `--use_ratio=2 --use_mutual=2`

### [TODO] Train with your own local feature or data 

The provided model are trained using SIFT. You had better retrain the model if you want to use with 
your own local feature, such as ContextDesc, SuperPoint and etc. We will release the data generation scripts soon. 

## News

1. Together with the local feature [ContextDesc](https://github.com/lzx551402/contextdesc), we won both the stereo and muti-view tracks at the [CVPR19 Image Matching Challenge](https://image-matching-workshop.github.io/leaderboard/) (June. 2, 2019).

2. We also rank the third place on the [Visual Localization Benchmark](https://www.visuallocalization.net/workshop/cvpr/2019/) using ContextDesc (Aug. 30, 2019).

## Acknowledgement
This code is heavily borrowed from [Learned-Correspondence](https://github.com/vcg-uvic/learned-correspondence-release).


## Changelog

