import time
from rpi_ws281x import *
import argparse
import numpy
import numpy as np
import pandas

import yfinance as yf
import pytz

# LED strip configuration:
LED_COUNT = 1024  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 20  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

#################################################################################################
ledWidth = 32
ledHeight = 32
ledTopSectionHeight = 10
ledBottomSectionHeight = 10
ledMiddleSectionHeight = ledHeight - ledTopSectionHeight - ledBottomSectionHeight

letterSpace = np.array([[0],
                        [0],
                        [0],
                        [0],
                        [0],
                        [0],
                        [0],
                        [0],
                        [0],
                        [0]])

letterDot = np.array([[0],
                      [0],
                      [0],
                      [0],
                      [0],
                      [0],
                      [0],
                      [0],
                      [0],
                      [1]])

letterA = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1]])

letterB = np.array([[1, 1, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 0]])

letterC = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 0]])

letterD = np.array([[1, 1, 0, 0],
                    [1, 1, 1, 0],
                    [1, 0, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 1, 1],
                    [1, 1, 1, 0],
                    [1, 1, 0, 0]])

letterE = np.array([[1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]])

letterF = np.array([[1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 1, 0],
                    [1, 1, 1, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0]])

letterG = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 0]])

letterH = np.array([[1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1]])

letterI = np.array([[0, 1, 1, 1],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 1, 1, 1]])

letterJ = np.array([[1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [1, 0, 1, 0],
                    [1, 0, 1, 0],
                    [1, 1, 1, 0],
                    [0, 1, 0, 0]])

letterK = np.array([[1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 1, 0],
                    [1, 1, 1, 0],
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [1, 0, 1, 0],
                    [1, 0, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1]])

letterL = np.array([[1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 1, 1]])

letterM = np.array([[1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1]])

letterN = np.array([[1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 0, 1],
                    [1, 1, 0, 1],
                    [1, 1, 0, 1],
                    [1, 0, 1, 1],
                    [1, 0, 1, 1],
                    [1, 0, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1]])

letterO = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 0]])

letterP = np.array([[0, 1, 1, 0],
                    [1, 0, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 1, 1],
                    [1, 1, 1, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0]])

letterQ = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 1, 0],
                    [1, 1, 1, 1],
                    [0, 1, 0, 1]])

letterR = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [1, 0, 1, 0],
                    [1, 0, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1]])

letterS = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 1, 1],
                    [0, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 0]])

letterT = np.array([[0, 1, 1, 1],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0]])

letterU = np.array([[1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 0]])

letterV = np.array([[1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0]])

letterW = np.array([[1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 0, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 0]])

letterX = np.array([[1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1]])

letterY = np.array([[0, 1, 0, 1],
                    [0, 1, 0, 1],
                    [0, 1, 0, 1],
                    [0, 1, 0, 1],
                    [0, 1, 1, 1],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0]])

letterZ = np.array([[1, 1, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 1, 1, 0],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 1, 1]])

letter0 = np.array([[0, 1, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0]])

letter1 = np.array([[0, 1, 1, 0],
                    [1, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [1, 1, 1, 1]])

letter2 = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 1, 1],
                    [0, 1, 1, 0],
                    [1, 1, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 1, 1]])

letter3 = np.array([[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 1, 1, 0],
                    [0, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 0]])

letter4 = np.array([[0, 0, 1, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [1, 0, 1, 0],
                    [1, 0, 1, 0],
                    [1, 1, 1, 1],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0]])

letter5 = np.array([[1, 1, 1, 1],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0]])

letter6 = np.array([[1, 1, 1, 1],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 0],
                    [1, 1, 1, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0]])

letter7 = np.array([[1, 1, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1]])

letter8 = np.array([[0, 1, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0]])

letter9 = np.array([[0, 1, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0]])

