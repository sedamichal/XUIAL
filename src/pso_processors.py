import numpy as np
import cv2

class PSO:
    def __init__(self, data, dim, pop=30, iters=50, w=0.72, c1=1.49, c2=1.49):
        # Parameters:

        # image: obrazek

        # pop: population size - Počet částic ve swarmu.
        # Větší hodnota = širší průzkum prostoru, ale pomalejší běh.
        # Typicky 20–50.

        # iters: iterations - Počet iterací PSO algoritmu.
        # Každá iterace aktualizuje pozice částic podle rychlostí.

        # w: inertia weight - Váha setrvačnosti – určuje, jak moc částice pokračuje ve své předchozí trajektorii.
        # Větší w → více průzkumu, menší w → více exploatace (focení na dobrá místa).
        # Typicky 0.4 nebo 0.9.

        # c1: cognitive coefficient - „Učící se“ složka – váha toho, jak moc částice sleduje své vlastní nejlepší dosažené místo (personal best).
        # Typicky 1–2.

        # c2: social coefficient - „Sociální“ složka – váha toho, jak moc částice sleduje globální nejlepší místo (swarm best).
        # Typicky 1–2.

        self._data = data
        self._pop = pop
        self._iters = iters
        self._w = w
        self._c1 = c1
        self._c2 = c2

        self._dim = dim

        # self._particles = np.random.random((self._pop, self._dim))
        self._init_particles()
        self._velocities = np.zeros((self._pop, self._dim))

        self._best = np.copy(self._particles)
        self._best_score = np.array([self._fitness(p) for p in self._particles])

        self._global_best_idx = np.argmax(self._best_score)
        self._global_best = self._best[self._global_best_idx]
        self._global_best_score = self._best_score[self._global_best_idx]

    def _init_particles(self):
        self._particles = np.random.random((self._pop, self._dim))

    def _fitness(self, params):
        return 0     

    def optimize(self):
        for it in range(self._iters):
            for i in range(self._pop):
                r1, r2 = np.random.rand(self._dim), np.random.rand(self._dim)
                self._velocities[i] = (
                    self._w * self._velocities[i]
                    + self._c1 * r1 * (self._best[i] - self._particles[i])
                    + self._c2 * r2 * (self._global_best - self._particles[i])
                )
                self._particles[i] += self._velocities[i]

                # Vyhodnocení fitness
                score = self._fitness(self._particles[i])
                if score > self._best_score[i]:
                    self._best_score[i] = score
                    self._best[i] = np.copy(self._particles[i])

            # Aktualizace globálního nejlepšího
            best_idx = np.argmax(self._best_score)
            if self._best_score[best_idx] > self._global_best_score:
                self._global_best_score = self._best_score[best_idx]
                self._global_best = np.copy(self._best[best_idx])

        return self._global_best, self._global_best_score

class PSOProcessor():
    def __init__(self, id: str, pop=30, iters=50, w=0.72, c1=1.49, c2=1.49):
        self._id = id
        self._pop = pop
        self._iters = iters
        self._w = w
        self._c1 = c1
        self._c2 = c2

    def get_mask(self, image):
        pass

    @property
    def id(self):
        return self._id


class PSOKapurEntropy(PSO):
    def __init__(self, image, pop=30, iters=50, w=0.72, c1=1.49, c2=1.49):
        super().__init__(
            image, dim=1, pop=pop, iters=iters, w=w, c1=c1, c2=c2
        )

    def _kapur_entropy_th(self, t):
        """
        thresholds: list nebo pole prahů [t1, t2, ...]
        """
        hist, _ = np.histogram(self._data.ravel(), bins=256, range=(0, 256), density=True)
        hist = hist.astype(float) / hist.sum()

        P1 = np.sum(hist[:t])
        P2 = np.sum(hist[t:])

        if P1 ==0 or P2 == 0:
            return -np.inf

        p1 = hist[:t] / P1
        p2 = hist[t:] / P2

        H1 = -np.sum(p1[p1 > 0] * np.log(p1[p1 > 0]))
        H2 = -np.sum(p2[p2 > 0] * np.log(p2[p2 > 0]))

        return H1 + H2

    def _fitness(self, params):
        t = params[0]
        t = int(np.clip(t, 1, 254))
        return self._kapur_entropy_th(t)

class PSOKapurEntropyProcessor(PSOProcessor):
    def __init__(self, pop=30, iters=50, w=0.72, c1=1.49, c2=1.49):
        super().__init__("KapurEntropy", pop, iters, w, c1, c2)

    def get_mask(self, image):
        blurred = cv2.GaussianBlur(image, (5, 5), 2)  # kernel size 5x5, sigma 0 → auto
        pso = PSOKapurEntropy(
            blurred, self._pop, self._iters, self._w, self._c1, self._c2
        )
        t, _ = pso.optimize()
        th = int(round(t[0]))
        _, mask = cv2.threshold(
            image, th, 255, cv2.THRESH_BINARY
        )
        return mask


class PSOBlockClustering(PSO):
    """
    pop=30, iters=50, w=0.5, c1=1.5, c2=1.5
    """
    def __init__(self, data, pop=30, iters=50, w=0.72, c1=1.49, c2=1.49, clusters_cnt=2):
        self._clusters_cnt = clusters_cnt
        super().__init__(
            data, dim=clusters_cnt, pop=pop, iters=iters, w=w, c1=c1, c2=c2
        )

    def _init_particles(self):
        self._particles = np.array(
            [
                np.random.choice(self._data, self._clusters_cnt)
                for _ in range(self._pop)
            ],
            dtype=float,
        )

    def _fitness(self, params):
        score = 0
        for x in self._data:
            score += min((x - c) ** 2 for c in params)
        return -score  # menší chyba → větší fitness


class PSOBlockClusteringProcessor(PSOProcessor):
    def __init__(self,  pop=30, iters=50, w=0.72, c1=1.49, c2=1.49, block_size=16):
        super().__init__("BlockClustering", pop, iters, w, c1, c2)
        self._block_size = block_size

    def get_mask(self, image):
        blurred = cv2.GaussianBlur(image, (5, 5), 2)  # kernel size 5x5, sigma 0 → au
        means, blocks = self._block_means(blurred)

        pso = PSOBlockClustering(
            np.array(means),
            self._pop,
            self._iters,
            self._w,
            self._c1,
            self._c2,
            clusters_cnt=2,
        )
        centroids, _ = pso.optimize()
        hot_cluster = np.argmax(centroids)
        mask_blocks = np.zeros_like(image)
        for mean_val, (i, j, shape) in zip(means, blocks):
            if np.argmin([abs(mean_val - c) for c in centroids]) == hot_cluster:
                mask_blocks[i : i + shape[0], j : j + shape[1]] = 255

        return mask_blocks        

    def _block_means(self, image):
        h, w = image.shape
        means = []
        blocks = []
        for i in range(0, h, self._block_size):
            for j in range(0, w, self._block_size):
                block = image[i : i + self._block_size, j : j + self._block_size]
                mean_val = np.mean(block)
                means.append(mean_val)
                blocks.append((i, j, block.shape))
        return means, blocks
