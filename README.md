# dance-archive

Consists of two parts: an Instagram scraper and a Django based website. The data collected via the scraper was used to populate the website's database. The website itself features a search function that allows visitors to search and filter through the posts stored. Only posts with consent within their description will be shown on the website. 

## Requirements
1. Selenium
      * [Installation instructions](https://pypi.org/project/selenium/)
      * [Unofficial documentation](https://selenium-python.readthedocs.io/) 
2. Django
      * [Installation instructions](https://docs.djangoproject.com/en/3.1/intro/install/)
      * [Documentation](https://docs.djangoproject.com/en/3.1/)
3. django-filters
      * [Installation instructions](https://pypi.org/project/django-filter/)
      * [Documentation](https://django-filter.readthedocs.io/en/stable/index.html)
4. django-crispy-forms
      * [Installation instructions](https://pypi.org/project/django-crispy-forms/)
      * [Documentation](https://django-crispy-forms.readthedocs.io/en/latest/index.html)

## vid_scraper.py
An scraper that focuses on getting data from video posts of a particular user. Uses selenium to explore the given user's feed to determine which posts contain videos and which of those videos are for our use. 

### Script Requirements
1. Chrome driver for Selenium
2. Windows OS

### User Requirements
1. The user feed being scraped exists and is public
2. The description of all videos posts of the user have the following format
    ```
    [some description text]
    
    Display: True/False
    Song: Example Song
    Artist: Example Artist
    ```

### Expected Directory Structure
```
├── /output_dir/
├── chrome_driver
└── vid_scraper.py
```

### Usage
`vid_scraper.py [-h] -d chrome_driver_path -o output_dir usernames`

Argument `usernames` can be a single username or multiple, each separated by a space. 

### Output
```
/output_dir/
  ├── [username]_stats.json
  ├── [username]_videos.json
  ├── [username]_carousels.json
  ├── [username]_singles.json
  └── [username]_*.jpg
```


## Django website

### Populating backend database
You will need files `[username]_stats.json`, `[username]_videos.json`, and all `[username]_*.jpg` files
1. Within the \archive\ directory, run `py manage.py shell`
    1. Run the following
    ```
    from search.models import *
    import json
    ```
2. Create a User object using the data from `[username]_stats.json`
    1. Run the following
    ```
    infile = open(path_to_stats_file, "r")
    stats = json.load(infile)
    infile.close()
    
    [username] = User()
    for k, v in stats.items():
        setattr([username], k, v)
    
    [username].save()
    ```
3. Create Post objects for each item in `[username]_videos.json`
    1. Run the following
    ```
    infile = open(path_to_videos_file, "r")
    videos = json.load(infile)
    infile.close()
    
    [username] = User.objects.get(username = "[username]")
    for i in range(len(videos)):
        post = Post(user = [username])
        
        for k, v in videos[i].items():
            if k == 'user' or k == 'post_id':
                continue
            else:
                setattr(post, k, v)
        
        post.save()
    ```
4. Place all `[username]_*.jpg` files in the `archive\search\static\search\images\` directory

### Viewing the website
1. Within the \archive\ directory, run `py manage.py runserver`
2. Visit http://127.0.0.1:8000/search/
