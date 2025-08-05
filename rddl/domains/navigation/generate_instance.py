import os
import random
import argparse
import numpy as np


class NavigationInstanceGenerator:
    def __init__(self, instance_name: str, size_x: int, size_y: int, 
                 obfuscate_mode: str, horizon: int, discount: float):
        """Initialize the NavigationGenerator with individual parameters."""       
        self.instance_name = instance_name
        self.size_x = size_x
        self.size_y = size_y
        
        if obfuscate_mode == "obfuscate":
            self.obfuscate = True
        elif obfuscate_mode == "normal":
            self.obfuscate = False
        else:
            raise ValueError(f"Expected one of {{obfuscate,normal}}, got '{obfuscate_mode}'")
            
        self.horizon = horizon
        self.discount = discount
    
    def generate(self) -> str:
        """Generate the RDDL content based on obfuscation setting."""
        if self.obfuscate:
            return self.generate_obfuscate()
        else:
            return self.generate_normal()
    
    def generate_normal(self) -> str:
        """Generate normal (non-obfuscated) RDDL content."""
        sb = []
        
        sb.append(f"non-fluents nf_{self.instance_name} {{\n")
        sb.append("\tdomain = navigation_mdp;\n")
        sb.append("\tobjects {\n")
        
        # X positions
        sb.append("\t\txpos : {")
        x_positions = []
        for i in range(1, self.size_x + 1):
            x_positions.append(f"x{i}")
        sb.append(",".join(x_positions))
        sb.append("};\n")
        
        # Y positions
        sb.append("\t\typos : {")
        y_positions = []
        for j in range(1, self.size_y + 1):
            y_positions.append(f"y{j}")
        sb.append(",".join(y_positions))
        sb.append("};\n")
        
        sb.append("\t};\n")
        
        # Non-fluents
        sb.append("\tnon-fluents {\n")
        
        # NORTH/SOUTH connections
        for j in range(2, self.size_y + 1):
            sb.append(f"\t\tNORTH(y{j-1},y{j});\n")
            sb.append(f"\t\tSOUTH(y{j},y{j-1});\n")
        sb.append("\n")
        
        # EAST/WEST connections
        for i in range(2, self.size_x + 1):
            sb.append(f"\t\tEAST(x{i-1},x{i});\n")
            sb.append(f"\t\tWEST(x{i},x{i-1});\n")
        sb.append("\n")
        
        # Min/Max positions
        sb.append("\t\tMIN-XPOS(x1);\n")
        sb.append(f"\t\tMAX-XPOS(x{self.size_x});\n")
        sb.append("\t\tMIN-YPOS(y1);\n")
        sb.append(f"\t\tMAX-YPOS(y{self.size_y});\n\n")
        
        # Goal
        sb.append(f"\t\tGOAL(x{self.size_x},y{self.size_y});\n\n")
        
        # Obstacle probabilities
        dp = []
        for i in range(1, self.size_x + 1):
            for j in range(2, self.size_y):
                prob = (0.01 + (0.9 * (i - 1)) / (self.size_x - 1)) + 0.05 * random.uniform(0, 1)
                dp.append(f"\t\tP(x{i},y{j}) = {prob};\n")
        
        # Add probabilities (not permuted in normal mode for simplicity)
        for prob_line in dp:
            sb.append(prob_line)
        
        sb.append("\t};\n}")
        
        # Instance section
        sb.append(f"\n\ninstance {self.instance_name} {{\n")
        sb.append("\tdomain = navigation_mdp;\n")
        sb.append(f"\tnon-fluents = nf_{self.instance_name};\n")
        sb.append("\tinit-state {\n")
        
        # Initial robot position
        sb.append(f"\t\trobot-at(x{self.size_x},y1);\n")
        
        sb.append("\t};\n")
        sb.append("\tmax-nondef-actions = 1;\n")
        sb.append(f"\thorizon = {self.horizon};\n")
        sb.append(f"\tdiscount = {self.discount};\n")
        sb.append("}\n")
        
        return "".join(sb)
    
    def generate_obfuscate(self) -> str:
        """Generate obfuscated RDDL content."""
        sb = []
        
        sb.append(f"non-fluents nf_{self.instance_name} {{\n")
        sb.append("\tdomain = navigation_mdp;\n")
        sb.append("\tobjects {\n")
        
        # X positions (obfuscated)
        sb.append("\t\txpos : {")
        xp = []
        for i in range(1, self.size_x + 1):
            xp.append(f"x{i*i+5}")
        
        # Permute x positions
        indices = np.random.permutation(len(xp))
        x_positions = []
        for i in range(len(indices)):
            x_positions.append(xp[indices[i]])
        sb.append(",".join(x_positions))
        sb.append("};\n")
        
        # Y positions (obfuscated)
        sb.append("\t\typos : {")
        yp = []
        for j in range(1, self.size_y + 1):
            yp.append(f"y{j*j+11}")
        
        # Permute y positions
        indices = np.random.permutation(len(yp))
        y_positions = []
        for j in range(len(indices)):
            y_positions.append(yp[indices[j]])
        sb.append(",".join(y_positions))
        sb.append("};\n")
        
        sb.append("\t};\n")
        
        # Non-fluents (all in one list for permutation)
        sb.append("\tnon-fluents {\n")
        
        dp = []
        
        # NORTH/SOUTH connections (obfuscated)
        for j in range(2, self.size_y + 1):
            dp.append(f"\t\tNORTH(y{(j-1)*(j-1)+11},y{j*j+11});\n")
            dp.append(f"\t\tSOUTH(y{j*j+11},y{(j-1)*(j-1)+11});\n")
        
        # EAST/WEST connections (obfuscated)
        for i in range(2, self.size_x + 1):
            dp.append(f"\t\tEAST(x{(i-1)*(i-1)+5},x{i*i+5});\n")
            dp.append(f"\t\tWEST(x{i*i+5},x{(i-1)*(i-1)+5});\n")
        
        # Min/Max positions (obfuscated)
        dp.append("\t\tMIN-XPOS(x6);\n")
        dp.append(f"\t\tMAX-XPOS(x{self.size_x*self.size_x+5});\n")
        dp.append("\t\tMIN-YPOS(y12);\n")
        dp.append(f"\t\tMAX-YPOS(y{self.size_y*self.size_y+11});\n")
        
        # Goal (obfuscated)
        dp.append(f"\t\tGOAL(x{self.size_x*self.size_x+5},y{self.size_y*self.size_y+11});\n")
        
        # Obstacle probabilities (obfuscated)
        for i in range(1, self.size_x + 1):
            for j in range(2, self.size_y):
                prob = (0.01 + (0.9 * (i - 1)) / (self.size_x - 1)) + 0.05 * random.uniform(0, 1)
                dp.append(f"\t\tP(x{i*i+5},y{j*j+11}) = {prob};\n")
        
        # Permute all declarations
        indices = np.random.permutation(len(dp))
        for i in range(len(dp)):
            sb.append(dp[indices[i]])
        
        sb.append("\t};\n}")
        
        # Instance section
        sb.append(f"\n\ninstance {self.instance_name} {{\n")
        sb.append("\tdomain = navigation_mdp;\n")
        sb.append(f"\tnon-fluents = nf_{self.instance_name};\n")
        sb.append("\tinit-state {\n")
        
        # Initial robot position (obfuscated)
        sb.append(f"\t\trobot-at(x{self.size_x*self.size_x+5},y12);\n")
        
        sb.append("\t};\n")
        sb.append("\tmax-nondef-actions = 1;\n")
        sb.append(f"\thorizon = {self.horizon};\n")
        sb.append(f"\tdiscount = {self.discount};\n")
        sb.append("}\n")
        
        return "".join(sb)
    
    def save_instance(self, content: str, output_dir: str | None = None):
        if output_dir is None:
            output_dir = "."
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write to file
        output_file = os.path.join(output_dir, f"{self.instance_name}.rddl")
        with open(output_file, 'w') as f:
            f.write(content)


