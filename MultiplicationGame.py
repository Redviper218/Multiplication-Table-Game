
from random import randrange,shuffle
import tkinter as tk
def make_dynamic(widget,uniform = False ,rows = None,columns = None):

	col_count,row_count = widget.grid_size()
	if rows == None:
		rows = range(row_count)
	for i in rows:
		widget.grid_rowconfigure(i, weight = 1, uniform = uniform)

	if columns  == None:
		columns = range(col_count)
	for i in columns:
		widget.grid_columnconfigure(i, weight = 1, uniform = uniform)



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
		if self.when_finished:
			self.when_finished()
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

class SettingMenuApp:
	def __init__(self,root):
		content = tk.Frame(root)
		if content:
			timer_frame = tk.LabelFrame(content,text = 'Timer')
			if timer_frame:
				f1 = tk.Frame(timer_frame)
				if f1:
					duration_label = tk.Label(f1,text = 'Duration : ',font = ('',14,'bold'))
					duration_entry = tk.Entry(f1,font = ('',14,'bold'),width = 8)
			
			save_button_frame = tk.Frame(content)
			save_button_frame.configure(highlightthickness = 1 ,highlightbackground = 'black')
			if save_button_frame:
				save_button = tk.Button(save_button_frame,text = 'Save')
				
		
		content.grid(sticky = 'nswe',padx = 5,pady = 5)
		
		timer_frame.grid(sticky = 'nsew')
		f1.grid(sticky = 'nw',pady = (0,5))
		duration_label.grid()
		duration_entry.grid(row = 0,column = 1,padx = (0,5))
		save_button_frame.grid(row = 1,column = 0,pady=(3,0),sticky = 'es')
		save_button.grid()
		make_dynamic(root)
		make_dynamic(content,rows = (0,))
		make_dynamic(timer_frame)

		#{{{{{{{{{self widget attributes}}}}}}}}}#
		self.duration_entry = duration_entry
		self.save_button = save_button
		self.root =root
		self.configure()
		self.root.update()
		self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
		self.root.bind('<Return>', lambda *args:self._save_button_command())
		self.root.title("Settings")

	def configure(self):
		self.duration_entry_var = tk.StringVar() 
		self.duration_entry.configure(textvariable = self.duration_entry_var)

		self.save_button.configure(command = self._save_button_command)
	def save_button_command(self):
		pass
	def _save_button_command(self):
		self.save_button_command()
		self.root.destroy()

