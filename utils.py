import cv2
import matplotlib.pyplot as plt

def show_images(images):
    unit = 10
    
    _, axs = plt.subplots(1, len(images), figsize=(len(images) * unit, unit))
    for i in range(len(images)):
        axs[i].axis('off')
        axs[i].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
    plt.show()