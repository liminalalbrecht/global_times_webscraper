# global_times_webscraper

This scraper allows to automatically download English articles of the Chinese newspaper Global Times via a keyword search - both for the title as well as the body text. In addition, you can set a specific time frame. The downloaded articles include the publication date, authors,  title,  body text, and link. The data table will be stored as an excel file. 

PS: If you come across a bug, lemme know! I appreciate also any tips and constructive criticism!






Necessary Updates:


(1) For a small percentage of articles, the information for the authors is missing. Either the article does not have author names, or the author information is not in the usual format. In the latter case, I still need to write an update.

(2) Sometimes, the title and article text is missing. Usually, this is due to the fact that the link leads to a video, which has a different title format and features no text. The script does not download the transcripts of the videos.