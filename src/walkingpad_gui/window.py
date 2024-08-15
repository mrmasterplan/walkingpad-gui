import asyncio
import tkinter as tk
from tkinter import ttk

from ph4_walkingpad.pad import Scanner


class Window(tk.Tk):
    def __init__(self, loop):
        self.loop = loop
        self.root = tk.Tk()
        self.animation = "░▒▒▒▒▒"
        self.label = tk.Label(text="")
        self.label.grid(row=0, columnspan=2, padx=(8, 8), pady=(16, 0))
        self.progressbar = ttk.Progressbar(length=280)
        self.progressbar.grid(row=1, columnspan=3, padx=(8, 8), pady=(16, 0))
        button_block = tk.Button(text="Calculate Sync", width=10, command=self.calculate_sync)
        button_block.grid(row=2, column=0, sticky=tk.W, padx=8, pady=8)
        button_non_block = tk.Button(text="Calculate Async", width=10, command=lambda: self.loop.create_task(self.calculate_async()))
        button_non_block.grid(row=2, column=1, sticky=tk.W, padx=8, pady=8)
        button_non_block = tk.Button(text="Scan", width=10, command=lambda: self.loop.create_task(self.scan()))
        button_non_block.grid(row=2, column=2, sticky=tk.W, padx=8, pady=8)

    async def scan(self):
        print("initializing scan")
        scanner = Scanner()
        print("starting scan")
        await scanner.scan(timeout=10)

        print("finished scan")

        if scanner.walking_belt_candidates:
            candidates = scanner.walking_belt_candidates
            print("WalkingPad candidates: %s" % (candidates,))


            # if self.args.address_filter:
            #     candidates = [x for x in candidates if str(x.address).startswith(self.args.address_filter)]
            # return candidates[0] if candidates else None

    async def update(self):
        self.label["text"] = self.animation
        self.animation = self.animation[1:] + self.animation[0]
        self.root.update()

    def calculate_sync(self):
        max = 3000000
        for i in range(1, max):
            self.progressbar["value"] = i / max * 100

    async def calculate_async(self):
        max = 3000000
        for i in range(1, max):
            self.progressbar["value"] = i / max * 100
            if i % 1000 == 0:
                await asyncio.sleep(0)
