# -*- coding: utf-8 -*-
from random import randrange
import random 
import os
import os.path



def pgcd(a, b): 
	if a < b: 
		return pgcd(b, a) 
	elif a % b == 0: 
		return b; 
	else: 
		return pgcd(b, a % b) 
def power(a, b, c): 
	x = 1
	y = a 

	while b > 0: 
		if b % 2 == 0: 
			x = (x * y) % c; 
		y = (y * y) % c 
		b = int(b / 2) 

	return x % c 
def egcd(a,b):
	    if a == 0:
	        return b, 0, 1
	    else:
	        g, y, x = egcd(b % a, a)
	        return g, x - (b // a) * y, y
def modinv(a,p):
		if a < 0:
			return p - modinv(-a,p)
		g, x, y = egcd(a,p)
		if g != 1:
			print("les deux nombre ne sont pas premiers entre eux")
		else:
			return x % p
def Miller_Rabin_Optimized (n,k):
    d=(n-1)>>1      
    s=1             
    while not d&1 : 
        s+=1        
        d>>=1       
    while k :  
        k-=1
        a=randrange(1,n) 
        if pow(a,d,n)!=1: 
            while s: 
                s-=1
                if pow(a,d<<s,n)!=n-1: 
                    return True
                
    return False  
def generate (lengh=2048,nombredetest=4400,marge=1) :
    pre=1<<int(lengh)
    pre2=pre>>int(marge)
    pre2+=1
    r1=True
    while r1 :
        t=randrange(pre2,pre,2)
        r1=Miller_Rabin_Optimized(t,nombredetest)
    return t

class Trio :
	def __init__(self):
		self.x=0
		self.y=0
		self.z=0

	def __repr__(self):
		return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"
class Personne:
	def __init__(self,p,g,name) :
		self.name=name
		self.privatek=0
		self.publick=Trio()
		self.p=p
		self.g=g		

	def generationcles(self):
		self.privatek=random.randint(10**20,self.p)
		self.publick.x=self.p
		self.publick.y=self.g
		self.publick.z=power(self.g,self.privatek,self.p)

	def chiffrement(self,msg,name):
		msgcrypt = []
		k=random.randint(10**20,self.p)
		while pgcd(self.p,k) != 1: 
			k=random.randint(10**20,self.p)
		res = []
		liste = []
		for i in range(len(msg)) :
			liste.append(msg[i])
			res.append(ord(liste[i]))
		i=0
		while i<len(res):
			msgcrypt.append((power(name.publick.z,k,self.p)*res[i])%self.p)
			i=i+1
			
		alpha=power(self.g,k,self.p)
		path=os.getcwd()+"/"+str(name.name)
		filecrypt=open(path+"/msgcrypte.txt","w")
		filecrypt.write("#alpha= #"+str(alpha))
		filecrypt.write("#msgcrypte= #[")
		for i in range(len(msgcrypt)):
			filecrypt.write(","+str(msgcrypt[i]))
		filecrypt.write("]")
		filecrypt.close()

	def dechiffrement(self):
		path=os.getcwd()+"/"+self.name
		filecrypt=open(path+"/msgcrypte.txt","r")
		liste=filecrypt.read().split("#",-1)
		alpha=int(liste[2])
		msgcrypt=(liste[4][2:][:-1]).split(",",-1)

		alphaps=power(alpha,self.privatek,self.p)
		inv=modinv(alphaps,self.p)
		msgdecrypt = []
		for i in range(len(msgcrypt)):
				msgdecrypt.append((int(msgcrypt[i])*inv)%self.p)
		msgclaire=""
		for j in range(len(msgdecrypt)):
			msgdecrypt[j]=chr(int(msgdecrypt[j]))
			msgclaire+=msgdecrypt[j]

		path=os.getcwd()+"/"+self.name
		filemsgdecrypt=open(path+"/msgresultant.txt","w")
		filemsgdecrypt.write(msgclaire)
	
	def traitement(self):
		path=os.getcwd()
		if not os.path.exists(self.name):
 			os.makedirs(self.name)
 		path=path+"/"+self.name
		filePrivate=open(path+"/privatek.key", "w")
		filePublic=open(path+"/publick.key","w")
		filePublic.write("La clé publique : ("+str(self.publick.x)+","+str(self.publick.y)+")")
		filePrivate.write("La clé privée :"+str(self.privatek))
		filePublic.close()
		filePrivate.close()


	def exchange(self,name):
		path=os.getcwd()+"/"+name
		filePublic=open(path+"/"+self.name+"publick.key","w")
		filePublic.write("La clé publique de "+self.name+" : ("+str(self.publick.x)+","+str(self.publick.y)+")")



p=generate()
g=random.randint(10**20,p)

Alice=Personne(p,g,"Alice")
Alice.generationcles()
Alice.traitement()

Bob=Personne(p,g,"Bob")
Bob.generationcles()
Bob.traitement()

Alice.exchange("Bob")
Bob.exchange("Alice")

Alice.chiffrement("La cryptographie sur les courbes elliptiques (en anglais, elliptic curve cryptography ou ECC) regroupe un ensemble de techniques cryptographiques qui utilisent une ou plusieurs proprietes des courbes elliptiques, ou plus generalement d'une variete abelienne. Lusage des courbes elliptiques en cryptographie a ete suggere, de maniere independante, par Neal Koblitz et Victor Miller en 19851,2. Lutilisation de ces proprietes permet d'ameliorer les primitives cryptographiques existantes, par exemple en reduisant la taille des cles cryptographiques, ou de construire de nouvelles primitives cryptographiques qui netaient pas connues auparavant3",Bob)
Bob.dechiffrement()

#p=78084951718833187247463657970187635903089107970849189063607467831286793591317
#256#112489706547805680681997956586322193988966711729069468701815855726628664961071
#128#266630928676002844456974016357904043283
#512#12090746193124469179524718808873322184854326015972092444965790407317478541754793385378333116480845332238519333399419492325564723872970143077530700739576061
#1024#179050961710446192895682572212499115394219671322495801929355102504548683845366092639196183751597813545048511563855851106719107856738886211748220164372313996741569841683197759024884757192605917005860866856103023055606617020566057720160899334818356478269298568446820457451298427466902117366124113957419198161223
