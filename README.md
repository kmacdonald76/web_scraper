# A scrappy web scraper.

The main goal here is to generalize scraping data found in html tables on the internet; to exploit
 the fact that a lot of statistics usually conform to a table format that is easily parsable, then
 inject this data into a postgres database that can be more easily searched, and fed into learning 
 algorithms.

What you'll find is that each table of data found on the internet needs certain customizations,
 also depending on the desired goal of the data scientist.  There's several challenges with this of
 course, firstly, identifying column headers.  The next is simplying the customizations that the 
 developer needs to code in order to massage the data into whatever the data format the data scientist
 desires.

Although there will _never_ be one correct method for parsing an HTML table, there is on-going 
 efforts to generalize various modification methods so that it can be modified to cover majority
 of the cases, by a simple function call.  I am not quite there yet, but it is coming.

My goal is to cover 80% of the cases, then allow developers to easily add their own, so the code
 base doesn't get too bloated.  This is mostly crumbs from my current personal project that I'd
 like to share.


# Laundry List of Stuff Todo ..

 - Crawling paginated tables
 - Add configuration files
 - Better logging
 - Better cache naming convention
 - Add more generalized methods for massaging data
 - Add compression to cached data possibly
