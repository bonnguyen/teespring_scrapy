#!/bin/bash
cd /Projects/teespring_scrapy/
echo 'Run crawl teespring shop'
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl shop