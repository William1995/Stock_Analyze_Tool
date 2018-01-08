import requests,re

proxyList = []
proxy = {}

def getProxy():
    p_List=[]
    src='http://dev.kuaidaili.com/api/getproxy/?orderid=917228028483433&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sp1=1&sp2=1&quality=1&sort=2&sep=2'
    ips=requests.get(src)
    use=re.findall('(\S*)',ips.text)

    for x in use:
        if x !='':
            p_List.append(x)

    return p_List

def getRes(src_url):
	global proxyList
	global proxy
	while(True):
		try:
			if len(proxyList) <5:
				proxyList=getProxy()
			head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/32.0.1948.69'}
			res=requests.get(src_url,proxies=proxy,timeout=5,headers=head)
			if res.status_code == 200:
				res.close()
				return res
			else:
				proxy={'http':'http://'+proxyList.pop()}
		except Exception as e:
			print(e)
			proxy={'http':'http://'+proxyList.pop()}
			pass

if __name__=='__main__':
    print(getProxy())
