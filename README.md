# Alpha3
Logiciel embarqué du projet __Alpha3__  
  
Réalisé dans le cadre d'une résidence au seins du FabLab de La Casemate, Alpha3 propose uen éxperience ludique basée sur la mythologie de l'alchimie.
Son but est double :  
* Prendre en main des composants éléctroniques et leur intégration dans un script Python  
  
* Observer le comportment des joueurs face à un jeu aux moyens d'intéraction non conventionnels  

L'ensemble du programme se trouve dans le dossier __/script__ :  
  
* /script/AlphaV3.py : Script principal  
* /script/data.py : Données de jeu
* /script/cache.py : Mise en cache des animations  
* /script/sound.py : Gestion du son 
* /script/driver_button.py : Gestion du mécanisme d'activation d'Alpha  
* /script/driver_encoder.py : Detection de l'engrenage d'Alpha, basé sur un encoder rotatif incrémental (1200P / R) 
* /script/driver_potentiometer.py : Detection du potentiomètre d'Alpha, basé sur un potentiomètre linéraire 10k ohm  
* /script/settings.py : Variables diverses
