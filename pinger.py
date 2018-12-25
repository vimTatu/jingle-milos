import queue
import socket
import threading

from settings import src_address

#Load file with IPv6 address range to ping.
with open('ipv6.txt', 'r') as ranges:
    ips = ranges.readlines()

class Pinger(threading.Thread):
    """
    Class which will ingerit python threading class.
    Builds without params. After thread finished jobs in queue, it needs to be `.join`ed
    """

    def __init__(self, threadID, name, q):
        """
        Thread constructor.
        Args: 
        threadID - unique thread identifier
        name - unique thread name
        q - IP addresses queue.
        Returns:
        Object with start() function, which is run ping.
        """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = str(name)
        self.q = q

    
    def run(self):
        """
        Decorative function.
        Prints thread info before and after job
        """
        print('Started thread {}'.format(self.name))
        ping(self.name, self.q)
        print("Exiting" + self.name)


def ping(threadName, q):
    """
    Send empty ICMP packets for IP addresses in thread queue
    data - minimal requirenment for ICMP packet
    src_address should be specified in settings.py
    Args:
    threadName - name of thread
    q - IP addresses queue
    """
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            PING_TARGET = q.get()
            if PING_TARGET:
                queueLock.release()
                data = b'\x80\0\0\0\0\0\0\0'
                sock = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.getprotobyname('ipv6-icmp'))
                sock.bind((src_address, 0))
                sock.sendto(data, (PING_TARGET, 0, 0, 0))
                sock.close()


# Creates pool of names for thread. Range defines count of threads.
thread_list = []
for i in range(1, 10):
    thread_list.append(i)

queueLock = threading.Lock()
workQueue = queue.Queue(50000)
#list of current working threads
threads = []


def main():
    """
    Main function of project.
    Runs cyclic. Renders image on remote LED-display.
    exitFlag - global variable which is triggering thread exit.
    """
    global exitFlag
    exitFlag = 0
    threadID = 1
    queueLock.acquire()
    for target in ips:
        workQueue.put(target)
    queueLock.release()
    for tname in thread_list:
        thread = Pinger(threadID, tname, workQueue)
        threadID += 1
        thread.start()
        threads.append(thread)
    while not workQueue.empty():
        pass
    exitFlag = 1
    for t in threads:
        t.join()
        
    main()


if __name__ == '__main__':
    main()
