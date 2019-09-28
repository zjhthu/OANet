First, download raw image data.
```bash
wget xxx
tar -xvf xxx 
```

You need generate local features for these images. We provide an example for SIFT.
```bash
cd gen_data
python extract_feature.py
```

Then generate files for training and testing.
```bash
python yfcc.py
```