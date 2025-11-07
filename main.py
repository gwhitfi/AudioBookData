import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from datetime import datetime


filesDict = {}
badFileNames = []
fileCounter = 0

path = os.path.join(os.getcwd(), "data")
csv_files = glob.glob(os.path.join(path, "*.csv"))


def getFileNameInfo(file, fileCounter):
    try:
        filePath = os.path.basename(file)
        fileDate = filePath.split("-")[1]
        fileMonth = fileDate[4:6]
        fileDay = fileDate[6:8]
        fileYear = fileDate[:4]
        filesDict[fileCounter] = {
            "month": fileMonth,
            "day": fileDay,
            "year": fileYear,
            "full-date": f"{fileMonth}-{fileDay}-{fileYear}",
            "path": file,
            "minutes": 0,
            "listens": 0,
        }
    except Exception as e:
        badFileNames.append(os.path.basename(file))
        print(f"Error parsing file name for: {os.path.basename(file)}  - {e}")


def getFileData(key, path):
    df = pd.read_csv(path)
    df = df[
        [
            "Listener Country",
            "Total Minutes Listened",
            "Complete Listen Equivalents (Total Minutes / Length of Book)",
        ]
    ]
    df.columns = ["Country", "Minutes", "Listens"]
    filesDict[key]["minutes"] = round(df["Minutes"].sum())
    filesDict[key]["listens"] = round(df["Listens"].sum())


def plotData(dates, minutes, listens):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

    ax1.plot(dates, minutes, marker="o")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Minutes")
    ax1.set_title("Total Minutes Listened")
    ax1.tick_params(axis="x", rotation=90)

    ax2.plot(dates, listens, marker="o")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Listens")
    ax2.set_title("Total Complete Listens")
    ax2.tick_params(axis="x", rotation=90)
    plt.tight_layout()
    plt.show()


for file in csv_files:
    getFileNameInfo(file, fileCounter)
    fileCounter += 1

for key, fileInfo in filesDict.items():
    getFileData(key, fileInfo["path"])


def year_to_date():
    dates = [
        f"{v["month"]}-{v["day"]}-{v["year"]}"
        for v in filesDict.values()
        if v["year"] == str(datetime.now().year)
    ]
    minutes = [
        v["minutes"]
        for v in filesDict.values()
        if v["year"] == str(datetime.now().year)
    ]
    listens = [
        v["listens"]
        for v in filesDict.values()
        if v["year"] == str(datetime.now().year)
    ]
    plotData(dates, minutes, listens)


def all_data():
    dates = [f"{v["month"]}-{v["day"]}-{v["year"]}" for v in filesDict.values()]
    minutes = [v["minutes"] for v in filesDict.values()]
    listens = [v["listens"] for v in filesDict.values()]
    plotData(dates, minutes, listens)


def from_starting_date(startDate):
    key = next((k for k, v in filesDict.items() if v["full-date"] == startDate), None)
    from_start = sorted((k, v) for k, v in filesDict.items() if k >= key)
    dates = [f"{v["month"]}-{v["day"]}-{v["year"]}" for _, v in from_start]
    minutes = [v["minutes"] for _, v in from_start]
    listens = [v["listens"] for _, v in from_start]
    plotData(dates, minutes, listens)


root = tk.Tk()
root.title("Achieve It - AudioBook Data")
root.geometry("200x150")

allDates = [f"{v["month"]}-{v["day"]}-{v["year"]}" for v in filesDict.values()]
frame = ttk.Frame(root, padding=0)
frame.pack(expand=True)

starting_date = ttk.Combobox(root, state="readonly", values=allDates, width=25)
starting_date.pack(pady=5)

ytd_button = ttk.Button(
    root,
    text="From Starting Date",
    command=lambda: from_starting_date(starting_date.get()),
)
ytd_button.pack(pady=5, ipadx=10, ipady=3)
ytd_button.config(width=25)

ytd_button = ttk.Button(root, text="YTD", command=year_to_date)
ytd_button.pack(pady=5, ipadx=10, ipady=3)
ytd_button.config(width=25)

all_data_button = ttk.Button(root, text="All Data", command=all_data)
all_data_button.pack(pady=5, ipadx=10, ipady=3)
all_data_button.config(width=25)

root.mainloop()
