#!/bin/sh

# fail if any errors
set -e

# declare -a domains=("academic_advising" "crossing_traffic" "game_of_life" "navigation" "skill_teaching" "sysadmin" "tamarisk" "traffic" "wildfire" "recon" "triangle_tireworld" "elevators")

declare -a domains=("navigation")
# declare -a instances=($(seq 0 99))
declare -a instances=($(seq 0 5))

for i in "${domains[@]}"
do
	for j in "${instances[@]}"
	do
    	./new_instance.sh "rddl/domains/"$i"_mdp.rddl" "rddl/domains/"$i"_inst_mdp__"$j".rddl" $i"_inst_mdp__"$j $j
    done
done
