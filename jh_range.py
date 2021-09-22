import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class JupiterHellGun():
    def __init__(self, minimum_range=0, optimal_range=3, maximum_range=6):
        self.min = 2
        self.optimal = 3
        self.max = 6

    def update(self, *, min_range=None, optimal_range=None, max_range=None):
        self.min = min_range or self.min
        self.optimal = optimal_range or self.optimal
        self.max = max_range or self.max

    def __str__(self):
        if self.min > 0:
            return f'{self.min}/{self.optimal}/{self.max}'
        return f'{self.optimal}/{self.max}'

class JupiterHellRangeVisualizer():
    def __init__(self, area=7, vision_threshold=6.25 ):
        distance_matrix = np.zeros( [area+1,area+1] )
        for x in range(area+1):
            for y in range(area+1):
                distance_matrix[y, x] = ( (x**2) + (y**2) ) ** 0.5
        self._distance_matrix = distance_matrix

        self._distance_matrix_v = distance_matrix.copy()
        self._distance_matrix_v[ self._distance_matrix_v > vision_threshold ] = 0

        self.gun = JupiterHellGun()

    def _to_hit(self, distance):
        if distance < self.gun.min:
            return distance / self.gun.min
        elif distance <= self.gun.optimal:
            return 1.0
        else: 
            hit_chance = 0.0
            try:
                hit_chance = 1.0 - ( ( distance - self.gun.optimal ) / ( 1 + self.gun.max - self.gun.optimal ) )
            except ZeroDivisionError:
                pass
            return max(0.0, hit_chance)

    @property
    def distance_matrix(self):
        return self._distance_matrix

    @property
    def distance_matrix_v(self):
        return self._distance_matrix_v

    @property
    def to_hit(self, vision_limited=True):
        if vision_limited:
            return np.vectorize(self._to_hit)(self.distance_matrix_v)
        return np.vectorize(self._to_hit)(self.distance_matrix)

    def visualize(self, show=True, out_filename=None, ax=None):
        ax.clear()
        sns.set_theme()
        heatmap = sns.heatmap(self.to_hit, annot=True, cbar=False, ax=ax)
        heatmap.invert_yaxis()
        if out_filename is not None:
            heatmap.set_title(f'Accuracy for {self.gun}')
            heatmap.get_figure().savefig(out_filename)
            print(f'{out_filename} saved.')
        elif show:
            heatmap.set_title(f'Accuracy for {self.gun}')
            plt.show()


if __name__ == '__main__':
    v = JupiterHellRangeVisualizer()
    try:
        minr = int( input('Minimum Range? ' ) or 0 )
        optr = int( input('Optimum Range? ' ) )
        maxr = int( input('Maximum Range? ' ) )
        v.gun.update( minimum_range=minr, optimal_range=optr, maximum_range=maxr )

        out_filename = input('Enter a filename to save to file, or press enter to display: ') or None
        v.visualize(out_filename=out_filename)
    except ValueError:
        raise
