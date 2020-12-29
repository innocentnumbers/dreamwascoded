import multiprocessing
import numpy as np
import time
from columnar import columnar
from click import style
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

t10 = time.time()

ep_weight = 20
blaze_weight = 1
dream_ep = 42
dream_ep_attempts = 262
dream_blaze = 211
dream_blaze_att = 305

def attempts(id, biggest, totalCount, over30, over40, blaze_biggest, blaze_over200, dreamLuck, ss_ep, ss_br, ss_cmo, ender_sample, blaze_sample):
    count = 0
    print("thread "+str(id)+" started")
    while True:
        count += 1
        x=np.random.randint((403+ep_weight), size=(dream_ep_attempts))
        y=np.random.randint((1+blaze_weight), size=(dream_blaze_att))
        #EPS
        #check where ep trades would happen
        ender_trades = (x < ep_weight).sum()
        #keep track of single luckiest ender pearl session
        if ender_trades > biggest.value:
            biggest.value = ender_trades
        #keep track of ender pearl sessions over 30
        if ender_trades >= 30:
            over30.value += 1
        #keep track of ender pearl sessions over 40
        if ender_trades >= 40:
            over40.value += 1

        #blazes
        blaze = (y < blaze_weight).sum()
        #keep track of single luckiest blaze session
        if blaze > blaze_biggest.value:
            blaze_biggest.value = blaze
        #keep track of blaze sessions over 200
        if blaze >= 200:
            blaze_over200.value += 1

        #estimate of luckiest session
        if ((ender_trades/dream_ep_attempts)*4.3 + (blaze/dream_blaze_att)) >  ((ss_ep.value/dream_ep_attempts)*4.3 + (ss_br.value/dream_blaze_att)):
            ss_ep.value = ender_trades
            ss_br.value = blaze

        if ender_trades >= 35 and blaze >= 190:
            ss_cmo.value += 1
        #if dream luck actually happens
        if blaze >= dream_blaze and ender_trades >= dream_ep:
            ss_ep.value = ender_trades
            ss_br.value = blaze
            dreamLuck.value = 1

        #increment total count by 100, also check if dream luck acheived
        if count % 100 == 0:
            if id == 1 or id == 2 or id == 3:
                ender_sample.value = ender_trades
                blaze_sample.value = blaze
            totalCount.value += 1
            count = 0
            if dreamLuck.value == 1:
                return 0

