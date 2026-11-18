# Experiment 6 - Robot traversal using Means-End Analysis
# INPUT: start_pos = (2, 3), goal_pos = (5, 7)   (10x10 grid, 50px cells)
# Moves along x first, then y (as in the algorithm).
import tkinter as tk
import time

def mea_path(start, goal):
    """Pure-logic MEA: returns the list of positions visited."""
    x, y = start
    path = [(x, y)]
    while (x, y) != goal:
        x_diff, y_diff = goal[0] - x, goal[1] - y
        if x_diff != 0:
            x += 1 if x_diff > 0 else -1
        elif y_diff != 0:
            y += 1 if y_diff > 0 else -1
        path.append((x, y))
    return path

class RobotTraversalApp:
    def __init__(self, root, start, goal):
        self.root = root
        self.root.title("Robot Traversal Using Means-End Analysis")
        self.start, self.goal = start, goal
        self.current_position = start
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack()
        self.draw_grid()
        tk.Button(self.root, text="Start Traversal", command=self.start_traversal).pack(pady=20)
        self.output_label = tk.Label(self.root, font=("Helvetica", 12))
        self.output_label.pack()
        self.flow_label = tk.Label(self.root, text="Flow of Movement:", font=("Helvetica", 12))
        self.flow_label.pack(pady=10)

    def draw_grid(self):
        for i in range(0, 501, 50):
            self.canvas.create_line(i, 0, i, 500, fill="gray")
            self.canvas.create_line(0, i, 500, i, fill="gray")
        sx, sy = self.start; gx, gy = self.goal
        self.canvas.create_rectangle(sx*50+10, sy*50+10, sx*50+40, sy*50+40, fill="green", outline="black")
        self.canvas.create_rectangle(gx*50+10, gy*50+10, gx*50+40, gy*50+40, fill="red", outline="black")

    def update_output(self, text):
        self.output_label.config(text=text)
        self.root.update_idletasks()

    def update_robot_position(self):
        self.canvas.delete("robot")
        x, y = self.current_position
        self.canvas.create_rectangle(x*50+10, y*50+10, x*50+40, y*50+40,
                                     fill="blue", outline="black", tags="robot")

    def move_robot(self):
        for pos in mea_path(self.current_position, self.goal)[1:]:
            self.current_position = pos
            self.update_robot_position()
            self.update_output(f"Current Position: {pos}")
            self.flow_label.config(text=f"Moving to: {pos}")
            self.root.update()
            time.sleep(0.5)

    def start_traversal(self):
        self.update_output(f"Starting at {self.start}")
        self.move_robot()
        self.update_output(f"Goal Reached at {self.goal}!")

if __name__ == "__main__":
    start_pos, goal_pos = (2, 3), (5, 7)
    print("Path:", mea_path(start_pos, goal_pos))
    root = tk.Tk()
    app = RobotTraversalApp(root, start_pos, goal_pos)
    root.mainloop()
