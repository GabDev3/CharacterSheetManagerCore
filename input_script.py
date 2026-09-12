import requests
import json
import time
import random

BASE_URL = "http://localhost:5126/api"
HEADERS = {"Content-Type": "application/json"}

def make_request(method, endpoint, data=None, retries=3):
    """Make HTTP request with error handling and retry logic"""
    url = f"{BASE_URL}/{endpoint}"
    
    for attempt in range(retries):
        try:
            if method == "POST":
                response = requests.post(url, headers=HEADERS, json=data, timeout=30)
            elif method == "GET":
                response = requests.get(url, headers=HEADERS, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=HEADERS, timeout=30)
            
            response.raise_for_status()
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.Timeout:
            print(f"⏱️  Timeout on attempt {attempt + 1} for {method} {endpoint}")
            if attempt < retries - 1:
                time.sleep(2)
                continue
            else:
                print(f"❌ Final timeout for {method} {endpoint}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error making {method} request to {endpoint} (attempt {attempt + 1}): {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            if attempt < retries - 1:
                time.sleep(1)
                continue
            return None
    
    return None

def clear_database():
    """Clear all existing data"""
    print("🗑️  Clearing existing data...")
    
    endpoints_to_clear = ["spells", "items", "characters", "spelltemplates", "itemtemplates"]
    
    for endpoint in endpoints_to_clear:
        records = make_request("GET", endpoint)
        if records:
            for record in records:
                if 'id' in record:
                    result = make_request("DELETE", f"{endpoint}/{record['id']}")
                    if result is not None:
                        print(f"✓ Deleted {endpoint}: {record.get('name', record['id'])}")
    
    print("✅ Database cleared!")

def seed_item_templates():
    """Create 20 item templates"""
    print("Creating item templates...")
    
    item_templates = [
        # Weapons
        {"name": "Excalibur", "effect": "The legendary sword of King Arthur.", "strengthBonus": 5, "charismaBonus": 3, "category": "Weapon", "isActive": True},
        {"name": "Mjolnir", "effect": "Thor's mighty hammer.", "strengthBonus": 6, "constitutionBonus": 3, "category": "Weapon", "isActive": True},
        {"name": "Gungnir", "effect": "Odin's spear that never misses.", "dexterityBonus": 4, "wisdomBonus": 3, "category": "Weapon", "isActive": True},
        {"name": "Dragonslayer Sword", "effect": "Forged to slay dragons.", "strengthBonus": 4, "category": "Weapon", "isActive": True},
        {"name": "Elven Longbow", "effect": "Masterfully crafted elven bow.", "dexterityBonus": 4, "category": "Weapon", "isActive": True},
        {"name": "Staff of Elements", "effect": "Controls elemental forces.", "intelligenceBonus": 4, "wisdomBonus": 2, "category": "Weapon", "isActive": True},
        {"name": "Shadow Daggers", "effect": "Twin daggers of shadow.", "dexterityBonus": 5, "category": "Weapon", "isActive": True},
        
        # Armor
        {"name": "Dragon Scale Mail", "effect": "Armor from dragon scales.", "armorBonus": 10, "constitutionBonus": 3, "category": "Armor", "isActive": True},
        {"name": "Celestial Plate", "effect": "Blessed by celestial beings.", "armorBonus": 9, "wisdomBonus": 2, "charismaBonus": 2, "category": "Armor", "isActive": True},
        {"name": "Shadowsilk Robes", "effect": "Woven from shadow and moonlight.", "armorBonus": 2, "dexterityBonus": 3, "category": "Armor", "isActive": True},
        {"name": "Adamantine Plate", "effect": "Nearly indestructible armor.", "armorBonus": 11, "category": "Armor", "isActive": True},
        {"name": "Archmage Vestments", "effect": "Ultimate magical robes.", "armorBonus": 3, "intelligenceBonus": 5, "wisdomBonus": 2, "category": "Armor", "isActive": True},
        {"name": "Leather of Agility", "effect": "Enhances movement and flexibility.", "armorBonus": 4, "dexterityBonus": 3, "category": "Armor", "isActive": True},
        
        # Accessories
        {"name": "Ring of Power", "effect": "One ring to rule them all.", "strengthBonus": 2, "dexterityBonus": 2, "constitutionBonus": 2, "intelligenceBonus": 2, "wisdomBonus": 2, "charismaBonus": 2, "category": "Accessory", "isActive": True},
        {"name": "Amulet of Life", "effect": "Protects against death magic.", "constitutionBonus": 4, "wisdomBonus": 2, "category": "Accessory", "isActive": True},
        {"name": "Boots of Speed", "effect": "Greatly increases movement speed.", "dexterityBonus": 4, "category": "Accessory", "isActive": True},
        {"name": "Gauntlets of Strength", "effect": "Grants incredible physical power.", "strengthBonus": 6, "category": "Accessory", "isActive": True},
        {"name": "Cloak of Protection", "effect": "Provides magical protection.", "armorBonus": 3, "constitutionBonus": 2, "category": "Accessory", "isActive": True},
        {"name": "Crown of Wisdom", "effect": "Enhances mental faculties.", "intelligenceBonus": 4, "wisdomBonus": 4, "category": "Accessory", "isActive": True},
        {"name": "Belt of Giant Strength", "effect": "Grants the strength of giants.", "strengthBonus": 5, "constitutionBonus": 2, "category": "Accessory", "isActive": True}
    ]
    
    created_templates = []
    for template in item_templates:
        result = make_request("POST", "itemtemplates", template)
        if result:
            created_templates.append(result)
            print(f"✓ Created item template: {template['name']}")
        else:
            print(f"✗ Failed to create item template: {template['name']}")
        time.sleep(0.3)
    
    return created_templates

def seed_spell_templates():
    """Create 20 spell templates"""
    print("\nCreating spell templates...")
    
    spell_templates = [
        # Cantrips
        {"name": "Fire Bolt", "effect": "A mote of fire streaks toward target.", "damage": "1d10", "level": 0, "school": "Evocation", "castingTime": "1 action", "range": "120 feet", "components": "V, S", "duration": "Instantaneous", "isActive": True},
        {"name": "Mage Hand", "effect": "A spectral hand appears.", "level": 0, "school": "Conjuration", "castingTime": "1 action", "range": "30 feet", "components": "V, S", "duration": "1 minute", "isActive": True},
        {"name": "Minor Illusion", "effect": "Create a sound or image.", "level": 0, "school": "Illusion", "castingTime": "1 action", "range": "30 feet", "components": "S, M", "duration": "1 minute", "isActive": True},
        {"name": "Eldritch Blast", "effect": "A crackling beam of energy.", "damage": "1d10", "level": 0, "school": "Evocation", "castingTime": "1 action", "range": "120 feet", "components": "V, S", "duration": "Instantaneous", "isActive": True},
        {"name": "Sacred Flame", "effect": "Radiance descends on target.", "damage": "1d8", "level": 0, "school": "Evocation", "castingTime": "1 action", "range": "60 feet", "components": "V, S", "duration": "Instantaneous", "isActive": True},
        
        # Level 1-3
        {"name": "Magic Missile", "effect": "Three darts of magical force.", "damage": "1d4+1", "level": 1, "school": "Evocation", "castingTime": "1 action", "range": "120 feet", "components": "V, S", "duration": "Instantaneous", "isActive": True},
        {"name": "Healing Word", "effect": "Heal a creature with a word.", "damage": "1d4+mod", "level": 1, "school": "Evocation", "castingTime": "1 bonus action", "range": "60 feet", "components": "V", "duration": "Instantaneous", "isActive": True},
        {"name": "Shield", "effect": "Invisible barrier protects you.", "level": 1, "school": "Abjuration", "castingTime": "1 reaction", "range": "Self", "components": "V, S", "duration": "1 round", "isActive": True},
        {"name": "Burning Hands", "effect": "Flames shoot from fingertips.", "damage": "3d6", "level": 1, "school": "Evocation", "castingTime": "1 action", "range": "Self (15-foot cone)", "components": "V, S", "duration": "Instantaneous", "isActive": True},
        {"name": "Cure Wounds", "effect": "Touch heals hit points.", "damage": "1d8+mod", "level": 1, "school": "Evocation", "castingTime": "1 action", "range": "Touch", "components": "V, S", "duration": "Instantaneous", "isActive": True},
        {"name": "Invisibility", "effect": "Become invisible.", "level": 2, "school": "Illusion", "castingTime": "1 action", "range": "Touch", "components": "V, S, M", "duration": "Concentration, up to 1 hour", "isActive": True},
        {"name": "Misty Step", "effect": "Teleport up to 30 feet.", "level": 2, "school": "Conjuration", "castingTime": "1 bonus action", "range": "Self", "components": "V", "duration": "Instantaneous", "isActive": True},
        {"name": "Fireball", "effect": "Explosion of flame.", "damage": "8d6", "level": 3, "school": "Evocation", "castingTime": "1 action", "range": "150 feet", "components": "V, S, M", "duration": "Instantaneous", "isActive": True},
        {"name": "Lightning Bolt", "effect": "Line of lightning.", "damage": "8d6", "level": 3, "school": "Evocation", "castingTime": "1 action", "range": "Self (100-foot line)", "components": "V, S, M", "duration": "Instantaneous", "isActive": True},
        {"name": "Counterspell", "effect": "Interrupt spellcasting.", "level": 3, "school": "Abjuration", "castingTime": "1 reaction", "range": "60 feet", "components": "S", "duration": "Instantaneous", "isActive": True},
        
        # High Level
        {"name": "Dimension Door", "effect": "Teleport anywhere in range.", "level": 4, "school": "Conjuration", "castingTime": "1 action", "range": "500 feet", "components": "V", "duration": "Instantaneous", "isActive": True},
        {"name": "Polymorph", "effect": "Transform into a beast.", "level": 4, "school": "Transmutation", "castingTime": "1 action", "range": "60 feet", "components": "V, S, M", "duration": "Concentration, up to 1 hour", "isActive": True},
        {"name": "Telekinesis", "effect": "Move objects with your mind.", "level": 5, "school": "Transmutation", "castingTime": "1 action", "range": "60 feet", "components": "V, S", "duration": "Concentration, up to 10 minutes", "isActive": True},
        {"name": "Chain Lightning", "effect": "Lightning arcs between targets.", "damage": "10d8", "level": 6, "school": "Evocation", "castingTime": "1 action", "range": "150 feet", "components": "V, S, M", "duration": "Instantaneous", "isActive": True},
        {"name": "Time Stop", "effect": "Stop time briefly.", "level": 9, "school": "Transmutation", "castingTime": "1 action", "range": "Self", "components": "V", "duration": "Instantaneous", "isActive": True}
    ]
    
    created_templates = []
    for template in spell_templates:
        result = make_request("POST", "spelltemplates", template)
        if result:
            created_templates.append(result)
            print(f"✓ Created spell template: {template['name']}")
        else:
            print(f"✗ Failed to create spell template: {template['name']}")
        time.sleep(0.3)
    
    return created_templates

def seed_characters():
    """Create 20 characters"""
    print("\nCreating characters...")
    
    characters = [
        {"name": "Gandalf the Grey", "class": "Wizard", "level": 15, "armorClass": 12, "strength": 10, "dexterity": 11, "constitution": 12, "intelligence": 20, "wisdom": 18, "charisma": 16},
        {"name": "Aragorn", "class": "Ranger", "level": 12, "armorClass": 18, "strength": 16, "dexterity": 18, "constitution": 15, "intelligence": 14, "wisdom": 16, "charisma": 14},
        {"name": "Legolas", "class": "Ranger", "level": 10, "armorClass": 16, "strength": 12, "dexterity": 20, "constitution": 14, "intelligence": 13, "wisdom": 18, "charisma": 15},
        {"name": "Gimli", "class": "Fighter", "level": 11, "armorClass": 20, "strength": 18, "dexterity": 10, "constitution": 18, "intelligence": 10, "wisdom": 12, "charisma": 11},
        {"name": "Merlin", "class": "Wizard", "level": 20, "armorClass": 14, "strength": 8, "dexterity": 12, "constitution": 14, "intelligence": 20, "wisdom": 19, "charisma": 17},
        {"name": "Robin Hood", "class": "Rogue", "level": 8, "armorClass": 15, "strength": 12, "dexterity": 20, "constitution": 13, "intelligence": 14, "wisdom": 16, "charisma": 15},
        {"name": "Conan", "class": "Barbarian", "level": 9, "armorClass": 16, "strength": 20, "dexterity": 16, "constitution": 18, "intelligence": 10, "wisdom": 11, "charisma": 12},
        {"name": "Elara Moonwhisper", "class": "Cleric", "level": 7, "armorClass": 17, "strength": 13, "dexterity": 11, "constitution": 15, "intelligence": 14, "wisdom": 20, "charisma": 16},
        {"name": "Zara Nightblade", "class": "Rogue", "level": 13, "armorClass": 17, "strength": 10, "dexterity": 20, "constitution": 14, "intelligence": 16, "wisdom": 15, "charisma": 12},
        {"name": "Thorin Ironforge", "class": "Fighter", "level": 14, "armorClass": 19, "strength": 18, "dexterity": 12, "constitution": 17, "intelligence": 11, "wisdom": 13, "charisma": 10},
        {"name": "Luna Starweaver", "class": "Sorcerer", "level": 11, "armorClass": 13, "strength": 8, "dexterity": 16, "constitution": 13, "intelligence": 15, "wisdom": 12, "charisma": 20},
        {"name": "Finn the Bold", "class": "Bard", "level": 9, "armorClass": 14, "strength": 10, "dexterity": 16, "constitution": 12, "intelligence": 14, "wisdom": 13, "charisma": 18},
        {"name": "Brother Marcus", "class": "Monk", "level": 10, "armorClass": 16, "strength": 12, "dexterity": 18, "constitution": 15, "intelligence": 13, "wisdom": 20, "charisma": 11},
        {"name": "Draven Shadowmere", "class": "Warlock", "level": 12, "armorClass": 15, "strength": 10, "dexterity": 14, "constitution": 16, "intelligence": 15, "wisdom": 12, "charisma": 20},
        {"name": "Gaia Earthsong", "class": "Druid", "level": 13, "armorClass": 14, "strength": 12, "dexterity": 15, "constitution": 16, "intelligence": 13, "wisdom": 20, "charisma": 14},
        {"name": "Sir Galahad", "class": "Paladin", "level": 16, "armorClass": 20, "strength": 18, "dexterity": 10, "constitution": 16, "intelligence": 12, "wisdom": 15, "charisma": 18},
        {"name": "Tempest Stormborn", "class": "Sorcerer", "level": 14, "armorClass": 15, "strength": 9, "dexterity": 17, "constitution": 15, "intelligence": 16, "wisdom": 13, "charisma": 20},
        {"name": "Kael Swiftstrike", "class": "Ranger", "level": 11, "armorClass": 16, "strength": 14, "dexterity": 20, "constitution": 15, "intelligence": 12, "wisdom": 17, "charisma": 13},
        {"name": "Morgana Le Fay", "class": "Wizard", "level": 18, "armorClass": 16, "strength": 8, "dexterity": 14, "constitution": 13, "intelligence": 20, "wisdom": 16, "charisma": 17},
        {"name": "Bjorn Bloodaxe", "class": "Barbarian", "level": 12, "armorClass": 15, "strength": 20, "dexterity": 14, "constitution": 19, "intelligence": 8, "wisdom": 10, "charisma": 11}
    ]
    
    created_characters = []
    for character in characters:
        result = make_request("POST", "characters", character)
        if result:
            created_characters.append(result)
            print(f"✓ Created character: {character['name']} (Level {character['level']} {character['class']})")
        else:
            print(f"✗ Failed to create character: {character['name']}")
        time.sleep(0.3)
    
    return created_characters

def seed_items(characters, item_templates):
    """Create 20 items for characters"""
    print("\nCreating items...")
    
    if not characters or not item_templates:
        print("No characters or item templates available")
        return []
    
    created_items = []
    template_lookup = {t['name']: t['id'] for t in item_templates}
    
    # Assign specific items to first 10 characters
    assignments = [
        {"char_idx": 0, "item": "Staff of Elements"},      # Gandalf
        {"char_idx": 1, "item": "Elven Longbow"},          # Aragorn  
        {"char_idx": 2, "item": "Elven Longbow"},          # Legolas
        {"char_idx": 3, "item": "Mjolnir"},                # Gimli
        {"char_idx": 4, "item": "Archmage Vestments"},     # Merlin
        {"char_idx": 5, "item": "Shadow Daggers"},         # Robin Hood
        {"char_idx": 6, "item": "Dragonslayer Sword"},     # Conan
        {"char_idx": 7, "item": "Celestial Plate"},        # Elara
        {"char_idx": 8, "item": "Shadowsilk Robes"},       # Zara
        {"char_idx": 9, "item": "Adamantine Plate"},       # Thorin
        {"char_idx": 10, "item": "Ring of Power"},         # Luna
        {"char_idx": 11, "item": "Crown of Wisdom"},       # Finn
        {"char_idx": 12, "item": "Gauntlets of Strength"}, # Marcus
        {"char_idx": 13, "item": "Cloak of Protection"},   # Draven
        {"char_idx": 14, "item": "Amulet of Life"},        # Gaia
        {"char_idx": 15, "item": "Excalibur"},             # Galahad
        {"char_idx": 16, "item": "Belt of Giant Strength"}, # Tempest
        {"char_idx": 17, "item": "Boots of Speed"},        # Kael
        {"char_idx": 18, "item": "Dragon Scale Mail"},     # Morgana
        {"char_idx": 19, "item": "Gungnir"}                # Bjorn
    ]
    
    for assignment in assignments:
        char_idx = assignment["char_idx"]
        item_name = assignment["item"]
        
        if char_idx < len(characters) and item_name in template_lookup:
            item_request = {
                "itemTemplateId": template_lookup[item_name],
                "characterId": characters[char_idx]['id']
            }
            
            result = make_request("POST", "items/from-template", item_request)
            if result:
                created_items.append(result)
                print(f"✓ Created item: {item_name} for {characters[char_idx]['name']}")
            else:
                print(f"✗ Failed to create item: {item_name}")
            time.sleep(0.3)
    
    return created_items

def seed_spells(characters, spell_templates):
    """Create 20 spells for characters"""
    print("\nCreating spells...")
    
    if not characters or not spell_templates:
        print("No characters or spell templates available")
        return []
    
    created_spells = []
    template_lookup = {t['name']: t['id'] for t in spell_templates}
    
    # Assign spells to spellcasting characters
    spell_assignments = [
        {"char_idx": 0, "spell": "Fireball"},         # Gandalf
        {"char_idx": 0, "spell": "Lightning Bolt"},   # Gandalf
        {"char_idx": 4, "spell": "Time Stop"},        # Merlin
        {"char_idx": 4, "spell": "Chain Lightning"},  # Merlin
        {"char_idx": 7, "spell": "Healing Word"},     # Elara
        {"char_idx": 7, "spell": "Cure Wounds"},      # Elara
        {"char_idx": 10, "spell": "Magic Missile"},   # Luna
        {"char_idx": 10, "spell": "Invisibility"},    # Luna
        {"char_idx": 11, "spell": "Minor Illusion"},  # Finn
        {"char_idx": 11, "spell": "Misty Step"},      # Finn
        {"char_idx": 13, "spell": "Eldritch Blast"},  # Draven
        {"char_idx": 13, "spell": "Counterspell"},    # Draven
        {"char_idx": 14, "spell": "Cure Wounds"},     # Gaia
        {"char_idx": 14, "spell": "Polymorph"},       # Gaia
        {"char_idx": 15, "spell": "Sacred Flame"},    # Galahad
        {"char_idx": 15, "spell": "Shield"},          # Galahad
        {"char_idx": 16, "spell": "Fire Bolt"},       # Tempest
        {"char_idx": 16, "spell": "Dimension Door"},  # Tempest
        {"char_idx": 18, "spell": "Telekinesis"},     # Morgana
        {"char_idx": 18, "spell": "Burning Hands"}    # Morgana
    ]
    
    for assignment in spell_assignments:
        char_idx = assignment["char_idx"]
        spell_name = assignment["spell"]
        
        if char_idx < len(characters) and spell_name in template_lookup:
            spell_request = {
                "spellTemplateId": template_lookup[spell_name],
                "characterId": characters[char_idx]['id']
            }
            
            result = make_request("POST", "spells/from-template", spell_request)
            if result:
                created_spells.append(result)
                print(f"✓ Created spell: {spell_name} for {characters[char_idx]['name']}")
            else:
                print(f"✗ Failed to create spell: {spell_name}")
            time.sleep(0.3)
    
    return created_spells

def main():
    """Main seeding function - exactly 100 entries"""
    print("🚀 Starting Database Seeding - 100 Entries Total")
    print(f"Target URL: {BASE_URL}")
    print("-" * 50)
    
    try:
        # Test API connection
        test_response = make_request("GET", "characters")
        if test_response is None:
            print("❌ Cannot connect to API. Make sure your server is running at http://localhost:5000")
            return
        
        print("✅ API connection successful")
        
        # Clear existing data
        clear_database()
        
        # Create exactly 100 entries
        print("\n" + "="*40)
        print("📦 CREATING DATA")
        print("="*40)
        
        item_templates = seed_item_templates()    # 20 entries
        spell_templates = seed_spell_templates()  # 20 entries
        characters = seed_characters()            # 20 entries
        items = seed_items(characters, item_templates)      # 20 entries
        spells = seed_spells(characters, spell_templates)   # 20 entries
        
        # Summary
        print("\n" + "="*50)
        print("📊 FINAL SUMMARY")
        print("="*50)
        print(f"Item Templates: {len(item_templates)}")
        print(f"Spell Templates: {len(spell_templates)}")
        print(f"Characters: {len(characters)}")
        print(f"Items: {len(items)}")
        print(f"Spells: {len(spells)}")
        print("-" * 50)
        total = len(item_templates) + len(spell_templates) + len(characters) + len(items) + len(spells)
        print(f"TOTAL ENTRIES CREATED: {total}")
        print("\n✅ Database seeding completed successfully!")
        print(f"🌐 Visit http://localhost:5000 to see your data!")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()