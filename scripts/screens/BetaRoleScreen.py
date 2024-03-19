#!/usr/bin/env python3
# -*- coding: ascii -*-
import os
import pygame

from scripts.utility import scale

from .Screens import Screens

from scripts.utility import get_text_box_theme, shorten_text_to_fit
from scripts.cat.cats import Cat
from scripts.game_structure import image_cache
import pygame_gui
from scripts.game_structure.image_button import UIImageButton, UITextBoxTweaked
from scripts.game_structure.game_essentials import game, screen_x, screen_y, MANAGER
from ..game_structure.windows import ChangeCatToggles


class BetaRoleScreen(Screens):
    the_cat = None
    selected_cat_elements = {}
    buttons = {}
    next_cat = None
    previous_cat = None
    warrior_options_visible = True
    apprentice_options_visible = True
    role_text_buttons = {}
    scroll_options_size = ()
    favorite_string = ""
    

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                self.change_screen("profile screen")
            elif event.ui_element == self.next_cat_button:
                if isinstance(Cat.fetch_cat(self.next_cat), Cat):
                    game.switches["cat"] = self.next_cat
                    self.update_selected_cat()
                    self.invalid_disclaimer.hide()
                    self.update_available_roles()
                    self.warrior_options_visible = True
                    self.apprentice_options_visible = True
                    self.disable_other_buttons()
                    self.update_warrior_buttons()
                    self.update_apprentice_buttons()
                    
                    
                    
                else:
                    print("invalid next cat", self.next_cat)
            elif event.ui_element == self.previous_cat_button:
                if isinstance(Cat.fetch_cat(self.previous_cat), Cat):
                    game.switches["cat"] = self.previous_cat
                    self.update_selected_cat()
                    self.invalid_disclaimer.hide()
                    self.update_available_roles()
                    self.warrior_options_visible = True
                    self.apprentice_options_visible = True
                    self.disable_other_buttons()
                    self.update_warrior_buttons()
                    self.update_apprentice_buttons()
                   
                else:
                    print("invalid previous cat", self.previous_cat)
            elif event.ui_element == self.promote_leader:
                if self.the_cat == game.clan.deputy:
                    game.clan.deputy = None
                game.clan.new_leader(self.the_cat)
                if game.sort_type == "rank":
                    Cat.sort_cats()
                self.update_selected_cat()
            elif event.ui_element == self.promote_deputy:
                game.clan.deputy = self.the_cat
                self.the_cat.status_change("deputy", resort=True)
                self.update_selected_cat()
            elif event.ui_element == self.switch_warrior:
                self.update_warrior_buttons()
            elif event.ui_element == self.switch_defense:
                self.warrior_options_visible = True
                self.the_cat.status_change("defense", resort=True)
                self.update_selected_cat()
                self.disable_other_buttons()
            elif event.ui_element == self.switch_attack:
                self.warrior_options_visible = True
                self.the_cat.status_change("attack", resort=True)
                self.update_selected_cat()
                self.disable_other_buttons()
            elif event.ui_element == self.switch_hunt:
                self.warrior_options_visible = True
                self.the_cat.status_change("hunt", resort=True)
                self.update_selected_cat()
                self.disable_other_buttons()
            elif event.ui_element == self.switch_med_cat:
                if self.warrior_options_visible == False:
                    self.switch_defense.hide()
                    self.switch_attack.hide()
                    self.switch_hunt.hide()
                self.the_cat.status_change("medicine cat", resort=True)
                self.update_selected_cat()
                self.switch_defense.hide()
                self.switch_attack.hide()
                self.switch_hunt.hide()
            elif event.ui_element == self.switch_starteller:
                if self.warrior_options_visible == False:
                    self.switch_defense.hide()
                    self.switch_attack.hide()
                    self.switch_hunt.hide()
                self.the_cat.status_change("starteller", resort=True)
                self.update_selected_cat()
                self.switch_defense.hide()
                self.switch_attack.hide()
                self.switch_hunt.hide()
            elif event.ui_element == self.retire:
                self.the_cat.status_change("elder", resort=True)
                # Since you can't "unretire" a cat, apply the skill and trait change
                # here
                self.update_selected_cat()
            elif event.ui_element == self.switch_mediator:
                if self.warrior_options_visible == False:
                    self.switch_defense.hide()
                    self.switch_attack.hide()
                    self.switch_hunt.hide()
                self.the_cat.status_change("mediator", resort=True)
                self.update_selected_cat()
                self.switch_defense.hide()
                self.switch_attack.hide()
                self.switch_hunt.hide()
            elif event.ui_element == self.switch_warrior_app:
                self.update_apprentice_buttons()
            elif event.ui_element == self.switch_defense_app:
                self.apprentice_options_visible = True
                self.the_cat.status_change("defense apprentice", resort=True)
                self.update_selected_cat()
                self.disable_other_buttons()
            elif event.ui_element == self.switch_attack_app:
                self.apprentice_options_visible = True
                self.the_cat.status_change("attack apprentice", resort=True)
                self.update_selected_cat()
                self.disable_other_buttons()
            elif event.ui_element == self.switch_hunt_app:
                self.apprentice_options_visible = True
                self.the_cat.status_change("hunt apprentice", resort=True)
                self.update_selected_cat()
                self.disable_other_buttons()
            elif event.ui_element == self.switch_starteller_app:
                if self.apprentice_options_visible == False:
                    self.switch_defense_app.hide()
                self.the_cat.status_change("starteller apprentice", resort=True)
                self.update_selected_cat()
                self.switch_defense_app.hide()
                self.switch_attack_app.hide()
                self.switch_hunt_app.hide()
            elif event.ui_element == self.switch_med_app:
                if self.apprentice_options_visible == False:
                    self.switch_defense_app.hide()
                self.the_cat.status_change("medicine cat apprentice", resort=True)
                self.update_selected_cat()
                self.switch_defense_app.hide()
                self.switch_attack_app.hide()
                self.switch_hunt_app.hide()
            elif event.ui_element == self.switch_mediator_app:
                if self.apprentice_options_visible == False:
                    self.switch_defense_app.hide()
                self.the_cat.status_change("mediator apprentice", resort=True)
                self.update_selected_cat()
                self.switch_defense_app.hide()
                self.switch_attack_app.hide()
                self.switch_hunt_app.hide()
            elif event.ui_element == self.switch_queen:
                if self.warrior_options_visible == False:
                    self.switch_defense.hide()
                    self.switch_attack.hide()
                    self.switch_hunt.hide()
                self.the_cat.status_change("queen", resort=True)
                self.update_selected_cat()
                self.switch_defense.hide()
                self.switch_attack.hide()
                self.switch_hunt.hide()
            elif event.ui_element == self.switch_guide:
                if self.warrior_options_visible == False:
                    self.switch_defense.hide()
                    self.switch_attack.hide()
                    self.switch_hunt.hide()
                self.the_cat.status_change("guide", resort=True)
                self.update_selected_cat()
                self.switch_defense.hide()
                self.switch_attack.hide()
                self.switch_hunt.hide()
            elif event.ui_element == self.selected_cat_elements["favourite_button"]:
                self.the_cat.favourite = False
                self.selected_cat_elements["favourite_button"].hide()
                self.selected_cat_elements["not_favourite_button"].show()
                self.update_selected_cat()
                self.switch_defense_app.hide()
                self.switch_attack_app.hide()
                self.switch_hunt_app.hide()
                self.switch_defense.hide()
                self.switch_attack.hide()
                self.switch_hunt.hide()
            elif event.ui_element == self.selected_cat_elements["not_favourite_button"]:
                self.the_cat.favourite = True
                self.selected_cat_elements["favourite_button"].show()
                self.selected_cat_elements["not_favourite_button"].hide()
                self.update_selected_cat()
                self.switch_defense_app.hide()
                self.switch_attack_app.hide()
                self.switch_hunt_app.hide()
                self.switch_defense.hide()
                self.switch_attack.hide()
                self.switch_hunt.hide()
            if game.switches['window_open']:
                pass
        elif event.type == pygame.KEYDOWN and game.settings['keybinds']:
            if event.key == pygame.K_ESCAPE:
                self.change_screen("profile screen")
            elif event.key == pygame.K_RIGHT:
                game.switches["cat"] = self.next_cat
                self.update_selected_cat()
            elif event.key == pygame.K_LEFT:
                game.switches["cat"] = self.previous_cat
                self.update_selected_cat()


    def screen_switches(self):

        

        self.retire = UIImageButton(scale(pygame.Rect((250, 1300), (334, 72))), "",
                                    object_id="#retire_button",
                                    manager=MANAGER)

        self.next_cat_button = UIImageButton(scale(pygame.Rect((1244, 50), (306, 60))), "", object_id="#next_cat_button"
                                             , manager=MANAGER)
        self.previous_cat_button = UIImageButton(scale(pygame.Rect((50, 50), (306, 60))), "",
                                                 object_id="#previous_cat_button"
                                                 , manager=MANAGER)
        self.back_button = UIImageButton(scale(pygame.Rect((50, 120), (210, 60))), "", object_id="#back_button"
                                         , manager=MANAGER)
        self.cat_details_box = pygame_gui.elements.UIImage(scale(pygame.Rect
                                                                  ((25, 50), (1500, 1400))),
                                                            pygame.transform.scale(
                                                                pygame.image.load(
                                                                    "resources/images/cat_details_box.png").convert_alpha(),
                                                                (800, 700))
                                                            )
        self.roles_box = pygame_gui.elements.UIImage(scale(pygame.Rect
                                                                  ((40, 50), (1500, 1400))),
                                                            pygame.transform.scale(
                                                                pygame.image.load(
                                                                    "resources/images/roles_box.png").convert_alpha(),
                                                                (800, 700))
                                                            )
        self.role_blurb_box = pygame_gui.elements.UIImage(scale(pygame.Rect
                                                                  ((40, 51), (1500, 1400))),
                                                            pygame.transform.scale(
                                                                pygame.image.load(
                                                                    "resources/images/role_blurb_box.png").convert_alpha(),
                                                                (800, 700))
                                                            )
        self.role_section_labels = pygame_gui.elements.UIImage(scale(pygame.Rect
                                                                  ((40, 50), (1500, 1400))),
                                                            pygame.transform.scale(
                                                                pygame.image.load(
                                                                    "resources/images/role_section_labels.png").convert_alpha(),
                                                                (800, 700))
                                                            )
        self.invalid_disclaimer = pygame_gui.elements.UITextBox("This cat is either too young to change roles or their role is invalid.",
                                                                                 scale(pygame.Rect((780, 40),
                                                                                                   (600, 300))),
                                                                                 object_id="#text_box_27_horizcenter_vertcenter_spacing95",
                                                                                 starting_height=2,
                                                                                 manager=MANAGER)
        self.invalid_disclaimer.hide()
        scroll_pos = None
        if "main_scroll_container" in self.role_text_buttons and \
                            self.role_text_buttons["main_scroll_container"].vert_scroll_bar:
                        scroll_pos = self.role_text_buttons["main_scroll_container"].vert_scroll_bar.start_percentage
        if scroll_pos is not None:
                        self.role_text_buttons["main_scroll_container"].vert_scroll_bar.set_scroll_from_start_percentage(
                            scroll_pos)

        self.role_text_buttons[
            "main_scroll_container"] = pygame_gui.elements.UIScrollingContainer(
            scale(pygame.Rect((780, 300), (311, 544))), manager=MANAGER)

        self.scroll_options_size = self.role_text_buttons["main_scroll_container"].get_relative_rect()

        self.role_text_buttons[
            "main_scroll_container"].set_scrollable_area_dimensions(
            (311, self.scroll_options_size.height))
        self.role_text_buttons[
            "main_scroll_container"].horiz_scroll_bar.hide()
        self.switch_starteller = UIImageButton(scale(pygame.Rect((10, 60), (250, 60))), "starteller",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            manager=MANAGER)
       
        # LEADERSHIP
        self.promote_leader = UIImageButton(scale(pygame.Rect((775, 827), (320, 72))), "",
                                            object_id="#promote_leader_button",
                                            manager=MANAGER)
        self.promote_deputy = UIImageButton(scale(pygame.Rect((1105, 827), (320, 72))), "",
                                            object_id="#promote_deputy_button",
                                            manager=MANAGER)

        # ADULT CAT ROLES
        self.switch_warrior = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            manager=MANAGER)
        
        
        # difference of 40 per 'level' (FOR ABOVE & BELOW, not counting leader & dep)
        
        self.switch_med_cat = UIImageButton(scale(pygame.Rect((10, 120), (250, 60))), "medicine cat",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            manager=MANAGER)
        self.switch_mediator = UIImageButton(scale(pygame.Rect((10, 180), (250, 60))), "mediator",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            manager=MANAGER)
        self.switch_queen = UIImageButton(scale(pygame.Rect((10, 240), (250, 60))), "queen",
                                         	object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                         	manager=MANAGER)
        self.switch_guide = UIImageButton(scale(pygame.Rect((10, 300), (250, 60))), "guide",
                                         	object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                         	manager=MANAGER)
       

        # WARRIOR DROPDOWN STUFF (difference of 70 per level)
        self.switch_defense = UIImageButton(scale(pygame.Rect((1130, 300), (250, 60))), "guard",
                                         	object_id="#invis_hover_button",
                                            starting_height=2,
                                         	manager=MANAGER)
        self.switch_attack = UIImageButton(scale(pygame.Rect((1130, 370), (250, 60))), "runner",
                                         	object_id="#invis_hover_button",
                                            starting_height=2,
                                         	manager=MANAGER)
        self.switch_hunt = UIImageButton(scale(pygame.Rect((1130, 440), (250, 60))), "hunter",
                                         	object_id="#invis_hover_button",
                                            starting_height=2,
                                         	manager=MANAGER)

        

        # In-TRAINING ROLES:
        self.switch_warrior_app = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior",
                                                object_id="#invis_hover_button",
                                                container=self.role_text_buttons["main_scroll_container"],
                                                manager=MANAGER)
        self.switch_starteller_app = UIImageButton(scale(pygame.Rect((10, 60), (250, 60))), "starteller",
                                         	object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                         	manager=MANAGER)
        self.switch_med_app = UIImageButton(scale(pygame.Rect((10, 120), (250, 60))), "medicine cat",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            manager=MANAGER)
        self.switch_mediator_app = UIImageButton(scale(pygame.Rect((10, 180), (250, 60))), "mediator",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            manager=MANAGER)
        
        # APP DROPDOWN STUFF
        self.switch_defense_app = UIImageButton(scale(pygame.Rect((1130, 300), (250, 60))), "guard",
                                            object_id="#invis_hover_button",
                                            starting_height=2,
                                            manager=MANAGER)
        self.switch_attack_app = UIImageButton(scale(pygame.Rect((1130, 360), (250, 60))), "runner",
                                            object_id="#invis_hover_button",
                                            starting_height=2,
                                            manager=MANAGER)
        self.switch_hunt_app = UIImageButton(scale(pygame.Rect((1130, 420), (250, 60))), "hunter",
                                            object_id="#invis_hover_button",
                                            starting_height=2,
                                            manager=MANAGER)
        self.warrior_options_visible = True
        self.apprentice_options_visible = True
        self.update_selected_cat()
        self.update_available_roles()
        self.disable_other_buttons()
        self.update_warrior_buttons()
        self.update_apprentice_buttons()
        
        
    def update_warrior_abrv(self):
        self.the_cat = Cat.fetch_cat(game.switches['cat'])
        if self.the_cat.status == "defense":
            self.switch_warrior.hide()
            self.switch_warrior.kill()
            self.switch_warrior = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior (G)",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            starting_height=2,
                                            manager=MANAGER)
            self.switch_warrior.show()
        elif self.the_cat.status == "attack":
            self.switch_warrior.hide()
            self.switch_warrior.kill()
            self.switch_warrior = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior (R)",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            manager=MANAGER)
            self.switch_warrior.show()
        elif self.the_cat.status == "hunt":
            self.switch_warrior.hide()
            self.switch_warrior.kill()
            self.switch_warrior = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior (H)",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            starting_height=2,
                                            manager=MANAGER)
            self.switch_warrior.show()
        elif self.the_cat.status in ['apprentice','medicine cat apprentice', 'mediator apprentice', 'starteller apprentice']:
            self.switch_warrior.hide()
            self.switch_warrior.kill()
            self.switch_warrior_app.hide()
            self.switch_warrior_app.kill()
            self.switch_warrior_app = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior",
                                                object_id="#invis_hover_button",
                                                container=self.role_text_buttons["main_scroll_container"],
                                                starting_height=2,
                                                manager=MANAGER)
            self.switch_warrior_app.show()
        elif self.the_cat.status == "defense apprentice":
            self.switch_warrior.hide()
            self.switch_warrior.kill()
            self.switch_warrior_app.hide()
            self.switch_warrior_app.kill()
            self.switch_warrior_app = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior (G)",
                                                object_id="#invis_hover_button",
                                                container=self.role_text_buttons["main_scroll_container"],
                                                starting_height=3,
                                                manager=MANAGER)
            self.switch_warrior_app.show()
        elif self.the_cat.status == "attack apprentice":
            self.switch_warrior.hide()
            self.switch_warrior.kill()
            self.switch_warrior_app.hide()
            self.switch_warrior_app.kill()
            self.switch_warrior_app = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior (R)",
                                                object_id="#invis_hover_button",
                                                container=self.role_text_buttons["main_scroll_container"],
                                                starting_height=3,
                                                manager=MANAGER)
            self.switch_warrior_app.show()
        elif self.the_cat.status == "hunt apprentice":
            self.switch_warrior.hide()
            self.switch_warrior.kill()
            self.switch_warrior_app.hide()
            self.switch_warrior_app.kill()
            self.switch_warrior_app = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior (H)",
                                                object_id="#invis_hover_button",
                                                container=self.role_text_buttons["main_scroll_container"],
                                                starting_height=3,
                                                manager=MANAGER)
            self.switch_warrior_app.show()
        else:
            self.switch_warrior.hide()
            self.switch_warrior.kill()
            self.switch_warrior = UIImageButton(scale(pygame.Rect((10, 0), (250, 60))), "warrior",
                                            object_id="#invis_hover_button",
                                            container=self.role_text_buttons["main_scroll_container"],
                                            starting_height=3,
                                            manager=MANAGER)
            self.switch_warrior.show()

    def update_favorite_text(self):
        self.favorite_string = ""
        if self.the_cat.favourite:
            self.favorite_string = "\n" + "<em>* favorited!</em>"
        else:
            self.favorite_string = ""
            

    def disable_other_buttons(self):
        self.switch_starteller.disable()
        self.switch_med_cat.disable()
        self.switch_mediator.disable()
        self.switch_guide.disable()
        self.switch_queen.disable()
        self.switch_starteller_app.disable()
        self.switch_med_app.disable()
        self.switch_mediator_app.disable()
        print("disable other buttons activated")

    def decide_disable_for_update(self):
        self.the_cat = Cat.fetch_cat(game.switches['cat'])
        if self.the_cat.status == "warrior":
            pass
        elif self.the_cat.status == "starteller":
            self.switch_starteller.disable()
        elif self.the_cat.status == "medicine cat":
            self.switch_med_cat.disable()
        elif self.the_cat.status == "mediator":
            self.switch_mediator.disable()
        elif self.the_cat.status == "guide":
            self.switch_guide.disable()
        elif self.the_cat.status == "queen":
            self.switch_queen.disable()
        elif self.the_cat.status == "starteller apprentice":
            self.switch_starteller_app.disable()
        elif self.the_cat.status == "medicine cat apprentice":
            self.switch_med_app.disable()
        elif self.the_cat.status == "mediator apprentice":
            self.switch_mediator_app.disable()
        elif self.the_cat.status == "defense apprentice":
            self.switch_defense_app.disable()
        elif self.the_cat.status == "attack apprentice":
            self.switch_attack_app.disable()
        elif self.the_cat.status == "hunt apprentice":
            self.switch_hunt_app.disable()


    def update_warrior_buttons(self):
        if self.warrior_options_visible: # hide the dropdown when its already shown
            self.warrior_options_visible = False
            self.switch_defense.hide()
            self.switch_attack.hide()
            self.switch_hunt.hide()
            self.switch_starteller.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_guide.enable()
            self.switch_queen.enable()
            self.decide_disable_for_update()
            
            print("hide dropdown activated")
        else: # show the dropdown when its already hidden
            self.warrior_options_visible = True 
            self.switch_defense.show()
            self.switch_attack.show()
            self.switch_hunt.show()
            self.switch_starteller.disable()
            self.switch_med_cat.disable()
            self.switch_mediator.disable()
            self.switch_guide.disable()
            self.switch_queen.disable()

            print("show dropdown activated")

    def update_apprentice_buttons(self):
        if self.apprentice_options_visible: # hide the dropdown when its already shown
            self.apprentice_options_visible = False
            self.switch_defense_app.hide()
            self.switch_attack_app.hide()
            self.switch_hunt_app.hide()
            self.switch_starteller_app.enable()
            self.switch_med_app.enable()
            self.switch_mediator_app.enable()
            self.decide_disable_for_update()

            print("hide dropdown activated")
        else: # show the dropdown when its already hidden
            self.apprentice_options_visible = True 
            self.switch_defense_app.show()
            self.switch_attack_app.show()
            self.switch_hunt_app.show()
            self.switch_starteller_app.disable()
            self.switch_med_app.disable()
            self.switch_mediator_app.disable()

            print("show dropdown activated")
    def update_selected_cat(self):
        for ele in self.selected_cat_elements:
            self.selected_cat_elements[ele].kill()
        self.selected_cat_elements = {}

        self.the_cat = Cat.fetch_cat(game.switches['cat'])
        if not self.the_cat:
            return

        self.selected_cat_elements["cat_image"] = pygame_gui.elements.UIImage(
            scale(pygame.Rect((180, 290), (480, 480))),
            pygame.transform.scale(
                self.the_cat.sprite, (200, 200)),
            manager=MANAGER
        )

        name = str(self.the_cat.name)
        short_name = shorten_text_to_fit(name, 390, 40)
        self.selected_cat_elements["cat_name"] = pygame_gui.elements.UITextBox(short_name,
                                                                          scale(pygame.Rect((50, 120), (-1, 80))),
                                                                          object_id=get_text_box_theme(
                                                                              "#text_box_40_horizcenter"), manager=MANAGER)
        name_text_size = self.selected_cat_elements["cat_name"].get_relative_rect()
        self.selected_cat_elements["cat_name"].kill()

        self.selected_cat_elements["cat_name"] = pygame_gui.elements.UITextBox(short_name,
                                                                      scale(pygame.Rect(
                                                                        (440 - name_text_size.width, 230),
                                                                        (name_text_size.width * 2, 80))),
                                                                       object_id=get_text_box_theme(
                                                                        "#text_box_40_horizcenter"), manager=MANAGER)
        if game.settings['fullscreen']:
            x_pos = 390 - name_text_size.width//2
        else:
            x_pos = 395 - name_text_size.width
        self.selected_cat_elements["favourite_button"] = UIImageButton(scale(pygame.Rect
                                                                ((x_pos, 240), (56, 56))),
                                                              "",
                                                              object_id="#fav_cat",
                                                              manager=MANAGER,
                                                              tool_tip_text='Remove favorite status',
                                                              starting_height=2)

        self.selected_cat_elements["not_favourite_button"] = UIImageButton(scale(pygame.Rect
                                                                    ((x_pos, 240),
                                                                        (56, 56))),
                                                                 "",
                                                                 object_id="#not_fav_cat",
                                                                 manager=MANAGER,
                                                                 tool_tip_text='Mark as favorite',
                                                                 starting_height=2)  
        if self.the_cat.favourite:
            self.selected_cat_elements["favourite_button"].show()
            self.selected_cat_elements["not_favourite_button"].hide()
        else:
            self.selected_cat_elements["favourite_button"].hide()
            self.selected_cat_elements["not_favourite_button"].show()
        self.update_warrior_abrv()
        text = f"{self.the_cat.moons} "

        if self.the_cat.moons == 1:
            text += "moon"
        else:
            text += "moons"

        text += "\n" + self.the_cat.genderalign + "\n"

        text += self.the_cat.personality.trait + "\n"

        text += self.the_cat.skills.skill_string() + "\n"

        if self.the_cat.status == "attack":
            text += f"currently: <b>runner</b>"
        elif self.the_cat.status == "attack apprentice":
            text += f"currently: <b>runner's apprentice</b>"
        elif self.the_cat.status == "defense":
            text += f"currently: <b>guard</b>"
        elif self.the_cat.status == "defense apprentice":
            text += f"currently: <b>guard's apprentice</b>"
        elif self.the_cat.status == "hunt apprentice":
            text += f"currently: <b>hunter's apprentice</b>"
        elif self.the_cat.status == "hunt":
            text+= f"currently: <b>hunter</b>"
        else:
            text += f"currently: <b>{self.the_cat.status}</b>"
        text += "\n"
        if self.the_cat.mentor:
            text += "mentor: "
            mentor = Cat.fetch_cat(self.the_cat.mentor)
            if mentor:
                text += str(mentor.name)

        if self.the_cat.apprentice:
            if len(self.the_cat.apprentice) > 1:
                text += "apprentices: "
            else:
                text += "apprentice: "

            text += ", ".join([str(Cat.fetch_cat(x).name) for x in
                               self.the_cat.apprentice if Cat.fetch_cat(x)])
        self.update_favorite_text()
        text += self.favorite_string

        self.selected_cat_elements["cat_details"] = UITextBoxTweaked(text, scale(pygame.Rect((150, 800), (500, -1))),
                                                                     object_id="#text_box_34_horizleft",
                                                                     manager=MANAGER)

        self.selected_cat_elements["role_blurb"] = pygame_gui.elements.UITextBox(self.get_role_blurb(),
                                                                                 scale(pygame.Rect((800, 940),
                                                                                                   (600, 350))),
                                                                                 object_id="#text_box_27_horizcenter_vertcenter_spacing95",
                                                                                 manager=MANAGER)
        main_dir = "resources/images/"
        paths = {
            "leader": "leader_icon.png",
            "deputy": "deputy_icon.png",
            "starteller": "starteller_icon.png",
            "starteller apprentice": "starteller_app_icon.png",
            "medicine cat": "medic_icon.png",
            "medicine cat apprentice": "medic_app_icon.png",
            "mediator": "mediator_icon.png",
            "mediator apprentice": "mediator_app_icon.png",
            "warrior": "warrior_icon.png",
            "defense": "defense_icon.png",
            "defense apprentice": "defense_icon.png",
            "attack": "attack_icon.png",
            "attack apprentice": "attack_icon.png",
            "hunt": "hunt_icon.png",
            "hunt apprentice": "hunt_icon.png",
            "apprentice": "warrior_app_icon.png",
            "queen": "queen_icon.png",
            "guide": "guide_icon.png",
            "kitten": "kit_icon.png",
            "newborn": "kit_icon.png",
            "elder": "elder_icon.png",
        }

        if self.the_cat.status in paths:
            icon_path = os.path.join(main_dir, paths[self.the_cat.status])
        else:
            icon_path = os.path.join(main_dir, "buttonrank.png")

        self.selected_cat_elements["role_icon"] = pygame_gui.elements.UIImage(
            scale(pygame.Rect((520, 790), (156, 156))),
            pygame.transform.scale(
                image_cache.load_image(icon_path),
                (156 / 1600 * screen_x, 156 / 1400 * screen_y)
            ))

        self.determine_previous_and_next_cat()
        self.update_disabled_buttons()

    def update_disabled_buttons(self):
        # Previous and next cat button
        if self.next_cat == 0:
            self.next_cat_button.disable()
        else:
            self.next_cat_button.enable()

        if self.previous_cat == 0:
            self.previous_cat_button.disable()
        else:
            self.previous_cat_button.enable()

        if game.clan.leader:
            leader_invalid = game.clan.leader.dead or game.clan.leader.outside
        else:
            leader_invalid = True

        if game.clan.deputy:
            deputy_invalid = game.clan.deputy.dead or game.clan.deputy.outside
        else:
            deputy_invalid = True

        if self.the_cat.status == "apprentice":
            # LEADERSHIP
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()

            # In-TRAINING ROLES:
            self.switch_med_app.enable()
            self.switch_warrior_app.enable()
            self.switch_defense_app.enable()
            self.switch_attack_app.enable()
            self.switch_hunt_app.enable()
            self.switch_mediator_app.enable()
            self.switch_starteller_app.enable()
        elif self.the_cat.status == "warrior":
            # LEADERSHIP
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            # ADULT CAT ROLES
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()
        elif self.the_cat.status == "defense":
            # LEADERSHIP
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            # ADULT CAT ROLES
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.disable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()
        elif self.the_cat.status == "defense apprentice":
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()

            # In-TRAINING ROLES:
            self.switch_med_app.enable()
            self.switch_warrior_app.enable()
            self.switch_defense_app.disable()
            self.switch_attack_app.enable()
            self.switch_hunt_app.enable()
            self.switch_mediator_app.enable()
            self.switch_starteller_app.enable()
        elif self.the_cat.status == "attack":
            # LEADERSHIP
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            # ADULT CAT ROLES
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.disable()
            self.switch_hunt.enable()
            self.retire.enable()
        elif self.the_cat.status == "attack apprentice":
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()

            # In-TRAINING ROLES:
            self.switch_med_app.enable()
            self.switch_warrior_app.enable()
            self.switch_defense_app.enable()
            self.switch_attack_app.disable()
            self.switch_hunt_app.enable()
            self.switch_mediator_app.enable()
            self.switch_starteller_app.enable()
        elif self.the_cat.status == "hunt":
            # LEADERSHIP
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            # ADULT CAT ROLES
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.disable()
            self.retire.enable()
        elif self.the_cat.status == "hunt apprentice":
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()

            # In-TRAINING ROLES:
            self.switch_med_app.enable()
            self.switch_warrior_app.enable()
            self.switch_defense_app.enable()
            self.switch_attack_app.enable()
            self.switch_hunt_app.disable()
            self.switch_mediator_app.enable()
            self.switch_starteller_app.enable()
        elif self.the_cat.status == "deputy":
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            self.promote_deputy.disable()
            self.update_available_roles()
            # ADULT CAT ROLES
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()
        elif self.the_cat.status == "starteller":
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_starteller.disable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()

        elif self.the_cat.status == "medicine cat":
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            self.switch_warrior.enable()
            self.switch_med_cat.disable()
            self.switch_mediator.enable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()
        elif self.the_cat.status == "mediator":
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.disable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()
        elif self.the_cat.status == "queen":
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_queen.disable()
            self.switch_starteller.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()

        elif self.the_cat.status == "guide":
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()
            self.update_available_roles()
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_queen.enable()
            self.switch_starteller.enable()
            self.switch_guide.disable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()

        elif self.the_cat.status == "elder":
            if leader_invalid:
                self.promote_leader.enable()
            else:
                self.promote_leader.disable()

            if deputy_invalid:
                self.promote_deputy.enable()
            else:
                self.promote_deputy.disable()

            # ADULT CAT ROLES
            self.switch_warrior. enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.disable()

            # In-TRAINING ROLES:
            self.switch_med_app.disable()
            self.switch_warrior_app.disable()
            self.switch_defense_app.disable()
            self.switch_mediator_app.disable()
            self.switch_starteller_app.disable()
        elif self.the_cat.status == "starteller apprentice":
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()
            # In-TRAINING ROLES:
            self.switch_med_app.enable()
            self.switch_warrior_app.enable()
            self.switch_defense_app.enable()
            self.switch_attack_app.enable()
            self.switch_hunt_app.enable()
            self.switch_mediator_app.enable()
            self.switch_starteller_app.disable()

        elif self.the_cat.status == "medicine cat apprentice":
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()
            # In-TRAINING ROLES:
            self.switch_med_app.disable()
            self.switch_warrior_app.enable()
            self.switch_defense_app.enable()
            self.switch_attack_app.enable()
            self.switch_hunt_app.enable()
            self.switch_mediator_app.enable()
            self.switch_starteller_app.enable()
        elif self.the_cat.status == "mediator apprentice":
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()
            # In-TRAINING ROLES:
            self.switch_med_app.enable()
            self.switch_warrior_app.enable()
            self.switch_defense_app.enable()
            self.switch_attack_app.enable()
            self.switch_hunt_app.enable()
            self.switch_mediator_app.disable()
            self.switch_starteller_app.enable()
            
        elif self.the_cat.status == "leader":
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()
            # ADULT CAT ROLES
            self.switch_warrior.enable()
            self.switch_med_cat.enable()
            self.switch_mediator.enable()
            self.switch_starteller.enable()
            self.switch_queen.enable()
            self.switch_guide.enable()
            self.switch_defense.enable()
            self.switch_attack.enable()
            self.switch_hunt.enable()
            self.retire.enable()
        else:
            self.promote_leader.disable()
            self.promote_deputy.disable()
            self.update_available_roles()
            # ADULT CAT ROLES
            self.switch_warrior.disable()
            self.switch_med_cat.disable()
            self.switch_mediator.disable()
            self.switch_starteller.disable()
            self.switch_queen.disable()
            self.switch_guide.disable()
            self.switch_defense.disable()
            self.switch_attack.disable()
            self.switch_hunt.disable()
            self.retire.disable()

            # In-TRAINING ROLES:
            self.switch_med_app.disable()
            self.switch_warrior_app.disable()
            self.switch_defense_app.disable()
            self.switch_attack_app.disable()
            self.switch_hunt_app.disable()
            self.switch_mediator_app.disable()
            self.switch_starteller_app.disable()
            print("else clause activated in update_disabled_buttons")
        
    def update_available_roles(self):
        self.the_cat = Cat.fetch_cat(game.switches['cat'])
        if self.the_cat.status in ['apprentice','medicine cat apprentice', 'mediator apprentice', 'starteller apprentice', 'defense apprentice', 'attack apprentice', 'hunt apprentice']:
            self.switch_warrior.hide()
            self.switch_med_cat.hide()
            self.switch_mediator.hide()
            self.switch_starteller.hide()
            self.switch_queen.hide()
            self.switch_guide.hide()
            self.switch_defense.hide()
            self.switch_attack.hide()
            self.switch_hunt.hide()
            self.retire.hide()
            self.switch_med_app.show()
            self.switch_warrior_app.show()
            self.switch_mediator_app.show()
            self.switch_starteller_app.show()
            self.switch_defense_app.show()
            self.switch_attack_app.show()
            self.switch_hunt_app.show()
        elif self.the_cat.status in ['warrior','defense','attack','hunt','starteller','guide','queen','mediator','medicine cat', 'elder', 'leader', 'deputy']:
            self.switch_warrior.show()
            self.switch_med_cat.show()
            self.switch_mediator.show()
            self.switch_starteller.show()
            self.switch_queen.show()
            self.switch_guide.show()
            self.switch_defense.show()
            self.switch_attack.show()
            self.switch_hunt.show()
            self.retire.show()
            self.switch_med_app.hide()
            self.switch_warrior_app.hide()
            self.switch_mediator_app.hide()
            self.switch_starteller_app.hide()
            self.switch_defense_app.hide()
            self.switch_attack_app.hide()
            self.switch_hunt_app.hide()
        else:
            self.switch_warrior.hide()
            self.switch_med_cat.hide()
            self.switch_mediator.hide()
            self.switch_starteller.hide()
            self.switch_queen.hide()
            self.switch_guide.hide()
            self.switch_defense.hide()
            self.switch_attack.hide()
            self.switch_hunt.hide()
            self.switch_med_app.hide()
            self.switch_warrior_app.hide()
            self.switch_mediator_app.hide()
            self.switch_starteller_app.hide()
            self.switch_defense_app.hide()
            self.switch_attack_app.hide()
            self.switch_hunt_app.hide()
            self.retire.hide()
            self.role_text_buttons[
                "main_scroll_container"].hide()
            self.invalid_disclaimer.show()

    
    def get_role_blurb(self):
        if self.the_cat.status == "warrior":
            output = f"{self.the_cat.name} is a <b>warrior</b>. Warriors are adult cats who feed and protect their " \
                     f"Clan. They are trained to hunt and fight in addition to the ways of the warrior code. " \
                     f"Warriors are essential to the survival of a Clan, and usually make up the bulk of it's members. "
        elif self.the_cat.status == "defense":
            output = f"{self.the_cat.name} is a <b>defense-class warrior.</b>. Defense-class warriors, or guards, are adult cats who " \
                     f"protect the Clan. They accompany patrols to guard from threats, and often stay at camp " \
                     f"to protect the nursery, elders, or just the general camp. Either way, they aim to protect the Clan, even " \
                     f"above their own safety."
        elif self.the_cat.status == "attack":
            output = f"{self.the_cat.name} is an <b>attack-class warrior</b>. Attack-class warriors, or runners, are adult cats who " \
                     f"will fight for their Clan. They usually go on border patrols, will seize territory if need be,  " \
                     f"and be the front-line for any attack. They specialize in their fighting more than anything else. "
        elif self.the_cat.status == "hunt":
            output = f"{self.the_cat.name} is a <b>HUNT WARRIOR</b>. Warriors are adult cats who feed and protect their " \
                     f"Clan. They are trained to hunt and fight in addition to the ways of the warrior code. " \
                     f"Warriors are essential to the survival of a Clan, and usually make up the bulk of it's members. "
        elif self.the_cat.status == "leader":
            output = f"{self.the_cat.name} is the <b>leader</b> of {game.clan.name}Clan. The guardianship of all " \
                     f"Clan cats has been entrusted to them by StarClan. The leader is the highest " \
                     f"authority in the Clan. The leader holds Clan meetings, determines mentors for " \
                     f"new apprentices, and names new warriors. To help them protect the Clan, " \
                     f"StarClan has given them nine lives. They typically take the suffix \"star\"."
        elif self.the_cat.status == "deputy":
            output = f"{self.the_cat.name} is {game.clan.name}Clan's <b>deputy</b>. " \
                     f"The deputy is the second in command, " \
                     f"just below the leader. They advise the leader and organize daily patrols, " \
                     f"alongside normal warrior duties. Typically, a deputy is personally appointed by the current " \
                     f"leader. As dictated by the Warrior Code, all deputies must train at least one apprentice " \
                     f"before appointment.  " \
                     f"The deputy succeeds the leader if they die or retire. "
        elif self.the_cat.status == "starteller":
            output = f"{self.the_cat.name} is a <b>Starteller</b>. They are the prophets of the Clan. " \
                 	f"They always come in pairs, one older and one younger. " \
                 	f"They help eachother decode their prophecies, " \
                    f"and the oldest gives the youngest their wisdom, while the youngest gives " \
                    f"the oldest their perspective. " \
                    f"<b>Startellers</b> are often mysterious to the clan, and are odd in this way."
        elif self.the_cat.status == "medicine cat":
            output = f"{self.the_cat.name} is a <b>medicine cat</b>. Medicine cats are the healers of the Clan. " \
                     f"They treat " \
                     f"injuries and illnesses with herbal remedies. Unlike warriors, medicine cats are not expected " \
                     f"to hunt and fight for the Clan. In addition to their healing duties, medicine cats also have " \
                     f"a special connection to StarClan. Every half-moon, they travel to their Clan's holy place " \
                     f"to commune with StarClan. "
        elif self.the_cat.status == "mediator":
            output = f"{self.the_cat.name} is a <b>mediator</b>. Mediators are not typically required " \
                     f"to hunt or fight for " \
                     f"the Clan. Rather, mediators are charged with handling disagreements between " \
                     f"Clanmates and disputes between Clans. Some mediators train as apprentices to serve their Clan, " \
                     f"while others may choose to become mediators later in life. "
        elif self.the_cat.status == "guide":
            output = f"{self.the_cat.name} is a <b>guide</b>. Guides know the territory of both their Clan and others in and out, " \
                 	f"and can help patrols avoid dangerous areas or find particularly good hunting grounds. " \
                 	f"In general, they are key to the entire Clan being able to feel safe in their own territory. " \
		            f"Guides have full permission to be anywhere, even other Clan's territories." 
        elif self.the_cat.status == "elder":
            output = f"{self.the_cat.name} is an <b>elder</b>. They have spent many moons serving their Clan, " \
                     f"and have earned " \
                     f"many moons of rest. Elders are essential to passing down the oral tradition of the Clan. " \
                     f"Sometimes, cats may retire due to disability or injury. Whatever the " \
                     f"circumstance of their retirement, elders are held in high esteem in the Clan, and always eat " \
                     f"before Warriors and Medicine Cats. "
        elif self.the_cat.status == "apprentice":
            output = f"{self.the_cat.name} is an <b>apprentice</b>, in training to become a warrior. " \
                     f"Kits can be made warrior apprentices at six moons of age, where they will learn how " \
                     f"to hunt and fight for their Clan. Typically, the training of an apprentice is entrusted " \
                     f"to an single warrior - their mentor. To build character, apprentices are often assigned " \
                     f"the unpleasant and grunt tasks of Clan life. Apprentices take the suffix \"paw\", " \
                     f"to represent the path their paws take towards adulthood. "
        elif self.the_cat.status == "defense apprentice":
            output = f"{self.the_cat.name} is an <b>DEFENSE apprentice</b>, in training to become a warrior. " \
                     f"Kits can be made warrior apprentices at six moons of age, where they will learn how " \
                     f"to hunt and fight for their Clan. Typically, the training of an apprentice is entrusted " \
                     f"to an single warrior - their mentor. To build character, apprentices are often assigned " \
                     f"the unpleasant and grunt tasks of Clan life. Apprentices take the suffix \"paw\", " \
                     f"to represent the path their paws take towards adulthood. "
        elif self.the_cat.status == "attack apprentice":
            output = f"{self.the_cat.name} is an <b>ATTACK apprentice</b>, in training to become a warrior. " \
                     f"Kits can be made warrior apprentices at six moons of age, where they will learn how " \
                     f"to hunt and fight for their Clan. Typically, the training of an apprentice is entrusted " \
                     f"to an single warrior - their mentor. To build character, apprentices are often assigned " \
                     f"the unpleasant and grunt tasks of Clan life. Apprentices take the suffix \"paw\", " \
                     f"to represent the path their paws take towards adulthood. "
        elif self.the_cat.status == "hunt apprentice":
            output = f"{self.the_cat.name} is an <b>HUNT apprentice</b>, in training to become a warrior. " \
                     f"Kits can be made warrior apprentices at six moons of age, where they will learn how " \
                     f"to hunt and fight for their Clan. Typically, the training of an apprentice is entrusted " \
                     f"to an single warrior - their mentor. To build character, apprentices are often assigned " \
                     f"the unpleasant and grunt tasks of Clan life. Apprentices take the suffix \"paw\", " \
                     f"to represent the path their paws take towards adulthood. "
        elif self.the_cat.status == "starteller apprentice":
            output = f"{self.the_cat.name} is a <b>Starteller apprentice</b>. Startellers are the prophets of the Clan. " \
                 	f"{self.the_cat.name} is the younger of two <b>Startellers</b>, and help the older " \
                 	f"decode prophecies, giving insight that the older <b>Starteller</b> " \
                    f"may not have."
        elif self.the_cat.status == "medicine cat apprentice":
            output = f"{self.the_cat.name} is a <b>medicine cat apprentice</b>, training to become a full medicine cat. " \
                     f"Kits can be made medicine cat apprentices at six moons of age, where they will learn how to " \
                     f"heal their Clanmates and commune with StarClan. Medicine cat apprentices are typically chosen " \
                     f"for their interest in healing and/or their connecting to StarClan. Apprentices take the suffix " \
                     f"-paw, to represent the path their paws take towards adulthood."
        elif self.the_cat.status == "mediator apprentice":
            output = f"{self.the_cat.name} is a <b>mediator apprentice</b>, training to become a full mediator. " \
                     f"Mediators are in charge of handling disagreements both within the Clan and between Clans. " \
                     f"Mediator apprentices are often chosen for their quick thinking and steady personality. " \
                     f"Apprentices take the suffix \"paw\", " \
                     f"to represent the path their paws take towards adulthood. "
        elif self.the_cat.status == "queen":
            output = f"{self.the_cat.name} is a <b>queen</b>. These cats stay in the nursery and take care of " \
                 	f"kits and otherwise nursery-bound cats. " \
                 	f"They may do this after having kits of their own and deciding to stay in the nursery, " \
                    f"or they may choose to do it simply because they love taking care of the younger cats in their Clan."

        elif self.the_cat.status == "kitten":
            output = f"{self.the_cat.name} is a <b>kitten</b>. All cats below the age of six moons are " \
                     f"considered kits. Kits " \
                     f"are prohibited from leaving camp in order to protect them from the dangers of the wild. " \
                     f"Although they don't have any official duties in the Clan, they are expected to learn the " \
                     f"legends and traditions of their Clan. They are protected by every cat in the Clan and always " \
                     f"eat first. Kit take the suffix \"kit\"."
        elif self.the_cat.status == "newborn":
            output = f"{self.the_cat.name} is a <b>newborn kitten</b>. All cats below the age of six moons are " \
                     f"considered kits. Kits " \
                     f"are prohibited from leaving camp in order to protect them from the dangers of the wild. " \
                     f"Although they don't have any official duties in the Clan, they are expected to learn the " \
                     f"legends and traditions of their Clan. They are protected by every cat in the Clan and always " \
                     f"eat first. Kit take the suffix \"kit\"."
        else:
            output = f"{self.the_cat.name} has an unknown rank. I guess they want to make their own way in life! "

        return output

    def determine_previous_and_next_cat(self):
        """'Determines where the next and previous buttons point too."""

        is_instructor = False
        if self.the_cat.dead and game.clan.instructor.ID == self.the_cat.ID:
            is_instructor = True

        previous_cat = 0
        next_cat = 0
        if self.the_cat.dead and not is_instructor and self.the_cat.df == game.clan.instructor.df and \
                not (self.the_cat.outside or self.the_cat.exiled):
            previous_cat = game.clan.instructor.ID

        if is_instructor:
            next_cat = 1

        for check_cat in Cat.all_cats_list:
            if check_cat.ID == self.the_cat.ID:
                next_cat = 1
            else:
                if next_cat == 0 and check_cat.ID != self.the_cat.ID and check_cat.dead == self.the_cat.dead \
                        and check_cat.ID != game.clan.instructor.ID and check_cat.outside == self.the_cat.outside and \
                        check_cat.df == self.the_cat.df and not check_cat.faded:
                    previous_cat = check_cat.ID

                elif next_cat == 1 and check_cat != self.the_cat.ID and check_cat.dead == self.the_cat.dead \
                        and check_cat.ID != game.clan.instructor.ID and check_cat.outside == self.the_cat.outside and \
                        check_cat.df == self.the_cat.df and not check_cat.faded:
                    next_cat = check_cat.ID

                elif int(next_cat) > 1:
                    break

        if next_cat == 1:
            next_cat = 0

        self.next_cat = next_cat
        self.previous_cat = previous_cat
        

    def exit_screen(self):
        self.role_text_buttons[
            "main_scroll_container"].kill()
        del self.role_text_buttons[
            "main_scroll_container"]
        self.back_button.kill()
        del self.back_button
        self.next_cat_button.kill()
        del self.next_cat_button
        self.previous_cat_button.kill()
        del self.previous_cat_button
        self.promote_leader.kill()
        del self.promote_leader
        self.promote_deputy.kill()
        del self.promote_deputy
        self.switch_starteller.kill()
        del self.switch_starteller
        self.switch_warrior.kill()
        del self.switch_warrior
        self.switch_med_cat.kill()
        del self.switch_med_cat
        self.switch_mediator.kill()
        del self.switch_mediator
        self.retire.kill()
        del self.retire
        self.switch_starteller_app.kill()
        del self.switch_starteller_app
        self.switch_med_app.kill()
        del self.switch_med_app
        self.switch_warrior_app.kill()
        del self.switch_warrior_app
        self.switch_defense_app.kill()
        del self.switch_defense_app
        self.switch_attack_app.kill()
        del self.switch_attack_app
        self.switch_hunt_app.kill()
        del self.switch_hunt_app
        self.switch_mediator_app.kill()
        del self.switch_mediator_app
        self.switch_queen.kill()
        del self.switch_queen
        self.switch_guide.kill()
        del self.switch_guide
        self.cat_details_box.kill()
        del self.cat_details_box
        self.roles_box.kill()
        del self.roles_box
        self.role_blurb_box.kill()
        del self.role_blurb_box
        self.role_section_labels.kill()
        del self.role_section_labels
        self.switch_defense.kill()
        del self.switch_defense
        self.switch_attack.kill()
        del self.switch_attack
        self.invalid_disclaimer.kill()
        del self.invalid_disclaimer
        self.switch_hunt.kill()
        del self.switch_hunt
        for ele in self.selected_cat_elements:
            self.selected_cat_elements[ele].kill()
        self.selected_cat_elements = {}
