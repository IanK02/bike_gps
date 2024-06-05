const express = require('express');
const bodyParser = require('body-parser');
const puppeteer = require('puppeteer');
const jimp = require('jimp');
const app = express();
const port = 3000;
const sleep = ms => new Promise(res => setTimeout(res, ms));

//Express server to receieve coordinates from the gps module
app.use(bodyParser.json());
app.post('/coordinates', async (req, res) => {
  const { lati, long, zoom } = req.body;
  console.log(`Received coordinates: Lat ${lati}, Lng ${long}, Zoom ${zoom}`);
  await takeMapScreenshot(lati, long, 17, 'pic.png')
            .then(() => console.log('Map screenshot captured'))
            .catch(error => console.error('Error capturing map screenshot:', error));
  res.send({ message: 'Screenshot taken' });
});

//Pans the map to the given coordinates and the given zoom level, takes a screenshot, then saves it
//as 'screenshot.png', which is then converted to a black and white .bmp named 'pic.bmp', this path
//is the outputPath parameter
async function takeMapScreenshot(lati, long, zoom, outputPath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 400, height: 240 });
  await page.goto('http://127.0.0.1:5500/map_website.html');
  await page.waitForFunction(() => window.google && window.google.maps);
  await page.evaluate((lati, long, zoom) => {
    console.log(lati);
    console.log(long);
    map.panTo(new google.maps.LatLng(lati, long));
    map.setZoom(zoom);
  }, lati, long, zoom);
  await sleep(2000);
  await page.screenshot({path: 'screenshot.png'});
  await browser.close();
  await convertToBlackAndWhite('screenshot.png', outputPath);
}

//Converting the image to black and white in an effort to save RAM
async function convertToBlackAndWhite(inputPath, outputPath) {
  const image = await jimp.read(inputPath);
  image.grayscale();
  await image.writeAsync(outputPath);
  console.log('Black and white image saved');
}

//Start the express server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
