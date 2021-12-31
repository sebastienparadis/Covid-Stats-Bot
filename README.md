# Covid-Stats-Bot

Technologies Used: Python, Covid-19 Tracker API, Flask, Discord Developer Portal, Repl.it

Launched an interactive bot in a discord server that interprets user commands and returns statistics retrieved using the Covid-19 Tracker API. Using the information in the API, this bot can return the following for every Canadian province and Canada as a whole: Total Covid-19 Cases, Fatalitie, Vaccinations Administere, Vaccinated People, and Boosters Administered.

To initialize a command, the user must start the command with a "#". This is followed by the one-word call for the specific statistic, then seperated by a whitespace, the two-character provincial code or the full spelling of "Canada" for the provincial or national statistic, respectively.

e.g. To return the total Covid-19 Vaccinations Administered statistic for Manitoba, the user would send the following command to the Covid Stats Bot: "#Vaccinations MB"
