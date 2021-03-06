from tkinter import *
from connect import Database
database = Database("database.db")

class App:
    def __init__(self):
        #! Initialization 
        self.root = Tk()
        self.root.title('To Do Planner')
        self.selected_string = ''
        
        #! Toggle between fullscreen and quit 
        self.fullScreenState = True
        self.root.attributes("-fullscreen", self.fullScreenState)
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (self.w, self.h))
        self.root.bind("<F11>", self.toggleFullScreen)
        self.root.bind("<Escape>", self.quit)
        
        #! Title
        title = Label(self.root,text='TO DO PLANNER',bd=10,relief=GROOVE,font=('times new roman',40,'bold'),bg='darkblue',fg='white')
        title.pack(side=TOP,fill=X)

        #! Enter todo list
        self.lbl_enter = Label(self.root, text="Enter what do you plan to do:",font=("Times", "14", "bold"))
        self.lbl_enter.place(x=10,y=100)

        self.enter_text = StringVar()
        self.enter_text.trace('w', self.character_limit)

        self.entry_enter = Entry(self.root, textvariable=self.enter_text, width=50, fg='dark blue', font=("Times", "14"))
        self.entry_enter.place(x=300,y=100)
        
        #! Add button
        self.button_add = Button(self.root, text='Add', width=15, activebackground='white', relief=RIDGE,bg='darkblue',fg='white',
                                    font=("Times", "14", "italic bold"), cursor='hand2', command=self.add_command)
        self.button_add.place(x=850,y=100)
        
        #! Update button
        self.button_update = Button(self.root, text='Update', width=15, activebackground='white', relief=RIDGE,bg='darkblue',fg='white',
                                    font=("Times", "14", "italic bold"), cursor='hand2',command=self.update_selected)
        self.button_update.place(x=1075,y=100)
        
        #! Refresh button
        self.button_refresh = Button(self.root, text='Refresh', width=15, activebackground='white', relief=RIDGE,bg='darkblue',fg='white',
                                    font=("Times", "14", "italic bold"), cursor='hand2',command=self.refresh_text)
        self.button_refresh.place(x=1300,y=100)
        
        #! To do list 
        self.lbl_todo = Label(self.root, text="To do",font=("Times", "14", "bold"))
        self.lbl_todo.place(x=220,y=170)
        self.todo_list = Listbox(self.root, width=60,height=25, fg='dark blue', font=("Times", "12"), selectmode=SINGLE)
        self.todo_list.place(x=10,y=200)
        self.view_todo_command()
        self.todo_list.bind('<<ListboxSelect>>', self.get_selected_row_from_todo)
        
        #! Doing list 
        self.lbl_doing = Label(self.root, text="Doing",font=("Times", "14", "bold"))
        self.lbl_doing.place(x=745,y=170)
        self.doing_list = Listbox(self.root, width=60,height=25, fg='dark blue', font=("Times", "12"), selectmode=SINGLE)
        self.doing_list.place(x=525,y=200)
        self.view_doing_command()
        self.doing_list.bind('<<ListboxSelect>>', self.get_selected_row_from_doing)
        
        #! Done list 
        self.lbl_done = Label(self.root, text="Done",font=("Times", "14", "bold"))
        self.lbl_done.place(x=1260,y=170)
        self.done_list = Listbox(self.root, width=60,height=25, fg='dark blue', font=("Times", "12"), selectmode=SINGLE)
        self.done_list.place(x=1040,y=200)
        self.view_done_command()
        self.done_list.bind('<<ListboxSelect>>', self.get_selected_row_from_done)
        
        #! Push to doing button
        self.button_push_doing = Button(self.root, text='Push to doing', width=43, activebackground='white', relief=RIDGE,bg='darkblue',fg='white',
                                    font=("Times", "14", "italic bold"), cursor='hand2',command=self.push_doing_command)
        self.button_push_doing.place(x=10,y=720)
        
        #! Push to done button
        self.button_push_done = Button(self.root, text='Push to done', width=43, activebackground='white', relief=RIDGE,bg='darkblue',fg='white',
                                    font=("Times", "14", "italic bold"), cursor='hand2',command=self.push_done_command)
        self.button_push_done.place(x=525,y=720)
        
        #! delete button
        self.button_delete = Button(self.root, text='Delete', width=43, activebackground='white', relief=RIDGE,bg='darkblue',fg='white',
                                    font=("Times", "14", "italic bold"), cursor='hand2',command=self.delete_command)
        self.button_delete.place(x=1040,y=720)

        #! Info Keys log
        self.lblInstruction = Label(self.root,text="F11 - Toggle Fullscreen , Escape - Quit",bg="darkblue",fg="white",
                                font=('times new roman',15,'bold'),bd=5,relief=GROOVE)
        self.lblInstruction.pack(side=BOTTOM,fill=X)

        #! Mainloop
        self.root.mainloop()
        
    #! To toggle FullScreen
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)
    
    #! to quit
    def quit(self, event):
        self.root.quit()
        
    #! Limiting text 
    def character_limit(self, *args):
        value = self.enter_text.get()
        if len(value) > 70 and len(value) < 0:
            self.enter_text.set(value[:70])
        
    #! add list    
    def add_command(self):
        database.insert(self.enter_text.get())
        self.todo_list.delete(0, END)
        self.todo_list.insert(END, self.enter_text.get())
        self.todo_list.delete(0, END)
        self.refresh_text()
        
    #! clear text
    def refresh_text(self):
        self.entry_enter.delete(0, END)
        self.view_todo_command()
        self.view_doing_command()
        self.view_done_command()
        
    #! display todo lists
    def view_todo_command(self):
        self.todo_list.delete(0, END)
        for row in database.view_todo():
            row = str(row[0]) + '. ' + ''.join(row[1:])
            self.todo_list.insert(END, row)
            
    #! display doing lists
    def view_doing_command(self):
        self.doing_list.delete(0, END)
        for row in database.view_doing():
            row = str(row[0]) + '. ' + ''.join(row[1:])
            self.doing_list.insert(END, row)
            
    #! display done lists
    def view_done_command(self):
        self.done_list.delete(0, END)
        for row in database.view_done():
            row = str(row[0]) + '. ' + ''.join(row[1:])
            self.done_list.insert(END, row)

    #! select the row from the todo list by click
    def get_selected_row_from_todo(self, event):
        try:
            index = self.todo_list.curselection()
            if index:
                self.selected_string = self.todo_list.get(index)
                self.entry_enter.delete(0, END)
                self.entry_enter.insert(END, self.stripPrimaryKey(self.selected_string))
        except IndexError:
            pass
        
    #! select the row from the doing list by click
    def get_selected_row_from_doing(self, event):
        try:
            index = self.doing_list.curselection()
            if index:
                self.selected_string = self.doing_list.get(index)
                self.entry_enter.delete(0, END)
                self.entry_enter.insert(END, self.stripPrimaryKey(self.selected_string))
        except IndexError:
            pass
        
    #! select the row from the done list by click
    def get_selected_row_from_done(self, event):
        try:
            index = self.done_list.curselection()
            if index:
                self.selected_string = self.done_list.get(index)
                self.entry_enter.delete(0, END)
                self.entry_enter.insert(END, self.stripPrimaryKey(self.selected_string))
        except IndexError:
            pass
    
    #! get primary key from which we selected
    def getPrimaryKey(self,string):
        dotPos = string.find('. ')
        primaryKey = string[0:dotPos]
        return primaryKey

    #! get text from which we selected
    def stripPrimaryKey(self,string):
        separation_token = '. '
        dotPos = string.find(separation_token)
        return string[dotPos + len(separation_token):]
    
    #! update the text in list
    def update_selected(self):
        try:
            if len(self.enter_text.get()) > 1:
                database.update(self.getPrimaryKey(self.selected_string), self.enter_text.get())
        except NameError:
            pass
        self.refresh_text()
    
    #! delete the text in list
    def delete_command(self):
        try:
            database.delete(self.getPrimaryKey(self.selected_string))
        except NameError:
            pass
        self.refresh_text()
    
    #! Pusing the text into doing list    
    def push_doing_command(self):
        try:
            database.push_to_doing(self.getPrimaryKey(self.selected_string))
        except NameError:
            pass
        self.refresh_text()
        
    #! Pusing the text into done list    
    def push_done_command(self):
        try:
            database.push_to_done(self.getPrimaryKey(self.selected_string))
        except NameError:
            pass
        self.refresh_text()
    
if __name__ == '__main__':
    app = App()  