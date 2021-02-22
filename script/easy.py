import math

#Sont stockées içi des méthodes personnalisée utilisées un peu partout

def CenterBlit(surface,img,pos) : #Blit une image dont le centre sera les coordonannées précisées
	temp_pos=([pos[0]-(img.get_width()/2),pos[1]-(img.get_height()/2)])
	surface.blit(img,temp_pos)

def easy_trigo(angle,r) : #Retourne un tupple des coordonnée d'un point place sur un cercle de rayon r et placé sur un angle en radians
	tempX=r*math.cos(math.radians(angle))
	tempY=r*math.sin(math.radians(angle))
	return (tempX,tempY)

def coord_points_9(r0,r1,r2) : #Retourne une liste de coordonnées de 9 points placés le long de trois cercles de rayon r0, r1, r2
	points=[110,150,190,230,270,310,350,30,70]
	my_list=[0]
	for point in points :
		my_list.append(easy_trigo(point,r0))
	my_list.append(0)
	for point in points :
		my_list.append(easy_trigo(point,r1))
	my_list.append(0)
	for point in points :
		my_list.append(easy_trigo(point,r2))
	return my_list
