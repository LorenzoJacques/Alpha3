import math
import pygame
import easy
import settings

r0=settings.r0
r1=settings.r1
r2=settings.r2
point=easy.coord_points_9(r0,r1,r2) #Liste de coordonnées des 9 points placés le long des trois cercles prévue pour être redistribuée dans les positions de Data

#Data
Data=[0]*30
Data[1]=  { "img" : pygame.image.load("..//ressources//img//white//01.png").convert_alpha(), "need" : [],        "pos" : point[1],  "tilt" :  160  }
Data[2]=  { "img" : pygame.image.load("..//ressources//img//white//02.png").convert_alpha(), "need" : [1],       "pos" : point[2],  "tilt" : 120   }
Data[3]=  { "img" : pygame.image.load("..//ressources//img//white//03.png").convert_alpha(), "need" : [2],       "pos" : point[3],  "tilt" : 80    }
Data[4]=  { "img" : pygame.image.load("..//ressources//img//white//04.png").convert_alpha(), "need" : [1],       "pos" : point[4],  "tilt" : 40    }
Data[5]=  { "img" : pygame.image.load("..//ressources//img//white//05.png").convert_alpha(), "need" : [2,4],     "pos" : point[5],  "tilt" : 0     }
Data[6]=  { "img" : pygame.image.load("..//ressources//img//white//06.png").convert_alpha(), "need" : [3,5],     "pos" : point[6],  "tilt" : -40   }
Data[7]=  { "img" : pygame.image.load("..//ressources//img//white//07.png").convert_alpha(), "need" : [4],       "pos" : point[7],  "tilt" : -80   }
Data[8]=  { "img" : pygame.image.load("..//ressources//img//white//08.png").convert_alpha(), "need" : [5,7],     "pos" : point[8],  "tilt" : -120  }
Data[9]=  { "img" : pygame.image.load("..//ressources//img//white//09.png").convert_alpha(), "need" : [6,8],     "pos" : point[9],  "tilt" :  -160 }
Data[11]= { "img" : pygame.image.load("..//ressources//img//white//11.png").convert_alpha(), "need" : [1,00],    "pos" : point[11], "tilt" :  160  }
Data[12]= { "img" : pygame.image.load("..//ressources//img//white//12.png").convert_alpha(), "need" : [2,11],    "pos" : point[12], "tilt" : 120   }
Data[13]= { "img" : pygame.image.load("..//ressources//img//white//13.png").convert_alpha(), "need" : [3,12],    "pos" : point[13], "tilt" : 80    }
Data[14]= { "img" : pygame.image.load("..//ressources//img//white//14.png").convert_alpha(), "need" : [4,11],    "pos" : point[14], "tilt" : 40    }
Data[15]= { "img" : pygame.image.load("..//ressources//img//white//15.png").convert_alpha(), "need" : [5,12,14], "pos" : point[15], "tilt" : 0     }
Data[16]= { "img" : pygame.image.load("..//ressources//img//white//16.png").convert_alpha(), "need" : [6,13,15], "pos" : point[16], "tilt" : -40   }
Data[17]= { "img" : pygame.image.load("..//ressources//img//white//17.png").convert_alpha(), "need" : [7,14],    "pos" : point[17], "tilt" : -80   }
Data[18]= { "img" : pygame.image.load("..//ressources//img//white//18.png").convert_alpha(), "need" : [8,15,17], "pos" : point[18], "tilt" :  -120 }
Data[19]= { "img" : pygame.image.load("..//ressources//img//white//19.png").convert_alpha(), "need" : [9,16,18], "pos" : point[19], "tilt" :  -160 }
Data[21]= { "img" : pygame.image.load("..//ressources//img//white//21.png").convert_alpha(), "need" : [11],      "pos" : point[21], "tilt" : 160    }
Data[22]= { "img" : pygame.image.load("..//ressources//img//white//22.png").convert_alpha(), "need" : [12,21],   "pos" : point[22], "tilt" :   120 }
Data[23]= { "img" : pygame.image.load("..//ressources//img//white//23.png").convert_alpha(), "need" : [13,22],   "pos" : point[23], "tilt" : 80    }
Data[24]= { "img" : pygame.image.load("..//ressources//img//white//24.png").convert_alpha(), "need" : [14,21],   "pos" : point[24], "tilt" :   40  }
Data[25]= { "img" : pygame.image.load("..//ressources//img//white//25.png").convert_alpha(), "need" : [15,22,24],"pos" : point[25], "tilt" : 0     }
Data[26]= { "img" : pygame.image.load("..//ressources//img//white//26.png").convert_alpha(), "need" : [16,23,25],"pos" : point[26], "tilt" :   -40 }
Data[27]= { "img" : pygame.image.load("..//ressources//img//white//27.png").convert_alpha(), "need" : [17,24],   "pos" : point[27], "tilt" : -80   }
Data[28]= { "img" : pygame.image.load("..//ressources//img//white//28.png").convert_alpha(), "need" : [18,25,27],"pos" : point[28], "tilt" :   -120}
Data[29]= { "img" : pygame.image.load("..//ressources//img//white//29.png").convert_alpha(), "need" : [19,26,28],"pos" : point[29], "tilt" :   -160}

import pygame.freetype
pygame.freetype.init()
ending_font=pygame.freetype.Font("..//ressources//jmh-legajo.regular.ttf")

ending_text=["Du vide à la lumière",
"de pluton au soleil",
"de la mort à l'entre",
" ",
"De la periphérie vers le centre",
"de l'imparfait au parfait",
"vous avez complété le cercle",
"suivant les antiques méthodes de l'Alchimie",
" ",
"Et ainsi vous avez accédé par Esso",
"l\'être dans l'instant",
"à l'immortalité dans le présent",
" ",
"Nicolas Flamel"]

ending_image=pygame.Surface((500,500))
for i in range(0,len(ending_text)) :
    ending_font.render_to(ending_image,(0,i*10),ending_text[i],fgcolor=pygame.Color(0,0,0),bgcolor=pygame.Color(255,255,255),size=20)
