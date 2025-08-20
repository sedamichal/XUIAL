from pso_processors import PSOKapurEntropyProcessor, PSOBlockClusteringProcessor
from camera_capture import CameraCapture

cap = CameraCapture(
    # processors=[PSOBlockClusteringProcessor(), PSOKapurEntropyProcessor()]
    # processors=[
    #     PSOBlockClusteringProcessor(w=0.5, c1=1.5, c2=1.5, block_size=8),
    #     PSOBlockClusteringProcessor(block_size=8)
    # ]
    # processors=[PSOKapurEntropyProcessor()]
    processors=[PSOBlockClusteringProcessor(block_size=4)]
)

cap()
