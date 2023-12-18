import re
import requests
import time
import chardet
import os


def fetchUrl(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        encoding = chardet.detect(r.content)['encoding']
        return r.content.decode(encoding)
    except requests.exceptions.RequestException as e:
        print(f"无法获取URL {url} 的内容: {e}")
        return None

def deal_date1(date):
    return date[:7] + '/'+ date[8:]

def deal_date2(date):
    return re.sub(r'\D', '', date)

def format_number(n):
    return "{:02d}".format(n)

def clean_name(filename):
    invalid_chars = '<>:"/\\|?*\n'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def clean_author(string):
    string = re.sub(r'[\(\)\[\]]', '', string)
    names = string.split('、')
    names = [name.strip() for name in names]
    cleaned_author = '&'.join(names)
    return cleaned_author


def download_image(url, filepath):
    print(f"下载图片: {url}")
    response = requests.get(url, stream=True)
    with open(filepath, 'wb') as out_file:
        out_file.write(response.content)

def save_to_excel(df, filepath):
    print(f"保存excel: {filepath}")
    df.to_excel(filepath, index=False)

def save_webpage(args,suffix='html'):
    content = fetchUrl(args.url)
    filename = f"{args.date}_{args.page}_{args.title}_{args.author}.{suffix}"
    if not os.path.exists(args.destdir):
        os.makedirs(args.destdir)
    with open(os.path.join(args.destdir, filename), 'w', encoding='utf-8') as f:
        f.write(content)

def save_to_txt(args):
    filename = f"{args.date}_{args.page}_{args.title}_{args.author}.txt"
    if not os.path.exists(args.destdir):
        os.makedirs(args.destdir)
    with open(os.path.join(args.destdir, filename), 'w', encoding='utf-8') as f:
        f.write(args.content)