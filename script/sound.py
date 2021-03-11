import pygame
pygame.mixer.init(48000, -16, 1, 1024)
charge=pygame.mixer.Sound("..//ressources//sound//charge.wav")
bug=pygame.mixer.Sound("..//ressources//sound//bug.wav")
activation=pygame.mixer.Sound("..//ressources//sound//activation.wav")
loop=pygame.mixer.Sound("..//ressources//sound//loop.wav")

print("Volume of charge is "+str(charge.get_volume()))
print("Volume of bug is "+str(bug.get_volume()))
print("Volume of activation is "+str(activation.get_volume()))
print("Volume of loop is "+str(loop.get_volume()))
