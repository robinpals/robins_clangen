from random import choice
from scripts.cat.sprites import sprites
import random
from re import sub
from scripts.game_structure.game_essentials import game
from .pelts import Pelt


    

class Genotype():
    """Holds all appearence information for a cat. """
    def __init__(self,
                 ginger_gene:tuple= ("",""),
                 ) -> None:
        self.ginger_gene = ginger_gene
    def ginger_gene_create(self, gender:str):
        """creates ginger genes"""
        x = ""
        x2 = ""
        y = ""
        ginger_gene = (x,y)
        """this is by default bc i think you need to do this for functions to refer
        to it later. you'd also need to add it
        as a thing in cats.py i think. maybe this could be it's own py thing. shrug."""
        if gender == "male":
            ginger_gene = (x,y)
            if Pelt.colour in Pelt.ginger_colours:
                x = "O"
            elif Pelt.colour in Pelt.black_colours or Pelt.colour in Pelt.brown_colours:
                x = "o"
            else:
                x = ""
        elif gender == "female":
            ginger_gene  = (x,x2)
            if Pelt.colour in Pelt.ginger_colours and Pelt.name != "Tortie" and Pelt.name != "Calico":
                x = "O"
                x2 = "O"
            elif Pelt.name in ["Tortie", "Calico"]:
                x = "O"
                x2 = "o"
            elif Pelt.colour in Pelt.ginger_colours or Pelt.colour in Pelt.brown_colours:
                x = "o"
                x2 ="o"
        elif gender == "intersex":
            ginger_gene = (x,y)
            x = ""
            print("this is a placeholder until i add new intersex types. currently just takes from male code")
        return ginger_gene
        