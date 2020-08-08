# About
This project is a Scrapy crawler for nairaland.
The spider crawls nairaland users, topics and comments and stores them into a mongo db.
The current structure is :
```
Topic
=====
PageID
View Count

User
====
Sex

Comment
=======
Text
Timestamp
Attachments
Quoted Text         
```    
                

# Usage

1. ## Install requirements
```bash
pip install -r requirements.txt
```

2. Start the crawler
```bash
scrapy runspider nairaland_crawler
```

Note : You should edit the mongo details in `nailand/settings.py` if yours are different.