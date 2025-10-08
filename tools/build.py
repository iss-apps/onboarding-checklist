#!/usr/bin/env python3
"""
Build script for onboarding checklists.
Parses staff-onboarding.md and student-onboarding.md and generates staff.html and student.html from template.html
"""

import os
import re
import base64
import subprocess
from pathlib import Path

def parse_markdown_file(file_path):
    """Parse markdown file and extract frontmatter and content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not frontmatter_match:
        raise ValueError("No frontmatter found in markdown file")
    
    frontmatter_text = frontmatter_match.group(1)
    frontmatter = {}
    
    # Parse frontmatter key-value pairs
    for line in frontmatter_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"')
    
    # Extract content after frontmatter
    content_start = frontmatter_match.end()
    markdown_content = content[content_start:].strip()
    
    return frontmatter, markdown_content

def encode_logo_to_base64(logo_path):
    """Encode logo image to base64 string."""
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    return base64.b64encode(logo_data).decode('utf-8')

def convert_markdown_to_html(text):
    """Convert markdown formatting to HTML."""
    # Convert bold markdown to HTML
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Convert links markdown to HTML
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    return text

def parse_checklist_items(markdown_content):
    """Parse checklist items from markdown content."""
    items = []
    
    # Split content into lines and process
    lines = markdown_content.split('\n')
    current_item = None
    
    for line in lines:
        # Don't strip the line yet - we need to preserve indentation
        if not line.strip():
            continue
            
        # Check if this is a main checklist item (starts with - [ ])
        if line.startswith('- [ ]'):
            # Save previous item if exists
            if current_item:
                items.append(current_item)
            
            # Start new item
            item_text = line[5:].strip()  # Remove '- [ ]' prefix
            # Convert markdown to HTML
            item_text = convert_markdown_to_html(item_text)
            current_item = {
                'text': item_text,
                'sub_items': []
            }
        elif line.startswith('  -') and current_item:
            # This is a sub-item (indented with 2 spaces)
            sub_item_text = line[3:].strip()  # Remove '  -' prefix
            # Convert markdown to HTML
            sub_item_text = convert_markdown_to_html(sub_item_text)
            current_item['sub_items'].append(sub_item_text)
    
    # Add the last item
    if current_item:
        items.append(current_item)
    
    return items

def generate_checklist_html(items):
    """Generate HTML for checklist items using the provided template."""
    html_parts = []
    
    for i, item in enumerate(items, 1):
        # Start checklist item div
        html_parts.append(f'<div class="checklist-item" data-step="{i}">')
        html_parts.append('    <div class="checkbox"></div>')
        html_parts.append('    <div class="item-content">')
        html_parts.append(f'        <div class="item-text">{item["text"]}</div>')
        
        # Add sub-items
        for sub_item in item['sub_items']:
            html_parts.append(f'        <div class="sub-item">{sub_item}</div>')
        
        # Close item-content and checklist-item divs
        html_parts.append('    </div>')
        html_parts.append('</div>')
    
    return '\n'.join(html_parts)

def fill_template(template_path, frontmatter, checklist_html, logo_base64):
    """Fill template with extracted data."""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace template variables
    template = template.replace('{{title}}', frontmatter.get('title', ''))
    template = template.replace('{{subtitle}}', frontmatter.get('subtitle', ''))
    template = template.replace('{{description}}', frontmatter.get('description', ''))
    template = template.replace('{{LogoBase64}}', logo_base64)
    template = template.replace('{{content}}', checklist_html)
    
    return template

def lint_html(html_content):
    """Lint HTML content using tidy if available."""
    try:
        # Try to use tidy for HTML linting
        process = subprocess.run(
            ['tidy', '-q', '-asxhtml', '--show-warnings', 'no'],
            input=html_content,
            text=True,
            capture_output=True,
            check=True
        )
        return process.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If tidy is not available or fails, return original content
        print("    Warning: HTML tidy not available, skipping linting")
        return html_content



def build_checklist(markdown_file, output_file, template_html, logo_png):
    """Build a single checklist from markdown file."""
    print(f"  Processing {markdown_file.name}...")
    
    # Parse markdown file
    print("    Parsing markdown...")
    frontmatter, markdown_content = parse_markdown_file(markdown_file)
    print(f"      Found frontmatter: {list(frontmatter.keys())}")
    
    # Encode logo
    print("    Encoding logo...")
    logo_base64 = encode_logo_to_base64(logo_png)
    print(f"      Logo encoded ({len(logo_base64)} characters)")
    
    # Parse checklist items
    print("    Parsing checklist items...")
    items = parse_checklist_items(markdown_content)
    print(f"      Found {len(items)} checklist items")
    
    # Generate checklist HTML
    print("    Generating checklist HTML...")
    checklist_html = generate_checklist_html(items)
    
    # Fill template
    print("    Filling template...")
    final_html = fill_template(template_html, frontmatter, checklist_html, logo_base64)
    
    # Lint HTML
    print("    Linting HTML...")
    final_html = lint_html(final_html)
    
    # Write HTML output
    print(f"    Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    return final_html

def main():
    """Main build function."""
    try:
        # Define paths
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        staff_md = project_root / 'staff-onboarding.md'
        student_md = project_root / 'student-onboarding.md'
        template_html = project_root / 'doc' / 'template.html'
        logo_png = project_root / 'doc' / 'logo.png'
        dist_dir = project_root / 'dist'
        staff_output = dist_dir / 'staff.html'
        student_output = dist_dir / 'student.html'
        
        # Validate input files exist
        required_files = [staff_md, student_md, template_html, logo_png]
        for file_path in required_files:
            if not file_path.exists():
                raise FileNotFoundError(f"Required file not found: {file_path}")
        
        # Ensure dist directory exists
        dist_dir.mkdir(exist_ok=True)
        
        print("Building onboarding checklists...")
        
        # Build staff checklist
        print("Building staff checklist...")
        build_checklist(staff_md, staff_output, template_html, logo_png)
        
        # Build student checklist
        print("Building student checklist...")
        build_checklist(student_md, student_output, template_html, logo_png)
        
        print("Build complete! ✅")
        print(f"Output files:")
        print(f"  - {staff_output}")
        print(f"  - {student_output}")
        
    except Exception as e:
        print(f"Build failed: {e}")
        exit(1)

if __name__ == '__main__':
    main()
