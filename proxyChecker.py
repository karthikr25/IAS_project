import urllib.request
import threading
import random
import sys
import os
import argparse
from time import time

useragents=('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')

proxyType = ''

def checkproxy(txtfile):
	global out_file
	candidate_proxies = open(txtfile).readlines()
	filedl = open(txtfile, "w")
	filedl.close()
	out_file = open(txtfile, "a")
	threads = []
	for i in candidate_proxies:
		t = threading.Thread(target=checker, args=[i])
		t.start()
		threads.append(t)

	for t in threads:
		t.join()

	out_file.close()
	if args.verbose:
		print("\n\nCurrent IPs in proxylist: %s\n" % (len(open(txtfile).readlines())))

def checker(i):
	proxy = proxyType + '://' + i
	proxy_support = urllib.request.ProxyHandler({proxyType: proxy})
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)
	global site
	req = urllib.request.Request(proxyType + '://' + site)
	req.add_header("User-Agent", useragents)
	try:
		global chosenTimeout
		start_time = time()
		urllib.request.urlopen(req, timeout=chosenTimeout)
		end_time = time()
		time_taken = end_time - start_time
		out_file.write(i)
		if args.verbose:
			print ("%s works!" % proxy)
			print('time: ' + str(time_taken) + '\n')
	except:
		pass
		if args.verbose:
			print ("%s does not respond.\n" % proxy)


def start(self):
        for page in range(1, 10):
            page_result = self.extract_proxy(page)
            time.sleep(3)

            if not page_result:
                return

            self.result.extend(page_result)

def extract_proxy(self, page_num):
        try:
            rp = requests.get(self.url.format(page=page_num), proxies=self.cur_proxy, timeout=10)

            re_ip_result = self.re_ip_pattern.findall(rp.text)
            re_port_encode_result = self.re_port_encode_pattern.findall(rp.text)

            if not len(re_ip_result) or not len(re_port_encode_result):
                raise Exception("empty")

            if len(re_ip_result) != len(re_port_encode_result):
                raise Exception("len(host) != len(port)")

        except Exception as e:
            logger.error("[-] Request page {page} error: {error}".format(page=page_num, error=str(e)))
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []

        re_port_result = []
        for each_result in re_port_encode_result:
            each_result = each_result.strip()
            re_port_result.append(int(''.join(list(map(lambda x: self.port_dict.get(x, ''), each_result)))))

        result_dict = dict(zip(re_ip_result, re_port_result))
        return [{"host": host, "port": int(port), "from": "cnproxy"} for host, port in result_dict.items()]

def check_proxy(proxy):
    '''
        Function for check proxy return ERROR
        if proxy is Bad else
        Function return None
    '''
    try:
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        session.max_redirects = 300
        proxy = proxy.split('\n',1)[0]
        print(Fore.LIGHTYELLOW_EX + 'Checking ' + proxy)
        session.get(URL, proxies={'http':'http://' + proxy}, timeout=TIMEOUT,allow_redirects=True)
    except requests.exceptions.ConnectionError as e:
        print(Fore.LIGHTRED_EX + 'Error!')
        return e
    except requests.exceptions.ConnectTimeout as e:
        print(Fore.LIGHTRED_EX + 'Error,Timeout!')
        return e
    except requests.exceptions.HTTPError as e:
        print(Fore.LIGHTRED_EX + 'HTTP ERROR!')
        return e
    except requests.exceptions.Timeout as e:
        print(Fore.LIGHTRED_EX + 'Error! Connection Timeout!')
        return e
    except urllib3.exceptions.ProxySchemeUnknown as e:
        print(Fore.LIGHTRED_EX + 'ERROR unkown Proxy Scheme!')
        return e
    except requests.exceptions.TooManyRedirects as e:
        print(Fore.LIGHTRED_EX + 'ERROR! Too many redirects!')
        return e            

if __name__ == "__main__":

	global chosenTimeout
	global txtfile
	global site

	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--timeout", type=int, help="dismiss the proxy after -t seconds", default=20)
	parser.add_argument("-p", "--proxy", help="check HTTPS or HTTP proxies", default='http')
	parser.add_argument("-l", "--list", help="path to your list.txt", default='output.txt')
	parser.add_argument("-s", "--site", help="check with specific website like google.com", default='google.com')
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	chosenTimeout = args.timeout
	txtfile = args.list
	site = args.site
	proxyType = args.proxy

	threading.Thread(target=checkproxy, args=(txtfile,)).start()
