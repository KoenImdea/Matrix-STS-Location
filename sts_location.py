"""
v1.0 Started on 18/01/2021

Author: Koen

Purpose: Read STS locations from Matrix, and save them in separate file.
This should make data analysis easier.

For v1.0,

"""
#Import tkinter for GUI and matplotlib for plots
import tkinter
import tkinter.messagebox
#We'll make use of numpy
import numpy as np
#Just in case we want tu use a special character
import re
#Import os to help with filename stuff
import os
# Time keeping and sleeping
import time
# We'll need to multi-thread in order to not hang up GUI
import threading
#We need mate4dummies
import mate4dummies.objects as mo

"""Now we define the GUI parts, starting with the main window """
class MainWindow:
    """
    Here we create the main window when opening op the program. It is
    supposed to be modular and easily extendible.
    """
    def __init__(self, master):
        # Set up the GUI
        self.path = ""
        self.master = master
        self.master.resizable(False, False)
        # First block is the Code to allow to connect to Matrix
        self.ConnectFrame = tkinter.Frame(master, height = 100, width = 300)
        self.console = tkinter.Button(self.ConnectFrame, text='Connect to \n Matrix',
            command=self.connection)
        self.console.place(relx=.5, rely=.5, anchor="center")
        self.ConnectFrame.pack(side = "top")
        self.ConnectFrame.propagate(0)

        # Choose Channel to watch
        self.ChannelsFrame  = tkinter.Frame(master, height = 150, width = 300)
        self.I_V = tkinter.Button(self.ChannelsFrame, text='I(V)',
            command=self.I_V_watch)
        self.I_V.pack(side = "top")
        self.I_V["state"] = "disabled"

        self.df_V = tkinter.Button(self.ChannelsFrame, text='df(V)',
            command=self.df_V_watch)
        self.df_V.pack()
        self.df_V["state"] = "disabled"

        self.I_Z = tkinter.Button(self.ChannelsFrame, text='I(Z)',
            command=self.I_Z_watch)
        self.I_Z.pack()
        self.I_Z["state"] = "disabled"

        self.df_Z = tkinter.Button(self.ChannelsFrame, text='df(Z)',
            command=self.df_Z_watch)
        self.df_Z.pack()
        self.df_Z["state"] = "disabled"

        self.ChannelsFrame.pack(side = "top")
        self.ChannelsFrame.propagate(0)
        self.busy = False
        self.curve = False


    def connection(self):
        """Connect to, and disconnect from Matrix
            Meanwhile, update the available options.

        """
        if mo.mate.online == False:
            mo.mate.connect()

            if mo.mate.online:
                print("WTF")

                if mo.mate.exp_params['Result_File_Path'] == "void":
                    print("WTF2")
                    mo.mate.disconnect()
                    tkinter.messagebox.showinfo(title=None, message="No valid Matrix session found.")
                else:
                    print("WTF3")
                    self.console["text"] = "Disconnect from \n Matrix"
                    self.I_V["state"] = "active"
                    self.df_V["state"] = "active"
                    self.I_Z["state"] = "active"
                    self.df_Z["state"] = "active"
                    self.path = mo.mate.exp_params['Result_File_Path']


            else:

                print("Error")

        else:
            self.busy = False
            print("Kill Data gathering!!!!!!")
            mo.esc = True
            time.sleep(1)
            self.curve = False

            if mo.mate.online:
                self.helper = mo.view.Data()
                _ = mo.view.Deliver_Data(False)

                _ = mo.mate.disconnect()

            self.console["text"] = "Connect to \n Matrix"
            self.I_V["relief"] = "raised"
            self.df_V["relief"] = "raised"
            self.I_Z["relief"] = "raised"
            self.df_Z["relief"] = "raised"
            self.I_V["state"] = "disabled"
            self.df_V["state"] = "disabled"
            self.I_Z["state"] = "disabled"
            self.df_Z["state"] = "disabled"


    def I_V_watch(self):
        """
        To watch a channel we need to put the view name and the channel name.
        See .vied file for view name, and .expd for associated channel name.
        """

        self.I_V["relief"] = "sunken"
        self.df_V["relief"] = "raised"
        self.I_Z["relief"] = "raised"
        self.df_Z["relief"] = "raised"
        if self.busy:
            mo.esc = True
            time.sleep(1)
            mo.esc = False
            mo.view_name = 'I_V_Spec'
            mo.channel_name = 'I_V'
            self.write = threading.Thread(target= self.writedata)
            self.write.start()

        else:
            mo.view_name = 'I_V_Spec'
            mo.channel_name = 'I_V'
            self.busy = True
            self.write = threading.Thread(target= self.writedata)
            self.write.start()


    def df_V_watch(self):
        """
        To watch a channel we need to put the view name and the channel name.
        See .vied file for view name, and .expd for associated channel name.
        """

        self.I_V["relief"] = "raised"
        self.df_V["relief"] = "sunken"
        self.I_Z["relief"] = "raised"
        self.df_Z["relief"] = "raised"

        if self.busy:
            mo.esc = True
            time.sleep(1)
            mo.esc = False
            mo.view_name = "Aux1_V_Spec"
            mo.channel_name = 'Aux1_V'
            self.write = threading.Thread(target= self.writedata)
            self.write.start()

        else:
            mo.view_name = "Aux1_V_Spec"
            mo.channel_name = 'Aux1_V'
            self.busy = True
            self.write = threading.Thread(target= self.writedata)
            self.write.start()


    def I_Z_watch(self):
        """
        To watch a channel we need to put the view name and the channel name.
        See .vied file for view name, and .expd for associated channel name.
        """
        mo.view_name = 'I_Z_Spec'
        mo.channel_name = 'I_Z'
        self.I_V["relief"] = "raised"
        self.df_V["relief"] = "raised"
        self.I_Z["relief"] = "sunken"
        self.df_Z["relief"] = "raised"

        if self.busy:
            mo.esc = True
            time.sleep(1)
            mo.esc = False
            mo.view_name = 'I_Z_Spec'
            mo.channel_name = 'I_Z'
            self.write = threading.Thread(target= self.writedata)
            self.write.start()

        else:
            mo.view_name = 'I_Z_Spec'
            mo.channel_name = 'I_Z'
            self.busy = True
            self.write = threading.Thread(target= self.writedata)
            self.write.start()


    def df_Z_watch(self):
        """
        To watch a channel we need to put the view name and the channel name.
        See .vied file for view name, and .expd for associated channel name.
        """

        self.I_V["relief"] = "raised"
        self.df_V["relief"] = "raised"
        self.I_Z["relief"] = "raised"
        self.df_Z["relief"] = "sunken"

        if self.busy:
            mo.esc = True
            time.sleep(1)
            mo.esc = False
            mo.view_name = "Aux1_Z_Spec"
            mo.channel_name = 'Aux1_Z'
            self.write = threading.Thread(target= self.writedata)
            self.write.start()

        else:
            mo.view_name = "Aux1_Z_Spec"
            mo.channel_name = 'Aux1_Z'
            self.busy = True
            self.write = threading.Thread(target= self.writedata)
            self.write.start()


    def get_curve_data(self):
        #Make sure you know how much points to expect
        self.data_size = mo.view.Data_Size()
        #Get the data from Matrix
        self.y_data = mo.sample_data(self.data_size)
        #Read the run number
        #(X in the Matrix X-Y system for labeling curves and images)
        self.run_count = mo.view.Run_Count()
        #Read the cycle number
        #(Y in the Matrix X-Y system for labeling curves and images)
        self.cycle_count = mo.view.Cycle_Count()
        self.position = mo.xy_scanner.Target_Position()
        self.area = mo.xy_scanner.Area()
        self.curve = True


    def writedata(self):
        filename = self.path + r"\locations.txt"
        with open(filename, "a+") as file:
            file.write(mo.view_name + "\r\n")
        if mo.channel.Enable():
            self.helper = mo.view.Data(self.get_curve_data)
            _ = mo.view.Deliver_Data(True)
            #Now something to avoid waiting froever if we need to switch from I(V) to I(Z)
            while mo.mate.online and self.busy:
                mo.wait_for_event()
                if self.curve:
                    with open(filename, "a+") as file:
                        file.write(str(self.run_count) + "_" + str(self.cycle_count)+ ": ")
                        file.write("("+str(((self.position[0]+1)/2)*self.area[0]*1e9)+";"+str(((self.position[1]+1)/2)*self.area[1]*1e9)+")\r\n")
                self.curve = False
            self.helper = mo.view.Data()
            _ = mo.view.Deliver_Data(False)
        else:
            tkinter.messagebox.showinfo(title=None, message="Channel not enabled.")









root = tkinter.Tk()

client = MainWindow(root)
root.mainloop()
