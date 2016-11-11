#Install
pip install scrapy --user
pip install six --user
pip install twisted --user
pip install MySQL-Python --user
# How to run crawl
scrapy crawl shop
# Export to json file
scrapy crawl shop -o items.json -t json
# Setup with cron job
crontab -e
*/5 * * * * scrapy crawl shop
# Save cron
crontab: installing new crontab
# Run cron job

