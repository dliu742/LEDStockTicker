# LEDStockTicker
Using LEDs to display stock tickers

Hardware required:
Raspberry Pi
WS2812B RGB LED Boards
5V Power Supply

Connections:
Raspberry Pi data connects to GPIO 18 which will be the data pin to the LED boards
Connect the ground of the power supply, the board and raspberry pi together

Software:
sudo pip3 install rpi_ws281x
sudo pip3 install adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka
sudo apt-get install python3-numpy
sudo apt-get install python3-pandas
sudo pip3 install yfinance
   - yfinance will install the newest version of numpy, which does not work with the raspberry pi. It is necessary to uninstall the newest numpy
   - sudo pip3 uninstall numpy
   - sudo pip3 uninstall pandas
Configure the raspberry pi to enable GPIO communication

Folder configuration:
