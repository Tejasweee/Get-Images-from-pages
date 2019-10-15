# Get-Images-from-pages
This is a python script which helps to automatically extract images from pages of given URLs. If the page requires execution of javascript for execution of images or needs authentication to reach there, page can be saved as .html file and this script can be run on that file. This script can implement upto 6 threads for fast download of images.

# Requirements:
This script uses all the built-in libraries provided by python except for two libraries which are beautifulsoup and requests. They can be installed through pip using the command 'pip install beautifulsoup4' and 'pip install requests'. These can also be installed by running the requirements.py file which is present in this repository by running 'python requirements.py'.

# Using the Script:
- From Command Line Argument:

python getimg.py, url

python getimg.py, url1, url2, url3....

python getimg.py, afile.html

python getimg.py, afile1.html, afile2.html, afile3.html...

- Passing argument after running the script:
python getimg.py

-- Now arguments can be passed in the input prompt

