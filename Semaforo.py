from threading import Thread, Semaphore, Lock
import time
import random
mutex = Lock()
index = 0
n=3
buf = [] #area critica, impossivel alocar exatamente 1000 posições em python
out_ = 0
in_ = 0
bos = Semaphore(value=n)
dolu = Semaphore(value=0)
class Producer(Thread):

    def run(self):
        global buf
        global in_
        global bos
        global dolu
        while True:
            nums = range(5)
            item = random.choice(nums) #sorteia um numero q sera inserido no vetor
            bos.acquire()
            mutex.acquire()
            buf.append(item) #produz no final do vetor
            in_ = (in_ + 1) % n
            print("P["+str(in_)+"] Produziu o numero:  "+ str(item))
            print("Regiao critica: ");
            print(buf);
            mutex.release()
            dolu.release()
            time.sleep(2) #aguarda um tempo randomico para alimentar a area critica
class Consumer(Thread):
    def run(self):
        global buf
        global out_
        global bos
        global dolu
        while True:
            dolu.acquire()
            mutex.acquire()
            item = buf[0] #consome do inicio
            del(buf[0]);  #elimina o consumido
            print("C["+str(out_)+"] Consumiu o numero:  "+str(item))
            print("Regiao critica: ");
            print(buf);
            mutex.release()
            bos.release()
            time.sleep(2) #pause um tempo randomico até tentar consumir o proximo

#inicia 5 processos produtores, que executarão indeterminadamente alimentando o vetor
Producer().start()
Producer().start()
Producer().start()
Producer().start()
Producer().start()
#inicia 5 processos consumidores que consumem oq estiver disponivel no vetor
Consumer().start()
Consumer().start()
Consumer().start()
Consumer().start()
Consumer().start()
