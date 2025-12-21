"""
═══════════════════════════════════════════════════════════════════
　　　　　　　　　Ｆ Ｏ Ｎ Ｔ 　Ｃ Ａ Ｔ Ａ Ｌ Ｏ Ｇ Ｅ Ｒ　　　　　　　　
═══════════════════════════════════════════════════════════════════

　░▒▓█  ＴＡＧ　ＰＡＬＥＴＴＥ  █▓▒░

　geometric • formal • handwritten • fatface • monospaced • techno
　pixel • medieval • art nouveau • blobby • distressed • wood
　wacky • shaded • marker • futuristic • vintage • calm • playful
　sophisticated • business • stiff • childlike • horror • distorted
　clean • warm • aesthetic • brutalist • modular • neutral
　contemporary • rounded • approachable • humanist • coding
　retro • android

═══════════════════════════════════════════════════════════════════
　Ａｕｔｈｏｒ：　Duygu Dağdelen
　Ｄａｔｅ：　　December 2024
═══════════════════════════════════════════════════════════════════
"""

import json
import requests
from getpass import getpass
from base64 import b64encode, b64decode
import io
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os

# Check running environment
try:
    from google.colab import ai
    COLAB_AI_AVAILABLE = True
except ImportError:
    COLAB_AI_AVAILABLE = False
    # Fallback to Gemini API
    try:
        import google.generativeai as genai
        GEMINI_AVAILABLE = True
    except ImportError:
        GEMINI_AVAILABLE = False
        print("⚠  No AI available. Install: pip install google-generativeai pillow")


class CompactJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indent_level = 0
        
    def encode(self, obj):
        if isinstance(obj, list):
            return '[' + ','.join(json.dumps(item) for item in obj) + ']'
        return super().encode(obj)
    
    def iterencode(self, obj, _one_shot=False):
        if isinstance(obj, dict):
            yield '{\n'
            self.indent_level += 1
            items = list(obj.items())
            for i, (key, value) in enumerate(items):
                yield ' ' * (self.indent_level * 2)
                yield json.dumps(key) + ': '
                if isinstance(value, list):
                    yield '[' + ','.join(json.dumps(item) for item in value) + ']'
                elif isinstance(value, dict):
                    for chunk in self.iterencode(value):
                        yield chunk
                else:
                    yield json.dumps(value)
                if i < len(items) - 1:
                    yield ','
                yield '\n'
            self.indent_level -= 1
            yield ' ' * (self.indent_level * 2) + '}'
        elif isinstance(obj, list):
            yield '[\n'
            self.indent_level += 1
            for i, item in enumerate(obj):
                yield ' ' * (self.indent_level * 2)
                if isinstance(item, dict):
                    for chunk in self.iterencode(item):
                        yield chunk
                else:
                    yield json.dumps(item)
                if i < len(obj) - 1:
                    yield ','
                yield '\n'
            self.indent_level -= 1
            yield ' ' * (self.indent_level * 2) + ']'
        else:
            yield json.dumps(obj)


def format_catalog_json(catalog_data):
    result = '[\n'
    for i, font in enumerate(catalog_data):
        result += '  {\n'
        result += f'    "name": {json.dumps(font["name"])},\n'
        result += f'    "source": {json.dumps(font["source"])},\n'
        result += f'    "url": {json.dumps(font["url"])},\n'
        result += f'    "category": {json.dumps(font["category"])},\n'
        result += f'    "tags": [{",".join(json.dumps(tag) for tag in font["tags"])}]\n'
        result += '  }'
        if i < len(catalog_data) - 1:
            result += ','
        result += '\n'
    result += ']'
    return result


