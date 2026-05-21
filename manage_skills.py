#!/usr/bin/env python3
import os
import sys
import re
import shutil
import argparse

HOME = os.path.expanduser("~")
FABRIC_PATTERNS_DIR = os.path.join(HOME, ".config/fabric/patterns")
SKILLS_DIR = os.path.join(HOME, ".gemini/config/skills")
DISABLED_SKILLS_DIR = os.path.join(HOME, ".gemini/config/disabled_skills")
EXPLANATIONS_FILE = os.path.join(HOME, ".config/fabric/patterns/pattern_explanations.md")

def load_descriptions():
    descriptions = {}
    if os.path.exists(EXPLANATIONS_FILE):
        with open(EXPLANATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                m1 = re.match(r'^\d+\.\s+\*\*([a-zA-Z0-9_-]+)\*\*:\s*(.*)$', line.strip())
                if m1:
                    name, desc = m1.groups()
                    descriptions[name] = desc.strip()
                    continue
                m2 = re.match(r'^-\s+.*?\*\*([a-zA-Z0-9_-]+)\*\*,\s*(.*)$', line.strip())
                if m2:
                    name, desc = m2.groups()
                    descriptions[name] = desc.strip()
                    continue
    return descriptions

def get_available_fabric_patterns():
    if not os.path.exists(FABRIC_PATTERNS_DIR):
        return []
    patterns = []
    for item in os.listdir(FABRIC_PATTERNS_DIR):
        item_path = os.path.join(FABRIC_PATTERNS_DIR, item)
        if os.path.isdir(item_path):
            system_md = os.path.join(item_path, "system.md")
            if os.path.exists(system_md):
                patterns.append(item)
    return sorted(patterns)

def get_skill_name(pattern_name):
    slug = pattern_name.replace("_", "-")
    return f"fabric-{slug}"

def get_dir_skills(dir_path):
    if not os.path.exists(dir_path):
        return []
    return sorted([d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))])

def import_fabric_pattern(pattern_name, descriptions, target_dir):
    pattern_path = os.path.join(FABRIC_PATTERNS_DIR, pattern_name)
    system_md_path = os.path.join(pattern_path, "system.md")
    
    if not os.path.exists(system_md_path):
        print(f"Error: system.md not found for pattern '{pattern_name}'", file=sys.stderr)
        return False
        
    skill_name = get_skill_name(pattern_name)
    skill_dir = os.path.join(target_dir, skill_name)
    os.makedirs(skill_dir, exist_ok=True)
    
    desc = descriptions.get(pattern_name, f"Fabric pattern for {pattern_name.replace('_', ' ')}")
    desc_clean = desc.replace("\n", " ").replace("\"", "\\\"")
    
    with open(system_md_path, 'r', encoding='utf-8') as f:
        system_content = f.read()
        
    skill_md_content = f"""---
name: {skill_name}
description: [Fabric] {desc_clean}
---

# Fabric Pattern: {pattern_name}

This skill provides the instructions for the Fabric pattern `{pattern_name}`.
Use this skill when the user asks to run the `{pattern_name}` pattern or when its specific capability is needed.

## Pattern Instructions

```markdown
{system_content.strip()}
```
"""
    
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(skill_md_content)
        
    print(f"Imported Fabric pattern: {pattern_name} -> {skill_name} (in {os.path.basename(target_dir)})")
    return True

def move_skill(skill_name, src_dir, dest_dir):
    src_path = os.path.join(src_dir, skill_name)
    dest_path = os.path.join(dest_dir, skill_name)
    
    if not os.path.exists(src_path):
        return False
        
    os.makedirs(dest_dir, exist_ok=True)
    shutil.move(src_path, dest_path)
    return True

