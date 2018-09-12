import Tkinter as Tk

class mainthing(Tk.Frame):
   def __init__(self,parent):
      Tk.Frame.__init__(self, parent)
      self.parent = parent
      self.initialize()

   def initialize(self):

      self.parent.title("RUN ON START TEST")
      self.parent.grid_rowconfigure(0,weight=1)
      self.parent.grid_columnconfigure(0,weight=1)
      self.parent.config(background="red")

      self.frame = Tk.Frame(self.parent)
      self.frame.pack(fill=Tk.X, padx=5, pady=5)

      self.topEntry = Tk.Entry(self.frame, bg = "#006600", fg = "#00ff00")
      self.topEntry.grid(column=0, row=1, sticky="ew")


      yesBut = Tk.Button(self.frame, text="Yes")
      yesBut.grid(column=1, row=1)

      query = Tk.Label(self.frame, fg="#00ff00", bg="#001a00", anchor="w")
      query.grid(column=1, row=0, columnspan=2, sticky="ew")


if __name__ == "__main__":
   root=Tk.Tk()
   app = mainthing(root)
   root.mainloop()
