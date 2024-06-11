import data_handler
import api_server
import time

if __name__ == "__main__":
    data_handler.start_data_thread()
    api_server.start_api_thread()

    while True:
        time.sleep(1)  # Keep the main thread alive
