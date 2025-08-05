#!/bin/bash

WORKSPACE=/workspace/symnet3

# Copy the instance file
(
    # Wait for lock on /var/lock/.myscript.exclusivelock (fd 200) for 10 seconds
    flock -s -x -w 300 200

    # Do stuff
    cp $WORKSPACE/$2 $WORKSPACE/gym/envs/rddl/$2

    # Create a dbn file
    mkdir $WORKSPACE/temp_merger_$3
    cat $WORKSPACE/$1 $WORKSPACE/$2 > $WORKSPACE/temp_merger_$3/temp.rddl

    echo "$WORKSPACE/rddlsim-master/run.sh rddl.viz.RDDL2Graph ./temp_merger_$3/temp.rddl $3"
    $WORKSPACE/rddlsim-master/run.sh rddl.viz.RDDL2Graph ./temp_merger_$3/temp.rddl $3

    # Copy the dbn file
    cp $WORKSPACE/rddlsim-master/tmp_rddl_graphviz.dot $WORKSPACE/rddl/dbn/$3.dot
    cp $WORKSPACE/rddl/dbn/$3.dot $WORKSPACE/gym/envs/rddl/rddl/dbn/

    # Create a dot file
    echo "STARTING RDDL-PARSER"
    echo "/workspace/prost/rddl-parser $1 $2 ."
    /workspace/prost/rddl-parser $1 $2 $WORKSPACE
    echo "FINISHED WITH RDDL-PARSER"

    # Copy dot file
    cp $3 $WORKSPACE/rddl/parsed/$3
    cp $3 $WORKSPACE/gym/envs/rddl/rddl/parsed/$3

    # rm ./rddlsim-master/tmp_rddl_graphviz.dot
    rm $3


) 200>./.myscript.exclusivelock