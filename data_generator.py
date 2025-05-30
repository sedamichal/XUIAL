import torchvision.transforms as T
import cv2
from torch.utils.data import Dataset
import numpy as np


class ThermalHotspotDataset(Dataset):
    def __init__(self, samples_size=1000, image_size=(640, 480)):
        self._samples_size = samples_size
        self._image_size = image_size
        self._transform = T.ToTensor()

    def __len__(self):
        return self._samples_size

    def __getitem__(self, idx):
        image = np.random.normal(
            loc=30,
            scale=2,
            size=self._image_size
            ).denorm().astype(np.uint8)

        # náhodný hotspot
        min, max = round(self._image_size[0] * 0.2), round(self._image_size[0] * 0.6)
        x, y = np.random.randint(min, max), np.random.randint(min, max)
        radius = np.random.randint(5, 20)
        color = int(60 + 10 * np.random.rand())

        cv_image = image.copy()
        cv_image = cv2.circle(
            img=cv_image,
            center=(x, y),
            radius=radius,
            color=color,
            thickness=-1,
            lineType=cv2.LINE_8,
            shift=0
        )
        # cv_image = cv2.circle(cv_image, (x, y), radius, 60 + np.random.rand()*10, -1)
        mask = (cv_image > 50).astype(np.float32)
        return self._transform(cv_image)[0:1, :, :], self._transform(mask)[0:1, :, :]