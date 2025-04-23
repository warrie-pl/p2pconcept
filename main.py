import socket
import threading


def listen_for_messages(conn):
    while True:
        try:
            message = conn.recv(1024).decode()
            if message:
                print(f"\nPeer: {message}")
            else:
                print("Connection closed by the peer.")
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[+] Listening on {host}:{port}...")
    conn, addr = server.accept()
    print(f"[+] Connection established with {addr}")
    return conn


def connect_to_peer(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"[+] Connected to {host}:{port}")
    return client


def peer_mode():
    choice = input("Do you want to [h]ost or [c]onnect? ")
    if choice.lower() == 'h':
        conn = start_server('0.0.0.0', 12345)
    else:
        target_ip = input("Enter the IP address of the peer: ")
        conn = connect_to_peer(target_ip, 12345)

    threading.Thread(target=listen_for_messages,
                     args=(conn,), daemon=True).start()
    while True:
        msg = input("You: ")
        if msg.lower() == 'exit':
            print("Exiting...")
            conn.close()
            break
        conn.send(msg.encode())


#TODO: Implement it in a main project


if __name__ == "__main__":
    peer_mode()