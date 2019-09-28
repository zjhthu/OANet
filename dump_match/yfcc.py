import os
import numpy as np
import multiprocessing as mp
import argparse
import h5py
import pickle
from datasets import Dataset

def str2bool(v):
    return v.lower() in ("true", "1")
# Parse command line arguments.
parser = argparse.ArgumentParser(description='extract sift.')
parser.add_argument('--raw_data_path', type=str, default='../raw_data/',
  help='Image directory or movie file or "camera" (for webcam).')
parser.add_argument('--dump_dir', type=str, default='../data_dump/',
  help='Image directory or movie file or "camera" (for webcam).')
parser.add_argument('--desc_name', type=str, default='sift-2000',
  help='prefix of filename, default:sift-2000')
parser.add_argument('--vis_th', type=int, default=50,
  help='visibility threshold')
parser.add_argument('--pair_num', type=int, default=1000,
  help='pair num. 1000 for test seq')

class YFCC(object):
    def __init__(self, dataset_path, dump_dir, seqs, mode, desc_name, vis_th, pair_num, pair_path=None):
        self.dataset_path = dataset_path
        self.dump_dir = dump_dir
        self.seqs = seqs
        self.mode = mode
        self.desc_name = desc_name
        self.vis_th = vis_th
        self.pair_num = pair_num
        self.pair_path = pair_path
        self.dump_data()

    def collect(self):
        data_type = ['xs','ys','Rs','ts', 'ratios', 'mutuals',\
            'cx1s', 'cy1s', 'cx2s', 'cy2s', 'f1s', 'f2s']
        pair_idx = 0
        dump_file = self.dump_dir+'/yfcc-'+self.desc_name+'-'+self.mode+'.hdf5'
        with h5py.File(dump_file, 'w') as f:
            data = {}
            for tp in data_type:
                data[tp] = f.create_group(tp)
            for seq in self.seqs:
                print(seq)
                data_seq = {}
                for tp in data_type:
                    data_seq[tp] = pickle.load(open(self.dump_dir+'/'+seq+'/'+self.desc_name+'/'+self.mode+'/'+str(tp)+'.pkl','rb'))
                seq_len = len(data_seq['xs'])

                for i in range(seq_len):
                    for tp in data_type:
                        data_item = data_seq[tp][i]
                        if tp in ['cx1s', 'cy1s', 'cx2s', 'cy2s', 'f1s', 'f2s']:
                            data_item = np.asarray([data_item])
                        data_i =  data[tp].create_dataset(str(pair_idx), data_item.shape, dtype=np.float32)
                        data_i[:] = data_item.astype(np.float32)
                    pair_idx = pair_idx + 1

    def dump_data(self):
        # make sure you have already saved the features
        for seq in self.seqs:
            pair_name = None if self.pair_path is None else self.pair_path+'/'+seq+'-te-1000-pairs.pkl'
            dataset_path = self.dataset_path+'/'+seq+'/'+self.mode
            dump_dir = self.dump_dir+'/'+seq+'/'+self.desc_name+'/'+self.mode
            dataset = Dataset(dataset_path, dump_dir, self.desc_name, self.vis_th, self.pair_num, pair_name)
            print('dump intermediate files.')
            dataset.dump_intermediate()
            print('dump matches.')
            dataset.dump_datasets()
        print('collect pkl.')
        self.collect()
        
if __name__ == "__main__":
    config = parser.parse_args()
    # dump yfcc test
    test_seqs = ['buckingham_palace','notre_dame_front_facade','reichstag', 'sacre_coeur']
    yfcc_te = YFCC(config.raw_data_path+'yfcc100m/', config.dump_dir, test_seqs, 'test', config.desc_name, \
        config.vis_th, config.pair_num, config.raw_data_path+'pairs/')
    #'''
    # dump yfcc training seqs
    with open('yfcc_train.txt','r') as ofp:
        train_seqs = ofp.read().split('\n')
    if len(train_seqs[-1]) == 0:
        del train_seqs[-1]
    print('train seq len '+str(len(train_seqs)))
    #yfcc_tr_va = YFCC(config.raw_data_path+'yfcc100m/', config.dump_dir, train_seqs, 'val', config.desc_name, \
    #    config.vis_th, 100, None)
    yfcc_tr_tr = YFCC(config.raw_data_path+'yfcc100m/', config.dump_dir, train_seqs, 'train', config.desc_name, \
        config.vis_th, 10000, None)
    #'''