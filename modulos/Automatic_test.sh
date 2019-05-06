#!/bin/bash


# 1 = OWGIS Global
# 2 = OWGIS meteorologia
# 3 = OWGIS Oleaje
# 4 = los 3 anteriores
source ~/anaconda3/envs/tensorflow/bin/activate selenuim
python ../Lib/Automatic_test.py 4