intervals = (
    ('years', 86400*30*12),
    ('months', 86400*30),
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def tkLabel(string, fgcolor, bgcolor, w, h):
    label = tk.Label(
        text=string,
        fg=fgcolor,
        bg=bgcolor,
        width=w,
        height=h
    )
    label.config(font=("Courier", 20, 'bold'))
    return label

class dreamGUI:
    def __init__(self, biggest, totalCount, over30, over40, blaze_biggest, blaze_over200, dreamLuck, ss_ep, ss_br, ss_cmo, ender_sample1, blaze_sample1, ender_sample2, blaze_sample2, ender_sample3, blaze_sample3):
        self.window = tk.Tk()
        self.window.geometry("1920x1080")
        self.window.configure(background='black')
        self.wTitle = tkLabel("Current Drop Rate Data", "white", "black", 30, 5)
        self.wTitle.config(font=("Courier", 24, 'bold'))
        self.wTitle.place(relx = 0.25, rely = 0.0, anchor = 'nw')
        self.sTitle = tkLabel("Current Needed Play Time", "white", "black", 30, 5)
        self.sTitle.config(font=("Courier", 24, 'bold'))
        self.sTitle.place(relx = 0.325, rely = 0.45, anchor = 'nw')

        load = Image.open("enderp.png")
        load = load.resize((50, 50)) ## The (250, 250) is (height, width)
        self.enderRender = ImageTk.PhotoImage(load)

        load = Image.open("blazer.png")
        load = load.resize((50, 50)) ## The (250, 250) is (height, width)
        self.blazeRender = ImageTk.PhotoImage(load)



        dream_runs = 23
        wr_run_t2b = 10*60+30
        t1 = time.time()
        try:
            self.enderpearl = tkLabel("Ender Pearls:", "#2dcdb1", "black", 20, 5)
            self.enderpearl.place(relx = 0.0, rely = 0.15, anchor = 'nw')
            self.blazerods = tkLabel("Blaze Rods:", "#bf5a00", "black", 20, 5)
            self.blazerods.place(relx = 0.0, rely = 0.25, anchor = 'nw')
            self.combined = tkLabel("Combined In\n One Session:", "#b4e62d", "black", 20, 5)
            self.combined.place(relx = 0.0, rely = 0.35, anchor = 'nw')

            self.luckiest_t = tkLabel("Luckiest Trial", "white", "black", 30, 2)
            self.luckiest_t.place(relx = 0.1, rely = 0.13, anchor = 'nw')
            self.trials_ox = tkLabel("Trials Over X", "white", "black", 20, 2)
            self.trials_ox.place(relx = 0.32, rely = 0.13, anchor = 'nw')
            self.timeleft = tkLabel("Time Left Till Dream Luck Estimate", "white", "black", 35, 2)
            self.timeleft.place(relx = 0.57, rely = 0.13, anchor = 'nw')

            self.bigender = tkLabel("0", "#2dcdb1", "black", 5, 1)
            self.bigender.config(font=("Courier", 30, 'bold'))
            self.bigender.place(relx = 0.19, rely = 0.20, anchor = 'nw')
            self.bigblaze = tkLabel("0", "#bf5a00", "black", 5, 2)
            self.bigblaze.config(font=("Courier", 30, 'bold'))
            self.bigblaze.place(relx = 0.19, rely = 0.28, anchor = 'nw')

            self.bigboth1 = tkLabel("0", "#2dcdb1", "black", 4, 2)
            self.bigboth1.config(font=("Courier", 30, 'bold'))
            self.bigboth1.place(relx = 0.16, rely = 0.38, anchor = 'nw')
            self.bigboth2 = tkLabel(" & ", "white", "black", 3, 2)
            self.bigboth2.config(font=("Courier", 30, 'bold'))
            self.bigboth2.place(relx = 0.2, rely = 0.38, anchor = 'nw')
            self.bigboth3 = tkLabel("0", "#bf5a00", "black", 4, 2)
            self.bigboth3.config(font=("Courier", 30, 'bold'))
            self.bigboth3.place(relx = 0.23, rely = 0.38, anchor = 'nw')

            self.over3040 = tkLabel("30 or more: " + "0" + "\n40 or more: " + "0", "#2dcdb1", "black", 28, 3)
            self.over3040.place(relx = 0.29, rely = 0.18, anchor = 'nw')

            self.over200 = tkLabel("200 or more: " + "0", "#bf5a00", "black", 28, 2)
            self.over200.place(relx = 0.29, rely = 0.29, anchor = 'nw')

            self.combinedoverxe = tkLabel("35 or more ender and ", "#2dcdb1", "black", 28, 1)
            self.combinedoverxe.place(relx = 0.29, rely = 0.38, anchor = 'nw')
            self.combinedoverxb = tkLabel("190 or more blaze: " + "0", "#bf5a00", "black", 28, 1)
            self.combinedoverxb.place(relx = 0.29, rely = 0.42, anchor = 'nw')

            timeLeftEnder = str(display_time(round((40000000000/240000))))

            timeLeftBlaze = str(display_time(round((77000000000/240000))))

            timeCombined = str(display_time((round((77000000000*40000000000)/240000))))

            self.tend = tkLabel(timeLeftEnder, "#2dcdb1", "black", 50, 2)
            self.tend.place(relx = 0.51, rely = 0.19, anchor = 'nw')
            self.tblaze = tkLabel(timeLeftBlaze, "#bf5a00", "black", 50, 2)
            self.tblaze.place(relx = 0.51, rely = 0.29, anchor = 'nw')
            self.tcombined = tkLabel(timeCombined, "#b4e62d", "black", 50, 2)
            self.tcombined.place(relx = 0.51, rely = 0.39, anchor = 'nw')

            self.singlep = tkLabel("Single Person Playing:", "#c32728", "black", 25, 5)
            self.singlep.place(relx = 0.0, rely = 0.65, anchor = 'nw')
            self.speedyp = tkLabel("All MC Speedrunners:", "#fed667", "black", 25, 5)
            self.speedyp.place(relx = 0.0, rely = 0.75, anchor = 'nw')
            self.allp = tkLabel("All Minecraft Players:", "#62b853", "black", 25, 5)
            self.allp.place(relx = 0.0, rely = 0.85, anchor = 'nw')

            self.numplayers = tkLabel("# Of Players", "white", "black", 30, 2)
            self.numplayers.place(relx = 0.14, rely = 0.6, anchor = 'nw')
            self.sessionscompl = tkLabel("Sessions Completed\n(262 Trades & 311 Blaze Kills)", "white", "black", 30, 2)
            self.sessionscompl.place(relx = 0.35, rely = 0.6, anchor = 'nw')
            self.ingametime = tkLabel("In Game Time Per Player\n(Only Bartering & Killing Blazes)", "white", "black", 35, 2)
            self.ingametime.place(relx = 0.61, rely = 0.6, anchor = 'nw')

            self.singlep1 = tkLabel("1", "#c32728", "black", 15, 2)
            self.singlep1.place(relx = 0.20, rely = 0.695, anchor = 'nw')
            self.speedyp1 = tkLabel("2,789", "#fed667", "black", 15, 2)
            self.speedyp1.place(relx = 0.20, rely = 0.795, anchor = 'nw')
            self.allp1 = tkLabel("126,000,000", "#62b853", "black", 15, 2)
            self.allp1.place(relx = 0.20, rely = 0.895, anchor = 'nw')

            self.singlepr = tkLabel("0", "#c32728", "black", 15, 2)
            self.singlepr.place(relx = 0.415, rely = 0.695, anchor = 'nw')
            self.speedypr = tkLabel("0", "#fed667", "black", 15, 2)
            self.speedypr.place(relx = 0.415, rely = 0.795, anchor = 'nw')
            self.allpr = tkLabel("0", "#62b853", "black", 15, 2)
            self.allpr.place(relx = 0.415, rely = 0.895, anchor = 'nw')

            self.singlept = tkLabel("0", "#c32728", "black", 40, 2)
            self.singlept.place(relx = 0.59, rely = 0.695, anchor = 'nw')
            self.speedypt = tkLabel("0", "#fed667", "black", 40, 2)
            self.speedypt.place(relx = 0.59, rely = 0.795, anchor = 'nw')
            self.allpt = tkLabel("0", "#62b853", "black", 40, 2)
            self.allpt.place(relx = 0.59, rely = 0.895, anchor = 'nw')

            self.img1 = tk.Label(image=self.enderRender, borderwidth=0, highlightthickness=0)
            self.img1.image = self.enderRender
            self.img1.place(relx = 0.25, rely = 0.2, anchor = 'nw')

            self.img2 = tk.Label(image=self.blazeRender, borderwidth=0, highlightthickness=0)
            self.img2.image = self.blazeRender
            self.img2.place(relx = 0.25, rely = 0.3, anchor = 'nw')


            # add something to axes
            self.ax1 = plt.axes()
            # set limits
            plt.xlim(0,20)
            plt.ylim(0,220)
            self.ax1.tick_params(labelbottom=False)
            plt.title("Random Ender Pearl & Blaze Rod Luck vs. Dream Luck.", fontsize=20)
            plt.xlabel("{:,}".format((totalCount.value*100)) + "+ Simulations Completed.", fontsize=18)


            self.ax1.plot([0, 20], [211, 211], color='#bf5a00', marker='_', label="Dream Blaze Rod Luck")
            self.ax1.plot([0, 20], [42, 42], color='#2dcdb1', marker='_', label="Dream Ender Pearl Luck")
            plt.legend(loc = 'center right')

            self.window.after(200, self.refresh, biggest, totalCount, over30, over40, blaze_biggest, blaze_over200, dreamLuck, ss_ep, ss_br, False, 0, 0, 0, ss_cmo, ender_sample1, blaze_sample1, ender_sample2, blaze_sample2, ender_sample3, blaze_sample3, 0, self.ax1)
            self.window.mainloop()

            if dreamLuck.value >= 1:
                print("\n\nDREAM LUCK REACHED! IT ONLY TOOK " + str(totalCount.value*100) + " ATTEMPTS!")
                print("HIGHEST ENDER PEARL BARTER DROP RATE: " + str(biggest.value))
                print("HIGHEST BLAZE ROD DROP RATE: "+ str(blaze_biggest.value))
                print("AND IT ONLY TOOK: " + str(t1-t0) + " SECONDS LMAO")
                return 0

        except StopIteration:
            self.window.destroy()

    def refresh(self, biggest, totalCount, over30, over40, blaze_biggest,
        blaze_over200, dreamLuck, ss_ep, ss_br, destroy, endercycles, blazecycles,
        combinedcycles, ss_cmo, ender_sample1, blaze_sample1, ender_sample2,
        blaze_sample2, ender_sample3, blaze_sample3, counter, ax1):
        dream_runs = 23
        wr_run_t2b = 10*60+30
        t1 = time.time()

        if destroy == True:
            time.sleep(30000000)
            self.window.quit()
        try:
            self.bigender.config(text=str(biggest.value))
            self.bigblaze.config(text=str(blaze_biggest.value))

            self.bigboth1.config(text=str(ss_ep.value))
            self.bigboth3.config(text=str(ss_br.value))

            self.over3040.config(text="30 or more: " + str(over30.value) + "\n40 or more: " + str(over40.value))
            self.over200.config(text="200 or more: " + str(blaze_over200.value))

            self.combinedoverxb.config(text="190 or more blaze: " + str(ss_cmo.value))

            timeLeftEnder = endercycles
            if biggest.value >= dream_ep and endercycles == 0:
                endercycles =  "COMPLETED! Took " + str(display_time(t1-t10)) + " and\n" + str(totalCount.value*100) + " simulations to reach 42."
                timeLeftEnder = endercycles

            else:
                if endercycles == 0:
                    timeLeftEnder = str(display_time((40000000000/240000 - totalCount.value*100/240000)))

            timeLeftBlaze = blazecycles
            if blaze_biggest.value >= dream_blaze and blazecycles == 0:
                blazecycles =  "COMPLETED! Took " + str(display_time(t1-t10)) + " and\n" + str(totalCount.value*100) + " simulations to reach 211."
                timeLeftBlaze = blazecycles
            else:
                if blazecycles == 0:
                    timeLeftBlaze = str(display_time((77000000000/240000 - totalCount.value*100/240000)))

            timeCombined = combinedcycles
            if dreamLuck.value >= 1 and combinedcycles == 0:
                combinedcycles =  "COMPLETED! Took " + str(display_time(t1-t10)) + "and\n" + str(totalCount.value*100) + " simulations to reach 42 & 211."
                timeCombined = combinedcycles
            else:
                if combinedcycles == 0:
                    timeCombined = str(display_time(((77000000000*40000000000)/240000 - totalCount.value*100/240000)))

            self.tend.config(text=timeLeftEnder)
            self.tblaze.config(text=timeLeftBlaze)
            self.tcombined.config(text=timeCombined)

            self.singlepr.config(text="{:,}".format((round(totalCount.value*100))))
            self.speedypr.config(text="{:,}".format((round(totalCount.value*100/2789))))
            self.allpr.config(text="{:,}".format((round(totalCount.value*100/126000000))))

            self.singlept.config(text=str(display_time(round(totalCount.value*100*dream_runs*wr_run_t2b))))
            self.speedypt.config(text=str(display_time(round(totalCount.value*100/2789*dream_runs*wr_run_t2b))))
            self.allpt.config(text=str(display_time(round(totalCount.value*100/126000000*dream_runs*wr_run_t2b))))

            self.img1 = tk.Label(image=self.enderRender, borderwidth=0, highlightthickness=0)
            self.img1.image = self.enderRender
            self.img1.place(relx = 0.25, rely = 0.2, anchor = 'nw')

            self.img2 = tk.Label(image=self.blazeRender, borderwidth=0, highlightthickness=0)
            self.img2.image = self.blazeRender
            self.img2.place(relx = 0.25, rely = 0.3, anchor = 'nw')
            # add something to axes

            self.ax1.scatter([counter], [blaze_sample1.value], color='#bf5a00', marker='^', label = "Blaze Rod Sample Luck")
            self.ax1.scatter([counter], [blaze_sample2.value], color='#bf5a00', marker='^')
            self.ax1.scatter([counter], [blaze_sample3.value], color='#bf5a00', marker='^')

            self.ax1.scatter([counter], [ender_sample1.value], color='#2dcdb1', marker='o', label = "Ender Pearl Sample Luck")
            self.ax1.scatter([counter], [ender_sample2.value], color='#2dcdb1', marker='o')
            self.ax1.scatter([counter], [ender_sample3.value], color='#2dcdb1', marker='o')


            if counter == 0:
                plt.legend(loc = 'center right')
            counter += 1
            # draw the plot
            plt.draw()
            plt.pause(0.01) #is necessary for the plot to update for some reason

            if counter % 20 == 0:
                plt.cla()
                plt.xlim(0,20)
                plt.ylim(0,220)
                self.ax1.tick_params(labelbottom=False)
                plt.title("Random Ender Pearl & Blaze Rod Luck vs. Dream Luck.", fontsize=20)
                plt.xlabel("{:,}".format((totalCount.value*100)) + "+ Simulations Completed.", fontsize=18)

                self.ax1.plot([0, 20], [211, 211], color='#bf5a00', marker='_', label="Dream Blaze Rod Luck")
                self.ax1.plot([0, 20], [42, 42], color='#2dcdb1', marker='_', label="Dream Ender Pearl Luck")
                plt.legend(loc = 'center right')
                counter = 0

            if dreamLuck.value >= 1:
                endercycles =  "COMPLETED! Took " + str(display_time(t1-t10)) + "\nand " + str(totalCount.value*100) + " simulations."
                timeLeftEnder = endercycles

                blazecycles =  "COMPLETED! Took " + str(display_time(t1-t10)) + "\nand " + str(totalCount.value*100) + " simulations."
                timeLeftBlaze = blazecycles

                combinedcycles =  "COMPLETED! Took " + str(display_time(t1-t10)) + "\nand " + str(totalCount.value*100) + " simulations."
                timeCombined = combinedcycles

                self.tend.config(text=timeLeftEnder)
                self.tblaze.config(text=timeLeftBlaze)
                self.tcombined.config(text=timeCombined)

                self.wTitle = tkLabel("DREAM LUCK REACHED! FINAL DROP RATE DATA", "white", "black", 60, 2)
                self.wTitle.config(font=("Courier", 24, 'bold'))
                self.wTitle.place(relx = 0.10, rely = 0.03, anchor = 'nw')
                self.sTitle = tkLabel("DREAM LUCK REACHED! FINAL NEEDED PLAY TIME", "white", "black", 60, 2)
                self.sTitle.config(font=("Courier", 24, 'bold'))
                self.sTitle.place(relx = 0.20, rely = 0.48, anchor = 'nw')
                self.window.after(200, self.refresh, biggest, totalCount, over30, over40, blaze_biggest, blaze_over200, dreamLuck, ss_ep, ss_br, True, endercycles, blazecycles, combinedcycles, ss_cmo, ender_sample1, blaze_sample1, ender_sample2, blaze_sample2, ender_sample3, blaze_sample3, counter, ax1)
            else:
                self.window.after(200, self.refresh, biggest, totalCount, over30, over40, blaze_biggest, blaze_over200, dreamLuck, ss_ep, ss_br, False, endercycles, blazecycles, combinedcycles, ss_cmo, ender_sample1, blaze_sample1, ender_sample2, blaze_sample2, ender_sample3, blaze_sample3, counter, ax1)
        except StopIteration:
            window.destroy()

def display(biggest, totalCount, over30, over40, blaze_biggest, blaze_over200, dreamLuck, ss_ep, ss_br, ss_cmo, ender_sample1, blaze_sample1, ender_sample2, blaze_sample2, ender_sample3, blaze_sample3):
    t0 = time.time()
    dream_runs = 23
    wr_run_t2b = 10*60+30

    while True:
        time.sleep(0.5)
        t1 = time.time()
        d = dreamGUI(biggest, totalCount, over30, over40, blaze_biggest, blaze_over200, dreamLuck, ss_ep, ss_br, ss_cmo, ender_sample1, blaze_sample1, ender_sample2, blaze_sample2, ender_sample3, blaze_sample3)

        if dreamLuck.value >= 1:
            print("\n\nDREAM LUCK REACHED! IT ONLY TOOK " + str(totalCount.value*100) + " ATTEMPTS!")
            print("HIGHEST ENDER PEARL BARTER DROP RATE: " + str(biggest.value))
            print("HIGHEST BLAZE ROD DROP RATE: "+ str(blaze_biggest.value))
            print("AND IT ONLY TOOK: " + str(t1-t0) + " SECONDS LMAO")
            return 0

if __name__ == "__main__":
    # input list
    # creating new process
    luckiest = multiprocessing.Value('i',0)
    totalCount = multiprocessing.Value('i',0)
    over_30 = multiprocessing.Value('i',0)
    over_40 = multiprocessing.Value('i',0)
    bluckiest = multiprocessing.Value('i',0)
    bover_200 = multiprocessing.Value('i',0)
    ss_ender = multiprocessing.Value('i',0)
    ss_blaze = multiprocessing.Value('i',0)
    dluck = multiprocessing.Value('i',0)
    ss_combined = multiprocessing.Value('i',0)

    p1_sample_ender = multiprocessing.Value('i',0)
    p1_sample_blaze = multiprocessing.Value('i',0)
    p2_sample_ender = multiprocessing.Value('i',0)
    p2_sample_blaze = multiprocessing.Value('i',0)
    p3_sample_ender = multiprocessing.Value('i',0)
    p3_sample_blaze = multiprocessing.Value('i',0)


    p1 = multiprocessing.Process(target=attempts, args=(1,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,p1_sample_ender, p1_sample_blaze,))
    p2 = multiprocessing.Process(target=attempts, args=(2,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,p2_sample_ender, p2_sample_blaze,))
    p3 = multiprocessing.Process(target=attempts, args=(3,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,p3_sample_ender, p3_sample_blaze,))
    p4 = multiprocessing.Process(target=attempts, args=(4,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,None, None,))
    p5 = multiprocessing.Process(target=attempts, args=(5,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,None, None,))
    p6 = multiprocessing.Process(target=attempts, args=(6,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,None, None,))
    p7 = multiprocessing.Process(target=attempts, args=(7,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,None, None,))
    p8 = multiprocessing.Process(target=attempts, args=(8,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,None, None,))
    p9 = multiprocessing.Process(target=attempts, args=(9,luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined,None, None,))
    p10 = multiprocessing.Process(target=display, args=(luckiest,totalCount,over_30,over_40,bluckiest,bover_200,dluck,ss_ender,ss_blaze,ss_combined, p1_sample_ender, p1_sample_blaze,p2_sample_ender, p2_sample_blaze,p3_sample_ender, p3_sample_blaze,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()
    t11 = time.time()
    print("TIME " +str(t11-t10))
