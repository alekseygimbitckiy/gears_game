from dataclasses import dataclass, field
from typing import Literal###################TYPE_CHECKING
import math

from figure import Figure

@dataclass
class Gear:
    num_figures: int
    alpha: float
    figure_type: str
    figures: list[Figure] = None
    neighbors: dict[str, 'Gear'] = field(default_factory=dict)
    indx_to_swap: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        self.figures = [Figure(self.figure_type) for _ in range(self.num_figures)] if self.figures is None else self.figures
        self.indx_to_swap['r'] = 0
        self.indx_to_swap['l'] = int(self.num_figures/2)
        self.indx_to_swap['d'] = int(self.num_figures/4)
        self.indx_to_swap['u'] = 3 * int(self.num_figures/4)
        if not self.num_figures % 4 == 0:
            raise ValueError("num_figures must divide by 4 to swap figures in all dirrections")
        self.was_rotated = False

    def rotate(self, step: int):
        # self.figures = self.figures[-step:] + self.figures[:-step]###################TODO: check is it correct

        #or
        for k in self.indx_to_swap:
            self.indx_to_swap[k] -= step
            self.indx_to_swap[k] %= self.num_figures

        self.alpha += step * 360 / self.num_figures
        self.alpha %= 360
        self.was_rotated = True

        for d in ['r', 'l', 'd', 'u']:
            if d in self.neighbors and not self.neighbors[d].was_rotated:
                self.neighbors[d].rotate(-step)

    def swap_fig(self, dirr: Literal['l', 'r', 'u', 'd']):
        match dirr:
            case 'l':
                self.figures[self.indx_to_swap['l']], self.neighbors['l'].figures[self.neighbors['l'].indx_to_swap['r']] = \
                    self.neighbors['l'].figures[self.neighbors['l'].indx_to_swap['r']], self.figures[self.indx_to_swap['l']]
            case 'r':
                self.figures[self.indx_to_swap['r']], self.neighbors['r'].figures[self.neighbors['r'].indx_to_swap['l']] = \
                    self.neighbors['r'].figures[self.neighbors['r'].indx_to_swap['l']], self.figures[self.indx_to_swap['r']]
            case 'd':
                self.figures[self.indx_to_swap['d']], self.neighbors['d'].figures[self.neighbors['d'].indx_to_swap['u']] = \
                    self.neighbors['d'].figures[self.neighbors['d'].indx_to_swap['u']], self.figures[self.indx_to_swap['d']]


    