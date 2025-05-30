import numpy as np
import time
from datetime import timedelta


class CellularAutomataSegmentation:
    '''
        A class to handle the segmentation process using Cellular automata.
        activation_neigbours_cnt: int  # Number of active neighbors required to activate a cell
        activation_cell_value_treshold: float  # Threshold for the cell's value to be considered active
        threshold: float  # Threshold for initial segmentation
        iterations: int  # Number of iterations to run the algorithm
    '''

    def __init__(self, image, activation_neigbours_cnt=3, activation_cell_value_treshold=0.4,threshold=0.8, iterations=100, debug=False):
        self._debug = debug
        self._epsilon = 1e-8  # Small value to avoid division by zero
        self._iterations = iterations
        self._threshold = threshold
        self._activation_neigbours_cnt = activation_neigbours_cnt
        self._activation_cell_value_treshold = activation_cell_value_treshold

        self._image = np.array(image, dtype=np.float32)
        self._image = self._image / (self._image.max() + self._epsilon)
        self._state = (self._image > self._threshold).astype(np.uint8)  # Initial state based on threshold

    def run(self):
        if self._debug:
            start_time = time.time()
            
        for i in range(self._iterations):            
            self._iteration(i)
        
        if self._debug:
            duration = time.time() - start_time  # type: ignore          
            print(f"Duration {timedelta(seconds=int(duration))}:")
        return self._state

    def _iteration(self, iteration):
        if self._debug:
            start_time = time.time()
            
        new_state = self._state.copy()
        for y in range(1, self._image.shape[0] - 1):
            for x in range(1, self._image.shape[1] - 1):
                if self._state[y, x] == 1:
                    continue # Skip already activated cells
                neighbors = self._state[y-1:y+2, x-1:x+2]
                active_neighbors = np.sum(neighbors) - self._state[y, x]  # Count active neighbors
                if self._is_active(active_neighbors, self._image[y, x]):
                    new_state[y, x] = 1
        self._state = new_state
        
        if self._debug:
            duration = time.time() - start_time  # type: ignore
            print(f"Iteration {iteration} {timedelta(seconds=int(duration))}:")

    def _is_active(self, active_neighbors_count, cell_value):
        return active_neighbors_count >= self._activation_neigbours_cnt and cell_value > self._activation_cell_value_treshold
