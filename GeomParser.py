#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Parse a Spectral Solver Geometry File and Generate material.config file
import numpy as np
import os
import argparse


PhaseCrys=open('CrysPhaseCpTi.txt','r')
PC=PhaseCrys.readlines()
PhaseCrys.close()

os.system('clear')

parser=argparse.ArgumentParser()
parser.add_argument("--geom",help=" Enter the .geom filename ")
args=parser.parse_args()

try:
  fGeom=open(args.geom,"r")
except IOError: 
  sys.exit("Did not find specified .geom file")  
  
HStr=fGeom.readline().split('\t')[0]

Header=int(HStr)

H=[]
for i in range(Header):
  H.append(fGeom.readline())

GeomStr=fGeom.readlines()

fGeom.close()

GrainID=[]
EulerStr=[]

for i in range(len(H)):
  if H[i].split()[0][1:6]=='Grain':
    GrainID.append(int(H[i][6:-2]))
  elif H[i].split('\t')[0]=='(gauss)':
    EulerStr.append(H[i].split('\t')[1:-2])
    
EulerAng=np.empty((len(EulerStr),3))
for i in range(len(EulerAng)):
  EulerAng[i,0]=float(EulerStr[i][0].split()[1])
  EulerAng[i,1]=float(EulerStr[i][1].split()[1])
  EulerAng[i,2]=float(EulerStr[i][2].split()[1])
  
GeomS=[i.split() for i in GeomStr]
Geom = [item for sublist in GeomS for item in sublist]
Geom=np.asarray(Geom)
for i in range(len(Geom)):
  Geom[i]=Geom[i].astype(int)

UID=np.unique(Geom).astype(int)
UID=np.sort(UID)
GrainNum=range(1,len(UID)+1)

IDString=[]
for i in GrainNum:#UID:
  if i<=9:
    IDString.append('[Grain'+'000'+str(i)+']'+'\n')
  elif i<=99:
    IDString.append('[Grain'+'00'+str(i)+']'+'\n')
  elif i<=999:
    IDString.append('[Grain'+'0'+str(i)+']'+'\n')
  else:
    IDString.append('[Grain'+str(i)+']'+'\n')



EulerDict={}
for i in range(len(UID)):
  EulerDict[UID[i]]=EulerAng[GrainID.index(UID[i])]

NumDict={}

NewGrain=np.arange(1,len(UID)+1).astype(str)
for i in range(len(UID)):
  NumDict[str(UID[i])]=NewGrain[i]
for i in range(len(GeomS)):
  for j in range(len(GeomS[0])):
    GeomS[i][j]=NumDict[GeomS[i][j]]

for i in range(len(GeomS)):
  GeomS[i]='\t'.join(GeomS[i])


"""NewGeomFile=open('NewGeom.geom','w')
for lines in GeomS:
  NewGeomFile.write("%s\n" % lines)

NewGeomFile.close()"""
  
  
# Write material.config file
OutFile=open('material.config','w')
OutFile.writelines('<homogenization>\n')
OutFile.writelines('[SX]\n')
OutFile.writelines('type\tNone\n')
OutFile.writelines('#Ngrains\t'+str(len(UID))+'\n')
OutFile.writelines('<microstructure>\n')
for i in range(len(IDString)):
  OutFile.write(IDString[i])  
  OutFile.write('crystallite\t1\n')
  OutFile.write('(constituent)\tphase\t1\ttexture\t\t'+str(GrainNum[i])+'\t\tfraction\t1.0'+'\n')
for lines in PC:
  OutFile.write("%s\n" %lines)
OutFile.writelines('<texture>\n')
for i in range(len(UID)):
  OutFile.write(IDString[i])
  OutFile.write('(gauss)'+'\t'+'phi1'+'\t'+str(EulerDict[UID[i]][0])+'\t'+'Phi'+\
                '\t'+str(EulerDict[UID[i]][1])+'\t'+'phi2'+'\t'+str(EulerDict[UID[i]][2])+\
                '\t'+'scatter'+'\t'+'0.0'+'\t'+'fraction'+'\t'+'1.0'+'\n')

    

OutFile.close()








