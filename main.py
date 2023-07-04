from multiprocessing import freeze_support

import scanner
import handler

if __name__ == "__main__":
    freeze_support()

    try:
        scanner_process, data_queue = scanner.start_process()
        handler.start(data_queue) # blocks
    except Exception as e:
        print(e)
    finally:
        scanner_process.terminate()

