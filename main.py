import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from object_loader import Object3D
from projection import ProjectiveSystem

# Screen dimensions
WIDTH, HEIGHT = 800, 600

def main():
    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Projective Visualization System")

    # OpenGL Init
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT) # 2D Ortho for drawing projected points directly
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Load Object
    obj_filename = "cube.txt"
    if len(sys.argv) > 1:
        obj_filename = sys.argv[1]
        
    obj = Object3D()
    try:
        obj.load_from_file(obj_filename)
        print(f"Loaded object '{obj_filename}' with {len(obj.vertices)} vertices and {len(obj.faces)} faces.")
    except Exception as e:
        print(f"Failed to load object: {e}")
        return

    # Initial Projection Parameters
    C = [0, 0, 5]       # Viewpoint
    P1 = [-1, -1, 0]    # Plane Point 1
    P2 = [1, -1, 0]     # Plane Point 2
    P3 = [0, 1, 0]      # Plane Point 3
    
    # Try to load config
    try:
        with open("config.txt", "r") as f:
            for line in f:
                parts = line.split()
                if not parts: continue
                if parts[0] == 'C': C = [float(x) for x in parts[1:]]
                if parts[0] == 'P1': P1 = [float(x) for x in parts[1:]]
                if parts[0] == 'P2': P2 = [float(x) for x in parts[1:]]
                if parts[0] == 'P3': P3 = [float(x) for x in parts[1:]]
        print("Loaded configuration from config.txt")
    except FileNotFoundError:
        print("config.txt not found, using defaults.")
    except Exception as e:
        print(f"Error loading config: {e}")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                # Simple controls to move C
                if event.key == pygame.K_w: C[2] -= 0.5
                if event.key == pygame.K_s: C[2] += 0.5
                if event.key == pygame.K_a: C[0] -= 0.5
                if event.key == pygame.K_d: C[0] += 0.5
                if event.key == pygame.K_q: C[1] += 0.5
                if event.key == pygame.K_e: C[1] -= 0.5

        # Update Projection System
        sys_proj = ProjectiveSystem(C, P1, P2, P3)

        # Project Vertices
        projected_verts = []
        for v in obj.vertices:
            p = sys_proj.project_point(v)
            if p:
                projected_verts.append(p)
            else:
                projected_verts.append(None)

        valid_points = [p for p in projected_points_raw(projected_verts) if p is not None]
        
        screen_coords = sys_proj.window_viewport_transform(
            [p for p in projected_verts if p is not None], WIDTH, HEIGHT
        )
        
        # Rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
                
        # Re-map indices
        idx_map = {}
        valid_idx = 0
        for i, p in enumerate(projected_verts):
            if p is not None:
                idx_map[i] = valid_idx
                valid_idx += 1
            else:
                idx_map[i] = -1
        
        for face in obj.faces:
            # Draw edges for the face
            for i in range(len(face)):
                idx1 = face[i]
                idx2 = face[(i+1) % len(face)]
                
                if idx_map[idx1] != -1 and idx_map[idx2] != -1:
                    p1 = screen_coords[idx_map[idx1]]
                    p2 = screen_coords[idx_map[idx2]]
                    glVertex2f(p1[0], p1[1])
                    glVertex2f(p2[0], p2[1])
        
        glEnd()
        
        pygame.display.flip()
        clock.tick(60)

def projected_points_raw(verts):
    return verts

if __name__ == "__main__":
    main()
