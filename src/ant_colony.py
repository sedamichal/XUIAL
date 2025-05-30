import numpy as np


class AntSegmentationProcess:
    '''
        A class to handle the segmentation process using Ant Colony Optimization.
        alpha: float  # Pheromone importance
        beta: float  # Visibility importance
        evaporation_rate: float  # Rate at which pheromone evaporates
        n_ants: int  # Number of ants
        n_iterations: int  # Number of iterations to run the algorithm
        steps: int  # Number of steps each ant takes
    '''

    def __init__(self, image, n_ants=100, n_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.95, steps=100, device="cpu"):
        self._image = image.copy().astype(np.float32)
        self._n_ants = n_ants
        self._n_iterations = n_iterations
        self._alpha = alpha
        self._beta = beta
        self._evaporation_rate = evaporation_rate
        self._steps = steps
        self._pheromone = None
        self._visibility = None
        self._device = device
        self._epsilon = 1e-8  # Small value to avoid division by zero

    def run(self):
        self._init_before_run()
        
        for _ in range(self._n_iterations):
            self._iterate()
        return self._pheromone

    def _init_before_run(self):
        self._pheromone = np.ones_like(self._image, dtype=np.float32)  # Initialize pheromone levels
        self._visibility = self._image / self._image.max()  # Initialize visibility (inverse of distance)
        self._visibility = 1.0 / (self._visibility + self._epsilon)  # Avoid division by zero

    def _iterate(self):
        delta_pheromone = np.zeros_like(self._pheromone)
        for ant in range(self._n_ants):
            y, x = np.random.randint(0, self._image.shape[0]), np.random.randint(0, self._image.shape[1])            
            for step in range(self._steps):
                neighbors = [(y+i, x+j) for i in [-1, 0, 1] for j in [-1, 0, 1] if 0 <= y+i < self._image.shape[0] and 0 <= x+j < self._image.shape[1]]
                print(neighbors)
                probs = self._get_probabilities(neighbors)
                print(probs)    
                try:
                    index = np.random.choice(len(neighbors), p=probs)
                    print(index)
                except Exception as e:
                    print(f"Error: {e}")
                    continue
                y, x = neighbors[index]
                delta_pheromone[y, x] += 1
                # print(f"Ant {ant+1}/{self._n_ants}, Step {step+1}/{self._steps}, Position: ({y}, {x}) delta pheromone: {delta_pheromone[y, x]}")
                
            self._pheromone = self._pheromone * self._evaporation_rate + delta_pheromone # type: ignore
            self._pheromone = self._pheromone / self._pheromone.max()
            
    def _get_probabilities(self, neighbors):
        probs = np.array([
            ((self._pheromone[ny, nx] + self._epsilon) ** self._alpha) * ((self._visibility[ny, nx] + self._epsilon) ** self._beta) # type: ignore
            for ny, nx in neighbors
        ])
        if np.sum(probs) == 0:
            probs = np.ones_like(probs) / len(probs)
        else:
            probs /= np.sum(probs)
        return probs
