import os
import time
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import displayio
import displayio
import busio
import sharpdisplay
import adafruit_imageload
import framebufferio
from io import BytesIO
import adafruit_gps
import gc

#Run garbage collector
gc.collect()

#Connect to SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
#--------------------------------------------------------------------------------------------------
#Initialize Display
displayio.release_displays()
bus = busio.SPI(board.GP14, MOSI=board.GP15)
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, board.GP13, 400, 240)
display = framebufferio.FramebufferDisplay(framebuffer, auto_refresh = True)
#--------------------------------------------------------------------------------------------------
#Send GPS coordinates to express server
RX = board.GP17
TX = board.GP16
uart = busio.UART(TX, RX, baudrate=9600, timeout=30)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')
last_print = time.monotonic()
while True:
    gps.update()
    current = time.monotonic()
    if current - last_print >= 5.0:
        gc.collect()
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
            continue
        print('=' * 40) 
        lat = gps.latitude
        long = gps.longitude
        rounded_lat = round(gps.latitude, 9)
        rounded_lng = round(gps.longitude, 9)
        lat_str = "{:.9f}".format(rounded_lat)
        lng_str = "{:.9f}".format(rounded_lng)
        print('Latitude ' + lat_str)
        print('Longitude ' + lng_str)
        NODE_SERVER_URL = 'http://127.0.0.1:3000'
        try:
            print('trying to send')
            response = requests.post(f'{NODE_SERVER_URL}/coordinates', json={'lati': lat_str, 'long': lng_str, 'zoom': 12})
            response.close()
            print('coordinates sent successfully')
            bitmap_url = 'http://127.0.0.1:5500/pic.bmp'
            response = requests.get(bitmap_url, timeout=10)
            img_data = BytesIO(response.content)
            image, palette = adafruit_imageload.load(img_data)
            tile_grid = displayio.TileGrid(image, pixel_shader=palette)
            group = displayio.Group()
            group.append(tile_grid)
            display.root_group = group
        except Exception as e:
            print('Error sending request:', e)
        gc.collect()




