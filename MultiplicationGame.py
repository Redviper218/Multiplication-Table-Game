
from random import randrange,shuffle
from tkinter import *


def operations_generator():
	numbers1  = [str(i) for i in range(2,10)]
	numbers2 = [str(i) for i in range(2,10)]

	ops = []
	for i in range(len(numbers1)):
		a = numbers1[i]
		
		for j in range(len(numbers2)):
			b = numbers2[j]
			op = a+' x '+b + ' = '
			ops.append((op,int(a)*int(b)))
	return ops

OPERATIONS = operations_generator()
shuffle(OPERATIONS)
shuffle(OPERATIONS)

class Timer:
	def __init__(self,root,var,duration,step,reverse = True):
		self.root = root;
		self.var = var
		self.duration = duration
		self.step = step
		self.done = False
		self.when_finished = None

	def stop(self):
		self.done = True 
	def initiate(self):
		self.counter = self.duration 
		self.root.after(self.step,self.update)
	def update(self):
		if self.done:
			return
		self.counter -= self.step
		if self.counter <= 0:
			self.var.set(str('0'))
			self.done = True
			if self.when_finished:
				self.when_finished()
			return
		self.root.after(self.step,self.update)
		x = round(self.counter/1000,2)
		a = len(str(int(x)))+1
		x = str(x)

		if len(x) < a+2 :x = x + ''.join(['0']*(a+2-len(x)))
		self.var.set(str(x))

