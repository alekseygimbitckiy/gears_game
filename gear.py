from dataclasses import dataclass
from typing import Literal###################TYPE_CHECKING
import math

from figure import Figure

@dataclass
class Gear:
    indx_gear: int
    num_figures: int
    alpha: float
    figure_type: str
    figures: list[Figure] = None
    neighbor_l: 'Gear' = None
    neighbor_r: 'Gear' = None
    indx_to_swap_l: int = None
    indx_to_swap_r: int = 0

    def __post_init__(self):
        self.figures = [Figure(self.figure_type) for _ in range(self.num_figures)] if self.figures is None else self.figures
        self.indx_to_swap_l = int(self.num_figures/2)
        if self.num_figures % 2 == 1:
            raise ValueError("num_figures must be even to swap figures in boyh dirrections")

    def rotate(self, step: int):
        # self.figures = self.figures[-step:] + self.figures[:-step]###################TODO: check is it correct

        #or

        self.indx_to_swap_l -= step
        self.indx_to_swap_r -= step
        self.indx_to_swap_l %= self.num_figures
        self.indx_to_swap_r %= self.num_figures

        self.alpha += step * 360 / self.num_figures
        self.alpha %= 360

        if not self.neighbor_r is None:
            self.neighbor_r.rotate(-step)

    def swap_fig(self, dirr: Literal[-1, 1]):
        match dirr:
            case -1:
                self.figures[self.indx_to_swap_l], self.neighbor_l.figures[self.neighbor_l.indx_to_swap_r] = \
                    self.neighbor_l.figures[self.neighbor_l.indx_to_swap_r], self.figures[self.indx_to_swap_l]
            case 1:
                self.figures[self.indx_to_swap_r], self.neighbor_r.figures[self.neighbor_r.indx_to_swap_l] = \
                    self.neighbor_r.figures[self.neighbor_r.indx_to_swap_l], self.figures[self.indx_to_swap_r]
                y_ = 0


    