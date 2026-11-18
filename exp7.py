# Experiment 7 - TSP using A* (f = g + h, h = MST-based admissible heuristic)
# INPUT (in the window): number of cities = 12 -> click "Generate Cities" -> "Solve TSP"
# (Cities are random in 0..100 x 0..100. Allowed range: 2 to MAX_CITIES = 12.)
import heapq, math, random, time, threading
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def mst_cost(cities, nodes):
    """Prim's MST over the given node indices."""
    nodes = list(nodes)
    if len(nodes) <= 1:
        return 0.0
    in_tree, total = {nodes[0]}, 0.0
    edges = [(dist(cities[nodes[0]], cities[n]), n) for n in nodes[1:]]
    heapq.heapify(edges)
    while edges and len(in_tree) < len(nodes):
        c, n = heapq.heappop(edges)
        if n in in_tree:
            continue
        in_tree.add(n); total += c
        for m in nodes:
            if m not in in_tree:
                heapq.heappush(edges, (dist(cities[n], cities[m]), m))
    return total

def heuristic(cities, current, unvisited):
    """MST(unvisited) + cheapest link from current + cheapest link back to start (admissible)."""
    if not unvisited:
        return dist(cities[current], cities[0])
    return (mst_cost(cities, unvisited)
            + min(dist(cities[current], cities[u]) for u in unvisited)
            + min(dist(cities[0], cities[u]) for u in unvisited))

MAX_CITIES = 12   # A* over (city, visited-set) states grows like n * 2^n; see README note below

def a_star_tsp(cities):
    """Optimal TSP tour by A*. Returns (tour, length).

    A node is either a partial tour (f = g + h) or a COMPLETED tour, i.e. every city visited
    AND the closing edge back to city 0 already added (f = g = true tour length).
    A tour is returned only when a completed-tour node is popped, so every other node
    still queued has f >= its cost. With an admissible h that guarantees optimality.
    """
    n = len(cities)
    if n < 2:
        raise ValueError("Need at least 2 cities.")
    if n > MAX_CITIES:
        raise ValueError(f"A* TSP is limited to {MAX_CITIES} cities (got {n}).")

    counter = 0                                   # tie-breaker for the heap
    best_g = {(0, frozenset([0])): 0.0}
    # entry: (f, tie, g, city, path, is_complete)
    open_list = [(heuristic(cities, 0, set(range(1, n))), counter, 0.0, 0, [0], False)]
    while open_list:
        f, _, g, cur, path, complete = heapq.heappop(open_list)
        if complete:                              # goal test: a finished, closed tour
            return path, g
        visited = frozenset(path)
        if g > best_g.get((cur, visited), float("inf")):
            continue                              # stale entry
        unvisited = set(range(n)) - visited
        if not unvisited:                         # all cities visited -> close the tour
            total = g + dist(cities[cur], cities[0])
            counter += 1
            heapq.heappush(open_list, (total, counter, total, 0, path + [0], True))
            continue
        for nxt in unvisited:
            ng = g + dist(cities[cur], cities[nxt])
            state = (nxt, visited | {nxt})
            if ng < best_g.get(state, float("inf")):
                best_g[state] = ng
                rest = unvisited - {nxt}
                h = heuristic(cities, nxt, rest)  # rest empty -> distance back to start
                counter += 1
                heapq.heappush(open_list, (ng + h, counter, ng, nxt, path + [nxt], False))
    return None, None


