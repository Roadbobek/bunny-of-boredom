import socket

HOST = "127.0.0.1"
PORT = 33742

def run_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to bnuy at {HOST}:{PORT}")
            print("Type '/exit' to quit this client.")
            print("Press 'ENTER' or type '/cls' to clear the bnuy text.")
            print("Type '/shutdown' to shut down the server.")
            print("Enter text to update:")

            while True:
                msg = input("bnuy> ")
                if msg.lower() == "/exit":
                    break
                if not msg.strip():
                    s.sendall("/cls".encode('utf-8'))
                
                s.sendall(msg.encode('utf-8'))

    except ConnectionRefusedError:
        print(f"Could not connect to {HOST}:{PORT}. Make sure the bunny script is running first!")
    except KeyboardInterrupt:
        print("\nDisconnecting...")

if __name__ == "__main__":
    run_client()