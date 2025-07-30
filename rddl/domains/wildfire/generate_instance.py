#!/usr/bin/env python3
"""
RDDL Wildfire Instance Generator

This script generates new instances for the Wildfire RDDL domain with configurable:
- Grid dimensions (x and y sizes)
- Neighbor relationships (with option to omit specific ones)
- Target locations
- Initial burning locations

Usage:
    python generate_instances.py --x_size 4 --y_size 4 --instance_name "wildfire_4x4"
"""

import argparse
import os
from typing import List, Tuple

class WildfireInstanceGenerator:
    def __init__(self, x_size: int, y_size: int):
        self.x_size = x_size
        self.y_size = y_size
        self.x_objects = [f"x{i+1}" for i in range(x_size)]
        self.y_objects = [f"y{i+1}" for i in range(y_size)]
    
    def get_all_neighbors(self) -> List[Tuple[str, str, str, str]]:
        """Generate all possible neighbor relationships (8-connected grid)"""
        neighbors = []
        
        for i, x1 in enumerate(self.x_objects):
            for j, y1 in enumerate(self.y_objects):
                # Check all 8 directions around current cell
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:  # Skip self
                            continue
                        
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.x_size and 0 <= nj < self.y_size:
                            x2 = self.x_objects[ni]
                            y2 = self.y_objects[nj]
                            neighbors.append((x1, y1, x2, y2))
        
        return neighbors
    
    def get_4connected_neighbors(self) -> List[Tuple[str, str, str, str]]:
        """Generate 4-connected neighbor relationships (up, down, left, right only)"""
        neighbors = []
        
        for i, x1 in enumerate(self.x_objects):
            for j, y1 in enumerate(self.y_objects):
                # Check 4 directions: up, down, left, right
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.x_size and 0 <= nj < self.y_size:
                        x2 = self.x_objects[ni]
                        y2 = self.y_objects[nj]
                        neighbors.append((x1, y1, x2, y2))
        
        return neighbors
    
    def parse_position(self, pos_str: str) -> Tuple[str, str]:
        """Parse position string like 'x2,y3' or '(x2,y3)' into (x, y) tuple"""
        pos_str = pos_str.strip('()')
        x_part, y_part = pos_str.split(',')
        return x_part.strip(), y_part.strip()
    
    def generate_instance(self, 
                         instance_name: str,
                         targets: List[str] = None,
                         initial_burning: List[str] = None,
                         omitted_neighbors: List[str] = None,
                         connectivity: str = "8connected",
                         max_actions: int = 1,
                         horizon: int = 40,
                         discount: float = 1.0) -> str:
        """
        Generate a complete RDDL instance file.
        
        Args:
            instance_name: Name for the instance
            targets: List of target positions like ["x2,y2", "x3,y1"]
            initial_burning: List of initially burning positions
            omitted_neighbors: List of neighbor relationships to omit like ["x1,y3->x1,y2"]
            connectivity: "8connected" or "4connected"
            max_actions: Maximum non-default actions per step
            horizon: Planning horizon
            discount: Discount factor
        """
        
        # Set defaults
        if targets is None:
            # Default: center and some border targets
            center_x = self.x_objects[self.x_size // 2]
            center_y = self.y_objects[self.y_size // 2]
            targets = [f"{center_x},{center_y}"]
        
        if initial_burning is None:
            # Default: corner position
            initial_burning = [f"{self.x_objects[0]},{self.y_objects[-1]}"]
        
        if omitted_neighbors is None:
            omitted_neighbors = []
        
        # Generate neighbors based on connectivity
        if connectivity == "8connected":
            all_neighbors = self.get_all_neighbors()
        else:
            all_neighbors = self.get_4connected_neighbors()
        
        # Parse omitted neighbors
        omitted_set = set()
        for omit_str in omitted_neighbors:
            if '->' in omit_str:
                from_pos, to_pos = omit_str.split('->')
                x1, y1 = self.parse_position(from_pos)
                x2, y2 = self.parse_position(to_pos)
                omitted_set.add((x1, y1, x2, y2))
        
        # Filter out omitted neighbors
        neighbors = [n for n in all_neighbors if n not in omitted_set]
        
        # Generate the RDDL content
        rddl_content = self._generate_rddl_content(
            instance_name, neighbors, targets, initial_burning, 
            max_actions, horizon, discount, omitted_neighbors
        )
        
        return rddl_content
    
    def _generate_rddl_content(self, instance_name: str, neighbors: List[Tuple], 
                              targets: List[str], initial_burning: List[str],
                              max_actions: int, horizon: int, discount: float,
                              omitted_neighbors: List[str]) -> str:
        """Generate the complete RDDL file content"""
        
        # Header with comments about omitted neighbors
        content = f"non-fluents nf_{instance_name} {{\n"
        content += f"\tdomain = wildfire_mdp;\n"
        content += f"\tobjects {{\n"
        content += f"\t\tx_pos : {{{','.join(self.x_objects)}}};\n"
        content += f"\t\ty_pos : {{{','.join(self.y_objects)}}};\n"
        content += f"\t}};\n"
        content += f"\tnon-fluents {{\n"
        
        # Add neighbor relationships with comments for omitted ones
        for x1, y1, x2, y2 in neighbors:
            content += f"\t\tNEIGHBOR({x1},{y1},{x2},{y2});\n"
        
        # Add comments for omitted neighbors
        if omitted_neighbors:
            content += f"\t\t// Omitted neighbors:\n"
            for omit_str in omitted_neighbors:
                content += f"\t\t// {omit_str}\n"
        
        # Add target locations
        for target_str in targets:
            x, y = self.parse_position(target_str)
            content += f"\t\tTARGET({x},{y});\n"
        
        content += f"\t}};\n"
        content += f"}}\n\n"
        
        # Instance definition
        content += f"instance {instance_name} {{\n"
        content += f"\tdomain = wildfire_mdp;\n"
        content += f"\tnon-fluents = nf_{instance_name};\n"
        content += f"\tinit-state {{\n"
        
        # Add initial burning locations
        for burn_str in initial_burning:
            x, y = self.parse_position(burn_str)
            content += f"\t\tburning({x},{y});\n"
        
        content += f"\t}};\n\n"
        content += f"\tmax-nondef-actions = {max_actions};\n"
        content += f"\thorizon  = {horizon};\n"
        content += f"\tdiscount = {discount};\n"
        content += f"}}\n"
        
        return content
    
    def save_instance(self, instance_name: str, content: str, output_dir: str = None):
        """Save the instance to a file"""
        if output_dir is None:
            output_dir = "."
        
        filename = f"{instance_name}.rddl"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"Instance saved to: {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Generate RDDL Wildfire instances')
    parser.add_argument('--x_size', type=int, required=True, help='Grid width (number of x positions)')
    parser.add_argument('--y_size', type=int, required=True, help='Grid height (number of y positions)')
    parser.add_argument('--instance_name', type=str, required=True, help='Name for the instance')
    parser.add_argument('--targets', type=str, nargs='*', default=None, 
                       help='Target positions (e.g., x2,y2 x3,y1)')
    parser.add_argument('--initial_burning', type=str, nargs='*', default=None,
                       help='Initially burning positions (e.g., x1,y3)')
    parser.add_argument('--omit_neighbors', type=str, nargs='*', default=None,
                       help='Neighbor relationships to omit (e.g., "x1,y3->x1,y2")')
    parser.add_argument('--connectivity', type=str, choices=['8connected', '4connected'], 
                       default='8connected', help='Grid connectivity type')
    parser.add_argument('--output_dir', type=str, default='.', help='Output directory')
    parser.add_argument('--horizon', type=int, default=40, help='Planning horizon')
    parser.add_argument('--max_actions', type=int, default=1, help='Max non-default actions per step')
    parser.add_argument('--discount', type=float, default=1.0, help='Discount factor')
    
    args = parser.parse_args()
    
    # Create generator
    generator = WildfireInstanceGenerator(args.x_size, args.y_size)
    
    # Generate instance
    content = generator.generate_instance(
        instance_name=args.instance_name,
        targets=args.targets,
        initial_burning=args.initial_burning,
        omitted_neighbors=args.omit_neighbors or [],
        connectivity=args.connectivity,
        max_actions=args.max_actions,
        horizon=args.horizon,
        discount=args.discount
    )
    
    # Save to file
    generator.save_instance(args.instance_name, content, args.output_dir)
    
    # Print summary
    print(f"\nGenerated {args.x_size}x{args.y_size} grid instance:")
    print(f"  - Connectivity: {args.connectivity}")
    print(f"  - Targets: {args.targets or 'default (center)'}")
    print(f"  - Initial burning: {args.initial_burning or 'default (corner)'}")
    print(f"  - Omitted neighbors: {len(args.omit_neighbors or [])}")

if __name__ == "__main__":
    main()