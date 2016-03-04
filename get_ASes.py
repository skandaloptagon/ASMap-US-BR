import requests
from bs4 import BeautifulSoup

br = BeautifulSoup(requests.get("https://www-public.tem-tsp.eu/~maigron/RIR_Stats/RIR_Delegations/Delegations/ASN/BR.html").text, 'html.parser')
us = BeautifulSoup(requests.get("https://www-public.tem-tsp.eu/~maigron/RIR_Stats/RIR_Delegations/Delegations/ASN/US.html").text, 'html.parser')

with open("br.as", "wb") as f:
    for link in br.find_all('a'):
        try:
    	    f.write(str(int(link.text)) + '\n')
        except:
            continue

with open("us.as", "wb") as f:
    for link in us.find_all('a'):
        try:
    	    f.write(str(int(link.text)) + '\n')
	except:
	    continue
