# global_times_webscraper
This webscraper was written by M. Albrecht Hänig, a social scientist focusing on the media and public opinion in international relations. The scraper allows to automatically download articles of the Chinese newspaper Global Times via a keyword search - both for the title as well as the body text. In addition, you can set a specific time frame. The downloaded articles include the publication date, the authors, the title, the body text, and the link. The data table will be stored as an excel file. 

PS: If you come across a bug, lemme know!

Necessary Updates:
cat("\n")
(1) For a small percentage of articles, the information for the authors is missing. Either the article does not have author names, or the author name is not in the usual format. In the latter case, I still need to write an update.
cat("\n")
(2) Sometimes, the title is missing. Usually, this is due to the fact that the link leads to a video, with different title format.