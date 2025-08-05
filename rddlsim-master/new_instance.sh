
# echo "relative_path_domain_file relative_path_instance_file name_of_instance instance_number"
# echo "./new_instance.sh rddl/domains/sysadmin_mdp.rddl rddl/domains/sysadmin_inst_mdp__900.rddl sysadmin_inst_mdp__900 900"

# Lock configuration
LOCKFILE="./.myscript.exclusivelock"
TIMEOUT=300
RETRY_INTERVAL=1

# Function to try acquiring lock with timeout
acquire_lock() {
    local elapsed=0
    while [ $elapsed -lt $TIMEOUT ]; do
        if shlock -f "$LOCKFILE" -p $$; then
            return 0
        fi
        sleep $RETRY_INTERVAL
        elapsed=$((elapsed + RETRY_INTERVAL))
    done
    return 1
}

# Try to acquire lock
if acquire_lock; then
    # Set up cleanup trap to ensure lock is released
    trap 'rm -f "$LOCKFILE"' EXIT INT TERM
    
    echo "Lock acquired, proceeding with operations..."
    
    # Copy the instance file
    cp ../$2 ../gym/envs/rddl/$2

    # Create a dbn file
    mkdir temp_merger_$3
    cat ../$1 ../$2 > ./temp_merger_$3/temp.rddl

    ./run rddl.viz.RDDL2Graph ./temp_merger_$3/temp.rddl $3

    # Copy the dbn file
    cd ..
    cp ./rddlsim-master/tmp_rddl_graphviz.dot ./rddl/dbn/$3.dot
    cp ./rddl/dbn/$3.dot ./gym/envs/rddl/rddl/dbn/

    # Create a dot file
    echo "STARTING RDDL-PARSER"
    ./rddl/lib/rddl-parser $1 $2 .
    echo "FINISHED WITH RDDL-PARSER"
    # Copy dot file
    cp $3 ./rddl/parsed/$3
    cp $3 ./gym/envs/rddl/rddl/parsed/$3

    # Copy env ile
    # cp ./rddl/lib/clibxx.so ./rddl/lib/clibxx$4.so 
    # cp ./rddl/lib/clibxx.so ./gym/envs/rddl/rddl/lib/clibxx$4.so 
    # chmod +x ./gym/envs/rddl/rddl/lib/clibxx$4.so

    # rm ./rddlsim-master/tmp_rddl_graphviz.dot
    rm $3
    
    echo "Operations completed successfully"
    
else
    echo "Could not acquire lock within $TIMEOUT seconds" >&2
    exit 1
fi
