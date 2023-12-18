import re
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import os
import datetime
from urllib.parse import urljoin
from utils import *

class args:
    def __init__(self) -> None:
        self.date="", 
        self.page="", 
        self.pagename='',
        self.title="", 
        self.author="",
        self.content="",
        self.url="",
        self.destdir=""

def getPageList(date):
    url = 'http://paper.people.com.cn/rmrb/html/' + deal_date1(date) + '/nbs.D110000renmrb_01.htm'
    html = fetchUrl(url)
    if html is None:
        return None
    bsobj = bs4.BeautifulSoup(html,'html.parser')
    temp = bsobj.find('div', attrs = {'id': 'pageList'})
    if temp:
        pageList = temp.ul.find_all('div', attrs = {'class': 'right_title-name'})
    else:
        pageList = bsobj.find('div', attrs = {'class': 'swiper-container'}).find_all('div', attrs = {'class': 'swiper-slide'})

    linkList = ['http://paper.people.com.cn/rmrb/html/'  + deal_date1(date) + '/' + page.a["href"] for page in pageList]
    return linkList

def getTitleList(date, pageUrl):
    html = fetchUrl(pageUrl)
    if  html is None:
        return None
    bsobj = bs4.BeautifulSoup(html,'html.parser')
    temp = bsobj.find('div', attrs = {'id': 'titleList'})
    if temp:
        titleList = temp.ul.find_all('li')
    else:
        titleList = bsobj.find('ul', attrs = {'class': 'news-list'}).find_all('li')

    linkList = ['http://paper.people.com.cn/rmrb/html/'  + deal_date1(date) + '/' + title.a["href"] for title in titleList if 'nw.D110000renmrb' in title.a["href"] and title.find('div', class_='pci_c')]
    return linkList

def getContent(html, base_url):
    bsobj = BeautifulSoup(html,'html.parser')
    pagename = bsobj.find('p', class_='ban').text if bsobj.find('p', class_='ban') else ''
    title = ""
    try:
        title=bsobj.h3.text + '\n' + bsobj.h1.text + '\n' + bsobj.h2.text + '\n'
        author = bsobj.find('div', attrs = {'class': 'author'}).text if bsobj.find('div', attrs = {'class': 'author'}) else ''
        pList = bsobj.find('div', attrs = {'id': 'ozoom'}).find_all('p')
        content = ''.join([p.text + '\n' for p in pList])

    except Exception as e:
        print("获取失败",e)
        return None, None, None, None, None, None, None
    
    img_urls = []
    img_describes = []
    pic_authors = []
    
    for table in bsobj.find_all('table', class_='pci_c'):
        img = table.find('img')
        if img and 'src' in img.attrs:
            img_urls.append(urljoin(base_url, img['src']))
        p = table.find('p')
        if p:
            img_describe_parts = p.get_text(separator='\n').split('\n')
            img_describe = img_describe_parts[0].replace('\u3000', '') if len(img_describe_parts) > 0 else ''
            pic_author = img_describe_parts[1].replace('\u3000', '') if len(img_describe_parts) > 1 else ''
            img_describes.append(img_describe)
            pic_authors.append(pic_author)

    return pagename, title, author, content, img_urls, img_describes, pic_authors

def get_args(date, page, pagename, title, author,content, url,destdir):
    args.date = date
    args.page = page
    args.pagename = pagename
    args.title = title
    args.author = author
    args.content = content
    args.url = url
    args.destdir = destdir
    return args

def download_rmrb(cnt, date, data, outpath):
    for pageNo in range(1,5):
        for titleNo in range(1,5):
            url = 'http://paper.people.com.cn/rmrb/html/'+deal_date1(date)+'/nw.D110000renmrb_'+deal_date2(date)+'_'+str(titleNo)+'-'+str(format_number(pageNo))+'.htm'
            html = fetchUrl(url)
            if html is None:
                break

            pagename, title, author, content, img_urls, img_describes, img_author = getContent(html, url)

            if img_urls==None or not len(img_urls):
                # print(f"跳过URL {url} (无图片)")
                continue

            title = clean_name(title)
            author = clean_author(author)
            args = get_args(deal_date2(date), '第'+str(format_number(pageNo))+'版', pagename,'《'+title+'》', author, content, url, outpath)
            print(args.url)
            save_webpage(args)
            save_to_txt(args)
            for i, img_url in enumerate(img_urls):
                img_name = args.date + '_' + args.page + '_' + args.title + '_' + args.author + '_图片' + str(format_number(i+1))
                img_filepath = outpath + img_name + '.jpg'
                download_image(img_url, img_filepath)
                data.append([args.date, args.page, args.pagename, args.title, args.author, str(format_number(i+1)), clean_name(img_describes[i]),img_author[i]])
                cnt += 1
                if cnt % 20 == 0:
                    print("chekpoint:", cnt)
                    df = pd.DataFrame(data, columns=['日期', '版次', '版面名称','文章题目', '记者', '图片编号', '图片说明文字', '图片作者'])
                    save_to_excel(df, destdir + 'info.xlsx')

    return data, cnt

def every_date(year):
    start_date = datetime.date(year, 4, 2)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(days=1)
    dates = []
    while start_date <= end_date:
        dates.append(start_date.strftime('%Y-%m-%d'))
        start_date += delta
    return dates

if __name__ == '__main__':
    year = 2022
    data = []
    cnt = 0
    dates = every_date(year)  # 输入年份
    #dates = ['2023-01-01']
    destdir = './output/'+ str(year) + '/' # 输出文件夹

    filename = destdir + 'info.xlsx'
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        data = df.values.tolist()
        print("预读入：",data)

    for date in dates:
        data, cnt = download_rmrb(cnt, date, data, destdir)

    df = pd.DataFrame(data, columns=['日期', '版次', '版面名称','文章题目', '记者', '图片编号', '图片说明文字', '图片作者'])
    save_to_excel(df, filename)