# diggerz.io-bot
Automated grinding, using Selenium WebDriver in order to dig out items, that can later be collected.

The code is written in python 3(which you need to install, if you want to use this software).
It will open the browser game diggerz.io, using Chromedriver(which you need to install, if you want to use this software).
Responsive to commands in the terminal such as: pause, unpause, restart, trade.
The bot will pick a random username out of a large username-collection from another file.
It will also set its flag to a random one out of some popular ones
After enetering the game it will imitate a real person by jumping, moving, digging around.
After getting done with imitating a person it will enter the private lobby and go on to dig a large part of the map.
After being done it will refresh the browser and repeat.
It will also let you know in the termnial what it is currently doing.
If a disconnection occurs, the bot can be restarted by using the command "restart" or just waiting untill the loop repeasts by itself.
You will also need to install Selenium Webdriver to use this software.
