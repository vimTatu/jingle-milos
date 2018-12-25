import re
from tqdm import tqdm


X = 0
target_ip = []
Y = 0
with open('2018-12-25-16-25-35.html', 'r') as milos:
    html_source = milos.readlines()

for html_line in tqdm(html_source):

    color = re.findall('color:......\"', str(html_line))[0].split(':')[1].split('\"')[0]
    s = html_line.split('<')[1].split('>')[1]
    icolor = re.findall('..', str(color))
    for i in s:
        if X<150:
            target_ip.append('2001:4c08:2028:{}:{}:{}:{}:{}'.format(X, Y, icolor[0],icolor[1],icolor[2]))
            X +=1
        else:
            with open('ipv6.txt', 'a') as ips:
                for line in target_ip:
                    ips.write(line + '\n')
            Y += 1
            target_ip = []
            X = 0
