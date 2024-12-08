import GPIOServer

if __name__ == "__main__":
    try:
        app = GPIOServer.GPIOServerApp()
        app.getRoot().mainloop()
    except KeyboardInterrupt:
        print("Terminated by User!")
