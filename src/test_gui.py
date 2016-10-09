from Tkinter import *


class ActionListener:
    main = None

    def __init__(self, main):
        self.main = main;


    def action(self):
        print("ActionListener!");
        self.main.showJF2();


class Main:
    def __init__(self):
        self.currJF=None

        tk = Tk();
        self.mjf = Frame(tk, borderwidth=5, relief=SUNKEN);
        self.jf1 = Frame(self.mjf);
        self.jf1.configure(borderwidth=3, background="green", relief=GROOVE);

        bt1 = Button(self.jf1, text="JF1");
        bt2 = Button(self.jf1, text="JF1");
        bt3 = Button(self.jf1, text="JF1");
        bt1.pack(side=LEFT, fill=BOTH, expand=YES);
        bt2.pack(side=LEFT, fill=BOTH, expand=YES);
        bt3.pack(side=LEFT, fill=BOTH, expand=YES);

        self.jf2 = Frame(self.mjf);
        self.jf2.configure(borderwidth=3, background="red", relief=RIDGE);

        bt1 = Button(self.jf2, text="JF2");
        bt2 = Button(self.jf2, text="JF2");
        bt3 = Button(self.jf2, text="JF2");
        bt1.pack(side=LEFT, fill=BOTH, expand=YES);
        bt2.pack(side=LEFT, fill=BOTH, expand=YES);
        bt3.pack(side=LEFT, fill=BOTH, expand=YES);

        self.jf3 = Frame(self.mjf);
        self.jf3.configure(borderwidth=3, background="yellow", relief=RIDGE);
        bt1 = Button(self.jf3, text="JF3");
        bt2 = Button(self.jf3, text="JF3");
        bt3 = Button(self.jf3, text="JF3");
        bt1.pack(side=LEFT, fill=BOTH, expand=YES);
        bt2.pack(side=LEFT, fill=BOTH, expand=YES);
        bt3.pack(side=LEFT, fill=BOTH, expand=YES);

        btFrame = Frame(tk);
        bt1 = Button(btFrame, text="SHOW_JF1");
        bt2 = Button(btFrame, text="SHOW_JF2");
        bt3 = Button(btFrame, text="SHOW_JF3");

        # [ 1. Anonymous Callback Function with arguments
        bt1.configure(command=lambda s=self, event="JF1": s.showJF(event));

        # [ 2. ActionListener with arguments
        bt2.configure(command=ActionListener(self).action);

        # [ 3. Direct Callback Function
        bt3.configure(command=self.showJF3);

        bt1.pack(side=LEFT, fill=BOTH, expand=YES);
        bt2.pack(side=LEFT, fill=BOTH, expand=YES);
        bt3.pack(side=LEFT, fill=BOTH, expand=YES);

        btFrame.pack(side=TOP)
        self.mjf.pack(side=TOP, fill=BOTH, expand=YES);

        newBtFrame = Frame(tk);
        newBtFrame.pack(side=TOP, fill=X, expand=YES);
        bt1 = Button(newBtFrame, text="Bottom Button1");
        bt2 = Button(newBtFrame, text="Bottom Button2");
        bt1.pack(side=LEFT);
        bt2.pack(side=RIGHT);

        self.showJF("JF2");

    def showJF(self, event):
        print("Anonymous Callback Function with arguments");
        if (self.currJF != None):
            self.currJF.pack_forget();

        if (event == "JF1"):
            self.jf1.pack(side=TOP, fill=BOTH, expand=YES);
            self.currJF = self.jf1;

        if (event == "JF2"):
            self.jf2.pack(side=TOP, fill=BOTH, expand=YES);
            self.currJF = self.jf2;

        if (event == "JF3"):
            self.jf3.pack(side=TOP, fill=BOTH, expand=YES);
            self.currJF = self.jf3;

    def showJF2(self):
        if (self.currJF != None):
            self.currJF.pack_forget();

        self.jf2.pack(side=TOP, fill=BOTH, expand=YES);
        self.currJF = self.jf2;

    def showJF3(self):
        if (self.currJF != None):
            self.currJF.pack_forget();

        self.jf3.pack(side=TOP, fill=BOTH, expand=YES);
        self.currJF = self.jf3;


m = Main();
mainloop();