class App:
	response_time = 4
	timer_step = .01
	current_op_index = -1
	timer = None
	right_answers_counter = 0
	all_answers_counter = 0

	start_button_bg = '#B6219B'
	start_button_activebackground = "#e882d6"

	check_button_bg = '#00AE70'
	check_button_activebackground = "#56e8b4"

	def __init__(self,root):

		content = tk.Frame(root)
		
		if content:

			timer_frame = tk.LabelFrame(content,text= 'Timer')
			if timer_frame:
				timer_label = tk.Label(timer_frame, text = '15',font =("Arial", 35,'bold'))
			
			operation_frame = tk.LabelFrame(content,text = 'Operation')
			if operation_frame:

				f1 = tk.Frame(operation_frame)
				if f1:
					operation_label = tk.Label(f1,text= '? x ? = ',font = ("Arial", 35,'bold'))
					operation_entry = tk.Entry(f1,width = 3,font = ("Arial", 35,'bold'))

			start_button = tk.Button(content,text = 'Start',font = ("Arial", 30,'bold'))
			start_button.configure(bg = '#B6219B',activebackground="#e882d6")
			check_button = tk.Button(content,text = 'Check',font = ("Arial", 30,'bold'))
			check_button.configure(bg = '#00AE70',activebackground="#56e8b4")

		
		content.grid(sticky = 'nswe',padx = 5,pady = 5)

		timer_frame.grid(sticky = 'nswe')
		timer_label.grid(sticky = '')

		operation_frame.grid(sticky = 'nswe',pady = (0,3))
		f1.grid(sticky = '',pady = (0,10))
		operation_label.grid(sticky = '')
		operation_entry.grid(row =0,column = 1,sticky = '',padx = (0,10))
		
		start_button.grid(sticky = 'nswe',pady=0)
		check_button.grid(sticky = 'nswe')
		
		make_dynamic(root)
		make_dynamic(content,rows = ())

		make_dynamic(timer_frame)
		make_dynamic(timer_label)

		make_dynamic(operation_frame,uniform = True)

		#{{{{{{{self widget attributes}}}}}}}#
		self.root = root
		self.operation_frame = operation_frame
		self.f1 = f1
		self.operation_entry = operation_entry
		self.operation_label = operation_label
		self.timer_label = timer_label
		self.start_button = start_button
		self.check_button = check_button
		self.timer = None
		
		self.configure_menubar()
		self.configure_widgets()

		#{{{{{{{{lauch the app}}}}}}}}
		self.root.update()
		self.root.minsize(self.root.winfo_width(), self.root.winfo_height()+10)
		self.root.mainloop()

	def set_response_time(self,val):
		if int(float(str(val))) == float(str(val)):
			val = int(float(str(val)))
		else:
			val = float(str(val))
		self.response_time = val
		if not self.timer:
			self.timer_label_var.set(val)
		print(val)

	def configure_menubar(self):
		menubar = tk.Menu(root)
		
		if menubar:
			filemenu = tk.Menu(menubar, tearoff=0)
			if filemenu:
				def settings_command(*args):
					top=tk.Toplevel(self.root)
					top.focus()
					x,y = root.winfo_x(),root.winfo_y() 
					topapp = SettingMenuApp(top)
					topapp.duration_entry_var.set(self.response_time)
					topapp.save_button_command = lambda *args: self.set_response_time(topapp.duration_entry_var.get())
					top.geometry("200x100+%d+%d" % (x + 25, y + 120))
					top.bind("<FocusOut>", lambda event:top.destroy())
				filemenu.add_command(label="Settings" ,command = settings_command)
				filemenu.add_separator()
				filemenu.add_command(label="Exit", command=root.destroy)
			
			helpmenu = tk.Menu(menubar, tearoff=0)

			if helpmenu:
				def help_command():
					#Create a Toplevel window
					top= tk.Toplevel(root)
					top.focus()
					x,y = root.winfo_x(),root.winfo_y()
					
					
					op,result = OPERATIONS[self.current_op_index]
					solution = op + str(result)
					font = ('Arial',25,'bold')
					fg = '#00AE70'
					if self.current_op_index == -1:
						solution = 'Start The Game First'
						fg = '#FF5456'
						font = ('Arial',17,'bold')

					elif self.timer != None:
						if not self.timer.done:
							solution = 'Don\'t cheat !!'
							fg = '#FF5456'
							font = ('Arial',17,'bold')

					solution_frame = tk.LabelFrame(top,text = 'Solution')
					solution_frame_label = tk.Label(solution_frame,text = solution,font = font ,fg = fg)

					solution_frame.grid(sticky = 'nswe',padx = 5,pady = (5,10))
					solution_frame_label.grid(sticky = 'nswe')
					
					make_dynamic(top)
					make_dynamic(solution_frame)

					top.update()
					top.minsize(top.winfo_width(), top.winfo_height()+10)
					#top.maxsize(top.winfo_width(), top.winfo_height()+10)
					top.geometry("200x100+%d+%d" % (x + 13, y + 120))
					
					top.bind('<Return>', lambda *arg:top.destroy())
					top.bind('<FocusOut>', lambda *arg:top.destroy())
					top.title("Solution")


				helpmenu.add_command(label="Help Solution",command = help_command)
				helpmenu.add_separator()
				def about_command(*args):
					#Create a Toplevel window
					top= tk.Toplevel(root)
					top.focus()
					top.title('Solution')

					x,y = root.winfo_x(),root.winfo_y()
		
					font = ('Arial',15,'bold')
					
					labelframe = tk.LabelFrame(top,text = 'About')
					#l.pack(fill = 'both',padx = 5,pady= 5)
					if labelframe:
						frame = tk.Frame(labelframe,highlightbackground="#420420", highlightthickness=1)
						if frame:
							label1 = tk.Label(frame,text = 'Made for Fun ',font = font ,fg = '#00AE70')
							label2 = tk.Label(frame,text = 'by Redviper ',font = font ,fg = '#FF5456')
					#label.pack(pady = 10)
					labelframe.grid(padx=5,pady=5,sticky = 'nswe')
					frame.grid(sticky = '')
					label1.grid()
					label2.grid()
					make_dynamic(top)
					make_dynamic(labelframe)
					#make_dynamic(frame)
					top.update()
					top.minsize(top.winfo_width(), top.winfo_height())
					top.geometry("200x100+%d+%d" % (x + 50, y + 120))
					top.bind('<Return>', lambda *arg:top.destroy())
					top.bind('FocusOut>', lambda *arg:top.destroy())
					top.title("About...")
				
				helpmenu.add_command(label="About...",command = about_command)

		menubar.add_cascade(label="File", menu=filemenu)
		menubar.add_cascade(label="Help", menu=helpmenu)
		root.config(menu=menubar)

	def configure_widgets(self):

		self.operation_entry_var = tk.StringVar() ; self.operation_entry_var.set('??')
		self.operation_entry.configure(textvariable = self.operation_entry_var)

		self.timer_label_var = tk.StringVar() ; self.timer_label_var.set(str(self.response_time))
		self.timer_label.configure(textvariable = self.timer_label_var)

		self.operation_label_var = tk.StringVar() ; self.operation_label_var.set('? x ? = ')
		self.operation_label.configure(textvariable = self.operation_label_var)

		self.start_button.configure(command = self.start_button_command)
		self.start_button.configure(bg = self.start_button_bg,activebackground=self.start_button_activebackground)
		
		self.check_button.configure(command = self.check_button_command)
		self.check_button.configure(bg = self.check_button_bg,activebackground=self.check_button_activebackground)
		self.root.bind('<Return>', self.Enter_button_command)
		self.root.title('Multiplication Table Game')
		
	def Enter_button_command(self,*args):
		if self.timer:
			self.timer.stop()
		else:
			self.start_button_command()
	def enable_start_button(self):
		self.start_button['state'] = 'normal'
		self.start_button.configure(bg = self.start_button_bg )
	def disable_start_button(self):
		self.start_button['state'] = 'disabled'
		self.start_button.configure(bg = self.start_button_activebackground )

	def enable_operation_entry(self):
		self.operation_entry['state'] = 'normal'
	def disable_operation_entry(self):
		self.operation_entry['state'] = 'disabled'

	def on_start_animation(self):
		print('\nstart')
		
		self.operation_frame.configure(bg = '#F0F0F0')
		self.operation_label.configure(bg = '#F0F0F0')
		self.operation_entry.configure(disabledbackground= 'White')
		self.f1.configure(bg = '#F0F0F0')

	def on_right_answer_animation(self):
		print('Yes')
		self.operation_frame.configure(bg = '#00FF8E')
		self.operation_label.configure(bg = '#00FF8E')
		self.operation_entry.configure(disabledbackground= '#00FF8E')
		self.f1.configure(bg = '#00FF8E')
	def on_wrong_answer_animation(self):
		print('No')
		self.operation_frame.configure(bg = '#FF5456')
		self.operation_label.configure(bg = '#FF5456')
		self.operation_entry.configure(disabledbackground= '#FF5456')
		self.f1.configure(bg = '#FF5456')

	def start_button_command(self): 
		if self.current_op_index == len(OPERATIONS)-1:
			self.current_op_index = -1
			shuffle(OPERATIONS)

		#Focus on the input space
		self.operation_entry.focus()
		#Create and Start the timer
		self.timer = Timer(self.root,self.timer_label_var,self.response_time*1000,int(self.timer_step*1000))
		self.timer.when_finished = self.check_button_command
		self.timer.initiate()
		#increment the counters
		self.current_op_index +=1 
		self.all_answers_counter += 1
		# show the next operation
		next_operation = OPERATIONS[self.current_op_index][0]
		self.operation_label_var.set(next_operation)
		# clear the entry space
		self.operation_entry_var.set('')
		#disable the start button  {active, normal, disabled}
		self.disable_start_button()
		#Enable the input space 
		self.enable_operation_entry()
		#restore the default colors
		self.on_start_animation()

	def check_button_command(self):
		if not self.timer:
			return
		if not self.timer.done:
			self.timer.stop()
		#Destroy the timer
		del self.timer
		self.timer = None
		
		op,result = OPERATIONS[self.current_op_index]
		#get the user input
		user_input = str(self.operation_entry_var.get())
		#check if it s right or wrong and show it on the screen
		if not user_input:
			user_input = -1
		try:
			int(user_input)
		except:
			user_input = -1
		if int(user_input) == int(result):
			self.right_answers_counter += 1 
			self.on_right_answer_animation()
		else:
			self.on_wrong_answer_animation()
		#disable the input space 
		self.disable_operation_entry()
		#Enable the start button
		self.enable_start_button()
	
if __name__ == '__main__':
	root = tk.Tk()
	
	the_app = App(root)
	
	
