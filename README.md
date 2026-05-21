# Antigravity Skill Manager

A clean, portable CLI utility to dynamically enable, disable, and manage skills in your **Antigravity AI Coding Assistant** environment. This tool helps you save significant context tokens and keep your prompt focused by keeping unused skills deactivated.

---

## 📖 How It Works

By default, loading many skills in your active skills directory (`~/.gemini/config/skills/`) injects their metadata into the assistant's prompt for every chat turn, causing high token overhead.

This tool solves that by maintaining a `disabled_skills/` directory. Unused skills are safely moved there to be completely ignored by the AI, saving tokens and preserving context focus. When a skill is needed, it can be loaded instantly via the CLI or automatically by the manager.

---

## 🛠️ Installation & Setup

1. **Clone this repository** into your Projects folder:
   ```bash
   git clone git@github.com:leofishman/aby.git ~/Proyects/aby
   ```

2. **Make the script executable**:
   ```bash
   chmod +x ~/Proyects/aby/manage_skills.py
   ```

3. **Install the Skill Manager as the only active skill** in your Antigravity config:
   ```bash
   mkdir -p ~/.gemini/config/skills/skill-manager
   cp ~/Proyects/aby/SKILL.md ~/.gemini/config/skills/skill-manager/SKILL.md
   ```

Now, the AI assistant will always have the `skill-manager` capability loaded and will know how to load/unload other skills on-the-fly when requested.

---

## 🚀 CLI Usage

You can run the script manually from your terminal to manage your active skills.

### 1. List Available Skills
Lists all Active and Disabled skills:
```bash
~/Proyects/aby/manage_skills.py list
```

### 2. Enable Skills
Enables specific skills by name.
```bash
# Enable specific skills
~/Proyects/aby/manage_skills.py enable <skill_name>

# Enable all disabled skills at once
~/Proyects/aby/manage_skills.py enable --all
```

### 3. Disable Skills (Save Tokens!)
Safely deactivates skills by moving them to the `disabled_skills` directory.
```bash
# Disable specific active skills
~/Proyects/aby/manage_skills.py disable <skill_name>

# Disable all active skills (Safe Mode)
~/Proyects/aby/manage_skills.py disable --all
```

---

## 📂 Project Structure

```
.
├── manage_skills.py  # The main CLI management script
├── SKILL.md          # Antigravity skill configuration file
├── .gitignore        # Standard python/IDE gitignore
├── LICENSE           # MIT License
└── README.md         # This documentation
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
