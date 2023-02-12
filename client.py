import mido
import socket
import time

HOST = '10.1.1.160'
PORT = 12345 # needs to match host

def runit():
    with mido.open_output('IAC Driver Bus 1') as port:
        note = 50
        port.send(mido.Message('note_on', note=note, velocity=50))
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((HOST, PORT))
                while True:
                    s.sendall(b'ping')
                    data_raw = s.recv(1024)
                    data = int(data_raw.decode())
                    data_converted = int(data * 16000 / 511) - 8000
                    # print("Converted value:", data_converted)
                    pitch = data_converted
                    port.send(mido.Message('pitchwheel', pitch=pitch))
                    time.sleep(.05)
        except Exception:
            pass
        finally:
            port.send(mido.Message('note_off', note=note))