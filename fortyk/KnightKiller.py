import fortyk.WP  #weapon profile classes

class KnightKiller():
    def __init__(self, attacker, target, hiton): #attacker, target is a string
        #self.attacker = fortyk.WP.weapon_suite(attacker)
        self.weapon = fortyk.WP.weapon(attacker, hiton)
        self.target = fortyk.WP.Target(target)

    def calculate_attack(self):
        attackCount = []
        damage_print = [] #total attacks and damage of each attack per calculation
        for x in range(0,50):
            damage = []
            starting_wounds = self.target.wounds
            while self.target.checkdead() == False:
                attack_dmg = self.weapon.attack(self.target)
                #attack_dmg = self.attacker.attack_suite(self.target)
                self.target.wounds -= attack_dmg
                damage.append(attack_dmg)

            damage_print.append(damage)
            attackCount.append(len(damage)) #len(damage) how many turns were required for a takedown
            self.target.wounds = starting_wounds

        average = sum(attackCount)/len(attackCount) #average turns to kill
        return (average, damage_print) #tuplelife
