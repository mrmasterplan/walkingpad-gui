import asyncio

from walkingpad_gui.window import Window


class App:
    def __init__(self):
        self.scan_timeout = 5000
    async def main(self):
        self.window = Window(asyncio.get_event_loop())

        while True:
            await self.window.update()
            await asyncio.sleep(.05)

def main():
    print('hi')
    asyncio.run(App().main())

if __name__ == "__main__":
    main()