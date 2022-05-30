# Maagim Araby #

*	Author: Ibrahim Hamadeh
*	NVDA compatibility: 2019.3 and later
*	Download [version 1.3][1]

This addon helps you get the meaning of single arabic words or phrases  
from several Arabic dictionaries present on almaany.com website.  
[almaany.com](https://www.almaany.com/ar/dict/ar-ar/).  

***

## Usage

*	Press nvda+Alt+M, Maagim Araby dialog will be displayed  
and you will be standing on an edit field  
if when pressing this command, you were standing on a selected word, the word will be put in the edit field  
*	otherwise, enter in the edit field the arabic word or phrase you want  
tab an choose the arabic dictionary you want and press enter on it.  
if you want to get the meaning in the default, the comprehensive almaany arabic dictionary, you can always press enter on the edit field and after that the meaning of the word will be displayed in a separate browseable window.  
*	You can moreover, going to addon's setting dialog, through:  
NVDA menu/preferences/Settings/Maagim Araby  
from there, you can choose the type of window used to display the meaning.  
	1.	the default and first choice, is your ordinary default browser  
choosing this, the result will be displayed in your default ordinary full browser.  
	2.	the  second choice, is a browser like window as in firefox or google chrome, it is a browser window without file menus or address brar.  
please remember you can close this window only, with control+w or alt+f4.  
	3.	the third, is the native NVDA message box, used it only after testing and if it suits you, for in our experience it smetimes make NVDA freezes.  
*	From that setting dialog, you can also choose whether to close Maagim Araby dialog after requesting the meaning of word or not.  
 
## Changes for 1.3 ##

*	Make the addon compatible with NVDA 2022.1.
*	Removing pieces of unWanted text from the page, that was added recently, by using regular expression and replacing it with an empty string.

## Changes for 1.2 ##

*	Fiix a bug happened lately in the addon, most likely due to changes in server
The bug was fixed by removing the old user agent, and use instead user_agent module.

## Changes for 1.0 ##

*	Initial version.

[1]: https://github.com/ibrahim-s/maagimAraby/releases/download/1.3/maagimAraby-1.3.nvda-addon