import argparse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

def redirect_detect(timeout, dwell_time, url_list):
	print("[+] Creating browser object...")
	opts = Options()
	opts.set_headless()
	assert opts.headless  
	browser = Firefox(options=opts)
	browser.set_page_load_timeout(timeout)
	redirect_dict = {}
	print("[+] Visiting URLs with a dwell time of " + str(dwell_time) + " seconds...")
	with open(url_list) as f:
		lines = f.readlines()
		for line in lines:
			original_url = line.rstrip()
			if original_url.endswith('/'):    # Remove any trailing / first in case "http://example.com/" and "http://example.com" are in the input list
						original_url = original_url[:-1]
			if not original_url.startswith("http://") and not original_url.startswith("https://"):
				original_url = "http://" + original_url
			if original_url in redirect_dict.keys():    # In the event that there's a duplicate in the list, ignore
				continue
			else:
				try:
					browser.get(original_url)
					redirect = "No"
					secure = "No"
					browser.implicitly_wait(dwell_time)
					final_url = browser.current_url
					if final_url.endswith('/'):
						final_url = final_url[:-1]
					if original_url != final_url:
						redirect = "Yes"
					if final_url.startswith("https"):
						secure = "Yes"
					redirect_dict[original_url] = [final_url, redirect, secure]
				except TimeoutException:
					print("[-] Timeout while visiting " + original_url)
					redirect_dict[original_url] = ["Timeout", "N/A", "N/A"]
				except WebDriverException:
					print("[-] WebDriverException while visiting " + original_url)
					redirect_dict[original_url] = ["WebDriverException", "N/A", "N/A"]
		browser.quit()
		print("[+] Browser object closed.")
	redirect_count = 0
	redirect_urls = []
	print("[+] Results:\nOriginal URL - Final URL - Redirect - Secure")
	for key, value in redirect_dict.items():
		print(key, value[0], value[1], value[2])
		if redirect_dict[key][1] is "Yes":
			redirect_count += 1
		if redirect_dict[key][0] not in redirect_urls:
			redirect_urls.append(redirect_dict[key][0])
	print(str(len(redirect_dict)) + " unique original URLs.")
	print(str(len(redirect_urls)) + " unique final URLs.")
	print(str(redirect_count) + " redirections.")
	

def main():
	parser = argparse.ArgumentParser(description='Use Selenium to test a list of URLs for redirects')
	parser.add_argument('-d', '--dwell', dest='dwell_time', type=int, default=2, help='Time in seconds to dwell on a site after browsing to it. Default 2.')
	parser.add_argument('-t', '--timeout', dest='timeout', type=int, default=20, help='Timeout in seconds. Default 20.')
	parser.add_argument('-l', '--list', dest='url_list', required=True, help='File containing list of URLs, separated by line.')
	args = parser.parse_args()
	dwell_time = args.dwell_time
	timeout = args.timeout
	url_list = args.url_list
	redirect_detect(timeout, dwell_time, url_list)

if __name__ == '__main__':
	main()
