from selenium import webdriver
import time
import json
import sys, getopt
import requests

def access_account(driver, username):
	""" Determine whether the given username is a valid and accessible Instagram account """

	profile_url = "https://www.instagram.com/" + username + "/"
	driver.get(profile_url)
	time.sleep(3)

	try:
		# determine if account exists or not
		msg = driver.find_element_by_tag_name("h2")

		if msg.text != username:
			print("Instagram account @" + username + " does not exist")
			return False

		print("Instagram account @" + username + " exists")

		# determine if account is private or public
		msg = driver.find_element_by_class_name("rkEop")
		print("Instagram account @" + username + " is private")
		return False

	except:
		print("Instagram account @" + username + " is public")

	return True

def scroll_account(driver, amount): 
	""" Helper func to scroll down the page """

	for i in range(amount):
		scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
		driver.execute_script(scroll_down)
		time.sleep(3)

def clean_caption(caption):
	""" Helper func to clean the post's caption """
	max_ascii_val = 127

	if caption == '':
		return caption

	new_caption = ''

	# want only ASCII chars
	for x in range(len(caption)):
		if ord(caption[x]) > max_ascii_val:
			continue

		new_caption += caption[x]

	return new_caption

def short_caption(caption):
	""" Helper func to exclude music info from caption """

	if caption == '':
		return ''

	song_point = caption.find("Display:")

	if song_point == -1:
		return ''

	# subtract 2 to get rid of newlines
	return caption[:(song_point - 2)]

def get_tags(driver):
	""" Helper func to get all tag information from caption """
	first_char = 0

	mentions = []
	hashtags = []

	elems = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span/a')
	
	for x in range(len(elems)):
		tag = elems[x].text

		if tag[first_char] == '@':
			mentions.append(tag)
		else:
			hashtags.append(tag)

	return mentions, hashtags

def get_music_info(caption):
	""" Helper func to get music information from caption """
	song_tag_len = 6
	artist_tag_len = 8

	song_point = caption.find("Song:")
	artist_point = caption.find("Artist:")

	if song_point == -1 or artist_point == -1:
		return None, None

	song = caption[(song_point + song_tag_len):(artist_point - 1)]
	artist = caption[(artist_point + artist_tag_len):]

	return song, artist

def get_display_perm(caption):
	""" Helper func to get archive permissions from caption """
	perm_tag_len = 9

	perm_point = caption.find("Display:")
	song_point = caption.find("Song:")

	if perm_point == -1:
		return None

	perm = caption[(perm_point + perm_tag_len):(song_point - 1)]

	return (perm == "True")

def get_thumbnail(driver, output_dir, username, post_id):
	""" Helper func to get thumbnail of post """

	try:
		# video
		thumbnail = driver.find_element_by_tag_name("video")
		url = thumbnail.get_attribute("poster")

		name = ".\\" + output_dir + "\\" + username + "_" + str(post_id) + ".jpg"
		r = requests.get(url)

		file = open(name, "wb")
		file.write(r.content)
		file.close()

		return username + "_" + str(post_id) + ".jpg"

	except:
		return None

def access_caption(driver, output_dir, special_posts, username):
	""" Extract various information from the post & its caption """
	""" Currently only does so for the special_posts list """

	first_char = 0
	video_posts = []
	carousels = []

	for i in range(len(special_posts)):
		link = special_posts[i]
		driver.get(link)
		caption = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text
		
		permission = get_display_perm(caption)
		if permission == None:
			carousels.append(link)
			time.sleep(3)
			continue

		post = dict()
		post['post_id'] = len(video_posts) + 1
		post['user'] = username
		post['url'] = link
		post['display'] = permission
		post['full_caption'] = clean_caption(caption)
		post['short_caption'] = short_caption(post['full_caption'])

		mentions, hashtags = get_tags(driver)
		post['mentions'] = mentions
		post['hashtags'] = hashtags

		song, artist = get_music_info(post['full_caption'])
		post['song'] = song
		post['artist'] = artist	

		post['thumbnail'] = get_thumbnail(driver, output_dir, username, post['id'])	

		video_posts.append(post)
		time.sleep(3)

	return video_posts, carousels

def accessPosts(driver, special_posts, regular_posts, total):
	""" Gets the links of all the posts on the user's profile """
	""" Determines whether each post possibly has video content or not """

	if len(special_posts) + len(regular_posts) == total:
		return

	posts = driver.find_elements_by_tag_name("a")
	within_posts = False

	for i in range(len(posts)):
		link = posts[i].get_attribute("href")

		if within_posts == False and link.find("/p/") != -1:
			within_posts = True

		if within_posts == False:
			continue

		if within_posts == True and link.find("/p/") == -1:
			break

		if link in special_posts or link in regular_posts:
			continue

		type_icon = posts[i].find_elements_by_class_name("u7YqG")

		if len(type_icon) != 0:
			special_posts.append(link)
		else:
			regular_posts.append(link)

		if len(special_posts) + len(regular_posts) == total:
			return

def save_json(name, data):
	""" Helper function to save collected data into a json file """

	file_name = name + ".json"
	outfile = open(file_name, "w")

	json.dump(data, outfile)

	outfile.close()

def get_account_data(driver, output_dir, username, total):
	""" Gets post information from the user's profile """
	
	regular_posts = []
	special_posts = []
	first_pass = True

	while (True):
		if first_pass == False: 
			scroll_account(driver, 3)
		else:
			first_pass = False
			scroll_account(driver, 1)

		accessPosts(driver, special_posts, regular_posts, total)

		if len(special_posts) + len(regular_posts) == total:
			break

	videos_info, carousels_info = access_caption(driver, output_dir, special_posts, username)

	file_name = ".\\" + output_dir + "\\" + username + "_videos"
	save_json(file_name, videos_info)

	file_name = ".\\" + output_dir + "\\" + username + "_carousels"
	save_json(file_name, carousels_info)

	file_name = ".\\" + output_dir + "\\" + username + "_singles"
	save_json(file_name, regular_posts)

def account_stats(driver, output_dir, username):
	""" Gets user info from the user's profile """

	posts_index = 0
	followers_index = 1
	following_index = 2

	raw_stats = driver.find_elements_by_class_name("g47SY")

	stats = dict()
	stats['username'] = username
	stats["num_posts"] = int(raw_stats[posts_index].text)
	stats["num_followers"] = int(raw_stats[followers_index].text)
	stats["num_following"] = int(raw_stats[following_index].text)

	file_name = ".\\" + output_dir + "\\" + username + "_stats"
	save_json(file_name, stats)

	return stats

def main(argv):
	info = "USAGE: vid_scraper.py [-h] -d chrome_driver_path -o output_dir usernames"

	try:
		opts, args = getopt.getopt(argv, "hd:o:")

	except getopt.GetoptError:
		print(info)
		sys.exit(2)

	driver = None
	output_dir = ""
	path = ""

	for opt, arg in opts:
		if opt == '-h':
			print(info)
			sys.exit()
		
		if opt == '-d':
			path = arg

		if opt == '-o':
			output_dir = arg
	
	driver = webdriver.Chrome(path)

	for arg in args:
		username = arg

		if access_account(driver, username) is True:
			print("Instagram account @" + username +  " can be accessed")

			stats = account_stats(driver, output_dir, username)
			get_account_data(driver, output_dir, username, stats["num_posts"])

		else:
			print("Instagram account @" + username +  " cannot be accessed")

	driver.quit()

if __name__ == "__main__":
	main(sys.argv[1:])