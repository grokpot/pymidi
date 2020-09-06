# Clean up files and ports that I probabaly forgot to close
gc.collect()

import network
import machine
import socket
import time
from machine import ADC

WLAN_SSID = ''
WLAN_PW = ''

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(WLAN_SSID, WLAN_PW)
    while not wlan.isconnected():
        pass
print(wlan.ifconfig())
device_ip = wlan.ifconfig()[0]
print('Device IP:', device_ip)

pin = machine.Pin(32, machine.Pin.IN)
adc = ADC(pin)
# Calibrate ADC
# set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
adc.atten(ADC.ATTN_11DB)
# set 9 bit return values (returned range 0-511)
adc.width(ADC.WIDTH_9BIT)

HOST = device_ip
PORT = 12345    # Needs to match client

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    # Wait for new connections
    while True:
        s.listen(1)
        conn, addr = s.accept()
        print('Connected by', addr)
        # Wait for query
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(str(adc.read()).encode())
except KeyboardInterrupt:
    pass  # suppress keyboard interrupt traceback
finally:
    conn.close()
    s.close()