letterArrowUp = np.array([[0, 0, 1, 0, 0],
                          [0, 1, 1, 1, 0],
                          [1, 1, 1, 1, 1],
                          [0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])

letterArrowDown = np.array([[0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, 1, 0, 0],
                            [1, 1, 1, 1, 1],
                            [0, 1, 1, 1, 0],
                            [0, 0, 1, 0, 0]])

ledMappingMatrix = np.array([[255, 254, 253, 252, 251, 250, 249, 248, 263, 262, 261, 260, 259, 258, 257, 256, 767, 766,
                              765, 764, 763, 762, 761, 760, 775, 774, 773, 772, 771, 770, 769, 768],
                             [240, 241, 242, 243, 244, 245, 246, 247, 264, 265, 266, 267, 268, 269, 270, 271, 752, 753,
                              754, 755, 756, 757, 758, 759, 776, 777, 778, 779, 780, 781, 782, 783],
                             [239, 238, 237, 236, 235, 234, 233, 232, 279, 278, 277, 276, 275, 274, 273, 272, 751, 750,
                              749, 748, 747, 746, 745, 744, 791, 790, 789, 788, 787, 786, 785, 784],
                             [224, 225, 226, 227, 228, 229, 230, 231, 280, 281, 282, 283, 284, 285, 286, 287, 736, 737,
                              738, 739, 740, 741, 742, 743, 792, 793, 794, 795, 796, 797, 798, 799],
                             [223, 222, 221, 220, 219, 218, 217, 216, 295, 294, 293, 292, 291, 290, 289, 288, 735, 734,
                              733, 732, 731, 730, 729, 728, 807, 806, 805, 804, 803, 802, 801, 800],
                             [208, 209, 210, 211, 212, 213, 214, 215, 296, 297, 298, 299, 300, 301, 302, 303, 720, 721,
                              722, 723, 724, 725, 726, 727, 808, 809, 810, 811, 812, 813, 814, 815],
                             [207, 206, 205, 204, 203, 202, 201, 200, 311, 310, 309, 308, 307, 306, 305, 304, 719, 718,
                              717, 716, 715, 714, 713, 712, 823, 822, 821, 820, 819, 818, 817, 816],
                             [192, 193, 194, 195, 196, 197, 198, 199, 312, 313, 314, 315, 316, 317, 318, 319, 704, 705,
                              706, 707, 708, 709, 710, 711, 824, 825, 826, 827, 828, 829, 830, 831],
                             [191, 190, 189, 188, 187, 186, 185, 184, 327, 326, 325, 324, 323, 322, 321, 320, 703, 702,
                              701, 700, 699, 698, 697, 696, 839, 838, 837, 836, 835, 834, 833, 832],
                             [176, 177, 178, 179, 180, 181, 182, 183, 328, 329, 330, 331, 332, 333, 334, 335, 688, 689,
                              690, 691, 692, 693, 694, 695, 840, 841, 842, 843, 844, 845, 846, 847],
                             [175, 174, 173, 172, 171, 170, 169, 168, 343, 342, 341, 340, 339, 338, 337, 336, 687, 686,
                              685, 684, 683, 682, 681, 680, 855, 854, 853, 852, 851, 850, 849, 848],
                             [160, 161, 162, 163, 164, 165, 166, 167, 344, 345, 346, 347, 348, 349, 350, 351, 672, 673,
                              674, 675, 676, 677, 678, 679, 856, 857, 858, 859, 860, 861, 862, 863],
                             [159, 158, 157, 156, 155, 154, 153, 152, 359, 358, 357, 356, 355, 354, 353, 352, 671, 670,
                              669, 668, 667, 666, 665, 664, 871, 870, 869, 868, 867, 866, 865, 864],
                             [144, 145, 146, 147, 148, 149, 150, 151, 360, 361, 362, 363, 364, 365, 366, 367, 656, 657,
                              658, 659, 660, 661, 662, 663, 872, 873, 874, 875, 876, 877, 878, 879],
                             [143, 142, 141, 140, 139, 138, 137, 136, 375, 374, 373, 372, 371, 370, 369, 368, 655, 654,
                              653, 652, 651, 650, 649, 648, 887, 886, 885, 884, 883, 882, 881, 880],
                             [128, 129, 130, 131, 132, 133, 134, 135, 376, 377, 378, 379, 380, 381, 382, 383, 640, 641,
                              642, 643, 644, 645, 646, 647, 888, 889, 890, 891, 892, 893, 894, 895],
                             [127, 126, 125, 124, 123, 122, 121, 120, 391, 390, 389, 388, 387, 386, 385, 384, 639, 638,
                              637, 636, 635, 634, 633, 632, 903, 902, 901, 900, 899, 898, 897, 896],
                             [112, 113, 114, 115, 116, 117, 118, 119, 392, 393, 394, 395, 396, 397, 398, 399, 624, 625,
                              626, 627, 628, 629, 630, 631, 904, 905, 906, 907, 908, 909, 910, 911],
                             [111, 110, 109, 108, 107, 106, 105, 104, 407, 406, 405, 404, 403, 402, 401, 400, 623, 622,
                              621, 620, 619, 618, 617, 616, 919, 918, 917, 916, 915, 914, 913, 912],
                             [96, 97, 98, 99, 100, 101, 102, 103, 408, 409, 410, 411, 412, 413, 414, 415, 608, 609, 610,
                              611, 612, 613, 614, 615, 920, 921, 922, 923, 924, 925, 926, 927],
                             [95, 94, 93, 92, 91, 90, 89, 88, 423, 422, 421, 420, 419, 418, 417, 416, 607, 606, 605,
                              604, 603, 602, 601, 600, 935, 934, 933, 932, 931, 930, 929, 928],
                             [80, 81, 82, 83, 84, 85, 86, 87, 424, 425, 426, 427, 428, 429, 430, 431, 592, 593, 594,
                              595, 596, 597, 598, 599, 936, 937, 938, 939, 940, 941, 942, 943],
                             [79, 78, 77, 76, 75, 74, 73, 72, 439, 438, 437, 436, 435, 434, 433, 432, 591, 590, 589,
                              588, 587, 586, 585, 584, 951, 950, 949, 948, 947, 946, 945, 944],
                             [64, 65, 66, 67, 68, 69, 70, 71, 440, 441, 442, 443, 444, 445, 446, 447, 576, 577, 578,
                              579, 580, 581, 582, 583, 952, 953, 954, 955, 956, 957, 958, 959],
                             [63, 62, 61, 60, 59, 58, 57, 56, 455, 454, 453, 452, 451, 450, 449, 448, 575, 574, 573,
                              572, 571, 570, 569, 568, 967, 966, 965, 964, 963, 962, 961, 960],
                             [48, 49, 50, 51, 52, 53, 54, 55, 456, 457, 458, 459, 460, 461, 462, 463, 560, 561, 562,
                              563, 564, 565, 566, 567, 968, 969, 970, 971, 972, 973, 974, 975],
                             [47, 46, 45, 44, 43, 42, 41, 40, 471, 470, 469, 468, 467, 466, 465, 464, 559, 558, 557,
                              556, 555, 554, 553, 552, 983, 982, 981, 980, 979, 978, 977, 976],
                             [32, 33, 34, 35, 36, 37, 38, 39, 472, 473, 474, 475, 476, 477, 478, 479, 544, 545, 546,
                              547, 548, 549, 550, 551, 984, 985, 986, 987, 988, 989, 990, 991],
                             [31, 30, 29, 28, 27, 26, 25, 24, 487, 486, 485, 484, 483, 482, 481, 480, 543, 542, 541,
                              540, 539, 538, 537, 536, 999, 998, 997, 996, 995, 994, 993, 992],
                             [16, 17, 18, 19, 20, 21, 22, 23, 488, 489, 490, 491, 492, 493, 494, 495, 528, 529, 530,
                              531, 532, 533, 534, 535, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007],
                             [15, 14, 13, 12, 11, 10, 9, 8, 503, 502, 501, 500, 499, 498, 497, 496, 527, 526, 525, 524,
                              523, 522, 521, 520, 1015, 1014, 1013, 1012, 1011, 1010, 1009, 1008],
                             [0, 1, 2, 3, 4, 5, 6, 7, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516,
                              517, 518, 519, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023]])


def textToMatrix(ticker):
    for i in range(len(ticker)):
        match = matchingText(ticker[i])
        if i == 0:
            textMatrix = match
        elif len(textMatrix[0]) <= (ledWidth - 4):
            textMatrix = np.concatenate((textMatrix, letterSpace, match), axis=1)
        else:
            print("Error, line overflow")
    # print(textMatrix)
    return textMatrix


def matchingText(character):
    return {
        'A': letterA,
        'B': letterB,
        'C': letterC,
        'D': letterD,
        'E': letterE,
        'F': letterF,
        'G': letterG,
        'H': letterH,
        'I': letterI,
        'J': letterJ,
        'K': letterK,
        'L': letterL,
        'M': letterM,
        'N': letterN,
        'O': letterO,
        'P': letterP,
        'Q': letterQ,
        'R': letterR,
        'S': letterS,
        'T': letterT,
        'U': letterU,
        'V': letterV,
        'W': letterW,
        'X': letterX,
        'Y': letterY,
        'Z': letterZ,
        '0': letter0,
        '1': letter1,
        '2': letter2,
        '3': letter3,
        '4': letter4,
        '5': letter5,
        '6': letter6,
        '7': letter7,
        '8': letter8,
        '9': letter9,
        '.': letterDot
    }.get(character, "error")


def matrixPadding(inputMatrix, ledWidth, ledHeight):
    npInputMatrix = np.array(inputMatrix)
    (h, w) = npInputMatrix.shape
    # print(npInputMatrix.shape)
    paddedMatrix = np.pad(npInputMatrix, ((0, ledHeight - h), (0, ledWidth - w)), constant_values=0)
    return paddedMatrix


def matrixFlattenedZeroRemoved(inputMatrix):
    matrix = np.matrix(inputMatrix)
    inputList = matrix.flatten()
    return inputList[inputList != 0]


def tickerLength4(ticker):
    if len(ticker) <= 4:
        tickerProcessed = ticker
    else:
        tickerProcessed = ticker[0:4]
    return tickerProcessed


def topTickerLEDSectionMatrix(ticker):
    tickerProcessed = tickerLength4(ticker)
    textMatrix = textToMatrix(tickerProcessed)
    paddedTextMatrix = matrixPadding(textMatrix, ledWidth, ledTopSectionHeight)
    # maskedOnLEDMatrixed = numpy.multiply(ledMappingMatrix, paddedTextMatrix)
    # ledOnList = matrixFlattenedZeroRemoved(maskedOnLEDMatrixed)
    return paddedTextMatrix


def priceLengthChecker(price):
    if 0 <= price < 9999.99:
        price = round(price, 2)
    elif 9999.99 <= price < 99999:
        price = round(price, 1)
    elif 99999 <= price < 1000000:
        price = int(price)
    elif 1000000 <= price < 1000000000:
        price = round(price / 1000000, 2)
        price = str(price) + "M"
    else:
        print("Price Error")
    return price


def numberToMatrix(price):
    stringPrice = str(price)
    for i in range(len(stringPrice)):
        match = matchingText(stringPrice[i])
        if i == 0:
            priceMatrix = match
        elif len(priceMatrix[0]) <= (ledWidth - 4):
            priceMatrix = np.concatenate((priceMatrix, letterSpace, match), axis=1)
        else:
            print("Error, line overflow")
    # print(textMatrix)
    return priceMatrix


def bottomPriceLEDSectionMatrix(price):
    priceProcessed = priceLengthChecker(price)
    textMatrix = numberToMatrix(priceProcessed)
    paddedTextMatrix = matrixPadding(textMatrix, ledWidth, ledBottomSectionHeight)
    # maskedOnLEDMatrixed = numpy.multiply(ledMappingMatrix, paddedTextMatrix)
    # ledOnList = matrixFlattenedZeroRemoved(maskedOnLEDMatrixed)
    return paddedTextMatrix


def middleGraphLEDSectionMatrix():
    return np.zeros((ledMiddleSectionHeight, ledWidth), dtype=int)


def addTopMiddleBottomMatrix(top, middle, bottom):
    return np.concatenate((top, middle, bottom), axis=0)


def ledToTurnOnList(ticker, price):
    top = topTickerLEDSectionMatrix(ticker)
    middle = middleGraphLEDSectionMatrix()
    bottom = bottomPriceLEDSectionMatrix(price)
    matrix = addTopMiddleBottomMatrix(top, middle, bottom)
    maskedOnLEDMatrixed = numpy.multiply(ledMappingMatrix, matrix)
    flattenedOnLEDList = maskedOnLEDMatrixed.flatten()
    return flattenedOnLEDList[flattenedOnLEDList != 0]


###########################################################################################

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def showInputList(strip, input_list, color, wait_ms=5000):
    if color == 'green':
        colorInput = Color(0, 255, 0)
    elif color == 'red':
        colorInput = Color(255, 0, 0)
    else:
        colorInput = Color(255, 255, 255) #white

    ledOFF = Color(0, 0, 0) #black

    for i in input_list:
        strip.setPixelColor(i.item(), colorInput)
    strip.show()
    time.sleep(wait_ms / 1000.0)
    for i in input_list:
        strip.setPixelColor(i.item(), ledOFF)
    strip.show()


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


###########################################################
# Yahoo Fiance Part

# obtain yahoo finance historic data
def yfianceData(symbol):
    price_history = yf.Ticker(symbol).history(
        period='1d',  # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval='1m',  # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        actions=False)

    # calculating key price and date information
    opening_price = price_history.iloc[0]["Close"]
    closing_price = price_history.iloc[-1]["Close"]
    time_adjustment = price_history.index.tz_convert(pytz.timezone('America/Vancouver'))

    # obtain yesterday's end price
    ytd_price_history = yf.Ticker(symbol).history(period='5d', interval='1d', actions=False)
    ytd_data_range = len(ytd_price_history) - 2
    ytd_closing_price = ytd_price_history.iloc[ytd_data_range]["Close"]

    # determine if line is green or red based on today's gains or losses
    if (closing_price - ytd_closing_price) > 0:
        color_logic = 'green'
    else:
        color_logic = 'red'

    # calculate day's gains/loss and percentage change
    price_change = closing_price - ytd_closing_price
    percentage_change = (closing_price - ytd_closing_price) / ytd_closing_price * 100

    # update figure and Text
    ticker_current_price = round(closing_price, 2)
    ticker_price_change = round(price_change, 2)
    ticker_price_change_percentage = round(percentage_change, 2)

    return ticker_current_price, ticker_price_change_percentage, color_logic


# obtain ticker from csv file
ticker_csv_file_name = 'ticker.csv'
df_ticker = pandas.read_csv(filepath_or_buffer=ticker_csv_file_name)
tickers = df_ticker['tickers'].dropna().tolist()
crypto = df_ticker['crypto'].dropna().tolist()
selected_ticker = tickers + crypto
#######################################################################################


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print("List of Tickers")
            for ticker in selected_ticker:
                (tickerPrice, tickerPriceChangePercentage, color_logic) = yfianceData(ticker)
                tickerData = 'Ticker: {}, Price: {}, Change%: {}'.format(ticker,
                                                                         tickerPrice,
                                                                         round(tickerPriceChangePercentage, 2))
                print(tickerData)
                showInputList(strip, ledToTurnOnList(ticker, tickerPrice), color_logic)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
