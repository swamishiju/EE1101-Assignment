from itertools import accumulate
from typing import List

import numpy as np

from phasor import Phasor, pi


def convert_to_phasor_list(glyph, T=5, max_dlen=40) -> List[Phasor]:
    omega = 2 * pi / T
    ret_ = {m: Phasor(0, m * omega) for m in range(-max_dlen, max_dlen + 1)}

    func = convert_to_func(glyph, T=T)
    # func = convert_to_func(glyph_circle)

    for m in ret_:
        for t in range(len(func)):
            ret_[m].r += func[t] * np.exp(-1j * omega * m * t / 100) * 0.01 / T

    return list(ret_.values())


def convert_to_func(glyph_lines, T=2, dt=0.01):
    lengths = [abs(i[0] - i[2]) + abs(i[1] - i[3]) for i in glyph_lines]
    t_length = sum(lengths)
    t_div = int(T / dt)
    T_div_intervals = np.array(lengths) / t_length * t_div
    T_div_lengths = list(accumulate(T_div_intervals))
    index = 0
    t_index = 0
    ret = [0j] * t_div
    c_glyph = glyph_lines[0]
    p1 = c_glyph[0] + c_glyph[1] * 1j
    p2 = c_glyph[2] + c_glyph[3] * 1j
    t1 = 0
    t2 = T_div_lengths[0]

    while t_index < t_div:
        if t_index > T_div_lengths[index]:
            t1 = T_div_lengths[index]
            index += 1
            c_glyph = glyph_lines[index]
            t2 = T_div_lengths[index]
            p1 = c_glyph[0] + c_glyph[1] * 1j
            p2 = c_glyph[2] + c_glyph[3] * 1j

        ret[t_index] = (t_index - t1) / (t2 - t1) * (p2 - p1) + p1
        t_index += 1

    ret += [p2]
    return ret
