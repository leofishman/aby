# Antigravity Skill Manager

A clean, portable CLI utility to dynamically enable, disable, and manage skills in your **Antigravity AI Coding Assistant** environment. This tool helps you save significant context tokens and keep your prompt focused by keeping unused skills deactivated.

---

## 📖 How It Works

By default, loading many skills in your active skills directory (`~/.gemini/config/skills/`) injects their metadata into the assistant's prompt for every chat turn, causing high token overhead.

This tool solves that by maintaining a `disabled_skills/` directory. Unused skills are safely moved there to be completely ignored by the AI, saving tokens and preserving context focus. When a skill is needed, it can be loaded instantly via the CLI or automatically by the manager.

---

## 🛠️ Installation & Setup

You can clone this repository to any location (such as `~/Projects/aby` or directly into the skills folder). To activate it:

1. **Create the skill-manager directory**:
   ```bash
   mkdir -p ~/.gemini/config/skills/skill-manager
   ```

2. **Copy or Symlink both files** (`SKILL.md` and `manage_skills.py`) into the active skills directory:
   ```bash
   cp SKILL.md manage_skills.py ~/.gemini/config/skills/skill-manager/
   ```

3. **Make the script executable**:
   ```bash
   chmod +x ~/.gemini/config/skills/skill-manager/manage_skills.py
   ```

Once installed, the AI assistant will always have the `skill-manager` capability loaded and will know how to run the script inside its own directory dynamically.

---

## 🚀 CLI Usage

You can run the script manually from your terminal inside the skill folder, or let the assistant invoke it on your behalf.

### 1. List Available Skills
```bash
./manage_skills.py list
```

### 2. Enable Skills
```bash
./manage_skills.py enable <skill_name>
```

### 3. Disable Skills (Save Tokens!)
```bash
./manage_skills.py disable <skill_name>
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
