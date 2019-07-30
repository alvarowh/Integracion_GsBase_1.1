import tkinter as tk


class Example(tk.Frame):

    def __init__(self):
        super().__init__()

        self.initUI()




def main():

    root = tk.Tk()
    root.title("GsBaseConnector 1.0")
    root.geometry("950x540")
    root.mainloop()


if __name__ == '__main__':
    main()