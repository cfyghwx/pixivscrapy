# 使用说明
## 1.关于vpn设置说明
1）若使用shadowsock等设置本地端口代理方式的vpn，则需要自己修改middleware中的proxy
2）若使用其他的全局代理方式的vpn，注释掉middleware中的proxy

## 2.账户设置
爬取时需要设置记得的账户和密码，根据passwordsample格式设置，同时文件命名为password即可

# 更新日志 
## 5.27日
1.实现登录pixiv

## 6.12日
1.尝试完成日榜图片获取
2.想剩下的功能.....



# 踩过的坑
## 1.图片连接获取
图片连接获取的时候打开图片页发现浏览器和爬取页面有一定不同，然后就需要在那个js中搜索好久，好在还是发现了链接
## 2.scrapy自带的下载图片pipeline
这个pipeline好像是会对图片进行统一的压缩和格式统一，因为爬取下来的图片本来就是要做壁纸，so，这点不能接受，就改了用了requests在获取到连接后，请求图片
