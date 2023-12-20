# 人民日报爬虫

###### ***update 12.18***

Github:[https://github.com/RWLinno/RMRB/](https://github.com/RWLinno/RMRB/)

Author: @rwlinno

### 简介

输入时间的起始终止范围，或指定年份 / 日期列表 ，找寻日报中带有图片的报道，存成网页、图片、文稿以及汇总表的格式。

##### 预览效果

1.

![image-20231218230242272](https://s2.loli.net/2023/12/18/5YIpSs6NJW7mDgE.png)

2.

![image-20231218231204677](https://s2.loli.net/2023/12/18/5JjRCBh4b97vxkN.png)

##### 汇总结果及其格式

- 保存网页
  - 网页命名格式：`日期_版次_文章题目_文章作者姓名`_
  - 例：  `20091218_第01版_《温家宝会见巴西总统卢拉》_庞兴雷&韦冬泽`

- 保存图片
  - 图片命名格式：`日期_版次_文章题目_文章作者姓名_图片+No.`
  - 例：`20091218_第01版_《温家宝会见巴西总统卢拉》_庞兴雷&韦冬泽_图片01`
- 保存Excel

```
*日期 版次 版面名称 文章题目 文章作者姓名  图片编号. 图片说明文字  图片作者*  
日期：20030512
版次：01 02  03 …….
版面名称：（如有）01：要闻
文章题目：《xxxxxxxx》
文章作者姓名：  张三   张三&李四
图片编号：图片在文章内的编号  01 02  03
图片说明文字：(如能捕捉到)文字格式
图片作者：(如能捕捉到)  张三   张三&李四
```



### 文件结构

```
RMRB/
│───README.md
└───output/
│   │───年份/
│   │   │   文稿.txt
│   │   │   网页.html
│   │   │   图片1.jpg
│   │   │   图片2.jpg
│   │   ...
│   ...
│   new_people.py
│   old_people.py
│   utils.py
│   requirements.txt
│   ...
```

##### new_people.py

支持爬取新人民日报网(例如：http://paper.people.com.cn/rmrb/html/2023-12/15/nbs.D110000renmrb_01.htm)的数据，成功率高。

##### old_people.py

用来爬上个世纪的人民日报，**还没写完**，会面临验证和拒绝访问等问题。

##### utils.py

用来存放爬虫常用或其他实用方法。



### Quick Start

下面直接在命令行里创建虚拟环境->激活->安装依赖包->运行程序

```
conda create -n RMRB python=3.8
conda activate RMRB
pip install -r requirements.txt
python new_people.py
```

![image-20231220132612994](https://s2.loli.net/2023/12/20/GW9eKigMBsD25fE.png)



### 使用方法

修改下图所示参数，直接在IDE里运行爬虫程序即可。

![image-20231218232625885](https://s2.loli.net/2023/12/18/mg3HkYS5auhld4p.png)

建议按月份分批次爬取数据。



### 待更新

- 目前只能爬取新人民日报的数据，爬老人民日报(1957年之后)的程序oldpeople.py还没写完
- 长时间范围下的爬虫容易断开连接，按月爬取比较容易