class App:
    def __init__(self,root):
        self.root=root;root.title('Experiment 7 - TSP using A*');root.geometry('850x670')
        self.cities=[];self.busy=False
        controls=tk.Frame(root);controls.pack(pady=7)
        tk.Label(controls,text='Number of cities (2-12):').pack(side='left')
        self.count=tk.Entry(controls,width=5);self.count.insert(0,'5');self.count.pack(side='left',padx=5)
        tk.Button(controls,text='Create Input Fields',command=self.make_fields).pack(side='left',padx=3)
        tk.Button(controls,text='Random Cities',command=self.random_cities).pack(side='left',padx=3)
        self.solve_button=tk.Button(controls,text='Solve TSP',command=self.solve);self.solve_button.pack(side='left',padx=3)
        tk.Button(controls,text='Reset',command=self.reset).pack(side='left',padx=3)
        tk.Button(controls,text='Exit',command=root.destroy).pack(side='left',padx=3)
        self.field_frame=tk.Frame(root);self.field_frame.pack(pady=5)
        self.fields=[]
        self.result=tk.Label(root,text='Enter city coordinates or generate random cities',wraplength=820)
        self.result.pack(pady=5)
        self.fig=Figure(figsize=(7,4.4));self.ax=self.fig.add_subplot(111)
        self.canvas=FigureCanvasTkAgg(self.fig,master=root);self.canvas.get_tk_widget().pack(fill='both',expand=True,padx=10,pady=5)
        self.make_fields()
    def city_count(self):
        try:n=int(self.count.get())
        except ValueError:raise ValueError('Enter a whole number of cities.')
        if not 2<=n<=MAX_CITIES:raise ValueError(f'City count must be 2-{MAX_CITIES}.')
        return n
    def make_fields(self):
        try:n=self.city_count()
        except ValueError as exc:messagebox.showerror('Input error',str(exc));return
        for child in self.field_frame.winfo_children():child.destroy()
        self.fields=[];self.cities=[]
        for i in range(n):
            row,col=divmod(i,4)
            group=tk.Frame(self.field_frame);group.grid(row=row,column=col,padx=8,pady=3)
            tk.Label(group,text=f'City {i}:').pack(side='left')
            x=tk.Entry(group,width=5);x.pack(side='left',padx=2)
            y=tk.Entry(group,width=5);y.pack(side='left',padx=2)
            self.fields.append((x,y))
        self.clear_plot();self.result.config(text='Enter X and Y for each city, then click Solve TSP.')
    def read_cities(self):
        if len(self.fields)!=self.city_count():raise ValueError('Click Create Input Fields after changing city count.')
        try:points=[(float(x.get()),float(y.get())) for x,y in self.fields]
        except ValueError:raise ValueError('Enter valid numeric X and Y coordinates for every city.')
        if any(not math.isfinite(v) for point in points for v in point):raise ValueError('Coordinates must be finite numbers.')
        return points
    def random_cities(self):
        try:
            if len(self.fields)!=self.city_count():self.make_fields()
            for x,y in self.fields:
                x.delete(0,'end');x.insert(0,str(random.randint(0,100)))
                y.delete(0,'end');y.insert(0,str(random.randint(0,100)))
            self.cities=self.read_cities();self.plot(self.cities)
            self.result.config(text=f'{len(self.cities)} random cities generated. Click Solve TSP.')
        except ValueError as exc:messagebox.showerror('Input error',str(exc))
    def clear_plot(self):
        self.ax.clear();self.ax.set_xlabel('X');self.ax.set_ylabel('Y');self.canvas.draw()
    def plot(self,cities,path=None,total=None):
        self.ax.clear()
        for i,(x,y) in enumerate(cities):
            self.ax.scatter(x,y,c='green' if i==0 else 'blue',s=55)
            self.ax.annotate(str(i),(x,y),xytext=(5,5),textcoords='offset points')
        if path:
            for a,b in zip(path,path[1:]):
                p,q=cities[a],cities[b]
                self.ax.plot([p[0],q[0]],[p[1],q[1]],'r-',linewidth=2)
        self.ax.set_title('TSP route' + (f' - Distance: {total:.2f}' if total is not None else ''))
        self.ax.set_xlabel('X');self.ax.set_ylabel('Y');self.ax.grid(alpha=.25);self.canvas.draw()
    def solve(self):
        if self.busy:return
        try:self.cities=self.read_cities()
        except ValueError as exc:messagebox.showerror('Input error',str(exc));return
        self.busy=True;self.solve_button.config(state='disabled');self.result.config(text='Solving, please wait...')
        points=list(self.cities)
        def worker():
            begin=time.perf_counter()
            try:answer=a_star_tsp(points);error=None
            except Exception as exc:answer=None;error=str(exc)
            elapsed=time.perf_counter()-begin
            self.root.after(0,lambda:self.finished(points,answer,elapsed,error))
        threading.Thread(target=worker,daemon=True).start()
    def finished(self,points,answer,elapsed,error):
        self.busy=False;self.solve_button.config(state='normal')
        if error:messagebox.showerror('Error',error);self.result.config(text=error);return
        path,total=answer
        if path:
            self.plot(points,path,total)
            self.result.config(text=f'Tour: {" → ".join(map(str,path))} | Distance: {total:.2f} | Time: {elapsed:.3f}s')
        else:self.result.config(text='No solution found')
    def reset(self):
        if self.busy:
            messagebox.showinfo('Busy','Wait for the current search to finish.');return
        self.make_fields()

if __name__=='__main__':
    root=tk.Tk();App(root);root.mainloop()
