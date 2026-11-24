from kandinsky import fill_rect as R,draw_string as S,color as C
from ion import keydown as K,KEY_UP as U,KEY_DOWN as V,KEY_OK as W,KEY_BACK as B
WH=C(255,255,255);BK=C(0,0,0);GR=C(178,190,205);DG=C(90,105,125)
BL=C(28,60,120);OR=C(235,120,20);LG=C(240,244,250)
Z="""Alésage|Trou précis recevant un arbre|b|c,160,110,44,0
Arbre|Pièce cylindrique précise d'un assemblage|c|k,45,110,230,2
Arrondi|Arrondit l'arête d'un angle saillant|b|u,30,45,25,0
Bossage|Surépaisseur à l'entrée d'un perçage|b|g,80,25,40,20;g,200,25,40,20;w,95,45,14,132;w,215,45,14,132
Chambrage|Évidement d'alésage limitant sa portée|b|w,146,45,28,35;w,120,80,80,60;w,146,140,28,37
Chanfrein|Surface conique supprimant une arête vive|b|t,30,45,30,0;t,290,45,-30,0
Collet|Couronne cylindrique servant de butée|c|g,35,95,250,36
Congé|Surface arrondie entre deux surfaces|b|u,30,45,30,0
Dégagement|Usinage au fond d'un angle (contact)|b|w,150,150,50,27
Embase|Base élargie de la pièce (semelle)|b|g,15,160,290,17
Évidement|Vide pour alléger la pièce|b|w,80,75,160,102
Filetage|Rainure hélicoïdale sur un cylindre (vis)|c|z,55,62,210,42;z,55,112,210,44
Fraisure|Cône logeant la tête de vis|b|f,150,45,22,28;w,150,67,12,110
Gorge|Loge un joint ou un anneau (cylindre)|c|w,155,45,10,25
Lamage|Logement pour tête de vis|b|w,120,45,80,30;w,150,75,20,102
Languette|Entrant dans la rainure (liaison glissière)|b|g,140,28,40,17
Méplat|Surface plane sur un cylindre|q|w,40,72,64,80;k,104,72,2,80
Nervure|Paroi mince augmentant la rigidité|n|g,148,70,24,65
Perçage|Trou au foret, débouchant ou non|b|w,120,45,14,132;w,200,45,14,132
Perçage borgne|Trou sans traverser, fond pointu|b|p,150,45,20,85
Rainure|Entaille longue dans la pièce|b|w,70,80,180,18
Taraudage|Trou fileté (rainure hélicoïdale)|b|w,150,45,20,132;z,153,50,14,122
Épaulement|Changement de section (surface d'appui)|e|
Trou oblong|Fente allongée à bouts arrondis|b|w,90,105,140,26;c,103,118,13,0;c,217,118,13,0;k,103,105,114,1;k,103,130,114,1"""
T=[l.split("|") for l in Z.split("\n")];N=len(T)
def O(x,y,w,h):
 R(x,y,w,1,BK);R(x,y+h-1,w,1,BK);R(x,y,1,h,BK);R(x+w-1,y,1,h,BK)
def CF(x,y,r,c):
 i=-r
 while i<=r:t=int((r*r-i*i)**.5);R(x-t,y+i,2*t+1,1,c);i+=1
def ZG(x,y,w,h):
 yy=y
 while yy<y+h-3:
  xx=x+1
  while xx<x+w-5:R(xx,yy,2,3,DG);R(xx+3,yy+3,2,3,DG);xx+=8
  yy+=6
def BASE(b):
 if b=="c":R(45,45,230,132,GR);O(45,45,230,132)
 elif b=="q":CF(160,112,74,BK);CF(160,112,72,GR)
 elif b=="n":R(30,135,260,42,GR);O(30,135,260,42)
 elif b=="e":R(60,90,200,87,GR);O(60,90,200,87);R(110,45,100,46,GR);O(110,45,100,46)
 else:R(30,45,260,132,GR);O(30,45,260,132)
def FEAT(s):
 if not s:return
 for it in s.split(";"):
  x,y,w,h=[int(q) for q in it[2:].split(",")];k=it[0]
  if k=="w":R(x,y,w,h,WH)
  elif k=="g":R(x,y,w,h,GR);O(x,y,w,h)
  elif k=="k":R(x,y,w,h,BK)
  elif k=="c":CF(x,y,w+2,BK);CF(x,y,w,WH)
  elif k=="p":
   R(x,y,w,h,WH);n=0
   while w-2*n>0:R(x+n,y+h+n,w-2*n,2,WH);n+=1
  elif k=="f":
   for i in range(h):a=(w*i)//h;R(x-a,y+i,12+2*a,2,WH)
  elif k=="t":
   f=w>0
   if not f:w=-w
   for i in range(w):R(x-w+i if f else x,y+i,w-i,2,WH)
  elif k=="u":
   for i in range(w):t=int((w*w-(w-i)**2)**.5);R(x,y+i,w-i,2,WH);R(x,y+i,t,2,GR)
  elif k=="z":ZG(x,y,w,h)
def LIST(s):
 R(0,0,320,222,WH);R(0,0,320,26,BL);S("USINAGE STI2D",6,4,WH,BL)
 t=s-s%8
 for j in range(8):
  i=t+j
  if i>=N:break
  y=34+j*23
  if i==s:R(2,y-4,316,22,OR);S(T[i][0],8,y,WH,OR)
  else:S(T[i][0],8,y,BK,WH)
 S("OK:voir",4,200,DG,WH)
def CARD(i,rv):
 n,d,b,s=T[i]
 R(0,0,320,222,WH);R(0,0,320,26,BL)
 S(n,4,4,WH,BL);S(str(i+1)+"/"+str(N),250,4,OR,BL)
 BASE(b);FEAT(s)
 R(0,148,320,74,LG)
 if rv:
  for j in range(0,len(d),30):S(d[j:j+30],6,157+(j//30)*20,BL,LG)
 else:S("BAS:def",6,180,DG,LG)
m=0;i=0;rv=0;LIST(i)
while 1:
 if K(V):
  while K(V):pass
  if m:rv=1;CARD(i,rv)
  else:i=(i+1)%N;LIST(i)
 elif K(U):
  while K(U):pass
  if m and rv:rv=0;CARD(i,0)
  elif m:m=0;LIST(i)
  else:i=(i-1)%N;LIST(i)
 elif K(W):
  while K(W):pass
  if m:rv=1-rv;CARD(i,rv)
  else:m=1;rv=0;CARD(i,0)
 elif K(B):
  while K(B):pass
  if m:m=0;LIST(i)
