import os
from glob import glob
import shutil
from tqdm import tqdm
import dicom2nifti
import numpy as np
import nibabel as nib
from monai.transforms import(
    Compose,
    AddChanneld,
    LoadImaged,
    Resized,
    ToTensord,
    Spacingd,
    Orientationd,
    ScaleIntensityRanged,
    CropForegroundd,
)
from monai.data import DataLoader, Dataset, CacheDataset
from monai.utils import set_determinism

def prepare(in_dir, pixdim=(1.5, 1.5, 1.0), a_min=-200, a_max=200, spatial_size=[128,128,64], cache=False):
    """

    :param in_dir:
    :param pixdim:
    :param a_min:
    :param a_max:
    :param spatial_size:
    :param cache:
    :return:
    """

    set_determinism(seed=0)

    path_train_volumes = sorted(glob(os.path.join(in_dir, "TrainVolumes", "*.nii.gz")))
    path_train_segmentation = sorted(glob(os.path.join(in_dir, "TrainSegmentation", "*.nii.gz")))

    path_test_volumes = sorted(glob(os.path.join(in_dir, "TestVolumes", "*.nii.gz")))
    path_test_segmentation = sorted(glob(os.path.join(in_dir, "TestSegmentation", "*.nii.gz")))

    train_files = [{"vol": vol_path, "seg": seg_path} for vol_path, seg_path in zip(path_train_volumes, path_train_segmentation)]
    test_files = [{"vol": vol_path, "seg": seg_path} for vol_path, seg_path in zip(path_test_volumes, path_test_segmentation)]

    train_transforms = Compose(
        LoadImaged(keys=["vol", "seg"]),

    )