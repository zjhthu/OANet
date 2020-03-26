import h5py
import numpy as np
import argparse
import os
import glob
from learnedmatcher import LearnedMatcher

def str2bool(v):
    return v.lower() in ("true", "1")
# Parse command line arguments.
parser = argparse.ArgumentParser(description='match for imw2020')
parser.add_argument('--feat_path', type=str, default='/home/jhzhang/IMW2020/dump/imw2020_val_aslfeat_2k',
  help='dumped local feature path.')
parser.add_argument('--model_path', type=str, default='/home/jhzhang/IMW2020/pretrained/oanet-asl/model_best.pth',
  help='pretrained model path')
parser.add_argument('--inlier_th', type=float, default=0,
  help='inlier threshold of network output')
parser.add_argument('--net_mc', type=str2bool, default=True,
  help='perform mutual check using network')
parser.add_argument('--use_ratio', type=int, default=2,
  help='use ratio test in network')
parser.add_argument('--use_mutual', type=float, default=2,
  help='use mutual check in network')
parser.add_argument('--post_process', type=int, default=1,
  help='post process method. 0: None; 1: MAGSAC')
parser.add_argument('--ransac_th', type=float, default=1.25,
  help='inlier threshold (px) in RANSAC variants')
parser.add_argument('--ransac_iter', type=int, default=25000,
  help='inlier threshold (px) in RANSAC variants')


if __name__ == "__main__":
    args = parser.parse_args()
    if args.post_process == 1:
        import pymagsac
    datasets = os.listdir(args.feat_path)
    matcher = LearnedMatcher(args.model_path, args.inlier_th, use_ratio=args.use_ratio, use_mutual=args.use_mutual)
    for dataset in datasets:
        print('---'+str(dataset)+'---')
        feat_path = os.path.join(args.feat_path, dataset)
        desc_file = os.path.join(feat_path, 'descriptors.h5')
        kp_file = os.path.join(feat_path, 'keypoints.h5')
        matches_file = os.path.join(feat_path, 'matches.h5')
        img_list = []
        with h5py.File(kp_file,'r') as kp_f:
            for k, v in kp_f.items():
                img_list.append(k)
        img_list.sort(reverse = True) # large first
        img_num = len(img_list)
        pairs = []
        for idx_i in range(img_num):
            for idx_j in range(idx_i+1, img_num):
                pairs.append((img_list[idx_i],img_list[idx_j]))
        matches_dict = {}
        with h5py.File(desc_file, 'r') as desc_f, h5py.File(kp_file, 'r') as kp_f:
            for img1,img2 in pairs:
                print('-'.join([img1,img2]))
                desc1, desc2 = np.asarray(desc_f[img1]), np.asarray(desc_f[img2])
                kpt1, kpt2 = np.asarray(kp_f[img1]), np.asarray(kp_f[img2])
                matches, pts1, pts2 = matcher.infer([kpt1, kpt2], [desc1, desc2])
                if args.net_mc:
                    matches2, _, _, = matcher.infer([kpt2, kpt1], [desc2, desc1])
                    _, intersect_idx, _ = np.intersect1d(matches[:,0], matches2[:,0],return_indices=True)
                    matches = matches[intersect_idx, :]
                    pts1, pts2 = pts1[intersect_idx,:], pts2[intersect_idx,:]
                if args.post_process == 1:
                    F, mask = pymagsac.findFundamentalMatrix(pts1, pts2, args.ransac_th, max_iters = args.ransac_iter)
                    matches = matches[mask,:]
                matches_dict['-'.join([img1,img2])] = matches.T
        with h5py.File(matches_file, 'w') as matches_f:
            for k in matches_dict:
                matches_f.create_dataset(k, data=matches_dict[k])

                


        

