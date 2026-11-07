import asyncio
import tkinter as tk
from async_tkinter_loop import async_handler, async_mainloop
from ph4_walkingpad.pad import Scanner, WalkingPad, WalkingPadCurStatus, Controller

class MyController(Controller):
    def __init__(self):
        super().__init__()
        self.status = None

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

        self.mode_button = tk.Button(self.root, text="Mode: Unknown", command=self.toggle_mode, state=tk.DISABLED)
        self.mode_button.pack(fill=tk.X)

        self.speed_up_button = tk.Button(self.root, text="Speed Up", command=self.speed_up, state=tk.DISABLED)
        self.speed_up_button.pack(fill=tk.X)

        self.start_stop_button = tk.Button(self.root, text="---", command=self.start_stop, state=tk.DISABLED)
        self.start_stop_button.pack(fill=tk.X)

        self.speed_down_button = tk.Button(self.root, text="Speed Down", command=self.speed_down, state=tk.DISABLED)
        self.speed_down_button.pack(fill=tk.X)

        # add hotkeys
        self.root.bind("<Up>", lambda event: self.speed_up())
        self.root.bind("<Down>", lambda event: self.speed_down())
        self.root.bind("<space>", lambda event: self.start_stop())

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
        self.connect_button.config(text=f"Connected to {cand.name}", state=tk.DISABLED)

    @async_handler
    async def stats(self):
        last_stat = None
        while True:
            await self.ctler.ask_stats()
            await asyncio.sleep(0.3)
            if last_stat == self.ctler.status:
                continue
            last_stat = self.ctler.status

            modes = {
                1:"Manual",
                2:"Off",
                3:"Mode3",
                0:"Automatic"
            }
            self.mode_button.config(text=modes.get(self.ctler.status.manual_mode,"Unknown"),state=tk.NORMAL)
            if self.ctler.status.manual_mode == 1:
                states = {
                    0:"Start",
                    1:"Stop"
                }
                self.start_stop_button.config(text=states.get(self.ctler.status.belt_state,"Unknown"), state=tk.NORMAL)
                self.speed_up_button.config(state=tk.NORMAL)
                self.speed_down_button.config(state=tk.NORMAL)
            else:
                self.start_stop_button.config(text="---", state=tk.DISABLED)
                self.speed_up_button.config(state=tk.DISABLED)
                self.speed_down_button.config(state=tk.DISABLED)


    @async_handler
    async def toggle_mode(self):
        mode = self.ctler.status.manual_mode
        if mode !=1:
            await self.ctler.switch_mode(WalkingPad.MODE_MANUAL)
            # self.mode_button.config(text=f"Manual")
        else:
            await self.ctler.switch_mode(WalkingPad.MODE_AUTOMAT)
            # self.mode_button.config(text=f"Automatic")

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
