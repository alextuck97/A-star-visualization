from functools import partial
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from A_star_search import *
from graph import *
from time import sleep

class App:
    def __init__(self):
        self.a_star = AStarSearch()
        self.graph = Graph()

        self.parameters = {}
       
        self.master = tk.Tk()
        self.master.title("A* visualization")
        #self.master.geometry("400x200")
        self.img = tk.PhotoImage()
        button_frame = tk.Frame(self.master)
        
        size = tk.Label(button_frame, text="Size: ")
        size.grid(row=0,column=0)
        size_entry = tk.Entry(button_frame, width = 10)
        size_entry.insert(tk.END,"5")
        self.parameters["Size"] = size_entry
        size_entry.grid(row=0,column=1)

        btn_resize = tk.Button(button_frame, text="Resize", command=lambda: self.resize(int(size_entry.get())))
        btn_resize.grid(row=1,column=0)

        btn_place_start = tk.Button(button_frame, text="Place Start",  width=20, command=self.placeStart)
        btn_place_start.grid(row=2,columnspan=2, pady=10)

        btn_place_end = tk.Button(button_frame, text="Place End",  width=20, command=self.placeEnd)
        btn_place_end.grid(row=3,columnspan=2, pady=10)

        #btn_place_barriers = tk.Button(button_frame, text="Place Barriers", width=20, command=self.placeBarriers)
        #btn_place_barriers.grid(row=4,columnspan=2,pady=10)

        heuristic_label = tk.Label(button_frame, text="Heuristic: ")
        options = ["City Block", "Euclidean"]
        variable = tk.StringVar(button_frame)
        variable.set(options[0])
        heuristic_menu = tk.OptionMenu(button_frame, variable, *options)
        self.parameters["Heuristic"]=heuristic_menu
        heuristic_menu.config(width=8)
        #heuristic_combobox = ttk.Combobox(button_frame)
        #heuristic_combobox['values'] = ("City Block", "Euclidean")
        #heuristic_combobox.current(0)
        heuristic_label.grid(row=4,column=0,pady=10)
        heuristic_menu.grid(row=4,column=1,pady=10)

        btn_clear = tk.Button(button_frame, text="Clear", width=20, command=self.clearPath)
        btn_clear.grid(row=5,columnspan=2,pady=10)

        btn_clear_all = tk.Button(button_frame, text="Clear All", width=20,command=self.clearGraph)
        btn_clear_all.grid(row=6,columnspan=2,pady=10)

        btn_go = tk.Button(button_frame, text="Go!", width=20, command=lambda: self.go(heuristic_menu.getvar))
        btn_go.grid(row=7, columnspan=2,pady=10)

        button_frame.grid(row=0,column=0, padx=2)

        self.graph_frame = tk.Frame(self.master)
        self.graph_buttons = self.buildGraphFrame()
        self.graph_frame.grid(row=0,column=1)
        
    


    def run(self):
        self.master.mainloop()

    

    def placeStart(self):
        self.disableButtons()

        size = self.graph.size

        for i in range(size):
            for j in range(size):
                self.graph_buttons[i][j].configure(command = partial(self.colorButtonEndOrStart, (i,j), Spaces.START))
            


    def placeEnd(self):
        self.disableButtons()

        size = self.graph.size

        for i in range(size):
            for j in range(size):
                self.graph_buttons[i][j].configure(command = partial(self.colorButtonEndOrStart, (i,j), Spaces.END))

        
    def colorButtonEndOrStart(self, position, endorstart):
        result = self.graph.setEndPoint(position, endorstart)

        if result == 1:
            
            if endorstart == Spaces.END:
                self.graph_buttons[position[0]][position[1]].configure(bg="red")
            elif endorstart == Spaces.START:
                self.graph_buttons[position[0]][position[1]].configure(bg="green")
            self.enableBarrierToggles()
            self.enableButtons()
            

    def enableButtons(self):
        for c in self.master.winfo_children()[0].winfo_children():
                c.configure(state="normal")
    
    def disableButtons(self):
        for c in self.master.winfo_children()[0].winfo_children():
                c.configure(state="disable")


    def placeBarriers(self):
        pass


    def toggleBarrier(self, position):
        res = self.graph.toggleBarrier(position)

        if res == 0:
            self.graph_buttons[position[0]][position[1]].configure(bg="tan")
        elif res == 1:
            self.graph_buttons[position[0]][position[1]].configure(bg="gray")
        elif res == -1:
            pass


    def clearGraph(self):
        self.graph.resetMatrix()
        size = self.graph.size

        for i in range(size):
            for j in range(size):
                if i == 0 and j == 0:
                    self.graph_buttons[i][j].configure(bg="green")
                elif i == size-1 and j == size-1:
                    self.graph_buttons[i][j].configure(bg="red")
                else:
                    self.graph_buttons[i][j].configure(bg="tan")


    def clearPath(self):
        size = self.graph.size
        for i in range(size):
            for j in range(size):
                if self.graph.getPosition(i,j) == Spaces.START:
                    self.graph_buttons[i][j].configure(bg="green")
                elif self.graph.getPosition(i,j) == Spaces.END:
                    self.graph_buttons[i][j].configure(bg="red")
                elif self.graph.getPosition(i,j) == Spaces.BARRIER:
                    self.graph_buttons[i][j].configure(bg="gray")
                else:
                    self.graph_buttons[i][j].configure(bg="tan") 


    def go(self, heuristic):
        
        
        if heuristic == "Euclidean":
            h = EuclideanHeuristic
        else:
            h = CityBlockHeuristic
        self.a_star.setGraph(self.graph.matrix)
        self.a_star.setHeuristic(h)

        self.a_star.startSearch(self.graph.start, self.graph.end)

        n = None

        while n == None:
            n = self.a_star.iterateSearch(self.graph.end)
            self.colorExploredSet(self.a_star.explored_set)
            self.master.update_idletasks()
            sleep(0.2)
            

        if n == TERMINATE:
            pass
        else:
            self.colorPath(n, self.graph.start, self.graph.end)
        self.a_star.clearSearch()


    def colorExploredSet(self, explored_set):

        for n in explored_set:
            x = n.position[0]
            y = n.position[1]

            self.graph_buttons[x][y].configure(bg="blue")


    def colorPath(self, node, start, end):
        while node != None:
            x = node.position[0]
            y = node.position[1]
            self.graph_buttons[x][y].configure(bg="orange")
            node = node.parent
        
        self.graph_buttons[start[0]][start[1]].configure(bg="green")
        self.graph_buttons[end[0]][end[1]].configure(bg="red")

    def resize(self, new_size):
        if new_size > MAX_SIZE or new_size < MIN_SIZE:
            messagebox.showerror("Size error", f"Input size must be {MIN_SIZE} <= size <= {MAX_SIZE}.")
        else:
            self.graph.resizeMatrix(new_size)
            self.graph_frame.destroy()
            self.graph_frame = tk.Frame(self.master)
            self.graph_buttons = self.buildGraphFrame()
            self.graph_frame.grid(row=0,column=1)

    def buildGraphFrame(self):
        size = self.graph.size

        buttons = []
        

        for i in range(size):
            buttons.append([])
            for j in range(size):

                square_button = tk.Button(self.graph_frame, image=self.img)
                
                if self.graph.getPosition(i,j) == Spaces.START:
                    square_button.configure(bg="green")
                elif self.graph.getPosition(i,j) == Spaces.END:
                    square_button.configure(bg="red")
                elif self.graph.getPosition(i,j) == Spaces.BARRIER:
                    square_button.configure(bg="gray", command=partial(self.toggleBarrier, (i,j)))
                else:
                    square_button.configure(bg="tan", command=partial(self.toggleBarrier, (i,j)))

                square_button.config(width=150/ size, height = 150 /size)
                square_button.grid(column=j,row=i)
                buttons[i].append(square_button)
        
        return buttons
    

    def enableBarrierToggles(self):
        size = self.graph.size
        for i in range(size):
            for j in range(size):
                if self.graph.getPosition(i,j) == Spaces.START:
                    self.graph_buttons[i][j].configure(bg="green")
                elif self.graph.getPosition(i,j) == Spaces.END:
                    self.graph_buttons[i][j].configure(bg="red")
                elif self.graph.getPosition(i,j) == Spaces.BARRIER:
                    self.graph_buttons[i][j].configure(bg="gray", command=partial(self.toggleBarrier, (i,j)))
                else:
                    self.graph_buttons[i][j].configure(bg="tan", command=partial(self.toggleBarrier, (i,j)))
        


                