def main():
    """Main function to handle command line execution."""
    parser = argparse.ArgumentParser(
        description="Generate RDDL navigation instances",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "output_dir",
        help="Output directory for the generated RDDL file"
    )
    
    parser.add_argument(
        "instance_name", 
        help="Name of the instance (will be used as filename without .rddl extension)"
    )
    
    parser.add_argument(
        "size_x",
        type=int,
        help="Grid width (number of x positions)"
    )
    
    parser.add_argument(
        "size_y", 
        type=int,
        help="Grid height (number of y positions)"
    )
    
    parser.add_argument(
        "obfuscate_mode",
        choices=["obfuscate", "normal"],
        help="Whether to obfuscate the generated instance"
    )
    
    parser.add_argument(
        "horizon",
        type=int,
        help="Planning horizon (number of time steps)"
    )
    
    parser.add_argument(
        "discount",
        type=float,
        help="Discount factor (0.0 to 1.0)"
    )
    
    args = parser.parse_args()
    
    # Validate discount factor
    if not (0.0 <= args.discount <= 1.0):
        parser.error("Discount factor must be between 0.0 and 1.0")
    
    # Validate grid dimensions
    if args.size_x <= 0 or args.size_y <= 0:
        parser.error("Grid dimensions must be positive integers")
        
    # Validate horizon
    if args.horizon <= 0:
        parser.error("Horizon must be a positive integer")
    
    generator = NavigationInstanceGenerator(
        output_dir=args.output_dir,
        instance_name=args.instance_name,
        size_x=args.size_x,
        size_y=args.size_y,
        obfuscate_mode=args.obfuscate_mode,
        horizon=args.horizon,
        discount=args.discount
    )
    
    content = generator.generate()
    
    generator.save_instance(content, args.output_dir)
    
    print(f"Generated RDDL file: {args.output_dir}/{args.instance_name}.rddl")


if __name__ == "__main__":
    main()