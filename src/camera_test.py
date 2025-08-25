from pso_processors import PSOKapurEntropyProcessor, PSOBlockClusteringProcessor
from camera_capture import CameraCapture

cap = CameraCapture(
    processors=[
        PSOKapurEntropyProcessor(pop=10, iters=20),
        # PSOKapurEntropyProcessor(pop=5, iters=20),
        # PSOKapurEntropyProcessor(pop=5, iters=30),
        # PSOBlockClusteringProcessor(pop=10, iters=5),
    ],
    device_idx=0,
)

cap()
