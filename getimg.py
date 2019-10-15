import os
import sys
import threading
import time
from urllib.parse import urljoin
import urllib.request
import requests
from bs4 import BeautifulSoup

def extractor(sites):
    '''Extract images from a single or a list of urls or html filenames passed.'''
    if_file=os.getcwd()
    os.makedirs('ImagesDownloaded', exist_ok=True)
    os.chdir('ImagesDownloaded')
    return_dir= os.getcwd()
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"}

    for i in range(len(sites)):
        site = sites[i].strip()
        isAFile=False

        if (len(site.split('.'))==2) and ('.html' in site):
            isAFile=True
            os.chdir(if_file)
            try:
                with open(site, 'r', encoding='utf8') as f:
                    content= f.read()
            except Exception as e:
                print(e)
                print('Place file: ' + site + ' in ' + os.getcwd())

        fname=''
        if len(site.split('//'))>1:
            rawname = site.split('//')[1]
            for char in rawname:
                if ((char=='?') or (char==':') or (char=='|')):
                    pass
                else:
                    fname+=char
        else:
            fname = site
            site = 'http://'+site
        
        print('Extracting images from: ' + site)
        
        try:
            if isAFile==False:
                req=urllib.request.Request(site, headers=header)
                content = urllib.request.urlopen(req).read()
                soup = BeautifulSoup(content, 'html.parser')
            else:
                soup = BeautifulSoup(content, 'html.parser')
        except Exception as e:
            print(e)

        os.chdir(return_dir)
        os.makedirs(fname, exist_ok=True)
        os.chdir(fname)

    imagetags = soup.find_all('img',{"src":True})
    srclinks=[]
    for img in imagetags:
        if 'http' in img['src']:
            srclinks.append(img['src'])
        else:
            srclinks.append(urljoin(site, img['src']))

    links = soup.find_all('a')
    
    for link in links:
        z= link.get('href')
        if z==None:
            break
        if (('.png') or ('.jpg') or ('.jpeg') or ('.gif')) in z:
            if z not in srclinks:
                print(z)
                if 'http' in z:
                    srclinks.append(z)
                else:
                    srclinks.append(urljoin(site,z))
    
    total_files=len(srclinks)
    

    print(str(total_files) + ' image files are available in ' + site)
    print('')
    j=0
    fourlists=[[],[],[],[],[],[]]
    
    for k in range(len(srclinks)):
        rem=k%6
        fourlists[rem].append(srclinks[k])

    sixthreads=[]
 
    for m in range(6):
        arg=fourlists[m]
        if len(arg)!=0:
            threadname='athread'+str(m)
            threadname =threading.Thread(target= downloader, args=[arg])
            sixthreads.append(threadname)

    for thread in sixthreads:
        thread.start()

    for thread in sixthreads:
       thread.join()

    print('')   
    print(str(total_files) + ' image files extraced from ' + site+ ' at '+ os.getcwd())

def downloader(threadlist):
    for j in range(len(threadlist)):
        filename=''
        rawfilename= threadlist[j].split('/')[-1]
        for char in rawfilename:
            if ((char=='?') or (char==':') or (char=='|')):
                pass
            else:
                filename+=char
        
        if '.' not in filename:
            filename+='.jpg'
        try:
            response =requests.get(threadlist[j])
            print('Downloading... ' + filename)
            print(threadlist[j])
            with open(filename, 'wb') as file:
                file.write(response.content)
                print('Downloaded ' + filename)
                print('')
        except:
            print('Failed to download ' +filename )
    

if len(sys.argv)>1:
    sites = sys.argv[1:]
else:
    print('Enter URL (you can also pass list of urls using comma as seperator) OR You can also give filename of htmlfile: ' )
    sites=input()
    sites= sites.split(',')

    
starttime=time.time()

if __name__ == '__main__':
    extractor(sites)

endtime= time.time()
print('Total time taken by download is', endtime-starttime)
