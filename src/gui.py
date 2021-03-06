import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import ScrolledText as tkst
from threading import Thread
import controller
import Queue

class MainWindow:

    def __init__(self):
        self.controller = None
        self.logQ = Queue.Queue(maxsize=100)

    def show(self):
        self.root = root = Tkinter.Tk()  # create a Tk root window
        root.title("Company Data Parser")

        parentFrame = Frame(root)
        parentFrame.configure(borderwidth=3, relief=RAISED);
        parentFrame.pack(fill=X)

        w = 800  # width for the Tk root
        h = 800  # height for the Tk root

        # get screen width and height
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.lift()

        #bring the window to the front
        root.attributes("-topmost", True)
        root.after_idle(root.attributes, '-topmost', False)
        root.focus_force()

        frame = Frame(parentFrame)
        frame.configure(borderwidth=3, bg="#e1ffd6");
        frame.pack(side=TOP, expand=NO, fill=BOTH)

        label = Label(frame, text=u'\u8acb\u9078\u64c7\u76ee\u9304', bg="#e1ffd6")
        label.pack(side=LEFT)

        self.fileEntry = Entry(frame,width=50)
        self.fileEntry.pack(side=LEFT)

        selectFilebutton = Button(frame, text=u'\u700f\u89bd', command=self.load_file, width=10)
        selectFilebutton.pack(side=LEFT)

        optionFrame = Frame(parentFrame)
        optionFrame.configure(borderwidth=3, bg="#e1ffd6");
        optionFrame.pack(side=TOP, expand=NO, fill=BOTH)
        optionLabel = Label(optionFrame, text=u'\u9078\u9805\uff1a', bg="#e1ffd6")
        optionLabel.pack(side=LEFT)

        optionFrame2 = Frame(parentFrame)
        optionFrame2.configure(borderwidth=3, bg="#e1ffd6");
        optionFrame2.pack(side=TOP, fill=BOTH)
        op1Label = Label(optionFrame2, text=u'      \u53d6\u5f97\uff1a', bg="#e1ffd6")
        op1Label.pack(side=LEFT)

        self.dataType = StringVar()
        self.dataType.set("CompanyData")
        Radiobutton(optionFrame2, text=u'\u57fa\u672c\u8cc7\u6599', variable=self.dataType, value="CompanyData", bg="#e1ffd6").pack(side=LEFT)
        Radiobutton(optionFrame2, text=u'\u7d44\u7e54\u67b6\u69cb', variable=self.dataType, value="Hierarchy", bg="#e1ffd6").pack(side=LEFT)

        optionFrame3 = Frame(parentFrame)
        optionFrame3.configure(borderwidth=3, bg="#e1ffd6");
        optionFrame3.pack(side=TOP, fill=BOTH)
        op2Label = Label(optionFrame3, text=u'      \u5e74\u4efd\uff1a', bg="#e1ffd6")
        op2Label.pack(side=LEFT)

        self.selectYears = StringVar()
        self.selectYears.set("All")
        Radiobutton(optionFrame3, text=u'\u5168\u90e8', variable=self.selectYears, value="All", bg="#e1ffd6").pack(side=LEFT)
        Radiobutton(optionFrame3, text=u'\u6307\u5b9a\u5e74\u4efd', variable=self.selectYears, value="Designated", bg="#e1ffd6").pack(side=LEFT)

        self.yearEntry = Entry(optionFrame3, width=30)
        self.yearEntry.pack(side=LEFT)

        def handleReturn(event):
            self.selectYears.set("Designated")

        self.yearEntry.bind("<FocusIn>", handleReturn)

        Label(optionFrame3, text="(e.g. 2014,2015,Present)", bg="#e1ffd6").pack(side=LEFT)

        optionFrameFilterCompany = Frame(parentFrame)
        optionFrameFilterCompany.configure(borderwidth=3, bg="#e1ffd6");
        optionFrameFilterCompany.pack(side=TOP, fill=BOTH)
        Label(optionFrameFilterCompany, text=u'      \u6307\u5b9a\u516c\u53f8ID\uff1a', bg="#e1ffd6").pack(side=LEFT)

        self.filter_company_entry = tkst.ScrolledText(
            master=optionFrameFilterCompany,
            wrap='word',  # wrap text at full words only
            width=10,  # characters
            height=3,  # text lines
            bg='beige'  # background color of edit area
        )
        # self.edit_space.configure(state="disabled")
        self.filter_company_entry.pack(padx=10, pady=10, fill=BOTH, expand=True)

        optionFrame5 = Frame(parentFrame)
        optionFrame5.configure(borderwidth=3, bg="#e1ffd6");
        optionFrame5.pack(side=TOP, fill=BOTH)
        Label(optionFrame5, text=u'      \u5176\u4ed6\uff1a', bg="#e1ffd6").pack(side=LEFT)
        Label(optionFrame5, text=u'\u9593\u9694', bg="#e1ffd6").pack(side=LEFT)
        self.sleepEntry = Entry(optionFrame5, width=3)
        self.sleepEntry.pack(side=LEFT)
        self.sleepEntry.insert(END, '1')
        Label(optionFrame5, text=u'\u79d2\u6293\u4e0b\u4e00\u500b\u516c\u53f8', bg="#e1ffd6").pack(side=LEFT)

        Label(optionFrame5, text=u'    \u5e74\u8207\u5e74\u9593\u9694', bg="#e1ffd6").pack(side=LEFT)
        self.sleepYearEntry = Entry(optionFrame5, width=3)
        self.sleepYearEntry.pack(side=LEFT)
        self.sleepYearEntry.insert(END, '1')
        Label(optionFrame5, text=u'\u79d2', bg="#e1ffd6").pack(side=LEFT)

        optionFrame4 = Frame(parentFrame)
        optionFrame4.configure(borderwidth=3, bg="#e1ffd6");
        optionFrame4.pack(side=TOP, fill=BOTH)

        self.start_button = Button(optionFrame4, text=u'\u958b\u59cb', command=self.startCallBack)
        self.start_button.pack(side=LEFT)
        Label(optionFrame4, text="    ", bg="#e1ffd6").pack(side=LEFT)
        self.cancel_button = Button(optionFrame4, text=u'\u53d6\u6d88', command=self.cancelCallBack)
        self.cancel_button.pack(side=LEFT)

        separator = Frame(parentFrame)
        separator.configure(height=2, bd=1, background="#e1ffd6", relief=SUNKEN)
        # separator.pack(fill=X, padx=5, pady=5)

        optionFrame6 = Frame(parentFrame)
        optionFrame6.configure(borderwidth=3, bg="#e1ffd6");
        # optionFrame6.pack(side=TOP, expand=NO, fill=BOTH)
        # Label(optionFrame6, text=u'\u5931\u6557\u8655\u7406\uff1a', bg="#e1ffd6").pack(side=LEFT)

        self.retry_button = Button(optionFrame6, text=u'\u6293\u53d6\u524d\u6b21\u5931\u6557\u7684\u516c\u53f8', command=self.retryCallBack)
        self.retry_button.pack_forget() # (side=LEFT)
        self.retry_button.config(state="disabled")

        # Label(optionFrame6, text="    ", bg="#e1ffd6").pack(side=LEFT)

        self.save_button = Button(optionFrame6, text=u'\u5c07\u5931\u6557\u516c\u53f8ID\u5b58\u6210\u6a94\u6848', command=self.saveFailedCompanies)
        self.save_button.pack_forget() # .pack(side=LEFT)
        self.save_button.config(state="disabled")

        logFrame = Frame(root)
        logFrame.configure(borderwidth=3);
        logFrame.pack(fill=BOTH, expand=True)

        self.edit_space = tkst.ScrolledText(
            master=logFrame,
            wrap='word',  # wrap text at full words only
            width=25,  # characters
            height=10,  # text lines
            bg='beige'  # background color of edit area
        )
        # self.edit_space.configure(state="disabled")
        self.edit_space.pack(padx=10, pady=10, fill=BOTH, expand=True)

        root.grid_columnconfigure(0, weight=1)
        root.mainloop()  # starts the mainloop

    def load_file(self):
        # fname = askopenfilename(filetypes=[("HTML Files", "*.html"), ("HTML Files", "*.htm")])
        fname = tkFileDialog.askdirectory()
        if fname:
            try:
                self.set_input_file(fname)
            except:  # <- naked except is a bad idea
                tkMessageBox.showerror(u'\u932f\u8aa4', u'\u7121\u6cd5\u8b80\u53d6\u6307\u5b9a\u7684\u76ee\u9304')


    def set_input_file(self, text):
        self.fileEntry.delete(0, END)
        self.fileEntry.insert(0, text)

    def cancelCallBack(self):
        if self.controller:
            result = tkMessageBox.askquestion(u'\u53d6\u6d88', u'\u78ba\u5b9a\u53d6\u6d88\u55ce\uff1f', icon='warning')
            if result == 'yes':
                self.controller.isRunning = False

    def startCallBack(self):
        if not self.fileEntry.get():
            tkMessageBox.showerror(u'\u932f\u8aa4', u'\u8acb\u9078\u64c7\u76ee\u9304')
            return

        if self.selectYears.get() == "Designated" and not self.yearEntry.get():
            tkMessageBox.showerror(u'\u932f\u8aa4', u'\u8acb\u4f9d\u7167\u683c\u5f0f\u8f38\u5165\u6307\u5b9a\u5e74\u4efd\uff0c\u5982 2014,2015,Present')
            return

        if self.selectYears.get()=="Designated" and self.yearEntry.get():
            try:
                nums = self.yearEntry.get().split(",")
            except:
                tkMessageBox.showerror(u'\u8acb\u4f9d\u7167\u683c\u5f0f\u8f38\u5165\u6307\u5b9a\u5e74\u4efd\uff0c\u5982 2014,2015,Present')
                return
        else:
            nums=[]

        result = tkMessageBox.askquestion(u'\u78ba\u5b9a', u'\u78ba\u5b9a\u958b\u59cb\u55ce\uff1f', icon='warning')

        if result == 'no':
            return
        else:
            self.root.after(0, lambda: self.__run_it__(nums))

    def __run_it__(self, nums):
        self.retry_button.config(state="disabled")
        self.save_button.config(state="disabled")

        self.edit_space.configure(state='normal')
        self.edit_space.delete('1.0', END)
        self.edit_space.configure(state='disabled')

        if not self.sleepEntry.get():
            sleep=0
        else:
            sleep=float(self.sleepEntry.get())

        if not self.sleepYearEntry.get():
            sleepYear=0
        else:
            sleepYear=float(self.sleepYearEntry.get())

        filterCompanies = []

        if self.filter_company_entry.get(1.0, END).rstrip():
            filterCompanies = self.filter_company_entry.get(1.0, END).rstrip().split(",")

        self.controller = controller.ParserController([self.fileEntry.get()], sleep, sleepYear, self.logProgress, self.doNothing, nums, filterCompanies)

        self.t = Thread(
            target=self.__startInternal__)

        self.t.start()
        self.root.after(100, lambda: self.logProgressAsync())
        self.check_thread()


    def retryCallBack(self):
        if not self.controller or not self.controller.failed_companies:
            tkMessageBox.showerror(u'\u932f\u8aa4', u'\u4e26\u672a\u6709\u524d\u6b21\u5931\u6557\u7684\u516c\u53f8')
            return

        result = tkMessageBox.askquestion(u'\u78ba\u5b9a', u'\u78ba\u5b9a\u91cd\u6293\u524d\u6b21\u5931\u6557\u7684\u516c\u53f8\uff1f', icon='warning')
        if result == 'no':
            return
        else:
            self.root.after(0, self.__run_retry__)

    def __run_retry__(self):
        self.edit_space.configure(state='normal')
        self.edit_space.delete('1.0', END)
        self.edit_space.configure(state='disabled')

        self.t = Thread(
            target=self.__retryInternal__)

        self.t.start()
        self.root.after(100, lambda: self.logProgressAsync())
        self.check_thread()

    def check_thread(self):
        # Still alive? Check again in half a second
        if self.t.isAlive():
            self.root.after(500, self.check_thread)
        else:
            self.isDone()
    
    def doNothing(self):
        pass

    def __retryInternal__(self):
        self.start_button.config(state="disabled")
        self.controller.parseHierarchyDataForFailedCompanies()

    def __startInternal__(self):
        self.start_button.config(state="disabled")

        if self.dataType.get() == "CompanyData":
            self.controller.parseCompanyData()
        else:
            self.controller.parseHierarchyData()

    def logProgress(self, text):
        self.logQ.put(text)

    def logProgressAsync(self):
        while self.logQ.qsize():
            try:
                msg = self.logQ.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                self.__logProgress__(msg)
            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

        self.root.after(100, lambda: self.logProgressAsync())
		
    def __logProgress__(self, text):
        self.edit_space.configure(state='normal')
        self.edit_space.insert(INSERT, text + "\n")
        self.edit_space.see(Tkinter.END)
        self.edit_space.configure(state='disabled')
		
    def isDone(self):
        self.start_button.config(state="active")

        if not self.controller.failed_companies:
            self.retry_button.config(state="disabled")
            self.save_button.config(state="disabled")
            tkMessageBox.showinfo(u'\u8a0a\u606f', u'\u5de5\u4f5c\u5b8c\u6210')
        else:
            self.retry_button.config(state="active")
            self.save_button.config(state="active")
            tkMessageBox.showwarning(u'\u8a0a\u606f', u'\u5de5\u4f5c\u5b8c\u6210\u3002\u4f46\u6709\u672a\u80fd\u6210\u529f\u6293\u53d6\u7684\u516c\u53f8\uff0c\u53ef\u57f7\u884c\u91cd\u6293\u3002')
            # self.controller.saveFailedCompanies()

    def saveFailedCompanies(self):
        if self.controller and self.controller.failed_companies:
            self.controller.saveFailedCompanies()
            tkMessageBox.showinfo(u'\u8a0a\u606f', u'\u5132\u5b58\u5b8c\u6210')
