if __name__ == '__main__':
    # Import package
    from tkinter import *
    import tkinter as tk
    # import filedialog module
    from tkinter import filedialog


    # create window
    window = tk.Tk()
    window.title('Split Team Arrangement')
    align_mode = 'nswe'
    pad = 5


    # create frame
    width_size = 250
    height_size = 30
    div1 = tk.Frame(window,  width = width_size , height = height_size)
    div2 = tk.Frame(window,  width = width_size , height = height_size)
    div3 = tk.Frame(window,  width = width_size , height = height_size)
    div4 = tk.Frame(window,  width = width_size , height = height_size)


    # function
    def popup_bonus():
        win = tk.Toplevel()
        win.wm_title("Done!!")
        lb = tk.Label(win, text = "Finished!!!! Please check your destination file~")
        lb.pack()

    def open_source():
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File",
                                              filetypes = (("CSV files",
                                                           "*.csv*"),
                                                          ("all files",
                                                           "*.*")))
        label_source.configure(text = "File Opened: " + filename)
        in_dir.set(filename)

    def get_enrty():
        eq_input = entry_var.get()
        return eq_input

    def open_dest():
        file_dir = filedialog.askdirectory(initialdir = "/", title = "Select a Directory")
        label_destination.configure(text = "Destination: " + file_dir)
        ot_dir.set(file_dir)

    def grouping(in_dir, ot_dir, team_number):
        in_dir = in_dir.get()
        ot_dir = ot_dir.get() + "\grouping_result.csv"
        group = int(team_number)

        # read data
        import pandas as pd

        try:
            df = pd.read_csv(in_dir, encoding = 'big5')
        except:
            df = pd.read_csv(in_dir)

        # data to list
        name_list = list(df.iloc[:, 0])

        # covert to num
        df1 = pd.get_dummies(df.iloc[:, 1:])

        # hierarchy graph
        import scipy.cluster.hierarchy as sch
        import numpy as np

        disMat = sch.distance.pdist(df1, 'euclidean')
        Z = sch.linkage(disMat, method = 'average')
        P = sch.dendrogram(Z, labels = name_list , no_plot = True)

        # team list
        if len(P['ivl']) % group == 0:
            temp = np.asarray(P['ivl'])
        else:
            temp = P['ivl'] + [''] * (group - len(P['ivl']) % group)
        temp = np.asarray(temp).reshape(int(len(temp) / group), group)

        # output data
        team_sheet = pd.DataFrame(temp)
        team_sheet.columns = ['team_' + str(i + 1) for i in range(group)]
        team_sheet.to_csv(ot_dir, encoding = 'utf-8-sig')
        popup_bonus()


    # create function
    button_source = tk.Button(div1, text = "Select Source", command = open_source)
    label_source = tk.Label(div1, text = 'Your source is...'); in_dir = tk.StringVar()

    button_destination = tk.Button(div2, text="Select Destination", command = open_dest)
    label_destination = tk.Label(div2, text = 'Your destination is...'); ot_dir = tk.StringVar()

    label_teamnum = tk.Label(div3, text="Number of team: ")
    entry_var = StringVar(); entry = tk.Entry(div3, textvariable = entry_var, bd = 5)

    button_run = tk.Button(div4, text = "Run", command = lambda: grouping(in_dir, ot_dir, get_enrty()))

    # setting ui
    div1.grid(column = 0, row = 0, padx = pad, pady = pad, sticky = align_mode)
    button_source.grid(column = 0, row = 0)
    label_source.grid(column = 1, row = 0)

    div2.grid(column = 0, row = 1, padx = pad, pady = pad, sticky = align_mode)
    button_destination.grid(column = 0, row = 0)
    label_destination.grid(column = 1, row = 0)

    div3.grid(column = 0, row = 2, padx = pad, pady = pad, sticky = align_mode)
    label_teamnum.grid(column = 0, row = 0)
    entry.grid(column = 1, row = 0)

    div4.grid(column = 0, row = 3, padx = pad, pady = pad, sticky = align_mode)
    button_run.grid(column = 1,row = 0)

    # Let the window wait for any events
    window.mainloop()

    import os
    os.close(1)