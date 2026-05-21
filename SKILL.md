---
name: skill-manager
description: Manage and dynamically load/unload Antigravity skills to save context tokens. Use this skill when you need a capability you don't currently have active.
---

# Skill Manager

This is the central skill management tool. It allows you to enable and disable skills on-the-fly to keep the system context lightweight and save tokens.

**Script Path**: `~/Proyects/aby/manage_skills.py`

## Available Commands

When you realize you need a specific skill, you must use the `run_command` tool to execute the python script:

1. **List all available skills (Active and Disabled):**
   ```bash
   ~/Proyects/aby/manage_skills.py list
   ```

2. **Enable specific skills:**
   ```bash
   ~/Proyects/aby/manage_skills.py enable <skill_name1> <skill_name2>
   ```
   *Example:* `~/Proyects/aby/manage_skills.py enable my-special-skill`
   *Note: Check if the skill you need is active. If not, enable it using this command, and then read its `SKILL.md` via `view_file` to learn how to use it.*

3. **Disable specific skills:**
   ```bash
   ~/Proyects/aby/manage_skills.py disable <skill_name>
   ```
   *Note: You should disable skills when you are completely done with a task to save tokens.*

## Best Practices
- **Be conservative:** Only enable skills you absolutely need for the current task.
- After enabling a skill, its instructions will be available in `~/.gemini/config/skills/<skill-name>/SKILL.md`. You may need to read it via `view_file` to use the skill immediately since the system prompt might not update mid-conversation.
