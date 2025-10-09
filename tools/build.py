#!/usr/bin/env python3
"""
Build script for onboarding checklists.
Parses staff-onboarding.md and student-onboarding.md and generates staff.html and student.html from template.html
"""

import os
import re
import base64
import subprocess
import shutil
from pathlib import Path
from PIL import Image

# Configuration flag - set to False to copy logo file instead of embedding as base64
BASE64_LOGO = False

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

def generate_logo_sizes(logo_path, assets_dir):
    """Generate different sized logos from the source logo."""
    print("    Generating logo sizes...")
    
    # Define the sizes we need for PWA manifests
    sizes = [
        (32, 32),
        (96, 96), 
        (192, 192),
        (512, 512)
    ]
    
    try:
        # Open the source image
        with Image.open(logo_path) as img:
            # Convert to RGBA if not already (for transparency support)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            generated_files = []
            
            for width, height in sizes:
                # Resize image maintaining aspect ratio and quality
                resized = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Save to assets directory
                filename = f"logo-{width}x{height}.png"
                output_path = assets_dir / filename
                resized.save(output_path, 'PNG', optimize=True)
                generated_files.append(filename)
                print(f"      Generated {filename}")
            
            return generated_files
            
    except Exception as e:
        print(f"      Error generating logo sizes: {e}")
        return []

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

def fill_template(template_path, frontmatter, checklist_html, logo_data, manifest_path):
    """Fill template with extracted data."""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace template variables
    template = template.replace('{{title}}', frontmatter.get('title', ''))
    template = template.replace('{{subtitle}}', frontmatter.get('subtitle', ''))
    template = template.replace('{{description}}', frontmatter.get('description', ''))
    template = template.replace('{{logo}}', logo_data)
    template = template.replace('{{content}}', checklist_html)
    template = template.replace('{{manifest}}', manifest_path)
    
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



def build_checklist(markdown_file, output_file, template_html, logo_png, dist_dir, assets_dir, manifest_path):
    """Build a single checklist from markdown file."""
    print(f"  Processing {markdown_file.name}...")
    
    # Parse markdown file
    print("    Parsing markdown...")
    frontmatter, markdown_content = parse_markdown_file(markdown_file)
    print(f"      Found frontmatter: {list(frontmatter.keys())}")
    
    # Handle logo based on configuration
    if BASE64_LOGO:
        print("    Encoding logo to base64...")
        logo_data = encode_logo_to_base64(logo_png)
        print(f"      Logo encoded ({len(logo_data)} characters)")
    else:
        print("    Copying logo file...")
        logo_dest = assets_dir / 'logo-lg.png'
        shutil.copy2(logo_png, logo_dest)
        logo_data = 'assets/logo-lg.png'  # Use relative path
        print(f"      Logo copied to {logo_dest}")
    
    # Parse checklist items
    print("    Parsing checklist items...")
    items = parse_checklist_items(markdown_content)
    print(f"      Found {len(items)} checklist items")
    
    # Generate checklist HTML
    print("    Generating checklist HTML...")
    checklist_html = generate_checklist_html(items)
    
    # Fill template
    print("    Filling template...")
    final_html = fill_template(template_html, frontmatter, checklist_html, logo_data, manifest_path)
    
    # Lint HTML
    print("    Linting HTML...")
    final_html = lint_html(final_html)
    
    # Write HTML output
    print(f"    Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    return final_html

def load_manifest_template(template_path):
    """Load manifest template from JSON file."""
    import json
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_simplified_manifest(name, short_name, start_url, template_path):
    """Create a simplified PWA manifest using template."""
    template = load_manifest_template(template_path)
    
    # Replace template variables
    manifest = template.copy()
    manifest["name"] = name
    manifest["short_name"] = short_name
    manifest["start_url"] = start_url
    manifest["scope"] = start_url
    
    return manifest

def main():
    """Main build function."""
    try:
        # Define paths
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        staff_md = project_root / 'staff-onboarding.md'
        student_md = project_root / 'student-onboarding.md'
        template_html = project_root / 'doc' / 'template.html'
        template_json = project_root / 'doc' / 'template.json'
        logo_png = project_root / 'doc' / 'logo.png'
        dist_dir = project_root / 'dist'
        assets_dir = dist_dir / 'assets'
        staff_output = dist_dir / 'staff.html'
        student_output = dist_dir / 'student.html'
        
        # Validate input files exist
        required_files = [staff_md, student_md, template_html, template_json, logo_png]
        for file_path in required_files:
            if not file_path.exists():
                raise FileNotFoundError(f"Required file not found: {file_path}")
        
        # Clean and ensure directories exist
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        dist_dir.mkdir(exist_ok=True)
        assets_dir.mkdir(exist_ok=True)
        
        print("Building onboarding checklists...")
        
        # Generate logo sizes
        print("Generating logo assets...")
        generate_logo_sizes(logo_png, assets_dir)
        
        # Build staff checklist
        print("Building staff checklist...")
        build_checklist(staff_md, staff_output, template_html, logo_png, dist_dir, assets_dir, 'staff-manifest.json')
        
        # Build student checklist
        print("Building student checklist...")
        build_checklist(student_md, student_output, template_html, logo_png, dist_dir, assets_dir, 'student-manifest.json')
        
        # Create simplified manifests
        print("Creating PWA manifests...")
        
        # Staff manifest
        staff_manifest = create_simplified_manifest(
            "ISS Staff Onboarding Checklist",
            "ISS Staff",
            "staff.html",
            template_json
        )
        
        with open(dist_dir / 'staff-manifest.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(staff_manifest, f, indent=2)
        
        # Student manifest
        student_manifest = create_simplified_manifest(
            "ISS Student Onboarding Checklist", 
            "ISS Student",
            "student.html",
            template_json
        )
        
        with open(dist_dir / 'student-manifest.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(student_manifest, f, indent=2)
        
        print("Build complete! ✅")
        print(f"Output files:")
        print(f"  - {staff_output}")
        print(f"  - {student_output}")
        print(f"  - {dist_dir / 'staff-manifest.json'}")
        print(f"  - {dist_dir / 'student-manifest.json'}")
        print(f"  - Logo assets in {assets_dir}")
        
    except Exception as e:
        print(f"Build failed: {e}")
        exit(1)

if __name__ == '__main__':
    main()
