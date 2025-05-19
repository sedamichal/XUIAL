import cv2
import numpy as np
import matplotlib.pyplot as plt

class GaborFilterProcess:
    def __init__(self, ksize=16, sigma=4.0, lambd=10.0, gamma=0.5, psi=0, thetas=None):
        self._create_kernels(ksize=ksize, sigma=sigma, lambd=lambd, gamma=gamma, psi=psi, thetas=thetas)

    def _create_kernels(
        self, ksize=16, sigma=4.0, lambd=10.0, gamma=0.5, psi=0, thetas=None
    ):
        self._kernels = []

        if thetas == None:
            thetas = np.arange(0, np.pi, np.pi / 8)
            
        for theta in thetas:
            kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
            self._kernels.append(kernel)

    def __call__(self, img_or_path):
        if isinstance(img_or_path, str):
            img = cv2.imread(img_or_path, cv2.IMREAD_GRAYSCALE)
        else:
            img = cv2.cvtColor(img_or_path, cv2.COLOR_BGR2GRAY) if img_or_path.ndim == 3 else img_or_path

        filtered_imgs = []
        for kernel in self._kernels:
            filtered = cv2.filter2D(img, cv2.CV_8UC3, kernel)
            filtered_imgs.append(filtered)

        gabor_max = np.max(np.array(filtered_imgs), axis=0).astype(np.uint8)

        print(gabor_max.shape, gabor_max.dtype)

        _, binary_edge = cv2.threshold(gabor_max, 50, 255, cv2.THRESH_BINARY)

        # odstraneni sumu
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        binary_edge = cv2.morphologyEx(binary_edge, cv2.MORPH_CLOSE, kernel)
        binary_edge = cv2.morphologyEx(binary_edge, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(binary_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        for cnt in contours:
            if cv2.contourArea(cnt) > 100:  # filtruj malé objekty
                try:
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int32(box)
                    cv2.drawContours(output, [box], 0, (0, 255, 0), 2)
                except Exception as e:
                    print(box.shape, box.dtype)
                    print(e)
                    pass

        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.title("Původní obrázek")
        plt.imshow(img, cmap='gray')
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.title("Gabor filtry (max po orientacích)")
        plt.imshow(gabor_max, cmap='gray')
        plt.axis('off')

        plt.subplot(1, 3, 3)
        plt.title("Detekované orientované boxy")
        plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.show()
