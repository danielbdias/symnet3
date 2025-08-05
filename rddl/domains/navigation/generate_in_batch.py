#!/usr/bin/env python3
from generate_instance import NavigationInstanceGenerator

def main():
    """Run all examples"""
    print("Navigation Instance Generator Examples")
    print("=====================================")
    
    MIN_SIZE = 5
    MAX_SIZE = 20
    
    sizes = []
    
    for x_size in range(MIN_SIZE, MAX_SIZE+1):
        for y_size in range(MIN_SIZE, MAX_SIZE+1):
            sizes.append((x_size, y_size))
            
    sizes = sorted(sizes, key=lambda x: x[0] * x[1])
    instance_number = 0
            
    for x_size, y_size in sizes:
        instance_name = f"navigation_inst_mdp__{instance_number}"
        
        generator = NavigationInstanceGenerator(
            instance_name=instance_name,
            size_x=x_size,
            size_y=y_size,
            obfuscate_mode="normal",
            horizon=100,
            discount=0.95
        )
        
        content = generator.generate()
        
        generator.save_instance(content)
        
        instance_number += 1
        
        print(f"Generated: {instance_name}.rddl")
    

if __name__ == "__main__":
    main()