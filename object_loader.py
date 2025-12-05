
class Object3D:
    def __init__(self):
        self.vertices = []  # List of (x, y, z) tuples
        self.faces = []     # List of lists of vertex indices

    def load_from_file(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Filter out empty lines and comments
        lines = [l.strip() for l in lines if l.strip()]
        
        iterator = iter(lines)
        try:
            # Read Number of Vertices
            nv = int(next(iterator))
            
            # Read Vertices
            for _ in range(nv):
                parts = next(iterator).split()
                x, y, z = map(float, parts[:3])
                self.vertices.append((x, y, z))
            
            # Read Number of Surfaces
            ns = int(next(iterator))
            
            # Read Surfaces
            for _ in range(ns):
                parts = next(iterator).split()
                nvps = int(parts[0])
                indices = [int(idx) for idx in parts[1:1+nvps]]
                self.faces.append(indices)
                
        except StopIteration:
            print("Error: Unexpected end of file.")
        except ValueError as e:
            print(f"Error parsing file: {e}")

    def __repr__(self):
        return f"Object3D(vertices={len(self.vertices)}, faces={len(self.faces)})"
