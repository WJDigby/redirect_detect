import argparse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

def redirect_detect(wait_time, url_list):
	print("[+] Creating browser object...")
	opts = Options()
	opts.set_headless()
	assert opts.headless  
	browser = Firefox(options=opts)
	redirect_dict = {}
	print("[+] Visiting URLs with a " + str(wait_time) + " second delay...")
	with open(url_list) as f:
		lines = f.readlines()
		for line in lines:
			original_url = line.rstrip()
			if original_url in redirect_dict.keys():    # In the event that there's a duplicate in the list, ignore
				break
			else:
				browser.get(original_url)
				redirect = "No"
				secure = "No"
				browser.implicitly_wait(wait_time)
				final_url = browser.current_url
				if original_url != final_url:
					redirect = "Yes"
				if final_url.startswith("https"):
					secure = "Yes"
				redirect_dict[original_url] = [final_url, redirect, secure]
		browser.quit()
		print("[+] Browser object closed.")
	i = 0
	print("[+] Results:\nOriginal URL - Final URL - Redirect - Secure")
	for key, value in redirect_dict.items():
		print(key, value[0], value[1], value[2])
		if redirect_dict[key][1] is "Yes":
			i += 1
	print(str(len(redirect_dict)) + " unique URLS assessed.")
	print(str(i) + " redirections detected.")

def main():
	parser = argparse.ArgumentParser(description='Use Selenium to test a list of URLs for redirects')
	parser.add_argument('-t', '--time', dest='wait_time', type=int, default=2, help='Time in seconds to wait after browsing to site. Default 2.')
	parser.add_argument('-l', '--list', dest='url_list', required=True, help='File containing list of URLs, separated by line.')
	args = parser.parse_args()
	wait_time = args.wait_time
	url_list = args.url_list
	redirect_detect(wait_time, url_list)

if __name__ == '__main__':
	main()
