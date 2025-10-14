# ISS Onboarding Checklists

Interactive onboarding checklists for the International School of Stavanger (ISS). 

## 🚀 Live Checklists

- **[Staff Checklist](https://iss-apps.github.io/onboarding-checklist/staff/)** - Staff onboarding checklist
- **[Student Checklist](https://iss-apps.github.io/onboarding-checklist/student/)** - Student onboarding checklist

## ✨ Features

- 📝 **Markdown-based**: Edit `staff.md` or `student.md` to update checklists
- 🚀 **Automatic deployment**: GitHub Actions automatically builds and deploys changes
- 📱 **Responsive design**: Works on desktop and mobile devices
- ✅ **Interactive checklists**: Click items to mark them complete
- 🎉 **Progress tracking**: Visual progress bar and completion celebration
- 🎨 **Modern UI**: Clean, professional design matching ISS branding

## 🛠️ How to Update

1. **Edit a checklist**: Modify `staff.md` or `student.md`
2. **Commit changes**: Push to the `main` branch
3. **Automatic deployment**: GitHub Actions will build and deploy to GitHub Pages

That's it! Your changes will be live within minutes.

## 📁 Project Structure

```
├── staff.md                    # Staff onboarding checklist
├── student.md                  # Student onboarding checklist
├── template/
│   ├── template.html           # HTML template
│   └── template.json           # PWA manifest template
├── img/
│   └── logo.png               # ISS logo
├── tools/
│   └── build.py               # Build script
└── dist/                      # Generated files (auto-created)
    ├── staff/
    │   ├── index.html
    │   └── manifest.json
    └── student/
        ├── index.html
        └── manifest.json
```

## 🔧 Local Development

```bash
# Build locally
python3 tools/build.py

# Open in browser
open dist/staff/index.html
open dist/student/index.html
```

## 📝 Markdown Format

Each checklist uses this format:

```markdown
---
title: "Your Title"
subtitle: "Your Subtitle"
description: "Your description"
---

- [ ] **Main checklist item**
  - Sub-item with instructions
  - Another sub-item

- [ ] **Another main item**
  - More detailed instructions
```

## 🤖 GitHub Actions

The workflow automatically:
- Triggers on changes to markdown files, templates, or build script
- Builds the checklists using Python
- Deploys to GitHub Pages
- Creates PWA manifests for mobile installation

## 📄 License

This project is for internal use by the International School of Stavanger.