class FontCatalogManager:
    def __init__(self, token, repo_owner, repo_name, file_path="catalog.fonts.json", 
                 branch="main", use_ai=True, gemini_api_key=None):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.file_path = file_path
        self.branch = branch
        self.use_ai = use_ai
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Initialize based on environment
        if self.use_ai:
            if COLAB_AI_AVAILABLE:
                print("✓ Using Colab AI")
                self.ai_type = "colab"
                self.model = None
            elif GEMINI_AVAILABLE and gemini_api_key:
                print("✓ Using Gemini API")
                genai.configure(api_key=gemini_api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.ai_type = "gemini"
            else:
                print("🗿  AI not available")
                self.ai_type = None
                self.model = None
        else:
            self.ai_type = None
            self.model = None
    
    def get_current_catalog(self):
        """Fetch the current catalog from repository"""
        response = requests.get(self.api_url, headers=self.headers, params={"ref": self.branch})
        
        if response.status_code == 200:
            content = response.json()
            file_content = b64decode(content["content"]).decode("utf-8")
            return json.loads(file_content), content["sha"]
        elif response.status_code == 404:
            print("⚠  File not found. Will create new file.")
            return [], None
        else:
            raise Exception(f"Failed to fetch file: {response.status_code} - {response.text}")
    
    def update_catalog(self, catalog_data, sha, commit_message):
        formatted_json = format_catalog_json(catalog_data)
        content_bytes = formatted_json.encode("utf-8")
        content_b64 = b64encode(content_bytes).decode("utf-8")
        
        payload = {
            "message": commit_message,
            "content": content_b64,
            "branch": self.branch
        }
        
        if sha:
            payload["sha"] = sha
        
        response = requests.put(self.api_url, headers=self.headers, json=payload)
        
        if response.status_code in [200, 201]:
            print("☑️ Catalog updated successfully!")
            return True
        else:
            raise Exception(f"Failed to update file: {response.status_code} - {response.text}")
    
    def generate_font_specimen(self, name, source, url):
        """Generate a font specimen image for visual analysis"""
        try:
            # Download font file
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            # Save temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ttf') as tmp:
                tmp.write(response.content)
                tmp_path = tmp.name
            
            # Create specimen image
            img = Image.new('RGB', (800, 400), color='white')
            draw = ImageDraw.Draw(img)
            
            try:
                # Try to load the font
                font_large = ImageFont.truetype(tmp_path, 72)
                font_medium = ImageFont.truetype(tmp_path, 48)
                font_small = ImageFont.truetype(tmp_path, 32)
            except:
                # If font loading fails, return None
                os.unlink(tmp_path)
                return None
            
            # Draw text specimens
            draw.text((20, 20), "AaBbCc 123", fill='black', font=font_large)
            draw.text((20, 120), "The quick brown fox", fill='black', font=font_medium)
            draw.text((20, 180), "jumps over the lazy dog", fill='black', font=font_medium)
            draw.text((20, 250), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", fill='black', font=font_small)
            draw.text((20, 300), "abcdefghijklmnopqrstuvwxyz", fill='black', font=font_small)
            draw.text((20, 350), "0123456789 !@#$%^&*()", fill='black', font=font_small)
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            return img
            
        except Exception as e:
            print(f"　　　⚠  Could not generate specimen: {e}")
            return None
    
    def get_google_font_specimen(self, font_name):
        """Try to get Google Fonts specimen image"""
        try:
            # Google Fonts specimen
            specimen_url = f"https://fonts.gstatic.com/s/{font_name.lower().replace(' ', '')}/v1/specimen.png"
            
            response = requests.get(specimen_url, timeout=5)
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
            
            return None
        except:
            return None
    
    def analyze_font_with_colab_ai(self, name, source, url, category, specimen_img=None):
        """Use Colab AI for visual analysis"""
        try:
            prompt_base = """Analyze this font and describe its VISUAL aesthetic characteristics.

Look at the actual letterforms and identify 3-5 precise aesthetic tags based on what you SEE:

VISUAL STRUCTURE:
- Is it geometric (precise circles/squares) or organic (flowing curves)?
- Is it modular (built from repeated shapes) or varied?
- Is it monospaced (equal character width) or proportional?
- Are terminals rounded, sharp, or squared?

STYLE & MOOD:
- Does it look retro (70s/80s), futuristic, contemporary, or vintage?
- Is it playful, serious, calm, energetic, sophisticated?
- Does it feel warm (friendly curves) or cold (technical angles)?

SPECIAL CHARACTERISTICS:
- Brutalist (raw, harsh), clean (minimal), distressed (worn)?
- Handwritten, pixel-art, medieval, art nouveau style?
- Formal/business or casual/playful?
- Any unique traits: blobby, wacky, horror, stiff, etc.?

Reference tags (use these as inspiration but create your own if needed):
geometric, formal, handwritten, fatface, monospaced, techno, pixel, medieval, art nouveau, blobby, distressed, wood, wacky, shaded, marker, futuristic, vintage, calm, playful, sophisticated, business, stiff, childlike, horror, distorted, clean, warm, aesthetic, brutalist, modular, neutral, contemporary, rounded, approachable, humanist, coding, retro, android

Return ONLY 3-5 tags as a comma-separated list based on VISUAL APPEARANCE, no explanation.
Example: geometric, brutalist, contemporary, clean, modular"""

            if specimen_img:
                prompt = f"""Font Name: {name}
Category: {category}
Source: {source}

A visual specimen of this font is available showing letterforms.

{prompt_base}"""
            else:
                prompt = f"""Based on this font metadata, infer its likely VISUAL aesthetic:

Font Name: {name}
Source: {source}
Category: {category}

{prompt_base}"""
            
            # Call Colab AI (no model parameter needed)
            response = ai.generate_text(prompt=prompt)
            
            # Parse response
            tags_text = response.strip().replace('*', '').replace('`', '').replace('"', '')
            suggested_tags = [tag.strip().lower() for tag in tags_text.split(',') if tag.strip()]
            
            return suggested_tags[:5]
            
        except Exception as e:
            print(f"　　　🤷‍♀️ Oops, Colab AI error: {e}")
            return []
    
    def analyze_font_with_gemini(self, name, source, url, category, specimen_img=None):
        """Use Gemini API for visual analysis"""
        try:
            prompt_base = """Analyze this font and describe its VISUAL aesthetic characteristics.

Look at the actual letterforms and identify 3-5 precise aesthetic tags based on what you SEE:

VISUAL STRUCTURE:
- Is it geometric (precise circles/squares) or organic (flowing curves)?
- Is it modular (built from repeated shapes) or varied?
- Is it monospaced (equal character width) or proportional?
- Are terminals rounded, sharp, or squared?

STYLE & MOOD:
- Does it look retro (70s/80s), futuristic, contemporary, or vintage?
- Is it playful, serious, calm, energetic, sophisticated?
- Does it feel warm (friendly curves) or cold (technical angles)?

SPECIAL CHARACTERISTICS:
- Brutalist (raw, harsh), clean (minimal), distressed (worn)?
- Handwritten, pixel-art, medieval, art nouveau style?
- Formal/business or casual/playful?
- Any unique traits: blobby, wacky, horror, stiff, etc.?

Reference tags (use these as inspiration but create your own if needed):
geometric, formal, handwritten, fatface, monospaced, techno, pixel, medieval, art nouveau, blobby, distressed, wood, wacky, shaded, marker, futuristic, vintage, calm, playful, sophisticated, business, stiff, childlike, horror, distorted, clean, warm, aesthetic, brutalist, modular, neutral, contemporary, rounded, approachable, humanist, coding, retro, android

Return ONLY 3-5 tags as a comma-separated list based on VISUAL APPEARANCE, no explanation.
Example: geometric, brutalist, contemporary, clean, modular"""

            if specimen_img:
                response = self.model.generate_content([prompt_base, specimen_img])
            else:
                prompt = f"""Based on this font metadata, infer its likely VISUAL aesthetic:

Font Name: {name}
Source: {source}
Category: {category}

{prompt_base}"""
                response = self.model.generate_content(prompt)
            
            tags_text = response.text.strip().replace('*', '').replace('`', '').replace('"', '')
            suggested_tags = [tag.strip().lower() for tag in tags_text.split(',') if tag.strip()]
            
            return suggested_tags[:5]
            
        except Exception as e:
            print(f"　　　🤷‍♀️ Oops, Gemini API error: {e}")
            return []
    
    def analyze_font_visually(self, name, source, url, category):
        """Use AI to visually analyze font appearance"""
        if not self.ai_type:
            return []
        
        try:
            # Try to get font specimen image
            specimen_img = None
            
            if source == "google":
                print("　　　📡 Fetching Google Fonts specimen...")
                specimen_img = self.get_google_font_specimen(name)
            
            if not specimen_img and url:
                print("　　　📡 Generating font specimen from URL...")
                specimen_img = self.generate_font_specimen(name, source, url)
            
            # Analyze based on type
            if self.ai_type == "colab":
                return self.analyze_font_with_colab_ai(name, source, url, category, specimen_img)
            elif self.ai_type == "gemini":
                return self.analyze_font_with_gemini(name, source, url, category, specimen_img)
            
        except Exception as e:
            print(f"　　　🤷‍♀️ Oops, AI analysis error: {e}")
            return []
    
    def add_font_interactive(self, font_number=None):
        """Interactive prompt to add a new font"""
        header = "░▒▓█  ＡＤＤＩＮＧ　ＦＯＮＴ  █▓▒░"
        if font_number:
            header = f"░▒▓█  ＡＤＤＩＮＧ　ＦＯＮＴ　＃{font_number}  █▓▒░"
        
        print("\n" + "═" * 67)
        print(header)
        print("═" * 67)
        
        # Get font details
        print("\n　━━━ ＦＯＮＴ ＮＡＭＥ ━━━")
        name = input("　　　＞ ").strip()
        
        print("\n　━━━ ＳＯＵＲＣＥ ━━━")
        print("　　　（google • custom • other）")
        source = input("　　　＞ ").strip().lower()
        
        print("\n　━━━ ＵＲＬ ━━━")
        url = input("　　　＞ ").strip()
        
        print("\n　━━━ ＣＡＴＥＧＯＲＹ ━━━")
        print("　　　（sans-serif • serif • monospace • display • handwriting）")
        category = input("　　　＞ ").strip().lower()
        
        # AI-powered tag suggestion
        print("\n　━━━ ＴＡＧＳ ━━━")
        suggested_tags = []
        
        if self.ai_type:
            print("　　　🌀 Analyzing font visual aesthetics...")
            suggested_tags = self.analyze_font_visually(name, source, url, category)
            
            if suggested_tags:
                print(f"　　　👾 𝙰𝙸 𝚂𝚄𝙶𝙶𝙴𝚂𝚃𝙴𝙳 𝚃𝙰𝙶𝚂: {', '.join(suggested_tags)}")
                print("\n　　　ＯＰＴＩＯＮＳ：")
                print("　　　 • Press Enter to accept ALL")
                print("　　　 • Type tag numbers to keep (e.g., 1,3,5)")
                print("　　　 • Type your own tags (comma-separated)")
                
                # Display numbered tags
                print("\n　　　🏷️ ＳＵＧＧＥＳＴＥＤ　ＴＡＧＳ：")
                for i, tag in enumerate(suggested_tags, 1):
                    print(f"　　　　{i}. {tag}")
                
                tags_input = input("\n　　　＞ ").strip()
                
                if not tags_input:
                    # Accept all
                    tags = suggested_tags
                    print(f"　　　📜 Using all AI suggestions: {', '.join(tags)}")
                elif tags_input.replace(',', '').replace(' ', '').isdigit():
                    # Tag numbers selected
                    try:
                        selected_indices = [int(x.strip()) for x in tags_input.split(',')]
                        tags = [suggested_tags[i-1] for i in selected_indices if 1 <= i <= len(suggested_tags)]
                        print(f"　　　📜 Selected tags: {', '.join(tags)}")
                    except (ValueError, IndexError):
                        print("　　　⚠  Invalid selection, using all suggestions")
                        tags = suggested_tags
                else:
                    # Custom tags entered
                    tags = [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()]
                    print(f"　　　📜 Using custom tags: {', '.join(tags)}")
            else:
                print("　　　（Enter comma-separated tags）")
                tags_input = input("　　　＞ ").strip()
                tags = [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()]
        else:
            print("　　　（Enter comma-separated tags, e.g., geometric,neutral,modern）")
            tags_input = input("　　　＞ ").strip()
            tags = [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()]
        
        # Create new font entry
        new_font = {
            "name": name,
            "source": source,
            "url": url,
            "category": category,
            "tags": tags
        }
        
        print("\n" + "═" * 67)
        print("░▒▓█  ＰＲＥＶＩＥＷ  █▓▒░")
        print("═" * 67)
        preview_json = format_catalog_json([new_font])
        # Remove outer array brackets for single item preview
        preview_lines = preview_json.split('\n')[1:-1]
        print('\n'.join(preview_lines))
        print("═" * 67)
        
        confirm = input("\n　🔘 ＣＯＮＦＩＲＭ？ (yes/no)： ").strip().lower()
        
        if confirm in ['yes', 'y']:
            return new_font
        else:
            print("❌ Cancelled.")
            return None
    
    def run_batch_mode(self):
        """Batch mode to add multiple fonts"""
        try:
            # Fetch current catalog
            print("\n📡 Fetching current catalog...")
            catalog, sha = self.get_current_catalog()
            print(f"✓ Found {len(catalog)} existing fonts")
            
            new_fonts = []
            font_count = 1
            
            while True:
                # Add font
                new_font = self.add_font_interactive(font_number=font_count)
                
                if new_font:
                    # Check for duplicates
                    if any(font["name"] == new_font["name"] for font in catalog + new_fonts):
                        print(f"\n⚠  Font '{new_font['name']}' already exists!")
                        overwrite = input("　🔘 ＯＶＥＲＷＲＩＴＥ？ (yes/no)： ").strip().lower()
                        if overwrite in ['yes', 'y']:
                            # Remove from catalog if exists
                            catalog = [f for f in catalog if f["name"] != new_font["name"]]
                            # Remove from new_fonts if exists
                            new_fonts = [f for f in new_fonts if f["name"] != new_font["name"]]
                            new_fonts.append(new_font)
                            print(f"✓ Font '{new_font['name']}' added to batch")
                        else:
                            print("⊗ Font skipped.")
                    else:
                        new_fonts.append(new_font)
                        print(f"✓ Font '{new_font['name']}' added to batch")
                    
                    font_count += 1
                
                # Ask if user wants to add more
                print("\n" + "─" * 67)
                add_more = input("　➕ Add another font？(yes/no)：").strip().lower()
                
                if add_more not in ['yes', 'y']:
                    break
            
            # Final confirmation and commit
            if new_fonts:
                print("\n" + "═" * 67)
                print(f"░▒▓█  ＢＡＴＣＨ　ＳＵＭＭＡＲＹ：{len(new_fonts)} fonts ready  █▓▒░")
                print("═" * 67)
                
                for i, font in enumerate(new_fonts, 1):
                    print(f"\n　{i}. {font['name']}")
                    print(f"　　　Source: {font['source']}")
                    print(f"　　　Category: {font['category']}")
                    print(f"　　　Tags: {', '.join(font['tags'])}")
                
                print("\n" + "═" * 67)
                final_confirm = input(f"\n　🔘 Commit　all　{len(new_fonts)} fonts？(yes/no)：").strip().lower()
                
                if final_confirm in ['yes', 'y']:
                    # Add all fonts to catalog
                    catalog.extend(new_fonts)
                    
                    # Create commit message
                    if len(new_fonts) == 1:
                        commit_msg = f"Add {new_fonts[0]['name']} to font catalog"
                    else:
                        font_names = ', '.join([f['name'] for f in new_fonts[:3]])
                        if len(new_fonts) > 3:
                            commit_msg = f"Add {len(new_fonts)} fonts ({font_names}, ...)"
                        else:
                            commit_msg = f"Add {len(new_fonts)} fonts ({font_names})"
                    
                    print(f"\n🌀 Committing to catalog...")
                    self.update_catalog(catalog, sha, commit_msg)
                    print(f"╰┈➤ 🎊 Successfully added {len(new_fonts)} font(s) to catalog!")
                else:
                    print("❌ Batch cancelled.")
            else:
                print("\n⊗ No fonts to commit.")
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def run_single_mode(self):
        """Single font addition mode"""
        try:
            # Fetch current catalog
            print("\n📡 Fetching current catalog...")
            catalog, sha = self.get_current_catalog()
            print(f"✓ Found {len(catalog)} existing fonts")
            
            # Add new font interactively
            new_font = self.add_font_interactive()
            
            if new_font:
                # Check for duplicates
                if any(font["name"] == new_font["name"] for font in catalog):
                    print(f"\n⚠  Font '{new_font['name']}' already exists!")
                    overwrite = input("　🔘 ＯＶＥＲＷＲＩＴＥ？ (yes/no)： ").strip().lower()
                    if overwrite in ['yes', 'y']:
                        catalog = [f for f in catalog if f["name"] != new_font["name"]]
                    else:
                        print("❌ Cancelled.")
                        return
                
                # Add to catalog
                catalog.append(new_font)
                commit_msg = f"Add {new_font['name']} to font catalog"
                print(f"\n🌀 Committing to catalog...")
                self.update_catalog(catalog, sha, commit_msg)
                print(f"╰┈➤ 🎊 Successfully added '{new_font['name']}' to catalog!")
                
        except Exception as e:
            print(f"✗ Error: {e}")


def main():
    print("\n" + "═" * 67)
    print("░▒▓█  ＦＯＮＴ　ＣＡＴＡＬＯＧ　ＭＡＮＡＧＥＲ  █▓▒░")
    print("═" * 67)
    
    # Get credentials
    token = getpass("\n🗝 GitHub Access Token：")
    
    # Get repository in format username/repo-name
    while True:
        repo_full = input("\n🗄 Select repository (username/repo-name)： ").strip()
        if "/" in repo_full:
            repo_owner, repo_name = repo_full.split("/", 1)
            repo_owner = repo_owner.strip()
            repo_name = repo_name.strip()
            if repo_owner and repo_name:
                break
        print("　✗ Invalid format. Use: username/repo-name")
    
    # Optional: custom file path and branch
    file_path = input("\n🗃 Select file [default=catalog.fonts.json]:").strip() or "catalog.fonts.json"
    branch = input("🪜 Branch [default=main]:").strip() or "main"
    
    # AI configuration
    use_ai = True
    gemini_key = None
    
    if COLAB_AI_AVAILABLE:
        use_ai_input = input("\n👾 Use AI visual analysis? (yes/no)：").strip().lower()
        use_ai = use_ai_input in ['yes', 'y', '']
    elif GEMINI_AVAILABLE:
        use_ai_input = input("\n👾 Use AI visual analysis？(yes/no)：").strip().lower()
        if use_ai_input in ['yes', 'y']:
            gemini_key = getpass("🗝　Gemini API Key：")
            use_ai = True
        else:
            use_ai = False
    else:
        use_ai = False
    
    # Create manager
    manager = FontCatalogManager(token, repo_owner, repo_name, file_path, branch, use_ai, gemini_key)
    
    # Choose mode
    print("\n" + "═" * 67)
    print("░▒▓█  ＳＥＬＥＣＴ　ＭＯＤＥ  █▓▒░")
    print("═" * 67)
    print("\n　1. Single font (add one font)")
    print("　2. Batch mode (add multiple fonts)")
    
    mode_choice = input("\n🎚 ＭＯＤＥ　(1/2)： ").strip()
    
    if mode_choice == "2":
        manager.run_batch_mode()
    else:
        manager.run_single_mode()


if __name__ == "__main__":
    main()
