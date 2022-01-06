import random
from globalVars import GlobalVars
gv = GlobalVars()

flat_per_floor = 2
cross_floor_time = 180  # Вказуєтся зразу за весь підїзд
cross_pdz_time = 10
cross_building_time = 30
pdz_per_building = 9
avg_domofon_time = 60
domofon_time_dispersion = 30
domofon_deny_percent = 0.4
kolyadka_time = 180
avg_standard_bounty = 7
standard_bounty_dispersion = 3
avg_big_bounty = 35
big_bounty_dispersion = 15
big_bounty_percent = 0.02
deny_percent = 0.35
building_types = [5, 9, 5]
novaya_lita_percent = 0.001
gopstop_percent = 0.00001  # Вірогітність наткнутись на гоп-стоп
buildings_qty = abs(int(input("Buildings qty: ")))

gv.setVar({"tb": 0, "tt": 0, "td": 0})


def loot_flat():
    deny_chance = int(1 / deny_percent)
    if random.choice(range(deny_chance)) == 0:
        total_deny = gv["td"]
        total_deny += 1
        gv.updateVar({"td": total_deny})
    else:
        total_time = gv["tt"]
        total_time += kolyadka_time
        gv.updateVar({"tt": total_time})
        big_bounty_chance = int(1 / big_bounty_percent)
        if random.choice(range(big_bounty_chance)) == 0:
            bounty = avg_big_bounty + random.choice(range(0 - big_bounty_dispersion, big_bounty_dispersion))
        else:
            bounty = avg_standard_bounty + random.choice(range(0 - standard_bounty_dispersion, standard_bounty_dispersion))
        novaya_lita_chance = int(1 / novaya_lita_percent)
        if random.choice(range(novaya_lita_chance)) == 0:
            total_time = gv["tt"]
            total_time += kolyadka_time
            gv.updateVar({"tt": total_time})
        total_bounty = gv["tb"]
        total_bounty += bounty
        gv.updateVar({"tb": total_bounty})


def loot_floor():
    looted_flats = 0
    while looted_flats < flat_per_floor:
        loot_flat()
        looted_flats += 1


def loot_pdz():
    floor_qty = random.choice(building_types)
    looted_floors = 0
    while looted_floors < floor_qty:
        loot_floor()
        looted_floors += 1


def loot_building():
    looted_pdz = 0
    while looted_pdz < pdz_per_building:
        domofon_deny_chance = int(1 / domofon_deny_percent)
        if random.choice(range(domofon_deny_chance)) == 0:
            total_deny = gv["td"]
            total_deny += 1
            gv.updateVar({"td": total_deny})
            looted_pdz += 1
        else:
            total_time = gv["tt"]
            total_time += avg_domofon_time + random.choice(range(0 - domofon_time_dispersion, domofon_time_dispersion)) + cross_pdz_time + cross_floor_time
            gv.updateVar({"tt": total_time})
            loot_pdz()
            looted_pdz += 1


looted_buildings = 0
while looted_buildings < buildings_qty:
    total_time = gv["tt"]
    total_time += cross_building_time
    gv.updateVar({"tt": total_time})
    loot_building()
    gopstop_chance = int(1 / gopstop_percent)
    if random.choice(range(gopstop_chance)) == 0:
        b = gv["tb"]
        print(f"Гоп-стоп: вас ізбили і відібрали {b} грн")
        gv.updateVar({"tb": 0})
    looted_buildings += 1


total_bounty = gv["tb"]
total_time = gv["tt"]
total_deny = gv["td"]

print(f"Total bounty: {total_bounty}грн")
print(f"Total time {round(total_time / 60 / 60)}г")
print(f"Total deny: {total_deny}")
