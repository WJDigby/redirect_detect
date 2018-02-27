# redirect_detect
Python script to enumerate web redirections using Selenium.
Using the Selenium browser object should enables us to detect a redirect whether it's based on HTTP status codes, meta refresh, JavaScript, or some other method.

**Requirements:**

Currently written to use the Firefox, and so it requires the Selenium Firefox driver, "geckodriver": 

https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver 

Also requires Python argparse and selenium.

**Usage:**

 ```python3 redirect-detect.py -l /path/to/list/of/urls.lst -t 5```

-l / --list Path to a list of URLs, separated by line

-t / --time Time to wait between URL visits in seconds. Default is 2.
