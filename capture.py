import os 
import time
import argparse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pyvirtualdisplay import Display


parser = argparse.ArgumentParser()
login_form = 'ctrl.form'

def setArgs():
	parser.add_argument("--url", help="The target url to take the screenshot from. (e.g. 'http://myEmanage/#/vheads/browse')",
	                    type=str, required=True)
	parser.add_argument("--user", help="username for eManage login",
	                    type=str, required=True)
	parser.add_argument("--password", help="password for eManage login",
	                    type=str, required=True)
	parser.add_argument("--out", help="output file name (e.g. 'screenshot.png')",
	                    type=str, required=True)
	parser.add_argument("--chown", help="change the output file's ownership to the given user id (default is 'root')",
	                    type=int)
	
def wait_for_page_load(browser, targeturl):
	timeout = 15
	for x in xrange(timeout):
		if browser.current_url == targeturl:
			print "Page is ready!"
			time.sleep(1) # to allow loading all visual components
			return
		
		time.sleep(1)
	
	raise Exception("Loading the page took too much time! ({}s)".format(timeout))

def doLogin(browser, user, password):
	try:
		form_user_textfield = browser.find_element_by_name('username')
	except NoSuchElementException, e:
		# we're not on login page, skip login procedure
		print "User is already logged in, skipping ..."
	else:
		form_user_textfield.send_keys(user) # set username

		form_passwd_textfield = browser.find_element_by_name('password')
		form_passwd_textfield.send_keys(password) # set password

		form = browser.find_element_by_name(login_form)
		form.submit() # press login


def getPath(path):
	basepath = os.path.abspath(path)
	try: 
	    os.makedirs(basepath)
	except OSError:
	    if not os.path.isdir(path):
	        raise

	fileName = "screenshot.png"
	return os.path.join(basepath, fileName)


def main():
	setArgs()
	args = parser.parse_args()	
	print "Loading {} ...".format(args.url)

	# set virtual display (see: https://dzone.com/articles/taking-browser-screenshots-no)
	display = Display(visible=0, size=(1000, 1000))
	display.start()

	browser = webdriver.Firefox() # can also use PhantomJS (e.g. webdriver.PhantomJS("phantomjs")) but some objects are not rendering nicely on screen
	browser.get(args.url)

	print "login eManage ..."
	doLogin(browser, args.user, args.password)
	wait_for_page_load(browser, args.url)

	# path = getPath(args.out)
	browser.save_screenshot(args.out)
	print "captured screenshot: {0}".format(os.path.basename(args.out))

	uid = args.chown
	if uid is not None:
		os.chown(args.out, uid, -1)

	browser.close()
	display.stop()


if __name__ == "__main__":
    main()