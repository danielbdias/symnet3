#!/bin/bash
#SBATCH --time=06:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=4G

# fail if any errors
set -e

uv run python ./multi_train/deep_plan/train.py