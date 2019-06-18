import random

weaponDict = {
    "Lascannon":
    {
        "strength" : 9,
        "ap" : 3
    },
    "Bolterrifle":
    {
        "strength": 4,
        "ap" : 0
    },
    "Lasgun":
    {
        "strength" : 3,
        "ap" : 0
    },
    "Hellstrike":
    {
        "strength" : 8,
        "ap" : 2
    },
    "Melta":
    {
        "strength" : 8,
        "ap" : 4
    },
    "Vanquisher":
    {
        "strength" : 8,
        "ap" : 3
    },
    "Plasmacannon":
        {
        "strength" : 7,
        "ap" : 3
        },
    "Battlecannon":
    {
        "strength" : 8,
        "ap" : 2
    },
    "Banebladecannon":
    {
        "strength" : 8,
        "ap" : 3
    },
    "Heavybolter":
    {
        "strength": 5,
        "ap" : 1
    },
     "Autocannon":
    {
        "strength": 7,
        "ap" : 1
    },
    "Demolisher":
    {
        "strength": 10,
        "ap" : 3
    },
}

targetDict = {
    "Knight Castellan":
    {
        "toughness" : 8,
        "wounds" : 28,
        "save" :  3,
        "invulsave" : 5
    },

    "Baneblade":
    {
        "toughness" : 8,
        "wounds" : 24,
        "save" :  3,
        "invulsave" : 7 #7 means no invulsave
    },

    "Sentinel":
    {
        "toughness" : 6,
        "wounds" : 6,
        "save" : 3,
        "invulsave" : 7
    },

    "Plaguemarine":
    {
        "toughness" : 5,
        "wounds" : 1,
        "save" : 3,
        "invulsave" : 7
    },

    "Valkyrie":
    {
        "toughness" : 7,
        "wounds" : 14,
        "save" : 3,
        "invulsave" : 7
    },
    "Lemanruss":
    {
        "toughness" : 8,
        "wounds" : 12,
        "save" : 3,
        "invulsave" : 7
    },
    "Guardsman":
    {
        "toughness" : 3,
        "wounds" : 1,
        "save" : 5,
        "invulsave" : 7
    },
    "Primarisintercessor":
    {
        "toughness" : 4,
        "wounds" : 2,
        "save" : 3,
        "invulsave" : 7
    },
    "Spacemarine":
    {
        "toughness" : 4,
        "wounds" : 1,
        "save" : 3,
        "invulsave" : 7
    },
    "Nob":
    {
        "toughness" : 4,
        "wounds" : 4,
        "save" : 4,
        "invulsave" : 7
    },
    "Fireprism":
    {
        "toughness" : 7,
        "wounds" : 12,
        "save" : 3,
        "invulsave" : 7
    },
    "Carnifex":
    {
        "toughness" : 7,
        "wounds" : 8,
        "save" : 3,
        "invulsave" : 7
    },
    "Warlordbattletitan":
    {
        "toughness" : 15,
        "wounds" : 30,
        "save" : 2,
        "invulsave" : 3
    },
}

class weapon():
    def __init__(self, weaponKeyword, hiton=4):
        self.strength = weaponDict[weaponKeyword]["strength"]
        self.ap = weaponDict[weaponKeyword]["ap"] #must be a positive number!
        self.hiton = hiton
        self.attacks = -1
        self.profile = weaponKeyword

    def attack(self, target):
        hits = 0
        wounds = 0
        damage = 0
        #determine number of attacks
        if self.profile == "Battlecannon":
            self.attacks = random.randint(1,6)
        elif self.profile == "Banebladecannon":
            self.attacks = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
        elif self.profile == "Plasmacannon" or self.profile == "Demolisher":
            self.attacks = random.randint(1,3)
        elif self.profile == "Heavybolter":
            self.attacks = 3
        elif self.profile == "Autocannon":
            self.attacks = 2
        elif self.profile == "Vanquisher" or self.profile == "Melta" or self.profile == "Lascannon" or self.profile == "Hellstrike" or self.profile == "Lasgun" or self.profile == "Bolterrifle":
            self.attacks = 1
        else:
            print("error: Invalid weapon profile")

        for x in range(0, self.attacks): #hits
            if random.randint(1,6) >= self.hiton:
                hits += 1

        #resolve toughness/wounds
        if (target.toughness/2) > self.strength:
            woundon = 6
        elif (target.toughness) > self.strength:
            woundon = 5
        elif (target.toughness) == self.strength:
            woundon = 4
        elif (target.toughness) < self.strength:
            woundon = 3
        elif (target.toughness) < self.strength/2:
            woundon = 2
        else:
            woundon = 100
            print("error, invalid wounds")

        for x in range(0, hits):
            if random.randint(1, 6) >= woundon:
                wounds += 1

        #calculate save
        defender_save = target.save + self.ap #higher save means less chance of save
        if defender_save > target.invulsave:
            defender_save = target.invulsave

        #resolve damage
        for x in range(0, wounds):
            if (random.randint(1,6) > defender_save) == False: #save fails
                if self.profile == "Hellstrike" or self.profile == "Melta" or self.profile == "Vanquisher":
                    one = random.randint(1,6)
                    two = random.randint(1,6)
                    if two > one:
                        damage += two
                    else:
                        damage += one
                elif self.profile == "Battlecannon":
                    damage += random.randint(1,3)
                elif self.profile == "Lascannon" or self.profile == "Demolisher":
                    damage += random.randint(1,6)
                elif self.profile == "Banebladecannon":
                    damage += 3
                elif self.profile == "Autocannon" or self.profile == "Plasmacannon": #overcharge
                    damage += 2
                elif self.profile == "Lasgun" or self.profile == "Heavybolter" or self.profile == "Bolterrifle":
                    damage += 1
                else:
                    print("error, unlisted damage profile")

                if target.profile == "Plaguemarine": #disgustingly resiliant
                    for point in range(0, damage):
                        if random.randint(1,6) >= 5 and damage > 0:
                            damage -= 1
        return damage

class weapon_suite():
    def __init__(self, suiteprofile, hiton=4):
        self.suiteprofile = suiteprofile
        self.weapons_list = []
        self.hiton = hiton
        if self.suiteprofile == "Lemanruss":
            self.weapons_list.append(weapon("Battlecannon", self.hiton))
            self.weapons_list.append(weapon("Battlecannon", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))

        if self.suiteprofile == "Baneblade":
            self.weapons_list.append(weapon("Banebladecannon", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))
            self.weapons_list.append(weapon("Heavybolter", self.hiton))
            self.weapons_list.append(weapon("Autocannon", self.hiton))
            self.weapons_list.append(weapon("Demolisher", self.hiton))
            self.weapons_list.append(weapon("Lascannon", self.hiton))
            self.weapons_list.append(weapon("Lascannon", self.hiton))

    def create(self):
        return self.weapons_list

    def attack_suite(self, target):
        attack_dmg = 0
        for weapon in self.weapons_list:
            attack_dmg += weapon.attack(target)
        return attack_dmg

class Target():
    def __init__(self, targetKeyword):
            self.profile = targetKeyword
            self.toughness = targetDict[targetKeyword]["toughness"]
            self.wounds = targetDict[targetKeyword]["wounds"]
            self.save = targetDict[targetKeyword]["save"]
            self.invulsave = targetDict[targetKeyword]["invulsave"]

    def checkdead(self):
        if self.wounds <= 0:
            return True
        return False
