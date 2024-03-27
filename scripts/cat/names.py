import random
import os
import ujson

from scripts.housekeeping.datadir import get_save_dir

from scripts.game_structure.game_essentials import game

class Name():
    if os.path.exists('resources/dicts/names/names.json'):
        with open('resources/dicts/names/names.json') as read_file:
            names_dict = ujson.loads(read_file.read())

        if os.path.exists(get_save_dir() + '/prefixlist.txt'):
            with open(get_save_dir() + '/prefixlist.txt', 'r') as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split('\n')
                for new_name in new_names:
                    if new_name != '':
                        if new_name.startswith('-'):
                            while new_name[1:] in names_dict["normal_prefixes"]:
                                names_dict["normal_prefixes"].remove(new_name[1:])
                        else:
                            names_dict["normal_prefixes"].append(new_name)

        if os.path.exists(get_save_dir() + '/suffixlist.txt'):
            with open(get_save_dir() + '/suffixlist.txt', 'r') as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split('\n')
                for new_name in new_names:
                    if new_name != '':
                        if new_name.startswith('-'):
                            while new_name[1:] in names_dict["normal_suffixes"]:
                                names_dict["normal_suffixes"].remove(new_name[1:])
                        else:
                            names_dict["normal_suffixes"].append(new_name)

        if os.path.exists(get_save_dir() + '/specialsuffixes.txt'):
            with open(get_save_dir() + '/specialsuffixes.txt', 'r') as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split('\n')
                for new_name in new_names:
                    if new_name != '':
                        if new_name.startswith('-'):
                            del names_dict["special_suffixes"][new_name[1:]]
                        elif ':' in new_name:
                            _tmp = new_name.split(':')
                            names_dict["special_suffixes"][_tmp[0]] = _tmp[1]
                            
    if os.path.exists('resources/dicts/names/skill_reference.json'):
        with open('resources/dicts/names/skill_reference.json') as read_file_:
            skill_name_ref = ujson.loads(read_file_.read())
            
    def __init__(self,
                 status="warrior",
                 prefix=None,
                 suffix=None,
                 colour=None,
                 eyes=None,
                 pelt=None,
                 tortiepattern=None, # this is actually tortie_pelt in jsons
                 biome=None,
                 trait=None,
                 primary=None, # skill 1
                 secondary=None, # skill 2
                 specsuffix_hidden=False,
                 load_existing_name=False):
        self.status = status
        self.prefix = prefix
        self.suffix = suffix
        self.specsuffix_hidden = specsuffix_hidden

        name_fixpref = False
        # Set prefix
        if prefix is None:
            self.give_prefix(eyes, colour, pelt, tortiepattern, trait, primary, secondary)
            # needed for random dice when we're changing the Prefix
            name_fixpref = True

        # Set suffix
        if self.suffix is None:
            self.give_suffix(eyes, colour, pelt, tortiepattern, trait, primary, secondary)
            if name_fixpref and self.prefix is None:
                # needed for random dice when we're changing the Prefix
                name_fixpref = False

        if self.suffix and not load_existing_name:
            # Prevent triple letter names from joining prefix and suffix from occuring (ex. Beeeye)
            triple_letter = False
            possible_three_letter = (self.prefix[-2:] + self.suffix[0], self.prefix[-1] + self.suffix[:2])
            if all(i == possible_three_letter[0][0] for i in possible_three_letter[0]) or \
                    all(i == possible_three_letter[1][0] for i in possible_three_letter[1]):
                triple_letter = True
            # Prevent double animal names (ex. Spiderfalcon)
            double_animal = False
            if self.prefix in self.names_dict["animal_prefixes"] and self.suffix in self.names_dict["animal_suffixes"]:
                double_animal = True
            # Prevent the inappropriate names
            nono_name = self.prefix + self.suffix
            # Prevent double names (ex. Iceice)
            # Prevent suffixes containing the prefix (ex. Butterflyfly)
            
            i = 0
            while nono_name.lower() in self.names_dict["inappropriate_names"] or triple_letter or double_animal or \
                    self.suffix.lower() == self.prefix.lower() or (self.suffix.lower() in self.prefix.lower() and not str(self.suffix) == ''):

                # check if random die was for prefix
                if name_fixpref:
                    self.give_prefix(eyes, colour, pelt, tortiepattern, trait,primary, secondary)
                else:
                    self.give_suffix(eyes, colour, pelt, tortiepattern, trait, primary, secondary)

                nono_name = self.prefix + self.suffix
                possible_three_letter = (self.prefix[-2:] + self.suffix[0], self.prefix[-1] + self.suffix[:2])
                if not (all(i == possible_three_letter[0][0] for i in possible_three_letter[0]) or \
                        all(i == possible_three_letter[1][0] for i in possible_three_letter[1])):
                    triple_letter = False
                if not (self.prefix in self.names_dict["animal_prefixes"] and self.suffix in self.names_dict[
                    "animal_suffixes"]):
                    double_animal = False
                i += 1

    # Generate possible prefix
    def give_prefix(self, eyes, colour, pelt, tortiepattern,trait,  primary, secondary):
        # decided in game config: cat_name_controls
        # the chance system may be rewritten
        if game.config["cat_name_controls"]["always_name_after_appearance"] or game.config["cat_name_controls"]["always_name_after_appearance"]:
            if game.config["cat_name_controls"]["always_name_after_appearance"]:
                named_after_appearance = True
            if game.config["cat_name_controls"]["always_name_after_traits"]:
                named_after_traits = True
        else:
            named_after_appearance = not random.getrandbits(2)  # Chance for True is '1/4'
            named_after_traits = not random.getrandbits(2)  # Chance for True is '1/4'
            named_after_biome = not random.getrandbits(3)  # Chance for True is '1/8'
            
        possible_prefix_categories = []
        if named_after_appearance:
            if game.config["cat_name_controls"]["allow_eye_names"]: # game config: cat_name_controls
                if eyes in self.names_dict["eye_prefixes"]:
                    possible_prefix_categories.append(self.names_dict["eye_prefixes"][eyes])
            if colour in self.names_dict["colour_prefixes"]:
                possible_prefix_categories.append(self.names_dict["colour_prefixes"][colour])
            if pelt in ["Tortie", "Calico"] and tortiepattern in self.names_dict["tortie_pelt_prefixes"]:
                possible_prefix_categories.append(self.names_dict["tortie_pelt_prefixes"][tortiepattern]) # this just checks the pelt color, not the pattern
            if pelt in self.names_dict["pelt_prefixes"]:
                possible_prefix_categories.append(self.names_dict["pelt_prefixes"][pelt])
            
            
        elif named_after_traits:
            if trait in self.names_dict["trait_prefixes"]:
                possible_prefix_categories.append(self.names_dict["trait_prefixes"][trait])
            if primary is not None: # there's gotta be a better way to do this....
                i_need_this_for_some_reason = None
                if primary.skill in self.skill_name_ref:
                    i_need_this_for_some_reason = self.skill_name_ref[primary.skill]
                    primary_path = ' '.join([str(elem) for i,elem in enumerate(i_need_this_for_some_reason)])
                if primary_path in self.names_dict["skill_prefixes"]:
                    possible_prefix_categories.append(self.names_dict["skill_prefixes"][primary_path])
            if secondary is not None:
                i_need_this_for_some_reason_ = None
                if secondary.skill in self.skill_name_ref:
                    i_need_this_for_some_reason_ = self.skill_name_ref[secondary.skill]
                    secondary_path = ' '.join([str(elem) for i,elem in enumerate(i_need_this_for_some_reason_)])
                if secondary_path in self.names_dict["skill_prefixes"]:
                    possible_prefix_categories.append(self.names_dict["skill_prefixes"][secondary_path])
        
        """if game.config["cat_name_controls"]["restrict_biome_names"]:
           all_biome_prefixes = []
           for m in range(len(self.names_dict["biome_prefixes"])):
               for n in range(len(self.names_dict["biome_prefixes"][m])):
                  all_biome_prefixes.append(self.names_dict["biome_prefixes"][m][n])
           
           bad_biome_prefixes = [i for i in all_biome_prefixes if i not in self.names_dict["biome_prefixes"][biome]]
        
            if self.prefix in bad_biome_prefixes:
                self.give_prefix(eyes, colour, pelt, biome, tortiepattern, pattern, trait) # I have a feeling this will result in an endless loop in some cases... see if there's a better way
            """
                        
        if possible_prefix_categories:
            prefix_category = random.choice(possible_prefix_categories)
            self.prefix = random.choice(prefix_category)
        else:
            self.prefix = random.choice(self.names_dict["normal_prefixes"])

    # Generate possible suffix
    def give_suffix(self, eyes, colour, pelt, tortiepattern, trait, primary, secondary):
    
        if game.config["cat_name_controls"]["always_name_after_appearance"] or game.config["cat_name_controls"]["always_name_after_appearance"]:
            if game.config["cat_name_controls"]["always_name_after_appearance"]:
                named_after_appearance_ = True
            if game.config["cat_name_controls"]["always_name_after_traits"]:
                named_after_traits_ = True
        else:
            named_after_appearance_ = not random.getrandbits(2)  # Chance for True is '1/4'
            named_after_traits_ = not random.getrandbits(2)  # Chance for True is '1/4'
            named_after_biome_ = not random.getrandbits(3)  # Chance for True is '1/8'
            
        # i had to rewrite this whole thing bc it made no sense
        possible_suffix_categories = []
        if named_after_appearance_:
            if game.config["cat_name_controls"]["allow_eye_names"]: # game config: cat_name_controls
                if eyes in self.names_dict["eye_suffixes"]:
                    possible_suffix_categories.append(self.names_dict["eye_suffixes"][eyes])
            if colour in self.names_dict["colour_suffixes"]:
                possible_suffix_categories.append(self.names_dict["colour_suffixes"][colour])
            if pelt in self.names_dict["pelt_suffixes"]:
                possible_suffix_categories.append(self.names_dict["pelt_suffixes"][pelt])
            if pelt in ["Tortie", "Calico"] and tortiepattern in self.names_dict["tortie_pelt_suffixes"]:
                possible_suffix_categories.append(self.names_dict["tortie_pelt_suffixes"][tortiepattern]) # this just checks the pelt color, not the pattern
            
        elif named_after_traits_:
            if trait in self.names_dict["trait_suffixes"]:
                possible_suffix_categories.append(self.names_dict["trait_suffixes"][trait])
            if primary is not None: # there's gotta be a better way to do this....
                i_need_this_for_some_reason = None
                if primary.skill in self.skill_name_ref:
                    i_need_this_for_some_reason__ = self.skill_name_ref[primary.skill]
                    primary_path = ' '.join([str(elem) for i,elem in enumerate(i_need_this_for_some_reason__)])
                    if primary_path in self.names_dict["skill_suffixes"]:
                        possible_suffix_categories.append(self.names_dict["skill_suffixes"][primary_path])
            if secondary is not None:
                i_need_this_for_some_reason_ = None
                if secondary.skill in self.skill_name_ref:
                    i_need_this_for_some_reason___ = self.skill_name_ref[secondary.skill]
                    secondary_path = ' '.join([str(elem) for i,elem in enumerate(i_need_this_for_some_reason___)])
                if secondary_path in self.names_dict["skill_suffixes"]:
                    possible_suffix_categories.append(self.names_dict["skill_suffixes"][secondary_path])
                    
        if possible_suffix_categories:
            suffix_category = random.choice(possible_suffix_categories)
            self.suffix = random.choice(suffix_category)
        else:
            self.suffix = random.choice(self.names_dict["normal_suffixes"])

    def __repr__(self):
        if self.status in self.names_dict["special_suffixes"] and not self.specsuffix_hidden:
            return self.prefix + self.names_dict["special_suffixes"][self.status]
        else:
            if game.config['fun']['april_fools']:
                return self.prefix + 'egg'
            return self.prefix + self.suffix


names = Name()
