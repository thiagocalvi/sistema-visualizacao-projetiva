import math

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self):
        mag = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if mag == 0:
            return Vector(0, 0, 0)
        return Vector(self.x / mag, self.y / mag, self.z / mag)

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

class ProjectiveSystem:
    def __init__(self, C, P1, P2, P3):
        self.C = Vector(*C)
        self.P1 = Vector(*P1)
        self.P2 = Vector(*P2)
        self.P3 = Vector(*P3)
        
        # Calculate Normal N = (P1-P2) x (P3-P2)
        v1 = self.P1 - self.P2
        v2 = self.P3 - self.P2
        self.N = v1.cross(v2)
        self.n = self.N.normalize()
        
        # Calculate d0 and d1
        # d0 = C . n
        self.d0 = self.C.dot(self.n)
        
        # d1 = P1 . n (Any point on plane)
        self.d1 = self.P1.dot(self.n)
        
        # d = d1 - d0 (Distance parameter for matrix)
        # Note: The sign convention depends on the derivation.
        # Based on derivation: d = d1 - d0
        self.d = self.d1 - self.d0

    def project_point(self, P):
        x, y, z = P
        
        # Matrix multiplication
        # Row 0: d + a*nx, a*ny, a*nz, -a*d1
        # Row 1: b*nx, d + b*ny, b*nz, -b*d1
        # Row 2: c*nx, c*ny, d + c*nz, -c*d1
        # Row 3: nx, ny, nz, -d0
        
        nx, ny, nz = self.n.x, self.n.y, self.n.z
        a, b, c = self.C.x, self.C.y, self.C.z
        d = self.d
        d0 = self.d0
        d1 = self.d1
        
        # Compute x', y', z', w'
        xp = (d + a*nx)*x + (a*ny)*y + (a*nz)*z + (-a*d1)
        yp = (b*nx)*x + (d + b*ny)*y + (b*nz)*z + (-b*d1)
        zp = (c*nx)*x + (c*ny)*y + (d + c*nz)*z + (-c*d1)
        wp = (nx)*x + (ny)*y + (nz)*z + (-d0)
        
        if wp == 0:
            return None # Singularity or infinite projection
            
        return (xp/wp, yp/wp, zp/wp)

    def window_viewport_transform(self, projected_points, width, height):
        if not projected_points:
            return []
            
        # Find bounding box
        min_x = min(p[0] for p in projected_points)
        max_x = max(p[0] for p in projected_points)
        min_y = min(p[1] for p in projected_points)
        max_y = max(p[1] for p in projected_points)
        
        # Calculate scale to fit
        range_x = max_x - min_x
        range_y = max_y - min_y
        
        if range_x == 0: range_x = 1
        if range_y == 0: range_y = 1
        
        scale_x = (width * 0.8) / range_x
        scale_y = (height * 0.8) / range_y
        scale = min(scale_x, scale_y)
        
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        screen_points = []
        for x, y, z in projected_points:
            sx = (x - center_x) * scale + width / 2
            sy = (y - center_y) * scale + height / 2
            screen_points.append((sx, sy))
            
        return screen_points
