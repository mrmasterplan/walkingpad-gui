import asyncio
import tkinter as tk
from async_tkinter_loop import async_handler, async_mainloop
from ph4_walkingpad import pad
from ph4_walkingpad.pad import Scanner, WalkingPad, WalkingPadCurStatus, WalkingPadLastStatus, Controller
from ph4_walkingpad.utils import setup_logging

class MyController(Controller):
    status: WalkingPadCurStatus
    def on_cur_status_received(self, sender, status: WalkingPadCurStatus):
        """Override to receive current status"""
        self.status = status
        print(status)

class CounterApp:

    def __init__(self, root):
        super().__init__()
        self.root = root
        self.scanner = Scanner()
        self.ctler = MyController()

        self.speed = 20

        # Create and pack the buttons
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.pack(fill=tk.X)

        self.mode_button = tk.Button(self.root, text="Mode: Off", command=self.toggle_mode)
        self.mode_button.pack(fill=tk.X)

        self.speed_up_button = tk.Button(self.root, text="Speed Up", command=self.speed_up)
        self.speed_up_button.pack(fill=tk.X)

        self.start_stop_button = tk.Button(self.root, text="Start", command=self.start_stop)
        self.start_stop_button.pack(fill=tk.X)

        self.speed_down_button = tk.Button(self.root, text="Speed Down", command=self.speed_down)
        self.speed_down_button.pack(fill=tk.X)

    @async_handler
    async def connect(self):
        self.connect_button.config(text=f"Connecting ...")
        await self.scanner.scan()
        print(len(self.scanner.walking_belt_candidates), "candidates found")
        cand = self.scanner.walking_belt_candidates[0]
        print(cand)
        await self.ctler.run(cand)
        self.stats()
        # Implement connection logic here
        self.connect_button.config(text=f"Connected to {cand.name}")

    @async_handler
    async def stats(self):
        while True:
            await self.ctler.ask_stats()
            await asyncio.sleep(0.3)

    @async_handler
    async def toggle_mode(self):
        mode = self.ctler.status.manual_mode
        if mode !=1:
            await self.ctler.switch_mode(WalkingPad.MODE_MANUAL)
            self.mode_button.config(text=f"Manual")
        else:
            await self.ctler.switch_mode(WalkingPad.MODE_AUTOMAT)
            self.mode_button.config(text=f"Automatic")

    @async_handler
    async def speed_up(self):
        self.speed+=5
        await self.ctler.change_speed(self.speed)

    @async_handler
    async def speed_down(self):
        self.speed-=5
        await self.ctler.change_speed(self.speed)

    @async_handler
    async def start_stop(self):
        await self.ctler.start_belt()

def main():
    root = tk.Tk()
    app = CounterApp(root)
    async_mainloop(root)