class App:
	response_time = 10
	timer_step = .01
	current_op_index = -1
	timer = None
	right_answers_counter = 0
	all_answers_counter = 0

	def __init__(self, root):
		
		self.root = root

		timer_frame = LabelFrame(root,text='Timer', pady=0);
		timer_frame.pack(fill = 'x',padx=5)

		timer_var = StringVar() ;timer_var.set(str(self.response_time))
		timer_label = Label(timer_frame,textvariable = timer_var,font=("Arial", 35))
		timer_label.pack()
		def update_response_timer():
			timer_var.set(self.response_time)

		op_frame = LabelFrame(root,text='Operation', pady=0);
		op_frame.pack(fill = 'x',padx=5)


		op_var = StringVar();op_var.set('? x ? = ')
		op_label = Label(op_frame,textvariable = op_var,font=("Arial", 35,'bold'))
		op_label.pack(side = 'left',pady = 10)
		
		inp_var = StringVar();inp_var.set('??')
		
		def inp_var_check(var):
			text = var.get()
			if len(text) >2:
				text = text[:2]
			for c in text:
				if not c.isdigit():
					text = text.replace(c,'')
			var.set(text)
			

		inp_var.trace_add('write',lambda *args:inp_var_check(inp_var))
		inp_entree = Entry(op_frame,textvariable = inp_var,font=("Arial", 35,'bold'),width = 4)
		inp_entree.pack(side = 'left',expand = 'no',padx = 5)
		def inp_entree_disable():
			inp_entree['state'] = 'disabled'
		def inp_entree_enable():
			inp_entree['state'] = 'normal'

		start_button =  StringVar();start_button.set('Start')
		start_button = Button(root,textvariable =start_button ,font=("Arial", 25),bg = '#B6219B')
		start_button.pack(fill = 'x',padx=5,pady = 5,)
		
		def start_button_command():
			#  Display the next operation
			if self.timer:
				if not self.timer.done:
					return
			on_start_animation()
			if self.current_op_index == len(OPERATIONS)-1:
				self.current_op_index = -1
				shuffle(OPERATIONS)
			self.current_op_index +=1 
			
			self.all_answers_counter += 1

			op,result = OPERATIONS[self.current_op_index]
			op_var.set(op)
			inp_var.set('')
			inp_entree.focus()
			
			
			if self.timer :
				self.timer.stop()
			if inp_entree['state'] == 'disabled':
				inp_entree_enable() 
			# Start the timer
			
			self.timer = Timer(root,timer_var,self.response_time*1000,int(self.timer_step*1000)) #(self,root,var,duration,step,reverse = True):
			self.timer.when_finished = check_button_command
			self.timer.initiate()
			
		start_button.configure(command = start_button_command) 


		check_button =  StringVar();check_button.set('check')
		check_button = Button(root,textvariable =check_button ,font=("Arial", 25),bg = '#00AE70')
		check_button.pack(fill = 'x',padx=5,pady = 5,)
		
		def on_start_animation():
			print()
			op_frame.configure(bg = '#F0F0F0')
			op_label.configure(bg = '#F0F0F0')

		def on_right_answer_animation():
			print('yes')
			op_frame.configure(bg = '#00FF8E')
			op_label.configure(bg = '#00FF8E')
		def on_wrong_answer_animation():
			print('no')
			op_frame.configure(bg = '#FF5456')
			op_label.configure(bg = '#FF5456')

		def check_button_command():
			if not self.timer:
				return
			if not self.timer.done:
				self.timer.stop()
			inp_entree_disable()
			op,result = OPERATIONS[self.current_op_index]
			user_input = str(inp_var.get())
			if not user_input:
				user_input = -1
			try:
				int(user_input)
			except:
				user_input = -1
			if int(user_input) == int(result):
				self.right_answers_counter += 1 
				on_right_answer_animation()
			else:
				on_wrong_answer_animation()

		check_button.configure(command = check_button_command) 
		
		def func2(event):
			if self.timer:
				if self.timer.done :
					start_button_command()
				else:
					check_button_command()
			else:
				start_button_command()
		root.bind('<Return>', func2)
		def Settings_Popup():
			#Create a Toplevel window
			top= Toplevel(root)
			x = root.winfo_x()
			y = root.winfo_y()
			top.geometry("200x100+%d+%d" % (x + 50, y + 120))
			#Create an Entry Widget in the Toplevel window
			l = LabelFrame(top,text = 'Settings')
			l.pack(fill = 'both',padx=5,pady=0,expand = 'yes')
			def entry_var_check(var):
				text = var.get()
				for c in text:
					if not c.isdigit():
						text = text.replace(c,'')
				var.set(text)
			entry_var = StringVar()
			entry_var.set(self.response_time)
			entry_var.trace_add('write',lambda *args:entry_var_check(entry_var))
			entry= Entry(l, width= 25,textvariable = entry_var)
			entry.place(relwidth = 0.4,relx = 0.92,anchor = 'ne')
			label = Label(l,text='Timer Duration:', pady=0)
			label.place(relx = 0,anchor = 'nw')
			def on_save_button(*args):
				val = entry_var.get()
				if val:
					self.response_time = int(val)
					update_response_timer()
				top.destroy()
			save_button= Button(top, text="Ok", command=on_save_button)
			save_button.pack(side = 'right',padx=5,pady=2)
			top.update()
			top.minsize(top.winfo_width(), top.winfo_height()+10)
			top.bind('<Return>', on_save_button)
			top.title("Settings")

		def SolutionPopup():
			#Create a Toplevel window
			top= Toplevel(root)
			top.title('Solution')
			x = root.winfo_x()
			y = root.winfo_y()
			top.geometry("200x100+%d+%d" % (x + 50, y + 120))

			op,result = OPERATIONS[self.current_op_index]
			solution = op + str(result)
			font = ('Arial',25,'bold')
			fg = '#00AE70'
			if not self.timer:
				solution = 'Start The Game First'
				fg = '#FF5456'
				font = ('Arial',13,'bold')

			elif not self.timer.done:
				solution = 'Don\' cheat !!'
				fg = '#FF5456'
				font = ('Arial',13,'bold')

			l = LabelFrame(top,text = 'Solution')
			l.pack(fill = 'both',padx = 5,pady= 5)
			label = Label(l,text = solution,font = font ,fg = fg)
			label.pack(pady = 10)
			top.update()
			top.minsize(top.winfo_width(), top.winfo_height()+10)
			top.bind('<Return>', lambda *arg:top.destroy())
			top.title("Solution")

		def AboutPopup():
			#Create a Toplevel window
			top= Toplevel(root)
			top.title('Solution')
			x = root.winfo_x()
			y = root.winfo_y()
			top.geometry("200x100+%d+%d" % (x + 50, y + 120))

			font = ('Arial',15,'bold')
			
			l = LabelFrame(top,text = '')
			l.pack(fill = 'both',padx = 5,pady= 5)
			label = Label(l,text = 'Made for Fun ',font = font ,fg = '#00AE70')
			label.pack(pady = 10)

			label = Label(l,text = 'by Redviper ',font = font ,fg = '#FF5456')
			label.pack(pady = 10)
			top.update()
			top.minsize(top.winfo_width(), top.winfo_height()+10)
			top.bind('<Return>', lambda *arg:top.destroy())
			top.title("About...")

		
		menubar = Menu(root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Settings", command=Settings_Popup)
		#filemenu.add_command(label="Open", command=donothing)
		#filemenu.add_command(label="Save", command=donothing)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=root.quit)
		menubar.add_cascade(label="File", menu=filemenu)

		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Help Solution", command=SolutionPopup)
		helpmenu.add_command(label="About...", command=AboutPopup)
		menubar.add_cascade(label="Help", menu=helpmenu)

		root.config(menu=menubar)
		root.title("Multiplication Game")






root = Tk()

app = App(root)

root.eval('tk::PlaceWindow . center')
root.update()
root.minsize(root.winfo_width(), root.winfo_height()+10)

root.mainloop() 