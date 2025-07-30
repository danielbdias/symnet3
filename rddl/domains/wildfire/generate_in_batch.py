#!/usr/bin/env python3
from generate_instance import WildfireInstanceGenerator

def get_targets(x_size, y_size):
    targets = []
    
    x_target_area_start = x_size - (x_size // 3)
    y_target_area_start = y_size - (y_size // 3)
    
    # targets for odd x
    for x in range(x_size, x_target_area_start, -2):
        for y in range(y_size, y_target_area_start, -2):
            targets.append(f"x{x},y{y}")
            
    # targets for even x
    for x in range(x_size - 1, x_target_area_start, -2):
        for y in range(y_size - 1, y_target_area_start, -2):
            targets.append(f"x{x},y{y}")
            
    return targets

def get_initial_burning(x_size, y_size):
    initial_burning = []
    
    x_final_burning_area = (x_size // 3)
    y_final_burning_area = (y_size // 3)
    
    for x in range(1, x_final_burning_area + 1, 2):
        for y in range(1, y_final_burning_area + 1, 2):
            initial_burning.append(f"x{x},y{y}")
            
    for x in range(2, x_final_burning_area + 1, 2):
        for y in range(2, y_final_burning_area + 1, 2):
            initial_burning.append(f"x{x},y{y}")
            
    return initial_burning

def main():
    """Run all examples"""
    print("Wildfire Instance Generator Examples")
    print("=====================================")
    
    MIN_SIZE = 3
    MAX_SIZE = 12
    
    sizes = []
    
    for x_size in range(MIN_SIZE, MAX_SIZE+1):
        for y_size in range(MIN_SIZE, MAX_SIZE+1):
            sizes.append((x_size, y_size))
            
    sizes = sorted(sizes, key=lambda x: x[0] * x[1])
    instance_number = 0
            
    for x_size, y_size in sizes:
        generator = WildfireInstanceGenerator(x_size, y_size)
        
        instance_name = f"wildfire_inst_mdp__{instance_number}"
        
        content = generator.generate_instance(
            instance_name=instance_name,
            targets=get_targets(x_size, y_size),
            initial_burning=get_initial_burning(x_size, y_size),
            connectivity="8connected"    # Default 8-connected grid
        )
        generator.save_instance(instance_name, content)
        
        instance_number += 1
        
        print(f"Generated: {instance_name}.rddl")
    

if __name__ == "__main__":
    main()