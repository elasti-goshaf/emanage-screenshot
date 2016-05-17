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

def usage():
	parser.add_argument("--url", help="The target url to take the screenshot from. (e.g. 'http://myEmanage/#/vheads/browse')",
	                    type=str)
	parser.add_argument("--user", help="username for login eManage (optional - have defaults)",
	                    type=str)
	parser.add_argument("--password", help="password for login eManage (optional - have defaults)",
	                    type=str)

def getArgs():
	usage()
	parser.parse_args()
	return parser.parse_args()	
	
def getCredentials(parse_args):
	defaultUser, defaultPass = "admin", "changeme"
	user = parse_args.user
	password = parse_args.password

	if user is None:
		user = defaultUser
	if password is None:
		password = defaultPass

	return user, password	

def wait_for_page_load(browser, url):
	for x in xrange(10):
		if browser.current_url == url:
			print "Page is ready!"
			time.sleep(1) # allow loading all visual components
			return
		
		time.sleep(1)
	
	raise Exception("Loading took too much time!")

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




def main():
	args = getArgs()

	# set virtual display (see: https://dzone.com/articles/taking-browser-screenshots-no)
	display = Display(visible=0, size=(1000, 1000))
	display.start()

	browser = webdriver.Firefox()
	browser.get(args.url)
	# can also use PhantomJS but some objects are not rendering nicely on screen
	# e.g. webdriver.PhantomJS("phantomjs")

	print "login eManage ..."
	doLogin(browser, *getCredentials(args))
	wait_for_page_load(browser, args.url)

	path = os.getcwd()+'/screenshot.png' # TODO: parameterize with some default
	browser.save_screenshot(path)
	print "captured screenshot: {0}".format(path)

	browser.close()
	display.stop()


if __name__ == "__main__":
    main()