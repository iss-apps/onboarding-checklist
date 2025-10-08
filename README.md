# ISS Onboarding Checklists

This repository contains interactive onboarding checklists for the International School of Stavanger (ISS). The checklists are automatically built from Markdown files and deployed to GitHub Pages.

## Features

- 📝 **Markdown-based**: Edit `staff-onboarding.md` or `student-onboarding.md` to update checklists
- 🚀 **Automatic deployment**: Changes are automatically built and deployed via GitHub Actions
- 📱 **Responsive design**: Works on desktop and mobile devices
- ✅ **Interactive checklists**: Click items to mark them complete
- 🎉 **Progress tracking**: Visual progress bar and completion celebration
- 🎨 **Modern UI**: Clean, professional design matching ISS branding

## Quick Start

1. **Edit a checklist**: Modify `staff-onboarding.md` or `student-onboarding.md`
2. **Commit changes**: Push to the `main` branch
3. **Automatic deployment**: GitHub Actions will build and deploy to GitHub Pages

## File Structure

```
├── staff-onboarding.md      # Staff onboarding checklist (Markdown)
├── student-onboarding.md    # Student onboarding checklist (Markdown)
├── doc/
│   ├── template.html        # HTML template for checklists
│   └── logo.png            # ISS logo (base64 encoded in HTML)
├── tools/
│   └── build.py            # Python build script
├── dist/                   # Generated HTML files (auto-created)
│   ├── staff.html          # Staff checklist
│   └── student.html        # Student checklist
└── .github/workflows/
    └── deploy.yml          # GitHub Actions CI/CD pipeline
```

## Setting Up GitHub Pages

### 1. Enable GitHub Pages

1. Go to your repository **Settings**
2. Scroll down to **Pages** section
3. Under **Source**, select **GitHub Actions**
4. The workflow will automatically deploy when you push to `main`

### 2. Repository Permissions

The workflow requires these permissions (already configured in `.github/workflows/deploy.yml`):
- `contents: read` - Read repository contents
- `pages: write` - Deploy to GitHub Pages
- `id-token: write` - Generate deployment tokens

### 3. First Deployment

1. Push your changes to the `main` branch
2. Go to **Actions** tab to watch the deployment
3. Once complete, your site will be available at:
   `https://yourusername.github.io/your-repo-name`

## Local Development

### Prerequisites

- Python 3.11+ (or any Python 3.x)
- No additional dependencies required

### Building Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/onboarding-checklist.git
cd onboarding-checklist

# Build the checklists
python3 tools/build.py

# Open in browser (choose staff or student)
open dist/staff.html
```

### Testing Changes

1. Edit `staff-onboarding.md` or `student-onboarding.md`
2. Run `python3 tools/build.py`
3. Open `dist/staff.html` or `dist/student.html` in your browser
4. Commit and push changes to trigger automatic deployment

## Customizing Checklists

### Markdown Format

Each checklist file uses this format:

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

### Template Customization

Edit `doc/template.html` to modify:
- Colors and styling
- Layout and structure
- JavaScript functionality
- Progress tracking features

### Logo

Replace `doc/logo.png` with your school's logo. The build script will automatically encode it as base64 for embedding in the HTML.

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically:

1. **Triggers** on changes to:
   - `staff-onboarding.md`
   - `student-onboarding.md`
   - `doc/template.html`
   - `doc/logo.png`
   - `tools/build.py`

2. **Builds** the checklists using Python
3. **Deploys** to GitHub Pages
4. **Creates** an index page for easy navigation

## Troubleshooting

### Build Failures

- Check that all required files exist (`staff-onboarding.md`, `student-onboarding.md`, `doc/template.html`, `doc/logo.png`)
- Verify Markdown syntax in checklist files
- Check GitHub Actions logs for detailed error messages

### GitHub Pages Not Updating

- Ensure GitHub Pages is enabled in repository settings
- Check that the source is set to "GitHub Actions"
- Verify the workflow has the correct permissions
- Wait a few minutes for changes to propagate

### Local Build Issues

- Ensure you're using Python 3.x
- Check file paths and permissions
- Verify all required files are present

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `python3 tools/build.py`
5. Submit a pull request

## License

This project is for internal use by the International School of Stavanger.
