import pygame
import asyncio
import bleak
from bleak import BleakClient
from time import sleep
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps, ImageFilter
import os
import time
import math

def pg_init() :
	pygame.init()
	pos = pygame.display.set_mode((600, 800))
	pygame.display.set_caption('Positioning System')
	icon = pygame.image.load('C:/controller/posicon.png')
	pygame.display.set_icon(icon)

	return pos

def getKey(keyName) :
	ans = False
	for eve in pygame.event.get(): pass
	keyInput = pygame.key.get_pressed()
	myKey = getattr(pygame, 'K_{}'.format(keyName))
	if keyInput[myKey]:
		ans = True
	pygame.display.update()
	return ans

def readPath() :
    inFp = None
    inList, inStr = [], ''
    inFp = open('C:/linelist/testline.txt', 'r')
    inList = inFp.readlines()
    inFp.close()
    for i in range(0, len(inList)):
        inList[i] = list(map(int, inList[i].split(',')))

    return inList

def sin(x) :
	return math.sin(math.radians(x))

def cos(x) :
	return math.cos(math.radians(x))