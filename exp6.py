"""Experiment 6: Means-End Analysis, x-first then y; obstacle-free grid."""
import tkinter as tk
from tkinter import messagebox

def mea_path(start,goal):
    x,y=start;path=[start]
    while (x,y)!=goal:
        if x!=goal[0]:x+=1 if goal[0]>x else -1
        elif y!=goal[1]:y+=1 if goal[1]>y else -1
        path.append((x,y))
    return path

class App:
    def __init__(self,root):
        self.root=root;root.title('Experiment 6 - Robot Traversal')
        form=tk.Frame(root);form.pack(pady=8)
        self.entries={}
        for col,(label,default) in enumerate([('Grid size',10),('Start X',2),('Start Y',3),('Goal X',5),('Goal Y',7)]):
            tk.Label(form,text=label).grid(row=0,column=col,padx=4)
            e=tk.Entry(form,width=8);e.insert(0,str(default));e.grid(row=1,column=col,padx=4);self.entries[label]=e
        buttons=tk.Frame(root);buttons.pack(pady=6)
        tk.Button(buttons,text='Start',command=self.start).pack(side='left',padx=4)
        tk.Button(buttons,text='Reset',command=self.reset).pack(side='left',padx=4)
        tk.Button(buttons,text='Exit',command=root.destroy).pack(side='left',padx=4)
        self.canvas=tk.Canvas(root,width=500,height=500,bg='white');self.canvas.pack(padx=10)
        self.info=tk.Label(root,text='Enter coordinates and click Start',wraplength=550);self.info.pack(pady=8)
        self.after_id=None;self.path=[];self.index=0
        self.reset()
    def inputs(self):
        vals={k:int(v.get()) for k,v in self.entries.items()}
        n=vals['Grid size'];start=(vals['Start X'],vals['Start Y']);goal=(vals['Goal X'],vals['Goal Y'])
        if not 2<=n<=20 or any(not (0<=v<n) for v in start+goal):
            raise ValueError('Grid size must be 2-20 and coordinates must be between 0 and size-1.')
        return n,start,goal
    def draw(self,n,start,goal,robot):
        self.canvas.delete('all');cell=500/n
        for i in range(n+1):
            self.canvas.create_line(i*cell,0,i*cell,500,fill='gray')
            self.canvas.create_line(0,i*cell,500,i*cell,fill='gray')
        for pos,color in [(start,'green'),(goal,'red'),(robot,'blue')]:
            x,y=pos;pad=cell*.2
            self.canvas.create_rectangle(x*cell+pad,y*cell+pad,(x+1)*cell-pad,(y+1)*cell-pad,fill=color,outline='black')
    def reset(self):
        if self.after_id is not None:self.root.after_cancel(self.after_id);self.after_id=None
        self.path=[];self.index=0
        try:n,start,goal=self.inputs();self.draw(n,start,goal,start)
        except ValueError:self.canvas.delete('all')
        self.info.config(text='Enter coordinates and click Start')
    def start(self):
        self.reset()
        try:self.n,self.start_pos,self.goal_pos=self.inputs()
        except ValueError as exc:messagebox.showerror('Input error',str(exc));return
        self.path=mea_path(self.start_pos,self.goal_pos);self.advance()
    def advance(self):
        self.after_id=None
        pos=self.path[self.index];self.draw(self.n,self.start_pos,self.goal_pos,pos)
        self.info.config(text=f'Position: {pos} | Move {self.index}/{len(self.path)-1} | Path: {self.path}')
        if self.index<len(self.path)-1:
            self.index+=1;self.after_id=self.root.after(400,self.advance)
        else:self.info.config(text=f'Goal reached at {pos}! Total moves: {len(self.path)-1} | Path: {self.path}')

if __name__=='__main__':
    root=tk.Tk();App(root);root.mainloop()