def main():
    parser = argparse.ArgumentParser(description="Manage Antigravity AI skills (both standard skills and Fabric patterns).")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    subparsers.add_parser("list", help="List all skills (Active, Disabled, and Unimported Fabric patterns)")
    
    # Enable command
    enable_parser = subparsers.add_parser("enable", help="Enable specified skills")
    enable_parser.add_argument("skills", nargs="*", help="Names of skills to enable")
    enable_parser.add_argument("--all", action="store_true", help="Enable all currently disabled skills")
    
    # Disable command
    disable_parser = subparsers.add_parser("disable", help="Disable specified skills")
    disable_parser.add_argument("skills", nargs="*", help="Names of skills to disable")
    disable_parser.add_argument("--all", action="store_true", help="Disable all currently active skills")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    os.makedirs(SKILLS_DIR, exist_ok=True)
    os.makedirs(DISABLED_SKILLS_DIR, exist_ok=True)
    
    active_skills = get_dir_skills(SKILLS_DIR)
    disabled_skills = get_dir_skills(DISABLED_SKILLS_DIR)
    fabric_patterns = get_available_fabric_patterns()
    descriptions = load_descriptions()
    
    if args.command == "list":
        print("\n=== ACTIVE SKILLS ===")
        if not active_skills:
            print("  (None)")
        else:
            for s in active_skills: print(f"  [+] {s}")
            
        print("\n=== DISABLED SKILLS ===")
        if not disabled_skills:
            print("  (None)")
        else:
            for s in disabled_skills: print(f"  [-] {s}")
            
        unimported_fabric = []
        for p in fabric_patterns:
            s_name = get_skill_name(p)
            if s_name not in active_skills and s_name not in disabled_skills:
                unimported_fabric.append(p)
                
        print(f"\n=== UNIMPORTED FABRIC PATTERNS ({len(unimported_fabric)}) ===")
        if not unimported_fabric:
            print("  (None)")
        else:
            # Just show a few to not flood the terminal
            for p in unimported_fabric[:15]: 
                print(f"  [ ] {p}")
            if len(unimported_fabric) > 15:
                print(f"  ... and {len(unimported_fabric) - 15} more. (Use 'enable <pattern>' to import)")
        print()
                
    elif args.command == "enable":
        if not args.skills and not args.all:
            print("Error: Specify skills to enable, or use --all", file=sys.stderr)
            sys.exit(1)
            
        skills_to_enable = []
        if args.all:
            skills_to_enable = disabled_skills
        else:
            skills_to_enable = args.skills
            
        if not skills_to_enable:
            print("No skills to enable.")
            return
            
        success = 0
        for s in skills_to_enable:
            # Try to move from disabled to active
            if s in disabled_skills or os.path.exists(os.path.join(DISABLED_SKILLS_DIR, s)):
                if move_skill(s, DISABLED_SKILLS_DIR, SKILLS_DIR):
                    print(f"Enabled: {s}")
                    success += 1
            else:
                # Is it an unimported fabric pattern?
                # Check if they passed 'summarize' or 'fabric-summarize'
                clean_name = s.replace("fabric-", "").replace("-", "_")
                if clean_name in fabric_patterns:
                    if import_fabric_pattern(clean_name, descriptions, SKILLS_DIR):
                        success += 1
                elif s in fabric_patterns:
                    if import_fabric_pattern(s, descriptions, SKILLS_DIR):
                        success += 1
                else:
                    if s in active_skills:
                        print(f"Skill '{s}' is already enabled.")
                    else:
                        print(f"Error: Skill or pattern '{s}' not found.", file=sys.stderr)
                        
        print(f"Successfully enabled {success} skills.")
        
    elif args.command == "disable":
        if not args.skills and not args.all:
            print("Error: Specify skills to disable, or use --all", file=sys.stderr)
            sys.exit(1)
            
        skills_to_disable = []
        if args.all:
            skills_to_disable = active_skills
        else:
            skills_to_disable = args.skills
            
        if not skills_to_disable:
            print("No skills to disable.")
            return
            
        success = 0
        for s in skills_to_disable:
            # Handle if they typed 'summarize' instead of 'fabric-summarize'
            possible_names = [s, get_skill_name(s), f"fabric-{s}"]
            found = False
            for p_name in possible_names:
                if p_name in active_skills or os.path.exists(os.path.join(SKILLS_DIR, p_name)):
                    if move_skill(p_name, SKILLS_DIR, DISABLED_SKILLS_DIR):
                        print(f"Disabled: {p_name}")
                        success += 1
                        found = True
                        break
            if not found:
                if s in disabled_skills:
                    print(f"Skill '{s}' is already disabled.")
                else:
                    print(f"Error: Active skill '{s}' not found.", file=sys.stderr)
                    
        print(f"Successfully disabled {success} skills.")

if __name__ == "__main__":
    main()
