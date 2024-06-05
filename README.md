# Bike GPS
## The proposal
I wanted to make a small gps that could attatch to the handlebars of my bike. It had to be small and light, similar in size to either a [Wahoo ELEMNT](https://www.wahoofitness.com/devices/bike-computers/elemnt-roam-buy)
or a [Garmin Edge 540](https://www.garmin.com/en-US/p/798925). I wanted to keep the price under $60 and keep hardware to a minimum and preferably avoid having to make a pcb.
![Wahoo ELEMNT V2](https://flowmountainbike.com/wp-content/uploads/2023/05/Wahoo-Elemnt-Bolt-V2-GPS-07422.jpg)
## First Attempt
My first attempt at the project was made with a Raspberry Pi Pico W, Adafruit Sharp Memory Display, and ublox neo-6m gps module. The workings of the gps would be as follows.
1. Every 5 seconds the Raspberry Pi Pico W receives coordinates from the gps module, and then sends those coordinates as JSON data to an express server running
   on a computer.
2. Using the Pupeteer library by the Google Chrome team the script would navigate to a website(also hosted on the computer) that displayed the desired ride
   route on Google Maps, using the Google Maps API. The pupeteer script would then pan on the map to the coordinates received from the gps and take a screenshot
   of the map, which it then uploaded to the website as a .bmp file.
3. Now that the screenshot of the map at the current location of the gps was on the website, the Raspberry Pi Pico W would fetch the image with an HTTPS GET
   request and then display it on the Adafruit Sharp Memory Display.

## The Prototype
![First Bike GPS Prototype](/first_gps_prototype.jpg)

### The Issues
I knew straight from the start that the Raspberry Pi Pico W would not be nearly strong enough to handle the work of rendering a route on a map,
being only a microcontroller its resources are extremely limited. That is why I decided to outsource the job of loading a displaying a route on a map
to a website. This way I could give the illusion of a proper GPS displaying your location, a map, and a route, all while only using a microcontroller. And this
nearly worked, I had a prototype that could send gps coordinates, pan to the proper coordinates on the map, take a screenshot, then upload it to the website.
The issue however came in the Raspberry Pi Pico W retreiving the image from the website and then displaying it on the physical display. The Pico W comes with 
only 264kb of RAM, and after having imported all the neccessary packages and initialized the disply there was simply not enough RAM left to retrieve the image.
I tried to send the image in small chunks to save RAM. The display I was using was 400x240 and I found that for the Pico W to retrieve the images they had to
be a slim 40x240, meaning it would take 10 of these little chunks to create a full image on the display. I decided to abandon the idea as I was worried that by the  
time the gps was done taking 10 screenshots, uploading those ten screenshots, and displaying those ten screenshots side by side on the screen to make one cohesive image the
gps would already have refreshed and instead of seeing one image of their location the rider would see 10 of these sub images constantly being loaded and refreshed,
all out of sync and providing no valuable information. The code currently in the repository is my attempt at the gps with the Pico W, note that it does not work. The
circuitpy_gps.py file that was running on Circuit Python 9.0.4 on my Pico W will encounter a Memory Error in line 65, being unable to allocate enough RAM to retrieve
the image from the website. 

### Next Steps
This project is still ongoing, I've learned that the issues lie in the computing capabilities of the Raspberry Pi Pico W. As such I've decided to switch to a
[Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) to serve as the brains of the gps. It's a full fledged computer as opposed
to a microcontroller and I am hoping that with this I won't have to outsource the rendering work to a website, and instead the gps can be self contained, not relying
on any external computers or servers to work. This should make the development process much, much easier as I won't have to juggle web development and programming the
gps, and I won't be limited to only using Circuit Python as I was on the Pico W. I'm excited to see what the Raspberry Pi Zero 2 W is capable of and if I can
still achieve my goal of creating a small, light, and cheap GPS for my bike. 
