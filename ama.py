#!/usr/bin env python


"you can email me at: emmanuel.nsanga@gmail.com"

"""Copyright [2013] [Emmanuel Nsanga]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License."""


import subprocess
from scrapy.selector import HtmlXPathSelector  
import os
import shelve
import sys
#import requests

def scrap_prof(prof_link,fil):
    global scrap_prof, catg 
    a = subprocess.check_output("scrapy fetch '%s'"%prof_link,shell=True)
    aa = HtmlXPathSelector(text=a)
    for dd in aa.select('//a@b').extract():
        print dd
        if "location" in dd:
            print dd
            fil.write('%s'%dd)
            
    tdd = []        
    for d in aa.select('//td').extract():
        td = HtmlXPathSelector(text=d)
        tdd = td.select('//img/@src').extract()
        
    fil.write(tdd[1])   
    for dda in aa.select('//span/@b').extract():
         fil.write("name:%s"%dda)
        
    try:
       for it in aa.select('//div').extract():
           if "targ" in it:
               fil.write("website:%s"%it.split('href=')[1])
        
        
    except:
          it = None



def catg():
    sh = shelve.open("cat.db",writeback=False)['dict']
    urls = ['http://www.amazon.com/s/ref=sr_pg_2?rh=n%3A11091801%2Ck%3A%22&page=1&keywords=%22&ie=UTF8&qid=1375737123']    
    fil = open(fi[len(fi)-1].split('=')[1],"w")
    for i in sh:
        print i
        urls.append(urls[0].replace('mi',str(i)))
           
           
    #print urls       
    for ii in urls:
        #a = requests.get(ii,headers={'User-Agent': 'Mozilla/5.0'}).text #If you're on a windows machine, works for both windows and linux, but can sometimes be unreliable and slow.
        a = subprocess.check_output("scrapy fetch '%s'"%ii,shell=True) #I know wierd, but this seems to be quite reliable.
        hxs = HtmlXPathSelector(text=a)               
        for p in hxs.select('//span'):
            if 'class="pagnDisabled"' in p:
               n = (int(str(p).split('<')[2].split('>')[1])+1)
               if n > 1:
                  for ra in range(2, n):
                      pag = ii.replace('page=1','page=%s'%str(ra))
                      aa = subprocess.check_output("scrapy fetch '%s'"%pag,shell=True)               
                      li = []
                      for d in hxs.select('//a').extract(): # find the right class 
                          if 'ilo2 ilc2' in d: 
                             li.append(d)
                             
                      lin = []
                      for dd in li:
                          tt = HtmlXPathSelector(text=dd)
                          lin.append(tt.select('//a/@href').extract()[0])
                          
                     
                      for it in lin:
                           aaa = subprocess.check_output("scrapy fetch '%s'"%it,shell=True)
                           ttt = HtmlXPathSelector(text=aaa)
                           rev = ttt.select('//a')
                           revi = ""
                           for ite in rev:
                               if "customer reviews" in ite:
                                  revv = HtmlXPathSelector(text=ite)
                                  revi = revv.select('//a/@href').extract()
                                  break
                                  
                           revie = HtmlXPathSelector(text=subprocess.check_output("scrapy fetch '%s'"%revi,shell=True))
                           for renn in revie.selecet('//a/@href').extract():
                               if "profile" in renn:
                                  scrap_prof("http://www.amazon.com/"+renn)
                               

def main():
    fi = sys.argv[:1]
    if len(fi) > 1:
       catg(fi[len(fi)-1].split('=')[1])
       
    else:
        print "scrapy crawl amazon_reviewers --set FEED_URI=reviewers.csv --set FEED_FORMAT=csv"                                  
         
if __name__ == '__main__':
   main()
