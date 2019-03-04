#!/bin/bash

ipython full_pipe.py & \
ipython full_pipe1.py & \
ipython full_pipe2.py & \
ipython full_pipe3.py & \
ipython full_pipe4.py & \
ipython full_pipe5.py & \

wait

ipython concat.py
echo "RESULTS IN FINAL_RESULT.csv"
