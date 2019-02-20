## Disclaimer:
This is the first python program I wrote and I therefore don't really intend to upgrade
its usability or quality of code for the future. I'm adding this to git incase someone
from the future finds it suitable for their needs.

## Usage:
Running the program opens a `tkinter` finder window which allows you to select a *.xslx*
file. The program then uses the freegeoip.net `api` to find the City and State name associated
with an IP address. It adds two columns with the names `State Names` and `City Names`
next to a column called `ipAddr` and populates them (if you want to change the name
of the `ipAddr` column change it in line 102 of `update_columns()`). It then saves
the file as a *.xlsx*. I have implemented rate-limiting but please don't abuse the API.

